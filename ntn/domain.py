"""The documented S1 model and the team's qualitative ranking rules."""
from datetime import date

STRIDE = ["Spoofing", "Tampering", "Repudiation", "Information Disclosure",
          "Denial of Service", "Elevation of Privilege"]
COMPONENTS = [
    {"id": "C1", "name": "Rural UE", "domain": "User", "assets": ["A1", "A2", "A3"]},
    {"id": "C2", "name": "Transparent LEO relay", "domain": "Space relay", "assets": ["A1", "A3"]},
    {"id": "C3", "name": "NTN gateway", "domain": "Ground access", "assets": ["A1", "A3", "A4", "A5"]},
    {"id": "C4", "name": "Ground gNB", "domain": "Ground access", "assets": ["A1", "A2", "A3", "A4", "A5"]},
    {"id": "C5", "name": "5G Core interfaces", "domain": "Operator core", "assets": ["A1", "A2", "A3"]},
    {"id": "C6", "name": "Administration endpoint", "domain": "Privileged administration", "assets": ["A4", "A5"]},
]
ASSETS = [
    {"id": "A1", "name": "Confidentiality and integrity of user traffic"},
    {"id": "A2", "name": "Subscriber identity and authentication material"},
    {"id": "A3", "name": "Service availability and access capacity"},
    {"id": "A4", "name": "Ground configuration and administration credentials"},
    {"id": "A5", "name": "Administration change records and logs"},
]
FLOWS = [
    {"id": "F1", "name": "Service radio", "from": "C1", "to": ["C2"], "boundary": "TB1", "data": "User traffic and signalling"},
    {"id": "F2", "name": "Feeder radio", "from": "C2", "to": ["C3"], "boundary": "TB2", "data": "Relayed radio signals"},
    {"id": "F3", "name": "Ground transport", "from": "C3", "to": ["C4"], "boundary": None, "data": "Access transport within the ground domain"},
    {"id": "F4", "name": "Core connection", "from": "C4", "to": ["C5"], "boundary": "TB3", "data": "N2 control signalling and N3 user traffic"},
    {"id": "F5", "name": "Administration", "from": "C6", "to": ["C3", "C4"], "boundary": "TB4", "data": "Configuration changes and administration records"},
]
BOUNDARIES = [
    {"id": "TB1", "name": "User to space relay"},
    {"id": "TB2", "name": "Space relay to ground access"},
    {"id": "TB3", "name": "Ground access to operator core"},
    {"id": "TB4", "name": "Privileged administration access"},
]
FEASIBILITY = [
    {"level": 1, "label": "Very low", "criteria": "Exceptional access or resources. Rare conditions. Little evidence."},
    {"level": 2, "label": "Low", "criteria": "Specialist equipment or privileged access plus a plausible weakness."},
    {"level": 3, "label": "Moderate", "criteria": "Commercial equipment or valid credentials and moderate skill. A practical attack path exists."},
    {"level": 4, "label": "High", "criteria": "Low barrier. Commodity tools. Repeatable and supported by evidence."},
]
IMPACT = [
    {"level": 1, "label": "Minor", "criteria": "One UE with quick recovery."},
    {"level": 2, "label": "Limited", "criteria": "Temporary disruption or limited information exposure."},
    {"level": 3, "label": "Major", "criteria": "Several users of the shared service or exposure of sensitive traffic or configuration."},
    {"level": 4, "label": "Severe", "criteria": "Sustained loss of the selected service or compromise of ground administration."},
]
MODEL = {"scenario": "S1", "title": "Transparent LEO NTN access", "components": COMPONENTS,
         "assets": ASSETS, "flows": FLOWS, "boundaries": BOUNDARIES, "stride": STRIDE,
         "feasibility": FEASIBILITY, "impact": IMPACT,
         "method_note": "The 4 x 4 matrix and priority bands are this team's adaptation. Ansong et al. use a different matrix.",
         "purpose": "A static service snapshot using an existing 5G NTN baseline to discuss future 6G relevance.",
         "limits": ["No RF or orbital simulation", "No real attacks or satellite hardware", "No full core internals or satellite command systems", "One operator and one shared access service", "No LLM or OpenWebUI dependency"]}
MAPS = {"components": {x["id"] for x in COMPONENTS}, "assets": {x["id"] for x in ASSETS},
        "flows": {x["id"] for x in FLOWS}, "boundaries": {x["id"] for x in BOUNDARIES}}


class Invalid(ValueError):
    pass


class Conflict(ValueError):
    pass


def priority(feasibility, impact):
    if feasibility is None or impact is None:
        return None, "Unscored"
    score = feasibility * impact
    return score, ("Low" if score <= 3 else "Medium" if score <= 7 else "High" if score <= 11 else "Critical")


def required_text(value, field, limit=12000):
    if not isinstance(value, str) or not value.strip():
        raise Invalid(f"{field} is required")
    if len(value) > limit:
        raise Invalid(f"{field} is too long")
    return value.strip()


def rating(value, field, nullable=False):
    if value is None and nullable:
        return None
    if type(value) is not int or value not in range(1, 5):
        raise Invalid(f"{field} must be an integer from 1 to 4")
    return value


def valid_date(value, field="review_date"):
    try:
        parsed = date.fromisoformat(value)
        if parsed > date.today():
            raise ValueError()
    except (ValueError, TypeError):
        raise Invalid(f"{field} must be a real date no later than today")
    return value


def validate_threat(data, reference_ids):
    if not isinstance(data, dict):
        raise Invalid("A threat must be an object")
    import re
    result = {}
    tid = data.get("id", "")
    if not isinstance(tid, str) or not re.fullmatch(r"T-\d{2,4}", tid):
        raise Invalid("Threat ID must look like T-08")
    result["id"] = tid
    for key in ["title", "description", "actor", "conditions", "controls", "consequence",
                "feasibility_reason", "impact_reason", "confidence_reason", "origin", "limitations"]:
        result[key] = required_text(data.get(key), key)
    result["scenario"] = "S1"
    result["stride"] = data.get("stride")
    if result["stride"] not in STRIDE:
        raise Invalid("Unknown STRIDE category")
    result["feasibility"] = rating(data.get("feasibility"), "feasibility", True)
    result["impact"] = rating(data.get("impact"), "impact", True)
    if (result["feasibility"] is None) != (result["impact"] is None):
        raise Invalid("Supply both ratings or leave both unscored")
    for key, ids in MAPS.items():
        values = data.get(key)
        if not isinstance(values, list) or (not values and key != "boundaries") or any(not isinstance(v, str) or v not in ids for v in values):
            raise Invalid(f"{key} must contain valid S1 identifiers")
        if len(set(values)) != len(values):
            raise Invalid(f"{key} contains duplicates")
        result[key] = values
    result["confidence"] = data.get("confidence")
    if result["confidence"] not in ["Low", "Medium", "High"]:
        raise Invalid("Unknown evidence confidence")
    result["review_status"] = data.get("review_status", "Imported")
    if result["review_status"] not in ["Imported", "Draft", "Reviewed"]:
        raise Invalid("Unknown review status")
    result["reviewer"] = data.get("reviewer", "")
    result["review_date"] = data.get("review_date", "")
    if result["review_status"] == "Reviewed":
        result["reviewer"] = required_text(result["reviewer"], "reviewer")
        valid_date(result["review_date"])
    else:
        result["reviewer"] = result["review_date"] = ""
    evidence = data.get("evidence")
    if not isinstance(evidence, list) or not evidence:
        raise Invalid("At least one evidence or assumption entry is required")
    result["evidence"] = []
    for item in evidence:
        if not isinstance(item, dict):
            raise Invalid("Evidence entries must be objects")
        ref = item.get("reference_id") or None
        if ref is not None and ref not in reference_ids:
            raise Invalid("Unknown evidence reference")
        basis = item.get("basis", "Assumption")
        if basis not in ["Assumption", "Context", "Direct"]:
            raise Invalid("Unknown evidence basis")
        checked = item.get("checked", False)
        if type(checked) is not bool:
            raise Invalid("Evidence checked flag must be true or false")
        locator = item.get("locator", "")
        checked_by = item.get("checked_by", "")
        checked_date = item.get("checked_date", "")
        if checked:
            if not ref:
                raise Invalid("Checked source support needs a reference")
            locator = required_text(locator, "source page or section")
            checked_by = required_text(checked_by, "source checked by")
            valid_date(checked_date, "source checked date")
        else:
            checked_by = checked_date = ""
        result["evidence"].append({"reference_id": ref, "basis": basis, "locator": str(locator),
            "checked": checked, "checked_by": checked_by, "checked_date": checked_date,
            "note": required_text(item.get("note"), "evidence note")})
    mitigations = data.get("mitigations")
    if not isinstance(mitigations, list) or not mitigations:
        raise Invalid("At least one candidate mitigation is required")
    result["mitigations"] = []
    for item in mitigations:
        if not isinstance(item, dict):
            raise Invalid("Mitigations must be objects")
        ref = item.get("reference_id") or None
        if ref is not None and ref not in reference_ids:
            raise Invalid("Unknown mitigation reference")
        result["mitigations"].append({"text": required_text(item.get("text"), "mitigation"),
            "reference_id": ref, "note": required_text(item.get("note"), "mitigation evidence note")})
    return result
