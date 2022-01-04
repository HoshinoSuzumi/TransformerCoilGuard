from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import ctypes
import platform
import sys
import threading

import six
from numpy.ctypeslib import ndpointer

from artdaq.errors import Error


class DaqNotFoundError(Error):
    pass


class DaqFunctionNotSupportedError(Error):
    pass


class InvalidHandleError(Error):
    pass


class c_bool32(ctypes.c_uint):
    """
    Specifies a custom ctypes data type to represent 32-bit booleans.
    """

    def _getter(self):
        return bool(ctypes.c_uint.value.__get__(self))

    def _setter(self, val):
        ctypes.c_uint.value.__set__(self, int(val))

    value = property(_getter, _setter)

    del _getter, _setter


class CtypesByteString(object):
    """
    Custom argtype that automatically converts unicode strings to ASCII
    strings in Python 3.
    """
    def from_param(self, param):
        if isinstance(param, six.text_type):
            param = param.encode('ascii')
        return ctypes.c_char_p(param)


ctypes_byte_str = CtypesByteString()


def wrapped_ndpointer(*args, **kwargs):
    """
    Specifies an ndpointer type that wraps numpy.ctypeslib.ndpointer and
    allows a value of None to be passed to an argument of that type.

    Taken from http://stackoverflow.com/questions/32120178
    """
    if sys.version_info < (3,):
        if 'flags' in kwargs:
            kwargs['flags'] = tuple(
                f.encode('ascii') for f in kwargs['flags'])

    base = ndpointer(*args, **kwargs)

    def from_param(cls, obj):
        if obj is None:
            return obj
        return base.from_param(obj)

    return type(base.__name__, (base,),
                {'from_param': classmethod(from_param)})


def enum_bitfield_to_list(bitfield_value, bitfield_enum_type,
                          actual_enum_type):
    """
    Converts a bitfield value to a list of enums.

    Args:
        bitfield_value (int): Specifies the value of the bitfield.
        bitfield_enum_type (enum.Enum): Specifies the bitfield enum type
            from which to mask and extract the enum values.
        actual_enum_type (enum.Enum): Specifies the actual enum type.
    Returns:
        List[enum.Enum]: Indicates the converted list of enums.
    """
    supported_values = []
    for bitfield_mask in bitfield_enum_type:
        if bitfield_value & bitfield_mask.value:
            enum_value = next(
                e for e in actual_enum_type if e.name == bitfield_mask.name)
            supported_values.append(enum_value)

    return supported_values


def enum_list_to_bitfield(enum_list, bitfield_enum_type):
    """
    Converts a list of enums to a bitfield value.

    Args:
        enum_list (List[enum.Enum]): Specifies the list of enums.
        bitfield_enum_type (enum.Enum): Specifies the bitfield enum type
            from which to mask and extract the enum values.
    Returns:
        int: Indicates the value of the bitfield.
    """
    bitfield_value = 0
    for enum_value in enum_list:
        bitfield_mask = next(
            b for b in bitfield_enum_type if b.name == enum_value.name)
        bitfield_value |= bitfield_mask.value

    return bitfield_value


class DaqFunctionImporter(object):
    """
    Wraps the function getter function of a ctypes library.

    Allows the Art_DAQ Python API to fail elegantly if a function is not
    supported in the current version of the API.
    """

    def __init__(self, library):
        self._library = library
        self._lib_lock = threading.Lock()

    def __getattr__(self, function):
        try:
            cfunc = getattr(self._library, function)
            if not hasattr(cfunc, 'arglock'):
                with self._lib_lock:
                    if not hasattr(cfunc, 'arglock'):
                        cfunc.arglock = threading.Lock()
            return cfunc
        except AttributeError:
            raise DaqFunctionNotSupportedError(
                'The Art_DAQ function "{0}" is not supported in this '
                'version of Art_DAQ. Visit ni.com/downloads to upgrade your '
                'version of Art_DAQ.'.format(function))


class DaqLibImporter(object):
    """
    Encapsulates Art_DAQ library importing and handle type parsing logic.
    """

    def __init__(self):
        self._windll = None
        self._cdll = None
        self._cal_handle = None
        self._task_handle = None

    @property
    def windll(self):
        if self._windll is None:
            self._import_lib()
        return self._windll

    # @property
    # def cdll(self):
    #     if self._cdll is None:
    #         self._import_lib()
    #     return self._cdll

    @property
    def task_handle(self):
        if self._task_handle is None:
            self._parse_typedefs()
        return self._task_handle

    @property
    def cal_handle(self):
        if self._cal_handle is None:
            self._parse_typedefs()
        return self._cal_handle

    def _import_lib(self):
        """
        Determines the location of and loads the Art_DAQ CAI DLL.
        """

        if sys.platform.startswith('win') or sys.platform.startswith('cli'):
            lib_name = "Art_DAQ"

            if sys.version_info < (3,):
                lib_name = lib_name.encode('ascii')

            if 'iron' in platform.python_implementation().lower():
                windll = ctypes.windll.Art_DAQ

            else:
                windll = ctypes.windll.LoadLibrary(lib_name)

        else:
            raise DaqNotFoundError(
                'Art_DAQ Python is not supported on this platform: {0}. '
                'Please direct any questions or feedback to National '
                'Instruments.'.format(sys.platform))

        self._windll = DaqFunctionImporter(windll)

    def _parse_typedefs(self):
        self._task_handle = ctypes.c_void_p
        self._cal_handle = ctypes.c_uint


lib_importer = DaqLibImporter()
