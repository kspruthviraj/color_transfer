import os
import pathlib
import random
import sys
import tkinter as tk
import tkinter.filedialog
import tkinter.filedialog
import tkinter.filedialog
from tkinter import messagebox, ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from skimage import io

import utils


class ColorTransferApp:
    """
    A GUI application that performs color transfer from lake images to lab images.
    """

    def __init__(self, master):
        self.frame = None
        self.fig_frame = None
        self.fig = None
        self.canvas = None
        self.master = master
        self.lake_folder_path = None
        self.lake_mean = None
        self.lake_std = None
        self.lab_folder_path = None

        master.geometry('500x300')
        master.title('Perform color transfer')

        # Create a new frame for the buttons and progress bar
        self.frame = tk.Frame(self.master)
        self.frame.grid(row=0, column=0)

        self._create_button('Get color characteristics of lake images and do color transfer to lab images',
                            self._on_upload_lake_images, row=0, column=0)

        self._create_button('Load color characteristics of lake images and do color transfer to lab images',
                            self._on_load_lake_characteristics_from_excel, row=0, column=1)

        self._create_button('Exit', self._on_exit, row=0, column=2)

        # Create a new frame for the figure
        self.fig_frame = tk.Frame(self.master)
        self.fig_frame.grid(row=1, column=0)

    def _on_exit(self):
        self.master.destroy()

    def _create_button(self, text, command, row, column):
        button = tk.Button(self.frame, text=text, wraplength=150, command=command)
        button.grid(row=row, column=column, padx=20, pady=10)

    def plot_figure(self, img1, img2):
        self.fig = Figure(figsize=(5, 2))
        ax1 = self.fig.add_subplot(121)
        ax2 = self.fig.add_subplot(122)
        ax1.imshow(img1)
        ax2.imshow(img2)
        ax1.axis('off')
        ax2.axis('off')
        ax1.set_title('Original Lab Image')
        ax2.set_title('Transferred Lab Image')

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.fig_frame)
        self.canvas.draw()

        self.canvas.get_tk_widget().grid(row=0, column=0)

    def _on_upload_lake_images(self):
        self.lake_folder_path = tkinter.filedialog.askdirectory(
            title='Select main folder of lake images to get the color characteristics')
        self.lake_mean, self.lake_std = utils.get_lake_color_characteristics(self.lake_folder_path)

        self.lab_folder_path = tkinter.filedialog.askdirectory(
            title='Select main folder of lab images for doing color transfer')

        image_paths = utils.get_image_list(self.lab_folder_path)
        total_images = len(image_paths)
        images_processed = 0

        if total_images >= 2:
            pb = ttk.Progressbar(self.frame, orient='horizontal', mode='determinate', length=200)
            pb.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
            pb.start()

            for image_path in image_paths:
                new_folder_path = pathlib.Path.cwd() / 'lab_color_transfered_out'
                new_folder_path.mkdir(exist_ok=True)

                utils.color_transfer_on_single_image(image_path, self.lake_mean, self.lake_std,
                                                     new_folder_path)

                images_processed += 1
                pb['value'] = (images_processed / total_images) * 100
                self.master.update()

            pb.stop()
            pb.destroy()

            # # Display message box to indicate the operation is complete
            # messagebox.showinfo("Operation Complete", "The operation is complete.")
        else:
            # Display error message box if there are not enough images in the folder
            messagebox.showerror("Error", "There are not enough images in the folder.")

        random_filename = random.sample(image_paths, 1)
        original_lab_image = io.imread(random_filename[0])
        transferred_lab_image = utils.color_transfer_on_image(random_filename[0], self.lake_mean, self.lake_std)
        self.plot_figure(original_lab_image, transferred_lab_image)

    def _on_load_lake_characteristics_from_excel(self):
        self.excel_file_path = tkinter.filedialog.askopenfilename(
            title='Select the excel sheet containing lake image characteristics',
            filetypes=(('Excel files', '*.xlsx'), ('All files', '*.*')))
        self.lake_mean, self.lake_std = utils.load_lake_color_characteristics(self.excel_file_path)

        self.lab_folder_path = tkinter.filedialog.askdirectory(
            title='Select main folder of lab images for doing color transfer')

        image_paths = utils.get_image_list(self.lab_folder_path)
        total_images = len(image_paths)
        images_processed = 0

        if total_images >= 2:
            pb = ttk.Progressbar(self.frame, orient='horizontal', mode='determinate', length=200)
            pb.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
            pb.start()

            for image_path in image_paths:
                new_folder_path = pathlib.Path.cwd() / 'lab_color_transfered_out'
                new_folder_path.mkdir(exist_ok=True)

                utils.color_transfer_on_single_image(image_path, self.lake_mean, self.lake_std,
                                                     new_folder_path)

                images_processed += 1
                pb['value'] = (images_processed / total_images) * 100
                self.master.update()

            pb.stop()
            pb.destroy()

            # # Display message box to indicate the operation is complete
            # messagebox.showinfo("Operation Complete", "The operation is complete.")
        else:
            # Display error message box if there are not enough images in the folder
            messagebox.showerror("Error", "There are not enough images in the folder.")

        random_filename = random.sample(image_paths, 1)
        original_lab_image = io.imread(random_filename[0])
        transferred_lab_image = utils.color_transfer_on_image(random_filename[0], self.lake_mean, self.lake_std)
        self.plot_figure(original_lab_image, transferred_lab_image)


def main():
    root = tk.Tk()
    ColorTransferApp(root)
    root.mainloop()


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
