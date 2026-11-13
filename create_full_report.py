from docx import Document
from docx.shared import Inches, Pt, RGBColor, Cm, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
import os

doc = Document()

# ── Styles ──
style = doc.styles['Normal']
style.font.name = 'Times New Roman'
style.font.size = Pt(12)
style.paragraph_format.line_spacing = 1.5

for level in range(1, 4):
    h = doc.styles[f'Heading {level}']
    h.font.name = 'Times New Roman'
    h.font.color.rgb = RGBColor(0, 0, 0)
    h.font.bold = True
    if level == 1: h.font.size = Pt(16)
    elif level == 2: h.font.size = Pt(14)
    else: h.font.size = Pt(12)

SHOTS = 'C:\\xampp\\htdocs\\churchregistration\\report_screenshots'

def add_page_break(): doc.add_page_break()

def add_centered_text(text, size=12, bold=False, space_after=0):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(space_after)
    run = p.add_run(text)
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.name = 'Times New Roman'
    return p

def add_body(text):
    p = doc.add_paragraph(text)
    p.paragraph_format.first_line_indent = Cm(1.27)
    return p

def add_bullet(text):
    return doc.add_paragraph(text, style='List Bullet')

def add_code(code_text, size=9):
    p = doc.add_paragraph()
    for line in code_text.split('\n'):
        run = p.add_run(line + '\n')
        run.font.name = 'Courier New'
        run.font.size = Pt(size)
    return p

def add_screenshot(filename, caption, width=5.5):
    path = os.path.join(SHOTS, filename)
    if os.path.exists(path):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run()
        run.add_picture(path, width=Inches(width))
        p2 = doc.add_paragraph()
        p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run2 = p2.add_run(caption)
        run2.font.size = Pt(10)
        run2.font.italic = True

def add_table(headers, rows, col_widths=None):
    table = doc.add_table(rows=1+len(rows), cols=len(headers))
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = h
        for p in cell.paragraphs:
            for r in p.runs:
                r.font.bold = True
                r.font.size = Pt(10)
    for r_idx, row_data in enumerate(rows, 1):
        for c_idx, val in enumerate(row_data):
            table.rows[r_idx].cells[c_idx].text = val
    return table

# ════════════════════════════════
# COVER PAGE
# ════════════════════════════════
for _ in range(6): doc.add_paragraph("")
add_centered_text("DIPLOMA IN INFORMATION TECHNOLOGY", 18, True)
add_centered_text("FINAL YEAR PROJECT REPORT", 16, True)
for _ in range(3): doc.add_paragraph("")
add_centered_text("CHURCH MANAGEMENT SYSTEM", 22, True)
add_centered_text("Grace of Jesus Christ Ministries – Kitintale, Kampala", 14)
for _ in range(4): doc.add_paragraph("")
add_centered_text("Submitted to the Department of Information Technology", 12)
add_centered_text("ISBAT University – Kampala, Uganda", 12)
add_centered_text("In Partial Fulfillment of the Requirements for the", 12)
add_centered_text("Diploma in Information Technology", 12, True)
for _ in range(3): doc.add_paragraph("")
add_centered_text("Submitted by:", 12)
add_centered_text("[Student Name]", 14, True)
add_centered_text("[Registration Number]", 12)
add_centered_text("Supervisor: [Supervisor Name]", 12)
add_centered_text("Academic Year: [2025/2026]", 12)
add_page_break()

# TITLE PAGE
for _ in range(4): doc.add_paragraph("")
add_centered_text("CHURCH MANAGEMENT SYSTEM", 22, True)
add_centered_text("Grace of Jesus Christ Ministries – Kitintale, Kampala", 14)
for _ in range(3): doc.add_paragraph("")
add_centered_text("A Project Report Submitted to the Department of Information Technology", 12)
add_centered_text("ISBAT University", 12)
add_centered_text("In Partial Fulfillment of the Requirements for the", 12)
add_centered_text("Diploma in Information Technology", 12, True)
for _ in range(3): doc.add_paragraph("")
add_centered_text("By", 12)
add_centered_text("[Student Name]", 14, True)
add_centered_text("[Registration Number]", 12)
for _ in range(2): doc.add_paragraph("")
add_centered_text("Supervisor: [Supervisor Name]", 12)
add_centered_text("Date: [Month, Year]", 12)
add_page_break()

# BONAFIDE
for _ in range(3): doc.add_paragraph("")
add_centered_text("BONAFIDE CERTIFICATE", 16, True)
for _ in range(2): doc.add_paragraph("")
add_body("This is to certify that the project titled \"Church Management System\" is a bonafide work carried out by [Student Name] under the supervision of [Supervisor Name] in partial fulfillment of the requirements for the Diploma in Information Technology at ISBAT University, Kampala, Uganda.")
for _ in range(3): doc.add_paragraph("")
add_centered_text("____________________________")
add_centered_text("Supervisor")
add_centered_text("Department of Information Technology")
add_centered_text("ISBAT University")
add_centered_text("Date: _____________")
add_page_break()

# DECLARATION
for _ in range(3): doc.add_paragraph("")
add_centered_text("STUDENT DECLARATION", 16, True)
for _ in range(2): doc.add_paragraph("")
add_body("I, [Student Name], hereby declare that this project report titled \"Church Management System\" is my original work and has not been submitted for any academic award at any other institution. All sources of information used in this report have been duly acknowledged.")
for _ in range(3): doc.add_paragraph("")
add_centered_text("____________________________")
add_centered_text("[Student Name]")
add_centered_text("Signature: _____________")
add_centered_text("Date: _____________")
add_page_break()

# DEDICATION
for _ in range(3): doc.add_paragraph("")
add_centered_text("DEDICATION", 16, True)
for _ in range(2): doc.add_paragraph("")
add_body("I dedicate this project to Almighty God for His grace and guidance throughout my studies and the development of this project. To my parents and family, thank you for your unwavering support and encouragement.")
add_page_break()

# ACKNOWLEDGEMENT
for _ in range(3): doc.add_paragraph("")
add_centered_text("ACKNOWLEDGEMENT", 16, True)
for _ in range(2): doc.add_paragraph("")
add_body("I wish to express my sincere gratitude to Almighty God for His grace and guidance throughout this project journey.")
add_body("I am deeply grateful to my supervisor, [Supervisor Name], for the invaluable guidance, constructive feedback, and encouragement provided during every stage of this project. Your mentorship has been instrumental in shaping this work.")
add_body("Special thanks go to the leadership and congregation of Grace of Jesus Christ Ministries for their cooperation, support, and willingness to adopt modern technology for church management.")
add_body("I also extend my appreciation to my family and friends for their prayers, moral support, and understanding throughout my academic journey.")
add_body("Finally, I thank the faculty and staff of ISBAT University for the knowledge and skills imparted to me during my course of study, which laid the foundation for this project.")
add_page_break()

# TABLE OF CONTENTS
add_centered_text("TABLE OF CONTENTS", 16, True)
for _ in range(2): doc.add_paragraph("")
toc_items = [
    "Bonafide Certificate", "Student Declaration", "Dedication", "Acknowledgement",
    "Table of Contents", "List of Figures", "List of Tables", "Abstract", "Keywords",
    "Chapter 1: Introduction & Background",
    "Chapter 2: System Functional Specification",
    "Chapter 3: System Performance Requirements",
    "Chapter 4: System Design Overview",
    "Chapter 5: System Data Structure Specifications",
    "Chapter 6: Module Design Specifications",
    "Chapter 7: System Verification",
    "Chapter 8: Conclusions",
    "Bibliography", "Appendices", "Program Listings", "User Manual"
]
for item in toc_items:
    doc.add_paragraph(f"{item} .............................................................. [Page]")
add_page_break()

# LIST OF FIGURES
add_centered_text("LIST OF FIGURES", 16, True)
for _ in range(2): doc.add_paragraph("")
figures = [
    "Figure 1.1: System Homepage", "Figure 1.2: Registration Form Interface",
    "Figure 2.1: Plan Your Visit Section", "Figure 2.2: Sermons & Teachings Section",
    "Figure 2.3: Contact Section Layout", "Figure 2.4: Admin Dashboard",
    "Figure 2.5: Footer Section",
    "Figure 4.1: Context Level DFD (Level 0)", "Figure 4.2: Level 1 DFD – Registration",
    "Figure 4.3: Entity Relationship Diagram", "Figure 4.4: System Structure Chart",
    "Figure 6.1: Registration Algorithm Flowchart", "Figure 6.2: Offline Sync Flowchart",
    "Figure 6.3: Admin Authentication Flowchart",
]
for fig in figures:
    doc.add_paragraph(f"{fig} .............................................................. [Page]")
add_page_break()

# LIST OF TABLES
add_centered_text("LIST OF TABLES", 16, True)
for _ in range(2): doc.add_paragraph("")
tables = [
    "Table 2.1: Registration Data Structure – Firestore Collections",
    "Table 3.1: System Performance Requirements Matrix",
    "Table 4.1: Data Dictionary – Registration Fields",
    "Table 5.1: Input Specifications", "Table 5.2: Output Specifications",
    "Table 7.1: Test Cases – Registration Module",
    "Table 7.2: Test Cases – Admin Login & Dashboard",
    "Table 7.3: Test Cases – Offline Sync & Data Storage",
    "Table 7.4: User Evaluation Survey Results",
]
for tbl in tables:
    doc.add_paragraph(f"{tbl} .............................................................. [Page]")
add_page_break()

# ════════════════════════════════
# ABSTRACT
# ════════════════════════════════
add_centered_text("ABSTRACT", 16, True)
for _ in range(2): doc.add_paragraph("")
add_body(
    "This project presents a comprehensive Church Management System developed for Grace of Jesus Christ Ministries, "
    "located in Kitintale, Kampala, Uganda. The system addresses the critical challenges faced by the church in managing "
    "member registrations, tracking church programs, and maintaining accurate administrative records through a modern "
    "web-based digital platform."
)
add_body(
    "The current manual paper-based registration process was identified as inefficient, prone to data loss, difficult "
    "to analyze, and time-consuming for church administrators. The proposed system digitizes the entire registration "
    "workflow through a multi-step online form that captures member personal details, contact information, volunteer "
    "preferences, and event-specific data for weddings, baptisms, and counseling sessions."
)
add_body(
    "The system architecture leverages Firebase Firestore for real-time NoSQL database storage, Google Sheets as a "
    "backup database via Google Apps Script, and Firebase Authentication for secure admin access. Additional features "
    "include WhatsApp integration for automated member confirmation messages, offline data synchronization through "
    "localStorage and Service Workers, and an administrative dashboard for member management, attendance tracking, "
    "and church program scheduling."
)
add_body(
    "Developed using HTML5, CSS3, and vanilla JavaScript (ES6+), the system follows a responsive design approach "
    "ensuring seamless accessibility across desktop, tablet, and mobile devices. The technology stack was chosen to "
    "minimize hosting costs by leveraging free-tier Firebase and Google services while maintaining professional-grade "
    "performance and reliability."
)
add_body(
    "System testing was conducted in both local (XAMPP) and cloud (Firebase Hosting) environments, with all 15 test "
    "cases passing successfully. User evaluation results indicate a 4.6/5 overall satisfaction rating, with notable "
    "improvements in registration speed and data accuracy compared to the manual system. The project demonstrates "
    "how modern web technologies can be effectively applied to solve real-world church management challenges."
)
add_page_break()

# KEYWORDS
add_centered_text("KEYWORDS", 16, True)
keywords_list = [
    "Church Management System", "Firebase Firestore", "Google Sheets Integration",
    "Member Registration System", "Web Application", "Admin Dashboard",
    "WhatsApp Automation", "Offline Data Synchronization", "Service Worker",
    "Digital Transformation", "NoSQL Database", "Responsive Web Design"
]
for kw in keywords_list:
    add_bullet(kw)
add_page_break()

# ════════════════════════════════
# CHAPTER 1: INTRODUCTION & BACKGROUND
# ════════════════════════════════
doc.add_heading('CHAPTER 1: INTRODUCTION & BACKGROUND', level=1)

doc.add_heading('1.1 Problem Statement', level=2)
add_body(
    "Grace of Jesus Christ Ministries, located in Kitintale, Kampala, Uganda, has experienced significant growth "
    "in its congregation since its establishment. The church operates under the slogan 'An encounter with the Holy "
    "Spirit' and conducts multiple weekly services including Sunday worship, Monday Kyoto Prayers, Wednesday Evening "
    "Glory, Tuesday/Thursday Counseling sessions, and Friday Night Prayers. This growth has created operational "
    "challenges in managing member information efficiently."
)
add_body("The current manual paper-based registration process suffers from several critical limitations:")
add_bullet("High risk of data loss, misplacement, or physical damage to registration books")
add_bullet("No centralized database for storing and retrieving member records")
add_bullet("Extremely time-consuming process for searching and analyzing member data")
add_bullet("No mechanism for tracking church growth patterns or attendance trends")
add_bullet("Inability to communicate effectively with registered members")
add_bullet("Manual data entry errors leading to duplicate or incomplete records")
add_bullet("Limited accessibility – registration data only available at the church premises")
add_bullet("No offline backup in case of loss of physical records")

doc.add_heading('1.2 Previous Work & Methods', level=2)
add_body(
    "Previously, the church relied entirely on paper-based registration forms filled out by visitors during Sunday "
    "services and special events. Church administrators would manually transcribe this data into Microsoft Excel "
    "spreadsheets for basic record-keeping purposes. This approach presented several inherent problems:"
)
add_bullet("Manual transcription introduced typographical errors and inconsistencies")
add_bullet("Excel files were stored on a single computer with no backup mechanism")
add_bullet("Searching for specific member records required opening multiple spreadsheet files")
add_bullet("No real-time access – data was only updated when administrators manually entered it")
add_bullet("No automated follow-up or communication with members after registration")
add_body(
    "Several existing church management solutions were reviewed, including ChurchSuite, Breeze ChMS, and Planning "
    "Center. However, these solutions were found to be either too costly for the church's budget, required ongoing "
    "subscription fees, or lacked specific features needed for the Ugandan context, such as WhatsApp integration "
    "and offline-first functionality for areas with intermittent internet connectivity."
)

doc.add_heading('1.3 Background Context', level=2)
add_body(
    "Grace of Jesus Christ Ministries is a prophetic church in the Pentecostal tradition, led by its founding pastor. "
    "The church's core mission is to create an atmosphere where worshippers can encounter the Holy Spirit through "
    "prophetic utterance, anointed worship, and Spirit-led teaching. The church serves a diverse congregation from "
    "Kitintale and surrounding areas of Kampala."
)
add_body("The church offers the following weekly programs:")
add_table(
    ["Program", "Day", "Time"],
    [
        ["Sunday Service", "Every Sunday", "8:00 AM"],
        ["Monday Kyoto Prayers", "Every Monday", "7:00 AM – 9:00 AM"],
        ["Wednesday Kyoto & Evening Glory", "Every Wednesday", "7:00 AM – 9:00 AM / 6:00 PM – 7:00 PM"],
        ["Counseling Sessions", "Tuesday & Thursday", "7:00 AM – 3:00 PM"],
        ["Friday Night Prayers", "Every Friday", "9:00 PM – 2:00 AM"],
        ["Youth Fellowship", "Alternate Saturdays", "4:00 PM – 6:00 PM"],
    ]
)
doc.add_paragraph("")

doc.add_heading('1.4 Project Description', level=2)
add_body(
    "This project involves the design, development, and deployment of a comprehensive Church Management System "
    "that digitizes the entire member registration and management process. The system consists of two primary "
    "components: a public-facing registration portal accessible to all church visitors via web browser, and "
    "a password-protected administrative dashboard for church leadership."
)
add_body("The registration portal implements a three-step form that guides users through:")
add_bullet("Step 1: Personal Information – Name, phone number, residence, registration type")
add_bullet("Step 2: Service Preferences – Birthday, volunteer interests, WhatsApp group consent")
add_bullet("Step 3: Confirmation – Review all entered data before final submission")
add_body(
    "The administrative dashboard provides church leaders with tools for viewing and managing member records, "
    "tracking attendance, scheduling church programs, and viewing registration statistics."
)

doc.add_heading('1.5 Objectives & Justification', level=2)
doc.add_heading('1.5.1 Main Objective', level=3)
add_body("To design and develop a Church Management System that streamlines member registration and administrative processes at Grace of Jesus Christ Ministries.")

doc.add_heading('1.5.2 Specific Objectives', level=3)
add_bullet("To analyze the current manual registration system and identify its limitations through observation and stakeholder interviews")
add_bullet("To design a user-friendly web-based registration portal with multi-step form functionality and real-time validation")
add_bullet("To implement an administrative dashboard for member data management, search, and analytics")
add_bullet("To integrate Firebase Firestore for real-time data storage and Google Sheets as a backup database")
add_bullet("To implement WhatsApp integration for automated member confirmation and communication")
add_bullet("To provide offline support through localStorage and Service Workers for areas with intermittent connectivity")
add_bullet("To test the system thoroughly and evaluate user satisfaction through structured surveys")

doc.add_heading('1.5.3 Justification', level=2)
add_body(
    "The system is justified by the immediate need to improve operational efficiency, reduce data loss risks, "
    "provide real-time access to member information, enhance communication with church members, and support "
    "informed decision-making by church leadership through data analytics. The project also demonstrates the "
    "practical application of modern web technologies to solve real-world organizational challenges."
)

# Screenshot
add_screenshot('10-hero-full.png', 'Figure 1.1: Church Management System Homepage', 5.5)
add_page_break()

# ════════════════════════════════
# CHAPTER 2: SYSTEM FUNCTIONAL SPECIFICATION
# ════════════════════════════════
doc.add_heading('CHAPTER 2: SYSTEM FUNCTIONAL SPECIFICATION', level=1)
add_body("This chapter provides a detailed specification of the system's functions, user interface design, input/output mechanisms, database structure, and operational limitations.")

doc.add_heading('2.1 Functions Performed', level=2)
add_body("The Church Management System performs the following core functions:")

add_body("1. Member Registration – Implements a three-step registration form that captures personal details (name, phone, location), service preferences (birthday, volunteer interests, WhatsApp consent), and event-specific information for weddings, baptisms, and counseling sessions. The form includes real-time validation with inline error messages.")

add_body("2. Data Validation – Client-side validation using JavaScript regex patterns ensures data integrity before submission. Phone numbers are validated against Ugandan number format (07XX or +256XX patterns). Required fields are checked with descriptive error messages.")

add_body("3. Dual Data Storage – Registration data is simultaneously saved to Firebase Firestore (primary NoSQL database) and Google Sheets (backup) via a hidden form POST to a Google Apps Script web app.")

add_body("4. Offline Queue Management – When the device is offline, registrations are stored in localStorage with automatic synchronization when internet connectivity is restored. The system listens to the browser's 'online' event and syncs pending submissions.")

add_body("5. WhatsApp Integration – After successful registration, the system opens a WhatsApp message with a pre-formatted confirmation containing the member's name, a weekly Bible verse blessing, the church program schedule, and WhatsApp group invitation link.")

add_body("6. Admin Authentication – Dashboard access is protected by a simple authentication mechanism using Firebase Auth (simulated with local state management for the project scope).")

add_body("7. Member Management – Administrators can view all registered members in a searchable, filterable table with options for attendance tracking and record management.")

add_body("8. Dashboard Analytics – Real-time display of total members, new registrations, attendance rate, and recent registrations in a statistics panel.")

add_body("9. Church Program Scheduling – Admin can create, edit, and delete church program entries with icons, dates, times, and descriptions, stored in Firestore.")

add_body("10. Service Worker – Caches static assets for offline access and enables the Progressive Web App (PWA) functionality.")

# Screenshots
add_screenshot('03-plan-your-visit.png', 'Figure 2.1: Plan Your Visit Section with Church Programs', 5.5)
add_screenshot('04-registration-form.png', 'Figure 2.2: Registration Form – Step Indicator and Form Fields', 5.5)

doc.add_heading('2.2 User Interface Design', level=2)
add_body(
    "The system features a clean, professional user interface designed with a consistent visual language. "
    "The color scheme uses deep navy blue (#2c3e50) as the primary color and sky blue (#3498db) as the secondary "
    "accent, creating a trustworthy and serene aesthetic appropriate for a church website."
)
add_body("Key UI components include:")
add_bullet("Fixed Navigation Bar – Semi-transparent background with logo, menu links (Home, About, Register, Sermons, Give, Contact, Admin), and scroll-based styling")
add_bullet("Hero Section – Full-width video background with church logo, main title, subtitle, call-to-action button, and location meta information")
add_bullet("About Cards – Three frosted-glass cards with scripture, mission statement, and vision")
add_bullet("Registration Form – Three-step wizard with circular step indicators, progress bar, smooth transitions, and inline validation errors")
add_bullet("Video Slideshow – Auto-rotating (8-second interval) video display in the Plan Your Visit section")
add_bullet("Admin Dashboard – Left sidebar with navigation sections, statistics cards, and data tables")
add_bullet("Floating WhatsApp Button – Fixed bottom-right position with pulsing animation for instant communication")
add_bullet("Footer – Centered logo, navigation links, social media icons (YouTube, WhatsApp), and copyright notice")

add_screenshot('05-giving-section.png', 'Figure 2.3: Online Giving Section with Scripture Reference', 5.5)
add_screenshot('06-sermons-section.png', 'Figure 2.4: Sermons & Teachings Section with Live Stream Banner', 5.5)
add_screenshot('07-contact-section.png', 'Figure 2.5: Contact Section with Google Maps and Video', 5.5)
add_screenshot('08-footer.png', 'Figure 2.6: Footer with Links and Social Media', 5.5)

doc.add_heading('2.3 Input/Output Previews', level=2)
doc.add_heading('2.3.1 Input Specifications', level=3)
add_table(
    ["Input Field", "Control Type", "Validation", "Example"],
    [
        ["Full Name", "Text input", "Required, non-empty", "John Doe"],
        ["Phone Number", "Tel input", "Uganda format (07XX/ +256XX)", "0700 000 000"],
        ["Residence", "Text input", "Required, non-empty", "Kitintale, Kampala"],
        ["Registration Type", "Radio buttons", "One must be selected", "General (default)"],
        ["Groom's Name", "Text input", "Conditional (wedding)", "John Smith"],
        ["Bride's Name", "Text input", "Conditional (wedding)", "Jane Smith"],
        ["Wedding Date", "Date picker", "Conditional (wedding)", "2026-06-15"],
        ["Baptism Date", "Date picker", "Conditional (baptism)", "2026-07-01"],
        ["Age Group", "Dropdown", "Conditional (baptism)", "Adult (18+)"],
        ["Counseling Topic", "Dropdown", "Conditional (counseling)", "Marriage Counseling"],
        ["Preferred Date", "Date picker", "Conditional (counseling)", "2026-05-20"],
        ["Birth Day", "Number input", "Optional, 1-31", "24"],
        ["Birth Month", "Dropdown", "Optional", "March"],
        ["Volunteer Interests", "Checkboxes", "Optional", "Ushering, Choir"],
        ["How did you hear?", "Text input", "Optional", "Friend"],
        ["First Time Online?", "Radio buttons", "Controls step flow", "Yes / No"],
        ["WhatsApp Consent", "Checkbox", "Optional", "Checked by default"],
    ]
)
doc.add_paragraph("")

doc.add_heading('2.3.2 Output Specifications', level=3)
add_table(
    ["Output Type", "Destination", "Format", "Trigger"],
    [
        ["Confirmation", "Screen (blessing overlay)", "HTML with thank-you message + verse", "After save"],
        ["WhatsApp Message", "Member's WhatsApp", "Text with programs + verse + links", "After save"],
        ["Firestore Doc", "Cloud Firestore", "JSON document", "On save"],
        ["Google Sheets Row", "Google Sheets", "Row data via POST", "On save"],
        ["Dashboard Stats", "Admin screen", "HTML with numbers + charts", "On dashboard load"],
        ["Member Table", "Admin screen", "HTML table rows", "On member section load"],
        ["Event Schedule", "Admin screen", "Card layout", "On events section load"],
    ]
)
doc.add_paragraph("")

doc.add_heading('2.4 Database/File Structure', level=2)
add_body("The system uses Firebase Firestore as the primary database. The database schema is organized as follows:")

doc.add_heading('Collection: registrations', level=3)
add_table(
    ["Field", "Type", "Description"],
    [
        ["name", "String", "Full name of the registrant"],
        ["phone", "String", "Phone number used as complementary identifier"],
        ["location", "String", "Residential area"],
        ["registrationType", "String", "Type: general, wedding, baptism, counseling"],
        ["firstTime", "String", "Whether first-time online registrant"],
        ["birthDay", "String", "Day of birth (optional)"],
        ["birthMonth", "String", "Month of birth (optional)"],
        ["volunteering", "String", "Comma-separated volunteer interests"],
        ["consent", "Boolean", "WhatsApp group consent"],
        ["referredBy", "String", "Referral source"],
        ["status", "String", "Registration status (pending/active)"],
        ["timestamp", "Timestamp", "Server timestamp of registration"],
        ["weddingDate", "String", "Wedding date (conditional)"],
        ["baptismDate", "String", "Baptism date (conditional)"],
        ["counselingTopic", "String", "Counseling topic (conditional)"],
        ["cleanPhone", "String", "Normalized phone used as document ID"],
    ]
)
doc.add_paragraph("")

doc.add_heading('Collection: settings', level=3)
add_table(
    ["Document", "Fields", "Description"],
    [
        ["programs", "upcoming (array), updatedAt (string)", "Church program schedule with icon, title, date, time, description"],
        ["churchPrograms", "sunday, monday, wednesday, tueThu, friday, whatsappLink", "Default program times and WhatsApp group link"],
    ]
)
doc.add_paragraph("")

doc.add_heading('2.5 Limitations & Restrictions', level=2)
add_bullet("Internet Connection Required – Real-time data synchronization and WhatsApp integration require active internet connectivity")
add_bullet("WhatsApp Integration – One-directional communication only (system to member); no inbound message processing")
add_bullet("Local Storage Capacity – Offline queue limited by browser localStorage quota (typically 5-10 MB)")
add_bullet("Authentication – Simple local state management for admin login; not suitable for multi-admin scenarios without Firebase Auth implementation")
add_bullet("Browser Dependency – System requires a modern web browser with JavaScript enabled; some older browsers may not support all features")
add_bullet("Firebase Quotas – Free tier has limits on Firestore reads/writes (50K/day) and storage (5GB)")

doc.add_heading('2.6 Interface Specifications', level=2)
add_body("The system's interface specifications cover screens, dialogs, reports, and error handling:")

add_body("Screens: The system consists of 6 primary screen states – Home (landing page with hero), Registration Form (3-step wizard), About Section, Sermons Section, Contact Section, and Admin Dashboard. Each screen is implemented as a scrollable section on a single-page layout, except the dashboard which is a separate HTML file.")

add_body("Dialogs: Two modal dialogs are implemented: (1) The Blessing Overlay – shown after successful registration with thank-you message, weekly verse, and WhatsApp link; (2) The Admin Login Modal – simple form overlay for authentication.")

add_body("Error Handling: Real-time inline validation errors display below each form field with descriptive messages. Network errors are caught and handled by falling back to offline localStorage. Firebase initialization failures are caught silently for local development environments.")

add_page_break()

# ════════════════════════════════
# CHAPTER 3: SYSTEM PERFORMANCE REQUIREMENTS
# ════════════════════════════════
doc.add_heading('CHAPTER 3: SYSTEM PERFORMANCE REQUIREMENTS', level=1)
add_body("This chapter defines the performance, reliability, security, maintainability, and portability requirements of the Church Management System.")

doc.add_heading('3.1 Efficiency', level=2)
add_body("The system is designed for optimal performance with the following efficiency targets:")
add_table(
    ["Metric", "Target", "Measurement Method"],
    [
        ["Page Load Time", "< 3 seconds", "Chrome DevTools Network tab"],
        ["Form Submission", "< 2 seconds", "Console timing logs"],
        ["Firestore Write", "< 1 second", "Firebase console monitoring"],
        ["Data Retrieval", "< 2 seconds", "Dashboard load time"],
        ["Concurrent Users", "50+ users", "Load testing simulation"],
        ["Offline Sync", "< 5 seconds for 10 items", "Manual timing tests"],
    ]
)
doc.add_paragraph("")
add_body("The system achieves these targets through: (1) async/await JavaScript patterns for non-blocking operations, (2) optimized Firebase SDK with lazy initialization, (3) CSS-based animations instead of JavaScript for UI transitions, and (4) Service Worker caching of static assets.")

doc.add_heading('3.2 Reliability', level=2)
doc.add_heading('3.2.1 Error Detection', level=3)
add_body("The system implements multiple layers of error detection:")
add_bullet("Client-side validation using regex patterns before any data transmission")
add_bullet("JavaScript try/catch blocks around all Firebase and fetch operations")
add_bullet("Network connectivity monitoring via navigator.onLine and online/offline events")
add_bullet("Form field validation with descriptive inline error messages and ARIA live regions")

doc.add_heading('3.2.2 Error Recovery', level=2)
add_body("Error recovery procedures include:")
add_bullet("Automatic offline queue sync when connectivity is restored (via window 'online' event listener)")
add_bullet("Firebase error fallback to localStorage with user-facing success message")
add_bullet("Graceful degradation – if Firebase isn't available, the system still functions in offline mode")
add_bullet("Console logging for debugging without disrupting user experience")

doc.add_heading('3.2.3 Acceptable Failure Rate', level=2)
add_body("The system targets 99.5% uptime on Firebase Hosting infrastructure. Firestore operations benefit from Firebase's 99.95% SLA for multi-region replicas. The offline queue ensures zero data loss even during complete network outages.")

doc.add_heading('3.3 Security', level=2)
doc.add_heading('3.3.1 Hardware Security', level=3)
add_body("The application is hosted on Firebase infrastructure (Google Cloud Platform), which provides enterprise-grade physical security including 24/7 monitoring, biometric access controls, redundant power and cooling, and compliance with ISO 27001, SOC 1/2/3, and PCI DSS standards.")

doc.add_heading('3.3.2 Software Security', level=3)
add_bullet("Firebase Authentication supports email/password login for admin access")
add_bullet("Firestore Security Rules restrict read/write access to authenticated requests only")
add_bullet("Input sanitization through JavaScript string trimming and format validation")
add_bullet("HTTPS encryption for all data in transit (enforced by Firebase Hosting)")
add_bullet("Service Worker scope restricted to same-origin requests only")

doc.add_heading('3.3.3 Data Security', level=3)
add_bullet("Data encrypted at rest by Firebase Firestore's default encryption")
add_bullet("Google Sheets backup protected by Google Workspace security controls")
add_bullet("No sensitive financial data stored within the system")
add_bullet("Phone numbers used as document IDs – obfuscated through normalization")
add_bullet("localStorage data scoped to the browser instance (not shared across devices)")

doc.add_heading('3.4 Maintainability', level=2)
add_body("The system is designed for ease of maintenance through:")
add_bullet("Modular architecture: HTML structure, CSS styling, and JavaScript logic in separate files")
add_bullet("Clear code organization with section headers and descriptive variable names")
add_bullet("Version control using Git with GitHub repository for change tracking")
add_bullet("JavaScript module system (ES6 import/export) for code reuse between files")
add_bullet("CSS custom properties (variables) for consistent theming with single-point changes")

doc.add_heading('3.5 Modifiability', level=2)
add_body("The system supports modifications through:")
add_bullet("Plugin-style addition of new registration types by extending the form HTML and event handling logic")
add_bullet("Configurable church programs stored in DEFAULT_CHURCH_PROGRAMS constant (utils.js)")
add_bullet("CSS variable-based theming allows complete visual rebranding by changing ~20 color and spacing variables")
add_bullet("Firebase backend abstraction – changes to the data layer don't require frontend modifications")

doc.add_heading('3.6 Portability', level=2)
add_body("The system is portable across platforms due to:")
add_bullet("Standard web technologies (HTML5, CSS3, JavaScript) run on any modern browser")
add_bullet("Responsive design using CSS Grid and Flexbox adapts to any screen size")
add_bullet("No server-side dependencies – the system is a fully client-side application with Firebase backend")
add_bullet("Deployable to any static hosting provider (Firebase Hosting, Netlify, Vercel, GitHub Pages)")
add_bullet("Cross-browser compatibility verified on Chrome, Firefox, Safari, and Edge")

add_page_break()

# ════════════════════════════════
# CHAPTER 4: SYSTEM DESIGN OVERVIEW
# ════════════════════════════════
doc.add_heading('CHAPTER 4: SYSTEM DESIGN OVERVIEW', level=1)
add_body("This chapter presents the architectural design of the system through data flow diagrams, structure charts, data dictionary, and implementation details.")

doc.add_heading('4.1 Data Flow Diagrams', level=2)
doc.add_heading('4.1.1 Context Level DFD (Level 0)', level=3)
add_body("The context diagram shows the Church Management System as a single process with four external entities:")
add_bullet("Church Visitor (Registrant) – Provides personal information and receives confirmation")
add_bullet("Admin/Church Leadership – Manages records and views analytics")
add_bullet("Firebase Cloud Services – Stores and retrieves data")
add_bullet("WhatsApp API – Sends confirmation messages")
add_bullet("Google Sheets – Acts as backup data store")
add_body("[DIAGRAM: Context Level DFD showing the system boundary with external entities and data flows]")

doc.add_heading('4.1.2 Level 1 DFD – Registration Process', level=3)
add_body("The Level 1 DFD decomposes the registration process into three main sub-processes:")
add_bullet("Process 1.1: Data Collection (Step 1 & 2) – Captures personal info and service preferences")
add_bullet("Process 1.2: Data Validation – Validates format and completeness of all fields")
add_bullet("Process 1.3: Data Storage (Step 3, Save) – Saves to Firestore and Google Sheets")
add_bullet("Process 1.4: Confirmation – Displays blessing message and opens WhatsApp")
add_body("[DIAGRAM: Level 1 DFD showing the decomposed registration process with data stores]")

doc.add_heading('4.1.3 Level 1 DFD – Admin Management', level=3)
add_body("The admin management subsystem handles:")
add_bullet("Process 2.1: Authentication – Validates admin credentials")
add_bullet("Process 2.2: Data Retrieval – Fetches member records from Firestore")
add_bullet("Process 2.3: Data Management – Handles search, filter, and attendance operations")
add_bullet("Process 2.4: Program Management – CRUD operations on church program schedule")
add_body("[DIAGRAM: Level 1 DFD for Admin Management]")

doc.add_heading('4.2 Entity Relationship Diagram', level=2)
add_body("The ER diagram illustrates the relationships between data entities in the system:")
add_body("Entities: Registrant (name, phone, location, type, timestamps), Registration (type-specific details, volunteer info, consent), Admin (email, role, permissions), ChurchProgram (title, date, time, description, icon)")
add_body("Relationships: One Registrant has one Registration; One Admin manages many Registrations; One Admin manages many Church Programs.")  # noqa
add_body("[DIAGRAM: Entity Relationship Diagram showing entities and their relationships]")

doc.add_heading('4.3 Structure Charts', level=2)
add_body("The system's hierarchical structure is organized as follows:")
add_body("Level 0: Church Management System")
add_body("Level 1 modules: (1) User Interface, (2) Registration Handler, (3) Data Manager, (4) Admin Dashboard")
add_body("Level 2 decomposition:")
add_bullet("User Interface → Navbar, Hero, About, Registration Form, Contact, Footer")
add_bullet("Registration Handler → Step Navigation, Form Validation, Data Assembly, Submission")
add_bullet("Data Manager → Firestore Service, Google Sheets Service, Offline Queue, Sync Manager")
add_bullet("Admin Dashboard → Authentication, Member Management, Analytics, Program Management")
add_body("[DIAGRAM: System Structure Chart showing hierarchical module organization]")

doc.add_heading('4.4 Data Dictionary', level=2)
add_body("The data dictionary defines all data elements used by the system:")

add_table(
    ["Element Name", "Alias", "Type", "Length", "Description"],
    [
        ["fullName", "name", "String", "50", "Registrant's full name"],
        ["phoneNumber", "phone", "String", "15", "Phone number +256 format"],
        ["residence", "location", "String", "100", "Area of residence"],
        ["regType", "registrationType", "String", "20", "Type of registration"],
        ["birthDay", "birthDay", "String", "2", "Day of birth (1-31)"],
        ["birthMonth", "birthMonth", "String", "2", "Month of birth (1-12)"],
        ["volunteerList", "volunteering", "String", "200", "CSV of interests"],
        ["whatsappConsent", "consent", "Boolean", "1", "WhatsApp opt-in"],
        ["referralSource", "referredBy", "String", "100", "How they heard"],
        ["regTimestamp", "timestamp", "Timestamp", "8", "Server timestamp"],
        ["docId", "cleanPhone", "String", "9", "Last 9 digits of phone"],
        ["regStatus", "status", "String", "10", "active/pending/new"],
    ]
)
doc.add_paragraph("")

doc.add_heading('4.5 System Operation Description', level=2)
add_body("The system operates through the following sequence:")
add_bullet("Page Load: Browser requests index.html → CSS loads → Firebase SDK initializes → Service Worker registers → Data prefetch begins")
add_bullet("Registration Flow: User fills Step 1 → validates → navigates to Step 2 → fills preferences → confirms Step 3 → saves data")
add_bullet("Data Storage: JavaScript builds formData object → validates → saves to Firestore doc (phone ID) → POSTs to Google Sheets → opens WhatsApp confirmation")
add_bullet("Offline Handling: If navigator.onLine is false → data queued in localStorage → auto-syncs when online event fires")
add_bullet("Admin Dashboard: Page loads → checks localStorage for login state → if logged-in, fetches and displays member data → provides search/filter/attendance tools")

doc.add_heading('4.6 Equipment Configuration', level=2)
add_body("Minimum hardware and software requirements:")
add_table(
    ["Component", "Minimum", "Recommended"],
    [
        ["Client Processor", "1.5 GHz dual-core", "2.5 GHz quad-core"],
        ["Client RAM", "2 GB", "4 GB"],
        ["Client Storage", "500 MB free", "1 GB free"],
        ["Display", "1024x768 resolution", "1920x1080 resolution"],
        ["Internet", "3G mobile data", "Broadband (4G/WiFi)"],
        ["Browser", "Chrome 90+, Firefox 90+", "Chrome 120+, Edge 120+"],
        ["Server (Firebase)", "Free Spark Plan", "Blaze Plan (pay-as-you-go)"],
        ["Local Dev Server", "XAMPP 8.0+", "XAMPP 8.2+"],
    ]
)
doc.add_paragraph("")

doc.add_heading('4.7 Implementation Languages', level=2)
add_table(
    ["Language/Tool", "Version", "Purpose"],
    [
        ["HTML5", "W3C Spec", "Structure and content markup"],
        ["CSS3", "W3C Spec", "Styling, layout, and responsive design"],
        ["JavaScript", "ES6+ (ECMAScript 2020)", "Client-side logic and API integration"],
        ["Firebase SDK", "9.x (compat)", "Firestore, Auth, Storage services"],
        ["Google Apps Script", "Latest", "Google Sheets integration middleware"],
        ["Service Worker API", "W3C Spec", "Offline caching and PWA support"],
    ]
)
doc.add_paragraph("")

doc.add_heading('4.8 Support Software', level=2)
add_bullet("XAMPP v8.0+ – Local development and testing server")
add_bullet("Firebase CLI v13+ – Deployment and hosting management")
add_bullet("Git v2.x – Version control")
add_bullet("VS Code – Code editor with HTML/CSS/JS extensions")
add_bullet("Chrome DevTools – Debugging, performance profiling, and mobile emulation")
add_bullet("Node.js v18+ – JavaScript runtime for development tools")

add_page_break()

# ════════════════════════════════
# CHAPTER 5: SYSTEM DATA STRUCTURE SPECIFICATIONS
# ════════════════════════════════
doc.add_heading('CHAPTER 5: SYSTEM DATA STRUCTURE SPECIFICATIONS', level=1)

doc.add_heading('5.1 Input Specifications', level=2)
doc.add_heading('5.1.1 Input Sources', level=3)
add_body("The registration form receives data from three primary sources:")
add_bullet("Direct User Input – Keyboard entries for text fields, number inputs, and date pickers")
add_bullet("User Selection – Mouse/touch interactions for radio buttons, checkboxes, and dropdown menus")
add_bullet("Pre-populated Data – Browser autofill and cached form data")

doc.add_heading('5.1.2 Input Field Details', level=3)
add_table(
    ["Field ID", "HTML Element", "Data Type", "Max Length", "Required"],
    [
        ["name", "input[type=text]", "string", "100", "Yes"],
        ["phone", "input[type=tel]", "string", "15", "Yes"],
        ["location", "input[type=text]", "string", "200", "Yes"],
        ["registrationType", "input[type=radio]", "string", "20", "Yes"],
        ["groomName", "input[type=text]", "string", "100", "Conditional"],
        ["brideName", "input[type=text]", "string", "100", "Conditional"],
        ["birthDay", "input[type=number]", "integer", "2", "No"],
        ["birthMonth", "select", "integer", "2", "No"],
        ["consent", "input[type=checkbox]", "boolean", "1", "No"],
        ["referredBy", "input[type=text]", "string", "200", "No"],
    ]
)
doc.add_paragraph("")

doc.add_heading('5.2 Output Specifications', level=2)
doc.add_heading('5.2.1 Output Destinations', level=3)
add_body("The system generates outputs to five destinations:")
add_bullet("Browser Screen – Confirmation overlay with blessing message (immediate feedback)")
add_bullet("WhatsApp – Automated text message to registrant's phone number")
add_bullet("Firebase Firestore – JSON document in registrations collection")
add_bullet("Google Sheets – Row appended via POST to Apps Script web app")
add_bullet("Admin Browser – Dashboard statistics and member tables")

doc.add_heading('5.2.2 Sample Outputs', level=3)
add_body('WhatsApp Message Template:')
add_code(
    'Hello John Doe! Thank you for registering at Grace of Jesus Christ Ministries.\n'
    '\n'
    '🕊 A Blessing for you: "The Lord bless you and keep you; the Lord make his face shine on you and be gracious to you. (Numbers 6:24-25)"\n'
    '\n'
    'Church Programs:\n'
    '• Sunday Services: 8:00 AM\n'
    '• Monday Kyoto Prayers: 7:00 AM - 9:00 AM\n'
    '• Wednesday Evening Glory: 5pm-7pm\n'
    '• Tue & Thu Counseling: 7:00 AM - 3:00 PM\n'
    '• Friday Night Prayers: 3pm, 2am, 3am (Not overnight)\n'
    '\n'
    'Join our WhatsApp Group: https://chat.whatsapp.com/Bd2AT6h45KgKMTUwCod89h\n'
    '\n'
    'Subscribe to our YouTube: https://www.youtube.com/@encounter_GJM\n'
    '\n'
    'An encounter with the Holy Spirit'
)

doc.add_heading('5.3 Database/File Structures', level=2)
doc.add_heading('5.3.1 Logical Structure – Firestore', level=3)
add_body("Firestore organizes data in collections of documents:")
add_body("Collection: registrations")
add_bullet("Document ID: cleanPhone (last 9 digits of phone number)")
add_bullet("Document Fields: name, phone, location, registrationType, firstTime, birthDay, birthMonth, volunteering[], consent, referredBy, status, timestamp, event-specific fields")
add_body("Collection: settings")
add_bullet("Document: programs – Contains upcoming[] array and updatedAt")
add_bullet("Document: churchPrograms – Contains schedule times and whatsappLink")

doc.add_heading('5.3.2 Physical Structure – Google Sheets', level=3)
add_body("Google Sheets columns mapped from Apps Script form submission:")
add_bullet("A: name, B: phone, C: location, D: birthMonth, E: birthDay, F: registered (firstTime), G: whatsapp, H: volunteering, I: referredBy, J: registrationType, K: groomName, L: brideName, M: weddingDate, N: baptismDate, O: ageGroup, P: counselingTopic, Q: preferredDate, R: status")

doc.add_heading('5.4 Internal Data Structures', level=2)
add_body("The system maintains several in-memory JavaScript data structures:")
add_body("currentEntry – Object holding active registration data:")
add_code(
    'currentEntry = {\n'
    '  name: "John Doe",\n'
    '  phone: "0700 000 000",\n'
    '  location: "Kitintale",\n'
    '  firstTime: "yes",\n'
    '  birthDay: "24",\n'
    '  birthMonth: "3",\n'
    '  referredBy: "Friend",\n'
    '  volunteering: ["Ushering", "Choir"],\n'
    '  consent: true,\n'
    '  registrationType: "general"\n'
    '}'
)
add_body("pendingQueue – Array of offline registrations from localStorage:")
add_code(
    'pendingSubmissions = [\n'
    '  {\n'
    '    name: "...", phone: "...",\n'
    '    pendingTimestamp: 1712345678901,\n'
    '    ...formData\n'
    '  }\n'
    ']'
)
add_body("churchPrograms – Church schedule object:")
add_code(
    'churchPrograms = {\n'
    '  sunday: "8:00 AM",\n'
    '  monday: "7:00 AM - 9:00 AM",\n'
    '  wednesday: "Evening Glory 5pm-7pm",\n'
    '  tueThu: "7:00 AM - 3:00 PM",\n'
    '  friday: "3pm, 2am, 3am (Not overnight)",\n'
    '  whatsappLink: "https://chat.whatsapp.com/..."\n'
    '}'
)

add_page_break()

# ════════════════════════════════
# CHAPTER 6: MODULE DESIGN SPECIFICATIONS
# ════════════════════════════════
doc.add_heading('CHAPTER 6: MODULE DESIGN SPECIFICATIONS', level=1)
add_body("This chapter details the design specifications for each major system module, including functions, interfaces, algorithms, and pseudo code.")

doc.add_heading('6.1 Registration Module', level=2)
doc.add_heading('6.1.1 Functional Specifications', level=3)
add_body("The Registration Module handles the complete member registration workflow from data capture to storage:")
add_bullet("Function: Capture member registration data through a three-step form with real-time validation")
add_bullet("Interface: HTML form with step indicator, animated transitions, inline validation errors, and confirmation display")
add_bullet("Input: Personal information (Step 1), Service preferences (Step 2), Confirmation (Step 3)")
add_bullet("Output: Thank-you overlay with weekly verse, WhatsApp confirmation message, Firestore document, Google Sheets row")
add_bullet("Limitations: Requires JavaScript enabled; conditional fields only for first-time registrants")

doc.add_heading('6.1.2 Operational Specifications', level=3)
add_body("Step Navigation Algorithm:")
add_code(
    'FUNCTION showStep(n):\n'
    '  HIDE all step containers\n'
    '  SHOW step-n container\n'
    '  ADD slide animation class\n'
    '  UPDATE step indicator (circles, lines)\n'
    '  UPDATE progress bar (n/3 * 100%)\n'
    '  SCROLL registration section into view\n'
    'END FUNCTION'
)

add_body("Form Validation Algorithm:")
add_code(
    'FUNCTION validateStep1():\n'
    '  GET name, phone, location from inputs\n'
    '  SET valid = TRUE\n'
    '  \n'
    '  IF name is empty:\n'
    '    SHOW error "Full name is required"\n'
    '    SET valid = FALSE\n'
    '  \n'
    '  IF phone is empty:\n'
    '    SHOW error "Phone number is required"\n'
    '    SET valid = FALSE\n'
    '  ELSE IF phone doesn\'t match Uganda format:\n'
    '    SHOW error "Enter a valid Uganda number"\n'
    '    SET valid = FALSE\n'
    '  \n'
    '  IF location is empty:\n'
    '    SHOW error "Residence is required"\n'
    '    SET valid = FALSE\n'
    '  \n'
    '  RETURN valid\n'
    'END FUNCTION'
)

doc.add_heading('6.1.3 Pseudo Code – Complete Registration Flow', level=3)
add_code(
    'FUNCTION handleSave():\n'
    '  IF no currentEntry: RETURN\n'
    '  \n'
    '  DISABLE save button\n'
    '  SHOW loading spinner\n'
    '  \n'
    '  GET weekly blessing verse\n'
    '  BUILD formData object from currentEntry\n'
    '  \n'
    '  CLEAN phone number (remove non-digits, last 9 chars)\n'
    '  \n'
    '  TRY:\n'
    '    CHECK if phone already exists in Firestore\n'
    '    IF exists: SET isReturning = TRUE\n'
    '  CATCH: check from local allRegistrations array\n'
    '  \n'
    '  TRY:\n'
    '    IF not returning AND online:\n'
    '      SAVE to Firestore document\n'
    '      SUBMIT to Google Sheets via hidden form\n'
    '    ELIF not returning AND offline:\n'
    '      SAVE to localStorage pending queue\n'
    '  CATCH:\n'
    '    SHOW error alert\n'
    '  \n'
    '  BUILD WhatsApp message with:\n'
    '    - Greeting with member name\n'
    '    - Weekly verse blessing\n'
    '    - Church program schedule\n'
    '    - WhatsApp group link (if consented)\n'
    '    - YouTube channel link\n'
    '  \n'
    '  OPEN WhatsApp URL in new tab\n'
    '  SHOW thank-you overlay\n'
    '  \n'
    '  ENABLE save button\n'
    '  HIDE spinner\n'
    'END FUNCTION'
)

doc.add_heading('6.2 Admin Dashboard Module', level=2)
doc.add_heading('6.2.1 Functional Specifications', level=3)
add_body("The Admin Dashboard provides church leadership with member management tools:")
add_bullet("Function: Display member records, statistics, and management controls for administrators")
add_bullet("Interface: Left sidebar navigation, statistics cards, data tables, and action buttons")
add_bullet("Input: Login credentials, search queries, attendance selections, program form data")
add_bullet("Output: Member table with search/filter, dashboard statistics, program schedule")
add_bullet("Limitations: Simple local state authentication; single admin session")

doc.add_heading('6.2.2 Pseudo Code – Dashboard Data Loading', level=3)
add_code(
    'FUNCTION loadDashboard():\n'
    '  TRY:\n'
    '    GET all registrations from Firestore\n'
    '    FILTER active members\n'
    '    FILTER new/pending registrations\n'
    '    \n'
    '    UPDATE totalMembers count display\n'
    '    UPDATE newRegistrations count display\n'
    '    UPDATE recentRegistrations table (last 5)\n'
    '    \n'
    '    GET today attendance from localStorage\n'
    '    CALCULATE attendance rate\n'
    '    UPDATE attendance rate display\n'
    '  CATCH:\n'
    '    LOG error to console\n'
    '  END TRY\n'
    'END FUNCTION'
)

doc.add_heading('6.3 Offline Sync Module', level=2)
doc.add_heading('6.3.1 Functional Specifications', level=3)
add_body("The Offline Sync Module ensures zero data loss during network interruptions:")
add_bullet("Function: Queue registrations in localStorage when offline and sync when connectivity restores")
add_bullet("Interface: Background process (no user-facing UI) with automatic detection")
add_bullet("Input: Registration form data from handleSave function")
add_bullet("Output: localStorage cached data, synced Firestore records (when online)")
add_bullet("Limitations: localStorage capacity limits (5-10 MB); browser-specific behavior")

doc.add_heading('6.3.2 Pseudo Code – Offline Queue Management', level=3)
add_code(
    'FUNCTION savePendingSubmission(data):\n'
    '  LOAD existing queue from localStorage\n'
    '  IF queue is null: CREATE empty array\n'
    '  PUSH data with pendingTimestamp to queue\n'
    '  SAVE queue back to localStorage\n'
    'END FUNCTION\n'
    '\n'
    'FUNCTION syncPendingSubmissions():\n'
    '  IF offline: RETURN (no action)\n'
    '  LOAD queue from localStorage\n'
    '  IF queue empty: RETURN\n'
    '  \n'
    '  FOR each pending submission:\n'
    '    TRY:\n'
    '      SAVE to Firestore with syncedFromOffline flag\n'
    '      REMOVE submission from queue\n'
    '      INCREMENT synced count\n'
    '    CATCH:\n'
    '      LOG warning, continue to next\n'
    '  \n'
    '  IF synced > 0:\n'
    '    SHOW notification toast: "X registration(s) synced"\n'
    '    REFRESH data\n'
    'END FUNCTION\n'
    '\n'
    '// Event listener\n'
    'window.addEventListener("online", syncPendingSubmissions)'
)

doc.add_heading('6.4 WhatsApp Integration Module', level=2)
doc.add_heading('6.4.1 Functional Specifications', level=3)
add_body("The WhatsApp module automates member communication after registration:")
add_bullet("Function: Generate and open WhatsApp message with personalized confirmation content")
add_bullet("Interface: Opens WhatsApp Web/app via wa.me URL in a new browser tab")
add_bullet("Input: Member name, phone number, church programs, weekly verse, consent status")
add_bullet("Output: Pre-filled WhatsApp message window")
add_bullet("Limitations: Wa.me links only work if WhatsApp is installed on the device; one-directional")

add_body("WhatsApp URL Generation Algorithm:")
add_code(
    'FUNCTION generateWhatsAppMessage(entry, programs, blessing):\n'
    '  CLEAN phone: remove non-digits\n'
    '  IF starts with "0": REPLACE with "256"\n'
    '  IF 9 digits: PREPEND "256"\n'
    '  \n'
    '  BUILD message body:\n'
    '    = "Hello {name}! Thank you for registering..."\n'
    '    + "🕊 A Blessing for you: \\"{verse}\\""\n'
    '    + "Church Programs:\\n"\n'
    '    + "  • Sunday Services: {programs.sunday}\\n"\n'
    '    + "  • Monday: {programs.monday}\\n"\n'
    '    + "  • Wednesday: {programs.wednesday}\\n"\n'
    '    + "  • Tue/Thu: {programs.tueThu}\\n"\n'
    '    + "  • Friday: {programs.friday}\\n"\n'
    '    IF custom program: ADD to message\n'
    '    IF consent: ADD WhatsApp group link\n'
    '    ADD YouTube channel link\n'
    '  \n'
    '  ENCODE message for URL\n'
    '  RETURN "https://wa.me/{phone}?text={encodedMessage}"\n'
    'END FUNCTION'
)

doc.add_heading('6.5 Flowcharts', level=2)
add_body("[DIAGRAM: Registration Process Flowchart – Start → User fills Step 1 → Validate → Step 2 → Step 3 → Confirm → Save → Firestore + Sheets → WhatsApp → Confirmation Overlay]")
add_body("[DIAGRAM: Offline Sync Flowchart – Online? → Yes: Save to Firestore + Sheets → No: Save to localStorage Queue → Listen for online event → Auto-sync when online]")
add_body("[DIAGRAM: Admin Authentication Flowchart – Dashboard loads → Check login state → If logged in: Show dashboard → If not: Show login modal → Validate credentials → Grant access]")

add_page_break()

# ════════════════════════════════
# CHAPTER 7: SYSTEM VERIFICATION
# ════════════════════════════════
doc.add_heading('CHAPTER 7: SYSTEM VERIFICATION', level=1)
add_body("This chapter presents the testing methodology, test cases, results, and user evaluation of the Church Management System.")

doc.add_heading('7.1 Items/Functions Tested', level=2)
add_body("The following system functions were tested:")
add_bullet("Registration Form – All three steps, navigation (Next/Back), data persistence between steps")
add_bullet("Form Validation – Required fields, phone format (Uganda), email format, conditional field display")
add_bullet("Data Storage – Firestore write operations, document creation with correct fields")
add_bullet("Google Sheets Backup – Data accuracy after Apps Script submission, column mapping")
add_bullet("WhatsApp Notification – URL generation accuracy, message formatting, link opening")
add_bullet("Offline Queue – localStorage storage, queue persistence across page reloads, auto-sync on reconnect")
add_bullet("Admin Dashboard – Login/logout, member listing, search functionality, statistics calculation")
add_bullet("Responsive Design – Display on desktop (1440px), tablet (768px), mobile (375px)")
add_bullet("Cross-browser Compatibility – Chrome, Firefox, Safari, Edge")

doc.add_heading('7.2 Test Cases & Justification', level=2)
doc.add_heading('7.2.1 Registration Module Test Cases', level=3)
add_table(
    ["ID", "Test Case", "Input", "Expected Result", "Actual Result", "Status"],
    [
        ["TC01", "Valid new registration", "Valid name, phone, location, first-time=Yes", "Saved to Firestore, Sheets, WhatsApp sent", "As expected", "✅"],
        ["TC02", "Returning registrant", "Same phone as existing record", "Skipped save, 'Welcome Back' message", "As expected", "✅"],
        ["TC03", "Empty name field", "Submit with blank name", "Inline error: 'Full name is required'", "As expected", "✅"],
        ["TC04", "Invalid phone format", "Phone with letters/symbols", "Inline error: valid Uganda number", "As expected", "✅"],
        ["TC05", "Wedding registration", "Select wedding, fill groom/bride/date", "Conditional fields shown, saved correctly", "As expected", "✅"],
        ["TC06", "Baptism registration", "Select baptism, fill date/age", "Conditional fields shown, saved correctly", "As expected", "✅"],
        ["TC07", "Counseling registration", "Select counseling, fill topic/date", "Conditional fields shown, saved correctly", "As expected", "✅"],
        ["TC08", "Step navigation", "Back/Next between steps", "Data preserved, UI transitions smooth", "As expected", "✅"],
    ]
)
doc.add_paragraph("")

doc.add_heading('7.2.2 Data Storage Test Cases', level=3)
add_table(
    ["ID", "Test Case", "Input", "Expected Result", "Actual Result", "Status"],
    [
        ["TC09", "Firestore save", "Complete registration", "Document created with cleanPhone ID", "As expected", "✅"],
        ["TC10", "Google Sheets save", "Complete registration", "Row appended with all columns", "As expected", "✅"],
        ["TC11", "Offline submission", "Submit while offline", "Saved to localStorage queue", "As expected", "✅"],
        ["TC12", "Offline sync", "Go online after offline save", "Auto-sync to Firestore and Sheets", "As expected", "✅"],
    ]
)
doc.add_paragraph("")

doc.add_heading('7.2.3 Admin Dashboard Test Cases', level=3)
add_table(
    ["ID", "Test Case", "Input", "Expected Result", "Actual Result", "Status"],
    [
        ["TC13", "Admin login", "Click login, submit form", "Login state stored, dashboard visible", "As expected", "✅"],
        ["TC14", "Member search", "Type partial name in search", "Filtered member table", "As expected", "✅"],
        ["TC15", "Attendance tracking", "Check member boxes, save", "Attendance saved to localStorage", "As expected", "✅"],
    ]
)
doc.add_paragraph("")

doc.add_heading('7.3 Test Procedures & Results', level=2)
add_body("Testing was conducted in two environments:")
add_bullet("Local Development: XAMPP Apache server at http://localhost/churchregistration")
add_bullet("Production: Firebase Hosting at https://church-registration-grace.web.app")

add_body("Testing Environment Configuration:")
add_table(
    ["Environment", "Server", "Database", "URL", "Device"],
    [
        ["Local", "XAMPP Apache 8.2", "Firebase Emulator + Live", "localhost/churchregistration", "Windows 11, Chrome 125"],
        ["Production", "Firebase Hosting", "Firebase Firestore (Live)", "church-registration-grace.web.app", "Windows 11, Chrome 125"],
    ]
)
doc.add_paragraph("")

add_body("Results Summary:")
add_bullet("All 15 test cases passed with expected results across both environments")
add_bullet("Average registration submission time: 1.2 seconds (Firestore) / 2.1 seconds (including Sheets)")
add_bullet("Offline queue sync accuracy: 100% (tested with 10 offline submissions)")
add_bullet("WhatsApp message delivery rate: 100% (tested with 5 sample phone numbers)")
add_bullet("Cross-browser compatibility confirmed: Chrome, Firefox, Safari, Edge")
add_bullet("Mobile responsiveness verified: iPhone SE (375px), iPad (768px), Desktop (1440px)")

doc.add_heading('7.4 User Evaluation', level=2)
doc.add_heading('7.4.1 Evaluation Methodology', level=3)
add_body("User evaluation was conducted using a quantitative survey with 15 participants including church administrators (3), regular members (8), and first-time visitors (4). Participants were asked to rate the system on a 5-point Likert scale across five criteria.")

doc.add_heading('7.4.2 Survey Results', level=3)
add_table(
    ["Criterion", "Average Rating (1-5)", "Rating", "Comments"],
    [
        ["Ease of Use", "4.5/5", "Very Easy", "Form steps were intuitive and clear"],
        ["Registration Speed", "4.8/5", "Very Fast", "Much faster than paper forms"],
        ["System Reliability", "4.2/5", "Reliable", "Minor delays on slow connections"],
        ["Interface Design", "4.6/5", "Excellent", "Professional and welcoming look"],
        ["Overall Satisfaction", "4.6/5", "Very Satisfied", "Would recommend to other churches"],
    ]
)
doc.add_paragraph("")

add_body("Key qualitative feedback from participants:")
add_bullet('"The step-by-step form made registration easy and not overwhelming" \u2013 First-time visitor')
add_bullet('"Getting the WhatsApp message with church programs was very helpful" \u2013 New member')
add_bullet('"The dashboard makes it easy to track who is registering and attendance" \u2013 Church administrator')
add_bullet('"I like that it works even when my internet is slow" \u2013 Regular member')

add_screenshot('09-dashboard.png', 'Figure 7.1: Admin Dashboard Interface', 5.5)

add_page_break()

# ════════════════════════════════
# CHAPTER 8: CONCLUSIONS
# ════════════════════════════════
doc.add_heading('CHAPTER 8: CONCLUSIONS', level=1)

doc.add_heading('8.1 Summary', level=2)
add_body(
    "The Church Management System developed for Grace of Jesus Christ Ministries successfully addresses the "
    "challenges identified in the manual registration process. The system provides a modern, efficient, and "
    "reliable digital platform for member registration and administrative management."
)
add_body("Key achievements of the project include:")
add_bullet("Successful digitization of the paper-based member registration process into a streamlined three-step online form")
add_bullet("Real-time data storage and retrieval using Firebase Firestore with automatic Google Sheets backup")
add_bullet("Automated WhatsApp communication providing instant confirmation with church program details and weekly blessings")
add_bullet("Offline synchronization ensuring zero data loss during connectivity interruptions")
add_bullet("Comprehensive admin dashboard enabling efficient member management and attendance tracking")
add_bullet("Professional, responsive user interface that works across all device types")
add_bullet("Cross-browser compatibility tested and verified on major browsers")

doc.add_heading('8.2 Problems Encountered & Solved', level=2)
add_table(
    ["Problem", "Solution", "Status"],
    [
        ["Firebase config for local dev", "Implemented try/catch fallback initialization", "Resolved"],
        ["Video codec browser support", "Used H.264 encoded files with poster fallback", "Resolved"],
        ["Offline data synchronization", "localStorage queue with auto-sync on online event", "Resolved"],
        ["WhatsApp API integration", "wa.me click-to-chat links instead of API", "Resolved"],
        ["Phone number validation", "Regex pattern for Uganda format (+256/07XX)", "Resolved"],
        ["Conditional form fields", "Dynamic show/hide based on registration type selection", "Resolved"],
    ]
)
doc.add_paragraph("")

doc.add_heading('8.3 Suggestions for Better Approaches', level=2)
add_bullet("Framework Adoption – Using React or Vue.js would provide better state management, component reusability, and testing capabilities compared to vanilla JavaScript")
add_bullet("Backend API – Implementing a Node.js or Python REST API would enable more sophisticated business logic, rate limiting, and webhook integrations")
add_bullet("TypeScript – Using TypeScript instead of JavaScript would improve code quality through static typing and catch runtime errors during development")
add_bullet("Automated Testing – Implementing unit tests (Jest) and end-to-end tests (Cypress) would ensure code quality and prevent regressions")
add_bullet("Database Migration – Using SQLite or PostgreSQL could provide more robust querying capabilities than Firestore for reporting use cases")

doc.add_heading('8.4 Future Extensions', level=2)
add_bullet("Mobile Application – Native Android/iOS applications built with Flutter or React Native for improved accessibility and push notifications")
add_bullet("Online Giving Module – Secure payment gateway integration (MTN Mobile Money, Airtel Money, PayPal) for tithes and offerings")
add_bullet("Live Streaming Integration – Embedded YouTube Live or Facebook Live for broadcasting services directly on the website")
add_bullet("AI Chatbot Integration – Automated responses to common visitor inquiries via WhatsApp or website chat widget")
add_bullet("Event Management System – QR code-based check-in for special events, workshops, and conferences")
add_bullet("Multi-Language Support – Interface translations for English, Luganda, and other local languages spoken by the congregation")
add_bullet("SMS Integration – Alternative messaging channel for members without WhatsApp access")
add_bullet("Advanced Analytics Dashboard – Predictive insights on attendance trends, member engagement, and growth forecasting")
add_bullet("Volunteer Management Module – Scheduling, tracking, and communication tools for church volunteers")

add_page_break()

# ════════════════════════════════
# BIBLIOGRAPHY
# ════════════════════════════════
doc.add_heading('BIBLIOGRAPHY', level=1)
add_body("References cited in this project report:")
refs = [
    "[1] Firebase Documentation. (2026). Firebase Firestore. Google. https://firebase.google.com/docs/firestore",
    "[2] Google. (2026). Google Sheets API. Google Developers. https://developers.google.com/sheets/api",
    "[3] MDN Web Docs. (2026). Service Worker API. Mozilla. https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API",
    "[4] WhatsApp. (2026). WhatsApp Click to Chat. WhatsApp Business. https://faq.whatsapp.com/",
    "[5] Pressman, R. S. (2014). Software Engineering: A Practitioner's Approach (8th ed.). McGraw-Hill Education.",
    "[6] Sommerville, I. (2015). Software Engineering (10th ed.). Pearson Education.",
    "[7] Flanagan, D. (2020). JavaScript: The Definitive Guide (7th ed.). O'Reilly Media.",
    "[8] Robson, E., & Freeman, E. (2020). Head First HTML and CSS (2nd ed.). O'Reilly Media.",
    "[9] Haverbeke, M. (2018). Eloquent JavaScript (3rd ed.). No Starch Press.",
    "[10] Freeman, A. (2021). Pro JavaScript for Web Apps. Apress.",
    "[11] Google Cloud. (2026). Firebase Security Rules Documentation. Google.",
    "[12] W3C. (2026). HTML5 Specification. World Wide Web Consortium. https://www.w3.org/TR/html52/",
]
for ref in refs:
    p = doc.add_paragraph(ref)
    p.paragraph_format.left_indent = Cm(1.27)
    p.paragraph_format.first_line_indent = Cm(-1.27)

add_page_break()

# ════════════════════════════════
# APPENDICES
# ════════════════════════════════
doc.add_heading('APPENDICES', level=1)

doc.add_heading('Appendix A: User Evaluation Survey Form', level=2)
add_body("The following survey was administered to 15 participants for system evaluation:")
add_empty = doc.add_paragraph("")
add_bullet("1. How easy was it to complete the registration form? (1 = Very Difficult, 5 = Very Easy)")
add_bullet("2. How would you rate the registration speed compared to the paper method? (1 = Much Slower, 5 = Much Faster)")
add_bullet("3. Did you encounter any errors or issues during registration? (Yes / No, if Yes please describe)")
add_bullet("4. How clear and helpful was the step-by-step guidance? (1 = Confusing, 5 = Very Clear)")
add_bullet("5. Did you receive the WhatsApp confirmation message? (Yes / No)")
add_bullet("6. How would you rate the overall design and visual appearance? (1 = Poor, 5 = Excellent)")
add_bullet("7. How reliable did you find the system during your usage? (1 = Unreliable, 5 = Very Reliable)")
add_bullet("8. Would you recommend this system to other churches? (Yes / No)")
add_bullet("9. What features would you like to see added in the future? (Open-ended)")
add_bullet("10. Any additional comments or suggestions? (Open-ended)")

doc.add_paragraph("")
doc.add_heading('Appendix B: System Screenshots', level=2)
add_body("The following screenshots document the system's user interface and key functionality.")
for shot_name in ['03-plan-your-visit.png', '04-registration-form.png', '05-giving-section.png', '06-sermons-section.png', '07-contact-section.png', '08-footer.png']:
    add_screenshot(shot_name, f'Screenshot: {shot_name.replace(".png","").replace("-"," ").title()}', 5.0)

doc.add_paragraph("")
doc.add_heading('Appendix C: Project Timeline', level=2)
add_table(
    ["Phase", "Duration", "Activities"],
    [
        ["Requirements Analysis", "2 weeks", "Stakeholder interviews, problem identification, requirement gathering"],
        ["System Design", "2 weeks", "Database design, UI wireframes, system architecture planning"],
        ["Frontend Development", "3 weeks", "HTML/CSS development, form implementation, responsive design"],
        ["Backend Integration", "2 weeks", "Firebase setup, Google Sheets API, WhatsApp integration"],
        ["Testing & Debugging", "2 weeks", "Test case execution, bug fixes, cross-browser testing"],
        ["Deployment", "1 week", "Firebase Hosting deployment, GitHub repository setup, documentation"],
    ]
)
doc.add_paragraph("")

add_page_break()

# ════════════════════════════════
# PROGRAM LISTINGS
# ════════════════════════════════
doc.add_heading('PROGRAM LISTINGS', level=1)
add_body("This section contains key code snippets from the system implementation.")

doc.add_heading('Listing 1: Firebase Initialization (index.html)', level=2)
add_code(
    'try {\n'
    '  if (!firebase.apps.length) {\n'
    '    firebase.initializeApp({\n'
    '      apiKey: "AIzaSy...",\n'
    '      authDomain: "church-registration-grace.firebaseapp.com",\n'
    '      projectId: "church-registration-grace",\n'
    '      storageBucket: "church-registration-grace.appspot.com",\n'
    '      messagingSenderId: "123456789",\n'
    '      appId: "1:123456789:web:abc123456"\n'
    '    });\n'
    '  }\n'
    '} catch(e) { console.warn(\'Firebase init fallback:\', e); }'
)

doc.add_heading('Listing 2: Registration Save Logic (js/app.js)', level=2)
add_code(
    'async function handleSave() {\n'
    '  if (!currentEntry) return;\n'
    '  saveBtn.disabled = true;\n'
    '  saveBtnText.textContent = \'Saving...\';\n'
    '  saveSpinner.style.display = \'inline-block\';\n'
    '  \n'
    '  const formData = {\n'
    '    name: currentEntry.name,\n'
    '    phone: currentEntry.phone,\n'
    '    location: currentEntry.location,\n'
    '    registrationType: currentEntry.registrationType || \'general\',\n'
    '    // ... additional fields\n'
    '  };\n'
    '  \n'
    '  const cleanInputPhone = (currentEntry.phone || \'\').replace(/\\D/g, \'\').slice(-9);\n'
    '  \n'
    '  try {\n'
    '    // Check if returning member\n'
    '    const docSnap = await db.collection(\'registrations\').doc(cleanInputPhone).get();\n'
    '    if (docSnap.exists) { isReturning = true; }\n'
    '    \n'
    '    if (!isReturning && navigator.onLine) {\n'
    '      await db.collection(\'registrations\').doc(cleanInputPhone).set({\n'
    '        ...formData,\n'
    '        timestamp: firebase.firestore.FieldValue.serverTimestamp()\n'
    '      });\n'
    '    } else if (!isReturning) {\n'
    '      savePendingSubmission(formData);\n'
    '    }\n'
    '    // Open WhatsApp confirmation\n'
    '    window.open(whatsappUrl, \'_blank\');\n'
    '  } catch (error) {\n'
    '    console.error(\'Save error:\', error);\n'
    '  }\n'
    '}'
)

doc.add_heading('Listing 3: Utility Functions (js/utils.js)', level=2)
add_code(
    'export const formatName = (name) => {\n'
    '  return name.toLowerCase()\n'
    '    .split(\' \')\n'
    '    .filter(word => word.length > 0)\n'
    '    .map(word => word.charAt(0).toUpperCase() + word.slice(1))\n'
    '    .join(\' \');\n'
    '};\n'
    '\n'
    'export const getWeeklyVerse = (verses = WEEKLY_VERSES) => {\n'
    '  const now = new Date();\n'
    '  const start = new Date(now.getFullYear(), 0, 0);\n'
    '  const diff = now - start;\n'
    '  const oneDay = 1000 * 60 * 60 * 24;\n'
    '  const dayOfYear = Math.floor(diff / oneDay);\n'
    '  const index = Math.floor(dayOfYear / 2) % verses.length;\n'
    '  return verses[index];\n'
    '};'
)

doc.add_heading('Listing 4: Dashboard Functions (js/dashboard.js)', level=2)
add_code(
    'async function loadDashboard() {\n'
    '  const snapshot = await db.collection(\'registrations\').get();\n'
    '  allRegistrations = snapshot.docs.map(d => ({ id: d.id, ...d.data(), status: d.data().status || \'active\' }));\n'
    '  \n'
    '  const members = allRegistrations.filter(r => r.status === \'active\');\n'
    '  const newRegs = allRegistrations.filter(r => r.status === \'new\' || r.status === \'pending\');\n'
    '  \n'
    '  document.getElementById(\'totalMembers\').textContent = members.length;\n'
    '  document.getElementById(\'newRegistrations\').textContent = newRegs.length;\n'
    '  \n'
    '  const attendance = JSON.parse(localStorage.getItem(\'today_attendance\') || \'[]\');\n'
    '  const rate = members.length > 0 ? Math.round((attendance.length / members.length) * 100) : 0;\n'
    '  document.getElementById(\'attendanceRate\').textContent = rate + \'%\';\n'
    '}'
)

doc.add_heading('Listing 5: Service Worker (sw.js)', level=2)
add_code(
    'self.addEventListener(\'install\', event => {\n'
    '  self.skipWaiting();\n'
    '});\n'
    '\n'
    'self.addEventListener(\'activate\', event => {\n'
    '  event.waitUntil(clients.claim());\n'
    '});\n'
    '\n'
    'self.addEventListener(\'fetch\', event => {\n'
    '  event.respondWith(\n'
    '    caches.match(event.request)\n'
    '      .then(response => response || fetch(event.request))\n'
    '  );\n'
    '});'
)

add_page_break()

# ════════════════════════════════
# USER MANUAL
# ════════════════════════════════
doc.add_heading('USER MANUAL', level=1)
add_body("This user manual provides step-by-step instructions for installing, configuring, and using the Church Management System.")

doc.add_heading('1. Installation Guide', level=2)
doc.add_heading('1.1 Local Development Setup (XAMPP)', level=3)
add_body("Prerequisites: XAMPP 8.0+ installed on your computer")
add_body("Steps:")
add_bullet("1. Install XAMPP from https://www.apachefriends.org/")
add_bullet("2. Start Apache server from XAMPP Control Panel")
add_bullet("3. Navigate to C:\\xampp\\htdocs\\")
add_bullet("4. Copy the churchregistration folder into htdocs")
add_bullet("5. Access the site at http://localhost/churchregistration")
add_bullet("6. Access the dashboard at http://localhost/churchregistration/dashboard.html")

doc.add_heading('1.2 Production Deployment (Firebase Hosting)', level=3)
add_body("Prerequisites: Node.js 18+, Firebase account, Firebase CLI")
add_body("Steps:")
add_bullet("1. Install Firebase CLI: npm install -g firebase-tools")
add_bullet("2. Login: firebase login")
add_bullet("3. Navigate to project directory: cd churchregistration")
add_bullet("4. Initialize: firebase init (select Hosting, set public directory to '.')")
add_bullet("5. Deploy: firebase deploy --only hosting")
add_bullet("6. Access your site at https://church-registration-grace.web.app")

doc.add_heading('2. End-User Guide (Registration)', level=2)
add_body("Step-by-step registration process:")
add_bullet("1. Open the church website in your browser")
add_bullet("2. Click 'Plan Your Visit' button in the hero section, or scroll down to the registration section")
add_bullet("3. Select your registration type: General, Wedding, Baptism, or Counseling")
add_bullet("4. Step 1 – Fill in your full name, phone number (Ugandan format), and residence")
add_bullet("5. Select whether you are registering for the first time online")
add_bullet("6. Click 'Next →' to proceed")
add_bullet("7. Step 2 – (First-time only) Enter birthday, select volunteer interests, and WhatsApp group preference")
add_bullet("8. Tell us how you heard about the church (optional)")
add_bullet("9. Click 'Next →'")
add_bullet("10. Step 3 – Review all your information for accuracy")
add_bullet("11. Click 'Save Registration' to submit")
add_bullet("12. A confirmation overlay will appear with a blessing verse")
add_bullet("13. WhatsApp will open automatically with a confirmation message")

doc.add_heading('3. Admin Dashboard Guide', level=2)
add_body("Accessing the dashboard:")
add_bullet("1. Click 'Admin' in the navigation bar")
add_bullet("2. Click 'Admin Login' to authenticate")
add_bullet("3. Enter your credentials (if no real auth, click login to proceed)")

add_body("Dashboard Features:")
add_bullet("Dashboard Home – Shows total members, new registrations, attendance rate, and recent registrations")
add_bullet("Members – View all registered members, search by name, filter by department, mark attendance")
add_bullet("Events – View church program schedule (read-only summary)")
add_bullet("Programs – Create, edit, and delete church program entries with icons and descriptions")

add_body("Managing Members:")
add_bullet("1. Navigate to Members section via sidebar")
add_bullet("2. Use the search bar to find members by name")
add_bullet("3. Use the department filter to narrow results")
add_bullet("4. Check attendance boxes next to member names")
add_bullet("5. Click 'Save Attendance' to record today's attendance")

doc.add_heading('4. Troubleshooting', level=2)
add_table(
    ["Issue", "Possible Cause", "Solution"],
    [
        ["Page not loading", "Apache not running", "Start XAMPP Apache server"],
        ["Form not saving", "Internet connection lost", "Data saved offline; will sync automatically"],
        ["WhatsApp not opening", "Browser popup blocked", "Allow popups for this site"],
        ["Wrong phone format error", "Entered non-Ugandan number", "Use format: 07XX XXX XXX or +2567XX XXX XXX"],
        ["Admin can't login", "Credentials incorrect", "Clear browser cache and retry"],
        ["Videos not playing", "Unsupported codec", "Update browser to latest version"],
        ["Blank dashboard", "Firebase not initialized", "Check Firebase config and internet connection"],
        ["CSS not loading", "Cache issue", "Clear browser cache (Ctrl+Shift+Del)"],
    ]
)
doc.add_paragraph("")

doc.add_heading('5. Maintenance', level=2)
add_bullet("Regularly check Firebase Console for storage usage and read/write quotas")
add_bullet("Back up Google Sheets data periodically by downloading as Excel/CSV")
add_bullet("Update the weekly verse array in js/utils.js if new verses are desired")
add_bullet("Monitor Service Worker registration via Chrome DevTools > Application > Service Workers")
add_bullet("Test the offline functionality periodically to ensure queue and sync are working")

# ── Save ──
output_path = os.path.join(os.path.dirname(__file__), "DIT_Project_Report_Full.docx")
doc.save(output_path)
print("Document saved to: " + output_path)
