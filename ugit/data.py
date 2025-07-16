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

def update_ref(ref, value, deref=True):
    ref = _get_ref_internal(ref, deref)[0]

    assert value.value
    if value.symbolic:
        value = f'ref: {value.value}'
    else:
        value = value.value

    ref_path = f'{GIT_DIR}/{ref}'
    os.makedirs(os.path.dirname(ref_path), exist_ok=True)
    with open(ref_path, 'w') as f:
        f.write(value)

#
def get_ref (ref, deref=True):
    return _get_ref_internal (ref, deref)[1]

# Given ref name, return oid
def _get_ref_internal(ref, deref):
    ref_path = f'{GIT_DIR}/{ref}'
    value = None
    if os.path.isfile(ref_path):
        with open(ref_path) as f:
            value = f.read().strip()

    symbolic = bool(value) and value.startswith('ref:')
    if symbolic:
        value = value.split(':', 1)[1].strip()
        # If this ref pointing to another ref, Recursively go to the next ref
        if deref:
            return _get_ref_internal(value, deref=True)

    return ref, RefValue (symbolic=symbolic, value=value)

def iter_refs(prefix='', deref=True):
    refs = ['HEAD']
    for root, _, filenames in os.walk(f'{GIT_DIR}/refs/'):
        root = os.path.relpath(root, GIT_DIR)
        refs.extend(f'{root}/{name}' for name in filenames)

    for refname in refs:
        if not refname.startswith(prefix):
            continue
        yield refname, get_ref(refname, deref=deref)

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