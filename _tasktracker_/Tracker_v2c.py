import json

class Task:
    def __init__(self, name, description, prerequisites=None):
        self.name = name
        self.description = description 
        self.completed = False
        self.prerequisites = prerequisites if prerequisites else []

    def can_complete(self):
        # Validate prerequisites
        for prereq in self.prerequisites:  
            if prereq not in playthrough.tasks or not playthrough.tasks[prereq].completed:
                print(f"Prerequisite {prereq} not complete.")
                return False
        return True

class CentralTrackerLibrary:
    def __init__(self):
        self.tasks = {}
        self.completed_tasks = []
    
    def add_task(self, task):
       # Validate prerequisites
       if all(prereq in self.tasks for prereq in task.prerequisites):
           self.tasks[task.name] = task
       else:
           print("Error: Missing prerequisite")
           
    def complete_task(self, task):
        if task.can_complete():
            task.completed = True  
            self.completed_tasks.append(task.name)
            
class UI:
    def __init__(self, playthrough):
        self.playthrough = playthrough

    def show_menu(self):
        print("""
        1. Add new task
        2. Complete task
        3. View playthrough
        4. Save playthrough
        5. Load playthrough
        6. Exit
        """)
    
    def add_task(self):
        name = input("Enter task name: ")
        desc = input("Enter description: ")
        prerequisites = []
        
        add_more = True
        while add_more:
            prereq = input("Enter prerequisite (leave blank if none): ")
            if prereq:
                prerequisites.append(prereq)
            else:
                add_more = False
                
        task = Task(name, desc, prerequisites)
        self.library.add_task(task)
        print(f"Task {name} was added.")
    
    def show_status(self):
        print("Completed tasks:")
        print(library.completed_tasks)
        
        print("Remaining tasks:")
        for name, task in library.tasks.items():
            if not task.completed:
                print(name)
                
def save_library(library, file):
   json.dump(library.__dict__, file)
   
def load_library(file):
    data = json.load(file)
    library = CentralTrackerLibrary() 
    library.__dict__ = data
    return library
            
def main():
    
    library = CentralTrackerLibrary() 
    ui = UI(library)

    # Load previous save if exists
    try:
        with open("savefile.json", "r") as f:
            playthrough = load_library(f)
    except FileNotFoundError:
        playthrough = CentralTrackerLibrary()
        
    
    run = True
    while run:
        
        ui.show_menu()
        
        choice = input("Enter choice: ")
        
        if choice == "1": 
            ui.add_task()
            
        elif choice == "2":
            name = input("Enter task name to complete: ")
            task = playthrough.tasks.get(name)
            if task:
                playthrough.complete_task(task) 
            else:
                print("Task not found!")
                
        elif choice == "3":
            ui.show_status()
            
        elif choice == "4":
            with open("savefile.json", "w") as f:
                save_library(playthrough, f)  
            print("Game saved.")
            
        elif choice == "5": 
            with open("savefile.json", "r") as f:
                playthrough = load_library(f)
            print("Game loaded.")
               
        elif choice == "6":  
            run = False
            
    # Final save  
    with open("savefile.json", "w") as f:
        save_library(library, f) 
        
if __name__ == "__main__":
    main()
    
main()