import os
import sys
import json

mfl_data_path = os.getcwd()+"/.FreeCAD/mfl.json"

try:
    with open(mfl_data_path, 'r') as file:
        mfl_module_path = json.load(file)['path']
except:
    with open(mfl_data_path, 'w') as file:
        mfl_module_path = input(
            "Please input path to mfl's parent folder:"
        )
        json.dump(
            {'path':mfl_module_path},
            file
        )
finally:
    sys.path.append(mfl_module_path)

print(
    "You may now import mfl using FreeCAD's Python console."
)
