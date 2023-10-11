from fastapi import FastAPI, File, HTTPException, Request, status
from fastapi.responses import Response, JSONResponse
from fastapi.exceptions import RequestValidationError
from typing import Annotated
import PyPDF2
import logging
from io import BytesIO

app = FastAPI()

def do_pdf_merge(file1: BytesIO, file2: BytesIO) -> BytesIO:
    merger = PyPDF2.PdfMerger()

    file1_pdfreader = PyPDF2.PdfReader(file1)
    file2_pdfreader = PyPDF2.PdfReader(file2)

    # Append to merger
    merger.append(file1_pdfreader)
    merger.append(file2_pdfreader)

    # Write output to a byte stream
    output_stream = BytesIO()
    merger.write(output_stream)
    output_stream.seek(0)  # Reset stream pointer
    
    return output_stream

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
	exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
	logging.error(f"{request}: {exc_str}")
	content = {'status_code': 10422, 'message': exc_str, 'data': None}
	return JSONResponse(content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

@app.post("/merge/")
async def merge_pdfs(file1: Annotated[bytes, File()] = None, file2: Annotated[bytes, File()] = None):
    if not file1 or not file2:
        raise HTTPException(status_code=400, detail="Both files are required")

    try:
        # Read the content of the uploaded files
        file1_content = await file1.read()
        file2_content = await file2.read()

        # Convert content to byte streams
        file1_stream = BytesIO(file1_content)
        file2_stream = BytesIO(file2_content)

        # Write output to a byte stream
        output_stream = do_pdf_merge(file1_stream, file2_stream)

        # Return the merged PDF
        return Response(output_stream.read(), headers={"Content-Disposition": "attachment; filename=merged.pdf"})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
