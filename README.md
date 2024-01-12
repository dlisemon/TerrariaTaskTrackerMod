# TerrariaTaskTrackerMod

## tasktracker module

Contains Task and CentralTrackerLibrary classes
Task stores name/description/completion status/parent tasks
Library holds all Task instances and completed names
Methods to add, complete, and retrieve tasks

## tttgui module

Implements a Tkinter GUI for the program
Has TTTGui class that builds interface
Creates menu, left sidebar with tree, details pane, status bar
Binds events like button clicks to actions on tasks
Loads and saves task data to synchronize with Library

### The GUI should allow users to:

View task tree showing dependencies
Select tasks to populate a details pane
Buttons to add/complete/delete tasks
Menu system to save and load task data

## tttdriver module

Launches the application
Creates Library and TTTGui objects
Handles passing data between UI and logic
Manages overall flow

