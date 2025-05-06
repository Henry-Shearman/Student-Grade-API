#!/bin/bash

db_name=$DB_NAME #Assign a name for application database from environment variable.
db_username=$DB_USERNAME #Assign the username for application database from environment variable. Should be current user.
db_password=$DB_PASSWORD #Assign password for user in application database from environment variable.


#Create dummy student grade data
python3 create_dummy_data.py
mv StudentDummyData.csv /tmp
sudo chmod 444 /tmp/StudentDummyData.csv


#Create database and user provisions
sudo -u postgres dropdb --if-exists $db_name
sudo -u postgres createdb $db_name

echo "${db_name} database created"

sudo -u postgres psql -c "CREATE USER ${db_username} WITH PASSWORD '${db_password}';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE ${db_name} TO ${db_username};"
sudo -u postgres psql -c "GRANT pg_read_server_files TO ${db_username};"
psql -U $db_username -d $db_name -c "CREATE SCHEMA class AUTHORIZATION ${db_username};"

echo "All privileges granted for user ${db_username} on ${db_name} database"


#Create and load data warehouse from SQL script
psql -U $db_username -d $db_name -f "LoadStudentGrades.sql"

rm -f /tmp/StudentDummyData.csv
