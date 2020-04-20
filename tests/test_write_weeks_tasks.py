import unittest
from unittest.mock import patch, mock_open

import write_weeks_tasks as reminder

class WriteWeeksTasksTest(unittest.TestCase):

    def test_get_file_data_halts_script_on_error(self):
        errors = [FileNotFoundError, PermissionError]
        for error in errors:
            # Create a MagicMock object using the mock_open helper function.
            mocked_open = mock_open()
            # Raise an exception when the mock is called.
            mocked_open.side_effect = error
            # Patch replaces the target, open() method, with the mocked_open.
            with patch("builtins.open", mocked_open):
                # Call the function and check exception wasn't consumed by a try/except.
                with self.assertRaises(error):
                    reminder.get_file_data("filename")

    def test_get_file_data__expected_output(self):
        mocked_data = "multi\nline\n\ndata\n"
        mocked_open = mock_open(read_data=mocked_data)
        with patch("builtins.open", mocked_open):
            result = reminder.get_file_data("filename")
        expected = ['multi\n', 'line\n', '\n', 'data\n']
        self.assertEqual(result, expected)

    def test_strip_line_endings__removes_line_endings_and_paragraphs(self):
        weekly_tasks = [
            'some text\n', '\n', 'Monday\n', 'skiing\n', '\n', 'Tuesday\n',
            '\n', 'Wednesday\n', '\n', 'Thursday\n', 'Friday\n', '\n', 
            'Saturday\n', '\n', 'Sunday\n', 'snooker\n', 'bins out\n'
            ]
        expected = [
            'some text', 'Monday', 'skiing', 'Tuesday', 'Wednesday',
            'Thursday', 'Friday', 'Saturday', 'Sunday', 'snooker', 'bins out'
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

    def test_convert_to_dictionary__returns_expected_with_text_before_first_day(self):
        weekly_tasks = [
            "some text", "Monday", "skiing", "Tuesday", "Wednesday", "Thursday", 
            "Friday", "Saturday", "Sunday", "snooker", "bins out"
            ]
        expected = {
            'Monday': 'skiing\n', 'Tuesday': '', 'Wednesday': '',
            'Thursday': '', 'Friday': '', 'Saturday': '',
            'Sunday': 'snooker\nbins out\n'
            }
        result = reminder.convert_to_dictionary(weekly_tasks, reminder.DAYNAMES)
        self.assertEqual(expected, result)

