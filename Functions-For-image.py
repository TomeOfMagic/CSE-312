import numpy as np
import math
from PIL import Image as im


def Create_Stage(Image, X_value, Y_value, Radius, Color):
    ## filled in Circle Equation, (X-X_value)^2 + (Y-Y_value)^2 <= Radius^2
    x1 = 0
    y1 = 0
    for x in Image:
        x1 = x1 + 1
        y1 = 0
        for y in x:
            y1 = y1 +1
            if ((x1-X_value) ** 2 + (y1-Y_value) ** 2) <= (Radius ** 2):
                Image[x1][y1] = Color

    

def Create_Wafer_edge(Image, X_value, Y_value, Radius, Color):

    x1 = 0
    y1 = 0
    for x in Image:
        x1 = x1 + 1
        y1 = 0
        for y in x:
            y1 = y1 +1
            if ((x1-X_value) ** 2 + (y1-Y_value) ** 2) <= (Radius ** 2):
                Image[x1][y1] = Color

def Create_Notch(Image1, X_value, Y_value, Radius, Radius2, Color):

    Create_Stage(Image1, (X_value + Radius), Y_value, Radius2, Color)



def Create_Grid_pattern(Image, X_value, Y_value, Radius, increment_x, increment_y, Color):

    #dim = Image.shape

    #dim_x = dim[0]
    #dim_y = dim[1]

    xi = 0
    x=0
    x_i = 0
    y=0
    y_i = 0

    for x1 in Image:
        y = 0
        y_i = 0
        for y1 in x1:
            if (x == x_i):
                #print("found_x")
                xi = 1
                if ((x-X_value) ** 2 + (y-Y_value) ** 2) <= (Radius ** 2):
                    #print("found")
                    Image[x][y] = Color
            if(y == y_i):
                #print("found_y")
                y_i += increment_y
                if ((x-X_value) ** 2 + (y-Y_value) ** 2) <= (Radius ** 2):
                    #print("found")
                    Image[x][y] = Color
            y += 1  
        x += 1
        if(xi):
            x_i += increment_x
            xi = 0



def main():

    Image1 = np.zeros((1801,1801), dtype=np.uint8)

    dim = Image1.shape

    dim_x = dim[0]
    dim_y = dim[1]

    center_x = math.floor(dim_x/2)
    center_y = math.floor(dim_y/2)

    radius1 = 0.85*(center_x)
    radius2 = 0.8*(center_x)
    radius3 = 0.02*(center_x)
    radius4 = 0.95*radius2

    color1 = 20
    color2 = 40

    color4 = 200

    increment_x = 20
    increment_y = 20

    Create_Stage(Image1, center_x, center_y, radius1, color1)

    Create_Wafer_edge(Image1, center_x, center_y, radius2, color2)

    Create_Grid_pattern(Image1, center_x, center_y, radius4, increment_x, increment_y, color4)

    Create_Notch(Image1, center_x, center_y, radius2, radius3, color1)

    data = im.fromarray(Image1)

    data.save('gfg_dummy_pic.png')

main()
  
