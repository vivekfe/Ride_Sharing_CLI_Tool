# PyQuant Exercise 2022

Python Take Home exercise for Bank's 2022 Test for New Quant Dev Candidates.

## Project Description

This utility has been written for calculating monthly driver payments for a raide hailing company which has implemented a new system for calculating payroll.

# Rules for calculating Payments

•	Customers may subsequently submit a rating of 1-5 stars after each ride.
•	The basic payment is $1 per 5 minutes plus $1 per km. Drivers receive an additional $1 for every 5 stars they are awarded cumulatively.
•	Driver pay is calculated monthly.

# How to use this utility ?

As of the date of completion of this utility, author used  **Python 3.8.5** on win32 however since this does use any system calls, this utility should run on any other platform as well.

To use this, Unzip the file directly and it should result in a folder **pyquant-exercise-2022**.
Open this project into Pycharm or any other Python IDE. **Main.py** file implements the usage of this file.

If you are using a virtual environment, then please make sure below modules are installed or else install them using pip.

**pip install win32file
pip install sqlite3
pip install argparse** 

As the challenge provided 3 commands already as test cases, use below 3 commands, which can be run using Pycharm terminal if the working directory is alread set. Below comnmands are replica of commands provided in test case file however with an added feature of providing named arguments from command line.

**python main.py --operation_type ride_finished --ride_date 2022-01-01 --driver_id 1 --ride_id 1 --time_taken 5  --distance 2**

**python main.py --operation_type rating_submitted --driver_id 1 --ride_id 1 --rating 5**

**python main.py --operation_type driver_payment --driver_id 1 --period_start 2022-01-01 --period_end 2022-01-31**


##Tree Structure 

![image](https://user-images.githubusercontent.com/435616/174783563-515d85c3-1b1a-441b-9294-3b366fb1fcb9.png)

This utility structures the code in a very logical manner.

**main.py** -> This is the file which can be used for running the actual utility using commands provided above in "How to use this utility"

**DataBaseManager.py** -> This class has an implementation of operations such as creation of database tables (if it does not exist in user's machine), connection to local DB and closing any connections to avoid memory leakage.

**utils.py** -> consists only a minor implementation of pretty_print which prints statements with a better formatting to keep things user friendly on command line.

**SalaryCalculator.py** -> This file consists of a class which implements static methods for performing operations such as insertion of ride details, driver ratings and driver payment's calculation.

##Type Hints 

Type hints have been provided in each class/method of the files in this utility so the code is self explanatory however for any doubts, please refer to this **README.md** file.

##How does Main.py takes care of variable number of arguments

Main.py is capable of receiving variable number of arguments from the user and uses **argparse** module to recieve commmand line arguments and uses a dispatcher to pass these to appropriate static methods of the  **SalaryCalculator** class.

Rationale for using static method was to keep things simple as these methods do not need to access any object specific attributes and are sufficient to perform operations on DB without any object dependency.


##What about the storage?

Since calculation of driver's payments depend on earlier ratings submitted by customers and parameters such as distance covered along with duration of trip, these details needed to persist in a storage. For this sake of simplicity, we have chosen local sqlite file which has 2 tables. Below is the schema for these tables

CREATE TABLE "DRIVER_RATING" (
	"driver_id"	INTEGER,
	"ride_id"	INTEGER NOT NULL,
	"rating"	INTEGER,
	PRIMARY KEY("ride_id")
);

CREATE TABLE "RIDE_DETAILS" (
	"ride_date"	TEXT,
	"driver_id"	INTEGER,
	"ride_id"	INTEGER NOT NULL,
	"time_taken"	INTEGER,
	"distance"	INTEGER,
	PRIMARY KEY("ride_id")
);

Whenever the main.py is executed by the user, utility checks if a local storage exists already or not. If it does not, then a database file is created automatically and saved on disk with appropriate tables. For the sake of simplicity, we are saving the DB file in the project folder itself.

##Unittests

Project folder also consists of unittests and to run these tests, we can directly use Pycharm's functionality to run the tests. One of the caveat's with unit tests is that it can fail if the database does not exist. In such case, if user enters commands in section **# How to use this utility ?**, then few sample enteries will be created and re-execution of the unitests will not result in failure.


##Assumptions

Since this DRIVER_RATING table does not have ride details so each time driver's payment calculation is done, it searches for all the instances when driver has been given rating of 5 irrespective of the month so in essence the driver is compensated for all his historical ratings as well each month. The advantage of such system is- better driver's rating is, better his/her compensation which can result increasing the service quality of car hailing company.
