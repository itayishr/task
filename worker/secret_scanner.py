import re
from typing import List, Tuple

# Comprehensive AWS secret patterns based on your info and common formats:

SECRET_PATTERNS = {
    # Access Key IDs: start with AKIA or ASIA (for session tokens)
    "AWS Access Key": re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),

    # Secret Access Keys: base64-like 40 char strings with + / =
    "AWS Secret Key": re.compile(r"(?<![A-Za-z0-9/+=])[A-Za-z0-9/+=]{40}(?![A-Za-z0-9/+=])"),

    # Session Tokens: longer base64-like strings (min length ~200 chars)
    "AWS Session Token": re.compile(
        r"FQoDYXdzE[a-zA-Z0-9+/=]{200,}"
    ),

    # Other AWS IDs you might want to catch, e.g., User IDs, Role IDs (AIDA, AROA prefixes)
    "AWS User ID": re.compile(r"\bAIDA[A-Z0-9]{16}\b"),
    "AWS Role ID": re.compile(r"\bARO[A-Z0-9]{13}\b"),
}


def scan_text_for_secrets(text: str) -> List[Tuple[str, str]]:
    """
    Scan text and return list of (secret_type, secret_value).
    """
    findings = []
    for secret_type, pattern in SECRET_PATTERNS.items():
        matches = pattern.findall(text)
        for match in matches:
            findings.append((secret_type, match))
    return findings
