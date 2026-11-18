import re
# Rules used to identify potentially suspicious XSS constructs.
XSS_RULES = [
    {
        "rule_id": "XSS-001",
        "technique": "Script element",
        "pattern": r"<\s*script\b",
        "severity": "high",
        "confidence": "high"
    },
    {
        "rule_id": "XSS-002",
        "technique": "HTML event handler",
        "pattern": r"\bon[a-z]+\s*=",
        "severity": "medium",
        "confidence": "medium"
    },
    {
        "rule_id": "XSS-003",
        "technique": "JavaScript URL",
        "pattern": r"javascript\s*:",
        "severity": "high",
        "confidence": "medium"
    }
]


def detect_xss(value):
    findings = []

    if not isinstance(value, str):
        return findings

    for rule in XSS_RULES:
        matches = re.finditer(
            rule["pattern"],
            value,
            re.IGNORECASE
        )

        for match in matches:
            findings.append({
                "rule_id": rule["rule_id"],
                "technique": rule["technique"],
                "severity": rule["severity"],
                "confidence": rule["confidence"],
                "evidence": match.group()
            })

    return findings
