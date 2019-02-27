import unittest
from unittest.mock import patch
import work_log

from peewee import *


class TestWorklog(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from work_log import Entry
        db = SqliteDatabase('work_log.db')
        db.connect()
        db.create_tables([Entry], safe=True)

    def test_add_entry(self):
        from work_log import add_entry
        test_entry = add_entry('Test Name', 'Test Title', '2', 'Test Notes')
        self.assertEqual(test_entry.employee_name, 'Test Name')
        test_entry.delete_instance()

    def test_get_unique_employees(self):
        from work_log import get_unique_employees, add_entry
        test_entry = add_entry('Test Name', 'Test Title', '2', 'Test Notes')
        unique_names = get_unique_employees()
        self.assertTrue(unique_names)
        test_entry.delete_instance()

    def test_get_unique_dates(self):
        from work_log import get_unique_dates, add_entry
        test_entry = add_entry('Test Name', 'Test Title', '2', 'Test Notes')
        unique_dates = get_unique_dates()
        self.assertTrue(unique_dates)
        test_entry.delete_instance()

    def test_validate_name_input(self):
        from work_log import validate_name_input
        self.assertTrue(validate_name_input('Jeremy'))
        self.assertFalse(validate_name_input(''))
        self.assertFalse(validate_name_input('Jeremy_Nootenboom'))
        self.assertFalse(validate_name_input('123'))

    def test_validate_title_input(self):
        from work_log import validate_title_input
        self.assertTrue(validate_title_input('Task'))
        self.assertFalse(validate_title_input(''))

    def test_validate_duration_input(self):
        from work_log import validate_duration_input
        self.assertTrue(validate_duration_input('90'))
        self.assertFalse(validate_duration_input('90 minutes'))
        self.assertFalse(validate_duration_input('Two'))

    def test_validate_notes_input(self):
        from work_log import validate_notes_input
        self.assertEqual(validate_notes_input('Some notes'), 'Some notes')
        self.assertEqual(validate_notes_input(''), 'None')

    def test_validate_employee_search_format(self):
        from work_log import validate_employee_search_format
        self.assertTrue(validate_employee_search_format('Jeremy'))
        self.assertFalse(validate_employee_search_format(''))

    def test_validate_date_search_format(self):
        from work_log import validate_date_search_format
        self.assertTrue(validate_date_search_format('12/30/1991'))
        self.assertFalse(validate_date_search_format('30/12/1991'))

    def test_validate_duration_search_format(self):
        from work_log import validate_duration_search_format
        self.assertTrue(validate_duration_search_format('90'))
        self.assertFalse(validate_duration_search_format('Two'))

    def test_validate_term_search_format(self):
        from work_log import validate_term_search_format
        self.assertTrue(validate_term_search_format('Stuff'))
        self.assertFalse(validate_term_search_format(''))

    def test_work_log_add_entry_call(self):
        user_input = ['a', 'c', 'ignored value']
        with patch('builtins.input', side_effect=user_input):
            with patch('work_log.new_entry') as new_entry_patch:
                with self.assertRaises(SystemExit):
                    work_log.work_log()
            new_entry_patch.assert_called_once_with()


if __name__ == '__main__':
    unittest.main()
