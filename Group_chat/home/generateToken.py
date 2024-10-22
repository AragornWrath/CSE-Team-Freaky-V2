import string
import random

def generateToken() :
    val = ""
    validChars = string.ascii_letters
    for letter in range(15) :
        val += random.choice(validChars)
    
    return val