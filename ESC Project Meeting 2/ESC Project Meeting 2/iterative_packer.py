def packFloorspace(floorSpace):
    sorted_Project_Array = sorted(project_Array, key=operator.attrgetter("project_Area"))
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