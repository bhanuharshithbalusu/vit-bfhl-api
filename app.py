from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Any

app = FastAPI(title="VIT BFHL API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ====== EDIT THESE WITH YOUR DETAILS ======
FULL_NAME_LOWER = "john_doe"       # must be lowercase
DOB_DDMMYYYY    = "17091999"       # ddmmyyyy
EMAIL           = "john@xyz.com"
ROLL_NUMBER     = "ABCD123"
# ==========================================

class RequestModel(BaseModel):
    data: List[Any] = Field(..., description="Array of strings/values to process")

class ResponseModel(BaseModel):
    is_success: bool
    user_id: str
    email: str
    roll_number: str
    odd_numbers: List[str]
    even_numbers: List[str]
    alphabets: List[str]
    special_characters: List[str]
    sum: str
    concat_string: str

def is_all_digits(s: str) -> bool:
    return s.isdigit()

def is_all_alpha(s: str) -> bool:
    return s.isalpha()

def to_string(x: Any) -> str:
    # The challenge examples pass everything as strings, but we convert safely.
    return str(x)

def alternating_caps_reverse_concatenation(alphabet_items_upper: List[str]) -> str:
    """
    Build 'concat_string' as specified:
    - Take all alphabetical characters present in the input
    - Convert to uppercase (per character)
    - Concatenate in input order
    - Reverse the entire string
    - Apply alternating caps starting with UPPER at index 0
    """
    # 1) Uppercase per-letter and concatenate in input order
    letters = []
    for token in alphabet_items_upper:
        for ch in token:
            if ch.isalpha():
                letters.append(ch.upper())
    # 2) Reverse
    letters.reverse()
    # 3) Alternating caps starting with upper
    out_chars = []
    for i, ch in enumerate(letters):
        out_chars.append(ch.upper() if i % 2 == 0 else ch.lower())
    return "".join(out_chars)

@app.post("/bfhl", response_model=ResponseModel)
def bfhl(payload: RequestModel):
    try:
        raw_items = payload.data
    except Exception:
        # Pydantic will have already validated, but just in case
        raise HTTPException(status_code=400, detail="Invalid request format")

    even_numbers: List[str] = []
    odd_numbers: List[str] = []
    alphabets: List[str] = []
    special_characters: List[str] = []
    numeric_sum = 0

    for item in raw_items:
        s = to_string(item)

        if is_all_digits(s):
            # Numbers are returned as strings
            n = int(s)
            numeric_sum += n
            if n % 2 == 0:
                even_numbers.append(s)
            else:
                odd_numbers.append(s)
        elif is_all_alpha(s):
            # Entire token is alphabetic: store uppercase version
            alphabets.append(s.upper())
        else:
            # Mixed or contains any non-alphanumeric => special character
            # e.g., "&", "-", "*", "a1", "12.3", "", " "
            if s != "":
                special_characters.append(s)
            else:
                special_characters.append(s)  # keep empty strings if present

    concat_string = alternating_caps_reverse_concatenation(alphabets)

    response = ResponseModel(
        is_success=True,
        user_id=f"{FULL_NAME_LOWER}_{DOB_DDMMYYYY}",
        email=EMAIL,
        roll_number=ROLL_NUMBER,
        odd_numbers=odd_numbers,
        even_numbers=even_numbers,
        alphabets=alphabets,
        special_characters=special_characters,
        sum=str(numeric_sum),
        concat_string=concat_string
    )
    return response
