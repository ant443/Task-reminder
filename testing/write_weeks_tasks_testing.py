# -*- coding: utf-8 -*-
"""
Created on Tue Sep  4 13:05:35 2018

@author: Anthony
"""

# =============================================================================
# Test Suit
# =============================================================================

import datetime


weekday_tasks_location = "test_files/tasks_by_weekday.txt"
dated_tasks_location = "test_files/tasks_by_date.txt"
output_location = "test_files/output_test.txt"
# ============================================================================

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

working_data_from_test_file = {'Friday': 'Friday lines1\nFriday lines2\n',
        'Tuesday': 'Tuesday lines1\nTuesday lines2\n',
        'Saturday': 'lines for sat1\nlines for sat2\n',
        'Thursday': 'Thursday lines1\nThursday lines2\n',
        'Wednesday': 'Wednesday lines1\nWednesday lines2\n',
        'Sunday': 'sun lines1\nsun lines2',
        'Monday': 'Monday lines1\nMonday lines2\n'
        }

assert(read_weekday_tasks(weekday_tasks_location) == 
       working_data_from_test_file)

def make_nested_lists(single_list):
    return [i.split(", ", 2) for i in single_list]
    
def read_formatted_data(location):
    return make_nested_lists(read_data(location))

# read_formatted_data test cases
read_formatted_data_working_output = [['Sep 13 2018', '5d', 'test text1'], 
                 ['Sep 19 2018', '24w', 'test text 2'], 
                 ['Jan 01 2019', '365d', 'test text 3'], 
                 ['Dec 04 2018', '365d', 'test text 4'], 
                 ['Jul 20 2019', '365d', 'test text 5'], 
                 ['Jan 01 2021', '183w', 'test text 6']]
assert(read_formatted_data(dated_tasks_location) == 
       read_formatted_data_working_output)
# ============================================================================

def convert_to_date_tester(date_string):
    try:
        return datetime.datetime.strptime(date_string, "%b %d %Y").date()
    except ValueError as e:
        return e

#convert_to_date test cases
convert_to_date_tester("Sep 3 2018")
assert(isinstance(convert_to_date_tester(" 3 2018"), ValueError))

def validate_frequency_tester(text):
    import re
    try:
        if re.fullmatch("[0-9]+[wd]", text) is None:
            raise ValueError("Incorrect frequency format. "
                             "Expected digits then d or w. Example: 24w")
    except ValueError as e:
        return e       

#validate_frequency test cases
validate_frequency_tester("365d")
validate_frequency_tester("24w")
assert(isinstance(validate_frequency_tester(""), ValueError))
assert(isinstance(validate_frequency_tester("test text 6d"), ValueError))
assert(isinstance(validate_frequency_tester("24"), ValueError))
assert(isinstance(validate_frequency_tester("d"), ValueError))

def validate_three_items_tester(item_list):
    try:
        if len(item_list) != 3:
            raise IndexError("Expected 3 items in each list")
    except IndexError as e:
        return e
        
#validate_three_items test cases
assert(isinstance(validate_three_items_tester([]), IndexError))
assert(isinstance(validate_three_items_tester(["one item"]), IndexError))
validate_three_items_tester(["", "", "three items"])
assert(isinstance(validate_three_items_tester(["", "", "", "four items"]), 
                                              IndexError))
    
def validate_format(tasks_by_date):
    for i in range(len(tasks_by_date)):
        validate_frequency_tester(file_dates_test_data[i][1])
        validate_three_items_tester(file_dates_test_data[i])
        
file_dates_test_data = [['Sep 13 2018', '5d', 'test text1'], 
                 ['Sep 29 2018', '24w', 'test text 2'], 
                 ['Jan 01 2019', '365d', 'test text 3'], 
                 ['Dec 04 2018', '365d', 'test text 4'], 
                 ['Jul 20 2019', '365d', 'test text 5'], 
                 ['Jan 01 2021', '183w', 'test text 6']]

validate_format(file_dates_test_data)
# ============================================================================

def convert_to_num(day):
    import time
    return time.strptime(day, "%A").tm_wday

# convert_to_num test cases
assert((convert_to_num("Monday") == 0))
assert((convert_to_num("thursday") == 3))
# ============================================================================

def days_between_weekday(num1, num2):
    oneweek = 7
    return num2 - num1 if num1 <= num2 else num2+oneweek - num1
    
# days_between_weekday test cases
assert((days_between_weekday(0, 3)) == 3)
assert((days_between_weekday(3, 0)) == 4)
assert((days_between_weekday(0, 0)) == 0)
assert((days_between_weekday(3, 3)) == 0)
assert((days_between_weekday(6, 0)) == 1)
assert((days_between_weekday(0, 6)) == 6)
# ============================================================================

def make_list_and_format(date_obj):
    return date_obj.strftime('%A %d %b').split()

#make_list_and_format test cases
test_date = datetime.datetime.strptime("26 12 2000", "%d %m %Y")
assert(make_list_and_format(test_date) == ['Tuesday', '26', 'Dec'])

def get_date_suffix(day_of_month):
    return ('th' if 11<=day_of_month<=13
            else {1:'st',2:'nd',3:'rd'}.get(day_of_month%10, 'th'))

##get_date_suffix test cases
assert(get_date_suffix(11) == "th")
assert(get_date_suffix(21) == "st")
assert(get_date_suffix(2) == "nd")
assert(get_date_suffix(3) == "rd")
assert(get_date_suffix(30) == "th")
  
def make_readable(date_obj):
    formatted_date = make_list_and_format(date_obj)
    return (formatted_date[0] + ' ' + formatted_date[1].lstrip('0') +
            get_date_suffix(date_obj.day) + ' ' + formatted_date[2])

#make_readable test cases
test_date2 = datetime.datetime.strptime("26 12 2000", "%d %m %Y")
assert(make_readable(test_date2) == "Tuesday 26th Dec")
# ============================================================================

def convert_to_date_obj(date_string):
    """will raise error if wrong format"""
    return datetime.datetime.strptime(date_string, "%b %d %Y").date()

def convert_to_string(date_obj):
    return date_obj.strftime('%b %d %Y')

#convert_to_date_obj and convert_to_string test cases
assert(convert_to_string(convert_to_date_obj('Jan 01 2019'))) == "Jan 01 2019"

def get_future_date(todays_date_obj, days_to_target):
    return todays_date_obj + datetime.timedelta(days=days_to_target)

#get_future_date test cases
fake_todays_date = "Sep 16 2018"
todays_date = convert_to_date_obj(fake_todays_date)
assert(convert_to_string(get_future_date(todays_date, 5))) == "Sep 21 2018"

def make_timedelta(task_frequency):
    if task_frequency[-1] == 'd':
        return datetime.timedelta(days=int(task_frequency[:-1]))
    else:
        return datetime.timedelta(weeks=int(task_frequency[:-1]))

assert(type(make_timedelta("365d")) == datetime.timedelta)
assert(str(make_timedelta("365d")) == "365 days, 0:00:00")
assert(type(make_timedelta("24w")) == datetime.timedelta)
assert(str(make_timedelta("24w")) == "168 days, 0:00:00")

def process_matching_dates(date_in_loop, tasks_by_date, weeks_tasks):
    def missed_task_msg(date_indicated, days_old):
        return ("old task detected. Should have been done on "
                "{}({} days ago): ".format(date_indicated, days_old))
    
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

#process_matching_dates test cases
weeks_tasks = []
file_dates_test_data2 = [['Sep 13 2018', '5d', 'test text1'], 
                 ['Sep 16 2018', '24w', 'test text 2'], 
                 ['Jan 01 2019', '365d', 'test text 3'], 
                 ['Dec 04 2018', '365d', 'test text 4'], 
                 ['Jul 20 2019', '365d', 'test text 5'], 
                 ['Jan 01 2021', '183w', 'test text 6']]

tasks_by_date, weeks_tasks = process_matching_dates(todays_date, 
                                                      file_dates_test_data2, 
                                                      weeks_tasks)

assert(tasks_by_date == [['Sep 21 2018', '5d', 'test text1'], 
                      ['Mar 03 2019', '24w', 'test text 2'], 
                      ['Jan 01 2019', '365d', 'test text 3'], 
                      ['Dec 04 2018', '365d', 'test text 4'], 
                      ['Jul 20 2019', '365d', 'test text 5'], 
                      ['Jan 01 2021', '183w', 'test text 6']])
assert(weeks_tasks == (["old task detected. Should have been done on "
                             "Sep 13 2018(3 days ago): ", "test text1\n", 
                             "test text 2\n"]))

# ============================================================================

# output_weeks_tasks_and_update_file testing
def replace_file_data(location, tasks_list):
    with open(location, 'w') as f:
        for i in tasks_list:
            f.write(", ".join(i) + '\n')
            
def read_data2(location):
    """temp function for testing only"""      
    with open(location, "r") as f:
        return f.read()
stored_tasks_by_date = read_data2(dated_tasks_location)


def output_weeks_tasks_and_update_file():
                       
    def create_output_file(location, weeks_tasks):
        with open(location, 'a') as f:
            for i in weeks_tasks:
                f.write(i)
        
    fake_todays_date = "Sep 16 2018"
    todays_date = convert_to_date_obj(fake_todays_date)
    startday = "Monday"    
    tasks_by_weekday = read_weekday_tasks(weekday_tasks_location)
    tasks_by_date = read_formatted_data(dated_tasks_location)
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
        
    replace_file_data(dated_tasks_location, tasks_by_date)
    create_output_file(output_location, weeks_tasks)

output_weeks_tasks_and_update_file()

# test cases
working_tasks_by_date_overwrite = ("Sep 27 2018, 5d, test text1\n"
                                    "Mar 06 2019, 24w, test text 2\n"
                                    "Jan 01 2019, 365d, test text 3\n"
                                    "Dec 04 2018, 365d, test text 4\n"
                                    "Jul 20 2019, 365d, test text 5\n"
                                    "Jan 01 2021, 183w, test text 6\n")

assert(read_data2(dated_tasks_location) == 
       working_tasks_by_date_overwrite)

with open(dated_tasks_location, "w") as f:
    f.write(stored_tasks_by_date)

working_output_test_data = """Monday 17th Sep
old task detected. Should have been done on Sep 13 2018(4 days ago): test text1
Monday lines1
Monday lines2

Tuesday 18th Sep
Tuesday lines1
Tuesday lines2

Wednesday 19th Sep
test text 2
Wednesday lines1
Wednesday lines2

Thursday 20th Sep
Thursday lines1
Thursday lines2

Friday 21st Sep
Friday lines1
Friday lines2

Saturday 22nd Sep
test text1
lines for sat1
lines for sat2

Sunday 23rd Sep
sun lines1
sun lines2
"""

assert(read_data2(output_location) == working_output_test_data)

with open(output_location, "w") as f:
    pass

print("testing complete, no errors")








