import json
import tttgui_v1 as ui
import TTTv3 as tracker

def main():

    library = tracker.CentralTrackerLibrary()
    app = ui.TTTGui(library)

    try:
        with open("savefile.json") as file:
            data = json.load(file)
            library.tasks = data["tasks"]
            library.completed = data["completed"]
    except FileNotFoundError:
        pass
        
    app.populate_tasks(library.tasks)

    run = True    
    while run:
     
        app.display()   
        choice = app.get_choice()

        if choice == "1":
            name, desc, parents = app.get_task_info()
            new_task = tracker.Task(name, desc, parents)  
            library.add_task(new_task) 
            app.populate_tasks(library.tasks)

        elif choice == "2":
            name = app.get_selected() 
            task = library.tasks[name]
            if task:
                library.complete_task(task)
            app.set_completed(name)
        
        elif choice == "3":
           # View status code 
            app.display_status(library)

        elif choice == "4":
            app.save_tasks(library.tasks, library.completed)
        
        elif choice == "5":
           # Load code  
            app.populate_tasks(library.tasks)
            
        elif choice == "6":
            # Remove task 
            name = app.get_selected()
            if name in library.tasks:
                del library.tasks[name] 
            app.populate_tasks(library.tasks)
                
        elif choice == "7":
            # Reset  
            library.tasks = {}
            library.completed = [] 
            app.clear_display()
                                 
        run = choice != "Exit"
    
    # Final save
    app.save_tasks(library.tasks, library.completed)
    
if __name__ == "__main__":
    main()