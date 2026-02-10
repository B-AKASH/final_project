import os
from groq import Groq
from dotenv import load_dotenv

# -------------------------------------------------
# LOAD ENV VARIABLES
# -------------------------------------------------
load_dotenv()  # 🔴 REQUIRED

# -------------------------------------------------
# GROQ CLIENT SETUP
# -------------------------------------------------
API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    raise RuntimeError("GROQ_API_KEY is not set")

client = Groq(api_key=API_KEY)
# -------------------------------------------------
# INTELLIGENT QUERY PARSER
# -------------------------------------------------
def parse_inquiry(query: str) -> dict:
    """
    Uses LLM to translate natural language into structured SQL filters.
    """
    prompt = f"""
    SYSTEM:
    You are an elite medical data scientist. Parse the user's inquiry into a structured JSON query object.
    
    COLUMNS AVAILABLE:
    - patient_name (TEXT)
    - age (INTEGER)
    - gender (TEXT)
    - diagnosis (TEXT: 'Cardiac Issue', 'Infection', 'Asthma', 'Diabetes', 'Hypertension')
    - risk_level (TEXT: 'Low', 'Medium', 'High')
    - care_priority (TEXT: 'Normal', 'Urgent')
    - medication (TEXT)
    - has_insurance (BOOLEAN: 1 or 0)
    - cholesterol (INTEGER)
    - smoking_status (TEXT)
    
    INSTRUCTIONS:
    1. EXTRACT NAME: If a person's name is mentioned, put it in "specific_name".
    2. SQL FILTERS: Create a list of SQL conditions. 
       - For name, use LIKE: "patient_name LIKE '%name%'"
       - For risk, use equals: "risk_level = 'High'"
       - For diagnosis, use LIKE: "diagnosis LIKE '%keyword%'"
    3. DISPLAY MODE: Determine the best visual mode:
       - "PATIENT_SPOTLIGHT": If the user is asking about a specific individual by name.
       - "POLICY_FOCUS": If the user is asking about insurance, coverage, or hospital rules.
       - "ANALYTICS_GRID": For general searches yielding multiple patients (e.g. "show high risk patients").
    4. POLICY: If the user asks about coverage, insurance, or general policy rules, set "is_policy_query" to true.

    OUTPUT FORMAT (JSON ONLY):
    {{
      "sql_conditions": ["condition1", "condition2"],
      "specific_name": "extracted_name or null",
      "display_mode": "PATIENT_SPOTLIGHT" | "POLICY_FOCUS" | "ANALYTICS_GRID",
      "is_policy_query": true/false,
      "summary": "Clinical summary of the search intent"
    }}

    USER QUERY: "{query}"
    """

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            response_format={ "type": "json_object" },
            temperature=0,
        )
        import json
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"Parsing Error: {e}")
        return {"sql_conditions": [], "specific_name": None, "is_policy_query": False, "summary": "Error parsing query"}

# -------------------------------------------------
# MASTER EXPLANATION FUNCTION
# -------------------------------------------------
def explain_decision(patient: dict, reasons: list, evidence: list) -> str:
    """
    Generate a professional, empathetic clinical explanation
    using patient data, reasons, and PDF evidence.
    """

    # Safe fallbacks
    patient_name = patient.get("patient_name", "N/A")
    age = patient.get("age", "N/A")
    gender = patient.get("gender", "N/A")
    diagnosis = patient.get("diagnosis", "N/A")
    risk_level = patient.get("risk_level", "N/A")

    reasons_text = "\n".join(f"- {r}" for r in reasons) if reasons else "- General clinical indicators"
    evidence_text = "\n".join(f"- {e}" for e in evidence) if evidence else "- Standard hospital protocols"

    prompt = f"""
SYSTEM:
You are a senior clinical decision support assistant working in a hospital.
Your explanations must be:
- Professional
- Clear
- Empathetic
- Evidence-based
- Easy for clinicians to understand

PATIENT PROFILE:
- Name: {patient_name}
- Age: {age}
- Gender: {gender}
- Diagnosis: {diagnosis}
- Assessed Risk Level: {risk_level}

IDENTIFIED RISK FACTORS:
{reasons_text}

SUPPORTING CLINICAL & POLICY EVIDENCE:
{evidence_text}

INSTRUCTIONS:
1. Clearly explain **WHY** this risk level was assigned.
2. Connect risk factors with evidence logically.
3. Provide **actionable next steps** for the care team.
4. Use headings and bullet points.
5. Do NOT introduce new medical facts not present above.
6. Maintain a calm, professional, reassuring tone.
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=900
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"LLM Error: {str(e)}"
