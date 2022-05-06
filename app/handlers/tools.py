import random
import string

def random_string(length):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for i in range(length))