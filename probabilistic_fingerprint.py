import hashlib
from collections import Counter
import sys
import numpy as np
from multiprocessing import Pool
import pickle
import imp
np.random.seed(666)
gen_util = imp.load_source('gen_util', 'utils.py')

LOGGER = gen_util.get_logger()

def hash_helper(arguments):
    img = arguments['img']
    idx = arguments['idx']
    window_size = arguments['window_size']
    return hashlib.sha256(img[idx:idx + window_size]).hexdigest()


class InputTracker:
    def __init__(self, query, window_size, num_hashes_keep, round=50, step_size=1, workers=5, salt=None):
        self.window_size = window_size
        self.num_hashes_keep = num_hashes_keep
        self.round = round
        self.step_size = step_size
        if(salt != None):
            self.salt = salt
        else:
            self.salt = np.random.rand(*query.shape) * 255.

        self.hash_dict = {}
        self.output = {}
        self.input_idx = 0
        self.pool = Pool(processes=workers)

    
    def save(self, file):
        tracker_saved = InputTrackerSaveVersion(self.window_size, self.num_hashes_keep, self.round, self.salt, self.hash_dict, self.input_idx)
        pickle.dump(tracker_saved, open(file, "wb"))



    @staticmethod
    def load(file):
        tracker_saved = pickle.load(open(file, "rb"))
        tracker = InputTracker(None, tracker_saved.window_size, tracker_saved.num_hashes_keep, round=tracker_saved.round, workers=5, salt=tracker_saved.salt)
        tracker.hash_dict = tracker_saved.hash_dict
        tracker.input_idx = tracker_saved.input_idx
        return tracker


    def copy(self):
        new_tracker = InputTracker(None, self.window_size, self.num_hashes_keep, self.round, self.step_size, self.salt)
        new_tracker.hash_dict = self.hash_dict.copy()
        new_tracker.input_idx = self.input_idx
        return new_tracker    
    
    def delete(self):
        self.pool.close()
        

    def preprocess(self, array, round=1, normalized=True):
        if(normalized):
            # input image normalized to [0,1]
            array = np.array(array) * 255.
        array = (array + self.salt) % 255.
        array = array.reshape(-1)
        array = np.around(array / round, decimals=0) * round
        array = array.astype(np.int16)
        return array


    def hash_img(self, img, window_size, round, step_size, preprocess=True):
        if preprocess:
            img = self.preprocess(img, round)
        total_len = int(len(img))
        idx_ls = []
        for el in range(int((total_len - window_size + 1) / step_size)):
            idx_ls.append({"idx": el * step_size, "img": img, "window_size": window_size})
        hash_list = self.pool.map(hash_helper, idx_ls)
        hash_list = list(set(hash_list))
        hash_list = [r[::-1] for r in hash_list]
        hash_list.sort(reverse=True)
        return hash_list

    def check_img(self, hashes):
        sets = list(map(self.hash_dict.get, hashes))
        sets = [i for i in sets if i is not None]
        sets = [item for sublist in sets for item in sublist]
        if not sets:
            return 0
        sets = Counter(sets)
        cnt = sets.most_common(1)[0][1]
        return cnt
        
    def add_img(self, img):
        self.input_idx += 1
        hashes = self.hash_img(img, self.window_size, self.round, self.step_size)[:self.num_hashes_keep]
        cnt = self.check_img(hashes)
        for el in hashes:
            if el not in self.hash_dict:
                self.hash_dict[el] = [self.input_idx]
            else:
                self.hash_dict[el].append(self.input_idx)
        return cnt
        

class InputTrackerSaveVersion:
    def __init__(self, window_size, num_hashes_keep, round, salt, hash_dict, input_idx):
        self.window_size = window_size
        self.num_hashes_keep = num_hashes_keep
        self.round = round
        self.salt = salt

        self.hash_dict = hash_dict
        self.input_idx = input_idx
    


