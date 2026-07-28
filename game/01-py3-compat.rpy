# Python 3 compatibility shim for DDLC (originally built with Ren'Py 6.x / Python 2)

init -990 python:
    def _scrub_rollback():
        try:
            for entry in renpy.game.log.log:
                if hasattr(entry, 'stores') and 'store' in entry.stores and 'f' in entry.stores['store']:
                    entry.stores['store']['f'] = None
                if hasattr(entry, 'context') and hasattr(entry.context, 'stores') and entry.context.stores:
                    if 'store' in entry.context.stores and 'f' in entry.context.stores['store']:
                        entry.context.stores['store']['f'] = None
            if getattr(renpy.store, "f", None) is not None:
                renpy.store.f = None
        except Exception:
            pass

    config.interact_callbacks.append(_scrub_rollback)
