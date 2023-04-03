import os

import imageio
import numpy as np
import pandas as pd
import skimage
from skimage import color, io


def get_image_list(root_path):
    image_list = []
    for root, dirs, files in os.walk(root_path):
        for filename in files:
            if filename.endswith(('.jpeg', '.jpg')):
                image_list.append(os.path.join(root, filename))
    return image_list


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
    # df.to_excel(excel_file_path, index=False, header=['lake_mean', 'lake_std'], mode='w')
    df.to_excel(excel_file_path, index=False, header=['lake_mean', 'lake_std'])

    return lake_mean, lake_std


def color_transfer_on_single_image(labcam_image_path, lake_mean, lake_std, output_directory):
    # Load the LAB image
    lab_image = io.imread(labcam_image_path)

    # Calculate the mean and standard deviation of each channel in LAB color space for the input lab image
    lab_mean = color.rgb2lab(lab_image).mean(axis=(0, 1))
    lab_std = color.rgb2lab(lab_image).std(axis=(0, 1))

    # Compute the color transform from the lab image to the lake image
    a = (lake_std / lab_std) * (color.rgb2lab(lab_image) - lab_mean) + lake_mean
    img_transfer = color.lab2rgb(a)

    # Get the file name from the lab_image_path
    filename = os.path.basename(labcam_image_path)

    # Save the result as a JPEG image in the output directory
    output_path = os.path.join(output_directory, filename)
    os.makedirs(output_directory, exist_ok=True)

    # Convert the image to uint8
    img_uint8 = skimage.img_as_ubyte(img_transfer)

    # Save the uint8 image
    imageio.imwrite(output_path, img_uint8)

    # pb.stop()

    return img_transfer

#
# def color_transfer_on_single_image_2(labcam_image_path, lake_mean, lake_std, output_directory):
#     # Load the LAB image
#     lab_image = io.imread(labcam_image_path)
#
#     # Calculate the mean and standard deviation of each channel in LAB color space for the input lab image
#     lab_mean = color.rgb2lab(lab_image).mean(axis=(0, 1))
#     lab_std = color.rgb2lab(lab_image).std(axis=(0, 1))
#
#     # Calculate the first three moments of the color distribution for the lake and lab images
#     lake_moments = color.rgb2lab(skimage.io.imread(lake_image_path)).mean(axis=(0, 1)), \
#                    color.rgb2lab(skimage.io.imread(lake_image_path)).std(axis=(0, 1)), \
#                    skew(color.rgb2lab(skimage.io.imread(lake_image_path)).flatten())
#     lab_moments = lab_mean, lab_std, skew(color.rgb2lab(lab_image).flatten())
#
#     # Compute the color transform from the lab image to the lake image using color moments
#     a = ((lake_moments[1] / lab_moments[1]) ** 0.5) * (color.rgb2lab(lab_image) - lab_mean) + lake_mean
#     b = (lake_moments[2] / lab_moments[2]) ** 0.5 * a + (lake_moments[0] - lab_moments[0])
#     img_transfer = color.lab2rgb(b)
#
#     # Get the file name from the lab_image_path
#     filename = os.path.basename(labcam_image_path)
#
#     # Save the result as a JPEG image in the output directory
#     output_path = os.path.join(output_directory, filename)
#     os.makedirs(output_directory, exist_ok=True)
#
#     # Convert the image to uint8
#     img_uint8 = skimage.img_as_ubyte(img_transfer)
#
#     # Save the uint8 image
#     imageio.imwrite(output_path, img_uint8)
#
#     return img_transfer


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


def color_transfer_on_image(labcam_image_path, lake_mean, lake_std):
    lab_image = io.imread(labcam_image_path)
    # Calculate the mean and standard deviation of each channel in LAB color space for the input lab image
    lab_mean = color.rgb2lab(lab_image).mean(axis=(0, 1))
    lab_std = color.rgb2lab(lab_image).std(axis=(0, 1))

    # Compute the color transform from the lab image to the lake image
    a = (lake_std / lab_std) * (color.rgb2lab(lab_image) - lab_mean) + lake_mean
    img_transfer = color.lab2rgb(a)

    return img_transfer


def color_transfer_on_image_list(labcam_images_path, lake_mean, lake_std, output_directory):
    # Get lists of image file paths
    labcam_image_list = get_image_list(labcam_images_path)

    # Create the output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    # Iterate over all the LAB images in the input directory
    for lab_image_path in labcam_image_list:
        # Load the LAB image
        lab_image = io.imread(lab_image_path)

        # Calculate the mean and standard deviation of each channel in LAB color space for the input lab image
        lab_mean = color.rgb2lab(lab_image).mean(axis=(0, 1))
        lab_std = color.rgb2lab(lab_image).std(axis=(0, 1))

        # Compute the color transform from the lab image to the lake image
        a = (lake_std / lab_std) * (color.rgb2lab(lab_image) - lab_mean) + lake_mean
        img_transfer = color.lab2rgb(a)

        # Get the file name from the lab_image_path
        filename = os.path.basename(lab_image_path)

        # Save the result as a JPEG image in the output directory
        output_path = os.path.join(output_directory, filename)
        os.makedirs(output_directory, exist_ok=True)

        # Convert the image to uint8
        img_uint8 = skimage.img_as_ubyte(img_transfer)

        # Save the uint8 image
        imageio.imwrite(output_path, img_uint8)

        # io.imsave(output_path, img_transfer, quality=95)

    return
