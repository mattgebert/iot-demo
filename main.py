from fastapi import FastAPI
from pydantic import BaseModel
import datetime, os
import numpy as np
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware

DATA_SAVE_PATH = os.path.join(os.getcwd(), "data") # Specify something more static

app = FastAPI()

origins = ["*"]

# origins = [
#     "http://localhost",
#     "http://localhost:8000",
#     "http://127.0.0.1"
#     "http://127.0.0.1:8000",
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# class Item(BaseModel):
#     name: str
#     price: float
#     is_offer: bool | None = None

# @app.get("/")
# async def read_root():
#     return {"Hello":"World"}

# @app.get("/items/{item_id}")
# async def read_item(item_id: int, q : str | None = None):
#     return {"read_id" : item_id, "q": q}

# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item):
#     return {"item_name" : item.name, "item_id" : item_id}

# My Demo

# @app.get("/")
# def read_main():
    


def get_files_in_daterange(date_init : datetime.date, date_fin : datetime.date | None = None):
    """ Returns a list of abs paths to relevant files in the daterange.

    Parameters
    ----------
    date_init : datetime.date
        _description_
    date_fin : datetime.date | None, optional
        _description_, by default None

    Returns
    -------
    _type_
        _description_
    """
    if date_fin is None:
        date_fin = datetime.date.today(datetime.timezone.utc)
    
    # # Collect year folders
    # data_years = [f for f in os.listdir(DATA_SAVE_PATH) if os.path.isdir(os.path.join(DATA_SAVE_PATH, f))]
    # # Check for valid year range.
    # valid_years = [f for f in data_years if (int(f) >= date_init.year and int(f) <= date_fin.year)]
        
    files = []
    for file in [f for f in os.listdir(DATA_SAVE_PATH) if os.path.isfile(os.path.join(DATA_SAVE_PATH,f))]:
        if file.endswith("-temp_pres_data.csv"):
            filedate = file[0:8]
            filedate2 = datetime.datetime.strptime(filedate, "%Y%m%d").date()                
            
            if (filedate2 >= date_init and filedate2 <= date_fin):
                files.append(os.path.join(DATA_SAVE_PATH, file))
    return files


@app.get("/data/day")
async def read_past_day():
    timenow = datetime.datetime.now(datetime.timezone.utc)
    timeyesterday = timenow - datetime.timedelta(days=1)
    
    files = get_files_in_daterange(date_init=timeyesterday.date(), date_fin=timenow.date())
    
    # Process each file, retaining important information.
    datafiles = []
    for file in files: #maximum two files, unless we have smaller time increments in files...
        df = pd.read_csv(file)
        df["Datetime (UTC)"] = pd.to_datetime(df["Datetime (UTC)"], format="%Y%m%d_%H%M%S", utc=True)
    
        # Filter out-of-bounds timestamps.
        df = df.drop(df[
            (df["Datetime (UTC)"] < timeyesterday) & (df["Datetime (UTC)"] > timenow)
            ].index)
        datafiles.append(df)
        
    if len(datafiles) > 1:
        full_data = pd.concat(datafiles)
    else:
        full_data = datafiles[0]
        
    # Convert datetime to appropriate Plotly string.
    df["Datetime (UTC)"] = df["Datetime (UTC)"].dt.strftime('%Y-%m-%d %X') #2013-10-04 22:23:00
    timestamps = full_data["Datetime (UTC)"].to_list()
    timestrings = [str(t) for t in timestamps]
    print(timestrings[0:5])
    
    json = {
        "data" : [{
            "x" : timestrings,
            "y" : full_data[full_data.columns[1]].to_list(),
            "z" : full_data[full_data.columns[2]].to_list(),
            "type" : "scatter",
        }]
    }   
    return json


    # datashape = full_data.shape
    # if datashape[0] > 300: #count rows
        
    #     # Reduce data 
    #     # rF = int(np.ceil(datashape[0]) / 300) #reduction factor
        
    #     # Generate new data
    #     oidx = full_data["Datetime (UTC)"]
    #     nidx = pd.date_range(oidx.min(), oidx.max(), periods=300)
    #     full_data = full_data.reindex(oidx.union(nidx)).interpolate("Datetime (UTC)").reindex(nidx)
        
    # json = full_data.to_json()

@app.get("/data/fortnight")
async def read_past_fortnight():
    return

@app.get("/data/term")
async def read_past_term():
    return

@app.get("/data/year")
async def read_past_year():
    return
