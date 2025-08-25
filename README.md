# Resume–Job Match Scorer

A modern **Resume–Job Match Scorer** built with **React, TypeScript, Bootstrap** on the frontend and **FastAPI + Python** on the backend.  
It allows users to upload a resume and job description, then evaluates how well the resume matches the job using keyword analysis, giving a score, coverage percentage, matched/missing keywords, suggestions, and a pie chart visualization.

---

## Features

✅ Upload resume (.pdf for now) and enter job description  
✅ Score calculation (0–10)  
✅ Coverage percentage with progress bar  
✅ Matched vs missing keywords  
✅ Suggestions to improve resume  
✅ Pie chart visualization  
✅ Responsive UI with Bootstrap cards, shadows, and hover effects  
✅ Expressive styling with icons and subtle borders

---

## Upcoming Features

🔹 Focus more on **skills and important keywords** rather than all keywords  
🔹 Enhance UI with **additional CSS animations and styles**  
🔹 Add **storage support** for resumes and results  
🔹 Expand **supported file types** (docx, txt, etc.), not just PDFs

---

## Tech Stack

- **Frontend:** React, TypeScript, Bootstrap, Recharts
- **Backend:** Python, FastAPI
- **Libraries:** axios, pdfplumber, docx2txt, bootstrap-icons

---

## Installation & Running

### Backend

```bash
# create virtual environment
python -m venv .venv
# activate it
# Windows PowerShell
.venv\Scripts\Activate.ps1
# install dependencies
pip install fastapi uvicorn pdfplumber docx2txt python-multipart
# run server
uvicorn main:app --reload --port 8000
```
