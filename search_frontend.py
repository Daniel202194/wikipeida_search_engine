import os
from thesaurus import Thesaurus
import utils
from collections import defaultdict
from flask import Flask, request, jsonify
from MultiFileReader import MultiFileReader
from parser_module import Parse
from searcher import Searcher
from inverted_index_gcp import InvertedIndex
BLOCK_SIZE = 1999998
p = Parse()
synon = Thesaurus()
from flask_ngrok import run_with_ngrok


class MyFlaskApp(Flask):
    def run(self, host=None, port=None, debug=None, **options):
        super(MyFlaskApp, self).run(host=host, port=port, debug=debug, **options)


app = MyFlaskApp(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False


def relevant_postings(postings_list):
    reader = MultiFileReader()
    tf_list = {}
    for w, locs in postings_list.items():
        b = reader.read(locs, index.df[w] * TUPLE_SIZE)
        tf_list = {}
        for i in range(index.df[w]):
            doc_id = int.from_bytes(b[i * TUPLE_SIZE:i * TUPLE_SIZE + 4], 'big')
            tf = int.from_bytes(b[i * TUPLE_SIZE + 4:(i + 1) * TUPLE_SIZE], 'big')
            if doc_id in tf_list:
                tf_list[doc_id][w] = tf
            else:
                tf_list[doc_id] = {w: tf}
    return tf_list


def load_index(kind):
    inverted_index = utils.load_obj(kind)
    return inverted_index


def details(kind):
    path_postings = os.getcwd() + '\\' + 'postings'
    dir_doc_body_path = path_postings + '\\' + kind + '\\' + 'Documents'
    doc_path_body = dir_doc_body_path + '\\' + 'documents' + '.txt'
    document_body_file = open(doc_path_body, 'r')
    lines_of_file = document_body_file.readlines()
    document_body_file.close()
    return lines_of_file


def merge_top_k(list1, list2, tw, bw):
    new_list = []
    list1 = sorted(list1, key=lambda item: item[0], reverse=True)
    list2 = sorted(list2, key=lambda item: item[0], reverse=True)
    index_1 = 0
    index_2 = 0
    while index_1 < len(list1) and index_2 < len(list2):
        if list1[index_1][0] > list2[index_2][0]:
            new_elem = (list1[index_1][0], tw*list1[index_1][1])
            new_list.append(new_elem)
            index_1 += 1
        elif list1[index_1][0] < list2[index_2][0]:
            new_elem = (list2[index_2][0], bw*list2[index_2][1])
            new_list.append(new_elem)
            index_2 += 1
        else:
            new_elem = (list2[index_2][0], bw*list2[index_2][1] + tw*list1[index_1][1])
            new_list.append(new_elem)
            index_1 += 1
            index_2 += 1
    while index_1 < len(list1):
        new_elem = (list1[index_1][0], tw*list1[index_1][1])
        new_list.append(new_elem)
        index_1 += 1
    while index_2 < len(list2):
        new_elem = (list2[index_2][0], bw * list2[index_2][1])
        new_list.append(new_elem)
        index_2 += 1
    return sorted(new_list, key=lambda item: item[1], reverse=True)


def rank_docs_body(relevance_doc_tf, idx, query, doc_body, k=100):
    searcher2 = Searcher(inverted_index_body=idx, body=True)
    scored_docs = searcher2.ranker.cosine_similarity(relevance_doc_tf, query, doc_body)
    return searcher2.ranker.retrieve_top_k(scored_docs,k,wiki_titles)


def search_and_rank_query(query, wiki_title=None, k=100, d_title=[], d_anchor=[], d_body=[], search_type='bin',):

    query_as_list = p.parse_sentence(query)
    relevant_docs = searcher.relevant_docs_from_posting(query_as_list, synon)
    if search_type == 'bin':
        if searcher.title:
            return searcher.ranker.binary_rank(query_as_list, relevant_docs['title'], wiki_title=wiki_title)
        else:
            return searcher.ranker.binary_rank(query_as_list, relevant_docs['anchor'], wiki_title=wiki_title)
    else:
        if searcher.body:
            ranked_docs_body = searcher.ranker.rank_relevant_doc(relevant_docs['body'], d_body)
        if searcher.title:
            ranked_docs_title = searcher.ranker.rank_relevant_doc(relevant_docs['title'], d_title)
        if searcher.anchor:
            ranked_docs_anchor = searcher.ranker.rank_relevant_doc(relevant_docs['anchor'], d_anchor)
    if not searcher.body and not searcher.title:
        return searcher.ranker.retrieve_top_k(ranked_docs_anchor, k, wiki_title=wiki_title)
    elif not searcher.body and not searcher.anchor:
        return searcher.ranker.retrieve_top_k(ranked_docs_title, k, wiki_title=wiki_title)
    elif not searcher.anchor and not searcher.title:
        return searcher.ranker.retrieve_top_k(ranked_docs_body, k, wiki_title=wiki_title)
    else:
        new_k = (k*2) + 1
        if searcher.body and searcher.title:
            merge_boyd_title = merge_top_k(ranked_docs_title, ranked_docs_body, 0.35, 0.65)
            return searcher.ranker.retrieve_top_k(merge_boyd_title, wiki_title=wiki_title)
        elif searcher.body and searcher.anchor:
            merge_body_anchor = merge_top_k(ranked_docs_body[:new_k], ranked_docs_anchor[:new_k], 0.65, 0.35)
            return searcher.ranker.retrieve_top_k(merge_body_anchor, wiki_title=wiki_title)
        elif searcher.title and searcher.anchor:
            merge_title_anchor = merge_top_k(ranked_docs_title[:new_k], ranked_docs_anchor[:new_k], 0.85, 0.15)
            return searcher.ranker.retrieve_top_k(merge_title_anchor, wiki_title=wiki_title)


def get_data(kind):
    if kind == 'title':
        path = os.getcwd() + '\\' + 'postings\\title'
    elif kind == 'body':
        path = os.getcwd() + '\\' + 'postings\\body'
    else:
        path = os.getcwd() + '\\' + 'postings\\anchor'
    dir_data_path = path + '\\' + 'data'
    data_path = dir_data_path + '\\' + 'data' + '.txt'
    document_file = open(data_path, 'r')
    lines_of_data_file = document_file.readlines()
    document_file.close()
    return lines_of_data_file


def precision_at_k(true_list, predicted_list, k=40):
    new_predicted = predicted_list[:k]
    relevants = [x for x in new_predicted if x in true_list]
    res = round(len(relevants) / len(new_predicted), 3)
    return res if res < 1 else 1


def calculate_map_at_k(true_list, res, k=40):
    new_predicted = res[:k]
    indexex = [i + 1 for i in range(len(new_predicted)) if new_predicted[i] in true_list]
    precisions = [precision_at_k(true_list, res, i) for i in indexex]
    try:
        res = round(sum(precisions) / len(precisions), 3)
    except:
        return 0
    return res if res < 1 else 1

path = os.getcwd() + '\\postings\\'
index_path_title = path + 'title\\newPostings\\inverted_index_title'
index_path_anchor = path + 'anchor\\newPostings\\inverted_index_anchor'
index_path_body = path + 'body\\newPostings\\inverted_index_body'

old_index_path_body = path + 'body\\newPostings_2\\inverted_index_body'

inverted_index_title = load_index(index_path_title)
inverted_index_body = load_index(index_path_body)
inverted_index_anchor = load_index(index_path_anchor)
wiki_titles = utils.load_obj('titles_ids_2')
documents_body = utils.load_obj(path + 'body\\Documents')
documents_title = utils.load_obj(path + 'title\\Documents')
documents_anchor = utils.load_obj(path + 'anchor\\Documents')
data_titles = get_data('title')
data_anchor = get_data('anchor')
data_body = get_data('body')
index = InvertedIndex.read_index('', 'postings_gcp_index')
index_page_views = utils.load_obj('pageviews')
index_page_rank = utils.load_obj('page_rank_index')
searcher = Searcher(inverted_index_title, inverted_index_anchor, inverted_index_body, doc_title=documents_title, doc_body=documents_body, doc_anchor=documents_anchor)
TUPLE_SIZE = 6


@app.route("/search")
def search():
    ''' Returns up to a 100 of your best search results for the query. This is 
        the place to put forward your best search engine, and you are free to
        implement the retrieval whoever you'd like within the bound of the 
        project requirements (efficiency, quality, etc.). That means it is up to
        you to decide on whether to use stemming, remove stopwords, use 
        PageRank, query expansion, etc.

        To issue a query navigate to a URL like:
         http://YOUR_SERVER_DOMAIN/search?query=hello+world
        where YOUR_SERVER_DOMAIN is something like XXXX-XX-XX-XX-XX.ngrok.io
        if you're using ngrok on Colab or your external IP on GCP.
    Returns:
    --------
        list of up to 100 search results, ordered from best to worst where each 
        element is a tuple (wiki_id, title).
    '''
    # start = time.time()
    res = []
    query = request.args.get('query', '')
    if len(query) == 0:
        return jsonify(res)

    while not searcher.get_body():
        searcher.set_body()
    while not searcher.get_title():
        searcher.set_title()
    try:
        res = search_and_rank_query(wiki_title=wiki_titles, query=query, d_body=data_body, d_title=data_titles, search_type='notbin')
    except:
        while searcher.get_body():
            searcher.remove_body()
        while searcher.get_title():
            searcher.remove_title()
        return jsonify(res)
    while searcher.get_body():
        searcher.remove_body()
    while searcher.get_title():
        searcher.remove_title()
    return jsonify(res)


@app.route("/search_body")
def search_body():
    ''' Returns up to a 100 search results for the query using TFIDF AND COSINE
        SIMILARITY OF THE BODY OF ARTICLES ONLY. DO NOT use stemming. DO USE the 
        staff-provided tokenizer from Assignment 3 (GCP part) to do the 
        tokenization and remove stopwords. 

        To issue a query navigate to a URL like:
         http://YOUR_SERVER_DOMAIN/search_body?query=hello+world
        where YOUR_SERVER_DOMAIN is something like XXXX-XX-XX-XX-XX.ngrok.io
        if you're using ngrok on Colab or your external IP on GCP.
    Returns:
    --------
        list of up to 100 search results, ordered from best to worst where each 
        element is a tuple (wiki_id, title).
    '''
    res = []
    query = request.args.get('query', '')

    if len(query) == 0:
        return jsonify(res)
    # BEGIN SOLUTION
    try:
        new_query = p.parse_sentence(query, body=True)
        postings_list = defaultdict(list)
        for term in new_query:
            postings_list[term] = index.posting_locs[term]
        relevants_doc_tf = relevant_postings(postings_list)
        res = rank_docs_body(relevants_doc_tf, index, new_query, documents_body)
    except:
        return jsonify(res)
    # END SOLUTION
    return jsonify(res)


@app.route("/search_title")
def search_title():
    ''' Returns ALL (not just top 100) search results that contain A QUERY WORD 
        IN THE TITLE of articles, ordered in descending order of the NUMBER OF 
        QUERY WORDS that appear in the title. For example, a document with a 
        title that matches two of the query words will be ranked before a 
        document with a title that matches only one query term. 

        Test this by navigating to the a URL like:
         http://YOUR_SERVER_DOMAIN/search_title?query=hello+world
        where YOUR_SERVER_DOMAIN is something like XXXX-XX-XX-XX-XX.ngrok.io
        if you're using ngrok on Colab or your external IP on GCP.
    Returns:
    --------
        list of ALL (not just top 100) search results, ordered from best to 
        worst where each element is a tuple (wiki_id, title).
    '''
    res = []
    query = request.args.get('query', '')
    if len(query) == 0:
        return jsonify(res)
    # BEGIN SOLUTION
    try:
        while not searcher.get_title():
            searcher.set_title()
        res = search_and_rank_query(wiki_title=wiki_titles, query=query, k=7000000, d_title=data_titles, search_type='bin')
    except:
        while searcher.get_title():
            searcher.remove_title()
        return jsonify(res)
    # END SOLUTION
    while  searcher.get_title():
        searcher.remove_title()
    return jsonify(res)


@app.route("/search_anchor")
def search_anchor():
    ''' Returns ALL (not just top 100) search results that contain A QUERY WORD 
        IN THE ANCHOR TEXT of articles, ordered in descending order of the 
        NUMBER OF QUERY WORDS that appear in anchor text linking to the page. 
        For example, a document with a anchor text that matches two of the 
        query words will be ranked before a document with anchor text that 
        matches only one query term. 

        Test this by navigating to the a URL like:
         http://YOUR_SERVER_DOMAIN/search_anchor?query=hello+world
        where YOUR_SERVER_DOMAIN is something like XXXX-XX-XX-XX-XX.ngrok.io
        if you're using ngrok on Colab or your external IP on GCP.
    Returns:
    --------
        list of ALL (not just top 100) search results, ordered from best to 
        worst where each element is a tuple (wiki_id, title).
    '''

    res = []
    query = request.args.get('query', '')
    if len(query) == 0:
        return jsonify(res)
    # BEGIN SOLUTION
    try:
        while not searcher.get_anchor():
            searcher.set_anchor()
        res = search_and_rank_query(wiki_title=wiki_titles, query=query, k=7000000, d_anchor=data_anchor, search_type='bin')
    except:
        while searcher.get_anchor():
            searcher.remove_anchor()
        return jsonify(res)
    # END SOLUTION
    while searcher.get_anchor():
        searcher.remove_anchor()
    return jsonify(res)


@app.route("/get_pagerank", methods=['POST'])
def get_pagerank():
    ''' Returns PageRank values for a list of provided wiki article IDs. 

        Test this by issuing a POST request to a URL like:
          http://YOUR_SERVER_DOMAIN/get_pagerank
        with a json payload of the list of article ids. In python do:
          import requests
          requests.post('http://YOUR_SERVER_DOMAIN/get_pagerank', json=[1,5,8])
        As before YOUR_SERVER_DOMAIN is something like XXXX-XX-XX-XX-XX.ngrok.io
        if you're using ngrok on Colab or your external IP on GCP.
    Returns:
    --------
        list of floats:
          list of PageRank scores that correrspond to the provided article IDs.
    '''
    res = []
    wiki_ids = request.get_json()
    if len(wiki_ids) == 0:
        return jsonify(res)
    #
    # BEGIN SOLUTION
    for id in wiki_ids:
        try:
            res.append(float(index_page_rank[str(id)]))
        except:
            res.append(0)
    # END SOLUTION
    return jsonify(res)


@app.route("/get_pageview", methods=['POST'])
def get_pageview():
    ''' Returns the number of page views that each of the provide wiki articles
        had in August 2021.

        Test this by issuing a POST request to a URL like:
          http://YOUR_SERVER_DOMAIN/get_pageview
        with a json payload of the list of article ids. In python do:
          import requests
          requests.post('http://YOUR_SERVER_DOMAIN/get_pageview', json=[1,5,8])
        As before YOUR_SERVER_DOMAIN is something like XXXX-XX-XX-XX-XX.ngrok.io
        if you're using ngrok on Colab or your external IP on GCP.
    Returns:
    --------
        list of ints:
          list of page view numbers from August 2021 that correrspond to the 
          provided list article IDs.
    '''
    res = []
    wiki_ids = request.get_json()
    if len(wiki_ids) == 0:
        return jsonify(res)
    # BEGIN SOLUTION
    for id in wiki_ids:
        try:
            res.append(index_page_views[int(id)])
        except:
            res.append(0)
    # END SOLUTION
    return jsonify(res)

if __name__ == '__main__':
    # run the Flask RESTful API, make the server publicly available (host='0.0.0.0') on port 8080
    # app.run(host='0.0.0.0', port=8080, debug=True)
    run_with_ngrok(app)
    app.run()