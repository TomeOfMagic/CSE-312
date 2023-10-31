import numpy as np
import math
import random
import cv2 as cv
import json
import os

class GenerateData:
    def __init__(self,img_size, chip_low , chip_high , stage_mid_color , grid_mid_color , wafer_mid_color ,  
                stage_random , wafer_random , grid_random , pitch_x , pitch_y , scribe_x , scribe_y , ):
        self.img_size = img_size
        self.img_margin = 0.2*(self.img_size / 2)
        self.stage_margin = 0.15*(self.img_size/2)
        self.chip_low = chip_low
        self.chip_high = chip_high
        self.pitch_x = pitch_x
        self.pitch_y = pitch_y
        self.scribe_x = scribe_x
        self.scribe_y = scribe_y
        self.imgarr = np.zeros((img_size,img_size), dtype=np.uint8)
        self.dim_x = self.imgarr.shape[0]
        self.dim_y = self.imgarr.shape[1]
        self.center_x = math.floor(self.dim_x / 2)
        self.center_y = math.floor(self.dim_y / 2)
        self.stage_radius = self.img_size/2 - self.stage_margin
        self.wafer_radius = self.img_size/2 - self.img_margin
        self.notch_radius = round(1.25*(self.wafer_radius/100))
        self.grid_radius = 0.95*self.wafer_radius
        self.stage_color = stage_mid_color
        self.grid_color = grid_mid_color
        self.wafer_color = wafer_mid_color
        self.stage_random = stage_random
        self.wafer_random = wafer_random
        self.grid_random = grid_random
        self.boundary_box = []
    
    def GenerateJson(self , name , topr_x , topr_y , botr_x , botr_y):
        self.boundary_box.append({
            "label": f"{name}",
            "points": [[int(topr_x), int(topr_y)], [int(botr_x), int(botr_y)]],
            "group_id": None,
            "shape_type": "rectangle",
            "flags": {}
        })
        
    def Create_Stage(self):
        x1 = 0
        y1 = 0
        variation = math.floor(self.stage_random/2)
        for x in self.imgarr:
            y1 = 0
            for y in x:
                if ((x1-self.center_x) ** 2 + (y1-self.center_y) ** 2) <= (self.stage_radius ** 2):
                    self.imgarr[x1][y1] = self.stage_color + random.randint(-variation, variation)
                y1 = y1 +1
            x1 = x1 + 1

    def Create_Wafer_Edge(self):
        x1 = 0
        y1 = 0
        variation = math.floor(self.wafer_random/2)
        for x in self.imgarr:
            y1 = 0
            for y in x:

                if ((x1-self.center_x) ** 2 + (y1-self.center_y) ** 2) <= (self.wafer_radius ** 2):
                    self.imgarr[x1][y1] = self.wafer_color + random.randint(-variation, variation)
                y1 = y1 +1
            x1 = x1 + 1
            
    def Create_Notch(self):
        x1 = 0
        y1 = 0
        variation = math.floor(self.stage_random/2)
        for x in self.imgarr:
            y1 = 0
            for y in x:
                if ((x1-(self.center_x + self.wafer_radius)) ** 2 + (y1-self.center_y) ** 2) <= (self.notch_radius ** 2):
                    self.imgarr[x1][y1] = self.stage_color + random.randint(-variation, variation)
                y1 = y1 +1
            x1 = x1 + 1
            
    def Create_Grid(self):
        half_scribe_x = math.floor(self.scribe_x/2)
        half_scribe_y = math.floor(self.scribe_y/2)
        xi = 0
        x=0
        x_i = 0
        y=0
        y_i = 0
        variation = math.floor(self.grid_random/2)
        for x1 in self.imgarr:
            y = 0
            y_i = 0
            for y1 in x1:
                if (x == x_i):
                    #print("found_x")
                    xi = 1
                    if ((x-self.center_x) ** 2 + (y-self.center_y) ** 2) <= (self.grid_radius ** 2):
                        #print("found")
                        temp_x = x-half_scribe_x
                        while temp_x <= x+half_scribe_x:
                            self.imgarr[temp_x][y] = self.grid_color + random.randint(-variation, variation)
                            temp_x += 1
                if(y == y_i):
                    #print("found_y")
                    y_i += self.pitch_y
                    if ((x-self.center_x) ** 2 + (y-self.center_y) ** 2) <= (self.grid_radius ** 2):
                        #print("found")
                        temp_y = y-half_scribe_y
                        while temp_y <= y+half_scribe_y:
                            self.imgarr[x][temp_y] = self.grid_color + random.randint(-variation, variation)
                            temp_y += 1
                y += 1
            x += 1
            if(xi):
                x_i += self.pitch_x
                xi = 0
                
    def create_img(self):
        self.Create_Stage()
        self.Create_Wafer_Edge()
        self.Create_Grid()
        self.Create_Notch()
        print("Finish Wafer")

    def point_in_circle(self , center_x , center_y , radius):
        while True:
            x = np.random.randint(center_x - radius, center_x + radius + 1)
            y = np.random.randint(center_y- radius, center_y + radius + 1)
            if (x - center_x)**2 + (y - center_y)**2 <= radius**2:
                return x, y
    
    def DrawBoundary(self ,min_x , min_y , max_x , max_y , name , min_box_size):
        if name != 'Cloudy':
            width = abs(max_x - min_x)
            height = abs(max_y - min_y)
            if width < min_box_size:
                diff = min_box_size - width
                min_x -= diff // 2
                max_x += diff // 2
            if height < min_box_size:
                diff = min_box_size - height
                min_y -= diff // 2
                max_y += diff // 2
            #cv.rectangle(self.imgarr, (min_x - 2 , min_y - 2), (max_x + 2 , max_y + 2), (0, 0, 255), 1)
            self.GenerateJson(name=name , topr_x=min_x , topr_y= min_y , botr_x=max_x , botr_y= max_y)
            print(f"Finish Boundary for {name}")
        else:
            #cv.rectangle(self.imgarr, (min_x - 2 , min_y - 2), (max_x + 2 , max_y + 2), (0, 0, 255), 1)
            self.GenerateJson(name=name , topr_x=min_x , topr_y= min_y , botr_x=max_x , botr_y= max_y)
            print(f"Finish Boundary for {name}")

    def GenerateScratch(self, name, min_box_size, variance_add, scratch_variance, scratch_length, scratch_thickness,):
        x1, y1 = self.point_in_circle(self.center_x, self.center_y, self.grid_radius) # Check point in the circle
        angle = np.random.uniform(0, 2 * np.pi) # Generate a random 

        scratch_thickness = scratch_thickness - 1

        min_x = self.img_size
        max_x = 0
        min_y = self.img_size
        max_y = 0
        found = 0

        # Compute the x and y offsets using the angle and desired scratch length
        x2 = x1 + int(scratch_length * np.cos(angle))
        y2 = y1 + int(scratch_length * np.sin(angle))
        
        x = np.linspace(x1, x2, scratch_length, dtype=int) # Generate x array from start to end within the length
        y = np.linspace(y1, y2, scratch_length, dtype=int) # Generate y array from start to end within the length
           
        check_coords = [(ix, iy) for ix in range(-scratch_thickness, scratch_thickness + 1) 
                            for iy in range(-scratch_thickness, scratch_thickness + 1) 
                        if np.sqrt(ix**2 + iy**2) <= scratch_thickness]  
        
        
        for ix, iy in check_coords:
            x_check_coords = x + ix
            y_check_coords = y + iy
            valid_coords = (x_check_coords >= 0) & (x_check_coords < self.img_size) & (y_check_coords >= 0) & (y_check_coords < self.img_size) & (((x_check_coords-self.center_x) ** 2 + (y_check_coords-self.center_y) ** 2) <= (self.wafer_radius ** 2))
            x_check_coords, y_check_coords = x_check_coords[valid_coords], y_check_coords[valid_coords]
            
        for i in range(max(len(x_check_coords), len(y_check_coords))):
            if(variance_add == 2):
                self.imgarr[x_check_coords[i], y_check_coords[i]] = self.imgarr[x_check_coords[i], y_check_coords[i]] + random.randint(math.floor(scratch_variance/2), scratch_variance)
            else:
                self.imgarr[x_check_coords[i], y_check_coords[i]] = self.imgarr[x_check_coords[i], y_check_coords[i]] - random.randint(math.floor(scratch_variance/2), scratch_variance) 
            found = 1
            min_x = min(min_x, y_check_coords[i])
            max_x = max(max_x, y_check_coords[i])
            min_y = min(min_y, x_check_coords[i])
            max_y = max(max_y, x_check_coords[i])

        # Boundary Box
        #min_x = min(x) - scratch_thickness
        #min_y = min(y) - scratch_thickness
        #max_x = max(x) + scratch_thickness
        #max_y = max(y) + scratch_thickness
        if found == 1:
            self.DrawBoundary(min_x, min_y, max_x, max_y, name, min_box_size)
            
    def Cloudy_defect(self, min_r, max_r, set_radius_x, set_radius_y, min_box_size, name, blurriness,):
        x_radius = set_radius_x or random.randint(min_r, max_r)
        y_radius = set_radius_y or random.randint(min_r, max_r)

        min_x = self.img_size
        max_x = 0
        min_y = self.img_size
        max_y = 0
        found = 0
        
        if (x_radius > self.wafer_radius or y_radius > self.wafer_radius):
            return

        #while True:
        rand_x = random.randint(int(self.center_x - self.wafer_radius), int(self.center_x + self.wafer_radius))
        rand_y = random.randint(int(self.center_y - self.wafer_radius ), int(self.center_y + self.wafer_radius ))

            #Check if the entire ellipse lies within the wafer_radius
            #if all((((rand_x + dx) - self.center_x) ** 2 + ((rand_y + dy) - self.center_y) ** 2) <= self.wafer_radius ** 2 
            #    for dx in [-x_radius, x_radius] for dy in [-y_radius, y_radius]):
            #break
            
        if(blurriness % 2 == 0):
            blurriness += 1
        # Apply the Gaussian blur
        for i in range(1,blurriness,2):
            blurred_image = cv.GaussianBlur(self.imgarr, (i, i), 0)
        
        mask = np.zeros_like(self.imgarr)
        # Draw a ellipse on the mask.
        cv.ellipse(mask, (rand_x, rand_y), (x_radius, y_radius), 0, 0, 360, 255, -1)

        x1 = 0
        y1 = 0
        for x in mask:
            y1 = 0
            for y in x:
                if (not (((x1-self.center_x) ** 2 + (y1-self.center_y) ** 2) <= (self.wafer_radius ** 2))):
                    mask[x1, y1] = 0
                elif((((x1-self.center_x) ** 2 + (y1-self.center_y) ** 2) <= (self.wafer_radius ** 2))):
                    if(mask[x1,y1] == 255):
                        found = 1
                        min_x = min(min_x, y1)
                        max_x = max(max_x, y1)
                        min_y = min(min_y, x1)
                        max_y = max(max_y, x1)
                    
                y1 = y1 +1
            x1 = x1 + 1

        # Combine original and blurred images based on the mask.
        self.imgarr = cv.bitwise_and(self.imgarr, self.imgarr, mask=~mask)
        blurred_region = cv.bitwise_and(blurred_image, blurred_image, mask=mask)
        self.imgarr = cv.add(self.imgarr, blurred_region)
        
        # Draw the bounding box.
        #box_width = max(2 * x_radius, min_box_size)
        #box_height = max(2 * y_radius, min_box_size)
        #top_left = (int(rand_x - box_width / 2), int(rand_y - box_height / 2))
        #bottom_right = (int(rand_x + box_width / 2), int(rand_y + box_height / 2))
        if found == 1:
            self.DrawBoundary(min_x , min_y , max_x, max_y, name, min_box_size)

    def GenerateSpotDefects(self, name, min_box_size, spot_variance, spot_radius, variance_add):
        x, y = self.point_in_circle(self.center_x, self.center_y, self.grid_radius)

        min_x = self.img_size
        max_x = 0
        min_y = self.img_size
        max_y = 0
        found = 0

    # Now, create a spot defect at the given x, y with the desired radius.
        for dx in range(-spot_radius, spot_radius + 1):
            for dy in range(-spot_radius, spot_radius + 1):
                if dx**2 + dy**2 <= spot_radius**2:  # This ensures that we only draw inside the circle.
                    x_coord, y_coord = x + dx, y + dy
                    if (0 <= x_coord < self.img_size) and (0 <= y_coord < self.img_size):  # Ensure the coordinates are inside the image.
                        if(((x_coord-self.center_x) ** 2 + (y_coord-self.center_y) ** 2) <= (self.wafer_radius ** 2)):
                            if(variance_add == 2):
                                self.imgarr[x_coord][y_coord] = self.imgarr[x_coord][y_coord] + random.randint(math.floor(spot_variance/2), spot_variance)
                            else:
                                self.imgarr[x_coord][y_coord] = self.imgarr[x_coord][y_coord] - random.randint(math.floor(spot_variance/2), spot_variance)
                            found = 1
                            min_x = min(min_x, y_coord)
                            max_x = max(max_x, y_coord)
                            min_y = min(min_y, x_coord)
                            max_y = max(max_y, x_coord)
        # Boundary Box
        if found == 1:
            self.DrawBoundary(min_x , min_y , max_x, max_y, name , min_box_size)
        
    def GenerateRadial(self, name, min_box_size, radius, angle1, variance, variance_add):
        

        x1, y1 = self.point_in_circle(self.center_x, self.center_y, self.grid_radius)

        angle1 = math.floor(angle1/2)

        min_x = self.img_size
        max_x = 0
        min_y = self.img_size
        max_y = 0
        max_radius = self.grid_radius
        found =0

        # Set the triangle's height as a random value
        #triangle_height = random.uniform(0.1 * max_radius, 0.4 * max_radius)
        # Random angles for the radial defect
        #angle_start = random.uniform(0, 2 * np.pi)
        #angle_end = angle_start + ((angle1 * np.pi)/180)

        angle_help = np.arctan2((x1 - self.center_x), (y1 - self.center_y)) % (2 * np.pi)

        angle_start = angle_help - ((angle1 * np.pi)/180)
        angle_end = angle_help + ((angle1 * np.pi)/180)

        for x in range(self.img_size):
            for y in range(self.img_size):
                angle = np.arctan2(x - x1, y - y1) % (2 * np.pi) # find angle pixel respect to the center within 0 to 2pi
                # Calculate the maximum distance for a point to be considered within the triangle
                if angle_start <= angle <= angle_end:     # check if angle pixel lie within the angle
                    #triangle_ratio = (angle - angle_start) / (angle_end - angle_start) # How far triangle span
                    #max_distance = triangle_ratio * triangle_height    #maximum distance fro mthe center that pixel can be
                    #distance_to_edge = max_radius - np.sqrt((x - self.center_x)**2 + (y - self.center_y)**2) # radial distance from the center
                    #if 0 <= distance_to_edge <= max_distance:   # check if the pixel inside the triangle
                    #    # With a certain probability, fill the spot
                    new_x = x
                    new_y = y
                    if((new_x-x1) ** 2 + (new_y-y1) ** 2) <= (radius ** 2):
                    
                        # Ensure new_x and new_y are within image boundaries
                        if ((new_x-self.center_x) ** 2 + (new_y-self.center_y) ** 2) <= (self.wafer_radius ** 2):
                            if (variance_add == 2):
                                self.imgarr[new_x, new_y] = self.imgarr[new_x, new_y] + random.randint(math.floor(variance/2), variance)
                                
                            else:
                                self.imgarr[new_x, new_y] = self.imgarr[new_x, new_y] - random.randint(math.floor(variance/2), variance)
                            
                            found = 1
                            min_x = min(min_x, new_y)
                            max_x = max(max_x, new_y)
                            min_y = min(min_y, new_x)
                            max_y = max(max_y, new_x)
        if found==1:
            self.DrawBoundary(min_x , min_y  , max_x, max_y, name= name, min_box_size=min_box_size)
        
        
    def GenerateRadialDefect2(self, defect_length, thickness, num_lines_per_defect, spacing, line_height_scale , min_box_size):
        base_angle = np.random.uniform(0, 2 * np.pi)
        min_x, max_x, min_y, max_y = float('inf'), float('-inf'), float('inf'), float('-inf')  # Initialize min and max values

        for j in range(num_lines_per_defect):
            # Modify base_angle with a fixed spacin
            angle = base_angle + j * spacing
            
            # caculate line height
            length_offset = int(defect_length * np.random.uniform(-line_height_scale, line_height_scale))
            adjusted_defect_length = defect_length + length_offset

            x_start = self.center_x + int(self.grid_radius * np.cos(angle))
            y_start = self.center_y + int(self.grid_radius * np.sin(angle))

            x_end = x_start - int(adjusted_defect_length * np.cos(angle))
            y_end = y_start - int(adjusted_defect_length * np.sin(angle))

            x = np.linspace(x_start, x_end, adjusted_defect_length, dtype=int)
            y = np.linspace(y_start, y_end, adjusted_defect_length, dtype=int)

            self.imgarr[y, x] = np.random.randint(50, 90, size=x.shape)

            # Generating main line coordinates (with reduced thickness)
            line_coords = [(ix, iy) for ix in range(-thickness, thickness + 1) 
                for iy in range(-thickness, thickness + 1) 
                if np.sqrt(ix**2 + iy**2) <= thickness]

            for ix, iy in line_coords:
                x_line_coords = x + ix
                y_line_coords = y + iy
                valid_coords = (x_line_coords >= 0) & (x_line_coords < self.img_size) & (y_line_coords >= 0) & (y_line_coords < self.img_size)
                x_line_coords, y_line_coords = x_line_coords[valid_coords], y_line_coords[valid_coords]
                self.imgarr[y_line_coords, x_line_coords] = np.random.randint(50, 90, size=x_line_coords.shape)
        
            min_x = min(min_x, min(x))
            max_x = max(max_x, max(x))
            min_y = min(min_y, min(y))
            max_y = max(max_y, max(y))

        self.DrawBoundary(min_x , min_y  , max_x, max_y, name='Radial2' , min_box_size=min_box_size)
    
    def save_img(self , filename):
        cv.imwrite(filename, self.imgarr)
    
    def save_json(self , filename):
        data = {
            "version": "5.0.1",
            "flags": {},
            "shapes": self.boundary_box,
            "imagePath": filename,
            "imageData": None,
            "imageHeight": self.img_size,
            "imageWidth": self.img_size
        }
        json_file = os.path.join('img_data/', os.path.basename(filename).split('.')[0] + '.json')
        with open(json_file, 'w') as json_file:
            json.dump(data, json_file)
            
###################################################################################
    