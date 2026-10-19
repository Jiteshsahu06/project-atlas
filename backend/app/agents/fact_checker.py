
def check_answer(answer: str, citations: list[dict]) -> dict:
    if not citations:
        return {
            "verified": False,
            "confidence": 0.0,
            "reason": "No supporting citations found.",
        }

    supported_sources = {
        citation.get("source")
        for citation in citations
        if citation.get("source")
    }

    verified = bool(supported_sources)

    return {
        "verified": verified,
        "confidence": 0.7 if verified else 0.0,
        "reason": (
            "Sources are available; verify each claim against them."
            if verified
            else "No valid source metadata found."
        ),
    }
