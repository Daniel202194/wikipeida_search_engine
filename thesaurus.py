import linecache
import time
import os
import json as ja
from nltk.corpus import stopwords, lin_thesaurus as thes


class Thesaurus:

    def __init__(self):
        self.synonyms_idx = self.get_synonyms_index()

    @staticmethod
    def get_synonyms_index():
        path = os.getcwd() + '\\synonyms\\synonymsIndex.txt'
        file = open(path, 'r')
        synonyms = {}
        for line in file:
            split_line = line.split('~')
            synonyms[split_line[0]] = split_line[1]
        return synonyms

    def get_synonyms(self, word):
        list_of_word_synonyms = []
        if word.lower() in self.synonyms_idx.keys():
            line_of_synonms = int(self.synonyms_idx[word.lower()]) + 1
            line = linecache.getline(os.getcwd() + '\\synonyms\\synonyms.txt', line_of_synonms)
            line_split = line.split('~', 1)
            synonyms_split = line_split[1].split('|')
            if synonyms_split[len(synonyms_split) - 1][len(synonyms_split[len(synonyms_split) - 1]) - 1] == '\n':
                synonyms_split[len(synonyms_split) - 1] = synonyms_split[len(synonyms_split) - 1].replace('\n', '')
            new_syn = []
            for x in synonyms_split:
                new_syn.extend(x.split(' '))
            list_of_word_synonyms.extend(new_syn)
            return list_of_word_synonyms
        else:
            return list_of_word_synonyms

    @staticmethod
    def make_synonyms_file():
        words = ja.load(open(os.getcwd() + '\\words_dictionary.json'))
        stop = set(stopwords.words('english'))
        list_english_words = list(words.keys())
        words = sorted([w for w in list_english_words if w.lower() not in stop])
        synonyms = {}
        begin = time.time()
        count_synonyms = 0
        for word in words:
            word_synonyms = list(thes.synonyms(word.lower(), fileid="simN.lsp"))[:2]
            listA = list(thes.synonyms(word.lower(), fileid="simA.lsp"))[:2]
            listV = list(thes.synonyms(word.lower(), fileid="simV.lsp"))[:2]
            word_synonyms.extend(listA)
            word_synonyms.extend(listV)
            if len(word_synonyms) > 0:
                synonyms[word.lower()] = word_synonyms
                count_synonyms += 1
            if count_synonyms == 30000:
                print("Time take make 30,000 words" + str((time.time()-begin)/60) + "minutes")
                count_synonyms = 0

        end_make_synonyms = time.time()
        time_take = end_make_synonyms - begin
        time_take = time_take/60
        print("Finished make synonyms: time: " + str(time_take) + "minutes")
        sorted_synonyms = sorted(synonyms)
        path = os.getcwd() + "\\synonyms"
        synonyms_file_path = path + "\\synonyms.txt"
        synonyms_idx_path = path + "\\synonymsIndex.txt"
        synonyms_lines = []
        synonyms_idx = []
        os.mkdir(path)
        print("make synonyms folder")
        print("number of words in synonyms keys : " + str(len(sorted_synonyms)))
        begin = time.time()
        count = 0
        for idx, word in enumerate(sorted_synonyms):
            cur_line = str(word) + '~'
            cur_idx = str(word) + '~' + str(idx) + '\n'
            for index, synonym in enumerate(synonyms[word]):
                if index < len(synonyms[word]) - 1:
                    cur_line += str(synonym) + '|'
                else:
                    cur_line += str(synonym) + '\n'
                    synonyms_lines.append(cur_line)
            synonyms_idx.append(cur_idx)
            count += 1
            if count == 3000:
                count = 0
                print("Word number : " + str(idx))
                print("Time takes make 30,000 lines : " + str((time.time()-begin)/60) + "minutes")
        print("Starting making files")
        synonyms_file = open(synonyms_file_path, 'w')
        print("First file opened successfully")
        synonyms_idx_file = open(synonyms_idx_path, 'w')
        print("Second file opened successfully")
        synonyms_file.writelines(synonyms_lines)
        print("First file was written successfully")
        synonyms_idx_file.writelines(synonyms_idx)
        print("Second file was written successfully")
        synonyms_idx_file.close()
        synonyms_file.close()
