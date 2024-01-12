import json
from abc import ABC, abstractmethod

class TaskManager(ABC):

    @abstractmethod
    def add_task(self):
        pass

    @abstractmethod    
    def complete_task(self):
        pass

class Task:
    def __init__(self, name: str, description: str, parent_tasks: list[str] = None) -> None:
        self.name = name
        self.description = description
        self.completed = False
        self.parent_tasks = parent_tasks if parent_tasks else []

    def can_complete(self, library: 'CentralTrackerLibrary') -> bool:
        # Validate parent tasks 
        for parent in self.parent_tasks:
            if parent not in library.tasks or not library.tasks[parent].completed:
                print(f"Parent Task {parent} is not complete")
                return False
        return True

class CentralTrackerLibrary(TaskManager):
    def __init__(self):
        self.tasks: dict[str, Task] = {}
        self.completed_tasks: list[str] = []
        
    def add_task(self, task: Task) -> None:
        # Validate parent tasks
        if all(parent in self.tasks for parent in task.parent_tasks):
            self.tasks[task.name] = task
        else:
            print("Error: Missing parent task")

    def complete_task(self, task: Task) -> None:
        if task.can_complete(self): 
            task.completed = True
            self.completed_tasks.append(task.name)
    
    def print_status(self):
        print("Completed Tasks:")
        print(self.completed_tasks)
            
        print("Remaining Tasks:")
        for name, task in self.tasks.items():
            if not task.completed:
                print(name)
                
class UI:
    def __init__(self, library: CentralTrackerLibrary):
        self.library = library

    def show_menu(self):
        print("""  
        1. Add New Task
        2. Complete Task
        3. View Status 
        4. Save Game
        5. Load Game
        6. Exit""")
            
    def add_task(self):
        name = input("Enter task name: ")
        desc = input("Enter description: ")
        parents = []
            
        add_more = True
        while add_more:
            parent = input("Enter parent task (leave blank if none): ")
            if parent:
                parents.append(parent) 
            else:
                add_more = False
                
        task = Task(name, desc, parents)
        self.library.add_task(task)
        print(f"Task {name} was added.")
    
    def print_status(self):
        print("Completed Tasks:")
        print(self.library.completed_tasks)
            
        print("Remaining Tasks:")
        for name, task in self.library.tasks.items():
            if not task.completed:
                print(name)
        
def save_library(library: CentralTrackerLibrary, file):
    data = library.__dict__
    json.dump(data, file)
       
def load_library(file):
    data = json.load(file)
    library = CentralTrackerLibrary()
    library.__dict__ = data
    return library
        
if __name__ == "__main__":

    library = CentralTrackerLibrary()
    ui = UI(library)

    # Load previous save if exists
    try:
        with open("savefile.json", "r") as f:
            library = load_library(f)
    except FileNotFoundError:
        pass

    
    run = True
    while run:
        ui.show_menu()
            
        choice = input("Enter choice: ")
            
        if choice == "1":
            ui.add_task()
                
        elif choice == "2":
            name = input("Enter task name to complete: ")
            task = library.tasks.get(name)
            if task:
                library.complete_task(task)
            else:
                print("Task not found!")
                
        elif choice == "3": 
            ui.print_status()
                
        elif choice == "4":
            with open("savefile.json", "w") as f:
                save_library(library, f)  
            print("Game saved.")
                
        elif choice == "5":
            with open("savefile.json", "r") as f:
                library = load_library(f)
            print("Game loaded.")
               
        elif choice == "6":
            run = False
    
    # Final save   
    with open("savefile.json", "w") as f:
        save_library(library, f)