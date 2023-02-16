import re

numb_of_sentences = 'number of sentences'
numb_of_nondecl = 'number_of_nondeclarative sentences'
avrg_sentence_length = 'avrg_sentence_length'
avrg_word_length = 'avrg_word_length'
ngrams_list = 'ngrams_list'

sentence_template = r'[^\.|\.\.\.]+(\.|\.\.\.|?|!|?!)' #must be tested
word_template = r'\d*\w+[\w\d]*' #test too

def analyze_text(text, N, K):
    result_dict = {}

    sentences = re.findall(sentence_template, text)
    result_dict.update({numb_of_sentences: len(sentences)})

    proxy_dict = {numb_of_nondecl:0, 'sentences length':0, 'words count':0}
    for sentence in sentences:
        sentence_info = analyze_sentence(sentence)

        if sentence_info[0] == False :proxy_dict[numb_of_nondecl] += 1

        proxy_dict['words count'] += sentence_info[1]
        proxy_dict['sentences length'] += sentence_info[2]

    result_dict.update ({avrg_sentence_length : proxy_dict['sentences length']//result_dict[numb_of_sentences]})
    result_dict.update({avrg_word_length : proxy_dict['sentences length'] // proxy_dict['words count']})

    result_dict.update({numb_of_nondecl : proxy_dict[numb_of_nondecl]})

    result_dict.update({ngrams_list:list_of_ngrams(text, N, K)})
    return result_dict


def analyze_sentence(sentence):
    is_decl = sentence.group(1) == '.' or sentence.group(1)=='...'

    words = re.findall(word_template, sentence)
    symbols_in_sentence = 0
    for word in words:
        symbols_in_sentence += len(word)
    
    return (is_decl, len(words), symbols_in_sentence)


def list_of_ngrams(text, N, K):
    ngram_template = r'[\d\w]{' + str(N) + r'}'
    ngrams = re.findall(ngram_template, text)

    ngram_dict = {}

    for ngram in ngrams:
        if ngram_dict[ngram.group(0)] == None:
            ngram_dict.update({ngram.group(0) : 1})
        else:
            ngram_dict[ngram.group(0)] += 1

    return sorted(ngram_dict)[-K::-1]