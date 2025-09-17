import uvicorn
from schemas.SampleSchema import SampleSchema
from fastapi import FastAPI
from fastapi import UploadFile, HTTPException
import os 

import joblib
import pandas as pd

app = FastAPI()
# Load the model from the correct path (handles both local and Docker environments)
model_dir = os.getenv("MODEL_DIR", "../models/best")
model_path = os.path.join(model_dir, "best_model_pipeline.joblib")
model = joblib.load(model_path)

@app.get("/health", tags=['health'])  
def health_check():
    return {"status": "healthy"}
  
@app.post("/predict", tags=['predict'])
def predict(sample: SampleSchema):
    # Convert the sample to a DataFrame
    df = pd.DataFrame([dict(sample)])
    # Make prediction using the loaded model
    prediction = model.predict(df)[0]
    return {"prediction": prediction}
  
@app.post("/predict_batch", tags=['predict'])
def predict_batch(file: UploadFile):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=422, detail="Only CSV files are allowed.")
    
    df = pd.read_csv(file.file, encoding='utf-8', sep=';')    
    predictions = model.predict(df)
    
    return {
        "predictions": predictions.tolist()
    }
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)