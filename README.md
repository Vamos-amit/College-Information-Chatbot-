# 🎓 ITM University — CollegeBot AI Assistant

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-orange?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)
![University](https://img.shields.io/badge/ITM%20University-NAAC%20A%2B-purple?style=for-the-badge)

**A fully offline, AI-powered desktop chatbot for ITM University **  
Built with Python · Tkinter GUI · CSV Data Layer · NLP Intent Detection

</div>

---

## Preview

```
┌─────────────────────────────────────────────────────────────┐
│      CollegeBot · ITM University                    [Help]  │
│       ● Online                                              │
├─────────────────────────────────────────────────────────────┤
│   Courses   Fees        Placements    Faculty     Exams  │
│   Hostel    Scholarship      Contact                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│    Hello! I'm CollegeBot — your ITM University AI         │
│      Assistant! Ask me about courses, exams, fees...        │
│                                                             │
│                    What is the B.Tech AI exam list?  [You]  │
│                                                             │
│     Exam Schedule — B.Tech AI (20 subjects listed)         │
│  ┌──────────────────┬────────────────────────┬──────────┐  │
│  │ Dept/Sem         │ Subject                │ Date     │  │
│  ├──────────────────┼────────────────────────┼──────────┤  │
│  │ B.Tech AI Sem 1  │ Mathematics for AI     │ Nov 5    │  │
│  │ B.Tech AI Sem 2  │ Machine Learning Funds │ Nov 13   │  │
│  └──────────────────┴────────────────────────┴──────────┘  │
├─────────────────────────────────────────────────────────────┤
│  Ask me anything about ITM University…          [ Send ➤ ]  │
└─────────────────────────────────────────────────────────────┘
```

---

##  Features

###  Smart NLP Engine
- **Intent detection** using keyword synonyms, bigrams, and trigrams
- **Fuzzy matching** via `difflib` — handles typos and informal language
- **Entity extraction** — recognizes course names like `B.Tech AI`, `BCA`, `BBA`, `BSC`, `MBA`
- Supports **25+ intents** including greetings, jokes, and name memory

### Course-Aware Exam Lists
Ask `"B.Tech AI exam list"` → shows **only B.Tech AI exams** (all 8 semesters)  
Ask `"BCA exams"` → shows **only BCA exams**  
Each course has its own full semester-by-semester exam schedule:

| Course | Exam Subjects Covered |
|--------|-----------------------|
| B.Tech CSE | 22 exams (Sem 1–8) |
| B.Tech AI | 20 exams (Sem 1–8) |
| BCA | 10 exams (Sem 1–6) |
| BBA | 10 exams (Sem 1–6) |
| BSC | 10 exams (Sem 1–6) |
| MBA | 7 exams (Sem 1–4) |
| B.Tech ME, ECE | Full semester coverage |

###  Courses Offered
All course names are properly formatted:

| Code | Full Name |
|------|-----------|
| B.Tech CSE | Computer Science Engineering |
| B.Tech AI | Artificial Intelligence |
| B.Tech IT | Information Technology |
| B.Tech DS | Data Science |
| B.Tech ML | Machine Learning |
| B.Tech CY | Cyber Security |
| B.Tech CC | Cloud Computing |
| B.Tech ECE | Electronics & Communication |
| B.Tech ME | Mechanical Engineering |
| B.Tech RB | Robotics Engineering |
| B.Tech AE | Aerospace Engineering |
| BCA | Bachelor of Computer Applications |
| BBA | Bachelor of Business Administration |
| BSC | Bachelor of Science (CS) |
| MBA | Master of Business Administration |
| MCA | Master of Computer Applications |

###  Hostel Information (10 Blocks)
- Boys Hostel A, B, C (AC / Non-AC / Premium)
- Girls Hostel A, B, C (AC / Non-AC / Premium)
- International Student Hostel
- PG Scholar Hostel
- Faculty Guest House
- Special Needs Hostel (Accessible)

###  All Data Categories
| Category | Records | Description |
|----------|---------|-------------|
| Courses | 20 | All UG/PG programs with fees, HOD, cities |
| Exams | 90 | Semester-wise subject-wise exam schedule |
| Faculty | 30 | Name, dept, designation, qualification, awards |
| Placements | 35 | Company, role, LPA, year, eligible depts |
| Fees | 20 | Per course total/yearly/admission fee |
| Hostels | 10 | Block, capacity, rent, amenities, food |
| Scholarships | 10 | Type, eligibility, benefit amount |
| Admissions | 8 | JEE/CET/Management/NRI/Lateral modes |
| Events | 10 | Fests, hackathons, summits with prizes |
| Clubs | 10 | Activities, achievements, benefits |
| Facilities | 12 | Sports, cafeteria, medical, transport |
| Rules | 10 | Attendance, dress code, anti-ragging |
| Library | 5 | Collections, hours, digital access |
| Attendance | 8 | Policy per department |
| Toppers | 15 | CGPA, awards, scholarships won |
| Research | 5 | Patents, publications, funding |
| Accreditation | 6 | NAAC/NBA/NIRF/ISO/AICTE/UGC |
| Infrastructure | 6 | Campus, labs, WiFi, power, security |
| Contact | 10 | Phone, email, hours for all offices |

---

##  Project Structure

```
ITM-CollegeBot/
│
├── chatbot.py          # Main application — UI + NLP + Bot logic
├── database.py         # Data access layer — reads college_data.csv
├── college_data.csv    # All university data (19 categories, 300+ rows)
└── README.md           # This file
```

> **All three files must be in the same folder** to run correctly.

---

## Getting Started

### Prerequisites

- Python **3.10 or higher**
- `tkinter` (bundled with standard Python on Windows/macOS)

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/ITM-CollegeBot.git
cd ITM-CollegeBot
```

**2. (Optional) Create a virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

**3. No extra packages needed!**  
This project uses only Python's standard library (`tkinter`, `csv`, `re`, `difflib`, `threading`).

### Run the App

```bash
python chatbot.py
```

---

##  Example Queries

You can type naturally — the bot handles variations and typos.

| What you type | What you get |
|---------------|--------------|
| `show B.Tech AI exam list` | Full B.Tech AI exam schedule (Sem 1–8) |
| `BCA exams` | BCA semester-wise exam list |
| `fee for BBA` | BBA fee structure with breakdown |
| `B.Tech CSE faculty` | Faculty list for CSE dept |
| `hostel details` | All 10 hostel blocks with amenities |
| `top placements` | Top 15 packages sorted by LPA |
| `scholarship for sports` | Sports achievement scholarship info |
| `show all courses` | All 20 courses with duration, fee, HOD |
| `admission process` | All 8 admission modes |
| `naac ranking` | Accreditation and NIRF details |
| `contact admissions` | Admissions office phone + email |
| `tell me a joke` | Programming humour |

---

##  UI Design

The chatbot features a **clean, modern light theme**:

- **Background:** Airy light-blue white (`#F0F4FF`)
- **Accent:** Rich indigo blue (`#3A57E8`) — ITM brand-inspired
- **Bot bubbles:** White cards with soft border
- **User bubbles:** Indigo with white text
- **Tables:** Zebra-striped rows, sortable columns (click headers)
- **Quick-action chips:** One-click shortcuts for common queries
- **Bot avatar:** Indigo circle with 🤖 icon
- **Status bar:** Shows university name and ready state

---

##  Architecture

```
chatbot.py
├── SYNONYMS dict        → maps 200+ keywords to 25 intents
├── _tokenize()          → builds uni/bi/trigrams from input
├── detect_intents()     → scores and ranks intents
├── extract_entity()     → extracts course/dept name from query
├── Bot.respond()        → routes intent to correct data function
└── ChatUI               → full Tkinter interface

database.py
├── load_data(category)  → reads CSV rows by category
├── COURSE_EXAM_MAP      → maps course names to exam CSV prefixes
├── get_exams_by_dept()  → smart exam filtering per course
└── 20+ getter functions → one per data category

college_data.csv
└── 19 categories × 300+ rows → all university data
```

---

##  Customisation

### Update university data
Edit `college_data.csv` — all rows follow this format:
```
category,id,field1,field2,field3,field4,field5,field6
course,21,B.Tech IoT,4,760000,Dr. Example,80,Bangalore/Pune
```

### Add a new course's exams
Add rows in the CSV:
```
exam,91,B.Tech IoT Semester 1,Introduction to IoT,2025-11-05,Room 115,3 hrs,80 marks
exam,92,B.Tech IoT Semester 1,Embedded Systems,2025-11-07,Lab IoT,3 hrs,80 marks
```
Then add the mapping in `database.py`:
```python
COURSE_EXAM_MAP["b.tech iot"] = "B.Tech IoT"
COURSE_EXAM_MAP["iot"] = "B.Tech IoT"
```

### Change theme colours
Edit the `C = { ... }` dict at the top of `chatbot.py`.

---

##  Dependencies

| Library | Version | Purpose |
|---------|---------|---------|
| `tkinter` | Stdlib | GUI framework |
| `csv` | Stdlib | Data loading |
| `re` | Stdlib | Text tokenisation |
| `difflib` | Stdlib | Fuzzy intent matching |
| `threading` | Stdlib | Non-blocking bot replies |
| `random` | Stdlib | Response variety |

**Zero pip installs required.**

---

##  About ITM University

**ITM University Gwalior**, Gwalior Road, Indore, Madhya Pradesh  
-  **NAAC Grade A+** | Score 3.65/4.0  
-  **NIRF Rank 67** among Engineering Colleges of India  
-  **ISO 9001:2015** Certified  
-  **AICTE Approved** | **UGC Recognised** | **NBA Accredited**  
-  [www.itmuniversity.ac.in](https://www.itmuniversity.ac.in)

---

##  Contributing

Contributions are welcome!

1. Fork the repository
2. Create a new branch: `git checkout -b feature/your-feature`
3. Make your changes and commit: `git commit -m "Add: your feature"`
4. Push to your branch: `git push origin feature/your-feature`
5. Open a Pull Request

### Ideas for contributions
- Add voice input support (`speech_recognition`)
- Export table data to Excel / PDF
- Add a dark/light theme toggle button
- Add more courses and exam data
- Web version using Flask + JavaScript

---

## License

This project is licensed under the **MIT License**.

```
MIT License

Copyright (c) 2025 ITM University CollegeBot Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```


---

<div align="center">

Made with for ITM University, Indore

Star this repo if you found it useful!

</div>

