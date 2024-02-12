# iot-demo
Demo app for job interview, via Ubuntu OS and tested in Firefox.

## Setup

Use FastAPI dependencies:

    pip install fastapi "uvicorn[standard]"
    
## [main.py](main.py)

As per the FastAPI demo this application can be launched using:

    uvicorn main:app --reload

## [data_acquisition.py](data_acquisition.py)

Simulated sensor generation of data into a CSV format. 

Run as a dedicated process with "python <path-to-app>/data_acquisition.py"

Generates files into a subfolder "data". Creates folder if it doesn't exist.

Filenames are formatted as "./data/YYYYMMDD-temp_pres_data.csv".

## [webinterface.html](webinterface.html)

Static page, running Plotly graphing library.

Calls to local host to recieve updated JSON data.

Currently, have not fixed bug for Plotly updating with JSON packets, but can recieve (see console for log).

May require enabling of CORS (Cross-Origin Resource Sharing), by default disabled/blocked in Firefox.
