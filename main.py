from GenerateData import GenerateData
from PIL import Image
import numpy as np
import random


def save_base(gr , filename):
    gr.create_img()
    gr.save_img(filename)
    
if __name__ == '__main__':
    ##different paramters to change:
    
    number_of_images = 10
    number_of_reuse = 1 #how images will share the same background
    
    img_size= 601
    min_box_size = 20




    radial_defect_name = 'radial'
    spot_defect_name =  'spot'
    cloudy_defect_name = 'cloudy'
    line_defect_name = 'scratch'

    set_chip_color = None ##if you want to set the color directly
    set_stage_color = None ##if you want to set the color directly
    set_grid_color = None ##if you want to set the color directly
    set_grid_difference = None ## how much brighter or darker the grid is to the wafer
    set_grid_darker = None ##set to 1 if you want to make grid darker than wafer and 2 to make grid brighter otherwise random
    set_pitch_x = None ##if you want to set how big the grid is directly
    set_pitch_y = None ##if you want to set how big the grid is directly
    set_scribe_x = None ##if you want to set how thick the grid lines are
    set_scribe_y = None ##if you want to set how thick the grid lines are
    set_number_defects = None ##if you want to set how many defects per image
    set_cloudy_radius_x = None ##if you want to set the radius of the cloudy circle/oval
    set_cloudy_radius_y = None ##if you want to set the radius of the cloudy circle/oval
    set_cloudy_variance = None
    set_cloudy_variance_add = None ##set to 1 to make scratchs darker than base, 2 to make scratchs lighter than base
    set_cloudy_boundary = None ##how many pixels should the edge of any cloudy oval be from the wafer_edge
    set_scratch_length = None
    set_scratch_thickness = None
    set_scratch_variance = None
    set_scratch_variance_add = None ##set to 1 to make scratchs darker than base, 2 to make scratchs lighter than base
    set_spot_variance = None
    set_spot_radius = None
    set_spot_variance_add = None ##set to 1 to make spot darker than base, 2 to make scratchs lighter than base
    set_radial_radius = None
    set_radial_variance = None
    set_radial_angle = None
    set_radial_variance_add = None ##set to 1 to make radial darker than base, 2 to make scratchs lighter than base

    defect_min = 1
    defect_max = 5

    cloudy_check_inside = False ## set to true to check whether the entire clody rectangle is inside the wafer or not

    chip_low = 70
    chip_high = 200
    stage_low = 20
    stage_high = 40
    min_grid_difference = 10
    max_grid_difference = 20 
    pitch_min = 10
    pitch_max = 15
    scribe_min = 1
    scribe_max = 3
    stage_variation_low = 5
    stage_variation_high = 10
    wafer_variation_low = 5
    wafer_variation_high = 10
    grid_variation_low = 2
    grid_variation_high = 5

    scratch_length_min = 10
    scratch_length_max = 20
    scratch_thickness_min = 1
    scratch_thickness_max = 2
    scratch_variance_min = 30
    scratch_variance_max = 40

    spot_radius_min = 1
    spot_radius_max = 3
    spot_variance_min = 20
    spot_variance_max = 30

    cloudy_radius_min = 5
    cloudy_radius_max = 20
    cloudy_blurriness = 5 ##should only be odd but no error just adds one
    min_cloudy_variance = 20
    max_cloudy_variance = 30
    min_cloudy_boundary = 3
    max_cloudy_boundary = 7

    radial_variance_min = 30
    radial_variance_max = 40
    radial_angle_min = 1
    radial_angle_max = 10
    radial_radius_min = 10
    radial_radius_max = 40


    #end of changeable parameters

    



    stage_mid_color = set_stage_color or random.randint(stage_low, stage_high)
    wafer_mid_color = set_chip_color or random.randint(chip_low, chip_high)
    grid_darker = set_grid_darker or random.randint(1,2)
    grid_difference = set_grid_difference or random.randint(min_grid_difference, max_grid_difference)
    if(grid_darker == 2):
        grid_mid_color = set_grid_color or (wafer_mid_color + grid_difference)
    else: 
        grid_mid_color = set_grid_color or (wafer_mid_color - grid_difference)

    pitch_x = set_pitch_x or random.randint(pitch_min, pitch_max)
    pitch_y = set_pitch_y or random.randint(pitch_min, pitch_max)
    scribe_x = set_scribe_x or random.randint(scribe_min, scribe_max)
    scribe_y = set_scribe_y or random.randint(scribe_min, scribe_max)
    
    stage_random = random.randint(stage_variation_low, stage_variation_high)
    wafer_random = random.randint(wafer_variation_low, wafer_variation_high)
    grid_random = random.randint(grid_variation_low, grid_variation_high)


    gr = GenerateData(
        img_size,
        chip_low,
        chip_high,
        stage_mid_color,
        wafer_mid_color,
        grid_mid_color,
        stage_random,
        wafer_random,
        grid_random,
        pitch_x,
        pitch_y,
        scribe_x,
        scribe_y,
        
    )
    
    save_base(gr , "base_img/baseimg.jpg")
    
    for i in range(number_of_images):
        
        if(i % number_of_reuse == 0):
            stage_mid_color = set_stage_color or random.randint(stage_low, stage_high)
            wafer_mid_color = set_chip_color or random.randint(chip_low, chip_high)
            grid_darker = set_grid_darker or random.randint(1,2)
            grid_difference = set_grid_difference or random.randint(min_grid_difference, max_grid_difference)
            if(grid_darker == 2):
                grid_mid_color = set_grid_color or (wafer_mid_color - grid_difference)
            else: 
                grid_mid_color = set_grid_color or (wafer_mid_color + grid_difference)

            pitch_x = set_pitch_x or random.randint(pitch_min, pitch_max)
            pitch_y = set_pitch_y or random.randint(pitch_min, pitch_max)
            scribe_x = set_scribe_x or random.randint(scribe_min, scribe_max)
            scribe_y = set_scribe_y or random.randint(scribe_min, scribe_max)
    
            stage_random = random.randint(stage_variation_low, stage_variation_high)
            wafer_random = random.randint(wafer_variation_low, wafer_variation_high)
            grid_random = random.randint(grid_variation_low, grid_variation_high)

            gr = GenerateData(
            img_size,
            chip_low,
            chip_high,
            stage_mid_color,
            wafer_mid_color,
            grid_mid_color,
            stage_random ,
            wafer_random,
            grid_random,
            pitch_x,
            pitch_y,
            scribe_x,
            scribe_y,)

        gr.create_img()
        defect = set_number_defects or random.randint(defect_min, defect_max)
        
        
        for z in range(defect):

            cloudy_variance_add = set_cloudy_variance_add or random.randint(1,2)
            cloudy_variance = set_cloudy_variance or random.randint(min_cloudy_variance, max_cloudy_variance)
            cloudy_boundary = set_cloudy_boundary or random.randint(min_cloudy_boundary, max_cloudy_boundary)
            
            scratch_varince_add = set_scratch_variance_add or random.randint(1, 2)
            scratch_variance = set_scratch_variance or random.randint(scratch_variance_min, scratch_variance_max)
            scratch_length = set_scratch_length or random.randint(scratch_length_min, scratch_length_max)
            scratch_thickness = set_scratch_thickness or random.randint(scratch_thickness_min,scratch_thickness_max)
            
            spot_variance = set_spot_variance or random.randint(spot_variance_min, spot_variance_max)
            spot_radius = set_spot_radius or random.randint(spot_radius_min, spot_radius_max)
            spot_variance_add = set_spot_variance_add or random.randint(1,2)

            radial_radius = set_radial_radius or random.randint(radial_radius_min, radial_radius_max)
            radial_angle = set_radial_angle or random.randint(radial_angle_min, radial_angle_max)
            radial_variance = set_radial_variance or random.randint(radial_variance_min, radial_variance_max,)
            radial_variance_add = set_radial_variance_add or random.randint(1,2)


            random_defect = random.randint(1,4)
            if (random_defect == 1):
                done = gr.GenerateScratch(line_defect_name, min_box_size, scratch_varince_add, scratch_variance, scratch_length, scratch_thickness)
            if (random_defect == 2):
                done = gr.GenerateSpotDefects(spot_defect_name, min_box_size, spot_variance, spot_radius, spot_variance_add)
            if (random_defect == 3):
                done = gr.Cloudy_defect(cloudy_radius_min , cloudy_radius_max, set_cloudy_radius_x, set_cloudy_radius_y, min_box_size, cloudy_defect_name, cloudy_blurriness, cloudy_variance, cloudy_variance_add, cloudy_boundary, cloudy_check_inside)
            if (random_defect == 4):
                done = gr.GenerateRadial(radial_defect_name, min_box_size, radial_radius, radial_angle, radial_variance, radial_variance_add)
                # gr.GenerateRadialDefect2(min_box_size = min_box_size ,defect_length=random.randint(30, 50) , thickness=random.randint(1,5) , num_lines_per_defect=random.randint(2,5) , spacing=random.uniform(0.03 , 0.05) , line_height_scale=random.uniform(0.1,0.7))
            if(done == 0):
                defect = defect - 1

        
        #gr.GenerateScratch(line_defect_name, min_box_size, scratch_varince_add, scratch_variance, scratch_length, scratch_thickness)
        #gr.GenerateSpotDefects(spot_defect_name, min_box_size, spot_variance, spot_radius, spot_variance_add)
        #gr.Cloudy_defect(cloudy_radius_min , cloudy_radius_max, set_cloudy_radius_x, set_cloudy_radius_y, min_box_size, cloudy_defect_name, cloudy_blurriness)
        #gr.GenerateRadial(radial_defect_name, min_box_size, radial_radius, radial_angle, radial_variance, radial_variance_add)
        gr.save_img(filename= f'img_data/test{i+1}.jpg')
        gr.save_json(filename= f'test{i+1}.jpg')
        print("done")