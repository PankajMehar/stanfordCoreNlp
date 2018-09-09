import os
import json
import re
import nltk
import itertools

result = []
vocabulary_dict = dict()

with open ('./questionMatchingMentionSample.json', 'r') as f:
    data = json.load(f)


with open('vocabulary', 'r') as vocabulary:
    for line in vocabulary:
        tokens = line.split()
        vocabulary_dict[tokens[1]] = tokens[0]

def getIndexs(item):
    data = item.split(' ')
    return [vocabulary_dict[token] for token in data]

def filteringMentions(question_mention, answer_mention):
    list_of_pronoun_tags = ['PRP', 'PRP$', 'WP']
    part_of_speech = nltk.pos_tag([answer_mention])[0][1] 
    if part_of_speech in list_of_pronoun_tags:
        return answer_mention
    return None
    

def valid_cluster(cluster):
    if len(cluster) == 0 or len(cluster[0]) == 0:
        return False
    for pair in cluster[0]:
        if pair['position'][0] == 1:
            return True
    return False

def is_question_pair(pa):
    if pa['position'][0] == 1:
        return True
    return False

def build_pairs(cluster):
    answer_substrings = []
    pair = dict()
    for pa in cluster:
        if is_question_pair(pa):
            pair['replacements'] =  getIndexs(pa['text'])
            continue
        else:
            answer_substrings.append(filteringMentions(pair['replacements'],pa['text']))

    answer_substrings = list(set([x for x in answer_substrings if x is not None]))
    if(len(answer_substrings) == 0):
        return {}

    pair['answer_tokens'] = list(itertools.chain(*[getIndexs(item) for item in answer_substrings]))
    return pair

def referent_tokens():
    result = []
    for item in data:
        key = item.keys()[0]
        clusters = item.values()[0]
        pairs = []
        for cluster in clusters:
            answer_substrings = []
            if not valid_cluster(cluster):
                pairs.append({})
                continue
            else:
                pairs.append(build_pairs(cluster[0]))
        result.append({'key': key, 'pairs': pairs})        
                
    return result

with open('questionClusters.json', 'w') as file:
    json.dump(referent_tokens(), file)

    