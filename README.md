# Student Grade API

## Description
This repository creates and populates a simple PostgreSQL data warehouse with dummy student grade data and serves the data with a basic REST API interface. 
The data warehouse is contained completely within the "Class" schema contains two dimension tables: DimStudent and DimCourse which are automatically updated using triggers from the inserted data in the landing table.
This data warehouse has been designed to implement type 0 slowly changing dimensions which are immutable and do not change upon insertion of new matching records.<br />

The FactGrades table is also updated from the landing table via triggers and contains both numeric and academic grade entries for each student and course, supporting incremental or batch loading of new grade data. 
Batch data must be timestamped for which the latest available record will be used to update the user grades. <br />

The API offers searching, scaling, summary statistics and insertion functionalities via its standard endpoints. Each endpoint has been documented in the Endpoints.md file. 
The Flask server used to test the API in this project is a testing server and a WSGI should be configured for a production server to deploy the API in an application setting.

## Installation Instructions
The following installation instructions are for an Ubuntu system with requirements specified in the requirements.txt file:

### Step 1: Clone the Repository
Use the code below to clone the repository to the current directory:
```sh
git clone https://github.com/Henry-Shearman/Student-Grade-API.git
```
### Step 2: Create a Virtual Environment
Use the code below to create a virtual environment for the project in the current directory:
```sh
python3 -m venv Student_Grade_API_venv
```
### Step 3: Install Python Packages
Install the required python packages into the virtual environment using the code below: 
```sh
source Student_Grade_API_venv/bin/activate;
pip install Flask==3.1.0 names==0.3.0 numpy==2.2.5 pandas==2.2.3 psycopg2-binary==2.9.10;
deactivate
```

The project dependencies are now installed into the virtual environment and the project is ready to use.

## Usage Instructions

### Step 1: Activate the Virtual Environment
Use the command below to activate the virtual environment:
```sh
source Student_Grade_API_venv/bin/activate
```

### Step 2: Initialise Database Environment Variables
Insert the necessary details into the code below to initialise the database environment variables
```sh
export DB_NAME=studentgradesdb;
export DB_USERNAME=$USER;
export DB_PASSWORD="Insert user password";
export DB_HOSTNAME="Insert database hostname"
```

### Step 3: Create and Populate Data Warehouse with Dummy Data
Navigate to the Student-Grade-API directory and run the create_and_populate_DW.sh script using the commands below:
```sh
cd Student-Grade-API;
sudo chmod 700 create_and_populate_DW.sh;
./create_and_populate_DW.sh
```

Then enter the desired number of students into the displayed prompt. An example for 10 students is shown below:
```
Enter number of dummy students: 10
```

You will then be prompted for the root password. If entered successfully, the following should appear in the last line of the output for the 10 student example shown above:
```
COPY 70
```

This indicates that 70 grades have been successfully ingested into the data warehouse.

### Step 4: Run the API on the Flask Testing Server
Finally, start the test server locally using the following command:
```
python3 API.py
```

The server will now be running on localhost using the default port of 5000. Use the endpoints detailed in the Endpoints.md file to call the API.
