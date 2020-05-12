import unittest
from unittest.mock import patch, mock_open, Mock
import datetime

import reminder

class WriteWeeksTasksTest(unittest.TestCase):

    def try_or_fail(self, error, function, *args):
        """Helper function. Fails test if function, raises error, with args"""
        try:
            function(*args)
        except error:
            self.fail(f"{function.__name__} raised " \
                f"{error.__name__} unexpectedly!")

    def test_get_file_data_halts_script_on_error(self):
        errors = [FileNotFoundError, PermissionError]
        for error in errors:
            mocked_open = mock_open()
            mocked_open.side_effect = error
            with patch("reminder.open", mocked_open):
                with self.assertRaises(error):
                    reminder.get_file_data("filename")

    def test_get_file_data__expected_output(self):
        mocked_data = "multi\nline\n\ndata\n"
        mocked_open = mock_open(read_data=mocked_data)
        with patch("reminder.open", mocked_open):
            result = reminder.get_file_data("filename")
        expected = ["multi\n", "line\n", "\n", "data\n"]
        self.assertEqual(result, expected)

    def test_strip_line_endings__removes_line_endings_and_paragraphs(self):
        weekly_tasks = [
            "some text\n", "\n", "Monday\n", "skiing\n", "\n", "Tuesday\n",
            "\n", "Wednesday\n", "\n", "Thursday\n", "Friday\n", "\n", 
            "Saturday\n", "\n", "Sunday\n", "snooker\n", "bins out\n"
            ]
        expected = [
            "some text", "Monday", "skiing", "Tuesday", "Wednesday",
            "Thursday", "Friday", "Saturday", "Sunday", "snooker", "bins out"
            ]
        result = reminder.strip_line_endings(weekly_tasks)
        self.assertEqual(expected, result)

    def test_halt_on_missing_or_duplicate_days__missing(self):
        weekly_tasks = ["Monday", "skiing", "Sunday", "snooker", "bins out"]
        with self.assertRaises(ValueError):
            reminder.halt_on_missing_or_duplicate_days(weekly_tasks, reminder.DAYNAMES)

    def test_halt_on_missing_or_duplicate_days__duplicate(self):
        weekly_tasks = [
            "Monday", "skiing", "Tuesday", "Sunday", "Wednesday", "Thursday", 
            "Friday", "Saturday", "Sunday", "snooker", "bins out"
            ]
        with self.assertRaises(ValueError):
            reminder.halt_on_missing_or_duplicate_days(weekly_tasks, reminder.DAYNAMES)

    def test_halt_on_missing_or_duplicate_days__duplicate_but_correct_num_of(self):
        weekly_tasks = [
            "Tuesday", "Sunday", "Wednesday", "Thursday", 
            "Friday", "Saturday", "Sunday", "snooker", "bins out"
            ]
        with self.assertRaises(ValueError):
            reminder.halt_on_missing_or_duplicate_days(weekly_tasks, reminder.DAYNAMES)

    def test_halt_on_missing_or_duplicate_days__doesnt_raise_on_expected_data(self):
        weekly_tasks = [
            "Monday", "Tuesday", "Wednesday", "Thursday", 
            "Friday", "Saturday", "Sunday", "snooker", "bins out"
            ]
        self.try_or_fail(ValueError, 
            reminder.halt_on_missing_or_duplicate_days, 
            weekly_tasks, 
            reminder.DAYNAMES
        )

    def test_convert_to_dictionary__returns_expected_with_text_before_first_day(self):
        weekly_tasks = [
            "some text", "Monday", "skiing", "Tuesday", "Wednesday", "Thursday", 
            "Friday", "Saturday", "Sunday", "snooker", "bins out"
            ]
        expected = {
            "Monday": "skiing\n", "Tuesday": "", "Wednesday": "",
            "Thursday": "", "Friday": "", "Saturday": "",
            "Sunday": "snooker\nbins out\n"
            }
        result = reminder.convert_to_dictionary(weekly_tasks, reminder.DAYNAMES)
        self.assertEqual(expected, result)

    def test_split_twice_on_comma__with_expected_data(self):
        data = [
            "Sep 18 2018, 4w, Example monthly task.", 
            "Oct 2 2018, 5d, Example task, written every 5 days."
            ]
        expected = [
            ["Sep 18 2018", "4w", "Example monthly task."], 
            ["Oct 2 2018", "5d", "Example task, written every 5 days."]
            ]
        result = reminder.split_twice_on_comma(data)
        self.assertEqual(expected, result)

    def test_split_twice_on_comma__with_less_commas(self):
        less_than_two_commas = [
            "Sep 18 2018 4w, Example monthly task.", 
            "Oct 2 2018, 5d Example task, written every 5 days."
            ]
        expected = [
            ["Sep 18 2018 4w", "Example monthly task."], 
            ["Oct 2 2018", "5d Example task", "written every 5 days."]
            ]
        result = reminder.split_twice_on_comma(less_than_two_commas)
        self.assertEqual(expected, result)

    def test_validate_three_items__two_items(self):
        two_items = ["Sep 18 2018 4w", "Example monthly task."]
        with self.assertRaises(IndexError):
            reminder.validate_three_items(two_items)

    def test_validate_three_items__three_items(self):
        three_items = ["Sep 18 2018", "4w", "Example monthly task."]
        self.try_or_fail(IndexError, reminder.validate_three_items, three_items)

    def test_validate_frequency__days(self):
        self.try_or_fail(ValueError, reminder.validate_frequency, "3d")

    def test_validate_frequency__weeks(self):
        self.try_or_fail(ValueError, reminder.validate_frequency, "2w")

    def test_validate_frequency__years(self):
        self.try_or_fail(ValueError, reminder.validate_frequency, "1y")

    def test_validate_frequency__two_durations(self):
        self.try_or_fail(ValueError, reminder.validate_frequency, "3w 12d")

    def test_validate_frequency__three_durations(self):
        self.try_or_fail(ValueError, reminder.validate_frequency, "1y 2w 3d")

    def test_validate_frequency__white_space(self):
        function = reminder.validate_frequency
        self.try_or_fail(ValueError, function, "    1d    3w   ")

    def test_validate_frequency__empty(self):
        duration = ""
        with self.assertRaises(ValueError):
            reminder.validate_frequency(duration)

    def test_validate_frequency__text_before(self):
        duration = "text before 3d"
        with self.assertRaises(ValueError):
            reminder.validate_frequency(duration)

    def test_validate_frequency__text_after(self):
        duration = "5d text after"
        with self.assertRaises(ValueError):
            reminder.validate_frequency(duration)
    
    def test_validate_frequency__missing_duration_type(self):
        duration = "3"
        with self.assertRaises(ValueError):
            reminder.validate_frequency(duration)

    def test_validate_frequency__missing_digit(self):
        duration = "d"
        with self.assertRaises(ValueError):
            reminder.validate_frequency(duration)

    def test_validate_frequency__zero_digit(self):
        duration = "0d"
        with self.assertRaises(ValueError):
            reminder.validate_frequency(duration)
    
    def test_validate_frequency__negative_digit(self):
        duration = "1y -1d"
        with self.assertRaises(ValueError):
            reminder.validate_frequency(duration)

    def test_validate_frequency__two_duration_indicators(self):
        duration = "3wd"
        with self.assertRaises(ValueError):
            reminder.validate_frequency(duration)

    def test_validate_frequency__duplicate_duration_indicators(self):
        duration = "2y 5y"
        with self.assertRaises(ValueError):
            reminder.validate_frequency(duration)

    def test_get_day_num__monday(self):
        dayname = "Monday"
        expected = 0
        result = reminder.get_day_num(dayname)
        self.assertEqual(expected, result)

    def test_get_day_num__saturday(self):
        dayname = "Saturday"
        expected = 5
        result = reminder.get_day_num(dayname)
        self.assertEqual(expected, result)

    def test_get_num_days_between__next_week(self):
        today = 6
        start_day = 0
        expected = 1
        result = reminder.get_num_days_between(today, start_day)
        self.assertEqual(expected, result)

    def test_get_num_days_between__same_day(self):
        today = 0
        start_day = 0
        expected = 0
        result = reminder.get_num_days_between(today, start_day)
        self.assertEqual(expected, result)

    def test_get_num_days_between__later_in_week(self):
        today = 2
        start_day = 4
        expected = 2
        result = reminder.get_num_days_between(today, start_day)
        self.assertEqual(expected, result)

    def test_get_future_date__zero_days(self):
        date = datetime.date(2020, 2, 23)
        days_to_target = 0
        expected = datetime.date(2020, 2, 23)
        result = reminder.get_future_date(date, days_to_target)
        self.assertEqual(expected, result)

    def test_get_future_date__five_days(self):
        date = datetime.date(2020, 2, 23)
        days_to_target = 5
        expected = datetime.date(2020, 2, 28)
        result = reminder.get_future_date(date, days_to_target)
        self.assertEqual(expected, result)

    def test_format_and_split__Wednesday(self):
        date = datetime.date(2020, 1, 15)
        expected = ["Wednesday", "15", "Jan"]
        result = reminder.format_and_split(date)
        self.assertEqual(expected, result)

    def test_format_and_split__Thursday(self):
        date = datetime.date(2020, 3, 19)
        expected = ["Thursday", "19", "Mar"]
        result = reminder.format_and_split(date)
        self.assertEqual(expected, result)

    def get_date_suffix_returns_expected(self):
        result = [str(i) + reminder.get_date_suffix(i) for i in range(1,32)]
        expected = [
            "1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th",
            "10th", "11th", "12th", "13th", "14th", "15th", "16th", "17th",
            "18th", "19th", "20th", "21st", "22nd", "23rd", "24th", "25th",
            "26th", "27th", "28th", "29th", "30th", "31st"
            ]
        self.assertEqual(expected, result)

    def test_to_readable__expected_output_unittest(self):
        get_suffix = Mock(return_value="th")
        date = datetime.date(2020, 4, 12)
        expected = "Sunday 12th Apr"
        with patch("reminder.get_date_suffix", get_suffix):
            result = reminder.to_readable(date)
        self.assertEqual(expected, result)

    def test_to_timedelta__days(self):
        duration = "3d"
        expected = datetime.timedelta(3)
        result = reminder.to_timedelta(duration)
        self.assertEqual(expected, result)

    def test_to_timedelta__weeks(self):
        duration = "2w"
        expected = datetime.timedelta(14)
        result = reminder.to_timedelta(duration)
        self.assertEqual(expected, result)

    def test_to_timedelta__years(self):
        duration = "1y"
        expected = datetime.timedelta(365)
        result = reminder.to_timedelta(duration)
        self.assertEqual(expected, result)

    def test_to_combined_timedelta__returns_converted_duration(self):
        duration = "12d"
        to_delta = Mock(return_value=datetime.timedelta(12))
        expected = datetime.timedelta(12)
        with patch("reminder.to_timedelta", to_delta):
            result = reminder.to_combined_timedelta(duration)
        self.assertEqual(expected, result)

    def test_to_combined_timedelta__adds_three_durations(self):
        duration = "1y 2w 3d"
        to_delta = Mock()
        to_delta.side_effect = [
            datetime.timedelta(365), 
            datetime.timedelta(14),
            datetime.timedelta(3)
            ]
        expected = datetime.timedelta(382)
        with patch("reminder.to_timedelta", to_delta):
            result = reminder.to_combined_timedelta(duration)
        self.assertEqual(expected, result)

    def test_to_combined_timedelta__still_matches_with_white_space(self):
        duration = "    1d    3w   "
        to_delta = Mock()
        to_delta.side_effect = [datetime.timedelta(1), datetime.timedelta(21)]
        expected = datetime.timedelta(22)
        with patch("reminder.to_timedelta", to_delta):
            result = reminder.to_combined_timedelta(duration)
        self.assertEqual(expected, result)
    
    def test_to_datetime_date__expected_input(self):
        date = "Jan 23 2020"
        expected = datetime.date(2020, 1, 23)
        result = reminder.to_datetime_date(date)
        self.assertEqual(expected, result)

    def test_to_datetime_date__halts_on_wrong_format(self):
        date = "December 14 2020"
        with self.assertRaises(ValueError):
            reminder.to_datetime_date(date)

    def test_to_string__may(self):
        date = datetime.date(2020, 5, 18)
        expected = "May 18 2020"
        result = reminder.to_string(date)
        self.assertEqual(expected, result)

    def test_to_string__sep(self):
        date = datetime.date(2020, 9, 5)
        expected = "Sep 05 2020"
        result = reminder.to_string(date)
        self.assertEqual(expected, result)

    def test_replace_date__overdue_task_unittest(self):
        to_combined_timedelta = Mock(return_value=datetime.timedelta(28))
        to_string = Mock(return_value="Jun 24 2020")
        date_frequency_task = ["Jun 3 2019", "4w", "Example task."]
        target = datetime.date(2020, 5, 27)
        expected = ["Jun 24 2020", "4w", "Example task."]
        with patch("reminder.to_combined_timedelta", to_combined_timedelta):
            with patch("reminder.to_string", to_string):
                result = reminder.replace_date(date_frequency_task, target)
        self.assertEqual(expected, result)

    def test_prepare_task_string__due_task(self):
        task = "task."
        date_str = "Dec 23 2019"
        dt_date = datetime.date(2019, 12, 23)
        target = datetime.date(2019, 12, 23)
        expected = "task.\n"
        result = reminder.prepare_task_string(task, date_str, dt_date, target)
        self.assertEqual(expected, result)

    def test_prepare_task_string__overdue_task(self):
        task = "task."
        date_str = "Dec 22 2019"
        dt_date = datetime.date(2019, 12, 22)
        target = datetime.date(2019, 12, 23)
        expected = "Old task detected. Was due on " \
                f"Dec 22 2019(1 days ago): task.\n"
        result = reminder.prepare_task_string(task, date_str, dt_date, target)
        self.assertEqual(expected, result)

    @patch("reminder.to_datetime_date")
    @patch("reminder.prepare_task_string")
    @patch("reminder.replace_date")
    def test_get_due_tasks_update_date__task_due_unittest(self, replace_date, prepare_task_string, to_datetime_date):
        to_datetime_date.return_value = datetime.date(2018, 9, 18)
        prepare_task_string.return_value = "Example monthly task.\n"
        replace_date.return_value = ["Oct 16 2018", "4w", "Example monthly task."]
        target = datetime.date(2018, 9, 18)
        tasks_by_date = [["Sep 18 2018", "4w", "Example monthly task."]]
        result_task_by_date, result_weeks_tasks = reminder.get_due_tasks_update_date(target, tasks_by_date)
        expected_tasks_by_date = [["Oct 16 2018", "4w", "Example monthly task."]]
        expected_weeks_tasks = "Example monthly task.\n"
        self.assertEqual(expected_tasks_by_date, result_task_by_date)
        self.assertEqual(expected_weeks_tasks, result_weeks_tasks)

    def test_replace_file_data__calls_write_method_on_location_file(self):
        mocked_open = mock_open()
        data = [["some\n"], ["text\n"]]
        location = "file.txt"
        with patch("reminder.open", mocked_open) as m:
            reminder.replace_file_data(location, data)
        m.assert_called_with("file.txt", "w")

    def test_create_output_file(self):
        mocked_open = mock_open()
        data = ["some\n", "text\n"]
        location = "file.txt"
        with patch("reminder.open", mocked_open) as m:
            reminder.create_output_file(location, data)
        m.assert_called_with("file.txt", "a")    