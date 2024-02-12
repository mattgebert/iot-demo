# iot-demo
Demo app for job interview

## Setup

Use FastAPI dependencies:

'''
pip install fastapi "uvicorn[standard]"

'''

## [main.py](main.py)

As per the FastAPI demo this application can be launched using:

'''
uvicorn main:app --reload
'''

## [data_acquisition.py](data_acquisition.py)

Simulated sensor generation of data into a CSV format. 
Run as a dedicated process with "python <path-to-app>/data_acquisition.py"
Generates files into a subfolder "data". Creates folder if it doesn't exist.
Filenames are formatted as "./data/YYYYMMDD-temp_pres_data.csv".