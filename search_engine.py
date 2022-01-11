from reader import ReadFile
from configuration import ConfigClass
from parser_module import Parse
from Indexer import Indexer
import os
import utils
import time


def run_engine():
    """

    :return:
    """
    number_of_documents = 0
    config = ConfigClass()
    r = ReadFile(corpus_path=config.get__corpusPath())
    p = Parse()
    indexer = Indexer(config)
    begin = time.time()
    index_kind = ['anchor', 'title', 'body']
    for kind in index_kind:
        print('starting kind: {}'.format(kind))
        for file in os.listdir(r.corpus_path):
            begin_file = time.time()
            documents_list = r.read_file(file_name=file)
            print('begin parsing file : {} with {} wikipedia docs'.format(file, len(documents_list)))
            for idx, document in enumerate(documents_list):
                parsed_document = p.parse_doc(document, kind)
                number_of_documents += 1
                indexer.add_new_doc(parsed_document)
                if number_of_documents == 200000:
                    number_of_documents = 0
                    indexer.write_to_disk(kind)
                    indexer.clear()
            finished_doc = (time.time()-begin_file)/60
            print('finished parse in: {}'.format(finished_doc))
        if number_of_documents < 200000:
            indexer.write_to_disk(kind)
            indexer.clear()
        end_parse_and_write = (time.time() - begin) / 60
        print("Finished parsing and indexing: " + str(end_parse_and_write) + " minutes")
        start_merge = time.time()
        indexer.begin_to_merge(kind)
        finish_mege = (time.time() - start_merge) / 60
        print("Finished merge: " + str(finish_mege) + " minutes")
        indexer.pointer_terms('title')
        utils.save_obj(indexer.titles, "titles_ids")


def load_index():
    print('Load inverted index')
    inverted_index = utils.load_obj("inverted_idx")
    return inverted_index



def main():
    run_engine()
