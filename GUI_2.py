import logging
import os
import sys
import threading
import time
import tkinter.scrolledtext as ScrolledText
from tkinter import *
from tkinter import filedialog
import pandas as pd

import utils as util


class ReadFileApp:
    def __init__(self, master):
        # Initialize tkinter window with dimensions 300 x 300
        self.excel_file_name = None
        self.labfoldername = None
        self.lake_mean = None
        self.lake_std = None
        self.lakefoldername = None
        self.file_path = None
        self.predicted_df = None
        self.foldername = None
        self.GT_renamed_df = None
        self.filename = None
        master.geometry('400x300')

        master.title('Compare model performances with GT')

        button = Button(master, wraplength=100, text='Get color characteristics of lake images and do color transfer '
                                                     'to lab images ', command=self.UploadLakeimages)
        # Set the position of button to coordinate (100, 20)
        button.pack(side=LEFT, padx=20, pady=100)

        button = Button(master, wraplength=100, text='Load color characteristics of lake images and do color transfer '
                                                     'to lab images ', command=self.UploadLakeExcel)
        # Set the position of button to coordinate (100, 20)
        button.pack(side=LEFT, padx=10, pady=100)

    def UploadLakeimages(self):
        self.lakefoldername = filedialog.askdirectory(title="Select main folder of lake images to get the color "
                                                            "characteristics")
        self.lake_mean, self.lake_std = util.get_lake_color_characteristics(self.lakefoldername)
        self.labfoldername = filedialog.askdirectory(title="Select main folder of lab images for doing color transfer")
        util.color_transfer_on_image_list(self.labfoldername, self.lake_mean, self.lake_std, None)

        # self.GT_renamed_df = util.read_excel_filename(self.filename)

    def UploadLakeExcel(self):
        self.excel_file_name = filedialog.askopenfilename(title="Select the excel sheet  containing lake image "
                                                                "characteristics",
                                                          filetypes=(("xlxs files", ".*xlsx"),
                                                                     ("All Files", "*.")))
        self.lake_mean, self.lake_std = util.load_lake_color_characteristics(self.excel_file_name)
        self.labfoldername = filedialog.askdirectory(title="Select main folder of lab images for doing color transfer")
        util.color_transfer_on_image_list(self.labfoldername, self.lake_mean, self.lake_std, None)
        #
        # print('Selected:', self.filename)
        # print('Selected:', self.foldername)

    # def gen_report_function(self):
    #     print('')
    #     # util.perform_statistics(self.file_path, self.foldername, self.GT_renamed_df, self.predicted_df)
    #


def worker():
    # Skeleton worker function, runs in separate thread (see below)
    while True:
        # Report time / date at 2-second intervals
        time.sleep(2)
        timeStr = time.asctime()
        msg = 'Current time: ' + timeStr
        logging.info(msg)


def main():
    main = Tk()
    ReadFileApp(main)
    t1 = threading.Thread(target=worker, args=[])
    t1.start()
    main.mainloop()


if __name__ == "__main__":
    if getattr(sys, 'frozen', False):
        # If the application is run as a bundle, use the bundle directory as the working directory
        bundle_dir = sys._MEIPASS
    else:
        # If the application is run as a script, use the script directory as the working directory
        bundle_dir = os.path.dirname(os.path.abspath(__file__))

    # Add the bundle directory to the system path
    sys.path.append(bundle_dir)

    main()
