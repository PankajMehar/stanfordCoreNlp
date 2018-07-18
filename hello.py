import os
import json

with open('sampleStanfordCoref.json', 'r') as f:
    array1 = json.load(f)

with open('sampleStanfordCoref2.json', 'r') as f:
    array2 = json.load(f)    


final_array = array1 + array2
print('dqwdqwdq', final_array)

with open('finalFile.json', 'w') as f:
    json.dump(final_array, f)
