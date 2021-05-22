import tkinter as tk
import tkinter.filedialog as fd
import webbrowser
from documentor import Documentor


class Application:
    def __init__(self) -> None:
        self._root = tk.Tk()
        self._root.title('Documentor')

        self._width = 500
        self._height = 750

        self._root.geometry(f'{self._width}x{self._height}')

        self._files_path = ()
        self._saving_directory = ""
        self._path_label = None
        self._more_paths_button = None

    def _file_explorer(self):
        self._files_path = fd.askopenfilenames(title='Choose a file')
        if not self._files_path:
            return
        if self._path_label:
            self._path_label.config(text='')
        if self._more_paths_button:
            self._more_paths_button.destroy()
        height = 350
        self._directory_button.destroy()
        for i in range(len(self._files_path)):
            if i < 2:
                self._path_label = tk.Label(text=f'{i + 1}. {self._files_path[i].split("/")[-1]}')
                self._path_label.place(x=self._width // 2, y=height, anchor='center')
                height += 25
            else: 
                height += 5
                break
        if len(self._files_path) > 2:
            self._more_paths_button = tk.Button(text='More', command=self._show_paths)
            self._more_paths_button.place(x=self._width // 2, y=height, anchor='center', height=20)
            height += 10
            

        self._directory_button = tk.Button(text="Choose Saving Directory", width=22, height=1, background='black', foreground='white', font=('Arial', 12), command=self._directory_explorer)
        self._directory_button.place(x=self._width // 2, y=height + 30, anchor='center') 

    def _show_paths(self):
        paths_window = tk.Tk()
        paths_window.title = 'Paths'
        for i in range(len(self._files_path)):
            l = tk.Label(paths_window, text=f'{i + 1}. {self._files_path[i].split("/")[-1]}') 
            l.pack()

    def _directory_explorer(self):
        self._saving_directory = fd.askdirectory()

        l = tk.Label(text=self._saving_directory)
        l.place(x=self._width // 2, y=self._directory_button.winfo_y() + 60, anchor='center')

    def _generate(self):
        error_window = tk.Tk()
        error_window.title('ERROR')

        title = self._title_entry.get()
        source_url = self._source_entry.get()

        if not title:
            label = tk.Label(error_window, text="You forgot the title!", font=('Arial', 20), background='red')
            label.pack()
            return
        elif not source_url:
            label = tk.Label(error_window, text="You forgot the source code url!", font=('Arial', 20), background='red')
            label.pack()
            return 
        elif not self._files_path:
            label = tk.Label(error_window, text="You forgot the files", font=('Arial', 20), background='red')
            label.pack()
            return
        else:
            error_window.destroy()
            docs = Documentor(self._saving_directory, self._files_path, title, source_url)
            docs.create()
            webbrowser.open(f'{self._saving_directory}/{title}.html')

    def start(self):
        window_title = tk.Label(text='Documentor', font=('Arial', 50))
        window_title.place(x=self._width // 2, y=70, anchor='center')

        title_label = tk.Label(text="Title:", font=('Arial', 14))
        self._title_entry = tk.Entry(bg="#d1d1d1", width=20, font=('Arial', 14))
        title_label.place(x=20, y=150)
        self._title_entry.place(x=90, y=150)

        source_label = tk.Label(text="Source Code URL:", font=('Arial', 16))
        self._source_entry = tk.Entry(bg="#d1d1d1", width=20, font=('Arial', 16))
        source_label.place(x=20, y=220)
        self._source_entry.place(x=220, y=220)

        files_button = tk.Button(text="Choose Files", width=15, height=1, background='black', foreground='white', font=('Arial', 12), command=self._file_explorer)
        files_button.place(x=self._width // 2, y=310, anchor='center') 

        self._directory_button = tk.Button(text="Choose Saving Directory", width=22, height=1, background='black', foreground='white', font=('Arial', 12), command=self._directory_explorer)
        self._directory_button.place(x=self._width // 2, y=390, anchor='center') 

        button = tk.Button(text="Generate Docs", width=15, height=2, bg="green", fg="white", font=('Arial', 20), command=self._generate)
        button.place(x=self._width // 2, y=self._height - 130, anchor='center')

        self._root.mainloop()


if __name__ == '__main__':
    app = Application()
    app.start()