import os
from openai import OpenAI
from typing import List
from core.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

async def evaluate_cv(job_description: str, candidates: List):
    prompt = build_prompt(job_description, candidates)  

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an expert technical recruiter. Your job is to analyze CVs and evaluate fit for a job."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4,
        max_tokens=4096,
    )

    output = response.choices[0].message.content
    return parse_response(output)

def build_prompt(job_description: str, candidates: list) -> str:
    prompt = f"""Evaluate the following 3 candidates based on this job description:

Job Description:
\"\"\"
{job_description}
\"\"\"

"""

    for idx, candidate in enumerate(candidates, start=1):
        prompt += f"Candidate {idx}: {candidate['candidate_name']}\n"
        for chunk in candidate['text']:
            prompt += f"- {chunk.strip()}\n"
        prompt += "\n"

    prompt += """
For each candidate, return a JSON object like:
[
  {
    "name": "Candidate Name",
    "score": 85,
    "summary": "This candidate has strong experience in X and Y..."
  },
  ...
]
"""
    return prompt

def parse_response(output: str):
    try:
        import json
        return json.loads(output)
    except:
        return {"error": "Failed to parse LLM response", "raw": output}