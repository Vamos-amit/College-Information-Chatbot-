"""CollegeBot — ITM University AI Assistant"""

import tkinter as tk
from tkinter import ttk, font as tkfont
import threading, time, re, random, difflib, sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import database

# ── NLP ───────────────────────────────────────────────────────────────────────

SYNONYMS = {
    "course":        ["course","courses","program","programs","programme","degree","degrees",
                      "branch","stream","subject","subjects","study","btech","b.tech",
                      "mtech","m.tech","mba","bca","mca","bba","bsc","engineering","curriculum",
                      "syllabus","specialisation","specialization","allcourses","showcourses",
                      "b.tech ai","b.tech cse","b.tech it","b.tech ml","b.tech ds"],
    "fee":           ["fee","fees","cost","price","tuition","charges","payment","amount",
                      "afford","expensive","pay","rupee","rs","inr","money","budget",
                      "feestructure","showfees"],
    "placement":     ["placement","placements","job","jobs","recruit","hire","hiring",
                      "package","lpa","salary","company","companies","campus","offer","ctc",
                      "career","internship","drive","placed","showplacements"],
    "teacher":       ["teacher","teachers","faculty","faculties","professor","professors",
                      "staff","hod","instructor","sir","mam","lecturer","guide","mentor",
                      "educator","showteachers","allfaculty","showfaculty"],
    "exam":          ["exam","exams","examination","test","schedule","timetable","datesheet",
                      "paper","assessment","quiz","viva","practical","midterm","endterm",
                      "backlog","examschedule","showexams","examlist","examtimetable"],
    "library":       ["library","book","books","journal","reading","borrow","ebook","e-book",
                      "resource","novel","reference","issue","lib"],
    "hostel":        ["hostel","hostels","accommodation","room","rooms","stay","pg",
                      "dormitory","boarding","lodge","mess","warden","curfew"],
    "attendance":    ["attendance","present","absent","shortage","proxy","bunk",
                      "defaulter","leave","detain","detained","75","80","attendancepolicy"],
    "topper":        ["topper","toppers","rank","ranker","goldmedal","firstrank","merit",
                      "topstudent","highestcgpa","achiever","universitytop","beststudent"],
    "scholarship":   ["scholarship","scholarships","financialaid","stipend","feewaiver",
                      "concession","grant","funded","award","showscholarships"],
    "admission":     ["admission","admissions","apply","application","enrollment","join",
                      "entry","jee","cet","quota","eligibility","criteria","form","nri","lateral"],
    "facility":      ["facility","facilities","campusfacilities","sport","sports","gym","pool","swimming",
                      "cafeteria","canteen","bus","transport","atm","medical","clinic",
                      "auditorium","playground","ground","court","stadium"],
    "event":         ["event","events","fest","techfest","cultural","hackathon","competition",
                      "seminar","summit","workshop","symposium","exhibition","carnival"],
    "club":          ["club","clubs","society","committee","codingclub","roboticsclub",
                      "activity","nss","cell","chapter","team","group"],
    "rule":          ["rule","rules","regulation","policy","dresscode","mobile","ragging",
                      "discipline","conduct","guideline","norm","penalty","fine"],
    "research":      ["research","patent","publication","lab","innovation","project",
                      "phd","paper","csir","dst","funded"],
    "accreditation": ["naac","nba","nirf","ranking","accredit","iso","approved",
                      "graded","certified","recognition","ugc","aicte","accreditation"],
    "contact":       ["contact","contacts","phone","email","number","address","reach",
                      "helpline","telephone","office","enquiry","inquiry","showcontact"],
    "infra":         ["infrastructure","building","classroom","wifi","internet",
                      "power","smartclass","construction","campusinfrastructure"],
    "stats":         ["statistics","stats","summary","overview","highlights","aboutcollege"],
    "greeting":      ["hi","hello","hey","howdy","namaste","hii","greetings","yo","sup"],
    "bye":           ["bye","goodbye","seeyou","takecare","quit","exit","cya","later","tata"],
    "thanks":        ["thank","thanks","thankyou","thx","tysm","appreciate","grateful"],
    "help":          ["help","options","menu","commands","guide","features","capabilities"],
    "how_are_you":   ["howareyou","howru","howdoyoudo","youokay"],
    "joke":          ["joke","funny","laugh","humor","comedy","makemelaugh"],
    "name_set":      ["mynameis","iam","im","callme","naam","meranaam"],
    "name_ask":      ["whatismyname","doyouknowmyname","remembermyname"],
    "bot_name":      ["whatisyourname","whoareyou","yourname","introduceyourself"],
}

_W2I = {w.lower().replace(" ",""): intent
        for intent, words in SYNONYMS.items() for w in words}

def _tokenize(text):
    tokens = re.sub(r"[^\w\s%.]", " ", text.lower()).split()
    bi  = [tokens[i]+tokens[i+1] for i in range(len(tokens)-1)]
    tri = [tokens[i]+tokens[i+1]+tokens[i+2] for i in range(len(tokens)-2)]
    return list(set(tokens + bi + tri))

def detect_intents(text):
    scores, known = {}, list(_W2I)
    for t in _tokenize(text):
        key    = t.replace(" ","")
        intent = _W2I.get(key)
        if intent:
            scores[intent] = scores.get(intent, 0) + 2
        else:
            m = difflib.get_close_matches(key, known, n=1, cutoff=0.87)
            if m:
                scores[_W2I[m[0]]] = scores.get(_W2I[m[0]], 0) + 1
    return [k for k,_ in sorted(scores.items(), key=lambda x:-x[1])] or ["unknown"]

DEPT_MAP = {
    "B.Tech CSE":["cse","computer science","comps","b.tech cse","btech cse"],
    "B.Tech IT": ["information technology","infotech","b.tech it","btech it"],
    "B.Tech ECE":["ece","electronics","communication","b.tech ece","btech ece"],
    "B.Tech ME": ["me","mechanical","b.tech me","btech me"],
    "B.Tech CE": ["civil","b.tech ce","btech ce"],
    "B.Tech EE": ["electrical","b.tech ee","btech ee"],
    "B.Tech DS": ["data science","ds","b.tech ds","btech ds"],
    "B.Tech CY": ["cyber","cybersecurity","cyber security","b.tech cy","btech cy"],
    "B.Tech CC": ["cloud computing","cloud","b.tech cc","btech cc"],
    "B.Tech AI": ["artificial intelligence","b.tech ai","btech ai","ai"],
    "B.Tech ML": ["machine learning","ml","b.tech ml","btech ml"],
    "B.Tech RB": ["robotics","robot","b.tech rb","btech rb"],
    "B.Tech AE": ["aerospace","aero","b.tech ae","btech ae"],
    "B.Tech BT": ["biotech","biotechnology","b.tech bt","btech bt"],
    "B.Tech CH": ["chemical","b.tech ch","btech ch"],
    "MBA":  ["mba","management","business administration"],
    "BCA":  ["bca"],
    "MCA":  ["mca"],
    "BBA":  ["bba","bachelor of business"],
    "BSC":  ["bsc","bachelor of science","b.sc"],
}

def extract_entity(text):
    low = " " + text.lower() + " "
    for dept, kws in DEPT_MAP.items():
        if any((" "+kw+" ") in low or low.strip().endswith(kw) for kw in kws):
            return dept
    return None

def extract_year(text):
    m = re.search(r"\b(20\d{2})\b", text)
    return m.group(1) if m else None

def _tbl(title, cols, rows):
    return {"title": title, "columns": cols, "rows": rows}

# ── Bot ───────────────────────────────────────────────────────────────────────

JOKES = [
    "Why do programmers prefer dark mode?\nBecause light attracts bugs! 🐛",
    "How many CS students to change a bulb?\nNone — that's a hardware problem! 💡",
    "Why did the DB admin leave his wife?\nShe had too many relationships! 😄",
    "Favourite data structure? A linked list — always pointing to the next assignment! 📚",
    "Why do Java devs wear glasses?\nBecause they don't C#! 👓",
    "A SQL query walks into a bar and asks two tables… 'Can I join you?' 🍺",
]

WELCOME = (
    "👋 Hello! I'm CollegeBot — your ITM University AI Assistant!\n\n"
    "🏫 ITM University, Gwalior Road, Indore | NAAC A+ | NIRF Rank 67\n\n"
    "I show all data in neat sortable tables. Ask naturally — I handle typos!\n\n"
    "📌 Try: 'Show B.Tech AI courses' | 'B.Tech AI exam list' | 'Fee for BCA'\n"
    "         'Show hostel details' | 'Faculty in B.Tech CSE' | 'Scholarships'\n\n"
    "Click a chip above or type 'help' 😊"
)

# Tables with no extra parameters — intent maps directly to (title, cols, db_fn)
SIMPLE_TABLES = {
    "library":       ("📚 Library Information",
                      ["Library","Collection","Hours","Access Type","Rooms","Resources"],
                      database.get_all_library),
    "attendance":    ("📊 Attendance Policy",
                      ["Category","Min Required","Rule","Tracking","Alert","Reports"],
                      database.get_all_attendance),
    "scholarship":   ("🎁 Scholarships Available",
                      ["Scholarship","Who Can Apply","Benefit","Eligibility"],
                      database.get_scholarships),
    "admission":     ("📋 Admission Modes",
                      ["Mode","Applicable For","Criteria","Documents"],
                      database.get_admissions),
    "facility":      ("⚽ Campus Facilities",
                      ["Facility","Details","Timing","Note"],
                      database.get_facilities),
    "event":         ("🎪 Events & Fests",
                      ["Event","Type","Date","Details","Prize / Note"],
                      database.get_events),
    "club":          ("🎭 Student Clubs",
                      ["Club","Activities","Highlights","Benefit"],
                      database.get_clubs),
    "rule":          ("📋 Rules & Regulations",
                      ["Category","Rule","Consequence","Note"],
                      database.get_rules),
    "research":      ("🔬 Research & Innovation",
                      ["Area","Details","Metrics","Funding / Note"],
                      database.get_research),
    "accreditation": ("🏅 Accreditations & Rankings",
                      ["Body","Status","Score / Rank","Validity"],
                      database.get_accreditation),
    "contact":       ("📞 Contact Directory",
                      ["Department","Phone","Email","Hours"],
                      database.get_contact),
    "infra":         ("🏗 Campus Infrastructure",
                      ["Area","Details","Specification","Note"],
                      database.get_infrastructure),
}

_PCOLS = ["Company","Role / Designation","Package (LPA)","Year","Eligible Depts","Location"]

class Bot:
    def __init__(self): self.user_name = ""

    def respond(self, user_input):
        text    = user_input.strip()
        primary = detect_intents(text)[0]
        dept    = extract_entity(text)

        # name capture
        nm = re.search(r"(my name is|i am|i'm|call me|naam|mera naam)\s+([a-zA-Z]+)", text, re.I)
        if nm:
            self.user_name = nm.group(2).strip().title()
            return f"Great to meet you, {self.user_name}! 🙌 How can I help?", None

        n = f", {self.user_name}" if self.user_name else ""

        # conversational responses via dispatch dict
        CONV = {
            "name_ask":   lambda: (f"Your name is {self.user_name}! 😊" if self.user_name
                                   else "You haven't told me yet! Say 'My name is ...'", None),
            "bot_name":   lambda: ("I'm CollegeBot 🤖 — ITM University's AI assistant! Type 'help' to see what I can do!", None),
            "greeting":   lambda: (random.choice([f"Hello{n}! 👋",f"Hey{n}! 😊",f"Hi{n}! 🎓"])
                                   + " Welcome to ITM University! Ask me anything.", None),
            "bye":        lambda: (random.choice([f"Goodbye{n}! 👋",f"See you{n}! 😊",
                                                   f"Take care{n}! 🌟"]), None),
            "thanks":     lambda: (random.choice(["You're welcome! 😊","Happy to help! 🙌",
                                                   "Anytime! 🤖"]), None),
            "how_are_you":lambda: (random.choice(["Doing great! 😊","Full capacity! 🚀",
                                                   "Fantastic — ready to help!"]), None),
            "joke":       lambda: (random.choice(JOKES), None),
            "help":       lambda: (
                "🤖 ITM University CollegeBot — I can help with:\n\n"
                "🎓 Courses (B.Tech AI/CSE/BCA/BBA/BSC/MBA etc.)\n"
                "💰 Fees  |  🏢 Placements  |  👩\u200d🏫 Faculty  |  📅 Exams\n"
                "📚 Library  |  🏠 Hostel  |  📊 Attendance  |  🏆 Toppers\n"
                "🎁 Scholarships  |  📋 Admissions  |  ⚽ Facilities\n"
                "🎪 Events  |  🎭 Clubs  |  📋 Rules  |  🔬 Research\n"
                "🏅 Rankings  |  📞 Contact\n\n"
                "💡 Try: 'B.Tech AI exam list' | 'Fee for BBA' | 'BCA exams'\n"
                "        'Hostel details' | 'Scholarship for sports'", None),
        }
        if primary in CONV:
            return CONV[primary]()

        # simple no-parameter tables
        if primary in SIMPLE_TABLES:
            title, cols, fn = SIMPLE_TABLES[primary]
            return f"{title}: ℹ️", _tbl(title, cols, list(fn()))

        # parameterised tables
        if primary == "course":
            if dept:
                d = database.get_course_details(dept) or [
                    {"name":c[0],"duration":c[1],"fee":c[2],"hod":c[3],"intake":c[4],"cities":c[5]}
                    for c in database.get_courses() if dept.lower() in c[0].lower()]
                rows = [(c["name"],f"{c['duration']} yrs",f"₹{int(c['fee']):,}",
                         c["hod"],c["intake"],c["cities"]) for c in d]
            else:
                rows = [(c[0],f"{c[1]} yrs",f"₹{int(c[2]):,}",c[3],c[4],c[5])
                        for c in database.get_courses()]
            label = f" — {dept}" if dept else ""
            return (f"Courses{label}: 🎓",
                    _tbl(f"🎓 Available Courses{label}",
                         ["Course","Duration","Total Fee","HOD","Intake","Job Cities"], rows))

        if primary == "fee":
            d = database.get_all_fees()
            if dept: d = [f for f in d if dept.lower() in f[0].lower()]
            rows = [(f[0],f"₹{int(f[1]):,}",f"₹{int(f[2]):,}",f"₹{int(f[3]):,}",f[4]) for f in d]
            label = f" — {dept}" if dept else ""
            return (f"Fee structure{label}: 💰",
                    _tbl(f"💰 Fee Structure{label}",
                         ["Course/Dept","Total Fee","Per Year","Admission Fee","Note"], rows))

        if primary == "placement":
            top  = any(w in text.lower() for w in ["top","best","highest","maximum","package"])
            d    = (database.get_top_placements(15) if top else
                    database.get_placements_by_dept(dept) if dept else database.get_placements())
            rows = [(p[0],p[1],f"₹{p[2]} LPA",p[3],p[4],p[5]) for p in d]
            st   = database.get_placement_stats()
            msg  = (f"{'🌟 Top placements' if top else 'Placements'}"
                    f"{' — '+dept if dept else ''}: 🏢\n"
                    f"Highest: ₹{st['highest_lpa']} LPA | Avg: ₹{st['average_lpa']} LPA | "
                    f"Companies: {st['total_companies']}")
            title = f"{'🌟 Top 15 Packages' if top else '🏢 Placement Records'}{' — '+dept if dept else ''}"
            return msg, _tbl(title, _PCOLS, rows)

        if primary == "teacher":
            d = database.get_teacher_details(dept or "")
            label = f" — {dept}" if dept else ""
            return (f"Faculty{label}: 👩\u200d🏫",
                    _tbl(f"👩\u200d🏫 Faculty Directory{label}",
                         ["Name","Department","Designation","Qualification","Experience","Achievement"],
                         list(d)))

        if primary == "exam":
            d = database.get_exams_by_dept(dept or "")
            label = f" — {dept}" if dept else ""
            course_label = f" ({dept} Exam List)" if dept else ""
            return (f"Exam schedule{course_label}: 📅",
                    _tbl(f"📅 Exam Schedule{label}",
                         ["Dept/Sem","Subject","Date","Venue","Duration","Marks"], list(d)))

        if primary == "hostel":
            rows = [(h[0],h[1],f"₹{h[2]}/mo",h[3],h[4],h[5]) for h in database.get_all_hostels()]
            return ("Hostel details: 🏠",
                    _tbl("🏠 Hostel Details — ITM University",
                         ["Hostel Block","Capacity","Rent/Month","AC","Amenities","Food"], rows))

        if primary == "topper":
            year  = extract_year(text)
            d     = (database.get_toppers_by_dept(dept) if dept else
                     database.get_toppers_by_year(year) if year else database.get_topper())
            label = "College Toppers" + (f" — {year}" if year else "") + (f" ({dept})" if dept else "")
            return (f"{label}: 🏆",
                    _tbl(f"🏆 {label}",
                         ["Department","Student Name","CGPA","Year","Award","Benefit"], list(d)))

        if primary == "stats":
            st = database.get_placement_stats()
            return (f"🏫 ITM University at a Glance:\n"
                    f"  📚 Courses: {len(database.get_courses())}  |  "
                    f"👩\u200d🏫 Faculty: {len(database.get_teachers())}\n"
                    f"  🏢 Avg Placement: ₹{st['average_lpa']} LPA  |  "
                    f"Highest: ₹{st['highest_lpa']} LPA\n"
                    f"  🏅 NAAC: A+  |  NIRF Rank: 67  |  ISO 9001:2015 Certified", None)

        tips = random.sample(["courses","fees","placements","faculty","exams","hostel","scholarships"], 3)
        return f"Hmm, not sure 🤔  Try: {', '.join(tips)} — or type 'help'!", None


# ── Theme — Clean, beautiful light-meets-modern design ───────────────────────

C = {
    # Backgrounds — clean white/near-white with soft depth
    "bg":           "#F0F4FF",        # very light blue-white, airy
    "surface":      "#FFFFFF",        # pure white panels
    "surface2":     "#E8EEFF",        # soft chip / hover background
    "border":       "#D0D8F0",        # gentle blue-grey border
    # Accent — ITM brand-inspired deep indigo
    "accent":       "#3A57E8",        # rich indigo blue
    "accent_hover": "#2B45D4",        # deeper on hover
    "accent2":      "#10B981",        # green for "online" status
    "accent_light": "#EEF2FF",        # very pale indigo fill
    # Message bubbles
    "user_bubble":  "#3A57E8",        # indigo user bubble
    "user_text":    "#FFFFFF",
    "bot_bubble":   "#FFFFFF",        # white bot bubble with border
    "bot_border":   "#E0E6FF",
    # Text
    "text":         "#1E2348",        # deep navy text
    "subtext":      "#6B7280",        # muted grey
    "subtext2":     "#9CA3AF",
    # Table
    "table_head":   "#3A57E8",
    "table_head_fg":"#FFFFFF",
    "table_alt":    "#F7F9FF",
    "table_row":    "#FFFFFF",
    "table_sel":    "#C7D2FE",
    "table_sel_fg": "#1E2348",
    # Input
    "input_bg":     "#FFFFFF",
    "input_border": "#C7D2FE",
    "send_btn":     "#3A57E8",
    "send_hover":   "#2B45D4",
    # Header gradient effect (flat)
    "header_bg":    "#FFFFFF",
    "header_border":"#E0E6FF",
}

QUICK = [
    ("🎓 Courses","show all courses"),
    ("💰 Fees","show fee structure"),
    ("🏢 Placements","show placements"),
    ("👩\u200d🏫 Faculty","show all teachers"),
    ("📅 Exams","show exam schedule"),
    ("🏠 Hostel","hostel information"),
    ("🎁 Scholarship","show scholarships"),
    ("📞 Contact","show contact"),
]

# ── UI ────────────────────────────────────────────────────────────────────────

class ChatUI:
    def __init__(self):
        self.bot  = Bot()
        self.root = tk.Tk()
        self.root.title("🎓 ITM University — CollegeBot AI Assistant")
        self.root.geometry("1150x760")
        self.root.minsize(860, 560)
        self.root.configure(bg=C["bg"])
        self._fonts(); self._style(); self._layout(); self._welcome()
        self.root.mainloop()

    def _fonts(self):
        self.fh  = tkfont.Font(family="Segoe UI", size=15, weight="bold")
        self.fh2 = tkfont.Font(family="Segoe UI", size=11)
        self.fm  = tkfont.Font(family="Segoe UI", size=12)
        self.fi  = tkfont.Font(family="Segoe UI", size=12)
        self.fq  = tkfont.Font(family="Segoe UI", size=10, weight="bold")
        self.fs  = tkfont.Font(family="Segoe UI", size=9)
        self.ft  = tkfont.Font(family="Segoe UI", size=10)
        self.fth = tkfont.Font(family="Segoe UI", size=9, weight="bold")
        self.ftag= tkfont.Font(family="Segoe UI", size=9)

    def _style(self):
        s = ttk.Style(self.root)
        s.theme_use("clam")
        s.configure("T.Treeview",
                     background=C["table_row"], foreground=C["text"],
                     fieldbackground=C["table_row"], rowheight=30,
                     font=self.ft, borderwidth=0, relief="flat")
        s.configure("T.Treeview.Heading",
                     background=C["table_head"], foreground=C["table_head_fg"],
                     font=self.fth, relief="flat", borderwidth=0, padding=6)
        s.map("T.Treeview",
              background=[("selected", C["table_sel"])],
              foreground=[("selected", C["table_sel_fg"])])
        s.map("T.Treeview.Heading",
              background=[("active", C["accent_hover"])])

    def _layout(self):
        # ── Header ──────────────────────────────────────────────────────────
        hdr = tk.Frame(self.root, bg=C["header_bg"], height=68)
        hdr.pack(fill=tk.X); hdr.pack_propagate(False)

        # Left logo area
        logo_frame = tk.Frame(hdr, bg=C["header_bg"]); logo_frame.pack(side=tk.LEFT, padx=(14,0), pady=8)
        # Circle avatar
        canvas_av = tk.Canvas(logo_frame, width=46, height=46, bg=C["header_bg"],
                               highlightthickness=0)
        canvas_av.pack(side=tk.LEFT, padx=(0,10))
        canvas_av.create_oval(2, 2, 44, 44, fill=C["accent"], outline="")
        canvas_av.create_text(23, 23, text="🤖", font=("Segoe UI Emoji", 18))

        tf = tk.Frame(hdr, bg=C["header_bg"]); tf.pack(side=tk.LEFT, pady=10)
        tk.Label(tf, text="CollegeBot  ·  ITM University",
                 font=self.fh, bg=C["header_bg"], fg=C["text"]).pack(anchor="w")
        tk.Label(tf, text="● Online  |  NAAC A+  |  NIRF Rank 67  |  Indore, MP",
                 font=self.fs, bg=C["header_bg"], fg=C["accent2"]).pack(anchor="w")

        # Help button right
        hl = tk.Label(hdr, text="  Help  ", font=self.fq,
                      bg=C["accent_light"], fg=C["accent"],
                      cursor="hand2", padx=10, pady=7, relief=tk.FLAT)
        hl.pack(side=tk.RIGHT, padx=16, pady=16)
        hl.bind("<Button-1>", lambda e: self._inject("help"))
        hl.bind("<Enter>",    lambda e: hl.config(bg=C["accent"], fg=C["surface"]))
        hl.bind("<Leave>",    lambda e: hl.config(bg=C["accent_light"], fg=C["accent"]))

        tk.Frame(self.root, bg=C["header_border"], height=1).pack(fill=tk.X)

        # ── Quick Chips ─────────────────────────────────────────────────────
        qf = tk.Frame(self.root, bg=C["surface"], pady=8); qf.pack(fill=tk.X, padx=0)
        for lbl, q in QUICK:
            b = tk.Label(qf, text=lbl, font=self.ftag,
                         bg=C["surface2"], fg=C["accent"],
                         padx=11, pady=6, cursor="hand2",
                         relief=tk.FLAT)
            b.pack(side=tk.LEFT, padx=5)
            b.bind("<Button-1>", lambda e, qq=q: self._inject(qq))
            b.bind("<Enter>",    lambda e, w=b: w.config(fg=C["surface"], bg=C["accent"]))
            b.bind("<Leave>",    lambda e, w=b: w.config(fg=C["accent"], bg=C["surface2"]))

        tk.Frame(self.root, bg=C["border"], height=1).pack(fill=tk.X)

        # ── Chat Canvas ─────────────────────────────────────────────────────
        cc = tk.Frame(self.root, bg=C["bg"]); cc.pack(fill=tk.BOTH, expand=True)
        self.canvas = tk.Canvas(cc, bg=C["bg"], highlightthickness=0)
        vsb = tk.Scrollbar(cc, orient="vertical", command=self.canvas.yview,
                           bg=C["surface2"], troughcolor=C["bg"], width=8)
        self.canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.mf  = tk.Frame(self.canvas, bg=C["bg"])
        self._cw = self.canvas.create_window((0,0), window=self.mf, anchor="nw")
        self.mf.bind("<Configure>",
                     lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>",
                         lambda e: self.canvas.itemconfig(self._cw, width=e.width))
        self.canvas.bind_all("<MouseWheel>",
                             lambda e: self.canvas.yview_scroll(-1*(e.delta//120),"units"))

        # ── Input Bar ───────────────────────────────────────────────────────
        tk.Frame(self.root, bg=C["border"], height=1).pack(fill=tk.X)
        ib = tk.Frame(self.root, bg=C["surface"], pady=10); ib.pack(fill=tk.X)

        # Entry wrapper with rounded-feel border
        ew = tk.Frame(ib, bg=C["input_border"], padx=2, pady=2)
        ew.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(14,8))
        ei = tk.Frame(ew, bg=C["input_bg"])
        ei.pack(fill=tk.X)

        self.evar = tk.StringVar()
        self.ent  = tk.Entry(ei, textvariable=self.evar, font=self.fi,
                             bg=C["input_bg"], fg=C["text"],
                             insertbackground=C["accent"],
                             relief=tk.FLAT, bd=0)
        self.ent.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, ipady=9)
        self.ent.bind("<Return>", lambda e: self._send())
        self._ph = "Ask me anything about ITM University…"
        self.ent.insert(0, self._ph); self.ent.config(fg=C["subtext"])
        self.ent.bind("<FocusIn>",  self._cph)
        self.ent.bind("<FocusOut>", self._sph)

        sb = tk.Button(ib, text="Send ➤", font=self.fq,
                       bg=C["send_btn"], fg="white",
                       relief=tk.FLAT, padx=18, pady=11,
                       cursor="hand2", command=self._send, bd=0)
        sb.pack(side=tk.RIGHT, padx=14)
        sb.bind("<Enter>", lambda e: sb.config(bg=C["send_hover"]))
        sb.bind("<Leave>", lambda e: sb.config(bg=C["send_btn"]))

        # Status bar
        self.sv = tk.StringVar(value="Ready  •  ITM University CollegeBot")
        tk.Label(self.root, textvariable=self.sv, font=self.fs,
                 bg=C["bg"], fg=C["subtext2"]).pack(anchor="e", padx=14, pady=(0,4))

    def _cph(self, _):
        if self.ent.get() == self._ph:
            self.ent.delete(0, tk.END); self.ent.config(fg=C["text"])

    def _sph(self, _):
        if not self.ent.get():
            self.ent.insert(0, self._ph); self.ent.config(fg=C["subtext"])

    def _sb(self):
        self.canvas.update_idletasks(); self.canvas.yview_moveto(1.0)

    def _bubble(self, text, is_user):
        row = tk.Frame(self.mf, bg=C["bg"]); row.pack(fill=tk.X, padx=12, pady=(5,1))
        ts  = time.strftime("%H:%M")
        if is_user:
            tk.Frame(row, bg=C["bg"]).pack(side=tk.LEFT, expand=True)
            col = tk.Frame(row, bg=C["bg"]); col.pack(side=tk.RIGHT)
            bubble = tk.Frame(col, bg=C["user_bubble"],
                               padx=2, pady=2)
            bubble.pack(anchor="e")
            tk.Label(bubble, text=text, font=self.fm,
                     bg=C["user_bubble"], fg=C["user_text"],
                     wraplength=540, padx=12, pady=8,
                     justify=tk.LEFT).pack()
            tk.Label(col, text=f"You  •  {ts}", font=self.fs,
                     bg=C["bg"], fg=C["subtext2"]).pack(anchor="e", padx=4, pady=(1,3))
        else:
            col = tk.Frame(row, bg=C["bg"]); col.pack(side=tk.LEFT)
            # Bot avatar circle
            av = tk.Canvas(col, width=34, height=34, bg=C["bg"], highlightthickness=0)
            av.pack(side=tk.LEFT, anchor="n", padx=(0,8), pady=4)
            av.create_oval(2, 2, 32, 32, fill=C["accent"], outline="")
            av.create_text(17, 17, text="🤖", font=("Segoe UI Emoji",12))

            mc = tk.Frame(col, bg=C["bg"]); mc.pack(side=tk.LEFT)
            # White bubble with border
            bframe = tk.Frame(mc, bg=C["bot_border"], padx=1, pady=1)
            bframe.pack(anchor="w")
            tk.Label(bframe, text=text, font=self.fm,
                     bg=C["bot_bubble"], fg=C["text"],
                     wraplength=640, padx=12, pady=9,
                     justify=tk.LEFT).pack()
            tk.Label(mc, text=f"CollegeBot  •  {ts}", font=self.fs,
                     bg=C["bg"], fg=C["subtext2"]).pack(anchor="w", padx=4, pady=(1,3))
        self._sb()

    def _table(self, td):
        if not td or not td.get("rows"):
            self._bubble("⚠️ No data found.", False); return
        wrap = tk.Frame(self.mf, bg=C["bg"], pady=6); wrap.pack(fill=tk.X, padx=14)

        # Table title bar
        tbar = tk.Frame(wrap, bg=C["surface"], pady=7,
                         highlightbackground=C["border"], highlightthickness=1)
        tbar.pack(fill=tk.X)
        tk.Label(tbar, text=td["title"], font=self.fth,
                 bg=C["surface"], fg=C["accent"], padx=12).pack(side=tk.LEFT)
        tk.Label(tbar, text=f"  {len(td['rows'])} records", font=self.fs,
                 bg=C["surface"], fg=C["subtext"], padx=8).pack(side=tk.RIGHT)

        tvf  = tk.Frame(wrap, bg=C["bg"],
                         highlightbackground=C["border"], highlightthickness=1)
        tvf.pack(fill=tk.X)
        cols = td["columns"]
        tv   = ttk.Treeview(tvf, columns=cols, show="headings",
                             style="T.Treeview", height=min(len(td["rows"]),12))
        xsb  = tk.Scrollbar(tvf, orient="horizontal", command=tv.xview,
                             bg=C["surface2"], troughcolor=C["bg"], width=8)
        ysb  = tk.Scrollbar(tvf, orient="vertical",   command=tv.yview,
                             bg=C["surface2"], troughcolor=C["bg"], width=8)
        tv.configure(xscrollcommand=xsb.set, yscrollcommand=ysb.set)
        for i, col in enumerate(cols):
            vals = [str(r[i]) if i < len(r) else "" for r in td["rows"]]
            w    = min(max(len(col)*9, max((len(v) for v in vals), default=0)*7, 80), 300)
            tv.heading(col, text=col, command=lambda c=col: self._sort(tv, c, cols))
            tv.column(col, width=w, minwidth=60, stretch=True)
        tv.tag_configure("even", background=C["table_row"])
        tv.tag_configure("odd",  background=C["table_alt"])
        for i, row in enumerate(td["rows"]):
            tv.insert("", tk.END, values=row, tags=("even" if i%2==0 else "odd",))
        ysb.pack(side=tk.RIGHT, fill=tk.Y)
        tv.pack(side=tk.LEFT, fill=tk.X, expand=True)
        xsb.pack(fill=tk.X)
        tk.Label(wrap, text=f"CollegeBot  •  {time.strftime('%H:%M')}  ↕ Click headers to sort",
                 font=self.fs, bg=C["bg"], fg=C["subtext2"]).pack(anchor="w", padx=4, pady=(2,4))
        self._sb()

    def _sort(self, tv, col, cols):
        items = [(tv.set(k, col), k) for k in tv.get_children("")]
        try:    items.sort(key=lambda t: float(t[0].replace("₹","").replace(",","").replace(" LPA","").replace("/mo","").strip()))
        except: items.sort(key=lambda t: t[0].lower())
        for i, (_, k) in enumerate(items):
            tv.move(k, "", i); tv.item(k, tags=("even" if i%2==0 else "odd",))

    def _typing(self):
        row = tk.Frame(self.mf, bg=C["bg"]); row.pack(fill=tk.X, padx=14, pady=4)
        inner = tk.Frame(row, bg=C["bg"]); inner.pack(side=tk.LEFT)
        av = tk.Canvas(inner, width=34, height=34, bg=C["bg"], highlightthickness=0)
        av.pack(side=tk.LEFT, anchor="n", padx=(0,8))
        av.create_oval(2, 2, 32, 32, fill=C["accent"], outline="")
        av.create_text(17, 17, text="🤖", font=("Segoe UI Emoji",12))
        tk.Label(inner, text="CollegeBot is thinking…  ●●●",
                 font=self.fs, bg=C["bg"], fg=C["subtext"]).pack(side=tk.LEFT, pady=10)
        self._sb(); return row

    def _inject(self, q):
        self.ent.delete(0, tk.END); self.ent.config(fg=C["text"])
        self.ent.insert(0, q); self._send()

    def _send(self):
        raw = self.ent.get().strip()
        if not raw or raw == self._ph: return
        self.ent.delete(0, tk.END); self.ent.config(fg=C["text"])
        self._bubble(raw, True)
        self.sv.set("CollegeBot is thinking…")
        threading.Thread(target=self._reply, args=(raw,), daemon=True).start()

    def _reply(self, text):
        typ = self._typing()
        time.sleep(0.4 + min(len(text)*0.01, 0.9))
        resp, tbl = self.bot.respond(text)
        typ.destroy(); self._bubble(resp, False)
        if tbl: self._table(tbl)
        self.sv.set("Ready  •  ITM University CollegeBot")

    def _welcome(self): self._bubble(WELCOME, False)


if __name__ == "__main__":
    ChatUI()
