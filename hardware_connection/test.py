eol = '''{
    "code": "Success",
    "message": {
        "code": "12345678",
        "nfc_id": "12345678"
    }
}'''
msg=eval(eol)
print(msg["message"]["code"])