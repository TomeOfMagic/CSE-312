def Create_Stage(Image, X_value, Y_value, Radius, Color):
    ## filled in Circle Equation, (X-X_value)^2 + (Y-Y_value)^2 <= Radius^2

    # for all pixel values:
    ## if (X-X_value)^2 + (Y-Y_value)^2 <= Radius^2 then 
    ### Image[X_value][Y_value] = Color
    


def Create_Wafer_edge(Image, X_value, Y_value, Radius, Color):

    # for all pixel values:
    ## if (X-X_value)^2 + (Y-Y_value)^2 <= Radius^2 then 
    ### Image[X_value][Y_value] = Color


def Create_Notch(Image, Tip, Base_corner, Base, Height, Color):

    #



def Create_Grid_pattern(Image, X_value, Y_value, Radius, increment_x, increment_y, Color):

    # for pixel values staring with x=0 and y=0 incrementing x by say 10 everytime then check if within circle repeat then x>image.size_x increment y by 1 then repeat
    # for pixel values staring with x=0 and y=0 incrementing y by say 10 everytime then check if within circle repeat then y>image.size_y increment x by 1 then repeat
    # if both conditions hold change pixel value to color