from os import walk
from pathlib import Path
from os.path import join
from importlib import import_module
from boucanpy.core.utils import api_dir, snake_to_title

routers = []


def extact_routers(parent_dir, parent_mod):
    _routers = []
    for directory_name, sub_directories, files in walk(parent_dir):
        for sub_dir_name in sorted(sub_directories):
            if not sub_dir_name.startswith(("__", "base")):
                if Path(join(join(parent_dir, sub_dir_name), "router.py")).is_file():
                    sub_dir = join(parent_dir, sub_dir_name)
                    module_path = f"{parent_mod}.{sub_dir_name}.router"
                    module = import_module(module_path, "router")
                    _router = getattr(module, "router", None)
                    if _router:
                        _options = getattr(module, "options", {})
                        router = (_router, _options)
                        _routers.append(router)
                    else:
                        print(f"failed to find router in {module_path}")
            _routers = _routers + extact_routers(
                join(parent_dir, sub_dir_name), f"{parent_mod}.{sub_dir_name}"
            )
    return _routers


for r in extact_routers(api_dir("routers"), "boucanpy.api.routers"):
    routers.append(r)
