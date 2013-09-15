# -*- coding: utf-8 -*-

"""pyfs.py

Utility functions for determining disk usage, directory size, etc.
"""


import os


def recursive_glob(path, pattern='*'):
    import fnmatch
    
    path = os.path.normpath(path)
    for dirpath, _, filenames in os.walk(path):
        for f in filenames:
            if fnmatch.fnmatch(f, pattern):
                filename = os.path.join(dirpath, f)
                yield filename


def dir_size(path, recursive=True):
    if recursive:
        dir_size = 0
        for (dirpath, _, filenames) in os.walk(path):
            for f in filenames:
                dir_size += os.path.getsize(os.path.join(dirpath, f))
    else:
        dir_size = sum([os.path.getsize(os.path.join(path, f)) \
            for f in os.listdir(path) \
                if os.path.isfile(os.path.join(path, f))])

    return dir_size


def mount_point(path):
    path = os.path.abspath(path)
    while path != os.path.sep:
        if os.path.ismount(path):
            return path
        path = os.path.abspath(os.path.join(path, os.pardir))

    return path


def disk_usage(path):
    path = os.path.abspath(path)
    if hasattr(os, "statvfs"):
        import statvfs
        stats = os.statvfs(path)
        bytes_available = stats[statvfs.F_BSIZE] * stats[statvfs.F_BAVAIL]
        bytes_total = stats[statvfs.F_BSIZE] * stats[statvfs.F_BLOCKS]
        bytes_free = stats[statvfs.F_BSIZE] * stats[statvfs.F_BFREE]
        
    else:
        import ctypes
        bytes_available = ctypes.c_ulonglong(0)
        bytes_total = ctypes.c_ulonglong(0)
        bytes_free = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(u"%s" % path),
                                                   ctypes.pointer(bytes_available),
                                                   ctypes.pointer(bytes_total),
                                                   ctypes.pointer(bytes_free))

    return (bytes_available.value, bytes_total.value, bytes_free.value)
