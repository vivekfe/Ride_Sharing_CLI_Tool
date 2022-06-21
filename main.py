from DataBaseManager import DatabaseManager
from SalaryCalculator import SalaryCalculator
import os
import argparse
from utils import pretty_print
import win32file

parser = argparse.ArgumentParser()
parser.add_argument('--operation_type', help="operation type to be performed", type=str, required=True)
parser.add_argument('--ride_date', help="date at which ride was taken", type=str, default=None)
parser.add_argument('--driver_id', help="ID Number of the driver", type=int, default=None)
parser.add_argument('--ride_id', help="ID Number of the ride", type=int, default=None)
parser.add_argument('--time_taken', help="time taken to finish the ride", type=int, default=None)
parser.add_argument('--distance', help="total distance covered in the ride", type=int, default=None)
parser.add_argument('--rating', help="rating given by customer", type=int, default=None)
parser.add_argument('--period_start', help="start of the duration, usually start of the month", type=str, default=None)
parser.add_argument('--period_end', help="end of the duration, usually end of the month", type=str, default=None)

command_args = parser.parse_args()
operation_type = command_args.operation_type
ride_date = command_args.ride_date
driver_id = command_args.driver_id
ride_id = command_args.ride_id
time_taken = command_args.time_taken
distance = command_args.distance
rating = command_args.rating
period_start = command_args.period_start
period_end = command_args.period_end
local_storage = "driver_payments.db"

current_path = os.path.dirname(os.path.abspath(__file__))
driver_storage = win32file.GetFullPathName(os.path.abspath(os.path.join(current_path, local_storage)))


def main():
    pretty_print('Local Storage Initializer.')
    _ = DatabaseManager(driver_storage)
    salary_operations = SalaryCalculator()
    salary_operations.call_dispatcher(operation_type=operation_type,
                                      ride_date=ride_date,
                                      driver_id=driver_id,
                                      ride_id=ride_id,
                                      time_taken=time_taken,
                                      distance=distance,
                                      rating=rating,
                                      period_start=period_start,
                                      period_end=period_end)


if __name__ == '__main__':
    main()
