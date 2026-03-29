from core.tools_impl import (
    list_detected_issues_impl,
    risk_assessment_impl,
    create_maintenance_plan_impl,
    predict_failure_impl,
)

VALID_ACTIONS = {"issues", "risk", "plan", "failure"}


def handle_query(action: str, report_text: str) -> str:

    action = action.lower().strip()

    print("ACTION:", action)

    if action == "issues":
        return list_detected_issues_impl(report_text)

    if action == "risk":
        return risk_assessment_impl(report_text)

    if action == "plan":
        return create_maintenance_plan_impl(report_text)

    if action == "failure":
        return predict_failure_impl(report_text)

    return f"Invalid action '{action}'. Valid actions: {', '.join(sorted(VALID_ACTIONS))}"
