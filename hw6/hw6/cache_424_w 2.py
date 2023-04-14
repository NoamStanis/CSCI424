
'''
Base class file for Cache
Credit: R. Martin (W&M), A. Jog (W&M), Ramulator (CMU)
'''

import numpy as np
from math import log2
import random

class Cache:
    def __init__(self, cSize, ways=1, bSize=4):
        
        self.cacheSize = cSize  # Bytes
        self.ways = ways        # Default: 1 way (i.e., directly mapped)
        self.blockSize = bSize  # Default: 4 bytes (i.e., 1 word block)
        self.sets = cSize // bSize // ways

        self.blockBits = 0  # blockBits is the sum of byte offset bits (always 2 bits as one word has 4 bytes) and block offset bits
        self.setBits = 0

        if (self.blockSize != 1):
            self.blockBits = int(log2(self.blockSize))

        if (self.sets != 1):
            self.setBits = int(log2(self.sets))

        self.cache = np.zeros((self.sets, self.ways, self.blockSize), dtype=np.int64)
        self.cache = self.cache - 1

        self.metaCache = np.zeros((self.sets, self.ways), dtype=np.int64)
        self.metaCache = self.metaCache - 1

        self.hit = 0
        self.miss = 0
        self.hitlatency = 5 # cycle

    def reset(self):
        self.cache = np.zeros((self.sets, self.ways, self.blockSize), dtype=np.int64)
        self.cache = self.cache - 1

        self.metaCache = np.zeros((self.sets, self.ways), dtype=np.int64)
        self.metaCache = self.metaCache - 1

        self.hit = 0
        self.miss = 0
        
    '''
    Warning: DO NOT EDIT Anything Above
    '''


    '''
    Returns the set number of an address based on the policy discussed in the class
    '''

    def find_set(self, address):
        pass

    '''
    Returns the tag of an address based on the policy discussed in the class
    '''
    
    def find_tag(self, address):
        pass

    '''
    Search through cache for address
    return True if found
    otherwise False
    '''

    def find(self, address):
        pass
    
    '''
    Load data into the cache. 
    Something might need to be evicted from the cache and send back to memory
    '''
   
    def load(self, address):
        pass
