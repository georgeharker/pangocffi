import ctypes.util
import os
import warnings
from typing import List


# Attempt api mode if installed
api_mode = True
if ('PANGOCFFI_API_MODE' in os.environ and
        int(os.environ['PANGOCFFI_API_MODE']) == 0):
    # Allow explicit disable of api_mode
    api_mode = False

if api_mode:
    try:
        from _pangocffi import ffi
        from _pangocffi import lib as pango
        gobject = pango
        glib = pango
        api_mode = True
    except ImportError:
        api_mode = False

# Fall back to non api mode
if not api_mode:
    def _dlopen(dl_name: str, generated_ffi, names: List[str]):
        """
        :param dl_name:
            The name of the dynamic library. This is also used to determine the
            environment variable name to lookup. For example, if dl_name is "glib",
            this function will attempt to load "GLIB_LOCATION".
        :param generated_ffi:
            The FFI for pango/gobject/glib, generated by pangocffi.
        :param names:
            An array of library names commonly used across different platforms.
        :return:
            A FFILibrary instance for the library.
        """

        # Try environment locations if set
        env_location = os.getenv(f'{dl_name.upper()}_LOCATION')
        if env_location:
            names.append(env_location)
            try:
                return generated_ffi.dlopen(env_location)
            except OSError:
                warnings.warn(f"dlopen() failed to load {dl_name} library:"
                              f" '{env_location}'. Falling back.")

        # Try various names for the same library, for different platforms.
        for name in names:
            for lib_name in (name, 'lib' + name):
                try:
                    path = ctypes.util.find_library(lib_name)
                    lib = generated_ffi.dlopen(path or lib_name)
                    if lib:
                        return lib
                except OSError:
                    pass
        raise OSError(
            f"dlopen() failed to load {dl_name} library: {' / '.join(names)}"
        )

    from .ffi_build import ffi  # noqa

    pango = _dlopen('pango', ffi, ['pango', 'pango-1', 'pango-1.0', 'pango-1.0-0'])
    gobject = _dlopen('gobject', ffi, ['gobject-2.0', 'gobject-2.0-0'])
    glib = _dlopen('glib', ffi, ['glib-2.0', 'glib-2.0-0'])

# Imports are normally always put at the top of the file.
# But the wrapper API requires that the pango library be loaded first.
# Therefore, we have to disable linting rules for these lines.
from .version import *  # noqa
from .enums import *  # noqa
from .convert import *  # noqa
from .pango_object import PangoObject  # noqa
from .language import Language  # noqa
from .font_metrics import FontMetrics  # noqa
from .font import Font  # noqa
from .font_description import FontDescription  # noqa
from .rectangle import Rectangle  # noqa
from .item import Item  # noqa
from .context import Context  # noqa
from .glyph_item import GlyphItem  # noqa
from .glyph_item_iter import GlyphItemIter  # noqa
from .attribute import Attribute  # noqa
from .attr_list import AttrList  # noqa
from .tab_array import TabArray # noqa
from .layout_run import LayoutRun  # noqa
from .layout_iter import LayoutIter  # noqa
from .layout import Layout  # noqa
from .color import Color  # noqa
