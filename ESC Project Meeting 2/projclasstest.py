import unittest
#import Iterative_Algo

class project:

    project_FloorSpaceID = -1
    project_Name = "Default"
    project_Pillar = "SUTD"
    project_Length = 1.0
    project_Width = 1.0
    project_Dimensions = [1.0,1.0]
    project_Area = 1.0
    project_Placed = False
    project_Position = [0.0,0.0]

    def __init__(self, name, pillar, length, width):
        self.project_Position = [0.0,0.0]
        self.project_Name = name
        self.project_Length = length
        self.project_Width = width
        self.project_Pillar = pillar
        self.project_Dimensions = [length, width]
        self.project_Placed = False
        if length == -1.0 or width == -1.0:
            self.project_Area = -1.0
        else:
            self.project_Area = length*width

    def placeProject(self):
        self.project_Placed = True

    def unplaceProject(self):
        self.project_Placed = False

    def setPosition(self,x,y):
        self.project_Position[0]=x
        self.project_Position[1]=y

    def setProjectFloorspaceID(self, ID):
        self.project_FloorSpaceID = ID

class Testproject(unittest.TestCase):
    def test1(self):
        test1 = project("Proj1","ISTD",1.0,2.0)
        
        self.assertEquals(test1.project_Length,1.0)
        self.assertEquals(test1.project_Width,2.0)
        self.assertEquals(test1.project_Area,1.0*2.0)

        self.assertEquals(test1.project_Placed,False)
        test1.placeProject()
        self.assertEquals(test1.project_Placed,True)
        test1.unplaceProject()
        self.assertEquals(test1.project_Placed,False)
        
        self.assertEquals(test1.project_Position,[0.0,0.0])
        test1.setPosition(3.0,4.0)
        self.assertEquals(test1.project_Position,[3.0,4.0])


    def test_invalid(self):
        with self.assertRaises(TypeError):
            invalidinput = project("Proj1","ISTD","length is a string","width")
            
    def test_invalid2(self):
        try:
            invalidinput = project("Proj1","ISTD","length is a string",5.0)
        except:
            self.assertRaises(TypeError)

if __name__ == '__main__':
    unittest.main()