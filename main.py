from bm_to_pdf import pdfConverter
from fastapi import FastAPI, Response

app = FastAPI(title="PDF Processing API", version="1.0.0")

@app.get("/get_measurement_pdf")
async def generate_pdf(url: str, measurement: str):

    bm_pdf = pdfConverter( url, measurement) 

    # temp_input = f"bm.pdf"
    # temp_output = f"/tmp/{uuid.uuid4()}.pdf"
    # with open(temp_input, "wb") as f:
    #     f.write(await file.read())

    return Response(
        content = bm_pdf,
        media_type = "application/pdf",
        headers = {
            "Content-Disposition": "inline; "
            f"filename={measurement}.pdf"
        }
    )