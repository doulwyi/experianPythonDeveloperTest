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
import argparse
import calendar
import csv
import datetime
import os

import numpy as np


class Transactions:

    def __init__(self, csv_file):
        # This variable collects and saves all data from csv once for better performance.
        self.raw_data = parse_csv_file(csv_file)

    def first_type(self):
        """
        Transactions with same description, amount, and regularly-spaced dates
        :return: Creates a CSV file called transcation1.csv where contains all data needed.
        """
        data = find_indexes(self.raw_data)
        with open('transaction1.csv', "w+") as csvfile:
            csv_w = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for i in data.keys():
                # Convert numpay array to python list.
                array_to_list = data[i].tolist()
                new_list = list()
                # Runs through indexes and create a new list of transactions.
                for j in range(0, len(array_to_list), 1):
                    new_list.append((self.raw_data[array_to_list[j]][0], self.raw_data[array_to_list[j]][1],
                                     self.raw_data[array_to_list[j]][2]))
                if check_equal_price(new_list):
                    for i in new_list:
                        csv_w.writerow(i)

    def second_type(self):
        """
         Transactions with same description and amount, and dates that correspond to only the last Friday of each month.
         :return: Creates a CSV file called transcation2.csv where contains all data needed.
         """
        data = find_indexes(self.raw_data)
        with open('transaction2.csv', "w+") as csvfile:
            csv_w = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for i in data.keys():
                # Convert numpay array to python list.
                array_to_list = data[i].tolist()
                new_list = list()
                # Runs through indexes and create a new list of transactions.
                for j in range(0, len(array_to_list), 1):
                    new_list.append((self.raw_data[array_to_list[j]][0], self.raw_data[array_to_list[j]][1],
                                     self.raw_data[array_to_list[j]][2]))
                if check_equal_price(new_list):
                    for i in new_list:
                        if get_last_friday(i[0]):
                            csv_w.writerow(i)


def parse_csv_file(path_):
    """
    Simple csv parser.
    :param path_: String: Path to csv
    :return: A matrix with all data.
    """
    with open(path_) as csvfile:
        c = csv.reader(csvfile, delimiter=',')
        infos_list = list(map(list, c))
    return infos_list


def find_indexes(infos_list):
    """
    This function reads the matrix data and filters transactions with same price and name and save its indexes.
    :param infos_list:
    :return: Dict: Transaction Name : Array with indexes
    """
    value = np.array(infos_list)
    main_dict = dict()
    for i in range(len(infos_list)):
        transaction = (infos_list[i][1])
        if transaction != 'description':
            rows, cols = np.where(value == transaction)
            main_dict.update({transaction: rows})
    return main_dict


def check_equal_price(iterator):
    """
    Given a list of prices, this functions checks whether is the same price.
    :param iterator: List: List of prices
    :return: Boolean
    """
    prices = list()
    for price in iterator:
        prices.append(price[2])

    iterator = iter(prices)
    try:
        first = next(iterator)
    except StopIteration:
        return True
    return all(first == rest for rest in iterator)


def get_last_friday(date_):
    """
    Get las friday of given month and year.
    :param date_: String: date
    :return: Boolean
    """
    # Some of date from csv are in the correct format so this code will make sure that
    # all data will be processed.
    try:
        date_ = datetime.datetime.strptime(date_, "%d/%m/%Y").date()
    except:
        date_ = datetime.datetime.strptime(date_, "%m/%d/%Y").date()
    day = date_.day
    month = date_.month
    year = date_.year
    cal = calendar.monthcalendar(year, month)
    # Checks if month has 30 days or not.
    last_friday = cal[4][4] if cal[4][4] > 0 else cal[3][4]
    if day == last_friday:
        return True
    return False


def is_dir(dirname):
    """Checks if a path is an actual directory"""
    if not os.path.isdir(dirname):
        msg = "{0} is not a directory".format(dirname)
        raise argparse.ArgumentTypeError(msg)
    else:
        return dirname


if __name__ == '__main__':

    """Small CLI to execute all transactions."""

    parser = argparse.ArgumentParser(description='Process Transactions from csv')
    parser.add_argument('-t1', help='Proceed with transaction 1')
    parser.add_argument('-t2', help='Proceed with transaction 2')
    parser.add_argument('-path', help='Path to csv file.', type=is_dir, required=True)

    args = parser.parse_args()

    t = Transactions(args.path)

    if args.t1:
        t.first_type()
    if args.t2:
        t.second_type()
