# coding=utf-8
import csv
import sys
import time
import copy

class FPNode:
    def __init__(self, f = None, pv = None, sv = None, cv = 0):
        self.product = f
        if sv == None:
            self.listOfNext = []
        else:
            self.listOfNext = sv
        self.prev = pv
        self.supp = cv
        self.mark = False
    def addSupp(self):
        self.supp = self.supp + 1
    def Mark(self):
        self.mark = True
    def NotMark(self):
        self.mark = False
    def addNext(self, next):
        self.listOfNext.append(next)
    def retListOfNext(self):
        return self.listOfNext
    def isProductInNext(self, pr):
        if len(self.listOfNext) == 0:
            return None
        nextNode = None
        for node in self.listOfNext:
            if node.product == pr:
                nextNode = node
                break
        return nextNode
    def returnPr(self):
        return self.product
    def returnSupp(self):
        return self.supp
    def setSupp(self, s):
        self.supp = s
    def returnPrev(self):
        return self.prev
    def returnMark(self):
        return self.mark
    def delFromNext(self, pr):
        for i in range(len(self.listOfNext)):
            if self.listOfNext[i].product == pr:
                del self.listOfNext[i]
                break

def summClevel(fptr, pridx, dL):
    c = 0
    for node in fptr[pridx]:
        c = c + node.returnSupp()
    return (float(c) / dL)

def MakeFPTree(fptree, sortProduct, dataSort):
    for i in sortProduct:
        fptree.append(list())
    v0 = FPNode()
    for d in dataSort:
        v = v0
        for pr in d:
            n = v.isProductInNext(pr)
            if n == None:
                n = FPNode(pr, v)
                v.addNext(n)
                fptree[sortProduct.index(pr)].append(n)
            v = n
            v.addSupp()
    return v0

def SortProductByFrequency(sortProduct, frequency, dataLength, minsup):
    while (len(frequency) != 0):
        pr = max(frequency, key=frequency.get)
        if (float(frequency[pr]) / float(dataLength) < minsup):
            break
        del frequency[pr]
        sortProduct.append(pr)

def SortingDataTransactions(dataLength, sortProduct, dataSort, data):
    for i in range(dataLength):
        transaction = []
        for j in range(len(sortProduct)):
            if int(data[i][sortProduct[j]]) == 1:
                transaction.append(sortProduct[j])
        dataSort.append(transaction)

def makeNewtree(newtree, inxpr, sProd):

    for elem in newtree[inxpr]:
        elem.Mark()
        pelem = elem.returnPrev()
        while(pelem != None):
            pelem.Mark()
            pelem = pelem.returnPrev()

    for i in range(len(newtree)):
        dellist = []
        for j in range(len(newtree[i])):
            if newtree[i][j].returnMark() == False:
                prev = newtree[i][j].returnPrev()
                if prev != None:
                    prev.delFromNext(sProd[i])
                dellist.append(j)

        hlen = len(dellist)
        for h in range(hlen - 1, -1, -1):
            del newtree[i][dellist[h]]

    for elem in newtree[inxpr]:
        elem.NotMark()
        pelem = elem.returnPrev()
        while(pelem != None):
            pelem.NotMark()
            sum = 0
            nlist = pelem.retListOfNext()
            for n in nlist:
                sum = sum + n.returnSupp()
            pelem.setSupp(sum)
            pelem = pelem.returnPrev()

    for elem in newtree[inxpr]:
        pelem = elem.returnPrev()
        pelem.delFromNext(sProd[inxpr])
    newtree[inxpr] = []


def FPFind(sProd, dL, minsup, tree, root, phi, r, arOfSets):
    for inx in range(len(tree) - 1, -1, -1):
        s = summClevel(tree, inx, dL)
        if s >= minsup:
            p = list(phi)
            p.append(sProd[inx])
            r.append(p)
            sizeOfSet = len(p)
            if len(arOfSets) < sizeOfSet:
                arOfSets.append(dict())
            arOfSets[sizeOfSet - 1][tuple(sorted(p))] = s
            ntree = copy.deepcopy(tree)
            makeNewtree(ntree, inx, sProd)
            FPFind(sProd, dL, minsup, ntree, root, p, r, arOfSets)

def assocRules(r, p, x, mconf, sets):
    for idx in range(len(p)):
        if len(x) == 0 or p[idx] > x[-1]:
            p1 = list(p)
            p1.pop(idx)
            x1 = list(x)
            x1.append(p[idx])
            temp = sorted(p1 + x1)
            suppTemp = sets[len(temp) - 1][tuple(temp)]
            suppP1 = sets[len(p1) - 1][tuple(p1)]
            conf = float(suppTemp) / float(suppP1)
            if conf > mconf:
                r[0].append(tuple(p1))
                r[1].append(tuple(x1))
                if len(p1) > 1:
                    assocRules(r, p1, x1, mconf, sets)

if __name__ == "__main__":

    dataFileName = sys.argv[1]
    minsup = float(sys.argv[2])
    minconf = float(sys.argv[3])

    data = []
    dataLength = 0
    with open(dataFileName, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            del row[:1]
            data.append(row)
            dataLength = dataLength + 1


    startTime = time.time()

    product = [i for i in range(len(data[0]))]

    frequency = {}
    for i in range(len(product)):
        s = 0
        for j in range(dataLength):
            s = s + int(data[j][i])
        frequency[i] = s

    #отсортировать product по frequency
    sortProduct = []
    SortProductByFrequency(sortProduct, frequency, dataLength, minsup)

    #перебрать построчно data в порядке frequency, формируя списки номеров продуктов, если 1 есть в нужном продукте
    dataSort = []
    SortingDataTransactions(dataLength, sortProduct, dataSort, data)

    #построить FPдерево
    fptree = []
    v0 = MakeFPTree(fptree, sortProduct, dataSort)

    r = []
    phi = []
    fptree1 = copy.deepcopy(fptree)
    arrayOfSets = []
    FPFind(sortProduct, dataLength, minsup, fptree1, v0, phi, r, arrayOfSets)

    #вывести правила
    rules = []
    rules.append(list())
    rules.append(list())
    for set in r:
        if len(set) == 1:
            continue
        phi = sorted(list(set))
        y = list()
        assocRules(rules, phi, y, minconf, arrayOfSets)

    alltime = time.time() - startTime
    print (alltime)

    for i in range(len(rules[1])):
        print(str(rules[0][i]) + " -> " + str(rules[1][i]))

