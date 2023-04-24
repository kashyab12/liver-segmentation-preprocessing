import pandas as pd
import re

'''
    Method to read a CSV file and Obtain all the required X and Y values for the 
        polygon segementations.
        
    Issue(s) 
        (1) Looking into whether xy_matrix_list needs to be a NumPy Matrix
        (2) Look into returning the name of the respective CT-Scan Image along with 
            its respective Matrix. This would allow for the correlation of the CT-Scan
            Image and its matrix which would be used when creating the overlay for the  
            segment.
        (3) Optimization of the method of handling multiple polygons within an
            image. Current method being used would be slightly slower per iter.
            as two unnecessary if statements need to be checked for 'n-1' images,
            rather than just 1 if statement.
        (4) Could Optimize code by taking advantage of the Other Data given within the 
            .csv file such as Region Count to reduce search space.
'''
def parse_points(file_dir_name, COLUMN_NAME = 'region_shape_attributes', COMPARISION_FIELD = 'filename'):

    # Stores all of the Matrices containing respective XY pairs.
    xy_matrix_list = []
    # Stores the indices of the labelled polygons within a CT Scan (For the edge case of multiple polygons)
    multi_poly_image = []

    # Reading the CSV file via Pandas function
    ct_dataframe = pd.read_csv(file_dir_name)
    
    # Obtaining all the non-null column value strings
    column_values =  [col_val for col_val in ct_dataframe[COLUMN_NAME] if col_val != '{}']

    # Used to mitigate the issue of multiple polygons within an Image (This method can be further optimized)
    prev_attribute = 0

    '''
    Performing some String Regex to Narrow down the important data and retrieve the 
    X and Y values within their respective arrays.
    '''
    for attribute in column_values:
        
        multi_poly_index=[]

        # Narrow down results in a manner applicable for all the data files.
        refined_column = re.split('{|:|}', attribute)
        refined_column = [string for string in refined_column if any(character.isdigit() for character in string)]
        
        # Perform regex processing on the x and y strings to obtain the values in an array
        x_values = point_string_to_list(refined_column[0])
        y_values = point_string_to_list(refined_column[-1])
        
        # Combining the X and Y values into a list of [x,y] points
        xy_values = []
        for ctr in range(len(x_values)):
            xy_values.append([x_values[ctr], y_values[ctr]])

        ''' 
        Checking whether the points are part of the same image as the previous matrix of points 
        '''
        # Avoiding case of empty matrix list
        if len(xy_matrix_list) != 0 and ct_dataframe.loc[ct_dataframe[COLUMN_NAME] == 
                prev_attribute, COMPARISION_FIELD].item() == ct_dataframe.loc[ct_dataframe[COLUMN_NAME] == attribute, COMPARISION_FIELD].item():
            
            # Storing the last index of the previous polygon
            multi_poly_image[-1].append(len(xy_matrix_list[-1]))
            
            # We will append the xy_values to the previous matrix list
            for xy_val in xy_values:
                xy_matrix_list[-1].append(xy_val)
        else:
            # Just appending an empty list in case of no presence of multiple polygons
            multi_poly_image.append(multi_poly_index)
            # Adding the list of x and y values to their respective unique matrix.
            xy_matrix_list.append(xy_values)

        # Storing the previous attribute so as to check for polygons of the same image
        prev_attribute = attribute
        
    # Returning a tuple of the xy_matrix of points and their respective multi_poly_index list
    return (xy_matrix_list, multi_poly_image);

'''
    Method to return the file names of all the CT-Scan .jpg files which have the region
        of interest (the liver) labelled.
        
    Issue(s) - None currently
'''
def get_image_file_name(file_dir_name, COLUMN_NAME='filename', FILTER_COLUMN='region_shape_attributes'):
    
    # Reading the CSV file via Pandas function
    ct_dataframe = pd.read_csv(file_dir_name)
    
    # Filtering for non null entries
    is_labelled = ct_dataframe[FILTER_COLUMN]!='{}'
    
    # Shrink the dataframe to the relevant entries
    ct_dataframe_non_null = ct_dataframe[is_labelled] # Remove null elements of the column
    ct_dataframe_drop_duplicate = ct_dataframe_non_null.drop_duplicates(subset=COLUMN_NAME) # Remove duplicate Image names
    
    # Store all file names whose region points are non empty
    ct_image_names = [col_val for col_val in ct_dataframe_drop_duplicate[COLUMN_NAME]]
    
    return ct_image_names;

'''
    Helper Function
    ---
    Used to convert a string of numbers (comma seperated) into an array.
    
    Issues(s): Think more on the selection process for the String of Numbers
'''
def point_string_to_list(xy_string):
    xy_string = re.split('\[|\]', xy_string) # Removing unecessary values
    xy_string = [string for string in xy_string if any(character.isdigit() for character in string)][0]
    xy_val = [int(s) for s in xy_string.split(',')] # Convert string of numbers seperated by commas to a list.
    return xy_val;