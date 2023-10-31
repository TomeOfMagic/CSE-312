import streamlit as st
from GenerateData import GenerateData
import random
import os
import time

def save_base(gr , filename):
    gr.create_img()
    gr.save_img(filename)
    
    
img_size= 601
min_box_size = 20

radial_defect_name = 'radial'
spot_defect_name =  'spot'
cloudy_defect_name = 'cloudy'
line_defect_name = 'scratch'

defect_min = 1
defect_max = 5

#parameters to generate base image
chip_low = 70
chip_high = 200
stage_low = 20
stage_high = 40
grid_darkness = 20 ##how much darker than the wafer the grid is
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

#parameters to generate defects
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
radial_variance_min = 30
radial_variance_max = 40
radial_angle_min = 1
radial_angle_max = 10
radial_radius_min = 10
radial_radius_max = 40


#end of changeable parameters
stage_mid_color = random.randint(stage_low, stage_high)
wafer_mid_color = random.randint(chip_low, chip_high)
grid_mid_color = (wafer_mid_color - grid_darkness)

scratch_varince_add = random.randint(1, 2)
scratch_variance = random.randint(scratch_variance_min, scratch_variance_max)
scratch_length = random.randint(scratch_length_min, scratch_length_max)
scratch_thickness = random.randint(scratch_thickness_min,scratch_thickness_max)

spot_variance = random.randint(spot_variance_min, spot_variance_max)
spot_radius = random.randint(spot_radius_min, spot_radius_max)
spot_variance_add = random.randint(1,2)

radial_radius = random.randint(radial_radius_min, radial_radius_max)
radial_angle = random.randint(radial_angle_min, radial_angle_max)
radial_variance = random.randint(radial_variance_min, radial_variance_max,)
radial_variance_add = random.randint(1,2)


# Insert containers separated into tabs:
tab1, tab2 = st.sidebar.tabs(["Image", "Defects"])
tab1.write("Please Enter Silicon Wafer Dimensions")


with tab1:
    
    # Width of Grid
    set_pitch_x = st.number_input("Width of Grid",step=1)
    rndwg = st.checkbox('Randomize', key='rndwg_key')
    if rndwg:
        set_pitch_x = random.randint(pitch_min, pitch_max)

    # Height of Grid
    set_pitch_y  = st.number_input("Height of Grid",step=1)
    rndhg = st.checkbox('Randomize', key='rndhg_key')
    if rndhg:
        set_pitch_y = random.randint(pitch_min, pitch_max)
        
    # Vertical Line Thickness
    set_scribe_y = st.number_input("Verical Line Thickness",step=1)
    rndvt = st.checkbox('Randomize', key='rndvt_key')
    if rndvt:
        set_scribe_y = random.randint(scribe_min, scribe_max)

    # Horizontal Line Thickness
    set_scribe_x  = st.number_input("Horizontal Line Thickness",step=1)
    rndht = st.checkbox('Randomize', key='rndht_key')
    if rndht:
        set_scribe_x = random.randint(scribe_min, scribe_max)
    
    st.header("Proceed to next tab to enter defects")

    
with tab2:
    st.write("Please Enter Defects")
    #spot defects
    spot = st.number_input("Number of Spot Defects",step=1)
    rndSp = st.checkbox('Randomize', key='rndSp_key')
    
    #Scratch defects
    scratch = st.number_input("Number of Scratch Defects",step=1)
    rndSc = st.checkbox('Randomize', key='rndSc_key')
    
    #Cloudy defects
    cloudy = st.number_input("Number of Cloudy Defects",step=1)
    rndCl = st.checkbox('Randomize', key='rndCl_key')
    
    #Radial defects
    radial = st.number_input("Number of Radial Defects",step=1)
    rndRd = st.checkbox('Randomize', key='rndRd_key')
    
    submit_button1 = st.button('Submit', key='submit_button1')

if submit_button1: 
    
    gr = GenerateData(
        img_size,
        chip_low,
        chip_high,
        stage_mid_color,
        wafer_mid_color,
        grid_mid_color,
        stage_random = random.randint(stage_variation_low, stage_variation_high),
        wafer_random = random.randint(wafer_variation_low, wafer_variation_high),
        grid_random = random.randint(grid_variation_low, grid_variation_high),
        pitch_x = set_pitch_x,
        pitch_y = set_pitch_y,
        scribe_x = set_scribe_x,
        scribe_y = set_scribe_y,
    )
    
    gr.create_img()
    
    if rndSp:
        spot = random.randint(defect_min, defect_max)

    for i in range(spot): 
        gr.GenerateSpotDefects(spot_defect_name, min_box_size, spot_variance, spot_radius, spot_variance_add)
    
    if rndSc:
        scratch = random.randint(defect_min, defect_max)
    
    for i in range(scratch):
        gr.GenerateScratch(line_defect_name, min_box_size, scratch_varince_add, scratch_variance, scratch_length, scratch_thickness)
    
    if rndCl:
        cloudy = random.randint(defect_min, defect_max)
    
    for i in range (cloudy):
        gr.Cloudy_defect(cloudy_radius_min , cloudy_radius_max, set_pitch_x, set_pitch_y, min_box_size, cloudy_defect_name, cloudy_blurriness)
    
    if rndRd:
        radial = random.randint(defect_min, defect_max)
    
    for i in range(radial):
        gr.GenerateRadial(radial_defect_name, min_box_size, radial_radius, radial_angle, radial_variance, radial_variance_add)
    
    gr.save_img(filename="base_img/baseimg.jpg")
    


base_image = './base_img/baseimg.jpg'
# Create columns within the container
col1, col2,= st.columns([1, 1])
# Place images into the columns
with col1:
    
    if submit_button1: 
        with st.spinner(text='In progress'):
            time.sleep(5)
            
    if os.path.exists(base_image):
        st.image(base_image)
    else:
       st.write("Generate Base Image")
       
       
defects = spot + scratch + cloudy + radial


with col2:
    if os.path.exists(base_image):
        st.write("Details for Base Image")
        st.write("Image Size: ", img_size, "x", img_size, "pixels")
        st.write("Width of Grid: ", set_pitch_x)
        st.write("Height of Grid: ", set_pitch_y)
        st.write("Vertical Line Thickness: ", set_scribe_y)
        st.write("Horizontal Line Thickness: ", set_scribe_x)
        st.write("Number of Defects: ", defects)
    
# with col2:
#     st.write("Details for image 1")
    
# col3, col4,= st.columns([1, 1])

# with col3:
#     st.image('./Image/Screenshot 2023-10-19 at 10.13.39 PM.png')
#     st.write("Caption for Image 2")

# with col4:
#     st.image('./Image/Screenshot 2023-10-19 at 10.13.39 PM.png')

