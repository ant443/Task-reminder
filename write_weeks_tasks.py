# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 12:11:32 2017

@author: Ant443
"""
    
import datetime

def get_file_data(location: str) -> list:
    """Returns file data"""
    with open(location) as f:
        return f.readlines()

def strip_line_endings(data: list) -> list:
    """Removes line endings(\n). Removes item if only contains \n."""
    return [i.rstrip("\n") for i in data if i != "\n"]

def halt_on_missing_or_duplicate_days(days_and_tasks: list, daynames):
    """ Raises error, halting script, if missing or duplicate days"""
    days_found = set()
    for i in days_and_tasks:
        if i in daynames:
            if i in days_found:
                raise ValueError("Duplicate day found on it's own line, in weekly tasks list.")
            days_found.add(i)
    if len(days_found) < 7:
        raise ValueError("A day is missing from weekly tasks list. Make sure each day appears on it's own line")

def convert_to_dictionary(days_and_tasks_list, daynames: list):
    """ Populates days_and_tasks_dict with tasks from days_and_tasks_list.
        Ignores any text before first day heading.
    """
    days_and_tasks_dict = dict.fromkeys(daynames, "")
    current_day = ""
    for i in days_and_tasks_list:
        if i in daynames:
            current_day = i
        else:
            if current_day:
                days_and_tasks_dict[current_day] += i + "\n"
    return days_and_tasks_dict

DAYNAMES = [
    "Monday", "Tuesday", "Wednesday", "Thursday", 
    "Friday", "Saturday", "Sunday"
    ]

def get_weekly_tasks_as_dictionary(location, daynames: list):
    """Calls functions required to convert weekly_tasks to a dictionary"""
    weekly_tasks = get_file_data(location)
    weekly_tasks = strip_line_endings(weekly_tasks)
    halt_on_missing_or_duplicate_days(weekly_tasks, DAYNAMES)
    return convert_to_dictionary(weekly_tasks, DAYNAMES)

def make_nested_lists(single_list):
    return [i.split(", ", 2) for i in single_list]
    
def read_formatted_data(location):
    file_data = get_file_data(location)
    file_data = strip_line_endings(file_data)
    return make_nested_lists(file_data)

def validate_three_items(item_list):
    if len(item_list) != 3:
        raise IndexError("Expected 3 items in each list")
    
def validate_frequency(text):
    import re
    if re.fullmatch("[0-9]+[wd]", text) is None:
        raise ValueError("Incorrect frequency format. "
                            "Expected digits then d or w. Example: 24w")
        
def validate_format(tasks_by_date):
    for inner_list in tasks_by_date:
        validate_three_items(inner_list)
        validate_frequency(inner_list[1])
        
def convert_to_num(dayname):
    import time
    return time.strptime(dayname, "%A").tm_wday

def days_between_weekday(num1, num2):
    oneweek = 7
    return num2 - num1 if num1 <= num2 else num2+oneweek - num1

def make_list_and_format(date_obj):
    return date_obj.strftime('%A %d %b').split()

def get_date_suffix(day_of_month):
    return ('th' if 11<=day_of_month<=13 
            else {1:'st',2:'nd',3:'rd'}.get(day_of_month%10, 'th'))

def make_readable(date_obj):
    formatted_date = make_list_and_format(date_obj)
    return (formatted_date[0] + ' ' + formatted_date[1].lstrip('0') +
            get_date_suffix(date_obj.day) + ' ' + formatted_date[2])
    
def get_future_date(todays_date, days_to_target):
    return todays_date + datetime.timedelta(days=days_to_target)

def process_matching_dates(date_in_loop, tasks_by_date, weeks_tasks):
    def missed_task_msg(date_indicated, days_old):
        return ("old task detected. Should have been done on "
            "{}({} days ago): ".format(date_indicated, days_old))

    def make_timedelta(task_frequency):
        if task_frequency[-1] == 'd':
            return datetime.timedelta(days=int(task_frequency[:-1]))
        else:
            return datetime.timedelta(weeks=int(task_frequency[:-1]))
        
    def convert_to_date_obj(date_string):
        """will raise error if wrong format"""
        return datetime.datetime.strptime(date_string, "%b %d %Y").date()
    
    def convert_to_string(date_obj):
        return date_obj.strftime('%b %d %Y')

    tasks_by_date = tasks_by_date[:]
    weeks_tasks = weeks_tasks[:]
    
    for inner_list in tasks_by_date:
        task_date = inner_list[0]
        task_date_obj = convert_to_date_obj(inner_list[0])      
        task_frequency = inner_list[1]
        task_text = inner_list[2]
        
        if task_date_obj <= date_in_loop:
    # add task to weeks_tasks plus a notice if old date detected
            if task_date_obj < date_in_loop:
                num_days_old = (date_in_loop - task_date_obj).days
                weeks_tasks.append(missed_task_msg(task_date, num_days_old))
            weeks_tasks.append(task_text.replace(". ", "\n") + '\n')
    # update the tasks date        
            New_date_obj = date_in_loop + make_timedelta(task_frequency)
            New_date_str = convert_to_string(New_date_obj)
            inner_list[0] = New_date_str
    return tasks_by_date, weeks_tasks

def replace_file_data(location, tasks_list):
    with open(location, 'w') as f:
        for inner_list in tasks_list:
            f.write(", ".join(inner_list) + '\n')
            
def create_output_file(location, weeks_tasks):
    with open(location, 'a') as f:
        for i in weeks_tasks:
            f.write(i)

if __name__ == "__main__":

    todays_date = datetime.date.today()    
    startday = "Monday"    
    tasks_by_date_location = "tasks_by_date.txt"
    weekly_tasks_location = "weekly_tasks.txt"
    weekly_tasks = get_weekly_tasks_as_dictionary(weekly_tasks_location, DAYNAMES)

    tasks_by_date = read_formatted_data(tasks_by_date_location)
    validate_format(tasks_by_date)
    days_to_startday = days_between_weekday(todays_date.weekday(),
                                            convert_to_num(startday))
    weeks_tasks = []

    # loop from startday to endday
    for i in range(7):
        days_between = days_to_startday + i
        date_in_loop = get_future_date(todays_date, days_between)
        readable_date = make_readable(date_in_loop)
        weeks_tasks.append(readable_date + '\n')
        tasks_by_date, weeks_tasks = process_matching_dates(date_in_loop, 
                                                            tasks_by_date, 
                                                            weeks_tasks)                                                 
        weeks_tasks.append(weekly_tasks.get(readable_date.split()[0])+'\n')
        
    output_location = "weeks_tasks.txt"
    create_output_file(output_location, weeks_tasks)
    replace_file_data(tasks_by_date_location, tasks_by_date)
            
    print("Task complete")