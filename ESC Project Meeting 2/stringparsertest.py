import unittest
#import Iterative_Algo

def sizeStringParser(sizeString): #splits string in cvs entry to list of floats(dimensions)
    returnLS = []
    sizeStringls = sizeString.split("x")
    for i in sizeStringls:
        ils = i.split('m')
        ##print(ils)
        try:
            returnLS.append(float(ils[0]))
        except:
            print("illegal size")
            returnLS = [-1.0,-1.0]
    print(returnLS)

    return returnLS

class MyTest(unittest.TestCase):
    def test_height(self):
        self.assertEqual(sizeStringParser("8m (L) x 5m (B) x 3m (H)"),[8.0,5.0,3.0])

    def test_noheight(self):
        self.assertEqual(sizeStringParser("3m x 2m"),[3.0,2.0])

    def test_extrawords(self):
        self.assertEquals(sizeStringParser("8m x 5m x 4m (for test rig and clearance space for drone flight)"),[8.0,5.0,4.0])

    def test_numbers(self):
        self.assertEquals(sizeStringParser("5 x 4"),[5.0,4.0])
        
    def test_invalid(self):
        self.assertEquals(sizeStringParser("Library iWall and space around it (Already confirmed with SUTD Library)"),[-1.0,-1.0])

if __name__ == '__main__':
    unittest.main()