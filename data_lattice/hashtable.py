# Code adapted from Santho Shhari
# https://santhoshhari.github.io/Locality-Sensitive-Hashing/

import numpy as np
import random
import math
import hashlib
import functools
import mmh3
import matplotlib.pyplot as plt

class Murmur3HashTable:
    def __init__(self, num_buckets, floats = False):
        self.hash_function = functools.partial(mmh3.hash, seed = 1)
        self.num_buckets = num_buckets
        self.hash_table = dict()
        self.floats = floats

    def generate_hash(self, inp_vector):
        inp_str = ''
        if self.floats:
            inp_str = ','.join(['{:.10f}'.format(x) for x in inp_vector])
        else:
            inp_str = ','.join(map(str, inp_vector))
        return self.hash_function(inp_str) % self.num_buckets

    def __setitem__(self, inp_vec):
        hash_value = self.generate_hash(inp_vec)
        if hash_value in self.hash_table:
            self.hash_table[hash_value] = self.hash_table[hash_value] + 1
        else:
            self.hash_table[hash_value] = 1

    def makeDict(self, name):
        f = open('dict_murmur_' + name + '.txt', "w")
        maxKey = 0
        maxKeyNum = 0
        for key in self.hash_table.keys():
            f.write(str(key) + ' : ' + str(self.hash_table[key]) + '\n')
            if maxKeyNum < self.hash_table[key]:
                maxKey = key
                maxKeyNum = self.hash_table[key]
        f.close()
        # print(str(maxKey) + ' ' + str(maxKeyNum))

    def __getitem__(self, inp_vec):
        hash_value = self.generate_hash(inp_vec)
        if hash_value in self.hash_table:
            return self.hash_table[hash_value]
        else:
            return 0

    def conflicts(self):
        nConflicts = 0
        nBuckets = 0
        for key in self.hash_table.keys():
            nBuckets += 1
            if self.hash_table[key] > 1:
                nConflicts += 1
        return float(nConflicts)/nBuckets, float(nConflicts)/self.num_buckets, \
                float(self.num_buckets)/nBuckets

    def generateScatter(self, name):
        x = []
        y = []
        plt.figure(figsize=(30,10))
        for key in sorted(self.hash_table.keys()):
            x.append(key)
            y.append(self.hash_table[key])
        plt.scatter(x, y)
        plt.savefig('scatter_murmur_' + name + '.png')
        plt.close()

    def generateBar(self, name):
        bars = dict()
        for key in self.hash_table:
            if self.hash_table[key] in bars:
                bars[self.hash_table[key]] = bars[self.hash_table[key]] + 1
            else:
                bars[self.hash_table[key]] = 1
        x = []
        y = []
        for key in sorted(bars.keys()):
            x.append(key)
            y.append(bars[key])
        plt.bar(x, y)
        plt.title('Element Distribution in Buckets for Murmur3: ' + name)
        plt.xlabel('Number of Elements in a Bucket')
        plt.ylabel('Number of Buckets')
        plt.savefig('bar_murmur_' + name + '.png')
        plt.close()


class BuiltInHashTable:
    def __init__(self, num_buckets, floats = False):
        self.num_buckets = num_buckets
        self.hash_table = dict()
        self.floats = floats

    def generate_hash(self, inp_vector):
        inp_str = ''
        if self.floats:
            inp_str = ','.join(['{:.10f}'.format(x) for x in inp_vector])
        else:
            inp_str = ','.join(map(str, inp_vector))
        return int(hashlib.md5(inp_str.encode('utf-8')).hexdigest(), 16) % self.num_buckets

    def __setitem__(self, inp_vec):
        hash_value = self.generate_hash(inp_vec)
        if hash_value in self.hash_table:
            self.hash_table[hash_value] = self.hash_table[hash_value] + 1
        else:
            self.hash_table[hash_value] = 1

    def makeDict(self, name):
        f = open('dict_builtin_' + name + '.txt', "w")
        maxKey = 0
        maxKeyNum = 0
        for key in self.hash_table.keys():
            f.write(str(key) + ' : ' + str(self.hash_table[key]) + '\n')
            if maxKeyNum < self.hash_table[key]:
                maxKey = key
                maxKeyNum = self.hash_table[key]
        f.close()
        # print(str(maxKey) + ' ' + str(maxKeyNum))

    def __getitem__(self, inp_vec):
        hash_value = self.generate_hash(inp_vec)
        if hash_value in self.hash_table:
            return self.hash_table[hash_value]
        else:
            return 0

    def conflicts(self):
        nConflicts = 0
        nBuckets = 0
        for key in self.hash_table.keys():
            nBuckets += 1
            if self.hash_table[key] > 1:
                nConflicts += 1
        return float(nConflicts)/nBuckets, float(nConflicts)/self.num_buckets, \
                float(self.num_buckets)/nBuckets

    def generateScatter(self, name):
        x = []
        y = []
        plt.figure(figsize=(30,10))
        for key in sorted(self.hash_table.keys()):
            x.append(key)
            y.append(self.hash_table[key])
        plt.scatter(x, y)
        plt.savefig('scatter_builtin_' + name + '.png')
        plt.close()

    def generateBar(self, name):
        bars = dict()
        for key in self.hash_table:
            if self.hash_table[key] in bars:
                bars[self.hash_table[key]] = bars[self.hash_table[key]] + 1
            else:
                bars[self.hash_table[key]] = 1
        x = []
        y = []
        for key in sorted(bars.keys()):
            x.append(key)
            y.append(bars[key])
        plt.bar(x, y)
        plt.title('Element Distribution in Buckets for MD5: ' + name)
        plt.xlabel('Number of Elements in a Bucket')
        plt.ylabel('Number of Buckets')
        plt.savefig('bar_builtin_' + name + '.png')
        plt.close()

class PolyHashTable:
    def __init__(self, num_buckets, inp_dimensions):
        random.seed(137)
        self.num_buckets = num_buckets
        self.inp_dimensions = inp_dimensions
        self.hash_table = dict()
        self.coef = random.randint(0, self.num_buckets)

    def generate_hash(self, inp_vector):
        num = 0.0
        for i in range(self.inp_dimensions):
            num += ((self.coef ** (self.inp_dimensions - i - 1))*inp_vector[i])
        return str(int(math.fmod(abs(num), self.num_buckets)))

    def __setitem__(self, inp_vec, label='added'):
        hash_value = self.generate_hash(inp_vec)
        if hash_value in self.hash_table:
            self.hash_table[hash_value] = self.hash_table[hash_value] + 1
        else:
            self.hash_table[hash_value] = 1

    def makeDict(self, name):
        f = open('dict_poly_' + name + '.txt', "w")
        maxKey = 0
        maxKeyNum = 0
        for key in self.hash_table.keys():
            f.write(str(key) + ' : ' + str(self.hash_table[key]) + '\n')
            if maxKeyNum < self.hash_table[key]:
                maxKey = key
                maxKeyNum = self.hash_table[key]
        f.close()
        # print(str(maxKey) + ' ' + str(maxKeyNum))
        
    def __getitem__(self, inp_vec):
        hash_value = self.generate_hash(inp_vec)
        if hash_value in self.hash_table:
            return self.hash_table[hash_value]
        else:
            return 0

    def conflicts(self):
        nConflicts = 0
        nBuckets = 0
        for key in self.hash_table.keys():
            nBuckets += 1
            if self.hash_table[key] > 1:
                nConflicts += 1
        return float(nConflicts)/nBuckets, float(nConflicts)/self.num_buckets, \
                float(self.num_buckets)/nBuckets

    def generateScatter(self, name):
        x = []
        y = []
        plt.figure(figsize=(30,10))
        for key in sorted(self.hash_table.keys()):
            x.append(key)
            y.append(self.hash_table[key])
        plt.scatter(x, y)
        plt.savefig('scatter_poly_' + name + '.png')
        plt.close()

    def generateBar(self, name):
        bars = dict()
        for key in self.hash_table:
            if self.hash_table[key] in bars:
                bars[self.hash_table[key]] = bars[self.hash_table[key]] + 1
            else:
                bars[self.hash_table[key]] = 1
        x = []
        y = []
        for key in sorted(bars.keys()):
            x.append(key)
            y.append(bars[key])
        plt.bar(x, y)
        plt.title('Element Distribution in Buckets for PolynomialHash: ' + name)
        plt.xlabel('Number of Elements in a Bucket')
        plt.ylabel('Number of Buckets')
        plt.savefig('bar_poly_' + name + '.png')
        plt.close()
    
class HashTable:
    def __init__(self, hash_size, inp_dimensions):
        self.hash_size = hash_size
        self.inp_dimensions = inp_dimensions
        self.hash_table = dict()
        self.projections = np.random.randn(self.hash_size, inp_dimensions)
        
    def generate_hash(self, inp_vector):
        nums = np.dot(inp_vector, self.projections.T) 
        bools = (np.dot(inp_vector, self.projections.T) > 0).astype('int')
        return ''.join(bools.astype('str'))

    def __setitem__(self, inp_vec, label='added'):
        hash_value = self.generate_hash(inp_vec)
        if hash_value in self.hash_table:
            self.hash_table[hash_value] = self.hash_table[hash_value] + 1
        else:
            self.hash_table[hash_value] = 1
        # self.hash_table[hash_value] = self.hash_table\
            # .get(hash_value, list()) + [label]

    def makeDict(self, name):
        f = open('dict_' + name + '.txt', "w")
        maxKey = 0
        maxKeyNum = 0
        for key in self.hash_table.keys():
            f.write(str(key) + ' : ' + str(self.hash_table[key]) + '\n')
            if maxKeyNum < self.hash_table[key]:
                maxKey = key
                maxKeyNum = self.hash_table[key]
        f.close()
        # print(str(maxKey) + ' ' + str(maxKeyNum))
        
    def __getitem__(self, inp_vec):
        hash_value = self.generate_hash(inp_vec)
        if hash_value in self.hash_table:
            return self.hash_table[hash_value]
        else:
            return 0
        # return self.hash_table.get(hash_value, [])

    def getProjections(self):
        return self.projections

    def conflicts(self):
        nConflicts = 0
        nBuckets = 0
        for key in self.hash_table.keys():
            nBuckets += 1
            if self.hash_table[key] > 1:
                nConflicts += 1
        return float(nConflicts)/nBuckets, float(nConflicts)/(2 ** self.hash_size), \
                float((2**self.hash_size))/nBuckets

    def generateScatter(self, name):
        x = []
        y = []
        plt.figure(figsize=(30,10))
        for key in sorted(self.hash_table.keys()):
            x.append(key)
            y.append(self.hash_table[key])
        plt.scatter(x, y)
        plt.savefig('scatter_normal_' + name + '.png')
        plt.close()


