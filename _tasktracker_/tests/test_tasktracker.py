import unittest
from TTTv3 import Task, CentralTrackerLibrary, save_library, load_library

class TestTask(unittest.TestCase):

    def test_can_complete(self):
        task = Task("Test", "Description")
        library = CentralTrackerLibrary()
        
        task.parent_tasks = ["A","B"]
        parent_a = Task("A", "Parent A") 
        parent_b = Task("B", "Parent B")
        
        library.tasks["A"] = parent_a
        library.tasks["B"] = parent_b
         
        self.assertFalse(task.can_complete(library))
        
        parent_b.completed = True
        self.assertFalse(task.can_complete(library))
        
        parent_a.completed = True
        self.assertTrue(task.can_complete(library))
        
class TestLibrary(unittest.TestCase):

    def test_add_task_validation(self):
        library = CentralTrackerLibrary()
        task = Task("New Task", "Description")  
        prerequisite = Task("Prereq", "PreReq")
        
        library.tasks["Prereq"] = prerequisite 
        library.add_task(task)
        self.assertIn(task, library.tasks)  
        
        task2 = Task("Task2", "Desc", ["InvalidPrereq"]) 
        library.add_task(task2)
        self.assertNotIn(task2, library.tasks)
        
class TestPersistence(unittest.TestCase):

    def test_save_load(self):
        # Initialization code   
        save_library(library, "temp.json")
        
        loaded = load_library("temp.json")
       
        self.assertEqual(len(loaded.tasks), 1)
        self.assertIn(task1, loaded.tasks)
         
if __name__ == "__main__":
    unittest.main()