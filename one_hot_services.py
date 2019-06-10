# coding = 'utf-8'

def make_dict(sentences, start_num = 1):
    iterT = start_num
    word_ids = {}
    for i in list(set(sentences)):
        if i not in word_ids:
            word_ids[i] = iterT
            iterT += 1
        else:
            pass

    return word_ids

def word2id(cut_sentence, word_ids):
    return [word_ids[i] for i in cut_sentence]