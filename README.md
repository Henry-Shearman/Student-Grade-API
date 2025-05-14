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
