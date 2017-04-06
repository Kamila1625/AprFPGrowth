import unittest
import copy
from fpg import(
    SortProductByFrequency,
    SortingDataTransactions,
    summClevel,
    MakeFPTree,
    makeNewtree,
    FPFind,
    assocRules,
)

class TestFPG(unittest.TestCase):
    def setUp(self):
        self.data = []
        self.data.append([1, 0, 0, 1, 0, 1, 0])
        self.data.append([1, 0, 1, 1, 1, 0, 0])
        self.data.append([0, 1, 0, 1, 0, 0, 0])
        self.data.append([0, 1, 1, 1, 0, 0, 0])
        self.data.append([0, 1, 1, 0, 0, 0, 0])
        self.data.append([1, 1, 0, 1, 0, 0, 0])
        self.data.append([0, 1, 0, 1, 1, 0, 0])
        self.data.append([0, 1, 1, 0, 1, 0, 1])
        self.data.append([0, 0, 1, 1, 0, 1, 0])
        self.data.append([1, 1, 0, 1, 0, 0, 0])
        self.resSupp = {}
        self.resSupp[0] = 4 #0 a
        self.resSupp[1] = 7 #1 b
        self.resSupp[2] = 5 #2 c
        self.resSupp[3] = 8 #3 d
        self.resSupp[4] = 3 #4 e
        self.resSupp[5] = 2 #5 f
        self.resSupp[6] = 1 #6 g

        self.resSortSupp = [3, 1, 2, 0, 4]

        self.dataLen = len(self.data)
        self.rulesRes = []
        self.rulesRes.append(list())
        self.rulesRes.append(list())
        self.rulesRes[0].append(tuple((0, 1)))
        self.rulesRes[1].append(tuple((3, )))
        self.sets = []

        self.sortDataTransactions = []
        self.sortDataTransactions.append([3, 0])
        self.sortDataTransactions.append([3, 2, 0, 4])
        self.sortDataTransactions.append([3, 1])
        self.sortDataTransactions.append([3, 1, 2])
        self.sortDataTransactions.append([1, 2])
        self.sortDataTransactions.append([3, 1, 0])
        self.sortDataTransactions.append([3, 1, 4])
        self.sortDataTransactions.append([1, 2, 4])
        self.sortDataTransactions.append([3, 2])
        self.sortDataTransactions.append([3, 1, 0])

        self.frArrSuppLen1 = {(3, ): 0.8,
                              (1, ): 0.7,
                              (2, ): 0.5}
        self.frArrSuppLen2 = {(1, 3): 0.5}

        self.testArSet = [{(0,): 0.4, (1, ): 0.7, (3, ): 0.8},
                          {(1, 3): 0.5, (0, 1): 0.2, (0, 3): 0.4},
                          {(0, 1, 3): 0.2}]


    def test_Rules(self):
        rules = []
        rules.append(list())
        rules.append(list())
        p = list({0, 1, 3})
        x = []
        assocRules(rules, p, x, 0.8, self.testArSet)
        for i in range(len(rules[0])):
            self.assertEqual((rules[0][i], rules[1][i]), (self.rulesRes[0][i], self.rulesRes[1][i]), "False rules")

    def test_sortProduct(self):
        sortProduct = []
        SortProductByFrequency(sortProduct, self.resSupp, self.dataLen, 0.3)
        self.assertEqual(sortProduct, self.resSortSupp, "False frequency")

    def test_dataSort(self):
        sortProduct = []
        SortProductByFrequency(sortProduct, self.resSupp, self.dataLen, 0.3)
        dataSort = []
        SortingDataTransactions(self.dataLen, sortProduct, dataSort, self.data)
        self.assertEqual(dataSort,  self.sortDataTransactions, "False dating sort")

    def test_makeFPTree(self):
        sortProduct = []
        SortProductByFrequency(sortProduct, self.resSupp, self.dataLen, 0.3)
        dataSort = []
        SortingDataTransactions(self.dataLen, sortProduct, dataSort, self.data)
        fptree = []
        v0 = MakeFPTree(fptree, sortProduct, dataSort)
        vList = v0.retListOfNext()
        self.assertEqual(len(vList), 2, "False root of tree")
        self.assertEqual(vList[0].returnPr(), 3, "False root0 product of tree")
        self.assertEqual(vList[1].returnPr(), 1, "False root1 product of tree")
        self.assertEqual(vList[0].returnSupp(), 8, "False root0 value of tree")
        self.assertEqual(vList[1].returnSupp(), 2, "False root1 value of tree")
        self.assertEqual(len(fptree), 5, "False len of tree")
        self.assertEqual(len(fptree[4]), 3, "False num of lists")
        self.assertEqual(summClevel(fptree, 2, self.dataLen), 0.5, "False summ of level")
        makeNewtree(fptree, len(fptree) - 1, sortProduct)
        vNewList = v0.retListOfNext()
        self.assertEqual(len(vNewList), 2, "False root of new tree")
        self.assertEqual(vNewList[0].returnPr(), 3, "False root0 product of new tree")
        self.assertEqual(vNewList[0].returnSupp(), 2, "False root0 value of new tree")
        self.assertEqual(vNewList[1].returnPr(), 1, "False root1 product of tree")
        self.assertEqual(vNewList[1].returnSupp(), 1, "False root1 value of tree")
        self.assertEqual(len(fptree[4]), 0, "False num of new tree lists")

    def test_FPFind(self):
        sortProduct = []
        SortProductByFrequency(sortProduct, self.resSupp, self.dataLen, 0.5)
        dataSort = []
        SortingDataTransactions(self.dataLen, sortProduct, dataSort, self.data)
        fptree = []
        v0 = MakeFPTree(fptree, sortProduct, dataSort)
        r = []
        phi = []
        fptree1 = copy.deepcopy(fptree)
        arrayOfSets = []
        FPFind(sortProduct, self.dataLen, 0.5, fptree1, v0, phi, r, arrayOfSets)
        for i in self.frArrSuppLen1.keys():
            self.assertEqual(self.frArrSuppLen1[i], arrayOfSets[0][i], "False array Of Sets1")
        for i in self.frArrSuppLen2.keys():
            self.assertEqual(self.frArrSuppLen2[i], arrayOfSets[1][i], "False array Of Sets2")