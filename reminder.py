# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 12:11:32 2017

@author: Ant443
"""
    
import datetime
import re
import time
import copy

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
                raise ValueError("Duplicate day found on it's own line, in " \
                    "weekly tasks list.")
            days_found.add(i)
    if len(days_found) < 7:
        raise ValueError("A day is missing from weekly tasks list. Make sure" \
            " each day appears on it's own line")

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

def get_weekly_tasks_dictionary(location, daynames: list):
    """Calls functions required to convert weekly_tasks to a dictionary"""
    weekly_tasks = get_file_data(location)
    weekly_tasks = strip_line_endings(weekly_tasks)
    halt_on_missing_or_duplicate_days(weekly_tasks, DAYNAMES)
    return convert_to_dictionary(weekly_tasks, DAYNAMES)

def split_twice_on_comma(date_frequency_task_strings: list) -> list:
    """ 'date, frequency, task' strings become [date, frequency, task] lists"""
    return [i.split(", ", 2) for i in date_frequency_task_strings]
    
def validate_three_items(date_frequency_task: list):
    """raises error if a list doesn't contain exactly 3 items"""
    if len(date_frequency_task) != 3:
        raise IndexError(f"Expected task_by_date format: date, frequency, " \
            f"task on the same line. Problematic task: {date_frequency_task}")
    
def validate_frequency(frequency: str):
    """raises ValueError if incorrect format for task frequency.
       frequency: digits: 1+ letters: dwy, white space, any no. of times.
    """
    if re.fullmatch("( *[0-9]*[1-9][0-9]*[dwy] *)+", frequency) is None:
        raise ValueError("Incorrect frequency format. "
            f"Expected digits 1+ followed by d w or y. Example: 1y 24w")
    for i in ["d", "w", "y"]:
        if frequency.count(i) >1:
            raise ValueError("duplicate duration type found in tasks_by_date."
                "Make sure only one of each: d w y in duration per task.")
        
def validate_format(date_frequency_task_lists):
    """Checks tasks by date where format in correct format"""
    for inner_list in date_frequency_task_lists:
        validate_three_items(inner_list)
        validate_frequency(inner_list[1])
        
def get_date_frequency_task_lists(location) -> list:
    """Gets tasks by date and converts them to nested lists,
        each with date, frequency, task items.
    """
    tasks_by_date = get_file_data(location)
    tasks_by_date = strip_line_endings(tasks_by_date)
    date_frequency_task_lists = split_twice_on_comma(tasks_by_date)
    validate_format(date_frequency_task_lists)
    return date_frequency_task_lists

def get_day_num(dayname) -> int:
    """Converts dayname to 0 indexed number in week e.g Sunday -> 6"""
    return time.strptime(dayname, "%A").tm_wday

def get_num_days_between(day1: int, day2: int) -> int:
    """Return number of days between two days as their number in week"""
    one_week = 7
    return day2 - day1 if day1 <= day2 else day2+one_week - day1

def get_future_date(date: datetime.date, days_to_target: int) -> datetime.date:
    """Adds a number of days to a date object, returning a new date object"""
    return date + datetime.timedelta(days=days_to_target)

def format_and_split(date: datetime.date) -> list:
    """formats date into list items e.g. ["Wednesday", "15", "Jan"]"""
    return date.strftime("%A %d %b").split()

def get_date_suffix(day_the_month: int) -> str:
    """Returns the day number's suffix e.g. 22 -> 'nd'"""
    return ("th" if 11<=day_the_month<=13 
            else {1:"st",2:"nd",3:"rd"}.get(day_the_month%10, "th"))

def to_readable(date: datetime.date) -> str:
    """Converts a date to something more readable e.g. Monday 3rd Jan"""
    day_with_suffix = str(date.day) + get_date_suffix(date.day)
    day_name, _, month_abbreviation = format_and_split(date)
    return f"{day_name} {day_with_suffix} {month_abbreviation}"

def to_datetime_date(date: str) -> datetime.date:
    """Example: converts 'Jan 23 2020' to datetime.date(2020, 1, 23)
       Will raise error, halting script, if wrong format.
    """
    return datetime.datetime.strptime(date, "%b %d %Y").date()

def to_timedelta(duration: str) -> datetime.timedelta:
    """Converts digits and d/w/y days/weeks/years to a datetime duration"""
    duration_type = duration[-1]
    num_of = duration[:-1]
    timedelta = {
        "d": datetime.timedelta(days=int(num_of)),
        "w": datetime.timedelta(weeks=int(num_of)),
        "y": datetime.timedelta(days=int(num_of)*365),
    }
    return timedelta[duration_type]

def to_combined_timedelta(task_frequency: str) -> datetime.timedelta:
    """Extracts int+alpha from task_frequency, e.g. '1y' and '4w' from '1y 4w'.
        Returns the sum after each is converted to a timedelta.
    """
    matches = re.findall("[0-9]*[1-9][0-9]*[dwy]", task_frequency)
    return sum([to_timedelta(i) for i in matches], datetime.timedelta())

def to_string(date: datetime.date) -> str:
    """e.g. converts datetime.date(2020, 5, 6) to May 06 2020"""
    return date.strftime("%b %d %Y")

def get_new_due_date(frequency: str, base_date: datetime.date) -> list:
    """Returns a new date from adding base_date+frequency"""
    return to_string(base_date + to_combined_timedelta(frequency))

def prepare_task_string(task: str, due_date: str, dt_due_date, target):
    """Add some new lines. Notify user if task was overdue."""
    old_task_msg = ""
    if dt_due_date < target:
        days_since_due = (target - dt_due_date).days
        old_task_msg = "Old task detected. Was due on" \
                f" {due_date}({days_since_due} days ago): "
    return old_task_msg + task.replace(". ", ".\n") + "\n"

def get_due_tasks_update_date(target: datetime.date, tasks_by_date: list):
    """Builds string of due tasks incl. old task warnings. updates due date."""
    tasks_due = ""
    updated_tasks_by_date = []
    for date_frequency_task in tasks_by_date:
        due_date, frequency, task = date_frequency_task
        dt_due_date = to_datetime_date(due_date)
        if dt_due_date <= target:
            tasks_due += prepare_task_string(task, due_date, dt_due_date, target)
            date_frequency_task[0] = get_new_due_date(frequency, target)
        updated_tasks_by_date.append(date_frequency_task)
    return updated_tasks_by_date, tasks_due

def get_todays_date():
    """datetime.today is hard to mock otherwise"""
    return datetime.date.today()

def get_weeks_tasks_replace_due_task_dates(**kwargs):
    """From start_day, for each day in number of days specified or 7,
        make day's heading, get it's tasks, and update due date.
    """
    start_day = get_day_num(kwargs["start_day"])
    today = kwargs["todays_date"].weekday()
    days_to_start_day = get_num_days_between(today, start_day)
    due_tasks = ""
    weeks_tasks = []
    tasks_by_date = copy.deepcopy(kwargs["tasks_by_date"])
    for i in range(kwargs["num_days_to_write"]):
        days_to_target = days_to_start_day + i
        target_date = get_future_date(kwargs["todays_date"], days_to_target)
        readable_date_heading = to_readable(target_date) + "\n"
        weeks_tasks.append(readable_date_heading)
        tasks_by_date, due_tasks = get_due_tasks_update_date(target_date, tasks_by_date)
        if due_tasks:
            weeks_tasks.append(due_tasks)
        target_day_name = readable_date_heading.split()[0]
        target_days_weekly_tasks = kwargs["weekly_tasks"].get(target_day_name)
        weeks_tasks.append(target_days_weekly_tasks + "\n")
    return weeks_tasks, tasks_by_date

def replace_file_data(location, tasks: list):
    """Replaces location file's contents with data from a list of lists"""
    with open(location, "w") as f:
        for inner_list in tasks:
            f.write(", ".join(inner_list) + "\n")
            
def create_output_file(location, weeks_tasks: list):
    """Creates a new file with data from a list"""
    with open(location, "a") as f:
        for i in weeks_tasks:
            f.write(i)

def dayname_or_halt_script(alpha: str):
    name = alpha[0].upper() + alpha[1:]
    conversions = {
        "Mon": "Monday", "Tue": "Tuesday", "Wed": "Wednesday",
        "Thu": "Thursday", "Fri": "Friday", "Sat": "Saturday",
        "Sun": "Sunday"
        }
    if name in conversions:
        return conversions[name]
    elif name in DAYNAMES:
        return name
    else:
        raise ValueError("unrecognizable argument found. Accepts "
            "start day as a day of the week, or a number for number "
            "of days to write")

def is_int(arg: str) -> bool:
    try:
        int(arg)
        return True
    except:
        return False

def process(args: list) -> dict:
    kwargs = {}
    for arg in args:
        if is_int(arg):
            if int(arg) < 0:
                raise ValueError("Number of days to write may not be negative")
            if "num_days_to_write" in kwargs:
                raise ValueError("You have given two numbers for days to write")
            kwargs["num_days_to_write"] = int(arg)
        else:
            if "start_day" in kwargs:
                raise ValueError("You have given two names for day to start on")
            dayname = dayname_or_halt_script(arg)
            kwargs["start_day"] = dayname
    return kwargs

def main(start_day="Monday", num_days_to_write=7):
    tasks_by_date_location = "tasks_by_date.txt"
    weekly_tasks_location = "weekly_tasks.txt"
    weekly_tasks = get_weekly_tasks_dictionary(weekly_tasks_location, DAYNAMES)
    tasks_by_date = get_date_frequency_task_lists(tasks_by_date_location)
    todays_date = get_todays_date()
    kwargs = {
        "start_day": start_day,
        "num_days_to_write": num_days_to_write,
        "weekly_tasks": weekly_tasks,
        "tasks_by_date": tasks_by_date,
        "todays_date": todays_date
    }
    weeks_tasks, tasks_by_date = get_weeks_tasks_replace_due_task_dates(**kwargs)
    output_location = "weeks_tasks.txt"
    create_output_file(output_location, weeks_tasks)
    replace_file_data(tasks_by_date_location, tasks_by_date)
    print("Task complete")

if __name__ == "__main__":
    import sys
    
    args = sys.argv[1:]
    kwargs = process(args)
    main(**kwargs)