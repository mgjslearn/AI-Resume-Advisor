from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import json
import os
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()

app = FastAPI()

# Add CORS middleware to allow requests from React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Hugging Face API configuration
HF_API_URL = "https://api-inference.huggingface.co/models/gpt2"
HF_API_KEY = os.getenv("HF_API_KEY")

class AnalyzeRequest(BaseModel):
    resume: str
    job: str

class AnalyzeResponse(BaseModel):
    score: int
    suggestions: list[str]

@app.post("/api/analyze", response_model=AnalyzeResponse)
async def analyze_resume(request: AnalyzeRequest):
    print(f"HF_API_KEY present: {bool(HF_API_KEY)}")
    print(f"Request received - Resume length: {len(request.resume)}, Job length: {len(request.job)}")
    
    # For now, let's implement a simple keyword-based analysis as a fallback
    # This ensures your app works while we troubleshoot the Hugging Face API
    
    resume_lower = request.resume.lower()
    job_lower = request.job.lower()
    
    # Extract keywords from job description
    common_tech_words = ['react', 'node.js', 'nodejs', 'python', 'javascript', 'java', 'sql', 
                        'database', 'api', 'rest', 'html', 'css', 'git', 'docker', 'aws', 
                        'azure', 'mongodb', 'postgresql', 'express', 'vue', 'angular']
    
    job_keywords = []
    for word in common_tech_words:
        if word in job_lower:
            job_keywords.append(word)
    
    # Check how many job keywords appear in resume
    matching_keywords = []
    for keyword in job_keywords:
        if keyword in resume_lower:
            matching_keywords.append(keyword)
    
    # Calculate score based on keyword matching
    if len(job_keywords) > 0:
        score = min(int((len(matching_keywords) / len(job_keywords)) * 100), 95)
    else:
        score = 50  # Default score if no tech keywords found
    
    # Generate suggestions based on missing keywords
    missing_keywords = [kw for kw in job_keywords if kw not in matching_keywords]
    
    suggestions = []
    if missing_keywords:
        suggestions.append(f"Add experience with: {', '.join(missing_keywords[:3])}")
    
    suggestions.extend([
        "Include specific metrics and achievements in your experience section",
        "Tailor your summary to highlight skills mentioned in the job description",
        "Add relevant projects that demonstrate your technical abilities"
    ])
    
    return AnalyzeResponse(
        score=score,
        suggestions=suggestions[:3]  # Return only first 3 suggestions
    )

@app.get("/")
async def root():
    return {"message": "Resume AI Backend is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model": "gpt2"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3001)
