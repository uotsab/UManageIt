from tkinter import *
from tkinter import messagebox
import tkinter as tk
import struct_task
import pickle
import datetime
import tkinter.filedialog as browsediag
import os

#### Functions ####

# About window
def window_info_about():
    messagebox.showinfo("About", "Open Source task manager made by Uotsab Chakma (of Uju Studio) in 2026.")

# Makes new project file:
def create_new_file():
    global working_file_path
    working_file_path = browsediag.asksaveasfile(parent=root, defaultextension='.data', initialdir="projects/*.data", title='Save file', filetypes=[('Datatype', '*.data')])
    load_task_data()
    refresh_tasks()

# Asks by menu strip to open project
def menu_ask_open_project():
    last_projects[0] = ask_open_project()
    save_projects_data()
    load_task_data()
    refresh_tasks()

# Asks to open a project
def ask_open_project():
    global working_file_path
    working_file_path = browsediag.askopenfilename(parent=root, initialdir="projects/", title='Select a file', filetypes=[('Datatype', '*.data')])
    return working_file_path

# Update the scrollregion whenever the frame's size changes
def on_frame_configure(event):
    tasks_canvas.configure(scrollregion=tasks_canvas.bbox("all"))

# Make the inner window width match the canvas width (optional, keeps layout tidy)
def on_canvas_configure(event):
    tasks_canvas.itemconfig(canvas_window, width=event.width)

# Mouse wheel scrolling on Windows
def on_mousewheel(event):
    tasks_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

# Adds a new task
def add_task():
    new_task = struct_task.struct_task()
    new_task.title = task_title.get()
    new_task.assigndate = datetime.datetime.now()
    tasks.append(new_task)
    save_task_data()
    refresh_tasks()

def add_task_by_entry(event):
    add_task()

# Loads tasks list from file safely
def load_task_data():
    global working_file_path, tasks
    tasks = []
    if not working_file_path:
        return
    if not os.path.exists(working_file_path):
        return
    try:
        with open(working_file_path, "rb") as fp:
            data = pickle.load(fp)
            if isinstance(data, list):
                tasks = data
            else:
                messagebox.showerror("Error", "File probably is corrupted!")
                tasks = []
    except (FileNotFoundError, EOFError, pickle.UnpicklingError):
        save_task_data()
        tasks = []

# Saves tasks list to file safely
def save_task_data():
    global working_file_path
    if not working_file_path:
        # no project selected
        return
    try:
        os.makedirs(os.path.dirname(working_file_path), exist_ok=True)
        with open(working_file_path, "wb") as fp:
            pickle.dump(tasks, fp)
    except OSError:
        messagebox.showerror("Error", "OS Error")
        pass

# Loads projects list safely
def load_projects_data():
    global last_projects
    last_projects = []
    if not os.path.exists(projects_list_file_name):
        return
    try:
        with open(projects_list_file_name, "rb") as fp:
            data = pickle.load(fp)
            if isinstance(data, list):
                last_projects = data
            elif isinstance(data, str):
                last_projects = [data]
            else:
                last_projects = []
    except (FileNotFoundError, EOFError, pickle.UnpicklingError):
        last_projects = []

# Saves projects list safely
def save_projects_data():
    try:
        os.makedirs(os.path.dirname(projects_list_file_name), exist_ok=True)
        with open(projects_list_file_name, "wb") as fp:
            pickle.dump(last_projects, fp)
    except OSError:
        messagebox.showerror("Error", "OS Error")
        pass

# Get's each task items:
def refresh_tasks():
    root.title(working_file_path + " - UManageIt")
    for widget in tasks_frame.winfo_children():
        widget.destroy()
    index = 0
    for task in tasks:
        backcolortype :str = selectedcolor
        row = index + 1
        if getattr(task, "done", False):
            backcolortype = deselectedcolor
            text_done = tk.Label(tasks_frame, text="Done in " + str(getattr(task, "donedate", ""))[:10], bg=backcolortype)
            text_done.grid(row=row, column=0, padx=10, pady=1, sticky='w')
        else:
            backcolortype = selectedcolor
            done_button = tk.Button(tasks_frame, text="Done!", command=lambda t=task: mark_task_as_done(t), bg=backcolortype)
            done_button.grid(row=row, column=0, padx=10, pady=1, sticky='w')
        text_title = tk.Label(tasks_frame, text=str(getattr(task, "title", "")))
        text_title.grid(row=row, column=1, padx=10, pady=1, sticky='w')
        text_date = tk.Label(tasks_frame, text=str(getattr(task, "assigndate", ""))[:10])
        text_date.grid(row=row, column=2, padx=10, pady=1, sticky='w')
        delete_button = tk.Button(tasks_frame, text="×", command=lambda t=task: delete_task(t))
        delete_button.grid(row=row, column=3, padx=10, pady=1, sticky='w')
        index += 1

def mark_task_as_done(task: struct_task.struct_task):
    task.done = True
    task.donedate = datetime.datetime.now()
    save_task_data()
    refresh_tasks()

def delete_task(task: struct_task.struct_task):
    if task in tasks:
        tasks.remove(task)
        save_task_data()
        refresh_tasks()


#### Root ####
root = tk.Tk()

#### VARIABLES #####
tasks: list[struct_task.struct_task] = []
last_projects: list[str] = []

projects_list_file_name: str = "data/projects_list.data"
working_file_path: str = ""

backcolor = '#350785'
forecolor = '#DDCDFA'
selectedcolor = '#F5E79F'
deselectedcolor = '#7A703B'

icn = PhotoImage(file='icon.png')

load_projects_data()
if len(last_projects) < 1:
    working_file_path = ask_open_project()
    if working_file_path:
        last_projects.append(working_file_path)
        save_projects_data()
else:
    working_file_path = last_projects[0]
task_title = tk.StringVar()

## Window Setup ##
root.configure(bg=backcolor)
root.minsize(400, 400)
root.geometry("600x500")
root.iconphoto(False, icn)

## Menubar ##
menubar = Menu(root)

# Adding File Menu and commands
menufile = Menu(menubar, tearoff = 0)
menubar.add_cascade(label ='Options', menu = menufile)
menufile.add_command(label ='Open...', command = menu_ask_open_project)
menufile.add_command(label ='New File', command = create_new_file)
menufile.add_command(label ='About', command = window_info_about)

tasks_canvas = Canvas(root, width=100, height=300)
tools_canvas = Canvas(root, width=100, height=100)

## Creating scroll bar ##
scrollbar = Scrollbar(root, orient=VERTICAL, command=tasks_canvas.yview)
scrollbar.pack(side=RIGHT, fill=Y)

tasks_canvas.config(yscrollcommand=scrollbar.set)
tasks_canvas.pack(side=BOTTOM, fill=BOTH, expand=True)

## Creating a Frame of tasks_canvas ##
tasks_frame = Frame(tasks_canvas)
canvas_window = tasks_canvas.create_window((0, 0), window=tasks_frame, anchor='nw')

## Creating Frame for tools ##
tools_canvas.pack(side=TOP, fill=X, expand=False)
text_box_title = Entry(tools_canvas, textvariable=task_title, width = 5)
text_box_title.pack(side=LEFT, fill=X, expand=TRUE)
add_button = Button(tools_canvas, text="+", command=add_task)
add_button.pack(side=RIGHT, expand=FALSE)

#### LOGIC ####

load_task_data()

refresh_tasks()

tasks_frame.bind("<Configure>", on_frame_configure)
tasks_canvas.bind("<Configure>", on_canvas_configure)
text_box_title.bind("<Return>", add_task_by_entry)
root.bind_all("<MouseWheel>", on_mousewheel)

root.config(menu = menubar)

# Needs to force focus, otherwise it won't focus if selected file as working file by askopenfilename() function.
text_box_title.focus_force()

# tkinter heart loop:
root.mainloop()