'''
Glossary
---
ROI: Region of Interest
'''

# Import Statements
import DataPreprocessing as dp
import TestingModule as tm
import ImageProcessing as ip

# Directories for Input and Output

## Base Directories
INPUT_DIR = 'Input/'
OUTPUT_DIR = 'Output/S5020/'

## CSV File Name
TEST_CSV_INPUT = 'S5020.csv'

## CT Scan Original Raw Image Directory Name
TEST_CT_INPUT_DIR = 'S5020'

## Target Directory for the Masked and Focused ROI Directories
MASKED_ROI_DIR = '-MaskedOutput/'
FOCUSED_ROI_DIR = '-FocusedROIOutput/'

# Parsing Data
## Parsing the xy points for the ROI (Please note that a tuple is returned in order to handle Images with Multiple ROI's)
xy_matrix_tuple = dp.parse_points(INPUT_DIR + TEST_CSV_INPUT)
image_file_names = dp.get_image_file_name(INPUT_DIR + TEST_CSV_INPUT)

# Testing Parsing of the XY Points
## Testing the Parsed XY Points via Printing to Console
tm.parse_points_print_test(xy_matrix_tuple[0], image_file_names)
## Applying a mask over the ROI
tm.parse_points_visual_test(xy_matrix_tuple, image_file_names, input_dir_name=TEST_CT_INPUT_DIR, input_file_dir_path=INPUT_DIR + TEST_CT_INPUT_DIR, output_file_dir_path=OUTPUT_DIR)
## 2D Visualization of the Masked CT Scan Images
# ip.volume_rendering(OUTPUT_DIR + TEST_CT_INPUT_DIR + MASKED_ROI_DIR)

# Removal of Unneccesary Regions i.e. regions which aren't the ROI
## Now let us make all the regions except the Region of Interest Transparent
ip.transparent_background(xy_matrix_tuple, image_file_names, TEST_CT_INPUT_DIR, INPUT_DIR + TEST_CT_INPUT_DIR, OUTPUT_DIR)
## 2D and 3D Visualization of the Liver
ip.volume_rendering(OUTPUT_DIR + TEST_CT_INPUT_DIR + FOCUSED_ROI_DIR)


    
