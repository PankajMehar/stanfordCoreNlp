import os 
import json
import itertools

result = []
vocabulary_dict = dict()
with open('questionClusters.json', 'r') as f:
    data = json.load(f)

def build_referent_entitiy(item):
    if not any(item):
        return None

    pairs = []
    for answer_token in item['answer_tokens']:
        pair = answer_token + ':' +  ' '.join(item['replacements'])
        pairs.append(pair)
        
    return pairs

def  get_key_and_answer_indexs(line):
    line = ' '.join(line.split()).split(' ')
    key = line[0]
    token_indexs = line[1:]
    first_answer_index_in_list = 0
    counter = 0
    for token_index in token_indexs:
        if 'idx_' not in token_index:
            first_answer_index_in_list = counter
            break
            
        counter = counter +1 
    answer_indexs = token_indexs[first_answer_index_in_list: ]

    return answer_indexs[0: 20]

with open('InsuranceQA.question.anslabel.token.500.pool.solr.test.encoded', 'r') as file:
    line_index = 0
    result = []
    for line in file:
        line = line.rstrip()
        referent_part = ''
        answer_tokens = get_key_and_answer_indexs(line)
        original_string = line
        referent_clusters = data[line_index]
        referent_entities = []
        cluster_index = 0
        for cluster in referent_clusters['pairs']:
            referent_entites = build_referent_entitiy(cluster)
            answer_token = answer_tokens[cluster_index]
            if not referent_entites == None:
                referent_part = referent_part + ' ' +  answer_token + '[' + ';'.join(referent_entites) + ']'

            cluster_index = cluster_index + 1
            

        line_index = line_index + 1    
        final_string = line + '\t' + referent_part + '\n' 
        result.append(final_string)
         
with open('hello.txt', 'w') as f:
    for line in result:
        f.write(line)
            
         