import json
import os
from os import listdir
from os.path import isfile, join


dir_path = './corefFiles/'
onlyfiles = [f for f in listdir(dir_path) if isfile(join(dir_path, f))]
data = []

for i in range(1, 21):
    file_name = 'coref'+ str(i) + '.json'
    file_path = join(dir_path + file_name)
    with open(file_path, 'r') as f:
        coref = json.load(f)
        data = data + coref


with open('final_coref.json', 'w') as f:
    json.dump(data, f)        