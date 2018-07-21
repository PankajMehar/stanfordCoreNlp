import os 
import json
import itertools


result = []
vocabulary_dict = dict()
with open('questionClusters.json', 'r') as f:
    data = json.load(f)


with open('vocabulary', 'r') as vocabulary:
    for line in vocabulary:
        tokens = line.split()
        vocabulary_dict[tokens[1]] = tokens[0]

def getIndexs(item):
    data = item.split(' ')
    return [vocabulary_dict[token] for token in data]

def build_indexs():
    for item in data:
        for key , value in item.items():
            per_question_cluster_dict = dict()
            final_list = list()
            for cluster in value:
                per_answer_cluster = []
                if len(cluster) == 0:
                    final_list.append([])
                    continue

                per_pair_token_indexs= []
                for pair in cluster:
                    if len(pair) == 1 or len(pair) == 0:
                        per_pair_token_indexs.append([])
                        continue
                    question_mention = pair[0]
                    answer_mentions = pair[1:]
                    
                    question_mention_tokens = question_mention.split(' ')
                    question_mention_tokens_indexs = [vocabulary_dict[token] for token in question_mention_tokens]
                    per_pair_token_indexs.append(question_mention_tokens_indexs)
                    
                    ## this is for the second case 
                    answer_mentions_tokens_indexs = [getIndexs(item) for item in answer_mentions]
                    per_pair_token_indexs.append(answer_mentions_tokens_indexs)
                per_answer_cluster.append(per_pair_token_indexs)
                
                final_list.append(per_answer_cluster)

            per_question_cluster_dict.update({key: final_list})
            
        result.append(per_question_cluster_dict)           


build_indexs()

with open('dummy.json', 'w') as f:
    json.dump(result, f)


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

    return (key, answer_indexs[0: 20])


with open('corefQuestionFile.txt', 'w') as file:
    with open('InsuranceQA.question.anslabel.token.100.pool.solr.test.encoded', 'r') as original_file:
        question_number = 0
        for line in original_file:
            line = line.rstrip()
            key, answer_indexs = get_key_and_answer_indexs(line)            
            # have to make it work for the multiple questions 
            # need to build for the case when there are multiple matches for the answer ex- it , they 
            # need to refactor this one 
            cluster = result[question_number]
            answer_referent_clusters = cluster[key]
            counter = 0
            referent_string = ''
            for index in answer_indexs:
                answer_referent_cluster = answer_referent_clusters[counter]
                if len(answer_referent_cluster) == 0:
                    counter = counter + 1
                    continue
                token_string = ''
                for pair in answer_referent_cluster:
                    if len(pair[0]) == 0:
                        continue
                    question_referent_indexs = pair[0]
                    answer_referent_indexs = pair[1]
                    
                    answer_string = ''
                    
                    count_number_of_answer_referent_index = 0
                    print('count_number_of_answer_referent_index', answer_referent_indexs, count_number_of_answer_referent_index , len(answer_referent_indexs))
                    for list_of_index in answer_referent_indexs:
                        count = 1
                        length_of_index = len(list_of_index)
                        count_number_of_answer_referent_index = count_number_of_answer_referent_index + 1
                        for answer_index in list_of_index:
                            print('count', count)
                            answer_string =  answer_string  + answer_index + ':' + ' '.join(question_referent_indexs) 

                            if count < len(list_of_index) :
                                print('dewfwffew', count , len(list_of_index))
                                answer_string = answer_string + ';'
                                count = count + 1
                                 
                    token_string = token_string + answer_string  
                    referent_string = referent_string + index + str([token_string]) + ' ' 
                
                counter = counter + 1 

            final_string = line  +  '\t' + referent_string + '\n'
            file.write(final_string)
            final_string = ''
            question_number +=1

                
