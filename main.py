from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import FileResponse
import PyPDF2
from io import BytesIO

app = FastAPI()

@app.post("/merge/")
async def merge_pdfs(file1: UploadFile = None, file2: UploadFile = None):
    if not file1 or not file2:
        raise HTTPException(status_code=400, detail="Both files are required")

    # Create a PDF merger
    merger = PyPDF2.PdfFileMerger()
    
    try:
        # Read the content of the uploaded files
        file1_content = await file1.read()
        file2_content = await file2.read()

        # Convert content to byte streams
        file1_stream = BytesIO(file1_content)
        file2_stream = BytesIO(file2_content)

        # Append to merger
        merger.append(file1_stream)
        merger.append(file2_stream)

        # Write output to a byte stream
        output_stream = BytesIO()
        merger.write(output_stream)
        output_stream.seek(0)  # Reset stream pointer

        # Return the merged PDF
        return FileResponse(output_stream, headers={"Content-Disposition": "attachment; filename=merged.pdf"})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
