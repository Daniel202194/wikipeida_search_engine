import os
import pandas as pd


class ReadFile:
    def __init__(self, corpus_path, isIndexer=False,isPosting=False):
        self.corpus_path = corpus_path
        if isIndexer:
            self.list_of_files_name = self.get_files_names_index()
        else:
            self.list_of_files_name = self.get_files_names(isPosting)
        self.current_file = 0

    def get_files_names(self, is_posting=False):

        files_name = []
        for sub_dir, dirs, files in os.walk(self.corpus_path):
            for file in files:
                if not is_posting:
                    if os.path.splitext(file)[1] == '.parquet':
                        files_name.append(os.path.join(sub_dir, file))
                else:
                    files_name.append(os.path.join(sub_dir, file))
        return files_name

    def get_files_names_index(self):
        files_name = []
        for sub_dir, dirs, files in os.walk(self.corpus_path):
            for file in files:
                files_name.append(os.path.join(sub_dir, file))
        return files_name

    def read_file(self, file_name):
        """
        This function is reading a parquet file contains several wikipedia
        The file location is given as a string as an input to this function.
        :param file_name: string - indicates the path to the file we wish to read.
        :return: a dataframe contains wikipedia articles.
        """
        full_path = ''
        if self.corpus_path not in file_name:
            full_path = os.path.join(self.corpus_path, file_name)
        else:
            full_path = file_name
        df = pd.read_parquet(full_path, engine="pyarrow")
        list_files = df.values.tolist()
        return list_files

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_file < len(self.list_of_files_name):
            self.current_file += 1
            return self.list_of_files_name[self.current_file - 1]
        raise StopIteration
