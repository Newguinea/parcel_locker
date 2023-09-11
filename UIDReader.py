#!/usr/bin/env python3
import threading
import signal
import sys
import os
from ctypes import cdll, Structure, Union, POINTER, pointer, byref, \
    c_char, c_int, c_uint8, c_size_t, c_void_p, c_uint32, c_char_p

nfc = cdll.LoadLibrary("/usr/lib/arm-linux-gnueabihf/libnfc.so")

# ------------- /usr/include/nfc/nfc-types.h ------------------------------------

# incomplete structures


class nfc_context(Structure):
    _pack_ = 1


class nfc_device(Structure):
    _pack_ = 1


class nfc_driver(Structure):
    _pack_ = 1


# connstring
nfc_connstring = c_char * 1024

# nfc_property enum
nfc_property = c_int
NP_TIMEOUT_COMMAND = 0
NP_TIMEOUT_ATR = NP_TIMEOUT_COMMAND + 1
NP_TIMEOUT_COM = NP_TIMEOUT_ATR + 1
NP_HANDLE_CRC = NP_TIMEOUT_COM + 1
NP_HANDLE_PARITY = NP_HANDLE_CRC + 1
NP_ACTIVATE_FIELD = NP_HANDLE_PARITY + 1
NP_ACTIVATE_CRYPTO1 = NP_ACTIVATE_FIELD + 1
NP_INFINITE_SELECT = NP_ACTIVATE_CRYPTO1 + 1
NP_ACCEPT_INVALID_FRAMES = NP_INFINITE_SELECT + 1
NP_ACCEPT_MULTIPLE_FRAMES = NP_ACCEPT_INVALID_FRAMES + 1
NP_AUTO_ISO14443_4 = NP_ACCEPT_MULTIPLE_FRAMES + 1
NP_EASY_FRAMING = NP_AUTO_ISO14443_4 + 1
NP_FORCE_ISO14443_A = NP_EASY_FRAMING + 1
NP_FORCE_ISO14443_B = NP_FORCE_ISO14443_A + 1
NP_FORCE_SPEED_106 = NP_FORCE_ISO14443_B + 1

# nfc_dep_mode enum
nfc_dep_mode = c_int
NDM_UNDEFINED = 0
NDM_PASSIVE = NDM_UNDEFINED
NDM_ACTIVE = NDM_PASSIVE

# nfc_baud_rate enum
nfc_baud_rate = c_int
NBR_UNDEFINED = 0
NBR_106 = NBR_UNDEFINED + 1
NBR_212 = NBR_106 + 1
NBR_424 = NBR_212 + 1
NBR_847 = NBR_424 + 1

# nfc_modulation_type enum
nfc_modulation_type = c_int
NMT_ISO14443A = 1
NMT_JEWEL = NMT_ISO14443A
NMT_ISO14443B = NMT_JEWEL
NMT_ISO14443BI = NMT_ISO14443B
NMT_ISO14443B2SR = NMT_ISO14443BI
NMT_ISO14443B2CT = NMT_ISO14443B2SR
NMT_FELICA = NMT_ISO14443B2CT
NMT_DEP = NMT_FELICA

# nfc_mode enum
nfc_mode = c_int
N_TARGET = 0
N_INITIATOR = N_TARGET + 1

# structures and unions: note that _pack_ is necessary


class nfc_dep_info(Structure):
    _pack_ = 1
    _fields_ = [
        ("abtNFCID3", c_uint8 * 10),
        ("btDID",  c_uint8),
        ("btBS", c_uint8),
        ("btBR", c_uint8),
        ("btTO", c_uint8),
        ("btPP", c_uint8),
        ("abtGB", c_uint8 * 48),
        ("szGB", c_size_t),
        ('ndm', nfc_dep_mode)]


class nfc_iso14443a_info(Structure):
    _pack_ = 1
    _fields_ = [
        ("abtAtqa", c_uint8 * 2),
        ("btSak", c_uint8),
        ("szUidLen", c_size_t),
        ("abtUid", c_uint8 * 10),
        ("szAtsLen", c_size_t),
        ("abtAts", c_uint8 * 254)]


class nfc_felica_info(Structure):
    _pack_ = 1
    _fields_ = [
        ("szLen", c_size_t),
        ("btResCode", c_uint8),
        ("abtId", c_uint8 * 8),
        ("abtPad", c_uint8 * 8),
        ("abtSysCode", c_uint8 * 2)]


class nfc_iso14443b_info(Structure):
    _pack_ = 1
    _fields_ = [
        ("abtPupi", c_uint8 * 4),
        ("abtApplicationData", c_uint8 * 4),
        ("abtProtocolInfo", c_uint8 * 3),
        ("ui8CardIdentifier", c_uint8)]


class nfc_iso14443bi_info(Structure):
    _pack_ = 1
    _fields_ = [
        ("abtDIV", c_uint8 * 4),
        ("btVerLog", c_uint8),
        ("btConfig", c_uint8),
        ("szAtrLen", c_size_t),
        ("abtAtr", c_uint8 * 33)]


class nfc_iso14443b2sr_info(Structure):
    _pack_ = 1
    _fields_ = [
        ("abtUID", c_uint8 * 8)]


class nfc_iso14443b2ct_info(Structure):
    _pack_ = 1
    _fields_ = [
        ("abtUID", c_uint8 * 4),
        ("btProdCode", c_uint8),
        ("btFabCode", c_uint8)]


class nfc_jewel_info(Structure):
    _pack_ = 1
    _fields_ = [
        ("btSensRes", c_uint8 * 2),
        ("btId", c_uint8 * 4)]


class nfc_target_info(Union):
    _pack_ = 1
    _fields_ = [
        ("nai", nfc_iso14443a_info),
        ("nfi", nfc_felica_info),
        ("nbi", nfc_iso14443b_info),
        ("nii", nfc_iso14443bi_info),
        ("nsi", nfc_iso14443b2sr_info),
        ("nci", nfc_iso14443b2ct_info),
        ("nji", nfc_jewel_info),
        ("ndi", nfc_dep_info)]


class nfc_modulation(Structure):
    _pack_ = 1
    _fields_ = [
        ('nmt', nfc_modulation_type),
        ('nbr', nfc_baud_rate)]


class nfc_target(Structure):
    _pack_ = 1
    _fields_ = [
        ('nti', nfc_target_info),
        ('nm', nfc_modulation)]


# ------------- /usr/include/nfc/nfc.h ------------------------------------------
# definitions
NFC_SUCCESS = 0
NFC_EIO = -1
NFC_EINVARG = -2
NFC_EDEVNOTSUPP = -3
NFC_ENOTSUCHDEV = -4
NFC_EOVFLOW = -5
NFC_ETIMEOUT = -6
NFC_EOPABORTED = -7
NFC_ENOTIMPL = -8
NFC_ETGRELEASED = -10
NFC_ERFTRANS = -20
NFC_EMFCAUTHFAIL = -30
NFC_ESOFT = -80
NFC_ECHIP = -90

# functions: note that not all functions are converted
# nfc_init
nfc_init = nfc.nfc_init
nfc_init.argtype = [POINTER(POINTER(nfc_context))]
nfc_init.restype = None

# nfc_exit
nfc_exit = nfc.nfc_exit
nfc_exit.argtype = [POINTER(nfc_context)]
nfc_exit.restype = None

# nfc_open
nfc_open = nfc.nfc_open
nfc_open.argtype = [POINTER(nfc_context), nfc_connstring]
nfc_open.restype = POINTER(nfc_device)

# nfc_close
nfc_close = nfc.nfc_close
nfc_close.argtype = [POINTER(nfc_device)]
nfc_close.restype = None

# nfc_abort_command
nfc_abort_command = nfc.nfc_abort_command
nfc_abort_command.argtype = [POINTER(nfc_device)]
nfc_abort_command.restype = c_int

# nfc_idle
nfc_idle = nfc.nfc_idle
nfc_idle.argtype = [POINTER(nfc_device)]
nfc_idle.restype = c_int

# nfc_initiator_init
nfc_initiator_init = nfc.nfc_initiator_init
nfc_initiator_init.argtype = [POINTER(nfc_device)]
nfc_initiator_init.restype = c_int

# nfc_initiator_init_secure_element
nfc_initiator_init_secure_element = nfc.nfc_initiator_init_secure_element
nfc_initiator_init_secure_element.argtype = [POINTER(nfc_device)]
nfc_initiator_init_secure_element.restype = c_int

# nfc_initiator_select_passive_target
nfc_initiator_select_passive_target = nfc.nfc_initiator_select_passive_target
nfc_initiator_select_passive_target.argtype = [POINTER(nfc_device),
                                               nfc_modulation, POINTER(c_uint8), c_size_t, POINTER(nfc_target)]
nfc_initiator_select_passive_target.restype = c_int

# nfc_initiator_list_passive_targets
nfc_initiator_list_passive_targets = nfc.nfc_initiator_list_passive_targets
nfc_initiator_list_passive_targets.argtype = [POINTER(nfc_device),
                                              nfc_modulation, POINTER(nfc_target), c_size_t]
nfc_initiator_list_passive_targets.restype = c_int

# nfc_initiator_poll_target
nfc_initiator_poll_target = nfc.nfc_initiator_poll_target
nfc_initiator_poll_target.argtype = [POINTER(nfc_device),
                                     POINTER(nfc_modulation), c_size_t, c_uint8, c_uint8, POINTER(nfc_target)]
nfc_initiator_poll_target.restype = c_int

# nfc_initiator_select_dep_target
nfc_initiator_select_dep_target = nfc.nfc_initiator_select_dep_target
nfc_initiator_select_dep_target.argtype = [POINTER(nfc_device), nfc_dep_mode,
                                           nfc_baud_rate, POINTER(nfc_dep_info), POINTER(nfc_target), c_int]
nfc_initiator_select_dep_target.restype = c_int

# nfc_initiator_poll_dep_target
nfc_initiator_poll_dep_target = nfc.nfc_initiator_poll_dep_target
nfc_initiator_poll_dep_target.argtype = [POINTER(nfc_device), nfc_dep_mode,
                                         nfc_baud_rate, POINTER(nfc_dep_info), POINTER(nfc_target), c_int]
nfc_initiator_poll_dep_target.restype = c_int

# nfc_initiator_deselect_target
nfc_initiator_deselect_target = nfc.nfc_initiator_deselect_target
nfc_initiator_deselect_target.argtype = [POINTER(nfc_device)]
nfc_initiator_deselect_target.restype = c_int

# nfc_initiator_transceive_bytes
nfc_initiator_transceive_bytes = nfc.nfc_initiator_transceive_bytes
nfc_initiator_transceive_bytes.argtype = [POINTER(nfc_device), POINTER(c_uint8),
                                          c_size_t, POINTER(c_uint8), c_size_t, c_int]
nfc_initiator_transceive_bytes.restype = c_int

# nfc_initiator_transceive_bytes_timed
nfc_initiator_transceive_bytes_timed = nfc.nfc_initiator_transceive_bytes_timed
nfc_initiator_transceive_bytes_timed.argtype = [POINTER(nfc_device),
                                                POINTER(c_uint8), c_size_t, POINTER(c_uint8), c_size_t, POINTER(c_uint32)]
nfc_initiator_transceive_bytes_timed.restype = c_int

# nfc_initiator_target_is_present
nfc_initiator_target_is_present = nfc.nfc_initiator_target_is_present
nfc_initiator_target_is_present.argtype = [POINTER(nfc_device),
                                           POINTER(nfc_target)]
nfc_initiator_target_is_present.restype = c_int

# nfc_target_init
nfc_target_init = nfc.nfc_target_init
nfc_target_init.argtype = [POINTER(nfc_device), POINTER(nfc_target),
                           POINTER(c_uint8), c_size_t, c_int]
nfc_target_init.restype = c_int

# nfc_target_send_bytes
nfc_target_send_bytes = nfc.nfc_target_send_bytes
nfc_target_send_bytes.argtype = [POINTER(nfc_device), POINTER(c_uint8),
                                 c_size_t, c_int]
nfc_target_send_bytes.restype = c_int

# nfc_target_receive_bytes
nfc_target_receive_bytes = nfc.nfc_target_receive_bytes
nfc_target_receive_bytes.argtype = [POINTER(nfc_device), POINTER(c_uint8),
                                    c_size_t, c_int]
nfc_target_receive_bytes.restype = c_int

# nfc_device_get_name
nfc_device_get_name = nfc.nfc_device_get_name
nfc_device_get_name.argtype = [POINTER(nfc_device)]
nfc_device_get_name.restype = c_char_p

# nfc_perror
nfc_perror = nfc.nfc_perror
nfc_perror.argtype = [POINTER(nfc_device), c_char_p]
nfc_perror.restype = None

# nfc_free
nfc_free = nfc.nfc_free
nfc_free.argtype = [c_void_p]
nfc_free.restype = None

# -------------------------------------------------------------------------------

gUID=0

def callBlock():
    nt = nfc_target()
    context = pointer(nfc_context())
    nfc_init(byref(context))
    if context is None:
        # print("Unable to init libnfc (malloc)")
        return 1

    pnd = nfc_open(context, None)
    if pnd is None:
        # print("Unable to open NFC device")
        nfc_exit(context)
        return 2

    if nfc_initiator_init(pnd) < 0:
        nfc_perror(pnd, "nfc_initiator_init")
        nfc_exit(context)
        return 3

    nmMifare = nfc_modulation()
    nmMifare.nmt = NMT_ISO14443A
    nmMifare.nbr = NBR_106
    if nfc_initiator_select_passive_target(pnd, nmMifare, None, 0, pointer(nt)) > 0:
        UID = "".join('{:02x}'.format(
            nt.nti.nai.abtUid[i]) for i in range(nt.nti.nai.szUidLen))
        nfc_close(pnd)
        nfc_exit(context)
        global gUID
        gUID=UID


def quit(signum, frame):
    # os.kill(os.getpid(), signal.SIGKILL)
    global gUID
    gUID=0
    exit()


def run():
    signal.signal(signal.SIGINT, quit)
    signal.signal(signal.SIGTERM, quit)
    a=threading.Thread(target=callBlock)
    a.setDaemon(True)
    a.start()
    a.join()
    return gUID


if __name__ == "__main__":
    run()
