def route_query(query: str) -> str:

    q = query.lower()

    if any(x in q for x in ["issue", "problem", "fault"]):
        return "issues"

    if any(x in q for x in ["risk", "danger", "failure"]):
        return "risk"

    if any(x in q for x in ["fix", "repair", "solution", "what to do", "how to fix"]):
        return "plan"

    if any(x in q for x in ["recommend", "suggest"]):
        return "recommend"

    return "chat"
