import string
import random

def generateToken(length) :
    extras = "!@#$%^"
    val = ""
    validChars = string.ascii_letters + string.digits + extras
    for letter in range(length) :
        val += random.choice(validChars)
    
    return val