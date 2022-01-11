import operator
import re
from nltk.corpus import stopwords
from document import Document
from stemmer import Stemmer


class Parse:
    def __init__(self):
        self.stop_words = stopwords.words('english')
        self.stop_words_set = set(self.stop_words)
        self.add_stop_words()
        self.count = 0
        self.__max_term_appearance = 0
        self.__max_term = ''
        self.__length_of_all_terms = 0
        self.RE_WORD = re.compile(r"""[\#\@\w](['\-]?\w){2,24}""", re.UNICODE)

    def add_stop_words(self):
        """
        This function add all the stop words to stop word set .
        :param -
        :return: -
        """
        stop_word_list = ['www', 'http', 'https', 'html', 'com', 'co', 'il', 'ru', 'fr' 'a', 'b', 'c', 'd', 'e', 'f'
            , 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'ad', 'ae', 'af', 'ag', 'ai', 'al', 'al', 'an', 'ao'
            , 'ar', 'as', 'at', 'au', 'ca', 'rktnjsg', 'cm', 'li', 'qu', 'de', 'wo', 'bui', 'am', 'pm'
                                                                                                  'o', 'p', 'q', 'r',
                          's', 't', 'u', 'v', 'w', 'x', 'y', 'z', ':', '', ' ', 'rt' ':', ',',
                          '.', '/', '<', '>', ';', "'", '|', '*', '-', '=', 'rt', '+', '_', 'bit', 'ly', 'qu', 'ny'
                                                                                                               '(', ')',
                          '{', '}', '[', ']', '"', '%', '!', '$', '`', '~', '’', '#', '@', 'please', 'bn', 'tge'
            , 'yo', 'aj', 'ach', 'st', 'cesspoo', 'ex', 'nd', 'heeh', 'ie', 'cannot', 'would'
                          ]
        corpus_stopwords = ["category", "references", "also", "external", "links",
                            "may", "first", "see", "history", "people", "one", "two",
                            "part", "thumb", "including", "second", "following",
                            "many", "however", "would", "became"]
        stop_word_set = set(stop_word_list)

        self.stop_words_set.update(stop_word_set)
        self.stop_words_set.update(set(corpus_stopwords))

    def percent_parse(self, percent_number):
        """
        this function parsing number that contain percent
        and add them to the dictionaries
        :param percent_number : number contains percent from text
        :param term_dict: dictionary of terms
        :return: -
        """
        if not percent_number.isascii():
            return list()
        percent_list = []
        if percent_number[-1] == '%':
            percent_list.append(percent_number)
        elif 'percent' in percent_number.lower():
            percent = ''
            for char in percent_number:
                if char == ' ':
                    break
                else:
                    percent += char
            percent_number += '%'
            percent_list.append(percent)
        return percent_list


    def help_number_parse(self, num, kind=None):
        if not str(num).isascii():
            return list()
        """
        this function parsing numbers from text
        and add them to the dictionaries
        :param num : number contains percent from text
        :param term_dict: dictionary of terms
        :param kind: represent the letter after the number
        :return: -
        """
        try:
            numbers_list = []
            if type(num) is int or type(num) is float:
                if num < 1000:
                    numbers_list.append(str(num))
                elif num < 1000000:
                    num = round((float(num) / 1000), 3)
                    if num.is_integer():
                        num = int(num)
                    else:
                        num = round(num, 3)
                    numbers_list.append(str(num) + 'K')
                elif num < 1000000000:
                    num = round((float(num) / (1000 ** 2)), 3)
                    if num.is_integer():
                        num = int(num)
                    else:
                        num = round(num, 3)
                    numbers_list.append(str(num) + 'M')
                else:
                    num = round((float(num) / (1000 ** 3)), 3)
                    if num.is_integer():
                        num = int(num)
                    else:
                        num = round(num, 3)
                    numbers_list.append(str(num) + 'B')

            else:
                if round(float(num), 3) < 1000:
                    if float(num).is_integer():
                        numbers_list.append(str(int(num)) + kind)
                    else:
                        numbers_list.append(str(round(float(num))) + kind)
                elif round(float(num), 3) < 1000000:
                    if float(int(num) / 1000).is_integer():
                        if kind == 'K':
                            numbers_list.append(str(int(int(num) / 1000)) + 'M')
                        elif kind == 'M':
                            numbers_list.append(str(int(int(num) / 1000)) + 'B')
                    else:
                        if kind == 'K':
                            numbers_list.append(str(round(float(int(num) / 1000), 3)) + 'M')
                        elif kind == 'M':
                            numbers_list.append(str(round(float(int(num) / 1000), 3)) + 'B')
            return numbers_list
        except:
            return []

    def number_parse(self, number):
        """
        this function parsing numbers from text
        and add them to the dictionaries
        :param number : number contains percent from text
        :param term_dict: dictionary of terms
        :return: -
        """
        if not number.isascii():
            return list()
        if number.lower() == 'thousand':
            return self.help_number_parse('1', 'K')
        elif number.lower() == 'million':
            return self.help_number_parse('1', 'M')
        elif number.lower() == 'billion':
            return self.help_number_parse('1', 'B')
        if 'thousand' in number.lower():
            num = number[:len(number) - len('thousand')]
            return self.help_number_parse(num, "K")
        elif 'million' in number.lower():
            num = number[:len(number) - len('million')]
            return self.help_number_parse(num, "M")
        elif 'billion' in number.lower():
            num = number[:len(number) - len('billion')]
            return self.help_number_parse(num, "B")
        else:
            try:
                number = round(float(number), 3)
                if number.is_integer():
                    number = int(number)
                return self.help_number_parse(number)
            except:
                return []

    def belong_number(self, term):
        term = term.lower()
        if 'million' == term or 'milion' == term:
            return True, 'million'
        if 'thousand' == term or 'thousands' == term:
            return True, 'thousand'
        if 'billion' == term or 'bilion' == term:
            return True, 'billion'
        if term == '%' or 'percent' in term:
            return True, '%'
        return False, ''

    def operate_tokens(self, tokens_list_before_operation):
        operated_tokens = []
        need_pass = False
        for index, token in enumerate(tokens_list_before_operation):
            if need_pass:
                need_pass = False
                continue
            if token.isdigit():
                if index + 1 < len(tokens_list_before_operation):
                    next_term = tokens_list_before_operation[index + 1]
                    is_belong_to_number, add_to_term = self.belong_number(next_term)
                    if is_belong_to_number:
                        term_with_next = token + add_to_term
                        operated_tokens.append(term_with_next.lower())
                        need_pass = True
                    else:
                        operated_tokens.append(token.lower())
                else:
                    operated_tokens.append(token.lower())
            else:
                operated_tokens.append(token.lower())
        return operated_tokens

    def parse_sentence(self, text, stemming=False, body=False):
        """
        This function tokenize, remove stop words and apply lower case for every word within the text
        :param body:
        :param stemming:
        :param text:
        :return:
        """

        list_of_parsed_terms = []
        string = text
        if body:
            operated_tokens = [token.group() for token in self.RE_WORD.finditer(text.lower())]
        else:
            string = re.sub(r'(\D)(\d+)%', r'\1 \2% ', string)
            string = re.sub(r'(\S)@', r'\1 @', string)
            string = re.sub(r'(\S)#', r'\1 #', string)
            string = re.sub(r'\$', 'S', string)
            string = re.sub(r'(\d+)([a-zA-Z])', r'\1 \2', string)
            string = re.sub(r'(\d),(\d)', r'\1\2', string)
            string = re.sub(r'(\D)\.', r'\1 ', string)
            regx_string = re.split('\s|\b|!|\a|\(|\)|-|\?|~|[^a-zA-Z0-9_@#%]', string)
            text_tokens_without_stopwords = [term for term in regx_string if term.lower() not in self.stop_words_set and len(term) > 0]
            operated_tokens = self.operate_tokens(text_tokens_without_stopwords)

        for term in operated_tokens:
            if term[0].isdigit():
                if '%' in term:
                    if len(term) > 6:
                        continue
                    else:
                        list_of_parsed_terms.extend(self.percent_parse(term))
                else:
                    if len(term) > 14:
                        continue
                    else:
                        list_of_parsed_terms.extend(self.number_parse(term))
            else:
                list_of_parsed_terms.append(term)
        if stemming:
            stemming_list = self.return_finished_parsed_tokens_list(list_of_parsed_terms, stem=True)
            return stemming_list
        finished_parsed_terms = self.return_finished_parsed_tokens_list(list_of_parsed_terms)
        return finished_parsed_terms

    def return_finished_parsed_tokens_list(self, list_of_parsed_terms, stem=False):
        finished_parsed_terms = []
        for token in list_of_parsed_terms:
            if stem:
                stem = Stemmer()
                token = stem.stem_term(token)
            if len(token) < 1:
                continue
            if token.lower() in self.stop_words_set:
                continue
            if not token[0] == '#' and not token[0] == '@':
                if token[0].islower():
                    token = token.lower()
                else:
                    token = token.upper()
            count_chars = 1
            for idx, char in enumerate(token):
                if idx + 1 < len(token) and char == token[idx + 1]:
                    count_chars += 1
                if count_chars == 3 and not char.isdigit():
                    count_chars = 1
                    continue
                if count_chars == 11:
                    count_chars = 1
                    continue
            finished_parsed_terms.append(token)
        return finished_parsed_terms

    def add_term(self, term, term_dict, entities_dict):
        if term[0].isupper():
            if term.lower() in term_dict.keys():
                term_dict[term.lower()] = term_dict[term.lower()] + 1
                upper_term = term.upper()
                if upper_term in entities_dict.keys():
                    if entities_dict[upper_term] > 1:
                        entities_dict[upper_term] = entities_dict[upper_term] - 1
                    else:
                        del entities_dict[upper_term]
        else:
            if term in term_dict.keys():
                term_dict[term] = term_dict[term] + 1
            else:
                term_dict[term] = 1

    def parse_doc(self, doc_as_list, kind=None, stemm=False):
        """
        This function takes a wikipedia document as list and break it into different fields
        :param title:
        :param stemm:
        :param doc_as_list: list re-presenting the wiki page.
        :return: Document object with corresponding fields.

        """
        wiki_id = doc_as_list[0]
        wiki_title = doc_as_list[1]
        wiki_antchors = {x['id']: x['text'] for x in doc_as_list[3]}
        if kind == 'title':
            full_text = wiki_title.lower()
        elif kind == 'body':
            full_text = doc_as_list[2]
        elif kind == 'anchor':
            full_text = ''
            for key in wiki_antchors:
                full_text = full_text + wiki_antchors[key] + ' '
        entities_dict = {}
        term_dict = {}
        all_terms = set()
        if kind == 'body':
            tokenized_text = self.parse_sentence(full_text, stemming=stemm, body=False)
        else:
            tokenized_text = self.parse_sentence(full_text, stemming=stemm)
        doc_length = len(tokenized_text)  # after text operations.
        for term in tokenized_text:
            self.add_term(term, term_dict, {})
            all_terms.add(term)
        length_of_uniqe_term = len(all_terms)
        max_from_entitiy = False
        try:
            term_max = max(term_dict.values())
            try:
                entities_max = max(entities_dict.values())
                if entities_max > term_max:
                    max_from_entitiy = True
                self.__max_term_appearance = max(term_max, entities_max)
            except:
                self.__max_term_appearance = term_max
        except:
            try:
                entities_max = max(entities_dict.values())
                self.__max_term_appearance = entities_max
                max_from_entitiy = True
            except:
                self.__max_term_appearance = 0
        if self.__max_term_appearance > 1:
            if max_from_entitiy:
                self.__max_term = max(entities_dict.items(), key=operator.itemgetter(1))[0]
            else:
                self.__max_term = max(term_dict.items(), key=operator.itemgetter(1))[0]

        else:
            self.__max_term = ''
        self.__length_of_all_terms = len(tokenized_text)
        document = Document(wiki_id, wiki_title, full_text, wiki_antchors,term_dict, doc_length, length_of_uniqe_term,
                            self.__length_of_all_terms, self.__max_term, self.__max_term_appearance)
        return document


