import csv

import operator

project_Array = []
sorted_Project_Array = []

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
    print(returnLS)

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
                    if row[1] == "" or row[1] == "Total":
                        continue
                    else:
                        line_count+=1
                        size_String = row[4]
                        print(row[1])
                        dimensionLS = sizeStringParser(size_String)
                        print(dimensionLS)
                        if dimensionLS == [-1.0,-1.0]:
                            print(row[1])
                        proj = project(row[1],"SUTD",dimensionLS[1],dimensionLS[0])
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

def packFloorspace_Iter(floorSpaceArray):
    sorted_Project_Array = sorted(project_Array, key=operator.attrgetter("project_Area"), reverse = True)
    min_Project = sorted_Project_Array[len(sorted_Project_Array)-1]
    min_Width = min_Project.project_Width
    min_Length = min_Project.project_Length
    min_Size = min_Project.project_Area
    for i in floorSpaceArray:
        X_Coordinate = 0.0
        Y_Coordinate = 0.0
        for j in sorted_Project_Array:
            if j.project_Width < 0 or j.project_Length < 0:
                continue
            if j.project_Placed:
                continue
            if j.project_Width > i.floorspace_Width - Y_Coordinate or j.project_Area > i.floorspace_Area or j.project_Length > i.floorspace_Length - X_Coordinate:
                continue
            if i.floorspace_Length - X_Coordinate < 0 or i.floorspace_Width - Y_Coordinate < 0:
                continue
            else:
                j.setProjectFloorspaceID(i.floorspace_ID)
                j.setPosition(X_Coordinate,Y_Coordinate)
                ##print(str(Y_Coordinate) + "j loop")
                i.addProjectToFloorspace(j)
                j.placeProject()
                i.allocateFloorspace()
                if min_Size > j.project_Length*i.floorspace_Width or min_Width > i.floorspace_Width - Y_Coordinate or min_Length > i.floorspace_Length - X_Coordinate:
                    X_Coordinate = X_Coordinate + j.project_Length
                    Y_Coordinate = 0.0
                    continue
                else:
                    Y_Coordinate = Y_Coordinate + j.project_Width
                    for k in sorted_Project_Array:
                        if k.project_Width < 0 or k.project_Length < 0:
                            continue
                        if k.project_Placed:
                            continue
                        if k.project_Width > i.floorspace_Width - j.project_Width or k.project_Area > i.floorspace_Area or k.project_Length > j.project_Length:
                            continue
                        if i.floorspace_Length - X_Coordinate < 0 or i.floorspace_Width - Y_Coordinate < 0:
                            continue
                        else:
                            k.setProjectFloorspaceID(i.floorspace_ID)
                            k.setPosition(X_Coordinate,Y_Coordinate)
                            i.addProjectToFloorspace(k)
                            ##print(str(X_Coordinate) + "K loop")
                            k.placeProject()
                            i.allocateFloorspace()
                            break
                    Y_Coordinate = 0.0
                    X_Coordinate  = X_Coordinate + j.project_Length

        



floorspace_Array = []

def createFloorplan():
    for i in range(10):
        floorspace_Array.append(floor_Space(i,10.0,10.0))

class run_Algorithm:
    def __init__(self):
        count = 0
        createFloorplan()
        read_files("projects.csv")
        packFloorspace_Iter(floorspace_Array)
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

        with open('projects_file.csv', mode='w') as project_file:
            project_writer = csv.writer(project_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            header = ["FloorSpaceID","Placed","Name","Length","Width","Position"]
            project_writer.writerow(header)
            for x in project_Array:
                ls = [x.project_FloorSpaceID,x.project_Placed,x.project_Name,x.project_Length,x.project_Width,x.project_Position]
                try:
                    project_writer.writerow(ls)
                except:
                    continue

lmao = run_Algorithm()