  
import operator

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

    def __init__(self, ID, name, pillar, length, width):
        self.project_ID = ID
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
        self.project_Industry = ""

    def placeProject(self):
        self.project_Placed = True

    def unplaceProject(self):
        self.project_Placed = False

    def setPosition(self,x,y):
        self.project_Position[0]=x
        self.project_Position[1]=y

    def setProjectFloorspaceID(self, ID):
        self.project_FloorSpaceID = ID

    def setProjectIndustry(self, Industry):
        self.project_Industry = Industry

class floor_Space:

    floorspace_Allocated = False
    floorspace_ID = 0
    floorspace_Area = 1.0
    floorspace_Dimensions = [1.0,1.0]
    floorspace_Width = 1.0
    floorspace_Length = 1.0
    floorspace_Position = [0.0,0.0]
    floorspace_Projects = []

    def __init__(self, ID, width, length, x, y, degree, level):
        self.floorspace_Degree = degree
        self.floorspace_ID = ID
        self.floorspace_Area = length * width
        self.floorspace_Dimensions = [length, width]
        self.floorspace_Width = width
        self.floorspace_Length = length
        self.floorspace_Position = [x,y]
        self.floorspace_Projects = []
        self.floorspace_Allocated = False
        self.floorspace_Level = level
        self.floorspace_Position_in_floorplan = [x,y]


    def setPosition(self,x,y):
        self.floorspace_Position[0] = x
        self.floorspace_Position[1] = y

    def allocateFloorspace(self):
        self.floorspace_Allocated = True
    
    def deallocateFloorsapce(self):
        self.floorspace_Allocated = False
    
    def addProjectToFloorspace(self, project):
        self.floorspace_Projects.append(project)

def shuffle_LS(Main_LS,Add_LS):
    main_len = len(Main_LS)
    add_len = len(Add_LS)
    count = 0
    if main_len==0:
        return Add_LS
    if add_len==0:
        return Main_LS
    if main_len>=add_len:
        divisor = main_len//add_len
        for i in Add_LS:
            Main_LS.insert(count,i)
            count =+ divisor
        return Main_LS
    else:
        divisor = add_len//main_len
        for i in Main_LS:
            Add_LS.insert(count,i)
            count =+ 1
        return Add_LS

def shuffle_Projects(projects_by_industry):
    Main_LS = []
    industries = projects_by_industry.keys()
    for i in industries:
        ls = projects_by_industry.get(i)
        Main_LS = shuffle_LS(Main_LS, ls)
    return Main_LS

def packFloorspace_Iter(floorSpaceArray, project_Array):
    sorted_Project_Array = sorted(project_Array, key=operator.attrgetter("project_Area"), reverse = True)
    min_Project = sorted_Project_Array[len(project_Array)-1]
    min_Width = min_Project.project_Width
    min_Length = min_Project.project_Length
    min_Size = min_Project.project_Area
    for i in floorSpaceArray:
        X_Coordinate = 0.0
        Y_Coordinate = 0.0
        for j in project_Array:
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
                i.addProjectToFloorspace(j)
                j.placeProject()
                i.allocateFloorspace()
                if min_Size > j.project_Length*i.floorspace_Width or min_Width > i.floorspace_Width - Y_Coordinate or min_Length > i.floorspace_Length - X_Coordinate:
                    X_Coordinate = X_Coordinate + j.project_Length
                    Y_Coordinate = 0.0
                    continue
                else:
                    Y_Coordinate = Y_Coordinate + j.project_Width
                    for k in project_Array:
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
                            k.placeProject()
                            i.allocateFloorspace()
                            break
                    Y_Coordinate = 0.0
                    X_Coordinate  = X_Coordinate + j.project_Length
    return project_Array

def project_name_to_industry_dict(dd):
    keys_list = dd.get("teams").keys()
    re_dd = {}
    for i in keys_list:
        project_dd = dd["teams"].get(i)
        industry_type = project_dd.get("industry")
        if industry_type in re_dd:
            project_append = project(i, project_dd.get("projectName"),"SUTD", project_dd.get("sLength") ,project_dd.get("sWidth"))
            project_append.setProjectIndustry(industry_type)
            re_dd[industry_type].append(project_append)
        else:
            re_dd[industry_type] = []
            project_append = project(i,project_dd.get("projectName"),"SUTD", project_dd.get("sLength") ,project_dd.get("sWidth"))
            project_append.setProjectIndustry(industry_type)
            re_dd[industry_type].append(project_append)
    re_keys_list = re_dd.keys()
    for j in re_keys_list:
        ls = re_dd.get(j)
        re_dd[j] = sorted(ls, key=operator.attrgetter("project_Area"), reverse = True)
    return re_dd

def pixel_to_meter(pixel):
    return pixel/16.4

def createFloorplan():
    floorspace_Array = []
    floorspace_Array.append(floor_Space(0,pixel_to_meter(40),pixel_to_meter(130),420,275,0,1))
    floorspace_Array.append(floor_Space(1,pixel_to_meter(67),pixel_to_meter(67),510,265,0,1))
    floorspace_Array.append(floor_Space(2,pixel_to_meter(115),pixel_to_meter(93),550,150,0,1))
    floorspace_Array.append(floor_Space(3,pixel_to_meter(65),pixel_to_meter(130),650,300,0,1))
    floorspace_Array.append(floor_Space(4,pixel_to_meter(640),pixel_to_meter(640),640,460,-40,1))
    floorspace_Array.append(floor_Space(5,pixel_to_meter(216),pixel_to_meter(100),850,270,0,1))
    floorspace_Array.append(floor_Space(6,pixel_to_meter(250),pixel_to_meter(90),850,400,0,1))
    floorspace_Array.append(floor_Space(7,pixel_to_meter(140),pixel_to_meter(117),850,570,0,1))
    floorspace_Array.append(floor_Space(8,pixel_to_meter(75),pixel_to_meter(175),1010,250,0,1))
    floorspace_Array.append(floor_Space(9,pixel_to_meter(90),pixel_to_meter(90),1175,250,0,1))
    floorspace_Array.append(floor_Space(10,pixel_to_meter(100),pixel_to_meter(175),1080,450,315,1))

    floorspace_Array.append(floor_Space(11,pixel_to_meter(354),pixel_to_meter(60),864,188,0,2))
    floorspace_Array.append(floor_Space(12,pixel_to_meter(259),pixel_to_meter(60),1000,540,-30,2))
    floorspace_Array.append(floor_Space(13,pixel_to_meter(259),pixel_to_meter(60),652,500,30,2))

    illegal_projects = floor_Space(-1,-1,-1,0,0,0,0)
    illegal_projects.allocateFloorspace()
    floorspace_Array.append(illegal_projects)
    
    return floorspace_Array

def sort_by_industry(projects_Array):
    dd = {}
    for i in projects_Array:
        industry_Str = str(i.project_Industry)
        if industry_Str in dd:
            ls = dd.get(industry_Str)
            dd[industry_Str] = ls.append(i)
        else:
            dd[industry_Str] = []
    keys_ls = dd.keys()
    for j in keys_ls:
        project_ls = dd.get(j)
        sorted_project_ls = sorted(project_ls, key=operator.attrgetter("project_Area"), reverse = True)
        dd[j] = sorted_project_ls
    return dd

class run_Algorithm():
    global_project_Array = []
    floorspace_Array = []
    def __init__(self, project_dict_by_name):
        self.floorspace_Array = createFloorplan()
        industry_dd = project_name_to_industry_dict(project_dict_by_name)
        project_Array = shuffle_Projects(industry_dd)
        self.global_project_Array = packFloorspace_Iter(self.floorspace_Array, project_Array)

    def return_cluster(self):
        usedFloorSpace = []
        cluster = {}
        for i in self.floorspace_Array:
            if i.floorspace_Allocated:
                usedFloorSpace.append(i)
        for i in usedFloorSpace:
            cluster[str(i.floorspace_ID)] = {}
            cluster[str(i.floorspace_ID)]['level'] = i.floorspace_Level 
            cluster[str(i.floorspace_ID)]['clusPos'] = {'x':i.floorspace_Position_in_floorplan[0],'y':i.floorspace_Position_in_floorplan[1]}
            cluster[str(i.floorspace_ID)]['clusAngle'] = i.floorspace_Degree
            cluster[str(i.floorspace_ID)]['teams'] = {}
        for k in self.global_project_Array:
            if k.project_Placed==True:
                cluster[str(k.project_FloorSpaceID)]['teams'].update({k.project_ID:{'industry':k.project_Industry,'projectName':k.project_Name,'sLength':k.project_Length,'sWidth':k.project_Width,'relativeX':k.project_Position[0],'relativeY':k.project_Position[1]}})
            else:
                cluster[str(-1)]['teams'].update({k.project_ID:{'industry':k.project_Industry,'projectName':k.project_Name,'sLength':k.project_Length,'sWidth':k.project_Width,'relativeX':0.0,'relativeY':0.0}})
        return cluster
