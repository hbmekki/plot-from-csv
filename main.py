from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import pandas as pd

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/web", StaticFiles(directory="./dist", html=True), name="web")

@app.get("/api/v1/columns")
async def get_csv_columns():
    cols = pd.read_csv('./data/analysis_results.csv', nrows=0).columns.to_list()
    return cols

@app.get("/api/v1/columns-data")
async def get_csv_columns(x_col: str, y_col: str):
    cols = [x_col, y_col]
    df = pd.read_csv('./data/analysis_results.csv', skipinitialspace=True, usecols=cols)
    return {
        cols[0] : df[cols[0]].tolist()[:200],
        cols[1] : df[cols[1]].tolist()[:200]
    }
@app.post("/api/v1/upload-csv")
def upload(file: UploadFile = File(...)):
    try:
        with open('./data/analysis_results.csv', 'wb') as f:
            while contents := file.file.read(1024 * 1024):
                f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

    return {"message": f"Successfully uploaded {file.filename}"}