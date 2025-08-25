from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from io import BytesIO
import tempfile
import pdfplumber
from docx import Document
from text_utils import score_resume_vs_jd

app = FastAPI(title="Resume–Job Match Scorer API", version="0.2.0")

# Allow local dev frontends (Vite 5173, CRA 3000)
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------
# Resume text extraction
# ----------------------


def extract_text_from_pdf(file_bytes: bytes) -> str:
    try:
        text = []
        with pdfplumber.open(BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                t = page.extract_text() or ""
                text.append(t)
        return "\n".join(text).strip()
    except Exception:
        return ""


def extract_text_from_docx(file_bytes: bytes) -> str:
    try:
        with tempfile.NamedTemporaryFile(suffix=".docx", delete=True) as tmp:
            tmp.write(file_bytes)
            tmp.flush()
            doc = Document(tmp.name)
            return "\n".join([p.text for p in doc.paragraphs]).strip()
    except Exception:
        return ""


def extract_text_from_txt(file_bytes: bytes) -> str:
    try:
        return file_bytes.decode("utf-8", errors="ignore").strip()
    except Exception:
        return ""


def extract_resume_text(upload: UploadFile) -> str:
    filename = (upload.filename or "").lower()
    file_bytes = upload.file.read()

    if filename.endswith(".pdf"):
        text = extract_text_from_pdf(file_bytes)
    elif filename.endswith(".docx"):
        text = extract_text_from_docx(file_bytes)
    elif filename.endswith(".txt"):
        text = extract_text_from_txt(file_bytes)
    else:
        # fallback
        text = extract_text_from_pdf(file_bytes)
        if not text:
            text = extract_text_from_docx(file_bytes)
        if not text:
            text = extract_text_from_txt(file_bytes)
    return text

# ----------------------
# API Endpoints
# ----------------------


@app.post("/score")
async def score_endpoint(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
    position_title: Optional[str] = Form(None)
):
    if not job_description or len(job_description.strip()) < 20:
        raise HTTPException(
            status_code=400, detail="Job description seems too short.")

    resume_text = extract_resume_text(resume)
    if not resume_text or len(resume_text) < 20:
        raise HTTPException(
            status_code=422, detail="Could not extract text from resume. Try .pdf, .docx, or .txt.")

    try:
        result = score_resume_vs_jd(resume_text, job_description)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error scoring resume: {str(e)}")

    payload = {
        "title": position_title or "Unknown Role",
        **result,
        "resume_char_count": len(resume_text),
        "jd_char_count": len(job_description)
    }
    return payload


@app.get("/health")
async def health():
    return {"status": "ok"}
