import uuid 
import random
import string


def generate_ref_code():
    letters = string.ascii_lowercase
    code= ''.join(random.choice(letters) for i in range(6))
    return code
