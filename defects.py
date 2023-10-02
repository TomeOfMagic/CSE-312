import numpy as np
import math
import random
from PIL import Image as im
import cv2
import json
import os

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

def add_scratches(Image, X_value, Y_value, Radius, Color, num_scratches, scratch_length, scratch_thickness, json_filename, box_size):
    scratch_data = []  # List to store scratch data

    for i in range(num_scratches):
        # Randomly generate an angle and distance within the wafer boundary
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(0, Radius)

        # Calculate the starting coordinates within the wafer boundary
        x_start = int(X_value + distance * math.cos(angle))
        y_start = int(Y_value + distance * math.sin(angle))

        min_x = x_start
        min_y = y_start
        max_x = x_start
        max_y = y_start

        for j in range(scratch_length):
            x = int(x_start + j * math.cos(angle))
            y = int(y_start + j * math.sin(angle))

            min_x = min(min_x, x)
            min_y = min(min_y, y)
            max_x = max(max_x, x)
            max_y = max(max_y, y)

            if 0 <= x < Image.shape[1] and 0 <= y < Image.shape[0]:
                Image[y][x] = random.randint(50, 90)  # color of scratch


                for k in range(1, scratch_thickness):
                    for dx in range(-k, k + 1):
                        for dy in range(-k, k + 1):
                            if 0 <= x + dx < Image.shape[1] and 0 <= y + dy < Image.shape[0]:
                                Image[y + dy][x + dx] = random.randint(50, 90)

        x_end = x
        y_end = y

        # Calculate bounding box coordinates with a fixed size
        box_half_size = box_size // 2
        min_x = max(0, min_x - box_half_size)
        min_y = max(0, min_y - box_half_size)
        max_x = min(Image.shape[1] - 1, max_x + box_half_size)
        max_y = min(Image.shape[0] - 1, max_y + box_half_size)

        scratch = {
            "Label: Scratch": i + 1,
            "start_x": x_start,
            "start_y": y_start,
            "end_x": x_end,
            "end_y": y_end,
            "bounding_box": {
                "min_x": min_x,
                "min_y": min_y,
                "max_x": max_x,
                "max_y": max_y,
            }
        }
        cv2.rectangle(Image, (min_x, min_y), (max_x, max_y), (0, 0, 255), 1)

        scratch_data.append(scratch)  # Add the scratch data to the list

    # Save scratch data to a JSON file
    add_to_json(scratch_data, json_filename)


def add_spots(Image, X_value, Y_value, Radius, num_spots, spot_radius, json_filename, box_size):
    spot_data = []  # List to store spot data

    for i in range(num_spots):
        # Randomly generate an angle and distance within the wafer boundary
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(0, Radius)

        # Calculate the starting coordinates within the wafer boundary
        x_center = int(X_value + distance * math.cos(angle))
        y_center = int(Y_value + distance * math.sin(angle))

        min_x = x_center - spot_radius
        min_y = y_center - spot_radius
        max_x = x_center + spot_radius
        max_y = y_center + spot_radius

        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                if (
                    0 <= x < Image.shape[1]
                    and 0 <= y < Image.shape[0]
                    and (x - x_center) ** 2 + (y - y_center) ** 2 <= spot_radius ** 2
                ):
                    Image[y][x] = random.randint(50, 90)

        # Calculate bounding box coordinates with a fixed size
        min_x = max(0, x_center - box_size // 2)
        min_y = max(0, y_center - box_size // 2)
        max_x = min(Image.shape[1] - 1, x_center + box_size // 2)
        max_y = min(Image.shape[0] - 1, y_center + box_size // 2)

        spot = {
            "Label: Spot": i + 1,
            "center_x": x_center,
            "center_y": y_center,
            "radius": spot_radius,
            "bounding_box": {
                "min_x": min_x,
                "min_y": min_y,
                "max_x": max_x,
                "max_y": max_y,
            },
        }

        cv2.rectangle(Image, (min_x, min_y), (max_x, max_y), (0, 0, 255), 1)

        spot_data.append(spot)  # Add the spot data to the list

    # Save spot data to a JSON file
    add_to_json(spot_data, json_filename)

def add_whirl(Image, X_value, Y_value, Radius, num_slices, slice_length, slice_thickness, json_filename):
    whirl_data = []  # List to store whirl data

    for i in range(num_slices):
        # Randomly generate an angle within the wafer boundary
        angle = random.uniform(0, 2 * math.pi)

        # Calculate the coordinates at the center
        x_center = int(X_value)
        y_center = int(Y_value)

        # Calculate the coordinates for the points at the edge of the slice
        x_end1 = int(X_value + (Radius - slice_length) * math.cos(angle))
        y_end1 = int(Y_value + (Radius - slice_length) * math.sin(angle))
        x_end2 = int(X_value + (Radius - slice_length) * math.cos(angle + math.pi / num_slices))
        y_end2 = int(Y_value + (Radius - slice_length) * math.sin(angle + math.pi / num_slices))

        # Create the vertices of the slice shape
        vertices = [(x_center, y_center), (x_end1, y_end1), (x_end2, y_end2)]

        # Fill the slice shape with a random color
        cv2.fillPoly(Image, [np.array(vertices)], (random.randint(50, 90), random.randint(50, 90), random.randint(50, 90)))

        slice_data = {
            "Label: Slice": i + 1,
            "vertices": vertices,
        }

        whirl_data.append(slice_data)  # Add the slice data to the list

    # Save whirl data to a JSON file
    add_to_json(whirl_data, json_filename)


def add_to_json(data, json_filename):
    # Check if the JSON file already exists
    if os.path.exists(json_filename):
        with open(json_filename, "r") as json_file:
            existing_data = json.load(json_file)
    else:
        existing_data = []

    # Append the new data to the existing data
    existing_data.extend(data)

    # Write the updated data back to the JSON file
    with open(json_filename, "w") as json_file:
        pretty_json = json.dumps(existing_data, indent=4)
        json_file.write(pretty_json)

def main():

    img_size = 601  ## define img size
    img_margin = 0.2*(img_size/2) ## define margin between border of image and wafer edge as 20% of the total size
    stage_margin = 0.15*(img_size/2)  ## define margin between border of image and stage edge as 15% of the total size

    chip_low = 20  ## define the lower bound of chip color
    chip_high = 255 ## define the higher bound of chip color


    pitch_x = random.randint(10,20)
    pitch_y = random.randint(10,20)

    scribe_x = random.randint(1,3)
    scribe_y = random.randint(1,3)


    Image1 = np.zeros((img_size,img_size), dtype=np.uint8)  ##create image array

    dim = Image1.shape

    dim_x = dim[0]
    dim_y = dim[1]

    center_x = math.floor(dim_x/2)
    center_y = math.floor(dim_y/2)

    stage_radius = img_size/2 - stage_margin  ## define the radius of the stage as the image border minus the stage margin
    wafer_radius = img_size/2 - img_margin    ## define the radius of the wafer as the image border minus the wafer margin
    notch_radius = round(1.25*(wafer_radius/100))  ##  define the radius of the notch as 1.25/300 of the wafer
    grid_radius = 0.95*wafer_radius    ##  define the radius of the circle in which to put the grid pattern as 95% of wafer radius

    stage_color = 50  ## defines the center of the color options for the stage
    stage_randomness = random.randint(3,6) ## defines the color variance for the stage

    wafer_color = 100 ## defines the center of the color options for the wafer
    wafer_randomness = random.randint(10,20)  ## defines the color variance for the wafer

    grid_color = 200  ## defines the center of the color options for the grid
    grid_randomness =  random.randint(5,10) ## defines the color variance for the grid



    Create_Stage(Image1, center_x, center_y, stage_radius, stage_color, stage_randomness)

    Create_Wafer_edge(Image1, center_x, center_y, wafer_radius, wafer_color, wafer_randomness)

    Create_Grid_pattern(Image1, center_x, center_y, grid_radius, pitch_x, pitch_y, grid_color, scribe_x, scribe_y, grid_randomness)

    Create_Notch(Image1, center_x, center_y, wafer_radius, notch_radius, stage_color, stage_randomness)

    add_scratches(Image1, center_x, center_y, grid_radius, wafer_color, num_scratches=random.randint(1,5),
                  scratch_length=random.randint(1, 20), scratch_thickness= random.randint(0,1),
                  json_filename="defects_data.json", box_size = 25)

    add_spots(Image1, center_x, center_y, grid_radius, num_spots=random.randint(1, 4), spot_radius=random.randint(1, 6),
              json_filename="defects_data.json", box_size=25)

    # add_whirl(Image1, center_x, center_y, grid_radius, num_slices=random.randint(1, 5),
    #       slice_length=random.randint(10, 50), slice_thickness=random.randint(1, 5),
    #       json_filename="whirl_data.json")




    data = im.fromarray(Image1)

    data.save('gfg_dummy_pic.png')

main()
