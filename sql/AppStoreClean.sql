/*******************

  Cleaning script

*******************/

DROP TABLE IF EXISTS calculators CASCADE;
DROP TABLE IF EXISTS loan CASCADE;
DROP TABLE IF EXISTS students CASCADE;
DROP TABLE IF EXISTS locations CASCADE;
DROP FUNCTION IF EXISTS transformed_time(arg INTEGER);
