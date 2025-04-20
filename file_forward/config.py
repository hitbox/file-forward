import importlib.util
import os

def load_pyfile(path):
    module_name, _ = os.path.splitext(os.path.basename(path))
    spec = importlib.util.spec_from_file_location(module_name, path)
    config = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config)
    return config
