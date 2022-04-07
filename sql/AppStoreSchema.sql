
/*******************

  Create the schema

********************/

CREATE TABLE IF NOT EXISTS locations(
location_id INT PRIMARY KEY,
location_name VARCHAR(64) NOT NULL);

CREATE TABLE IF NOT EXISTS students(
email VARCHAR(64) PRIMARY KEY,
first_name VARCHAR(64) NOT NULL,
last_name VARCHAR(64) NOT NULL,
pass VARCHAR(64) NOT NULL,
admin_rights BOOLEAN DEFAULT FALSE,
time_availability INT CHECK (time_availability >= 0 AND 2359 >= time_availability),
number_of_transaction INT DEFAULT 0,
location_id INT REFERENCES locations(location_id) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE IF NOT EXISTS calculators(
brand VARCHAR(32),
serial_number VARCHAR(32),
calc_type VARCHAR(64) NOT NULL CHECK (calc_type = 'scientific' OR calc_type = 'graphing' OR calc_type = 'financial'),
price INT,
calc_condition VARCHAR(64),
availability VARCHAR(64) NOT NULL CHECK (availability = 'available' OR availability = 'not available'),
email VARCHAR(64) REFERENCES students(email) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED,
PRIMARY KEY (brand, serial_number));

CREATE TABLE IF NOT EXISTS loan(
loan_id INT PRIMARY KEY,
loan_time INT NOT NULL,
return_time INT NOT NULL,
owner_email VARCHAR(64) NOT NULL REFERENCES students(email) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED,
borrower_email VARCHAR(64) NOT NULL REFERENCES students(email) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED,
loan_location_id INT NOT NULL REFERENCES locations(location_id) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED,
return_location_id INT NOT NULL REFERENCES locations(location_id) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED,
brand VARCHAR(32),
serial_number VARCHAR(32),
FOREIGN KEY (brand, serial_number) REFERENCES calculators(brand, serial_number) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE IF NOT EXISTS test_students(
id INT PRIMARY KEY,
time INT,
location_id INT REFERENCES locations(location_id) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED);

