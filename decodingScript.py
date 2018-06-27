import os 
import re
question = list()
import json

def buildVocabulary():
    vocabularyList = []
    with open('./vocabulary', 'r') as file:
        for line in file:
            newline = ' '.join(line.split()).split(' ')
            vocabularyList.append(newline)
        return  vocabularyList   

vocabularyList = buildVocabulary()

def getAnswerLabels():
    labels = dict()
    with open('./InsuranceQA.label2answer.token.encoded', 'r') as file:
        for i, line in enumerate(file):
            newline = ' '.join(line.split()).split(' ')
            labels.update({newline[0]:newline[1:]})
        return  labels   

def buildResultString(list_of_strings):
    result_list_of_strings = []
    for item in list_of_strings:
        for vocabulary in vocabularyList:
            if vocabulary[0] == item:
                result_list_of_strings.append(vocabulary[1])
                break
    return result_list_of_strings

with open('./sampleQuestionFile.txt') as input:
    answerLabels = getAnswerLabels()
    for line in input:
        data = dict()
        data.update({'answers': []})
        list_of_strings = []
        newline = ' '.join(line.split()).split(' ')

        list_of_question_strings = [token for token in newline if 'idx_' in token]
        questionString = ' '.join(buildResultString(list_of_question_strings))
        data.update({'question': questionString})   
        print('data', data)   

        list_of_answer_indices = [token for token in newline if 'idx_' not in token][1:]
        for answer_index in list_of_answer_indices:
            if answer_index in answerLabels:
                answerString = ' '.join(buildResultString(answerLabels[answer_index]))
                answerString = answerString
                data['answers'].append(answerString)

        question.append({newline[0] :data})

with open('./sampleDecoded.txt', 'w') as output:
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
