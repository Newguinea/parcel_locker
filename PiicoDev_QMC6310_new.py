# Class and methods for the QMC6310 3-axis magnetometer.
# Written by Peter Johnston and Michael Ruppe at Core Electronics

# 2022 MAR 17 - Initial release
# 2022 APR 27 - Add initialisation parameters 'sign_z', 'sign_y', 'sign_z'.  Changed default sign to match silk screen. Updated the readPolar method to match the inversion of the Y axis.

import math
from PiicoDev_Unified import *

compat_str = '\nUnified PiicoDev library out of date.  Get the latest module: https://piico.dev/unified \n'

_I2C_ADDRESS = 0x1C
# Registers
_ADDRESS_XOUT = 0x01
_ADDRESS_YOUT = 0x03
_ADDRESS_ZOUT = 0x05
_ADDRESS_STATUS = 0x09
_ADDRESS_CONTROL1 = 0x0A
_ADDRESS_CONTROL2 = 0x0B
_ADDRESS_SIGN = 0x29
_BIT_MODE = 0
_BIT_ODR = 2
_BIT_OSR1 = 4
_BIT_OSR2 = 6
_BIT_RANGE = 2

def _readBit(x, n):
    return x & 1 << n != 0

def _setBit(x, n):
    return x | (1 << n)

def _clearBit(x, n):
    return x & ~(1 << n)

def _writeBit(x, n, b):
    if b == 0:
        return _clearBit(x, n)
    else:
        return _setBit(x, n)

def _writeCrumb(x, n, c):
    x = _writeBit(x, n, _readBit(c, 0))
    return _writeBit(x, n+1, _readBit(c, 1))

class PiicoDev_QMC6310(object):
    range_gauss = {3000:1e-3, 1200:4e-4, 800:2.6666667e-4, 200:6.6666667e-5} # Maps the range (key) to sensitivity (lsb/gauss)
    range_microtesla = {3000:1e-1, 1200:4e-2, 800:2.6666667e-2, 200:6.6666667e-3} # Maps the range (key) to sensitivity (lsb/microtesla)
    def __init__(self, bus=None, freq=None, sda=None, scl=None, addr=_I2C_ADDRESS, odr=3, osr1=0, osr2=3, range=3000, sign_x=0, sign_y=1, sign_z=1, calibrationFile='calibration.cal', suppress_warnings=False):
        try:
            if compat_ind >= 1:
                pass
            else:
                print(compat_str)
        except:
            print(compat_str)
        self.i2c = create_unified_i2c(bus=bus, freq=freq, sda=sda, scl=scl)
        self.addr = addr
        self.odr = odr
        self.calibrationFile = calibrationFile
        self.suppress_warnings = suppress_warnings
        self._CR1 = 0x00
        self._CR2 = 0x00
        sign = sign_x + sign_y*2 + sign_z*4
        try:
            self._setMode(1)
            self.setOutputDataRate(odr)
            self.setOverSamplingRatio(osr1)
            self.setOverSamplingRate(osr2)
            self.setRange(range)
            self._setSign(sign)
        except Exception as e:
            print(i2c_err_str.format(self.addr))
            raise e
        self.x_offset = 0
        self.y_offset = 0
        self.z_offset = 0
        self.declination = 0
        self.data = {}
        self._dataValid = False
        if calibrationFile is not None:
            self.loadCalibration()
        sleep_ms(5)
    
    def _setMode(self, mode):
        self._CR1 = _writeCrumb(self._CR1, _BIT_MODE, mode)
        self.i2c.writeto_mem(self.addr, _ADDRESS_CONTROL1, bytes([self._CR1]))

    def setOutputDataRate(self, odr):
        self._CR1 = _writeCrumb(self._CR1, _BIT_ODR, odr)
        self.i2c.writeto_mem(self.addr, _ADDRESS_CONTROL1, bytes([self._CR1]))

    def setOverSamplingRatio(self, osr1):
        self._CR1 = _writeCrumb(self._CR1, _BIT_OSR1, osr1)
        self.i2c.writeto_mem(self.addr, _ADDRESS_CONTROL1, bytes([self._CR1]))

    def setOverSamplingRate(self, osr2):
        self._CR1 = _writeCrumb(self._CR1, _BIT_OSR2, osr2)
        self.i2c.writeto_mem(self.addr, _ADDRESS_CONTROL1, bytes([self._CR1]))

    def setRange(self, range):
        assert range in [3000,1200,800,200], "range must be 200,800,1200,3000 (uTesla)"
        r={3000:0, 1200:1, 800:2, 200:3}
        self.sensitivity=self.range_microtesla[range]
        self._CR2 = _writeCrumb(self._CR2, _BIT_RANGE, r[range])
        self.i2c.writeto_mem(self.addr, _ADDRESS_CONTROL2, bytes([self._CR2]))

    def _setSign(self, sign):
        self.i2c.writeto_mem(self.addr, _ADDRESS_SIGN, bytes([sign]))

    def _convertAngleToPositive(self, angle):
        if angle >= 360.0:
            angle = angle - 360.0
        if angle < 0:
            angle = angle + 360.0
        return angle
    
    def _getControlRegisters(self):
        return self.i2c.readfrom_mem(self.addr, _ADDRESS_CONTROL1, 2)
            
    def _getStatusReady(self, status):
        return _readBit(status, 0)
        
    def _getStatusOverflow(self, status):
        return _readBit(status, 1)
    
    def read(self, raw=False):
        self._dataValid = False
        NaN = {'x':float('NaN'),'y':float('NaN'),'z':float('NaN')}
        try:
            status = int.from_bytes(self.i2c.readfrom_mem(self.addr, _ADDRESS_STATUS, 1), 'big')
        except:
            print(i2c_err_str.format(self.addr))
            self.sample = NaN
            return NaN
        if self._getStatusReady(status) is True:
            try:
                x = int.from_bytes(self.i2c.readfrom_mem(self.addr, _ADDRESS_XOUT, 2), 'little')
                y = int.from_bytes(self.i2c.readfrom_mem(self.addr, _ADDRESS_YOUT, 2), 'little')
                z = int.from_bytes(self.i2c.readfrom_mem(self.addr, _ADDRESS_ZOUT, 2), 'little')
            except:
                print(i2c_err_str.format(self.addr))
                self.sample = NaN
                return self.sample
            if self._getStatusOverflow(status) is True:
#                 print('Overflow')
                return NaN
            if (x >= 0x8000):
                x = -((65535 - x) + 1)
            x = (x - self.x_offset)
            if (y >= 0x8000):
                y = -((65535 - y) + 1)
            y = (y - self.y_offset)
            if (z >= 0x8000):
                z = -((65535 - z) + 1)
            z = (z - self.z_offset)
            if raw is False:
                x *= self.sensitivity
                y *= self.sensitivity
                z *= self.sensitivity
            self.sample = {'x':x,'y':y,'z':z}
            self._dataValid = True
            return self.sample
        else:
            print('Not Ready')
            self.sample = NaN
            return self.sample
    
    def dataValid(self):
        return self._dataValid
    
    def readPolar(self):
        cartesian = self.read()
        angle = ( math.atan2(cartesian['x'],-cartesian['y']) /math.pi)*180.0 + self.declination
        angle = self._convertAngleToPositive(angle)
        magnitude = math.sqrt(cartesian['x']*cartesian['x'] + cartesian['y']*cartesian['y'] + cartesian['z']*cartesian['z'])
        return {'polar':angle, 'Gauss':magnitude*100, 'uT':magnitude}
    
    def readMagnitude(self):
        return self.readPolar()['uT']
    
    def readHeading(self):
        return self.readPolar()['polar']
    
    def setDeclination(self, dec):
        self.declination = dec
    
    def calibrate(self, enable_logging=False):
        try:
            self.setOutputDataRate(3)
        except Exception as e:
            print(i2c_err_str.format(self.addr))
            raise e
        x_min = 65535
        x_max = -65535
        y_min = 65535
        y_max = -65535
        z_min = 65535
        z_max = -65535
        log = ''
        print('*** Calibrating.\n    Slowly rotate your sensor until the bar is full')
        print('[          ]', end='')
        range = 1000
        i = 0
        x=0;y=0;z=0;
        a=0.5 # EMA filter weight
        while i < range:
            i += 1
            sleep_ms(5)
            d = self.read(raw=True)
            x = a*d['x'] + (1-a)*x # EMA filter
            y = a*d['y'] + (1-a)*y
            z = a*d['z'] + (1-a)*z
            if x < x_min: x_min = x; i=0
            if x > x_max: x_max = x; i=0
            if y < y_min: y_min = y; i=0
            if y > y_max: y_max = y; i=0
            if z < z_min: z_min = z; i=0
            if z > z_max: z_max = z; i=0
            j = round(10*i/range);
            print( '\015[' + int(j)*'*' + int(10-j)*' ' + ']', end='') # print a progress bar
            if enable_logging:
                log = log + (str(d['x']) + ',' + str(d['y']) + ',' + str(d['z']) + '\n')
        self.setOutputDataRate(self.odr) # set the output data rate back to the user selected rate
        self.x_offset = (x_max + x_min) / 2
        self.y_offset = (y_max + y_min) / 2
        self.z_offset = (z_max + z_min) / 2
        f = open(self.calibrationFile, "w")
        f.write('x_min:\n' + str(x_min) + '\nx_max:\n' + str(x_max) + '\ny_min:\n' + str(y_min) + '\ny_max:\n' + str(y_max) + '\nz_min\n' + str(z_min) + '\nz_max:\n' + str(z_max) + '\nx_offset:\n')
        f.write(str(self.x_offset) + '\ny_offset:\n' + str(self.y_offset) + '\nz_offset:\n' + str(self.z_offset))
        f.close()
        if enable_logging:
            flog = open("calibration.log", "w")
            flog.write(log)
            flog.close

    def loadCalibration(self):
        try:
            f = open(self.calibrationFile, "r")
            for i in range(13): f.readline()
            self.x_offset = float(f.readline())
            f.readline()
            self.y_offset = float(f.readline())
            f.readline()
            self.z_offset = float(f.readline())
            sleep_ms(5)
        except:
            if not self.suppress_warnings:
                print("No calibration file found. Run 'calibrate()' for best results.  Visit https://piico.dev/p15 for more info.")
            sleep_ms(1000)
