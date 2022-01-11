import os
import sys
from string import ascii_lowercase
from reader import ReadFile

class Indexer:
    number_of_file = 0

    def __init__(self, config):
        self.postingDict = {}
        self.titles = {}
        self.entities = dict()
        self.config = config
        self.files_list = []
        self.documents_list = []
        self.number_of_wikis_in_corpus = 0
        self.sum_of_length = 0

    def add_new_doc(self, document):
        """
        This function perform indexing process for a document object.
        Saved information is captures via two dictionaries ('inverted index' and 'posting')
        :param document: a document need to be indexed.
        :return: -
        """
        self.titles[document.wiki_id] = document.wiki_title
        self.number_of_wikis_in_corpus += 1
        if document.max_word == "":
            values_of_doc = str(document.wiki_id) + ' ' + str(document.length_of_all_terms) + ' ' + str(
                document.length_of_uniqe_term) + ' ' + str(document.max_term_appearance) + ' ' + '\n'
        else:
            values_of_doc = str(document.wiki_id) + ' ' + str(document.length_of_all_terms) + ' ' + str(
                document.length_of_uniqe_term) + ' ' + document.max_word + ' ' + str(
                document.max_term_appearance) + ' ' + '\n'
        self.documents_list.append(values_of_doc)
        self.sum_of_length += document.length_of_all_terms
        document_dictionary = document.term_doc_dictionary
        for term in document_dictionary.keys():
            try:
                self.add_term(term, document.wiki_id, document_dictionary[term], False)
            except:
                pass

    def clear(self):
        self.postingDict = {}

    def add_term(self, term, wiki_id, appearance_number_in_wiki, is_entity):
        """
               This function add term to dictionary .
               Saved information and the term himself  or in the dictionary  ('entities') or in dictionary  ('posting')
               :param term: the term we want to add
               :param wiki_id: id of document that term showes in it
               :param appearance_number_in_wiki: number of appearance that term showes in document
               :param is_entity: this variable tell us if the term is entity or not
               :return: -
               """
        if not is_entity:
            if term.upper() not in self.postingDict.keys() and term.lower() not in self.postingDict.keys():
                wiki_list_details = dict()
                wiki_list_details[wiki_id] = appearance_number_in_wiki
                self.postingDict[term] = [wiki_list_details, appearance_number_in_wiki]
            else:
                self.lower_or_upper(term, wiki_id, appearance_number_in_wiki)
        else:
            if term not in self.entities.keys():
                if term.lower() not in self.postingDict.keys() and term not in self.postingDict.keys():
                    wiki_list_details = dict()
                    wiki_list_details[wiki_id] = appearance_number_in_wiki
                    self.entities[term] = [wiki_list_details, appearance_number_in_wiki]
                else:
                    self.lower_or_upper(term, wiki_id, appearance_number_in_wiki)
            else:
                if term.lower() not in self.postingDict.keys():
                    pre_appearance_number = self.entities[term][1]
                    wiki_list_details = dict()
                    for key in self.entities[term][0].keys():
                        wiki_list_details[key] = self.entities[term][0][key]
                    wiki_list_details[wiki_id] = appearance_number_in_wiki
                    self.postingDict[term] = [wiki_list_details, pre_appearance_number + appearance_number_in_wiki]
                    self.postingDict[term][0][wiki_id] = appearance_number_in_wiki
                    self.postingDict[term][1] = pre_appearance_number + appearance_number_in_wiki
                    del self.entities[term]
                else:
                    pre_appearance_number = self.entities[term][1]
                    wiki_list_details = dict()
                    for key in self.entities[term][0].keys():
                        wiki_list_details[key] = self.entities[term][0][key]
                    wiki_list_details[wiki_id] = appearance_number_in_wiki
                    number_of_entity = int(pre_appearance_number) + int(appearance_number_in_wiki)
                    self.postingDict[term.lower()][0].update(wiki_list_details)
                    self.postingDict[term.lower()][1] = int(self.postingDict[term.lower()][1]) + number_of_entity

    def write_to_disk(self, kind=None):
        """
        This function write sorted posting dictionary to disk.
        :param kind:
        :return: -
        """

        path = os.getcwd()
        sub_dir = kind
        if 'postings' not in os.listdir(path):
            os.mkdir(os.getcwd() + '\\postings')
        if sub_dir not in os.listdir(path + '\\postings'):
            os.mkdir(os.getcwd() + '\\postings\\' + sub_dir)
            for c in ascii_lowercase:
                path = os.getcwd() + '\\postings\\' + sub_dir
                path = os.path.join(path + '\\', c)
                os.mkdir(path)
            path = os.getcwd() + '\\postings\\' + sub_dir
            path_numbers = os.path.join(path + '\\', 'numbers')
            os.mkdir(path_numbers)
        all_letters = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", 'A', 'B', 'C', 'D', 'E', 'F',
                       'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
                       'Z', "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q",
                       "r", "s", "t", "u", "v", "w", "x", "y", "z"]
        sorted_temp_post = sorted(self.postingDict)
        current_path = os.getcwd() + '\\postings\\' + sub_dir
        num_file_per_dict = Indexer.number_of_file
        all_list = []

        for letter in all_letters:
            i = 0
            if letter.isdigit():
                save_path = current_path + '\\' + "numbers" + '\\' + 'file' + str(num_file_per_dict) + '.txt'
            else:
                save_path = current_path + '\\' + letter.lower() + '\\' + 'file' + str(num_file_per_dict) + '.txt'
            while i < len(sorted_temp_post) and sorted_temp_post[i][0] != letter:
                i += 1
            while i < len(sorted_temp_post) and sorted_temp_post[i][0] == letter:
                current_word = sorted_temp_post[i]
                number_of_appearance = self.postingDict[current_word][1]
                term_and_value = str(current_word)+'~'+str(number_of_appearance) + '~'
                last_term = list(self.postingDict[current_word][0].keys())[-1]
                for term in self.postingDict[current_word][0]:
                    term_and_value += str(term) + '_' + str(self.postingDict[current_word][0][term])
                    if term is not last_term:
                        term_and_value += '|'
                term_and_value += '~' + '\n'
                all_list.append(term_and_value)
                i = i+1
            if len(all_list) > 0:
                f = open(save_path, "a", encoding="utf-8")
                f.writelines(all_list)
                f.close()
                all_list = []
        Indexer.number_of_file = Indexer.number_of_file + 1

    def lower_or_upper(self, term, wiki_id, appearance_number_in_wiki):
        """
        This function check if the term will be in the dictionary in upper case or on lower case.

        :param term: the term we want to check
        :param wiki_id: id of document that term showes in it
        :param appearance_number_in_wiki: number of appearance that term showes in document
        :return: -
        """
        appearance_number_in_wiki = int(appearance_number_in_wiki)
        wiki_list_details = {}
        if term == term.lower():
            upper_term = term.upper()
            if upper_term in self.postingDict.keys():
               values_posting = self.postingDict[upper_term]
               wiki_list_details[wiki_id] = appearance_number_in_wiki
               self.postingDict[term] = [wiki_list_details, appearance_number_in_wiki]
               self.postingDict[term][0].update(values_posting[0])
               self.postingDict[term][1] = appearance_number_in_wiki + int(values_posting[1])
               del self.postingDict[upper_term]
            elif term in self.postingDict.keys():
                wiki_list_details[wiki_id] = appearance_number_in_wiki
                self.postingDict[term][0].update(wiki_list_details)
                self.postingDict[term][1] += appearance_number_in_wiki
            else:
                wiki_list_details[wiki_id] = appearance_number_in_wiki
                self.postingDict[term] = [wiki_list_details, appearance_number_in_wiki]

        elif term == term.upper():
            lower_term = term.lower()
            if lower_term in self.postingDict.keys():
                wiki_list_details[wiki_id] = appearance_number_in_wiki
                self.postingDict[term] = [wiki_list_details, appearance_number_in_wiki]
                values_doc_dict = self.postingDict[term]
                self.postingDict[lower_term][0].update(values_doc_dict[0])
                self.postingDict[lower_term][1] = int(self.postingDict[lower_term][1]) + values_doc_dict[1]
                del self.postingDict[term]
            elif term in self.postingDict.keys():
                wiki_list_details[wiki_id] = appearance_number_in_wiki
                self.postingDict[term][0].update(wiki_list_details)
                self.postingDict[term][1] += appearance_number_in_wiki
            else:
                wiki_list_details[wiki_id] = appearance_number_in_wiki
                self.postingDict[term] = [wiki_list_details, appearance_number_in_wiki]

    def begin_to_merge(self, kind=None):
        """
                      This function send the open the posting files on disc and send each time two files and more inputs to the function merging_files
                      after merging finished this function write list  of documents document file
                      :param -
                      :return: -
                      """
        i = 0
        all_letters = ["numbers", "a", "b", "c", "d", "e", "f",
                       "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x",
                       "y", "z"]
        current_path = os.getcwd() + '\\postings\\' + kind
        for letter in all_letters:
            counter = 0
            path = current_path + '\\' + letter+'\\'
            all_path = path + 'merged_file'
            self.files_list = []
            self.files_list = os.listdir(path)
            # print('megre {}'.format(path))
            if len(self.files_list) > 1:
                self.merging_files(path + self.files_list[0], path + self.files_list[1], all_path, counter, 0, 0)
                counter += 1
                while i != len(self.files_list)-1:
                    self.merging_files(path +self.files_list[i], path + self.files_list[-1], all_path, counter, i, -1)
                    counter += 1
        docs_average_length = self.sum_of_length / self.number_of_wikis_in_corpus
        docs_average_length = str(docs_average_length) + '\n'
        length_of_corpus = str(self.number_of_wikis_in_corpus)
        list_of_data = []
        list_of_data.append(docs_average_length)
        list_of_data.append(length_of_corpus)
        dir_doc_path = current_path + '\\' + 'data'
        doc_path = dir_doc_path + '\\' + 'data' + '.txt'
        os.mkdir(dir_doc_path)
        data_file = open(doc_path, 'w')
        data_file.writelines(list_of_data)
        data_file.close()
        dir_doc_path = current_path+'\\'+'Documents'
        doc_path = dir_doc_path + '\\' + 'documents'+'.txt'
        os.mkdir(dir_doc_path)
        doc_file = open(doc_path, 'w', encoding="utf-8")
        try:
            doc_file.writelines(self.documents_list)
        except:
            print("documents list: {}".format(self.documents_list))
        doc_file.close()

    def merging_files(self, file_1, file_2, path, counter, index_file_1, index_file_2):
        """
                              This function get two files, Go through the files and merge them
                              :param - file_1: file to merge
                              :param - file_2: file to merge
                              :param - path: path to merged file
                              :param - counter: number of merged file
                              :param - index_file_1: index of file the function delete from file after we merged them
                              :param - index_file_2: index of file the function delete from file after we merged them
                              :return: -
                              """
        f_1 = open(file_1, 'r')
        f_2 = open(file_2, 'r')
        lines_of_file_1 = f_1.readlines()
        lines_of_file_2 = f_2.readlines()
        merged_terms = []
        i = 0
        j = 0
        word_1_to_compare = ""
        word_2_to_compare = ""
        try:
            while i < len(lines_of_file_1) and j < len(lines_of_file_2):
                if word_1_to_compare == "":
                    word_1_to_compare = lines_of_file_1[i].split("~", 1)[0]
                if word_2_to_compare == "":
                    word_2_to_compare = lines_of_file_2[j].split("~", 1)[0]
                if word_1_to_compare == word_2_to_compare.upper() or word_1_to_compare == word_2_to_compare:
                    split_line_1 = lines_of_file_1[i].split("~")
                    split_line_2 = lines_of_file_2[j].split("~")
                    word_1_to_compare = ""
                    word_2_to_compare = ""
                    split_line_2[1] = int(split_line_1[1]) + int(split_line_2[1])
                    split_line_2[1] = str(split_line_2[1])
                    split_line_2[2] = split_line_2[2] + '|' + split_line_1[2]
                    return_to_string = split_line_2[0] + '~' + split_line_2[1] + '~' + split_line_2[2] + '~'+'\n'
                    merged_terms.append(return_to_string)
                    lines_of_file_1.remove(lines_of_file_1[i])
                    j += 1
                elif word_1_to_compare == word_2_to_compare.lower():
                    split_line_1 = lines_of_file_1[i].split("~")
                    split_line_2 = lines_of_file_2[j].split("~")
                    word_1_to_compare = ""
                    word_2_to_compare = ""
                    split_line_1[1] = int(split_line_1[1]) + int(split_line_2[1])
                    split_line_1[1] = str(split_line_1[1])
                    split_line_1[2] = split_line_2[2] + '|' + split_line_1[2]
                    return_to_string = split_line_1[0] + '~' + split_line_1[1] + '~' + split_line_1[2] + '~' + '\n'
                    merged_terms.append(return_to_string)
                    lines_of_file_2.remove(lines_of_file_2[j])
                    i += 1
                elif word_1_to_compare > word_2_to_compare:
                    word_2_to_compare = ""
                    merged_terms.append(lines_of_file_2[j])
                    j += 1

                elif word_2_to_compare > word_1_to_compare:
                    word_1_to_compare = ""
                    merged_terms.append(lines_of_file_1[i])
                    i += 1
            while i < len(lines_of_file_1):
                merged_terms.append(lines_of_file_1[i])
                i += 1
            while j < len(lines_of_file_2):
                merged_terms.append(lines_of_file_2[j])
                j += 1
            f_1.close()
            f_2.close()
            os.remove(file_1)
            os.remove(file_2)
            self.files_list.remove(self.files_list[index_file_1])
            self.files_list.remove(self.files_list[index_file_2])
            name_file = 'merged_file' + str(counter) + '.txt'
            merged_path = path + str(counter) + '.txt'
            merged_file = open(merged_path, 'a')
            merged_file.writelines(merged_terms)
            merged_file.close()
            self.files_list.append(name_file)
        except ValueError as err:
            print("ValueError error: {0}".format(err))
            print('Unexpected error: ', sys.exc_info()[0])
            print('File 1: {}')
            print('File 2: {}'.format(file_2))
    @staticmethod
    def pointer_terms(kind=None):
        """
        This function write the terms and number line the term shows in posting files
        :param kind:-
        :return: -
        """
        path = os.getcwd() + '\\postings\\' + kind
        terms = []
        r = ReadFile(path, isIndexer=True)
        for file in r:
            cur_file = open(file, 'r', encoding="utf-8")
            if file == path + '\\Documents\\documents.txt' or file == path + '\\data\\data.txt':
                continue
            for index, line in enumerate(cur_file):
                term = line.split('~', 1)[0]
                term += ',' + str(index) + '\n'
                terms.append(term)
        os.mkdir(path + '\\terms')
        file = open(path + '\\terms' + '\\terms.txt', 'w', encoding="utf-8")
        file.writelines(terms)

