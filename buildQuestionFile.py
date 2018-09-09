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



'''
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
    with open('sampleQuestion.txt', 'r') as original_file:
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
                    for list_of_index in answer_referent_indexs:
                        count_number_of_answer_referent_index = count_number_of_answer_referent_index + len(list_of_index)

                    count = 0
                    print('count_number_of_answer_referent_index', count_number_of_answer_referent_index)
                    for list_of_index in answer_referent_indexs:
                        print('list_of_index', list_of_index)
                        length_of_index = len(answer_referent_indexs)
                        print('coubt', count)
                        for answer_index in list_of_index:
                            answer_string =  answer_string  + answer_index + ':' + ' '.join(question_referent_indexs) 
                            count = count + 1

                            if count <= count_number_of_answer_referent_index -1:
                                answer_string = answer_string + ';'
                                
                                 
                    token_string = token_string + answer_string  
                    referent_string = referent_string + index + str([token_string]) + ' ' 
                
                counter = counter + 1 

            final_string = line  +  '\t' + referent_string + '\n'
            file.write(final_string)
            final_string = ''
            question_number +=1

                
'''