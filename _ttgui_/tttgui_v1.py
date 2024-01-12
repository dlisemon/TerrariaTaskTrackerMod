import tkinter as tk
from tkinter import ttk
from TTTv3 import Task, CentralTrackerLibrary

class TTTGui:
    def __init__(self, library):
        self.library = library
        self.root = tk.Tk()
        self.init_gui()
        
    def init_gui(self):
        self.root.title('Terraria Task Tracker')
        self.create_menu()
        self.create_left_pane() 
        self.create_right_pane()
        self.create_status_bar()
        
    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        
        file_menu = tk.Menu(menu_bar, tearoff=0) 
        file_menu.add_command(label="Save", command=self.handle_save)
        file_menu.add_command(label="Load", command=self.handle_load)
        menu_bar.add_cascade(label="File", menu=file_menu)
        
        tk.Tk.config(self.root, menu=menu_bar)
        
    def create_left_pane(self): 
        frame = tk.Frame(self.root)
        scrollbar = ttk.Scrollbar(frame) 
        self.task_tree = ttk.Treeview(frame, yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.task_tree.yview)
        # Add tree view contents  
        self.task_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True) 
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        frame.pack(fill=tk.BOTH, expand=True)
        
    def create_right_pane(self):
        nb = ttk.Notebook(self.root) 
        self.detail_tab = ttk.Frame(nb)
        self.logs_tab = ttk.Frame(nb)          
        nb.add(self.detail_tab, text='Task Details') 
        nb.add(self.logs_tab, text='History    ') 
        nb.pack(expand=True, fill='both')
        
    def create_status_bar(self):
        status = tk.StringVar()
        status_bar = tk.Label(self.root, textvariable=status, bd=1, relief=tk.SUNKEN, anchor=tk.W) 
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def update_status(self, msg):
        pass # Set status bar message
        
    def handle_save(self):
        data = {
            "tasks": self.library.tasks,
            "completed": self.library.completed_tasks
        }
        with open("savefile.json", "w") as f:
            json.dump(data, f)
        self.update_status("Game saved successfully!")
            
    def handle_load(self):
        try:
            with open("savefile.json") as f:
                data = json.load(f)
                self.library.tasks = data["tasks"] 
                self.library.completed_tasks = data["completed"]
            self.update_status("Loaded save file!")
        except FileNotFoundError:
            self.update_status("No save file found.")
        self.populate_task_tree()
            
    def populate_task_tree(self):
        for task in self.library.tasks:
            if task.parent_tasks:
                self.task_tree.insert(parent="", index="end", iid=task.name, text=task.name)  
            else:
                self.task_tree.insert("", "end", task.name, text=task.name) 
                
        for name in self.library.completed_tasks:
            self.task_tree.item(name, tags=["completed"])
            
    def handle_button_click(self, name):
        task = self.library.tasks.get(name) 
        if task:
            # Mark complete
            self.library.complete_task(task)  
            self.task_tree.item(name, tags=["completed"])
            msg = f"Completed task {name}"
        else:
            msg = f"No task named {name}"
        
        self.update_status(msg)
    
    def create_right_pane(self):
        
        # Notebook and tabs  
        nb = ttk.Notebook(self.root)
        
        # Details 
        details_frame = ttk.Frame(nb)
        self.detail_name = ttk.Label(details_frame) 
        self.detail_desc = ttk.Text(details_frame)
        self.detail_prereq = ttk.Label(details_frame) 
        
        self.detail_name.grid(row=0, column=0)
        self.detail_desc.grid(row=1, column=0) 
        self.detail_prereq.grid(row=2, column=0)
        
        nb.add(details_frame, text="Task Details")
        
        # Logs tab
        # ...
        
        nb.pack(fill=tk.BOTH)  
        
        
    def handle_tree_select(self, event):
        selected_id = self.task_tree.selection()[0] 
        task = self.library.tasks[selected_id]
        
        self.detail_name.config(text=task.name)
        self.detail_desc.insert(tk.END, task.description)
        prereqs = "\n".join(task.parent_tasks)
        self.detail_prereq.config(text=prereqs)
		
    
    def populate_task_tree(self):
		# Populate treeview  
        # Set event binding
        self.task_tree.bind('<<TreeviewSelect>>', self.handle_tree_select)