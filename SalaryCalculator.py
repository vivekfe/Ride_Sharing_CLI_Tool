import sqlite3
from DataBaseManager import DatabaseManager
import os
import win32file
from utils import pretty_print
from pathlib import Path
from typing import Union
pathtype = Union[str, Path]

local_storage: str = "driver_payments.db"
current_path: pathtype = os.path.dirname(os.path.abspath(__file__))
driver_storage: pathtype = win32file.GetFullPathName(os.path.abspath(os.path.join(current_path, local_storage)))


class SalaryCalculator(object):
    def __init__(self):
        pass

    def call_dispatcher(self, **call_args):
        operation_type: str = call_args['operation_type']
        ride_date: str = call_args['ride_date'] if call_args['ride_date'] is not None else None
        driver_id: int = call_args['driver_id'] if call_args['driver_id'] is not None else None
        ride_id: int = call_args['ride_id'] if call_args['ride_id'] is not None else None
        time_taken: int = call_args['time_taken'] if call_args['time_taken'] is not None else None
        distance: int = call_args['distance'] if call_args['distance'] is not None else None
        rating: int = call_args['rating'] if call_args['rating'] is not None else None
        period_start: str = call_args['period_start'] if call_args['period_start'] is not None else None
        period_end: str = call_args['period_end'] if call_args['period_end'] is not None else None
        if operation_type == 'ride_finished':
            self.ride_finished(ride_date, driver_id, ride_id, time_taken, distance)
        if operation_type == 'rating_submitted':
            self.rating_submitted(driver_id, ride_id, rating)
        if operation_type == 'driver_payment':
            self.calculate_driver_payment(driver_id, period_start, period_end)

    @staticmethod
    def ride_finished(ride_date: str, driver_id: int, ride_id: int, time_taken: int, distance: int) -> None:
        try:
            db_manager = DatabaseManager(driver_storage)
            db_connection = db_manager.connect_to_db()
            cur = db_connection.cursor()
            cur.execute(
                "INSERT INTO RIDE_DETAILS (ride_date, driver_id, ride_id, time_taken, distance) VALUES (?, ?, ?, ?, ?)",
                (ride_date, driver_id, ride_id, time_taken, distance))
            db_connection.commit()
            cur.close()
            pretty_print('Inserted a new record in DB')
        except sqlite3.Error as e:
            pretty_print(f'Failed to insert ride details with error {e}')

        finally:
            if db_connection is not None:
                db_connection.close()
                pretty_print("Closing the existing connection\n" + "/" * 60)
                return None

    @staticmethod
    def rating_submitted(driver_id: int, ride_id: int, rating: int) -> None:
        try:
            db_manager = DatabaseManager(driver_storage)
            db_connection = db_manager.connect_to_db()
            cur = db_connection.cursor()
            cur.execute("INSERT INTO DRIVER_RATING (driver_id, ride_id, rating) VALUES (?,?,?)",
                        (driver_id, ride_id, rating))
            db_connection.commit()
            cur.close()
            pretty_print('Inserted a new record in DB')
        except sqlite3.Error as e:
            pretty_print(f'Failed to insert ride details with error {e}')

        finally:
            if db_connection is not None:
                pretty_print("Closing the existing connection\n" + "/" * 60)
                db_connection.close()
                return None

    @staticmethod
    def calculate_driver_payment(driver_id: int, period_start: str, period_end: str) -> int:
        try:
            db_manager = DatabaseManager(driver_storage)
            db_connection = db_manager.connect_to_db()
            cur = db_connection.cursor()
            cur.execute("SELECT COUNT(rating) AS COUNT_HIGH_RATINGS FROM DRIVER_RATING WHERE driver_id=(?) and rating=5 ", (driver_id,))
            rows = cur.fetchall()
            count_top_rating = rows[0][0]
            cur.execute(
                "SELECT SUM(distance) AS DISTANCE, SUM(time_taken) AS TIME_TAKEN FROM RIDE_DETAILS WHERE driver_id= (?) AND ride_date >=(?) AND ride_date<=(?)",
                (driver_id, period_start, period_end))
            rows = cur.fetchall()
            total_distance_covered: int = rows[0][0]
            total_minutes_driven: int = rows[0][1]
            basic_payment: int = total_distance_covered * 1 + (total_minutes_driven / 5) * 1
            additional_payment: int = count_top_rating
            total_payment: int = basic_payment + additional_payment
            cur.close()
            db_connection.close()
            pretty_print(
                f"Calculate driver payment for Driver ID: {driver_id} between {period_start} and"
                f" {period_end} is USD {total_payment}\n" + "/" * 60)
            # return value could be float as well however challenge expected the output to be an integer
            return int(total_payment)

        except sqlite3.Error as e:
            pretty_print(f'Failed to insert ride details with error {e}')
