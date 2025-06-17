# accounts/utils.py

import random
import string

def generate_otp(length=5):
    characters = string.ascii_uppercase + string.digits  # A-Z and 0-9
    otp = ''.join(random.choices(characters, k=length))
    return otp
