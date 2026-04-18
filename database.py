"""
database.py — Enhanced CollegeBot Data Layer — ITM University
Reads from college_data.csv.  All functions return clean, well-typed data.
CSV layout: category, id, field1 … field6  (columns 0-7)
"""

import csv
import os

# Locate the CSV next to this script, or fall back to CWD
_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(_DIR, "college_data.csv")


# ─────────────────────────────────────────────────────────────────────────────
#  Core loader
# ─────────────────────────────────────────────────────────────────────────────

def load_data(category: str) -> list[list[str]]:
    """Return all rows whose first column matches *category* (case-insensitive)."""
    rows: list[list[str]] = []
    try:
        with open(CSV_FILE, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader)                        # skip header
            for row in reader:
                if row and row[0].strip().lower() == category.lower():
                    # Pad to 8 elements so callers never get IndexError
                    while len(row) < 8:
                        row.append("")
                    rows.append(row)
    except FileNotFoundError:
        print(f"[ERROR] {CSV_FILE} not found.")
    return rows

# Convenience: fields 2-7 only (the actual data columns)
def _fields(rows: list[list[str]]) -> list[list[str]]:
    return [r[2:8] for r in rows]


# ─────────────────────────────────────────────────────────────────────────────
#  Courses  (name, duration, fee, hod, intake, cities)
# ─────────────────────────────────────────────────────────────────────────────

def get_courses() -> list[tuple]:
    """Returns list of (name, duration, fee, hod, intake, cities)."""
    return [tuple(r) for r in _fields(load_data("course"))]


def get_course_details(query: str) -> list[dict]:
    results = []
    for r in load_data("course"):
        if query.lower() in r[2].lower():
            results.append({
                "name":     r[2], "duration": r[3], "fee":      r[4],
                "hod":      r[5], "intake":   r[6], "cities":   r[7],
            })
    return results


# ─────────────────────────────────────────────────────────────────────────────
#  Fees  (dept, total, per_year, admission, note)
# ─────────────────────────────────────────────────────────────────────────────

def get_all_fees() -> list[tuple]:
    return [tuple(r) for r in _fields(load_data("fee"))]


def get_fees(query: str = "") -> str:
    data = load_data("fee")
    if query:
        for r in data:
            if r[2].lower() in query.lower() or query.lower() in r[2].lower():
                return (f"💰 {r[2]} Fee:\n"
                        f"  Total      : ₹{int(r[3]):,}\n"
                        f"  Per Year   : ₹{int(r[4]):,}\n"
                        f"  Admission  : ₹{int(r[5]):,}\n"
                        f"  Note       : {r[6]}")
    result = "Fee Structure:\n"
    for r in data:
        result += f"  {r[2]}: ₹{int(r[3]):,} total | ₹{int(r[4]):,}/yr\n"
    return result


# ─────────────────────────────────────────────────────────────────────────────
#  Teachers  (name, dept, designation, qualification, experience, award)
# ─────────────────────────────────────────────────────────────────────────────

def get_teachers() -> list[tuple]:
    return [tuple(r) for r in _fields(load_data("teacher"))]


def get_teacher_details(dept_query: str = "") -> list[tuple]:
    rows = get_teachers()
    if not dept_query:
        return rows
    return [row for row in rows if dept_query.lower() in row[1].lower()]


# ─────────────────────────────────────────────────────────────────────────────
#  Placements  (company, role, lpa, year, dept, city)
# ─────────────────────────────────────────────────────────────────────────────

def get_placements() -> list[tuple]:
    return [tuple(r) for r in _fields(load_data("placement"))]


def get_top_placements(n: int = 10) -> list[tuple]:
    data = load_data("placement")
    sorted_data = sorted(data, key=lambda r: float(r[4]), reverse=True)
    return [tuple(r[2:8]) for r in sorted_data[:n]]


def get_placement_stats() -> dict:
    data = load_data("placement")
    lpas = [float(r[4]) for r in data]
    return {
        "total_companies": len(data),
        "highest_lpa":     max(lpas),
        "average_lpa":     round(sum(lpas) / len(lpas), 2),
        "lowest_lpa":      min(lpas),
    }


def get_placements_by_dept(dept_query: str = "") -> list[tuple]:
    rows = get_placements()
    if not dept_query:
        return rows
    return [row for row in rows if dept_query.lower() in row[4].lower()]


# ─────────────────────────────────────────────────────────────────────────────
#  Exams  (dept_semester, subject, date, room, duration, marks)
#  Smart mapping: user says "B.Tech AI" → matches "B.Tech AI Semester X" rows
# ─────────────────────────────────────────────────────────────────────────────

# Map user-friendly course names / abbreviations to CSV dept prefix
COURSE_EXAM_MAP = {
    "b.tech cse":   "B.Tech CSE",
    "btech cse":    "B.Tech CSE",
    "cse":          "B.Tech CSE",
    "b.tech ai":    "B.Tech AI",
    "btech ai":     "B.Tech AI",
    "artificial intelligence": "B.Tech AI",
    "b.tech it":    "B.Tech IT",
    "btech it":     "B.Tech IT",
    "information technology": "B.Tech IT",
    "b.tech me":    "B.Tech ME",
    "btech me":     "B.Tech ME",
    "mechanical":   "B.Tech ME",
    "b.tech ece":   "B.Tech ECE",
    "btech ece":    "B.Tech ECE",
    "electronics":  "B.Tech ECE",
    "b.tech ce":    "B.Tech CE",
    "btech ce":     "B.Tech CE",
    "civil":        "B.Tech CE",
    "b.tech ee":    "B.Tech EE",
    "btech ee":     "B.Tech EE",
    "electrical":   "B.Tech EE",
    "b.tech ds":    "B.Tech DS",
    "btech ds":     "B.Tech DS",
    "data science": "B.Tech DS",
    "b.tech cy":    "B.Tech CY",
    "btech cy":     "B.Tech CY",
    "cyber security": "B.Tech CY",
    "cybersecurity": "B.Tech CY",
    "b.tech cc":    "B.Tech CC",
    "btech cc":     "B.Tech CC",
    "cloud computing": "B.Tech CC",
    "b.tech ml":    "B.Tech ML",
    "btech ml":     "B.Tech ML",
    "machine learning": "B.Tech ML",
    "b.tech rb":    "B.Tech RB",
    "btech rb":     "B.Tech RB",
    "robotics":     "B.Tech RB",
    "b.tech ae":    "B.Tech AE",
    "btech ae":     "B.Tech AE",
    "aerospace":    "B.Tech AE",
    "b.tech bt":    "B.Tech BT",
    "btech bt":     "B.Tech BT",
    "biotechnology": "B.Tech BT",
    "b.tech ch":    "B.Tech CH",
    "btech ch":     "B.Tech CH",
    "chemical":     "B.Tech CH",
    "bca":          "BCA",
    "bba":          "BBA",
    "bsc":          "BSC",
    "mba":          "MBA",
    "mca":          "MCA",
}


def get_exams() -> list[tuple]:
    return [tuple(r) for r in _fields(load_data("exam"))]


def get_exams_by_dept(dept: str = "") -> list[tuple]:
    rows = get_exams()
    if not dept:
        return rows
    # First try smart map
    dept_lower = dept.lower().strip()
    mapped = COURSE_EXAM_MAP.get(dept_lower)
    if mapped:
        return [row for row in rows if row[0].startswith(mapped)]
    # Fallback: partial match
    return [row for row in rows if dept_lower in row[0].lower()]


# ─────────────────────────────────────────────────────────────────────────────
#  Library  (name, collection, hours, access, rooms, resources)
# ─────────────────────────────────────────────────────────────────────────────

def get_all_library() -> list[tuple]:
    return [tuple(r) for r in _fields(load_data("library"))]


def get_library() -> str:
    data = load_data("library")
    if not data:
        return "Library info not available."
    r = data[0]
    return f"📚 {r[2]}\n  Collection: {r[3]} | Hours: {r[4]}\n  Access: {r[5]}\n  {r[6]}"


# ─────────────────────────────────────────────────────────────────────────────
#  Hostel  (name, capacity, rent, ac, facilities, food)
# ─────────────────────────────────────────────────────────────────────────────

def get_all_hostels() -> list[tuple]:
    return [tuple(r) for r in _fields(load_data("hostel"))]


def get_hostel() -> str:
    data = load_data("hostel")
    if not data:
        return "Hostel info not available."
    r = data[0]
    return f"🏠 {r[2]}\n  Capacity: {r[3]} | Rent: ₹{r[4]}/mo | {r[5]} | {r[6]}"


# ─────────────────────────────────────────────────────────────────────────────
#  Attendance  (type, percentage, rule, tracking, alert, report)
# ─────────────────────────────────────────────────────────────────────────────

def get_all_attendance() -> list[tuple]:
    return [tuple(r) for r in _fields(load_data("attendance"))]


def get_attendance() -> str:
    data = load_data("attendance")
    if not data:
        return "Attendance info not available."
    r = data[0]  # r[2]=type, r[3]=%, r[4]=rule, r[5]=tracking, r[6]=alert, r[7]=report
    return f"Min {r[3]} required. {r[4]}. {r[5]}."


# ─────────────────────────────────────────────────────────────────────────────
#  Toppers  (dept, name, cgpa, year, award, benefit)
# ─────────────────────────────────────────────────────────────────────────────

def get_topper() -> list[tuple]:
    return [tuple(r) for r in _fields(load_data("topper"))]


def get_toppers_by_year(year: str = "2023") -> list[tuple]:
    """Returns toppers filtered by year (field index 3 in data = r[5] in raw)."""
    data = load_data("topper")
    return [tuple(r[2:8]) for r in data if r[5] == year]


def get_toppers_by_dept(dept_query: str = "") -> list[tuple]:
    rows = get_topper()   # (dept, name, cgpa, year, award, benefit)
    if not dept_query:
        return rows
    return [row for row in rows if dept_query.lower() in row[0].lower()]


# ─────────────────────────────────────────────────────────────────────────────
#  Facilities  (name, details, timing, note)
# ─────────────────────────────────────────────────────────────────────────────

def get_facilities() -> list[tuple]:
    return [(r[2], r[3], r[4], r[5]) for r in load_data("facility")]


def get_facility(name: str) -> dict | None:
    for r in load_data("facility"):
        if name.lower() in r[2].lower():
            return {"name": r[2], "details": r[3], "timing": r[4], "note": r[5]}
    return None


# ─────────────────────────────────────────────────────────────────────────────
#  Admissions  (mode, applicable_for, criteria, documents)
# ─────────────────────────────────────────────────────────────────────────────

def get_admissions() -> list[tuple]:
    return [(r[2], r[3], r[4], r[5]) for r in load_data("admission")]


# ─────────────────────────────────────────────────────────────────────────────
#  Scholarships  (name, beneficiaries, benefit, eligibility)
# ─────────────────────────────────────────────────────────────────────────────

def get_scholarships() -> list[tuple]:
    return [(r[2], r[3], r[4], r[5]) for r in load_data("scholarship")]


# ─────────────────────────────────────────────────────────────────────────────
#  Events  (name, type, date, details, prize_note)
# ─────────────────────────────────────────────────────────────────────────────

def get_events() -> list[tuple]:
    return [(r[2], r[3], r[4], r[5], r[6]) for r in load_data("event")]


# ─────────────────────────────────────────────────────────────────────────────
#  Clubs  (name, activities, highlights, benefit)
# ─────────────────────────────────────────────────────────────────────────────

def get_clubs() -> list[tuple]:
    return [(r[2], r[3], r[4], r[5]) for r in load_data("club")]


# ─────────────────────────────────────────────────────────────────────────────
#  Rules  (category, rule, consequence, note)
# ─────────────────────────────────────────────────────────────────────────────

def get_rules() -> list[tuple]:
    return [(r[2], r[3], r[4], r[5]) for r in load_data("rule")]


# ─────────────────────────────────────────────────────────────────────────────
#  Infrastructure  (area, details, specification, note)
# ─────────────────────────────────────────────────────────────────────────────

def get_infrastructure() -> list[tuple]:
    return [(r[2], r[3], r[4], r[5]) for r in load_data("infrastructure")]


# ─────────────────────────────────────────────────────────────────────────────
#  Accreditation  (body, status, score_rank, validity)
# ─────────────────────────────────────────────────────────────────────────────

def get_accreditation() -> list[tuple]:
    return [(r[2], r[3], r[4], r[5]) for r in load_data("accreditation")]


# ─────────────────────────────────────────────────────────────────────────────
#  Research  (area, details, metrics, funding_note)
# ─────────────────────────────────────────────────────────────────────────────

def get_research() -> list[tuple]:
    return [(r[2], r[3], r[4], r[5]) for r in load_data("research")]


# ─────────────────────────────────────────────────────────────────────────────
#  Contact  (dept, phone, email, hours)
# ─────────────────────────────────────────────────────────────────────────────

def get_contact() -> list[tuple]:
    return [(r[2], r[3], r[4], r[5]) for r in load_data("contact")]


def get_contact_by_dept(dept: str = "") -> str:
    data = load_data("contact")
    for r in data:
        if dept.lower() in r[2].lower():
            return f"{r[2]}: {r[3]} | {r[4]} | {r[5]}"
    return "\n".join([f"  {r[2]}: {r[3]}" for r in data])
