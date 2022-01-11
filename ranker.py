import math
from BM25 import BM25


class Ranker:
    def __init__(self):
        pass

    @staticmethod
    def cosine_similarity(relevants_doc_tf, query, doc_body):
        docs_size = {}
        docs_query_sigma = {}
        scores = {}
        query_size = math.sqrt(len(set(query)))
        for doc_id in relevants_doc_tf:
            for word in relevants_doc_tf[doc_id]:
                docs_query_sigma[doc_id] = docs_query_sigma.get(doc_id, 0) + query.count(word)*relevants_doc_tf[doc_id][word]
            try:
                docs_size[doc_id] = math.sqrt(int(doc_body[doc_id][1]))
            except:
                docs_size[doc_id] = 1
            scores[doc_id] = docs_query_sigma[doc_id]/(docs_size[doc_id]*query_size)
        sorted_doc_score = sorted(scores.items(), key=lambda item: item[1], reverse=True)
        # sorted_doc_scores = [(x[0], wiki_title[int(x[0])]) for x in sorted_doc_score]
        # sorted_doc_scores = [(x[0], x[1]) for x in sorted_doc_score]
        return sorted_doc_score
    @staticmethod
    def binary_rank(list_of_query_terms,  relevance_docs, wiki_title):
        scores = {}
        for token in list_of_query_terms:

            for doc_id in relevance_docs[token][0]:
                scores[doc_id] = scores.get(doc_id, 0) + int(relevance_docs[token][0][doc_id][2])
        sorted_doc_score = sorted(scores.items(), key=lambda item: item[1], reverse=True)
        sorted_doc_scores = [(int(x[0]), wiki_title[int(x[0])]) for x in sorted_doc_score]
        return sorted_doc_scores

    @staticmethod
    def rank_relevant_doc(relevant_doc, lines_of_data_file):
        """
        This function provides rank for each relevant document and sorts them by their scores.
        The current score considers solely the number of terms shared by the wiki page (full_text) and query.
        :param wiki_title:
        :param lines_of_data_file:
        :param relevant_doc: dictionary of documents that contains at least one term from the query.
        :return: sorted list of documents by score
        """
        doc_score = {}
        average_of_corpus_doc = float(lines_of_data_file[0])
        corpus_size = int(lines_of_data_file[1])
        bm25 = BM25()
        for term in relevant_doc.keys():
            for doc in relevant_doc[term][0].keys():
                score = bm25.score_BM25(relevant_doc[term][1], int(relevant_doc[term][0][doc][2]), 1, 0, corpus_size, relevant_doc[term][0][doc][0], average_of_corpus_doc)
                if doc in doc_score.keys():
                    doc_score[doc] += score
                else:
                    doc_score[doc] = score

        sorted_doc_score = sorted(doc_score.items(), key=lambda item: item[1], reverse=True)
        sorted_doc_scores = [(int(x[0]), x[1]) for x in sorted_doc_score]
        return sorted_doc_scores

    @staticmethod
    def retrieve_top_k(sorted_relevant_doc, k=100, wiki_title=None):
        """
        return a list of top K wiki articles based on their ranking from highest to lowest
        :param sorted_relevant_doc: list of all candidates docs.
        :param k: Number of top document to return
        :return: list of relevant document
        """

        docs = sorted_relevant_doc[:k]
        return [(int(x[0]), wiki_title[int(x[0])]) for x in docs]
