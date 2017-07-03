import numpy as np
from os.path import isfile
from os.path import sep
from tempfile import TemporaryFile

class SudokuData(object):
    """Data wrapper for sudoku problems."""
    def __init__(self, sample_size):
        super(SudokuData, self).__init__()
        self.sample_size = sample_size

    def _load_train_and_test(self):
        from sklearn.model_selection import train_test_split
        #randomly splits the data sample into train and test lots
        x_train, x_test, y_train, y_test = train_test_split(self.problems, self.solutions, test_size=.5)
        self.train = DataBean(x_train, y_train)
        self.test = DataBean(x_test, y_test)

    """Loads data from a previously generated binary npy"""
    def _loadCached(self, path_str_x, path_str_y):
        if isfile(path_str_x) and isfile(path_str_y):
            self.problems = np.load(path_str_x)
            self.solutions = np.load(path_str_y)
            return True
        return False

    def load(self):
        path_str_x = "data"+ sep +"array_x_"+str(self.sample_size)+".npy"
        path_str_y = "data"+ sep +"array_y_"+str(self.sample_size)+".npy"
        if not self._loadCached(path_str_x, path_str_y):
            self.problems = np.zeros((self.sample_size, 81), np.int32)
            self.solutions = np.zeros((self.sample_size, 81), np.int32)
            for i, line in enumerate(open('data/sudoku.csv', 'r').read().splitlines()[1:]):
                quiz, solution = line.split(",")
                for j, q_s in enumerate(zip(quiz, solution)):
                    q, s = q_s
                    self.problems[i, j] = q
                    self.solutions[i, j] = s
                if i == (self.sample_size-1):
                    break
            np.save(path_str_x, self.problems)
            np.save(path_str_y, self.solutions)
        self._load_train_and_test()

class DataBean(object):
    """docstring for DataBean."""
    def __init__(self, x, y):
        super(DataBean, self).__init__()
        self.problems = x
        self.solutions = y
        self.index = 0

    def next_batch(self, batch_size):
        x = self.problems[self.index:self.index+batch_size]
        y = self.solutions[self.index:self.index+batch_size]
        self.index += batch_size
        return x, y

def load_data(size):
    Data = SudokuData(size)
    Data.load()
    return Data
