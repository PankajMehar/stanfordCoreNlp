import os 
import json
import re


with open ('./questionMatchingMentionSample.json', 'r') as f:
    clusters = json.load(f)

result = list()
def filteringMentions(question_mention, answer_mention):
    if len(answer_mention) == 1:
        return answer_mention
    question_mention_tokens = question_mention.split(' ')
    question_mention_tokens_lowercase = [token.lower() for token in question_mention_tokens]
    answer_mention = answer_mention.split(' ')
    for mention in answer_mention: 
        if mention in question_mention_tokens or mention in question_mention_tokens_lowercase:
            return
    return answer_mention


def referent_tokens():
    for key, question_clusters in clusters[0].items():
        reffering_tokens = list()
        per_question_referring_tokens = dict()
        for answer_cluster in question_clusters:
            question_mention = ''
            per_answer_tokens = list()
            if len(answer_cluster) == 0:
                 reffering_tokens.append([])
                 continue
            for answer_mention_item in answer_cluster[0] :
                if answer_mention_item['position'][0] == 1:
                    question_mention = answer_mention_item['text']
                    per_answer_tokens.append(question_mention)
                    continue
                ### Todo find the better solution to reject the tokens
                mention = filteringMentions(question_mention, answer_mention_item['text'])
                if mention is not None:
                    per_answer_tokens.append(mention)


            reffering_tokens.append(per_answer_tokens)
        per_question_referring_tokens.update({key : reffering_tokens})   
        result.append(per_question_referring_tokens)  
                    
                    
                 
referent_tokens()
with open('questionClusters.json', 'w') as file:
    json.dump(result, file)