__all__ = []

import pkgutil
import inspect

for loader, name, is_pkg in pkgutil.walk_packages(__path__):
    module = loader.find_module(name).load_module(name)

    for name2, value in inspect.getmembers(module):
        if name2.startswith('__'):
            continue

        globals()[name2] = value
        __all__.append(name2)
