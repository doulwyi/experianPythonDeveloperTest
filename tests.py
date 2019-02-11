import csv
import os
import unittest

from main import Transactions
from main import get_last_friday, parse_csv_file, check_equal_price, find_indexes

"""
Imagine, you are given the following (synthetic) dataset, comprising a person’s bank account transactions. 
We would like you to write Python code that identifies the following subsets of transactions:

    1. Transactions with same description, amount, and regularly-spaced dates 
    2. Transactions with same description and amount, and dates that correspond to only the last Friday of each month.

Date regularity can be weekly, monthly, and fortnightly.
Very importantly, imagine the above code is meant for deployment to production. What would your standards be?

You have 5 days to complete the assignment. 
Please send us your code along with a set of CSVs containing the transactions corresponding to each of the 
above categories (as identified by your code).

Please do not share the test or its data with anyone. 
"""


class MainTest(unittest.TestCase):

    def setUp(self):
        self.path_to_csv_example = 'Python_Developer_Test.csv'
        self.data_example = [['12/01/2018', 'CLEANING', '50'],
                             ['26/01/2018', 'CLEANING', '50'],
                             ['09/02/2018', 'CLEANING', '50'],
                             ['02/23/2018', 'CLEANING', '50'],
                             ['09/03/2018', 'CLEANING', '50']]
        self.t = Transactions(self.path_to_csv_example)

    def test_csv_exists(self):
        self.assertTrue(os.path.isfile(self.path_to_csv_example))

    def test_csv_has_contents(self):
        c = parse_csv_file(self.path_to_csv_example)
        self.assertGreater(len(c), 0)

    def test_check_last_friday_correct_format(self):
        date = '26/01/2018'  # Last friday in Jan 2018 (dd/mm/yyyy)
        self.assertTrue(get_last_friday(date))

    def test_check_last_friday_wrong_format(self):
        date = '01/26/2018'  # Last friday in Jan 2018 (mm/dd/yyyy)
        self.assertTrue(get_last_friday(date))

    def test_check_last_friday_wrong_date(self):
        date = '27/01/2018'  # This is not the last friday.
        self.assertFalse(get_last_friday(date))

    def test_check_equal_price(self):
        lst_prices = [['20/04/2018', 'CLEANING', '50'], ['04/05/2018', 'CLEANING', '50'],
                      ['18/05/2018', 'CLEANING', '50']]
        self.assertTrue(check_equal_price(lst_prices))

    def test_check_different_price(self):
        lst_prices = [['20/04/2018', 'CLEANING', '51'], ['04/05/2018', 'CLEANING', '52'],
                      ['18/05/2018', 'CLEANING', '50']]
        self.assertFalse(check_equal_price(lst_prices))

    def test_find_indexes(self):
        expected = [0, 1, 2, 3, 4]
        result = find_indexes(self.data_example)
        res = result['CLEANING'].tolist()
        self.assertIsInstance(result, dict)
        self.assertEqual(expected, res)

    def test_first_transaction(self):
        self.t.first_type()
        self.assertTrue(os.path.isfile('transaction1.csv'))

    def test_first_transaction_contains_data(self):
        self.t.first_type()
        with open('transaction1.csv') as csvfile:
            c = csv.reader(csvfile, delimiter=',')
            result = list(map(list, c))
            self.assertIn('CLEANING', result[0])

    def test_second_transaction(self):
        self.t.second_type()
        self.assertTrue(os.path.isfile('transaction2.csv'))

    def test_seccond_transaction_contains_data(self):
        self.t.second_type()
        with open('transaction2.csv') as csvfile:
            c = csv.reader(csvfile, delimiter=',')
            result = list(map(list, c))
            self.assertIn('CLEANING', result[0])


if __name__ == "__main__":
    unittest.main()
