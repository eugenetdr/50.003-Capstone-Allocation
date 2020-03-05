def setup():
    size(500,500)
    stroke(255)
    global floorplan
    floorplan = loadImage("Main Hall.jpg")
    
space = 50
def draw():
    global space
    background(1)
    image(floorplan,0,0)

    for i in range(width/space):
        for j in range(height/space):
            line(i*space,0,i*space,height) #vertical line
            line(0,j*space,width,j*space)  #horizontal line

    # fill(255,0,0) #colour
    rect(6*space,5*space,space*2,space) #(x coord,ycoord,width,height)
    # noFill()
