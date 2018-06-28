from stanfordcorenlp import StanfordCoreNLP
import json 
import time
import psutil


import multiprocessing 

nlp = StanfordCoreNLP(r'./stanford-corenlp-full-2018-02-27')
props = {'annotators': 'coref, ssplit', 'pipelineLanguage': 'en'}

sentences = []
j = []
coref_data = []
qt =   []
answer = []

def get_chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def process_line(sentence):
    print('sentence', sentence)
    return nlp.annotate( 
        sentence, 
        properties = {
                    'timeout': '10000000',
                    'annotators': 'coref',
                    'outputFormat': 'json'
                    }) 
    

def setup():
    with open('sampleDecoded2.txt', 'r') as file:
        answer = []
        for line in file:
            if 'start question' in line: 
                index = 1
                j = []
                continue
        
            elif 'end question' in line:
                index = 0  
                coref_data.append({label: j, 'question': question})
                continue

            elif index == 1 :
                label = line.rstrip()
                index = 2
                continue
        
            elif index == 2:
                question = line
                question = question.rstrip()
                question = question + ' .'
                index = 0
                continue
        
        
            line = line.rstrip()       
            sentence = ' '.join([question, line])
            result = []
            qt.append(sentence) 





if __name__ == '__main__':
    setup()
    chunks = get_chunks(qt, 4)
    final_result = []
    for chunk in chunks:
        pool = multiprocessing.Pool(4)
        start_time = time.time()
        results = pool.map(process_line, chunk)
        final_result.append(result['corefs'])
        print('result', results)
        pool.close()
        pool.join()
        end_time = time.time()

    with open('hello.json', 'w') as f:
        json.dump(coref_data,  q)


nlp.close()
'''
processes = [mp.Process(target=rand_string, args=(output)) for x in range(4)]



processes = [mp.Process(target=rand_string, args=(5, output)) for x in range(4)]

# Run processes
for p in processes:
    p.start()


# Exit the completed processes
for p in processes:
    p.join()

# Get process results from the output queue
results = [output.get() for p in processes]

print(results)


if __name__ == '__main__':
    pool = Pool(processes=(cpu_count() - 1))
    


            jobs = []
            for i in range(4):
                annontation = Process(target=process_line, args=(qt[i],))
                jobs.append(annontation)
                annontation.start()
                annontation.join()
            result.append(jobs)
            qt = []
        else:
            pass


        result = json.loads(result)
    
        q = []
        for key, value in result['corefs'].items():
            print(value)
            u = []
            for i in value:
                u.append({'text': i['text'], 'position': i['position']})
            q.append(u)
        
        j.append(q)
          

with open('sampleStanfordCoref.json', 'w') as q:
    json.dump(coref_data,  q)
        

'''