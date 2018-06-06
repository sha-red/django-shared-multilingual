from __future__ import unicode_literals

__version__ = '0.1.1'

try:
    from ._version import __version__
except ImportError:
    pass

VERSION = __version__.split('+')
VERSION = tuple(list(map(int, VERSION[0].split('.'))) + VERSION[1:])
