"""rot13 cipher"""

def rot13(text):
    """rot 13 cipher"""
    rot = ""
    if text:
        for char in text:
            code = ord(char)
            if code >= 65 and code <= 90:
                code = 65 + ((code - 65 + 13) % 26)
                char = chr(code)
            elif code >= 97 and code <= 122:
                code = 97 + ((code - 97 + 13) % 26)
                char = chr(code)

            rot += char
    
    return rot
