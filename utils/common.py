# coding=utf-8

import hashlib
import random
from string import digits


def is_null(*args, **kwargs):
    if args:
        for _ in args:
            print(_)
            if _:
                return True

    if kwargs:
        for _ in kwargs:
            print(_)
            if kwargs[_]:
                return True

    return False


def get_random_md5(length=16, ret_plain=False):
    plain = ''.join([random.choice(digits) for _ in range(length)])
    m = hashlib.md5()
    m.update(bytes(plain, 'utf-8'))
    cipher = m.hexdigest() if hex else m.hexdigest()
    if ret_plain:
        return [plain, cipher]
    else:
        return cipher
