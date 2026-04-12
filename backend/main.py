from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from analyzer import analyze_text

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextInput(BaseModel):
    text: str

@app.post("/analyze")
async def analyze(input: TextInput):
    if not input.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    try:
        result = analyze_text(input.text)
        return result
    except Exception as e:
        print("ENDPOINT ERROR:", str(e))
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def root():
    return {"status": "TruthLens backend is running!"}

# ← ADD THIS
@app.get("/test")
def test():
    try:
        result = analyze_text("Einstein was born in Germany. He invented the television.")
        return result
    except Exception as e:
        return {"error": str(e)}