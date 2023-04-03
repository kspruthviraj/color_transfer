import tkinter as tk
import tkinter.filedialog
import pathlib
import sys
import utils
import os
import tkinter.messagebox as messagebox


class ColorTransferApp:
    """
    A GUI application that performs color transfer from lake images to lab images.
    """

    def __init__(self, master):
        self.master = master
        self.lake_folder_path = None
        self.lake_mean = None
        self.lake_std = None
        self.lab_folder_path = None

        master.geometry('450x300')
        master.title('Compare model performances with GT')

        self._create_button('Get color characteristics of lake images and do color transfer to lab images',
                            self._on_upload_lake_images)

        self._create_button('Load color characteristics of lake images and do color transfer to lab images',
                            self._on_load_lake_characteristics_from_excel)

        self._create_button('Exit', self._on_exit)

    def _on_exit(self):
        self.master.destroy()

    def _create_button(self, text, command):
        button = tk.Button(text=text, wraplength=150, command=command)
        button.pack(side=tk.LEFT, padx=20, pady=100)

    def _on_upload_lake_images(self):
        self.lake_folder_path = tkinter.filedialog.askdirectory(
            title='Select main folder of lake images to get the color characteristics')
        self.lake_mean, self.lake_std = utils.get_lake_color_characteristics(self.lake_folder_path)

        self.lab_folder_path = tkinter.filedialog.askdirectory(
            title='Select main folder of lab images for doing color transfer')

        new_folder_path = pathlib.Path.cwd() / 'lab_color_transfered_out'
        new_folder_path.mkdir(exist_ok=True)

        utils.color_transfer_on_image_list(self.lab_folder_path, self.lake_mean, self.lake_std, new_folder_path)

        # Display message box to indicate the operation is complete
        messagebox.showinfo("Operation Complete", "The operation is complete.")

    def _on_load_lake_characteristics_from_excel(self):
        self.excel_file_path = tkinter.filedialog.askopenfilename(
            title='Select the excel sheet containing lake image characteristics',
            filetypes=(('Excel files', '*.xlsx'), ('All files', '*.*')))
        self.lake_mean, self.lake_std = utils.load_lake_color_characteristics(self.excel_file_path)

        self.lab_folder_path = tkinter.filedialog.askdirectory(
            title='Select main folder of lab images for doing color transfer')

        utils.color_transfer_on_image_list(self.lab_folder_path, self.lake_mean, self.lake_std, None)

        # Display message box to indicate the operation is complete
        messagebox.showinfo("Operation Complete", "The operation is complete.")


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
