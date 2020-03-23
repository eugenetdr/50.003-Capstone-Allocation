import csv

import operator

project_Array = []
sorted_Project_Array = []

class project:

    project_FloorSpaceID = 0
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

def sizeStringParser(sizeString):
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
            ##print(returnLS)
          
    return returnLS

class read_files:
    def __init__(self, projectFile):
        with open(projectFile) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count <= 1:
                    line_count+=1
                else:
                    ##print(line_count)
                    line_count+=1
                    size_String = row[4]
                    dimensionLS = sizeStringParser(size_String)
                    #print(dimensionLS)
                    proj = project(row[1],"SUTD", dimensionLS[1], dimensionLS[0])
                    #print (proj.project_Dimensions)
                    project_Array.append(proj)

class floor_Space:

    floorspace_Allocated = False
    floorspace_ID = 0
    floorspace_Area = 1.0
    floorspace_Dimensions = [1.0,1.0]
    floorspace_Width = 1.0
    floorspace_Length = 1.0
    floorspace_Position = [0.0,0.0]
    floorspace_Projects = []

    def __init__(self, ID, width, length):
        self.floorspace_ID = ID
        self.floorspace_Area = length * width
        self.floorspace_Dimensions = [length, width]
        self.floorspace_Width = width
        self.floorspace_Length = length
        self.floorspace_Position = [0.0,0.0]
        self.floorspace_Projects = []
        self.floorspace_Allocated = False


    def setPosition(self,x,y):
        self.floorspace_Position[0] = x
        self.floorspace_Position[1] = y

    def allocateFloorspace(self):
        self.floorspace_Allocated = True
    
    def deallocateFloorsapce(self):
        self.floorspace_Allocated = False
    
    def addProjectToFloorspace(self, project):
        self.floorspace_Projects.append(project)


################TODO write iterative instead of recursive
def packFloorspace(floorSpace):
    sorted_Project_Array = sorted(project_Array, key=operator.attrgetter("project_Area"),reverse=True)
    ##print(sorted_Project_Array[0].project_Name)
    ##print(sorted_Project_Array[0].project_Dimensions)
    for i in sorted_Project_Array:
        if floorSpace.floorspace_Length<1 or floorSpace.floorspace_Width<1:
            pass
        if i.project_Width < 0 or i.project_Length < 0:
            pass
        if i.project_Placed:
            pass
        if i.project_Width > floorSpace.floorspace_Width or i.project_Length > floorSpace.floorspace_Length:
            pass
        if i.project_Width < floorSpace.floorspace_Width:
            project_x = floorSpace.floorspace_Position[0]
            project_y = floorSpace.floorspace_Position[1]

            i.placeProject()
            i.setPosition(project_x, project_y)

            small_width = floorSpace.floorspace_Width - i.project_Width
            small_length = i.project_Length

            big_width = floorSpace.floorspace_Width
            big_length = floorSpace.floorspace_Length - i.project_Length

            small_x = floorSpace.floorspace_Position[0]
            small_y = floorSpace.floorspace_Position[1] + i.project_Width
            big_x = floorSpace.floorspace_Position[0]
            big_y = floorSpace.floorspace_Position[1] + i.project_Length

            ID_parent = floorSpace.floorspace_ID
            break
        else:
            pass
    if small_width < 1:
        pass
    else:
        small_Floorspace = floor_Space(ID_parent, small_width, small_length)
        small_Floorspace.setPosition(small_x, small_y)
        packFloorspace(small_Floorspace)
    if big_length < 1:
        pass
    else:
        big_Floorspace = floor_Space(floor_Space.floorspace_ID, big_width, big_length)
        big_Floorspace.setPosition(big_x, big_y)
        packFloorspace(big_Floorspace)

floorspace_Array = []

def createFloorplan():
    for i in range(10):
        floorspace_Array.append(floor_Space(i,2.0,10.0))

class run_Algorithm:
    def __init__(self):
        print("run")
        count = 0
        createFloorplan()
        print("created")
        read_files("projects.csv")
        print("reading")
        for x in floorspace_Array:
            print(x.floorspace_ID)
            packFloorspace(x)
        usedFloorSpace = []

        for i in floorspace_Array:
            if i.floorspace_Allocated:
                print("Floorspace ID %d:" % i.floorspace_ID)
                for l in i.floorspace_Projects:
                    print(l.project_Name)
                    ##print(l.project_Dimensions)
                usedFloorSpace.append(i)

        ls = []
        for k in project_Array:
            if k.project_Placed==False:
                count = count + 1
                if k.project_Dimensions == [-1.0,-1.0]:
                    ls.append(k.project_Name + " has illegal size requirements.")
                else:
                    ls.append(k.project_Name + " does not fit in floorplan.")
        print("\n")
        print("%d projects have not been placed:" %count)
        for m in ls:
            print(m)

        print("\n")
        print("FloorSpace ID Used:")
        for j in usedFloorSpace:
            if j.floorspace_Allocated:
                print(j.floorspace_ID)

print("pre-lmao")
lmao = run_Algorithm()
print("lmao")