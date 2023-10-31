import numpy as np
import math
import random
from PIL import Image as im
import cv2 as cv
import os
import json

"""
def GenerateJson(self , name , topr_x , topr_y , botr_x , botr_y):
        self.DefectShape.append({
            "label": f"{name}",
            "points": [[topr_x, topr_y], [botr_x, botr_y]],
            "group_id": None,
            "shape_type": "rectangle",
            "flags": {}
        })

def save_img(self):
    cv.imwrite(self.file_name, self.image_arr)
    data = {
        "version": "5.0.1",
        "flags": {},
        "shapes": self.DefectShape,
        "imagePath": self.file_name,
        "imageData": None,
        "imageHeight": self.HeightScreen,
        "imageWidth": self.WidthScreen
    }
    json_file = os.path.join('json_data/', os.path.basename(self.file_name).split('.')[0] + '.json')
    with open(json_file, 'w') as json_file:
        json.dump(data, json_file)
"""

def Create_Stage(Image, X_value, Y_value, Radius, Color, stage_randomness):
    ## filled in Circle Equation, (X-X_value)^2 + (Y-Y_value)^2 <= Radius^2
    x1 = 0
    y1 = 0

    variation = math.floor(stage_randomness/2)


    for x in Image:

        y1 = 0
        for y in x:
            #print(x1)
            #print(y1)
            if ((x1-X_value) ** 2 + (y1-Y_value) ** 2) <= (Radius ** 2):
                Image[x1][y1] = Color + random.randint(-variation, variation)
            y1 = y1 +1
        x1 = x1 + 1

    

def Create_Wafer_edge(Image, X_value, Y_value, Radius, Color, wafer_randomness):

    x1 = 0
    y1 = 0

    variation = math.floor(wafer_randomness/2)


    for x in Image:
       
        y1 = 0
        for y in x:

            if ((x1-X_value) ** 2 + (y1-Y_value) ** 2) <= (Radius ** 2):
                Image[x1][y1] = Color + random.randint(-variation, variation)
            y1 = y1 +1
        x1 = x1 + 1

def Create_Notch(Image1, X_value, Y_value, Radius, Radius2, Color, stage_randomness):

    Create_Stage(Image1, (X_value + Radius+1), Y_value, Radius2, Color, stage_randomness)



def Create_Grid_pattern(Image, X_value, Y_value, Radius, increment_x, increment_y, Color, scribe_x, scribe_y, grid_randomness):

    #dim = Image.shape

    #dim_x = dim[0]
    #dim_y = dim[1]

    half_scribe_x = math.floor(scribe_x/2)
    half_scribe_y = math.floor(scribe_y/2)

    xi = 0
    x=0
    x_i = 0
    y=0
    y_i = 0


    variation = math.floor(grid_randomness/2)

    for x1 in Image:
        y = 0
        y_i = 0
        for y1 in x1:
            if (x == x_i):
                #print("found_x")
                xi = 1
                if ((x-X_value) ** 2 + (y-Y_value) ** 2) <= (Radius ** 2):
                    #print("found")
                    temp_x = x-half_scribe_x
                    while temp_x <= x+half_scribe_x:
                        Image[temp_x][y] = Color + random.randint(-variation, variation)
                        temp_x += 1
            if(y == y_i):
                #print("found_y")
                y_i += increment_y
                if ((x-X_value) ** 2 + (y-Y_value) ** 2) <= (Radius ** 2):
                    #print("found")
                    temp_y = y-half_scribe_y
                    while temp_y <= y+half_scribe_y:
                        Image[x][temp_y] = Color + random.randint(-variation, variation)
                        temp_y += 1
            y += 1  
        x += 1
        if(xi):
            x_i += increment_x
            xi = 0

def Cloudy_defect(Image, X_value, Y_value, Radius, min_r, max_r, min_box_size):
    
    true = 0

    x_radius = random.randint(min_r, max_r)
    y_radius = random.randint(min_r, max_r)

    while(true == 0):
        
        rand_X = random.randint(Radius-int(X_value), Radius+int(X_value))
        rand_y = random.randint(Radius-int(Y_value), Radius+int(Y_value))

        if (((rand_X+x_radius)-X_value) ** 2 + ((rand_y+y_radius)-Y_value) ** 2) <= (Radius ** 2):
            if (((rand_X-x_radius)-X_value) ** 2 + ((rand_y-y_radius)-Y_value) ** 2) <= (Radius ** 2):
                for i in range(1, 5, 2):
                    Image2 = cv.GaussianBlur(Image, (i, i), 0)
                true = 1

    x1 = 0

    for x in Image:
       
        y1 = 0
        for y in x:

            if ((((x1-rand_X) ** 2)/(x_radius ** 2)) + (((y1-rand_y) ** 2))/(y_radius ** 2)) <= 1 and ((x1-X_value) ** 2 + (y1-Y_value) ** 2) <= (Radius ** 2):
                Image[x1][y1] = Image2[x1][y1]
            y1 = y1 +1
        x1 = x1 + 1

    if (x_radius*2 >= min_box_size):
        top_left = (rand_X - x_radius - 5, rand_y - x_radius - 5)
        if(y_radius*2 >= min_box_size):
            bottom_right = (rand_X + y_radius + 5, rand_y + y_radius + 5)
        else:
            bottom_right = (rand_X + min_box_size + 5, rand_y + min_box_size + 5)
    else:
        top_left = (rand_X - min_box_size - 5, rand_y - min_box_size - 5)
        if (y_radius*2 >= min_box_size):
            bottom_right = (rand_X + y_radius + 5, rand_y + y_radius + 5)
        else:
            bottom_right = (rand_X + min_box_size + 5, rand_y + min_box_size + 5)

    
    
    #GenerateJson(name='Cloudy' , topr_x= top_left[0] , topr_y= top_left[1] , botr_x= bottom_right[0] , botr_y= bottom_right[1])

    Image[top_left[0], top_left[1]] = 0
    Image[bottom_right[0], bottom_right[1]] = 0




def main():

    img_size = 601  ## define img size
    img_margin = 0.2*(img_size/2) ## define margin between border of image and wafer edge as 20% of the total size
    stage_margin = 0.15*(img_size/2)  ## define margin between border of image and stage edge as 15% of the total size

    chip_low = 40  ## define the lower bound of chip color
    chip_high = 200 ## define the higher bound of chip color
    
    
    pitch_x = 20
    pitch_y = 20

    scribe_x = 3
    scribe_y = 3
    
    
    Image1 = np.zeros((img_size,img_size), dtype=np.uint8)  ##create image array

    dim = Image1.shape 

    dim_x = dim[0]
    dim_y = dim[1]

    center_x = math.floor(dim_x/2)
    center_y = math.floor(dim_y/2)

    stage_radius = img_size/2 - stage_margin  ## define the radius of the stage as the image border minus the stage margin
    wafer_radius = int(img_size/2 - img_margin)    ## define the radius of the wafer as the image border minus the wafer margin
    notch_radius = round(1.25*(wafer_radius/100))  ##  define the radius of the notch as 1.25/300 of the wafer
    grid_radius = 0.95*wafer_radius    ##  define the radius of the circle in which to put the grid pattern as 95% of wafer radius

    stage_color = random.randint(5,10)  ## defines the center of the color options for the stage
    stage_randomness = random.randint(3,6) ## defines the color variance for the stage
    
    wafer_color = random.randint(chip_low,chip_high) ## defines the center of the color options for the wafer
    wafer_randomness = random.randint(0,5)  ## defines the color variance for the wafer

    grid_color = wafer_color - 10  ## defines the center of the color options for the grid
    grid_randomness =  random.randint(0,5) ## defines the color variance for the grid



    Create_Stage(Image1, center_x, center_y, stage_radius, stage_color, stage_randomness)

    Create_Wafer_edge(Image1, center_x, center_y, wafer_radius, wafer_color, wafer_randomness)

    Create_Grid_pattern(Image1, center_x, center_y, grid_radius, pitch_x, pitch_y, grid_color, scribe_x, scribe_y, grid_randomness)

    Create_Notch(Image1, center_x, center_y, wafer_radius, notch_radius, stage_color, stage_randomness)

    Cloudy_defect(Image1, center_x, center_y, wafer_radius, 5, 15, 20)

    
    data = im.fromarray(Image1)

    data.save('gfg_dummy_pic.png')


    # Image1.saveimg()

main()
  
