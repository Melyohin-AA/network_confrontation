import os
import sys


def try_fix_project_root():
    current_path = os.path.abspath(sys.modules[__name__].__file__)
    root_path = current_path[:current_path.find("core") + 4]
    if root_path not in sys.path:
        sys.path.append(root_path)


try_fix_project_root()


import game_eng.game_model
