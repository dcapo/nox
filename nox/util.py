import string
import random

class Util:
    @staticmethod
    def random_filename(size=10, chars=string.ascii_lowercase + string.digits):
        return ''.join(random.choice(chars) for x in range(size))