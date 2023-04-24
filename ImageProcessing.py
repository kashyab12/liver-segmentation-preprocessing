import numpy as np
import cv2
import napari
import os
import glob
from skimage import data,io
from skimage.feature import register_translation
from scipy.ndimage import fourier_shift
from scipy.ndimage import shift

'''
    Method to make the regions except the ROI transparent
    
    Issue(s) - Code can be further refactored and optimized.     
'''
def transparent_background(xy_matrix_tuple, image_file_names, input_dir_name, input_file_dir_path, output_file_dir_path, output_ext = '.png', output_file_name = "-FocusedROIOutput"):
    
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

        WHITE_COLOR = (255,255,255)
    
        liver_region = np.array(xy_matrix_list[idx])
        liver_region = liver_region.reshape((-1,1,2))
        ct_image = cv2.imread(input_file_dir_path + "/" + image_file_names[idx]) # Reading the Input Image
        mask = np.zeros(ct_image.shape, dtype=np.uint8)
        start_idx = 0

        # In the case of Mutliple Polygons within an image
        if len(multi_poly_image[idx]) != 0:
            # This loop allows for multiple polylines to be drawn on the same image  without causing interference.
            for poly_idx in range(len(multi_poly_image[idx])):
                end_idx = multi_poly_image[idx][poly_idx]
                cv2.fillPoly(mask, [liver_region[start_idx:end_idx]], WHITE_COLOR)
                start_idx = end_idx
                
                
        liver_overlay_img = cv2.fillPoly(mask, [liver_region[start_idx:]], WHITE_COLOR)

        # apply the mask to remove all the Non-ROI background
        masked_image = cv2.bitwise_and(ct_image, mask)

        # Converting from a black background to a transparent background
        bgra_scheme = cv2.cvtColor(masked_image, cv2.COLOR_BGR2BGRA)
        # Slice of alpha channel
        alpha = bgra_scheme[:, :, 3]
        # Use logical indexing to set alpha channel to 0 where BGR=0
        alpha[np.all(bgra_scheme[:, :, 0:3] == (0, 0, 0), 2)] = 0
            
        # Regex Processing for naming output files properly.
        output_image_name = image_file_names[idx].split(".")
        
        # Saving / Writing the image to its respective folder (specified in the function input)
        cv2.imwrite(output_file_dir_path + output_dir_path + output_image_name[0] + output_file_name + output_ext, bgra_scheme)

    
'''
    Method to concatenate the 2D matrices (2D Slices) to form a 3D matrix (3D volume).
    
    Issue(s) - None as of now
'''
def volume_rendering(input_path, input_ext=".png"):
    slice_collection = io.imread_collection(input_path + "*" + input_ext)
    three_dim_volume = np.array(slice_collection.concatenate())
    print(three_dim_volume.shape)
    # io.imsave(input_path + "3DVolumeRendering" + output_ext, three_dim_volume)
    viewer = napari.view_image(three_dim_volume, rgb=True)
    napari.run()

'''
    Usage of Phase Corelation to Register the Volumes to one another
    
    Issue(s) - Need to fix Input and Output and Test
'''
def image_registration(original_image_dir_path, offset_image_dir_name, offset_image_dir_path, output_dir,  image_ext="*.jpg", UPSAMPLING_FACTOR=100):

    original_image_files = glob.glob(original_image_dir + image_ext)
    offset_image_files = glob.glob(offset_image_dir + image_ext)    

    for idx in range(len(original_image_dir)):
        image = io.imread(original_image_files[idx])
        offset_image = io.imread(offset_image_files[idx])

        shifted, error, diffphase = register_translation(image, offset_image, UPSAMPLING_FACTOR)
        corrected_image = shift(offset_image, shift=(shifted[0], shifted[1], shifted[2]), mode='constant')

