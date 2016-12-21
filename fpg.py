# coding=utf-8
import csv
import sys
import time

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
    def returnSupp(self):
        return self.supp
    def setSupp(self, s):
        self.supp = s
    def returnPrev(self):
        return self.prev
    def returnMark(self):
        return self.mark
    def delFromNext(self, pr):
        for next in self.listOfNext:
            if next.product == pr:
                del next

def summClevel(fptr, pridx, dL):
    c = 0
    for node in fptr[pridx]:
        c = c + node.returnSupp()
    return float(c) / dL

def makeNewtree(tree, newtree, inxpr, sProd):
    newtree = list(tree)

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
                prev.delFromNext(sProd[i])
                #dellist.append(j)
        #hlen = len(dellist)
        #for h in range(hlen):
            #del newtree[i][h]

    for elem in newtree[inxpr]:
        elem.NotMark()
        elem.setSupp(1)
        pelem = elem.returnPrev()
        while(pelem != None):
            sum = 0
            nlist = pelem.retListOfNext()
            for n in nlist:
                sum = sum + n.returnSupp()
            pelem.setSupp(sum)
            pelem = pelem.returnPrev()

    for elem in newtree[inxpr]:
        pelem = elem.returnPrev()
        pelem.delFromNext(sProd[inxpr])
    #newtree[inxpr].clear()


def FPFind(sProd, dL, minsup, tree, root, phi, r):
    for inx in range(len(tree) - 1, -1, -1):
        if summClevel(tree, inx, dL) >= minsup:
            p = list(phi)
            p.append(sProd[inx])
            phi.append(sProd[inx])
            r.append(p)
            ntree = []
            makeNewtree(tree, ntree, inx, sProd)
            FPFind(sProd, dL, minsup, ntree, root, phi, r)

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

friquency = {}
for i in range(len(product)):
    s = 0
    for j in range(dataLength):
        s = s + int(data[j][i])
    friquency[i] = s

#print friquency

#отсортировать product по friquency
sortProduct = []
while (len(friquency) != 0):
    pr = max(friquency, key=friquency.get)
    if (float(friquency[pr]) / float(dataLength) < minsup):
        break
    del friquency[pr]
    sortProduct.append(pr)

dataSort = []

print sortProduct
#перебрать построчно data в порядке friquency, формируя списки номеров продуктов, если 1 есть в нужном продукте
for i in range(dataLength):
    transaction = []
    for j in range(len(sortProduct)):
        if int(data[i][sortProduct[j]]) == 1:
            transaction.append(sortProduct[j])
    dataSort.append(transaction)

print dataSort

#построить FPдерево
fptree = []
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

r = []
phi = []
FPFind(sortProduct, dataLength, minsup, fptree, v0, phi, r)

print r

alltime = time.time() - startTime

print (alltime)