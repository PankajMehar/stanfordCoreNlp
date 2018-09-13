
def build_replacement_dict(pairs):
    result = []
    for pair in pairs:
        indexs = pair.split(':')
        result.append({'token': indexs[0], 'indexs': indexs[1]})
    return result

def get_replaced_token(token, replacement, vocab):
    replacement = replacement.split(' ')
    list_of_tokens = []
    for i in replacement:
        list_of_tokens.append(Token(vocab['idx_12236'], i))  
    return list_of_tokens  


def referent_answer_indexs(line, split_index):
    referent_token_pairs = []
    
    if(len(line) < split_index):
        return {}
    else:
        split_index = split_index - 1 if len(line) == split_index else split_index
        tokens = line[split_index].split(']')
        for i in tokens:
            split = i.split('[')
            if(len(split) == 2):
                answer_index = split[0].strip()
                print('answer_index', answer_index)
                replacement = build_replacement_dict(split[1].split(';'))
                referent_token_pairs.append({'answer_index': answer_index, 'replacement':replacement })
    return referent_token_pairs



def get_coreferent_tokens(orginal_tokens, referent_pairs, vocab):
    updated_tokens = original_tokens.copy()

    for pa in referent_pairs:
        for token in new_original_tokens:
            if token.index == pa['token']:
                token_index = updated_tokens.index(token)
                new_original_tokens[token_index] = get_replaced_token(token, pa['indexs'], vocab)
    return new_original_tokens




def build_coreference(pa, line, answers, vocab, split_index): 

    references = referent_answer_indexs(line, split_index)    
    keys = [item['answer_index'] for item in references]
    
    original_answer = answers[pa]

    if pa not in keys:
        return original_answer

    if pa in keys:
        referent_pairs = [value for key, value in references if key == pa]
        print('referent_pairs', referent_pairs)


        answer_updated_tokens = get_coreferent_tokens(original_answer.tokens, referent_pairs, vocab)
        text = ' '.join([' '.join([item.text for item in token]) if type(token) == list else token.text for token in answer_updated_tokens])

        referent_answer = TextItem(text, answer_updated_tokens)
        referent_answer.metadata['id'] = original_answer.metadata['id']
        return referent_answer 





with open('hello.txt', 'r') as f:
    for line in f:
        print(referent_answer_indexs(line.split('\t'), 4))