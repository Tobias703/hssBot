# fetch_and_parse_kursliste.py

import re
import json
from playwright.sync_api import sync_playwright
from config import *
import sys

TAG_RE = re.compile(r"<[^>]+>")

DATA_RE = re.compile(
    r"var\s+data\s*=\s*(\{.*?\});",
    re.DOTALL
)

def extract_data_object(html: str) -> dict:
    match = DATA_RE.search(html)
    if not match:
        raise RuntimeError("Could not find 'var data =' block")

    raw_json = match.group(1)
    return json.loads(raw_json)

def clean_kursname(raw: str) -> str:
    if "<br>" in raw:
        return raw.split("<br>", 1)[1].strip()
    return raw.strip()

def clean_status(raw: str) -> str:
    return TAG_RE.sub("", raw).strip()

def get_course_list(debug = 0):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(storage_state=AUTH_STATE)

        response = context.request.get(KURSLISTE_URL)
        if response.status != 200:
            raise RuntimeError(f"HTTP {response.status}")

        html = response.text()
        data = extract_data_object(html)

        courses = data["list"]
        processed = []

        for c in courses:
            processed.append({
                "CourseID": int(c["CourseID"]),
                "Sport": c["Sport"].strip(),
                "Kursname": clean_kursname(c["Kursname"]),
                "Zeit": c["WannUndZeitraum"],
                "Ort": c["Ort"].strip(),
                "Status": clean_status(c["Status"]),
            })

        processed.sort(key=lambda x: x["CourseID"])
        
        if debug:
            for c in processed:
                print(c)

        return processed
    
def get_course_ids(course_data, field_values, field_name = "Kursname"):
    found_course_ids = []
    missing_values = []

    field_values_set = set(field_values)
    matched_values = set()

    for c in course_data:
        value = c.get(field_name)
        if value in field_values_set:
            found_course_ids.append(c["CourseID"])
            matched_values.add(value)

    missing_values = field_values_set - matched_values

    if missing_values:
        for v in missing_values:
            print(f"Course '{v}' not found")

    if not found_course_ids:
        sys.exit(0)

    return found_course_ids

def check_enrollable(ids):
    data = get_course_list()

    enrollable = []
    ids_set = set(ids)

    for c in data:
        cid = c.get("CourseID")
        if cid in ids_set and c.get("Status") == "Buchbar":
            enrollable.append(cid)

    if not enrollable:
        missing = ids_set - {c.get("CourseID") for c in data}
        for cid in missing:
            print(f"Course {cid} not found in enrollment check!")

    return enrollable