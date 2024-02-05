

def error_message_log(name_file, message):
    return {
        "file": name_file,
        "message": message
    }

def error_message(tipo, message, url, fields_errors=None):
    return {
            "tipo": tipo,
            "message": message,
            "field_errors": fields_errors,
            "url": url
        }

def successfull_message(tipo, message, url, data):
    return {
            "tipo": tipo,
            "message": message,
            "url": url,
            "data": data,
    }