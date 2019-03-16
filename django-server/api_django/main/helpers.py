import datetime
import hashlib


def create_hash(model_object):
    now = datetime.datetime.now()
    secure_hash = hashlib.md5()
    secure_hash.update(
        f'{now}:{model_object}'.encode(
            'utf-8'))

    return secure_hash.hexdigest()