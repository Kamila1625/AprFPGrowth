# coding=utf-8
import csv
import sys
import time

def supp(l, phi, d):
    support = 0
    if l == 0:
        return 0
    for i in range(l):
        findini = 0
        for j in range(len(phi)):
            findini = findini + int(d[i][phi[j]])
        if findini == len(phi):
            support = support + 1
    return support / float(l)

def condSupp(l, phi, y, d):
    return supp(l, sorted(phi + y), d) / float(supp(l, phi, d))

def assocRules(r, p, x, mconf, l, d):
    for idx in range(len(p)):
        if len(x) == 0 or p[idx] > x[-1]:
            p1 = list(p)
            p1.pop(idx)
            x1 = list(x)
            x1.append(p[idx])
            if condSupp(l, p1, x1, d) > mconf:
                r[0].append(tuple(p1))
                r[1].append(tuple(x1))
                if len(p1) > 1:
                    assocRules(r, p1, x1, mconf, l, d)

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

    friquency = []

    for i in range(len(product)):
        phi = list()
        phi.append(i)
        friquency.append(supp(dataLength, phi, data))

    L0 = {}
    for i in range(len(product)):
        if friquency[i] >= minsup:
            l = []
            l.append(i)
            t = tuple(l)
            L0[t] = friquency[i]

    k = 1
    L = []
    L.append(L0)

    while len(L[k - 1]) != 0:
        Lk = {}
        for key0 in L0:
            for keyk1 in L[k - 1]:
                ck = []
                if keyk1.count(key0[0]) == 0:
                    if key0[0] > keyk1[-1]:
                        ck = list(keyk1)
                        ck.append(key0[0])
                inxpop = 0
                if k > 1:
                    #составить комбинации из ck
                    # проверить их наличие в Lk-1
                    for i in range(len(ck)):
                        ck1 = list(ck)
                        ck1.pop(i)
                        if tuple(ck1) in L[k - 1]:
                            inxpop = inxpop + 1
                #если наличие есть
                if (inxpop == len(ck) or k == 1) and len(ck) != 0:
                    #считаем support для ck
                    s = supp(dataLength, ck, data)
                    #если support >= minsup
                    if s >= minsup:
                        # добавляем ck в Lk вместе с его support
                        Lk[tuple(ck)] = s
        L.append(Lk)
        k = k + 1


    #вывести правила
    rules = []
    rules.append(list())
    rules.append(list())
    for i in range(1, k - 1):
        for key in L[i]:
            phi = list(key)
            y = list()
            assocRules(rules, phi, y, minconf, dataLength, data)

    alltime = time.time() - startTime

    print (alltime)
    for i in range(len(rules[1])):
        print(str(rules[0][i]) + " -> " + str(rules[1][i]))


