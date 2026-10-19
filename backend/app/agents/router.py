
def route_question(question: str) -> str:
    text = question.lower().strip()

    if not text:
        return "out_of_scope"

    unsafe_terms = [
        "ignore all instructions",
        "reveal system prompt",
        "bypass permissions",
        "steal credentials",
    ]

    if any(term in text for term in unsafe_terms):
        return "unsafe"

    if any(word in text for word in ["calculate", "cagr", "growth rate"]):
        return "calculation"

    if any(word in text for word in ["compare", "difference", "versus", " vs "]):
        return "comparison"

    if any(word in text for word in ["report", "market", "share", "revenue"]):
        return "factual"

    return "out_of_scope"
