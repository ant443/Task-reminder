# Project: task-reminder

## Description
Takes dated tasks and weekly tasks from two files, and writes due tasks for the week(or days specified) to a new file.


## Motivation
I wanted something like a calendar, that I didn't have to write the same task again.

## Prerequisites
Python 3.5+

## Installing: 
Clone/download repository to harddrive.

## Usage:
##### Add tasks:
In weekly_tasks.txt you can write tasks, to be done every week, under their day name.  
In tasks_by_date.txt you give a date and a duration/frequency to the tasks(examples in file). The script will update the due date each time, based on task's frequency.  
When reminder.py is run, weeks_tasks.txt will appear in the same directory containing dayname headings and their due tasks.

##### Run script:
In command line, cd to project folder, then type the following and press enter:  
`python reminder.py`  
Or if you have multiple python versions installed, try:  
`python3 reminder.py`  
tests can be run using the command:  
`python3 -m unittest discover`

##### Notes:  
Dated tasks separated by a full stop and a space will be placed on a new line for convenience.
Dated tasks will be printed last for each day.
If downloading zip and using Windows Notepad: Due to github sending Linux based line endings, Notepad on Windows won't display the line endings, so all the text will appear on the same line. I recommend adding them yourself, or try a different editor such as notepad++.
