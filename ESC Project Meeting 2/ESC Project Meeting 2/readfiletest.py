import csv
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

class floor_Space:

    floorspace_ID = 0
    floorspace_Area = 1.0
    floorspace_Dimensions = [1.0,1.0]
    floorspace_Width = 1.0
    floorspace_Length = 1.0
    floorspace_Position = [0.0,0.0]

    def __init__(self, ID, width, length):
        self.floorspace_ID = ID
        self.floorspace_Area = length * width
        self.floorspace_Dimensions = [length, width]
        self.floorspace_Width = width
        self.floorspace_Length = length
        self.floorspace_Position = [0.0,0.0]


    def setPosition(self,x,y):
        self.floorspace_Position[0] = x
        self.floorspace_Position[1] = y
        
floorplans = []

class read_files:
    def __init__(self, projectFile):
        with open(projectFile) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            #col_list = ["FloorSpaceID", "Placed","Name","Length","Width","Position X","Position Y"]
            lst = []
            numid = 0
            line_count = 0
            
            
            for row in csv_reader: #gets a list of floorspaceID
                if row:
                    if row[0] != "FloorSpaceID" :
                        if row[0] != "-1":
                            lst.append(row)
            #print(lst)
            
            for i in lst:
                id = int(i[0])
                if id>numid:
                    numid = id

            for i in range(numid+1): #creates lists inside floorspaces array
                floorplans.append([])
            #print(floorplans)
            

            for p in lst:
                line_count+=1
                proj = project(p[1],"SUTD",float(p[3]),float(p[4]))
                proj.setPosition(float(p[5]),float(p[6]))
                
                #print(proj.project_Position)
                floorplans[int(p[0])].append(proj.project_Position)
                
            print (floorplans)
            
                            
                        
fp = floor_Space(1,10,10) #test floorplan
multiplier = 50 #scaling size
# def setup():
#     size(fp.floorspace_Length*multiplier,fp.floorspace_Width*multiplier) #sets size of canvas

#    # size(fp.floorspace_Length,fp.floorspace_Width)
#     stroke(255)
#    # global floorplan
#    # floorplan = loadImage("Main Hall.jpg")
    
# space = multiplier/2 #0.5m intervals
# def draw():
#     global space
#     background(1)
#    # image(floorplan,0,0)

#     for i in range(width/space): #generates grid lines
#         for j in range(height/space):
#             line(i*space,0,i*space,height) #vertical line
#             line(0,j*space,width,j*space)  #horizontal line

#     fill(255,0,0) #colour
#     rect(6*space,5*space,space*2,space) #(x coord,ycoord,width,height)
#     # noFill()

read_files("projects_file.csv")