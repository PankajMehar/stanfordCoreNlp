import os 
import json

result = []
vocabulary_dict = dict()
with open('questionClusters.json', 'r') as f:
    data = json.load(f)


with open('vocabulary', 'r') as vocabulary:
    for line in vocabulary:
        tokens = line.split()
        vocabulary_dict[tokens[1]] = tokens[0]

def build_indexs():
    for item in data:
        for key , value in item.items():
            per_question_cluster_dict = dict()
            final_list = list()
            for cluster in value:
                per_question_cluster = []
                if len(cluster) == 1 or len(cluster) == 0:
                    final_list.append([])
                    print('it hits here ')
                    continue

                question_mention = cluster[0]
                answer_mentions = cluster[1]
                print('question_mention', question_mention, answer_mentions)
                question_mention_tokens = question_mention.split(' ')
                
                question_mention_tokens_indexs = [vocabulary_dict[token] for token in question_mention_tokens]
                answer_mentions_tokens = [ token.split(' ') for token in answer_mentions ]

                print('answer_mentions_tokens', answer_mentions_tokens)
                # if answer_mentions = ['it', 'hello this is law'] in these case we need to make some improvement here
                answer_mentions_tokens_indexs = [ vocabulary_dict[token[0]] for token in answer_mentions_tokens]
                print('answer_mentions_tokens_indexs', answer_mentions_tokens_indexs)
                
                question_answer_pair_index = [question_mention_tokens_indexs] + answer_mentions_tokens_indexs
                print('de', question_answer_pair_index)
                per_question_cluster.append(question_answer_pair_index)
                final_list.append(per_question_cluster)

            per_question_cluster_dict.update({key: final_list})
            
        result.append(per_question_cluster_dict)           


build_indexs()
print('result', result)        

def get_question_key(line):
    line = ' '.join(line.split()).split(' ')
    return line[0]

with open('resultQuestionFile.txt', 'w') as file:
    with open('sampleQuestionFile.txt', 'r') as original_file:
        for line in original_file:
            key = get_question_key(line)
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
            print('first_answer_index_in_list', first_answer_index_in_list)    
            answer_indexs = token_indexs[first_answer_index_in_list: ]  
            question_indexs = token_indexs[0: first_answer_index_in_list]
            
            # have to make it work for the multiple questions 
            # need to build for the case when there are multiple matches for the answer ex- it , they 
            # need to refactor this one 
            answer_referent_clusters = result[0][key]
            counter = 0
            referent_string = ''
            for index in answer_indexs:
                answer_referent_cluster = answer_referent_clusters[counter]
                if len(answer_referent_cluster) == 0:
                    referent_string = referent_string + ' ' + index
                    print('referent', referent_string)
                    counter = counter + 1
                    continue
                # need to get rid of this indexing 
                answer_referent_cluster = answer_referent_cluster[0]
                print('sdwd',answer_referent_cluster )

                question_referent_indexs = answer_referent_cluster[0]
                # only working for single matching mention in the answer with question
                answer_referent_indexs = [answer_referent_cluster[1]]
                referent_string = referent_string + ' ' + index + ' ' +  str(answer_referent_indexs) + ' ' + str(question_referent_indexs) 
                counter = counter + 1 
            
            final_string = key + '\t' + ' '.join(question_indexs) + '\t' + referent_string + '\n'
            file.write(final_string)
            
        

            