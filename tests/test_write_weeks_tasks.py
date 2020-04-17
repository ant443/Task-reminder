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

    def test_get_file_data_expected_output(self):
        mocked_data = "multi\nline\n\ndata\n"
        mocked_open = mock_open(read_data=mocked_data)
        with patch("builtins.open", mocked_open):
            result = reminder.get_file_data("filename")
        expected = ['multi\n', 'line\n', '\n', 'data\n']
        self.assertEqual(result, expected)