import importlib

__all__ = ["root", "login", "apply", "create"]

blueprints = []
for name in __all__:
    blueprints.append(importlib.import_module("pages."+name))
