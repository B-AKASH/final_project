import os
from pypdf import PdfReader
from pathlib import Path

# -------------------------------------------------
# FILE PATH CONFIG
# -------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
GUIDELINES_PDF = BASE_DIR.parent / "guidelines.pdf"
POLICY_PDF = BASE_DIR.parent / "policy.pdf"

# -------------------------------------------------
# PDF TEXT EXTRACTION
# -------------------------------------------------
def _read_pdf_text(pdf_path: Path) -> str:
    """
    Read and extract text from a PDF file safely.
    Returns full text or empty string if file not found.
    """
    if not pdf_path.exists():
        return ""

    try:
        reader = PdfReader(str(pdf_path))
        text = []
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(page_text)
        return "\n".join(text)
    except Exception as e:
        print(f"[PDF READ ERROR] {pdf_path.name}: {e}")
        return ""

# Cache PDF text (read once)
GUIDELINES_TEXT = _read_pdf_text(GUIDELINES_PDF)
POLICY_TEXT = _read_pdf_text(POLICY_PDF)

# -------------------------------------------------
# KEYWORD MAP (FOR SMART MATCHING)
# -------------------------------------------------
KEYWORD_MAP = {
    "diabetes": ["diabetes", "diabetic", "blood sugar", "glucose"],
    "asthma": ["asthma", "bronchial", "inhaler"],
    "obesity": ["obesity", "overweight", "bmi"],
    "kidney": ["kidney", "renal", "ckd"],
    "cholesterol": ["cholesterol", "lipid", "hdl", "ldl", "statin"],
    "cardiac": ["cardiac", "heart", "cardio", "hypertension"],
    "smoking": ["smoking", "smoker", "tobacco", "nicotine"]
}

# -------------------------------------------------
# MAIN RAG FUNCTION
# -------------------------------------------------
def retrieve_evidence(patient: dict, question: str = "") -> dict:
    """
    Retrieve relevant clinical guideline and insurance policy evidence
    based on patient data and inquiry question.
    """

    clinical_evidence = []
    insurance_evidence = []

    search_terms = set()

    # ---------------- PATIENT-BASED TERMS ----------------
    if patient.get("diabetes") == "Yes":
        search_terms.update(KEYWORD_MAP["diabetes"])

    if patient.get("asthma") == "Yes":
        search_terms.update(KEYWORD_MAP["asthma"])

    if patient.get("obesity") == "Yes":
        search_terms.update(KEYWORD_MAP["obesity"])

    if patient.get("chronic_kidney_disease") == "Yes":
        search_terms.update(KEYWORD_MAP["kidney"])

    if patient.get("cholesterol", 0) >= 200:
        search_terms.update(KEYWORD_MAP["cholesterol"])

    if "cardiac" in str(patient.get("diagnosis", "")).lower():
        search_terms.update(KEYWORD_MAP["cardiac"])

    if patient.get("smoking_status") == "Smoker":
        search_terms.update(KEYWORD_MAP["smoking"])

    # ---------------- QUESTION-BASED TERMS ----------------
    if question:
        for group in KEYWORD_MAP.values():
            for term in group:
                if term in question.lower():
                    search_terms.add(term)

    # ---------------- CLINICAL GUIDELINES SEARCH ----------------
    if GUIDELINES_TEXT:
        lines = GUIDELINES_TEXT.split("\n")
        seen = set()

        for term in search_terms:
            for line in lines:
                clean = line.strip()
                if clean and term.lower() in clean.lower() and clean not in seen:
                    clinical_evidence.append(clean)
                    seen.add(clean)
                    if len(clinical_evidence) >= 6:
                        break
            if len(clinical_evidence) >= 6:
                break

    # ---------------- INSURANCE / POLICY SEARCH ----------------
    insurance_keywords = [
        "insurance", "policy", "coverage", "claim",
        "billing", "premium", "deductible"
    ]

    is_insurance_query = any(
        kw in question.lower() for kw in insurance_keywords
    )

    if POLICY_TEXT and is_insurance_query:
        lines = POLICY_TEXT.split("\n")
        for line in lines:
            clean = line.strip()
            if (
                clean
                and len(clean) > 25
                and any(kw in clean.lower() for kw in insurance_keywords)
                and clean not in insurance_evidence
            ):
                insurance_evidence.append(clean)
                if len(insurance_evidence) >= 4:
                    break

    # ---------------- FALLBACKS ----------------
    if not clinical_evidence:
        clinical_evidence.append(
            "Risk assessment based on standard hospital clinical guidelines and best practices."
        )

    return {
        "clinical_evidence": clinical_evidence,
        "insurance_evidence": insurance_evidence
    }
