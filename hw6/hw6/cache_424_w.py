# Noam Stanislawski

'''
Base class file for Cache
Credit: R. Martin (W&M), A. Jog (W&M), Ramulator (CMU)
'''

import numpy as np
from math import log2, ceil
import random


class Cache:
    def __init__(self, cSize, ways=1, bSize=4):

        self.cacheSize = cSize  # Bytes
        self.ways = ways        # Default: 1 way (i.e., directly mapped)
        self.blockSize = bSize  # Default: 4 bytes (i.e., 1 word block)
        self.sets = cSize // bSize // ways
        print(cSize,bSize,ways)
        print(self.sets)

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
    Warning: DO NOT EDIT ANYTHING ABOVE THIS LINE
    '''


    '''
    Returns the set number of an address based on the policy discussed in the class
    Do NOT change the function definition and arguments
    '''

    def find_set(self, address):
        if address >= self.cacheSize // self.ways:
            return (address % (self.cacheSize // self.ways)) >> int(log2(self.blockSize))
        else:
            return address >> int(log2(self.blockSize))

    '''
    Returns the tag of an address based on the policy discussed in the class
    Do NOT change the function definition and arguments
    '''

    def find_tag(self, address):
        return address // (self.cacheSize // self.ways)

    '''
    Search through cache for address
    return True if found
    otherwise False
    Do NOT change the function definition and arguments
    '''

    def find(self, address):
        if address in self.cache:
        #    print(self.cache[self.find_set(address)])
            way = np.amin(self.metaCache[self.find_set(address)]) % self.ways
            self.hit += 1
            self.metaCache[self.find_set(address)][way] += 1

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
        way = 0

        if address in self.cache:
            return None

        if self.ways < 2: # DIRECT MAP
            if self.blockSize == 4: # 1 block = 1 word
                addr = address
                col = address % self.blockSize
                if address >= self.cacheSize:
                    set = (address % self.cacheSize) >> int(log2(self.blockSize))
                else:
                    set = address >> int(log2(self.blockSize))

                self.cache.itemset((set, way, col), addr)

            else: # multi-word block
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

                    self.cache.itemset((set, way, col), i)


        else: # ASSOCIATIVE CACHE
            if self.blockSize == 4: #1 word block
                addr = address
                col = address % self.blockSize
                set = self.find_set(address)

                for i in range(len(self.metaCache[set])):
                    if self.metaCache[set][i] == -1:
                        self.cache.itemset((set, i, col), addr)
                        self.metaCache[set][i] += 1
                        return None

                # Didn't find empty spot, needs to replace with LRU
        #        way = self.metaCache[set].index(min(self.metaCache[set]))
                way = np.argmin(self.metaCache[set])
                self.cache.itemset((set, way, col), addr)
                self.metaCache[set][way] += 1

            else: # multi-word block
                way = None

                if address % self.blockSize == 0:
                    lw = (address, address + self.blockSize)
                else:
                    highvalue = ceil(address / self.blockSize) * self.blockSize
                    lowvalue = highvalue - self.blockSize
                    lw = (lowvalue,highvalue)


                set = self.find_set(address)

                for i in range(len(self.metaCache[set])):
                    if self.metaCache[set][i] == -1: #found empty spot
                        #self.cache.itemset((set, i, col), addr)
                        way = i
                        self.metaCache[set][i] += 1
                        break

                # Didn't find empty spot, needs to replace with LRU
        #        way = self.metaCache[set].index(min(self.metaCache[set]))
                if way == None:
                    way = np.argmin(self.metaCache[set])
                    self.metaCache[set][way] += 1

                for i in range(lw[0],lw[1]):
                    col = i % self.blockSize
                    if i >= self.cacheSize // self.ways:
                        set = (i % (self.cacheSize // self.ways)) >> int(log2(self.blockSize))
                    else:
                        set = i >> int(log2(self.blockSize))

                    self.cache.itemset((set, way, col), i)
