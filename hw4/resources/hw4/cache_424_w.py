
# Write team member names here:
# Noam Stanislawski

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

        self.blockBits = 0
        self.setBits = 0

        if (self.blockSize != 1):
            self.blockBits = int(log2(self.blockSize))

        if (self.sets != 1):
            self.setBits = int(log2(self.sets))

        self.cache = np.zeros((self.sets, self.ways, self.blockSize), dtype=int)
        self.cache = self.cache - 1

        self.metaCache = np.zeros((self.sets, self.ways), dtype=int)
        self.metaCache = self.metaCache - 1

        self.hit = 0
        self.miss = 0
        self.hitlatency = 1 # cycle
        self.misspenalty = 10 # cycle

    def reset(self):
        self.cache = np.zeros((self.sets, self.ways, self.blockSize), dtype=int)
        self.cache = self.cache - 1

        self.metaCache = np.zeros((self.sets, self.ways), dtype=int)
        self.metaCache = self.metaCache - 1

        self.hit = 0
        self.miss = 0

    '''
    Warning: DO NOT EDIT ANYTHING ABOVE THIS LINE
    '''


    '''
    Returns the set number of an address based on the policy discussed in the class
    Do NOT change the function definition and arguments
    '''

    def find_set(self, address):
        if address >= self.cacheSize:
            return (address % self.cacheSize) >> int(log2(self.blockSize))
        else:
            return address >> int(log2(self.blockSize))
        return None

    '''
    Returns the tag of an address based on the policy discussed in the class
    Do NOT change the function definition and arguments
    '''

    def find_tag(self, address):
        return address // self.cacheSize

    '''
    Search through cache for address
    return True if found
    otherwise False
    Do NOT change the function definition and arguments
    '''

    def find(self, address):
        if address in self.cache:
            self.hit += 1
            return True
        else:
            self.miss += 1
            return False

    '''
    Load data into the cache.
    Something might need to be evicted from the cache and send back to memory
    Do NOT change the function definition and arguments
    '''

    def load(self, address):
        if address in self.cache:
            return None


        if self.blockSize > 4: #multi word blocks
            if self.find_set(address) == 1 or address == 0:
                lw = (address,address+ self.blockSize)
            else:
                lw = (address,address+(self.blockSize//2))

            address = address >> (self.blockSize // 4 - 1)
            for i in range(lw[0],lw[1]):
                col = i % self.blockSize
                if i >= self.cacheSize:
                    set = (i % self.cacheSize) >> int(log2(self.blockSize))
                else:
                    set = i >> int(log2(self.blockSize))

                self.cache.itemset((set, 0, col), i)

        else: # 1 word in a block
            addr = address
            col = address % self.blockSize
            if address >= self.cacheSize:
                set = (address % self.cacheSize) >> int(log2(self.blockSize))
            else:
                set = address >> int(log2(self.blockSize))

            self.cache.itemset((set, 0, col), addr) #can't have 0 for associative

if __name__ == "__main__":
    c = Cache(64,1,4)
    for i in range(0,61,4):
        c.load(i)
        print(i,"\n",c.cache,"\n\n")
    c.load(132)
    print(print(132,"\n",c.cache,"\n\n"))
