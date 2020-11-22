import numpy as np
import random

class DataSet:
    def __init__(self, path):
        self.importFile(path)
    def importFile(self, path):
        f = open(path, "r")
        line = f.readline()
        lines = []
        while line != "":
            line = line.rstrip().split(" ")
            line = list(map(int, line))
            lines.append(set(line))
            line = f.readline()

        self.data = lines

    def initWeightsFreq(self):
        weights = []
        sumweights = 0
        for t in self.data:
            weight = 2**len(t)
            sumweights += weight
            weights.append(weight)
        self.weights = weights
        self.sumweights = sumweights
    def initWeightsArea(self):
        weights = []
        sumweights = 0
        for t in self.data:
            D_size = len(t)
            weight = D_size * (2**D_size - 1)
            sumweights += weight
            weights.append(weight)
        self.weights = weights
        self.sumweights = sumweights

    def samplePatternFreq(self):
        tirage = random.randint(0,self.sumweights)
        sumprogress = 0
        for i in range(len(self.data)):
            t = self.data[i]
            sumprogress += self.weights[i]
            if(sumprogress>=tirage):
                break
        pattern = []
        for i in range(len(t)):
            tirage = random.random()
            if(tirage<0.5):
                pattern.append(list(t)[i])
        pattern = set(pattern)
        return pattern

    def samplePatternArea(self):
        tirage = random.randint(0,self.sumweights)
        sumprogress = 0
        for i in range(len(self.data)):
            t = self.data[i]
            sumprogress += self.weights[i]
            if(sumprogress>=tirage):
                break
        D_size = len(t)
        # tirage de k
        total = (D_size * (D_size + 1))/2
        tirage = random.randint(1,total)
        sumprogress = 0
        for i in range(D_size+1):
            sumprogress += i
            if(sumprogress>=tirage):
                k = i
                break
        pattern = set(random.sample(t,k))
        # freq = 0
        # for t in self.data:
            # if(pattern.issubset(t)):
                # freq +=1
        # return (pattern, freq*len(pattern))
        return pattern

    def getRealisationsFreq(self, n):
        self.initWeightsFreq()
        patterns = []
        c = 0
        while c<n:
            p = self.samplePatternFreq()
            if(p not in patterns):
                c += 1
                patterns.append(p)       
        patterns_freq = []
        for pattern in patterns:
            freq = 0
            for t in self.data:
                if(pattern.issubset(t)):
                    freq +=1
            patterns_freq.append((pattern, freq))
        return patterns_freq

    def getRealisationsArea(self, n):
        self.initWeightsArea()
        patterns = []
        c = 0
        while c<n:
            p = self.samplePatternArea()
            if(p not in patterns):
                c += 1
                patterns.append(p)       
        patterns_area = []
        for pattern in patterns:
            freq = 0
            for t in self.data:
                if(pattern.issubset(t)):
                    freq +=1
            patterns_area.append((pattern, freq*len(pattern)))
        return patterns_area
    def patternSimilarity(self,patterns):
        n = len(patterns)
        sumprogress = 0
        c = 0
        for i in range(0, n):
            for j in range(i+1, n):
                intersection = len(patterns[i][0].intersection(patterns[j][0]))
                union = len(patterns[i][0].union(patterns[j][0]))
                #indice de jaccard
                sumprogress += float(intersection)/float(union)
                c += 1
        #moyenne des indices de jaccard
        return sumprogress/c


if __name__ == '__main__':
    D = DataSet("mushroom.dat")
    patterns_freq = D.getRealisationsFreq(1000)
    # patterns_area = D.getRealisationsArea(1000)
    
    print(D.patternSimilarity(patterns_freq))
    # set_union = set()
    # set_inter = patterns_freq[0][0]
    # for i in range(0, len(patterns_freq)):
        # pat = patterns_freq[i][0]
        # set_union = set_union.union(pat)
        # set_inter = set_inter.intersection(pat)
    
    # AIRE
    # D.initWeightsArea()
    # patterns_area = []
    # c = 0
    # while c<1000:
        # p = D.samplePatternArea()
        # if(p not in patterns_area):
            # c += 1
            # patterns_area.append(p)
    # print(len(patterns_area))
