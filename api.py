from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import os
import uuid
import bm_to_pdf

app = FastAPI()

@app.post("/generate-pdf/")
async def generate_pdf(file: UploadFile = File(...)):
    temp_input = f"/tmp/{uuid.uuid4()}_{file.filename}"
    temp_output = f"/tmp/{uuid.uuid4()}.pdf"
    with open(temp_input, "wb") as f:
        f.write(await file.read())
    # Supondo que bm_to_pdf.py tenha uma função chamada 'convert_to_pdf'
    bm_to_pdf.convert_to_pdf(temp_input, temp_output)
    return FileResponse(temp_output, media_type="application/pdf", filename=os.path.basename(temp_output))
