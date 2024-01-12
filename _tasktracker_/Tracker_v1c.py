### Incomplete ###



import json
from tkinter import *

# Task class
class Task:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.completed = False
        self.prerequisites = []

# Playthrough class
class Playthrough:
    def __init__(self):
        self.tasks = {}
        self.completed_tasks = []
        
    def add_task(self, task):
        self.tasks[task.name] = task

    def complete_task(self, name):
        if name in self.tasks:
            task = self.tasks[name]
            if not task.completed and set(p.name for p in task.prerequisites).issubset(self.completed_tasks):
                task.completed = True
                self.completed_tasks.append(name)
                return True
        return False
        
# Persistence        
def save_playthrough(playthrough):
    data = {t.name:{'description':t.description,'completed':t.completed,'prerequisites':[p.name for p in t.prerequisites]} 
            for t in playthrough.tasks.values()}
    with open(f'{playthrough.name}.json','w') as f:
        json.dump(data,f)
        
def load_playthrough(name):
    playthrough = Playthrough()
    try:
        with open(f'{name}.json') as f:
            data = json.load(f)
        for tname,tdata in data.items():
            task = Task(tname, tdata['description'])
            task.completed = tdata['completed']
            task.prerequisites = [playthrough.tasks[pname] for pname in tdata['prerequisites']]
            playthrough.add_task(task)
    except:
        pass # file doesn't exist
    return playthrough

# UI CLASS    
class UI:
    # Implementation left as an exercise
    pass

playthroughs = {
    'pt1': load_playthrough('pt1') 
}

ui = UI()

def add_task(): 
    # Get task details and prerequisites
    # Validate prerequisites exist
    # Add new task to playthrough
    pass

def complete_task():
   # Validate completed prerequisites
   # Mark task completed
   pass
   
# Main program loop
while True:
    ui.show_menu()
    if selection == ADD_TASK:
         add_task()
    elif selection == COMPLETE_TASK:
         complete_task()