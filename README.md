# Project: task-reminder

## Description
A Python script that reads tasks from two files, one containing tasks by weekday, the other containing tasks by date. When run, it prints your weeks tasks to a new file and updates dated task's date based on the frequency you gave the task.

## Motivation
This saves me from having to remember tasks I need to do regularly.

## Prerequisites
Windows only. Only tested on windows 7. 
Requires Python 3 to be installed. Only tested with Python 3.5.3

## Installing: 
Clone/download repository to harddrive.

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
Screenshots below  

##### A small note if you choose download Zip and use notepad as your text editor: 
###### GitHub runs git archive on a linux machine that will default to linux line endings. Notepad doesn't know how to handle linux line endings, so all the example text will be on the same line. You may want to use a different text editor(or create new lines for the day names and tasks).

## Screenshots

![image](https://user-images.githubusercontent.com/31293098/47236776-0f1f3b80-d3d5-11e8-9ed9-37b8d12c9bdb.png)  
![image](https://user-images.githubusercontent.com/31293098/47232654-29065180-d3c8-11e8-8cd9-f22c6d0a25ae.png)
![image](https://user-images.githubusercontent.com/31293098/47232658-2dcb0580-d3c8-11e8-94c1-770de6438a97.png)
![image](https://user-images.githubusercontent.com/31293098/47231868-05420c00-d3c6-11e8-8a06-566c3fb2273c.png)
![image](https://user-images.githubusercontent.com/31293098/47231886-0ffca100-d3c6-11e8-8a37-dc55b9dcb349.png)
![image](https://user-images.githubusercontent.com/31293098/47231898-1559eb80-d3c6-11e8-9f06-bae6ea2e2c9b.png)
