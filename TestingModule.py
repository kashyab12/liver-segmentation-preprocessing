import cv2 # OpenCV Import
import numpy as np
import os

'''
    Simply validates the parse_points function via the DataPreprocessing Module.
    Performs a simple print to the console to ensure whether the parsed points are correct.
    
    Issue(s) - No issues as of now.
'''
def parse_points_print_test(xy_matrix_list, image_file_names):
    # Iterating over the matrices within the xy_matrix_list
    for matrix_idx in range(len(xy_matrix_list)):
        # Pretty Printing the X and Y pairs
        print("Matrix Number " + str(matrix_idx + 1) + ": " + str(image_file_names[matrix_idx]))
        for xy_point in xy_matrix_list[matrix_idx]:
            print("( " + str(xy_point[0]) + ", " + str(xy_point[1]) + ")", end = " | ")
        print()    
        
'''
    Enhanced validation function for the parse_points function from the DataPreprocessing Module.
    Creates an overlay over given CT-Scan Images based on the points parsed via the CSV File.

    Issue(s) - Further code optimization and refactorinf required.
'''
def parse_points_visual_test(xy_matrix_tuple, image_file_names, input_dir_name, input_file_dir_path, output_file_dir_path, output_ext = '.png', output_file_name = "-MaskedOutput"):
    
    # Setting the xy_matrix list and multi_ploy image lists via the tuple
    xy_matrix_list = xy_matrix_tuple[0]
    multi_poly_image = xy_matrix_tuple[1]
    
    # Creating output directory for the overlayed CT-Scan Images
    output_dir_path = input_dir_name + output_file_name + "/"
    
    # Try catch block in case the directory already exists.
    try:
        out_path = os.path.join(output_file_dir_path, output_dir_path)
        os.makedirs(out_path)
    except OSError as error:
        print("Error, directory already exists or issue while creating directory")
        
    for idx in range(len(image_file_names)):
    
        ct_image = cv2.imread(input_file_dir_path + "/" + image_file_names[idx]) # Reading the Input Image
        
        # Declaring constant values for the line drawing operation
        RED_COLOR = (0, 0, 255)
        LINE_THICKNESS = 4
    
        #  Converting the matrix of (x,y) points to a numpy array and reshaping its dimension
        liver_region = np.array(xy_matrix_list[idx])
        liver_region = liver_region.reshape((-1,1,2))
    
        # In the case of Mutliple Polygons within an image
        if len(multi_poly_image[idx]) != 0:
            # Setting the starting index for the masking
            start_idx = 0
            # This loop allows for multiple polylines to be drawn on the same image  without causing interference.
            for poly_idx in range(len(multi_poly_image[idx])):
                end_idx = multi_poly_image[idx][poly_idx]
                liver_overlay_img = cv2.fillPoly(ct_image, [liver_region[start_idx:end_idx]], RED_COLOR)
                start_idx = end_idx
                
                # In the case of the last polygon
                if poly_idx == len(multi_poly_image[idx]) - 1:
                    liver_overlay_img = cv2.fillPoly(ct_image, [liver_region[start_idx:]], RED_COLOR)
        else:
            # Filling the region of interest with RED
            liver_overlay_img = cv2.fillPoly(ct_image, [liver_region], RED_COLOR)
            
        # Regex Processing for naming output files properly.
        output_image_name = image_file_names[idx].split(".")
        
        # Saving / Writing the image to its respective folder (specified in the function input)
        cv2.imwrite(output_file_dir_path + output_dir_path + output_image_name[0] + output_file_name + output_ext, ct_image)       
    

    
    