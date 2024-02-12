import numpy as np
import datetime, os
import time
import asyncio

TEMPERATURE_MU = 18
TEMPERATURE_SIG = 0.1
DATA_HEADERS = ["Datetime (UTC)", "Temperature (deg C)", "Pressure (hPa)"]
DATA_SAVE_PATH = os.path.join(os.getcwd(), "data") # Specify something more static

def acquireData(data_save_path):
    # Acquire time
    t = datetime.datetime.now(datetime.timezone.utc)
    date_string = f'{t:%Y%m%d}'
    datetime_string = f'{t:%Y%m%d_%H%M%S}'
    
    # Generate random sensor acquisition (ie voltage):
    meas_temp = np.random.normal(TEMPERATURE_MU, TEMPERATURE_SIG, 1)[0] #get single element.
    
    # Add something interesting - heatup during day and cooldown during night.
    # Assume sunrise 8am.
    tt = t.time()
    SECS_PER_DAY = 24*60*60
    SUNRISE = datetime.time(8,0)
    secs_now = tt.hour * 60 * 60 + t.minute * 60 + t.second
    secs_sunrise = SUNRISE.hour * 60
    secs_daydelta = (secs_now - secs_sunrise) % SECS_PER_DAY
    meas_temp += 10 * np.sin(2*np.pi * secs_daydelta / SECS_PER_DAY)
    
    # Generate random pressure acquisition:
    meas_pres = np.random.normal(1008, 5, 1)[0] #get single element.
    
    # Check if dir exists:
    if not os.path.exists(data_save_path):
        os.mkdir(data_save_path)
    
    # Check if relevant file exists, otherwise create:
    dpath = os.path.join(data_save_path, date_string + "-temp_pres_data.csv")
    if not os.path.exists(dpath):
        with open(dpath, 'w') as newfile:
            for header in DATA_HEADERS[:-1]:
                newfile.write(header)
                newfile.write(",")
            newfile.write(DATA_HEADERS[-1])
            newfile.write("\n")
    
    # Generate data grouping 
    writable_data = [datetime_string, f'{meas_temp:.{2}f}', f'{meas_pres:.{2}f}']
    
    # Open Existing / Created file.
    with open(dpath, 'a') as datafile:
        for data in writable_data[:-1]:
            datafile.write(data)
            datafile.write(",")
        datafile.write(writable_data[-1])
        datafile.write("\n")
    return

async def app():
    acquireData(DATA_SAVE_PATH)
    await asyncio.sleep(3)

if __name__ == "__main__":
    while True:
        asyncio.run(app())