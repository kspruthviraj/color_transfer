import argparse
from pathlib import Path
from sys import exit

import utils


def run_color_transfer(lake_folder_path: str, lab_folder_path: str, outpath: str) -> None:
    transfer_function = utils.get_lake_color_characteristics_overall(lake_folder_path, lab_folder_path)

    image_paths = utils.get_image_list(lab_folder_path)
    total_images = len(image_paths)
    images_processed = 0

    outpath = Path(outpath)
    outpath.mkdir(parents=True, exist_ok=True)

    for image_path in image_paths:
        utils.color_transfer_on_single_image_overall(image_path, transfer_function, outpath)
        images_processed += 1
        print('Images processed:{} out of {}'.format(images_processed, total_images))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Perform color transfer from lake images to lab images.")
    parser.add_argument("lake_folder_path", type=str, help="Path to the folder containing lake images.")
    parser.add_argument("lab_folder_path", type=str, help="Path to the folder containing lab images.")
    parser.add_argument("outpath", type=str, help="Path to the folder to save the transferred images.")
    args = parser.parse_args()

    run_color_transfer(args.lake_folder_path, args.lab_folder_path, args.outpath)
