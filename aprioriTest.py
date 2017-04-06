import unittest
from mapriori import(
    supp,
    condSupp,
    assocRules,
)
class TestMapriori(unittest.TestCase):
    def setUp(self):
        self.data = []
        self.resSupp = []
        self.arrCondSupp = []
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
        self.dataLen = len(self.data)
        self.dataProd = len(self.data[0])
        self.resSupp.append(float(4) / self.dataLen)
        self.resSupp.append(float(7) / self.dataLen)
        self.resSupp.append(float(5) / self.dataLen)
        self.resSupp.append(float(8) / self.dataLen)
        self.resSupp.append(float(3) / self.dataLen)
        self.resSupp.append(float(2) / self.dataLen)
        self.resSupp.append(float(1) / self.dataLen)
        self.dictForSupp = {(0, 1): float(2) / self.dataLen,
                            (0, 2): float(1) / self.dataLen,
                            (0, 3): float(4) / self.dataLen,
                            (0, 4): float(1) / self.dataLen,
                            (0, 5): float(1) / self.dataLen,
                            (0, 6): float(0) / self.dataLen,
                            (0, 1, 3): float(2) / self.dataLen,
                            (2, 3): float(3) / self.dataLen,
                            }
        self.arrCondSupp.append(1)
        self.arrCondSupp.append(1)
        self.arrCondSupp.append(0.5)
        self.condSuppPhi = []
        self.condSuppPhi.append(list({0}))
        self.condSuppPhi.append(list({0, 1}))
        self.condSuppPhi.append(list({0}))
        self.condSuppY = []
        self.condSuppY.append(list({3}))
        self.condSuppY.append(list({3}))
        self.condSuppY.append(list({1, 3}))
        self.rulesRes = []
        self.rulesRes.append(list())
        self.rulesRes.append(list())
        self.rulesRes[0].append(tuple((0, 1)))
        self.rulesRes[1].append(tuple((3, )))

    def test_Rules(self):
        rules = []
        rules.append(list())
        rules.append(list())
        p = list({0, 1, 3})
        x = []
        assocRules(rules, p, x, 0.8, self.dataLen, self.data)
        for i in range(len(rules[0])):
            self.assertEqual((rules[0][i], rules[1][i]), (self.rulesRes[0][i], self.rulesRes[1][i]), "False rules")

    def test_Supp(self):
        for i in range(self.dataProd):
            self.assertEqual(supp(self.dataLen, list({i}), self.data), self.resSupp[i], "False support 1")
        for key in self.dictForSupp.keys():
            self.assertEqual(supp(self.dataLen, list(key), self.data), self.dictForSupp[key], "False support")

    def test_CondSupp(self):
        for i in range(len(self.arrCondSupp)):
            self.assertEqual(condSupp(self.dataLen, self.condSuppPhi[i], self.condSuppY[i], self.data),
                             self.arrCondSupp[i], "False cond support")

if __name__ == '__main__':
    unittest.main()
