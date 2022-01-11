class Document:

    def __init__(self, wiki_id, wiki_title=None, full_text=None, wiki_antchors=None, term_doc_dictionary=None, doc_length=None, length_of_uniqe_term=None, length_of_all_terms=None, max_word=None, max_term_appearance=None):
        """
        :param wiki_id: wiki_id
        :param full_text: full text as string from wikipages
        :param term_doc_dictionary: dictionary of term and documents.
        :param doc_length: doc length
        """
        self.wiki_id = wiki_id
        self.wiki_title = wiki_title
        self.full_text = full_text
        self.wiki_antchors = wiki_antchors
        self.term_doc_dictionary = term_doc_dictionary
        self.doc_length = doc_length
        self.length_of_uniqe_term = length_of_uniqe_term
        self.length_of_all_terms = length_of_all_terms
        self.max_word = max_word
        self.max_term_appearance = max_term_appearance
