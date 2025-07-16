import hashlib
import os

from collections import namedtuple

GIT_DIR = '.ugit'

def init ():
    if os.path.exists(GIT_DIR):
        print("Error: Repository already exists.")
        return
    os.makedirs (GIT_DIR)
    os.makedirs(os.path.join(GIT_DIR, "objects"))

RefValue = namedtuple ('RefValue', ['symbolic', 'value'])

def update_ref(ref, value):
    assert not value.symbolic
    ref = _get_ref_internal(ref)[0]
    ref_path = f'{GIT_DIR}/{ref}'
    os.makedirs(os.path.dirname(ref_path), exist_ok=True)
    with open(ref_path, 'w') as f:
        f.write(value.value)

def get_ref(ref):
    return _get_ref_internal (ref)[1]

def _get_ref_internal(ref):
    ref_path = f'{GIT_DIR}/{ref}'
    value = None
    if os.path.isfile(ref_path):
        with open(ref_path) as f:
            value = f.read().strip()

    symbolic = bool(value) and value.startswith('ref:')
    if symbolic:
        value = value.split(':', 1)[1].strip()
        return _get_ref_internal(value)
    return ref, RefValue(symbolic=False, value=value)

def iter_refs ():
    refs = ['HEAD']
    for root, _, filenames in os.walk(f'{GIT_DIR}/refs/'):
        root = os.path.relpath(root, GIT_DIR)
        refs.extend(f'{root}/{name}' for name in filenames)

    for refname in refs:
        yield refname, get_ref(refname)

# data is a content of a file
def hash_object (data, type_='blob'):
    obj = type_.encode() + b'\x00' + data
    oid = hashlib.sha1 (obj).hexdigest ()
    with open (f'{GIT_DIR}/objects/{oid}', 'wb') as out:
        out.write (obj)
    return oid

def get_object (oid, expected='blob'):
    with open (f'{GIT_DIR}/objects/{oid}', 'rb') as f:
        obj = f.read ()
    type_, _, content = obj.partition(b'\x00')
    type_ = type_.decode()

    if expected is not None:
        assert type_ == expected, f'Expected {expected}, got {type_}'
    return content