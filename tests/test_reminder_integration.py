import unittest
from unittest.mock import patch, mock_open

import write_weeks_tasks as reminder

class WriteWeeksTasksIntegrationTest(unittest.TestCase):
    
    def test_get_weekly_tasks_as_dictionary__returns_expected(self):
        weekly_tasks = 'some text\n\nMonday\nskiing\n\nTuesday\n\nWednesday' \
            '\n\nThursday\nFriday\n\nSaturday\n\nSunday\nsnooker\nbins out\n'
        mocked_open = mock_open(read_data=weekly_tasks)
        with patch("builtins.open", mocked_open):
            result = reminder.get_weekly_tasks_as_dictionary("filename", reminder.DAYNAMES)
        expected = {
            'Monday': 'skiing\n', 'Tuesday': '', 'Wednesday': '',
            'Thursday': '', 'Friday': '', 'Saturday': '',
            'Sunday': 'snooker\nbins out\n'
            }
        self.assertEqual(result, expected)