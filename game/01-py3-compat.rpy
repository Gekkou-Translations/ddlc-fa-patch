# Copyright (c) yorkyang2333
# The following code is borrowed from
# https://github.com/yorkyang2333/ddlc-renpy8

# Python 3 compatibility shim for DDLC (originally built with Ren'Py 6.x / Python 2)
# The game code calls renpy.file() which in store context is renpy.exports.file().
# In Ren'Py 8 (Python 3), this returns bytes. We wrap it to return str for text files.

init -990 python:

    class _DDLCFileWrapper(object):
        """Wraps a binary file to yield decoded lines when iterated,
        and .read() returns decoded str for text compat with Python 2 code."""
        def __init__(self, f):
            self._f = f
        def __enter__(self):
            return self
        def __exit__(self, *args):
            self._f.close()
        def read(self, *args):
            data = self._f.read(*args)
            if isinstance(data, bytes):
                try:
                    return data.decode('utf-8')
                except UnicodeDecodeError:
                    return data
            return data
        def __iter__(self):
            for line in self._f:
                if isinstance(line, bytes):
                    yield line.decode('utf-8')
                else:
                    yield line
        def readline(self, *args):
            line = self._f.readline(*args)
            if isinstance(line, bytes):
                try:
                    return line.decode('utf-8')
                except UnicodeDecodeError:
                    return line
            return line
        def close(self):
            self._f.close()
        def __getattr__(self, name):
            return getattr(self._f, name)

    # Get the real function from the actual source module
    import renpy.exports.loaderexports as _ldr
    _real_file = _ldr.file.__wrapped__ if hasattr(_ldr.file, '__wrapped__') else _ldr.file
    # Actually, just get open_file which is the real implementation
    _real_open_file = _ldr.open_file

    def _ddlc_file(fn, encoding=None):
        f = _real_open_file(fn, encoding=encoding)
        if encoding is not None:
            return f  # Already text mode
        return _DDLCFileWrapper(f)

    # Override only the 'file' function, not open_file
    # The store's `renpy` is `renpy.exports`, so we patch renpy.exports.file
    import sys
    sys.modules['renpy.exports'].file = _ddlc_file

    import os
    
    def _macos_readonly_check(label, abnormal):
        if label == "splashscreen":
            # Test if base directory is actually writeable
            test_path = os.path.join(config.basedir, ".rw_test")
            try:
                with open(test_path, "wb") as f:
                    f.write(b"test")
                os.remove(test_path)
            except Exception:
                # Read-only or permission denied
                renpy.jump("readonly")

    config.label_callbacks.append(_macos_readonly_check)
    
    def _scrub_rollback():
        try:
            for entry in renpy.game.log.log:
                if hasattr(entry, 'stores') and 'store' in entry.stores and 'srf' in entry.stores['store']:
                    entry.stores['store']['srf'] = None
                if hasattr(entry, 'context') and hasattr(entry.context, 'stores') and entry.context.stores:
                    if 'store' in entry.context.stores and 'srf' in entry.context.stores['store']:
                        entry.context.stores['store']['srf'] = None
            if getattr(renpy.store, "srf", None) is not None:
                renpy.store.srf = None
        except Exception:
            pass

    config.interact_callbacks.append(_scrub_rollback)
