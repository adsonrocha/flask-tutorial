import hashlib
import os


def length(f):
    f.seek(0, os.SEEK_END)
    file_length = f.tell()
    return file_length


def md5(f):
    """Get the md5 of a file's contents"""
    f.seek(0)
    file_md5 = hashlib.md5()
    chunk_size = 2 ** 10

    for bytes_chunk in iter(lambda: f.read(chunk_size), b''):
        file_md5.update(bytes_chunk)

    return file_md5.hexdigest()
