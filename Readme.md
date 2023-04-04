## Color transfer from lake images to lab images

Run script using the following command 

```python
python GUI.py
```
This opens the below GUI.

![GUI color transfer image](/GUI_color_transfer_image.png)


To find the lake color characteristics, you can either input the folder path containing the lake images or provide the saved characteristics from an excel sheet.

The steps are as follows:

1. If you choose the first button:
   1. Load the folder path of the lake images.
   2. Load the path of the lab images that require color transfer.
   3. The excel file with the color characteristics is saved in the current directory, and the transferred lab images are also stored in the same directory.

2. If you choose the second button:
   1. Load the excel file that contains the lake image color characteristics.
   2. Load the path of the lab images that require color transfer.
   3. The transferred lab images are stored in the current directory.


### Note: The standalone GUI script for Linux and Windows OS is under progress.