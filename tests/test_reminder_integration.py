import unittest
from unittest.mock import patch, mock_open, Mock
import datetime

import reminder

class WriteWeeksTasksIntegrationTest(unittest.TestCase):
    
    def test_get_weekly_tasks_dictionary__returns_expected(self):
        weekly_tasks = "some text\n\nMonday\nskiing\n\nTuesday\n\nWednesday" \
            "\n\nThursday\nFriday\n\nSaturday\n\nSunday\nsnooker\nbins out\n"
        mocked_open = mock_open(read_data=weekly_tasks)
        with patch("reminder.open", mocked_open):
            result = reminder.get_weekly_tasks_dictionary("filename", reminder.DAYNAMES)
        expected = {
            "Monday": "skiing\n", "Tuesday": "", "Wednesday": "",
            "Thursday": "", "Friday": "", "Saturday": "",
            "Sunday": "snooker\nbins out\n"
            }
        self.assertEqual(result, expected)

    def test_get_date_frequency_task_lists__returns_expected(self):
        dated_tasks = "Sep 18 2018, 4w, Example monthly task.\nOct 2 2018, " \
            "5d, Example task, written every 5 days.\n"
        mocked_open = mock_open(read_data=dated_tasks)
        with patch("reminder.open", mocked_open):
            result = reminder.get_date_frequency_task_lists("filename")
        expected = [
            ["Sep 18 2018", "4w", "Example monthly task."], 
            ["Oct 2 2018", "5d", "Example task, written every 5 days."]
            ]
        self.assertEqual(result, expected)

    def test_to_readable__expected_output(self):
        date = datetime.date(2019, 11, 3)
        expected = "Sunday 3rd Nov"
        result = reminder.to_readable(date)
        self.assertEqual(expected, result)

    def test_to_combined_timedelta__still_matches_with_white_space(self):
        duration = "    1d    3w   "
        expected = datetime.timedelta(22)
        result = reminder.to_combined_timedelta(duration)
        self.assertEqual(expected, result)

    def test_replace_date__overdue_task(self):
        date_frequency_task = ["Jun 3 2019", "4w", "Example task."]
        target = datetime.date(2020, 5, 27)
        expected = ["Jun 24 2020", "4w", "Example task."]
        result = reminder.replace_date(date_frequency_task, target)
        self.assertEqual(expected, result)

    def test_replace_date__due_task(self):
        date_frequency_task = ["Apr 3 2020", "6d", "Example task."]
        target = datetime.date(2020, 4, 3)
        expected = ["Apr 09 2020", "6d", "Example task."]
        result = reminder.replace_date(date_frequency_task, target)
        self.assertEqual(expected, result)

    def test_get_due_tasks_update_date__task_overdue(self):
        target = datetime.date(2020, 4, 27)
        tasks_by_date = [
            ["Sep 18 2018", 
            "4w", 
            "Example monthly task. Add tasks in this " \
            "format, use w for weeks, d for days."
            ], 
            ["Oct 2 2018", 
            "5d", 
            "Example task, written every 5 days."
            ]
        ]
        expected_tasks_by_date = [
            ["May 25 2020", "4w", "Example monthly task. Add tasks in this " \
             "format, use w for weeks, d for days."], 
            ["May 02 2020", "5d", "Example task, written every 5 days."]
        ]
        expected_weeks_tasks = "Old task detected. Was due on Sep 18 2018" \
            "(587 days ago): Example monthly task.\nAdd tasks in this " \
            "format, use w for weeks, d for days.\nOld task detected. Was " \
            "due on Oct 2 2018(573 days ago): Example task, written every 5 days.\n"
        result_task_by_date, result_weeks_tasks = reminder.get_due_tasks_update_date(target, tasks_by_date)
        self.assertEqual(expected_tasks_by_date, result_task_by_date)
        self.assertEqual(expected_weeks_tasks, result_weeks_tasks)

    def test_get_due_tasks_update_date__task_not_due(self):
        target = datetime.date(2018, 8, 11)
        tasks_by_date = [["Sep 18 2018", "4w", "Example monthly task."]]
        expected_tasks_by_date = [["Sep 18 2018", "4w", "Example monthly task."]]
        expected_weeks_tasks = ""
        result_task_by_date, result_weeks_tasks = reminder.get_due_tasks_update_date(target, tasks_by_date)
        self.assertEqual(expected_tasks_by_date, result_task_by_date)
        self.assertEqual(expected_weeks_tasks, result_weeks_tasks)

    def test_get_due_tasks_update_date__task_due(self):
        target = datetime.date(2018, 9, 18)
        tasks_by_date = [["Sep 18 2018", "4w", "Example monthly task."]]
        result_task_by_date, result_weeks_tasks = reminder.get_due_tasks_update_date(target, tasks_by_date)
        expected_tasks_by_date = [["Oct 16 2018", "4w", "Example monthly task."]]
        expected_weeks_tasks = "Example monthly task.\n"
        self.assertEqual(expected_tasks_by_date, result_task_by_date)
        self.assertEqual(expected_weeks_tasks, result_weeks_tasks)

    def test_get_weeks_tasks_replace_due_task_dates__with_due_not_due_overdue_tasks(self):
        weekly_tasks = {
            "Monday": "Example Monday task\n", "Tuesday": "", "Wednesday": "", 
            "Thursday": "", "Friday": "", "Saturday": "", "Sunday": ""
            }
        tasks_by_date = [
            ["Jun 19 2020", "1d", "Example 1 day task. Written every day."],
            ["Aug 08 2020", "4w", "Example 4 week task, written every 4 weeks."],
            ["Oct 31 2018", "1y 3d", "1 year 3 days task."]
        ]
        expected_weeks_tasks = [
            "Monday 15th Jun\n", "Old task detected. Was due on Oct 31 2018" \
            "(593 days ago): 1 year 3 days task.\n", "Example Monday task\n\n",
            "Tuesday 16th Jun\n", "\n", "Wednesday 17th Jun\n", "\n",
            "Thursday 18th Jun\n", "\n", "Friday 19th Jun\n",
            "Example 1 day task.\nWritten every day.\n", "\n",
            "Saturday 20th Jun\n", "Example 1 day task.\nWritten every day.\n",
            "\n", "Sunday 21st Jun\n", "Example 1 day task.\nWritten every day.\n", "\n"
            ]
        expected_tasks_by_date = [
            ["Jun 22 2020", "1d", "Example 1 day task. Written every day."],
            ["Aug 08 2020", "4w", "Example 4 week task, written every 4 weeks."],
            ["Jun 18 2021", "1y 3d", "1 year 3 days task."]
        ]
        todays_date = datetime.date(2020, 6, 14) # Sunday
        kwargs = {
            "start_day": "Monday",
            "num_days_to_write": 7,
            "weekly_tasks": weekly_tasks,
            "tasks_by_date": tasks_by_date,
            "todays_date": todays_date
            }
        result_weeks_tasks, result_tasks_by_date = reminder.get_weeks_tasks_replace_due_task_dates(**kwargs)
        self.assertEqual(expected_weeks_tasks, result_weeks_tasks)
        self.assertEqual(expected_tasks_by_date, result_tasks_by_date)

    def test_get_weeks_tasks_replace_due_task_dates__different_start_day(self):
        weekly_tasks = {
            "Monday": "Example Monday task\n", "Tuesday": "", "Wednesday": "", 
            "Thursday": "", "Friday": "", "Saturday": "", "Sunday": ""
            }
        tasks_by_date = [
            ["Jun 19 2020", "1d", "Example 1 day task. Written every day."],
            ["Aug 08 2020", "4w", "Example 4 week task, written every 4 weeks."],
            ["Oct 31 2018", "1y 3d", "1 year 3 days task."]
        ]
        expected_weeks_tasks = [
            "Wednesday 17th Jun\n", "Old task detected. Was due on Oct 31 " \
            "2018(595 days ago): 1 year 3 days task.\n", "\n",
            "Thursday 18th Jun\n", "\n", "Friday 19th Jun\n",
            "Example 1 day task.\nWritten every day.\n", "\n",
            "Saturday 20th Jun\n", "Example 1 day task.\nWritten every day.\n",
            "\n", "Sunday 21st Jun\n", "Example 1 day task.\nWritten every day.\n",
            "\n", "Monday 22nd Jun\n", "Example 1 day task.\nWritten every day.\n",
            "Example Monday task\n\n", "Tuesday 23rd Jun\n",
            "Example 1 day task.\nWritten every day.\n", "\n"
            ]
        expected_tasks_by_date = [
            ["Jun 24 2020", "1d", "Example 1 day task. Written every day."], 
            ["Aug 08 2020", "4w", "Example 4 week task, written every 4 weeks."], 
            ["Jun 20 2021", "1y 3d", "1 year 3 days task."]
            ]
        todays_date = datetime.date(2020, 6, 14) # Sunday
        kwargs = {
            "start_day": "Wednesday",
            "num_days_to_write": 7,
            "weekly_tasks": weekly_tasks,
            "tasks_by_date": tasks_by_date,
            "todays_date": todays_date
            }
        result_weeks_tasks, result_tasks_by_date = reminder.get_weeks_tasks_replace_due_task_dates(**kwargs)
        self.assertEqual(expected_weeks_tasks, result_weeks_tasks)
        self.assertEqual(expected_tasks_by_date, result_tasks_by_date)

    def test_main__opens_correct_files(self):
        weekly_tasks = "Monday\nExample Monday task\n\nTuesday\n\n\nWednesday" \
            "\n\n\nThursday\n\n\nFriday\n\n\nSaturday\n\n\nSunday\n"
        tasks_by_date = "Aug 08 2020, 4w, Example 4 week task, written " \
            "every 4 weeks.\nJun 19 2020, 1d, Example 1 day task. Written " \
            "every day.\nOct 31 2018, 1y 3d, 1 year 3 days task.\n"
        mocked_open = mock_open()
        mocked_open.side_effect = [
            mock_open(read_data=weekly_tasks).return_value,
            mock_open(read_data=tasks_by_date).return_value,
            mock_open().return_value,
            mock_open().return_value
        ]
        mock_todays_date_sunday = Mock(return_value=datetime.date(2020, 6, 14))
        with patch("reminder.open", mocked_open) as m:
            with patch("reminder.get_todays_date", mock_todays_date_sunday):
                reminder.main("Monday")
        expected = [
            (("weekly_tasks.txt",),),
            (("tasks_by_date.txt",),),
            (("weeks_tasks.txt", "a"),),
            (("tasks_by_date.txt", "w"),)
            ]
        self.assertEqual(expected, m.call_args_list)
    
    def test_process__no_args(self):
        args = []
        expected = {}
        result = reminder.process(args)
        self.assertEqual(expected, result)

    def test_process__positive_int(self):
        args = [1]
        expected = {"num_days_to_write": 1}
        result = reminder.process(args)
        self.assertEqual(expected, result)
    
    def test_process__dayname(self):
        args = ["Friday"]
        expected = {"start_day": "Friday"}
        result = reminder.process(args)
        self.assertEqual(expected, result)

    def test_process__day_abreviation(self):
        args = ["Fri"]
        expected = {"start_day": "Friday"}
        result = reminder.process(args)
        self.assertEqual(expected, result)

    def test_process__lowercase_dayname(self):
        args = ["friday"]
        expected = {"start_day": "Friday"}
        result = reminder.process(args)
        self.assertEqual(expected, result)

    def test_process__halts_on_random_letters(self):
        args = ["text"]
        with self.assertRaises(ValueError):
            reminder.process(args)

    def test_process__halts_on_negative_int(self):
        args = ["-1"]
        with self.assertRaises(ValueError):
            reminder.process(args)

    def test_process__dayname_and_int(self):
        args = ["Wednesday", 14]
        expected = {"start_day": "Wednesday", "num_days_to_write": 14}
        result = reminder.process(args)
        self.assertEqual(expected, result)

    def test_process__int_and_dayname(self):
        args = [14, "Wednesday"]
        expected = {"start_day": "Wednesday", "num_days_to_write": 14}
        result = reminder.process(args)
        self.assertEqual(expected, result)

    def test_process__halts_on_random_letters_and_int(self):
        args = ["chars", 3]
        with self.assertRaises(ValueError):
            reminder.process(args)

    def test_process__halts_on_dayname_and_random_letters(self):
        args = ["Sunday", "chars"]
        with self.assertRaises(ValueError):
            reminder.process(args)

    def test_process__halts_on_two_ints(self):
        args = [1, 3]
        with self.assertRaises(ValueError):
            reminder.process(args)

    def test_process__halts_on_two_daynames(self):
        args = ["Tuesday", "Thursday"]
        with self.assertRaises(ValueError):
            reminder.process(args)

    def test_process__halts_on_dayname_int_random_letters(self):
        args = ["Monday", 12, "letters"]
        with self.assertRaises(ValueError):
            reminder.process(args)