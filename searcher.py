from ranker import Ranker
import os
import utils


class Searcher:

    def __init__(self, inverted_index_title=None, inverted_index_anchor=None, inverted_index_body=None, body=False, title=False, anchor=False, doc_title=None, doc_body=None, doc_anchor=None):
        """
        :param inverted_index: dictionary of inverted index
        """
        self.ranker = Ranker()
        self.inverted_index_title = inverted_index_title
        self.inverted_index_anchor = inverted_index_anchor
        self.inverted_index_body = inverted_index_body
        self.body = body
        self.title = title
        self.anchor = anchor
        self.doc_title = doc_title
        self.doc_body = doc_body
        self.doc_anchor = doc_anchor

    def get_body(self):
        return self.body

    def get_title(self):
        return self.title

    def get_anchor(self):
        return self.anchor

    def set_body(self):
        self.body = True

    def set_title(self):
        self.title = True

    def set_anchor(self):
        self.anchor = True

    def remove_title(self):
        self.title = False

    def remove_body(self):
        self.body = False

    def remove_anchor(self):
        self.anchor = False

    def relevants_docs(self, list_of_query_terms, kind=None):
        if kind == 'title':
            inver_idx = self.inverted_index_title
        elif kind == 'body':
            inver_idx = self.inverted_index_body
        else:
            inver_idx = self.inverted_index_anchor
        information_docs_dict = {}
        query_result = {}
        postings = {}
        for term in list_of_query_terms:
            if term in inver_idx.keys():
                if term[0].isdigit():
                    letter = 'numbers'
                elif term[0].isalpha():
                    letter = term[0].lower()
                else:
                    while len(term) > 0 and not term[0].isalpha():
                        term = term[0:len(term) - 1]
                if f'{inver_idx[term]}' in postings:
                    pass
                else:
                    postings[f'{inver_idx[term]}'] = utils.load_obj(os.getcwd() + '\\postings\\' + kind + '\\newPostings\\' + f'{inver_idx[term]}')

                list_of_document = postings[f'{inver_idx[term]}'][term][1].keys()  # list of doc_ids for the term
                if self.title:
                    information_docs_dict = {doc: [self.doc_title[doc][0], self.doc_title[doc][1], postings[f'{inver_idx[term]}'][term][1].get(doc, 1)] for doc in list_of_document}
                elif self.anchor:
                    information_docs_dict = {doc: [self.doc_anchor[doc][0], self.doc_anchor[doc][1], postings[f'{inver_idx[term]}'][term][1].get(doc, 1)] for doc in list_of_document}
                elif self.body:
                    information_docs_dict = {doc: [self.doc_body[doc][0], self.doc_body[doc][1], postings[f'{inver_idx[term]}'][term][1].get(doc, 1)] for doc in list_of_document}
                list_of_details = [information_docs_dict, len(information_docs_dict)]
                query_result[term] = list_of_details
            information_docs_dict = {}
        return query_result

    def relevant_docs_from_posting(self, list_of_query_terms, synon=None):
        """
        This function loads the posting list and count the amount of relevant documents per term.
        :param query: query
        :return: dictionary of relevant documents.
        """
        relevance = {'body': None, 'title': None, 'anchor': None}
        if self.body:
            relevance['body'] = self.relevants_docs(list_of_query_terms, kind='body')
        if self.title:
            relevance['title'] = self.relevants_docs(list_of_query_terms, kind='title')
        if self.anchor:
            relevance['anchor'] = self.relevants_docs(list_of_query_terms, kind='anchor')
        return relevance

