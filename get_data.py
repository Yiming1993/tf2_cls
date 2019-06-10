import config
import mongoDB_services
import jieba_services
import one_hot_services

class Get_data(object):
    def __init__(self):
        self.db = config.db_path('NEWS')

    def get_data(self, limit = 2000):
        iterT = 0
        collections = []
        for i in mongoDB_services.get_data(self.db, 'NEWS', {"class":"web"}, ["title", "collect"]):
            if i != []:
                if i[1] == True:
                    single_data = [i[0], 1]
                else:
                    single_data = [i[0], 0]
                collections.append(single_data)
                if iterT >= limit:
                    break
                else:
                    iterT += 1
        return collections

if __name__ == '__main__':
    G = Get_data()
    collections = G.get_data(10)
    _collections = [[jieba_services.cut_sentence(i[0], 'list'), i[1]] for i in collections]
    corpus = []
    for i in _collections:
        corpus.extend(i[0])
    word_ids = one_hot_services.make_dict(corpus)

    _collections = [[one_hot_services.word2id(i[0], word_ids),i[1]] for i in _collections]
