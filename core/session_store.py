sessions: dict[str, str] = {}


def save_report(session_id: str, text: str) -> None:
    sessions[session_id] = text


def get_report(session_id: str) -> str | None:
    return sessions.get(session_id)
