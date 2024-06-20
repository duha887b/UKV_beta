import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import plotly.io as pio
import webbrowser
import os
from multiprocessing import Process
from gcode_parser import read_gcode, extract_coordinates
from csv_parser import read_csv, parse_csv_data
from plotter import plot_2d, plot_3d, plot_time
from synchronizer import synchronize_data

# Install pywin32 before running this script
# pip install pywin32
import win32gui  # For getting the desktop window handle


class ModernApp:
    def __init__(self, root):
        self.root = root
        self.root.title("UKV")

        self.style = ttk.Style()
        self.style.configure('TLabel', font=('Helvetica', 12))
        self.style.configure('TButton', font=('Helvetica', 12))
        self.style.configure('TRadiobutton', font=('Helvetica', 12))
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TEntry', font=('Helvetica', 12), padding=5)
        self.style.configure('TCheckbutton', font=('Helvetica', 12))

        self.root.configure(bg='#f0f0f0')

        # Variables
        self.gcode_file_path = None
        self.csv_file_path = None
        self.plot_mode = tk.StringVar()
        self.plot_mode.set("2D")
        self.num_points = tk.StringVar(value="100")
        self.open_in_browser = tk.BooleanVar(value=False)

        # Main Frame
        menu_width = 30  # Width of the menu entries
        main_frame = ttk.Frame(root, padding="10 10 10 10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.pack_propagate(False)

        # Layout for file selection
        ttk.Label(main_frame, text="G-Code:").grid(row=0, column=0, sticky="e")
        self.gcode_entry = ttk.Entry(main_frame, width=menu_width)
        self.gcode_entry.grid(row=0, column=1, padx=10, pady=5)
        ttk.Button(main_frame, text="Datei", command=self.load_gcode).grid(row=0, column=2, pady=5)

        ttk.Label(main_frame, text="CSV:").grid(row=1, column=0, sticky="e")
        self.csv_entry = ttk.Entry(main_frame, width=menu_width)
        self.csv_entry.grid(row=1, column=1, padx=10, pady=5)
        ttk.Button(main_frame, text="Datei", command=self.load_csv).grid(row=1, column=2, pady=5)

        ttk.Label(main_frame, text="Plot Modus", font=('Helvetica', 14)).grid(row=2, column=0, columnspan=3, pady=10)
        ttk.Radiobutton(main_frame, text="G-Code Plot 2D", variable=self.plot_mode, value="2D").grid(row=3, column=1,
                                                                                                     sticky="w",
                                                                                                     padx=20)
        ttk.Radiobutton(main_frame, text="G-Code Plot 3D", variable=self.plot_mode, value="3D").grid(row=4, column=1,
                                                                                                     sticky="w",
                                                                                                     padx=20)
        ttk.Radiobutton(main_frame, text="Time Plot", variable=self.plot_mode, value="Time").grid(row=5, column=1,
                                                                                                  sticky="w", padx=20)

        ttk.Label(main_frame, text="Anzahl der Punkte:").grid(row=6, column=0, sticky="e")
        self.num_points_entry = ttk.Entry(main_frame, textvariable=self.num_points, width=menu_width)
        self.num_points_entry.grid(row=6, column=1, padx=10, pady=5)

        self.browser_checkbutton = ttk.Checkbutton(main_frame, text="Im Browser öffnen", variable=self.open_in_browser)
        self.browser_checkbutton.grid(row=7, column=1, sticky="w", padx=20, pady=5)

        ttk.Button(main_frame, text="Generate Plot", command=self.generate_plot).grid(row=8, column=0, columnspan=3,
                                                                                      pady=20)

        self.browser_process = None

        # Get the screen width and height
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        # Calculate the position of the Tkinter window
        self.window_width = 500  # Set the window width to fit the menu (300 + 200)
        self.window_height = 400  # Set the window height to fit the menu
        self.root.geometry(f"{self.window_width}x{self.window_height}+0+0")

    def load_gcode(self):
        self.gcode_file_path = filedialog.askopenfilename(title="Wählen Sie die G-Code-Datei",
                                                          filetypes=[("G-Code Dateien", "*.gcode"),
                                                                     ("Alle Dateien", "*.*")])
        self.gcode_entry.delete(0, tk.END)
        self.gcode_entry.insert(0, self.gcode_file_path)

    def load_csv(self):
        self.csv_file_path = filedialog.askopenfilename(title="Wählen Sie die CSV-Datei",
                                                        filetypes=[("CSV Dateien", "*.csv"), ("Alle Dateien", "*.*")])
        self.csv_entry.delete(0, tk.END)
        self.csv_entry.insert(0, self.csv_file_path)

    def generate_plot(self):
        if not self.gcode_file_path or not self.csv_file_path:
            messagebox.showerror("Fehler", "Bitte wählen Sie beide Dateien aus.")
            return

        try:
            num_points = int(self.num_points.get())
        except ValueError:
            messagebox.showerror("Fehler", "Bitte geben Sie eine gültige Anzahl von Punkten ein.")
            return

        gcode_lines = read_gcode(self.gcode_file_path)
        x_coords, y_coords = extract_coordinates(gcode_lines)

        csv_lines = read_csv(self.csv_file_path)
        header, csv_data = parse_csv_data(csv_lines)

        first_index = int(header['First index'])
        sampling_cycle = int(header['Sampling cycle'].replace('us', ''))

        synchronized_data = synchronize_data(x_coords, y_coords, csv_data, first_index, sampling_cycle, num_points)

        plot_type = self.plot_mode.get()
        if plot_type == "2D":
            fig = plot_2d(x_coords, y_coords, synchronized_data, num_points)
        elif plot_type == "3D":
            fig = plot_3d(x_coords, y_coords, synchronized_data, num_points)
        elif plot_type == "Time":
            fig = plot_time(csv_data, sampling_cycle, first_index, num_points)

        if fig:
            html = pio.to_html(fig, full_html=False)
            with open("plot.html", "w", encoding="utf-8") as f:
                f.write(html)
            if self.open_in_browser.get():
                webbrowser.open("plot.html")
            else:
                if self.browser_process and self.browser_process.is_alive():
                    self.browser_process.terminate()
                self.browser_process = Process(target=start_cef_process, args=(
                "file://" + os.path.abspath("plot.html"), self.window_width, 0, self.window_width, self.window_height))
                self.browser_process.start()


def start_cef_process(url, x, y, width, height):
    from cefpython3 import cefpython as cef
    import sys
    import win32gui
    sys.excepthook = cef.ExceptHook
    window_info = cef.WindowInfo()
    parent_handle = win32gui.GetDesktopWindow()  # Get the handle to the desktop window
    window_info.SetAsPopup(parent_handle, "Plot")
    cef.Initialize()
    browser = cef.CreateBrowserSync(window_info=window_info, url=url)
    browser.SetBounds(x, y, width, height)
    cef.MessageLoop()
    cef.Shutdown()


if __name__ == "__main__":
    root = tk.Tk()
    app = ModernApp(root)
    root.mainloop()
    if app.browser_process and app.browser_process.is_alive():
        app.browser_process.terminate()



