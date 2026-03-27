from core.router import route_query
from core.tools_impl import (
    list_detected_issues_impl,
    risk_assessment_impl,
    create_maintenance_plan_impl,
    recommend_from_text_impl,
)


def handle_query(query: str, report_text: str) -> str:

    tool = route_query(query)

    print("ROUTED TO:", tool)

    if tool == "issues":
        return list_detected_issues_impl(report_text)

    elif tool == "risk":
        return risk_assessment_impl(report_text)

    elif tool == "plan":
        return create_maintenance_plan_impl(report_text)

    elif tool == "recommend":
        return recommend_from_text_impl(report_text)

    elif tool == "chat":
        return "Please ask about issues, risk, or maintenance plan."
