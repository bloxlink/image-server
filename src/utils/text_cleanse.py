def cleanse(text):
    string_encode = text.encode("ascii", "ignore")
    string_decode = string_encode.decode()

    return string_decode
