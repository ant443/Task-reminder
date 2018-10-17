# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 12:11:32 2017

@author: Anthony
"""
    
def output_weeks_tasks_and_update_file():
    import datetime
    
    def read_data(location):        
        with open(location, "r") as f:
            L = []
            for line in f:
                line = line.rstrip("\n")
                if line:
                    L.append(line)
            return L
    
    def read_weekday_tasks(file_location):
        weekdays = {"Monday": "", "Tuesday": "", "Wednesday": "", 
                "Thursday": "", "Friday": "", "Saturday": "", "Sunday": ""}
        dayname = ""
        days_tasks = ""
        days_found = set([])
        tasks_and_days_list = read_data(file_location)
        for i in tasks_and_days_list:
            if i in weekdays.keys():
                if dayname:
                    weekdays[dayname] = days_tasks
                    days_tasks = ""
                dayname = i
                days_found.add(dayname)
            else:
                days_tasks += i + "\n"
        weekdays[dayname] = days_tasks.rstrip("\n")
        assert len(days_found) == 7
        return weekdays
    
    def make_nested_lists(single_list):
        return [i.split(", ", 2) for i in single_list]
        
    def read_formatted_data(location):
        return make_nested_lists(read_data(location))
    
    def validate_three_items(item_list):
        if len(item_list) != 3:
            raise IndexError("Expected 3 items in each list")
        
    def validate_frequency(text):
        import re
        if re.fullmatch("[0-9]+[wd]", text) is None:
            raise ValueError("Incorrect frequency format. "
                             "Expected digits then d or w. Example: 24w")
            
    def validate_format(tasks_by_date):
        for i in range(len(tasks_by_date)):
            validate_three_items(tasks_by_date[i])
            validate_frequency(tasks_by_date[i][1])
            
    def convert_to_num(day):
        import time
        return time.strptime(day, "%A").tm_wday
    
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
        
        for i in range(len(tasks_by_date)):
            task_date = tasks_by_date[i][0]
            task_date_obj = convert_to_date_obj(tasks_by_date[i][0])      
            task_frequency = tasks_by_date[i][1]
            task_text = tasks_by_date[i][2]
            
            if task_date_obj <= date_in_loop:
        # add task to weeks_tasks plus a notice if old date detected
                if task_date_obj < date_in_loop:
                    num_days_old = (date_in_loop - task_date_obj).days
                    weeks_tasks.append(missed_task_msg(task_date, num_days_old))
                weeks_tasks.append(task_text.replace(". ", "\n") + '\n')
        # update the tasks date        
                New_date_obj = date_in_loop + make_timedelta(task_frequency)
                New_date_str = convert_to_string(New_date_obj)
                tasks_by_date[i][0] = New_date_str
        return tasks_by_date, weeks_tasks
    
    def replace_file_data(location, tasks_list):
        with open(location, 'w') as f:
            for i in tasks_list:
                f.write(", ".join(i) + '\n')
                
    def create_output_file(location, weeks_tasks):
        with open(location, 'a') as f:
            for i in weeks_tasks:
                f.write(i)
    
    todays_date = datetime.date.today()    
    startday = "Monday"    
    tasks_by_date_location = "tasks_by_date.txt"
    weekday_tasks_location = "monday_to_sunday_tasks.txt"
    tasks_by_weekday = read_weekday_tasks(weekday_tasks_location)
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
        weeks_tasks.append(tasks_by_weekday.get(readable_date.split()[0])+'\n')
        
    replace_file_data(tasks_by_date_location, tasks_by_date)
    output_location = "weeks_tasks.txt"
    create_output_file(output_location, weeks_tasks)
            
    print("Task complete", end='')

output_weeks_tasks_and_update_file()



# TODO:
# Add ability to use m and y in tasks_by_date.txt for months and years
# Add ability for script to remove task if labeled not regular in some way, 
# e.g. a one off appointment.