import os
import numpy as np
from skimage import color, exposure, io, transform
import matplotlib.pyplot as plt
import os
import random
import pandas as pd

import os
import pandas as pd


def get_image_list(root_path):
    image_list = []
    for root, dirs, files in os.walk(root_path):
        for filename in files:
            if filename.endswith(('.jpeg', '.jpg')):
                image_list.append(os.path.join(root, filename))
    return image_list


# def get_lake_color_characterstics(lakecam_images_path):
#     # Get lists of image file paths
#     lakecam_image_list = get_image_list(lakecam_images_path)
#
#     # Load the set of images taken from the lake camera
#     lake_images = [io.imread(image_path) for image_path in lakecam_image_list]
#
#     # Calculate the mean and standard deviation of each channel in LAB color space for the lake images
#     lake_mean = np.mean([color.rgb2lab(img).mean(axis=(0, 1)) for img in lake_images], axis=0)
#     lake_std = np.mean([color.rgb2lab(img).std(axis=(0, 1)) for img in lake_images], axis=0)
#
#     return lake_mean, lake_std

def get_lake_color_characteristics(lakecam_images_path):
    # Get lists of image file paths
    lakecam_image_list = get_image_list(lakecam_images_path)

    # Load the set of images taken from the lake camera
    lake_images = [io.imread(image_path) for image_path in lakecam_image_list]

    # Calculate the mean and standard deviation of each channel in LAB color space for the lake images
    lake_mean = np.mean([color.rgb2lab(img).mean(axis=(0, 1)) for img in lake_images], axis=0)
    lake_std = np.mean([color.rgb2lab(img).std(axis=(0, 1)) for img in lake_images], axis=0)

    # Create a pandas DataFrame with the lake mean and standard deviation
    df = pd.DataFrame({'lake_mean': lake_mean, 'lake_std': lake_std})

    # Get the current working directory and concatenate the Excel file name to it
    current_directory = os.getcwd()
    excel_file_path = os.path.join(current_directory, 'lake_color_characteristics.xlsx')

    # Write the DataFrame to an Excel file with headers
    df.to_excel(excel_file_path, index=False, header=['lake_mean', 'lake_std'], mode='w')

    return lake_mean, lake_std


def load_lake_color_characteristics(excel_file_name):
    # Get the Excel file path
    current_directory = os.getcwd()
    excel_file_path = os.path.join(current_directory, excel_file_name)

    # Load the Excel file as a pandas DataFrame, or return None if it doesn't exist
    if not os.path.exists(excel_file_path):
        print(f"Excel file '{excel_file_name}' doesn't exist in the current directory.")
        return None
    df = pd.read_excel(excel_file_path)

    # Extract the lake mean and standard deviation from the DataFrame
    lake_mean = df['lake_mean'].values
    lake_std = df['lake_std'].values

    return lake_mean, lake_std


def color_transfer_on_image(lab_image, lake_mean, lake_std):

    # Calculate the mean and standard deviation of each channel in LAB color space for the input lab image
    lab_mean = color.rgb2lab(lab_image).mean(axis=(0, 1))
    lab_std = color.rgb2lab(lab_image).std(axis=(0, 1))

    # Compute the color transform from the lab image to the lake image
    a = (lake_std / lab_std) * (color.rgb2lab(lab_image) - lab_mean) + lake_mean
    img_transfer = color.lab2rgb(a)

    return img_transfer


def color_transfer_on_image_list(input_directory, lake_mean, lake_std, output_directory):
    # Create the output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    # Iterate over all the LAB images in the input directory
    for filename in os.listdir(input_directory):
        if not filename.endswith('.jpg'):
            continue
        # Load the LAB image
        lab_image_path = os.path.join(input_directory, filename)
        lab_image = io.imread(lab_image_path)

        # Calculate the mean and standard deviation of each channel in LAB color space for the input lab image
        lab_mean = color.rgb2lab(lab_image).mean(axis=(0, 1))
        lab_std = color.rgb2lab(lab_image).std(axis=(0, 1))

        # Compute the color transform from the lab image to the lake image
        a = (lake_std / lab_std) * (color.rgb2lab(lab_image) - lab_mean) + lake_mean
        img_transfer = color.lab2rgb(a)

        # Save the result as a JPEG image in the output directory
        output_path = os.path.join(output_directory, filename)
        io.imsave(output_path, img_transfer, quality=95)

    return




#
# lakecam_images_path = 'RGB color correction/lakecam'
#
# lake_mean, lake_std = get_lake_color_characterstics(lakecam_images_path)
#
# # Set the path to the image folder
# image_folder = 'RGB color correction/labcam/1585731301/images/'
#
# # Get a list of all the image filenames in the folder
# image_filenames = os.listdir(image_folder)
#
# # Select 5 random image filenames
# random_filenames = random.sample(image_filenames, 5)
#
# # Create a subplot with 5 rows and 2 columns
# fig, ax = plt.subplots(5, 2, figsize=(10, 20))
#
# # Iterate over the 5 random filenames and plot the original and transferred images side by side
# for i, filename in enumerate(random_filenames):
#     # Load the lab image
#     lab_image = io.imread(os.path.join(image_folder, filename))
#
#     # Transfer the color characteristics of the lake image to the lab image
#     transferred_image = color_transfer(lab_image, lake_mean, lake_std)
#
#     # Plot the original and transferred images side by side
#     ax[i, 0].imshow(lab_image)
#     ax[i, 0].set_title('Original Lab Image')
#     ax[i, 1].imshow(transferred_image)
#     ax[i, 1].set_title('Transferred Lab Image')
#
# # Adjust the spacing between the subplots and show the plot
# plt.tight_layout()
# plt.show()