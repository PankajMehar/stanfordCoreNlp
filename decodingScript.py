import os 
import re
import sys
question = list()
import json
import itertools

## params
vocabularyList = []
answerLabels = dict()

def buildVocabulary():
    with open('./vocabulary', 'r') as file:
        for line in file:
            newline = ' '.join(line.split()).split(' ')
            vocabularyList.append(newline)


def buildAnswerLabels():
    with open('InsuranceQA.label2answer.token 2.encoded', 'r') as file:
        for i, line in enumerate(file):
            newline = ' '.join(line.split()).split(' ')
            answerLabels.update({newline[0]:newline[1:]})
        

def buildResultString(list_of_strings):
    result_list_of_strings = []
    for item in list_of_strings:
        for vocabulary in vocabularyList:
            if vocabulary[0] == item:
                result_list_of_strings.append(vocabulary[1])
                break
    return result_list_of_strings

def buildQuestionAnswerPair(line_index):
    with open('InsuranceQA.question.anslabel.token.500.pool.solr.valid.encoded') as input:
        range_start = (line_index -1) * 100
    
        range_end = range_start + 100
        print('range', range_start, range_end)

        for line in itertools.islice(input, range_start, range_end):
            data = dict()
            data.update({'answers': []})
            list_of_strings = []
            newline = ' '.join(line.split()).split(' ')

            list_of_question_strings = [token for token in newline if 'idx_' in token]
            questionString = ' '.join(buildResultString(list_of_question_strings))
            print('question_string', questionString)
            data.update({'question': questionString})   

            list_of_answer_indices = [token for token in newline if 'idx_' not in token][1:][0: 20]
            for answer_index in list_of_answer_indices:
                if answer_index in answerLabels:
                    answerString = ' '.join(buildResultString(answerLabels[answer_index]))
                    answerString = answerString
                    data['answers'].append(answerString)

            question.append({newline[0] :data})
        return question    


def buildText(file_index):
    buildVocabulary()
    answerLabels = buildAnswerLabels()
    questionAnswerPair = buildQuestionAnswerPair(int(file_index))
    input_file_path = './textData' + file_index + 'valid' + '.txt'
    with open(input_file_path, 'w') as output:
        for item in question:
            for key , value in item.items():
                output.write('start question'+ '\n')
                output.write(key + '\n')
                output.write(value['question'] + '\n')
                for answer in value['answers']:
                    output.write(answer + '\n')
                output.write('end question')
                output.write('\n')
        
        print('process competed')        


