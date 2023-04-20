import hashlib
from myprocess import settings


def md5(data_string):
    # salt = '234234'
    # obj = hashlib.md5(salt.encode('utf-8'))
    obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    obj.update(data_string.encode('utf-8'))
    return obj.hexdigest()
