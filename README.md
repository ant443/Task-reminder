# Project: task-reminder

## Description
A Python script that reads tasks from two files, one containing tasks by weekday, the other containing tasks by date. When run, it prints your weeks tasks to a new file and updates dated task's date based on the frequency you gave the task.

## Motivation
This saves me from having to remember tasks I need to do regularly.

## Prerequisites
Windows only. Only tested on windows 7. 
Requires Python 3 to be installed. Only tested with Python 3.5.3

## Installing: 
Copy/Clone repository to harddrive.

## Usage:
##### Add tasks to files:
tasks_by_date.txt has a specific format to use, with examples given inside it.  
Dated tasks separated by a full stop will be placed on a new line.  
In monday_to_sunday_tasks.txt you can just add tasks under the day name you want.
##### Run script:
cd to project folder in command line then type the following line and press enter:  
python write_weeks_tasks.py  
Or if that didn't work try:  
python3 write_weeks_tasks.py  
A new file weeks_tasks.txt will appear in the project folder.  
Note: Dated tasks will be printed last for each day.  
