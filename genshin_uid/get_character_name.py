import os
import json

FILE_PATH = os.path.join(os.path.join(os.path.dirname(__file__), 'mihoyo_libs'), 'mihoyo_bbs')
INDEX_PATH = os.path.join(FILE_PATH, 'index')


def get_char_name_json(name):
    with open(os.path.join(INDEX_PATH, 'char_alias.json'), 'r', encoding='utf8')as fp:
        char_data = json.load(fp)
        # return char_data
        for i in char_data:
            if name in i:
                name = i
            else:
                for k in char_data[i]:
                    if name in k:
                        name = i
        return name
