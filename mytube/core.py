import os
import sys
import json


class MyTubeCore:
    def __init__(self):
        pass

    def convert_list(self, a: list):
        it = iter(a)
        res_dict = dict(zip(it, it))
        return res_dict

    def example_json(self):
        return json

    def read_json(self, filename: str):
        filename += '.json' if not '.json' in filename else ''
        if not os.path.exists(filename):
            print(f"Can't {filename}, exiting...")
            sys.exit()
        with open(filename, 'r', encoding='utf-8') as jsonfile:
            data = json.load(jsonfile)
        return data
    
    def save_json(self, filename: str, data):
        filename += '.json' if not '.json' in filename else ''
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, indent=4)
            

