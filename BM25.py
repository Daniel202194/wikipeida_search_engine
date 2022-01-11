from math import log


class BM25:

    def __init__(self):
        self.k1 = 1.2
        self.k2 = 100
        self.b = 0.75
        self.R = 0

    def score_BM25(self, n, f, qf, r, N, dl, avdl):
        """
        this function calulate the score and return it
        and add them to the dictionaries
        :param n : length of document dictionary
        :param f: frequncy of the term in document
        :param qf: permanent
        :param r: permanent
        :param N: length od documents in corpus
        :param dl: length of document
        :param avdl: average of length of documents in corpus
        :return: score
        """
        K = self.compute_K(dl, avdl)
        first = log(((r + 0.5)/(self.R - r + 0.5))/((n - r + 0.5)/(N - n - self.R + r + 0.5)))
        second = ((self.k1 + 1) * f)/(K + f)
        third = ((self.k2+1) * qf)/(self.k2 + qf)
        return first * second * third

    def compute_K(self,dl, avdl):
        """
        this function calulate  and return the outcome
        and add them to the dictionaries
        :param dl: length of document
        :param avdl: average of length of documents in corpus

        :return: return the calculation
        """
        return self.k1 * ((1-self.b) + self.b * (float(dl)/float(avdl)))
