DETECTION_PATTERNS = [
    {
        "pattern": "v-html",
        "severity": "HIGH",
        "message": "Found v-html directive"
    },
    {
        "pattern": "eval(",
        "severity": "HIGH",
        "message": "Usage of eval() detected"
    },
    {
        "pattern": ':href="userProvidedUrl"',
        "severity": "MEDIUM",
        "message": "Possible user-controlled URL injection"
    },
    {
        "pattern": ':style="userProvidedStyles"',
        "severity": "MEDIUM",
        "message": "Possible user-controlled style injection"
    },
]