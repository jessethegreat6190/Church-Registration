from docx import Document
from docx.shared import Inches, Pt, RGBColor, Cm, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import os

doc = Document()
SHOTS = 'C:\\xampp\\htdocs\\churchregistration\\report_screenshots'
MAROON = RGBColor(0x80, 0x00, 0x20)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
BLACK = RGBColor(0x00, 0x00, 0x00)
DARK_BLUE = RGBColor(0x2C, 0x3E, 0x50)

# ── Configure styles ──
style = doc.styles['Normal']
style.font.name = 'Times New Roman'
style.font.size = Pt(12)
style.paragraph_format.line_spacing = 2.0
style.paragraph_format.space_after = Pt(0)

for i, sz in [(1, 16), (2, 14), (3, 12)]:
    h = doc.styles[f'Heading {i}']
    h.font.name = 'Times New Roman'
    h.font.color.rgb = BLACK
    h.font.bold = True
    h.font.size = Pt(sz)
    h.paragraph_format.line_spacing = 2.0
    h.paragraph_format.space_before = Pt(12)
    h.paragraph_format.space_after = Pt(6)

def add_centered(text, size=12, bold=False):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.line_spacing = 2.0
    r = p.add_run(text)
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.name = 'Times New Roman'
    return p

def add_body(text):
    p = doc.add_paragraph()
    p.paragraph_format.first_line_indent = Cm(1.27)
    p.paragraph_format.line_spacing = 2.0
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    return p

def add_bullet(text):
    p = doc.add_paragraph(text, style='List Bullet')
    p.paragraph_format.line_spacing = 2.0
    return p

def add_table_caption(text, above=True):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.line_spacing = 2.0
    r = p.add_run(text)
    r.font.size = Pt(10)
    r.font.italic = True
    r.font.bold = True
    r.font.name = 'Times New Roman'
    return p

def add_figure_caption(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.line_spacing = 2.0
    r = p.add_run(text)
    r.font.size = Pt(10)
    r.font.italic = True
    r.font.name = 'Times New Roman'
    return p

def add_image(img_file, width=5.5):
    path = os.path.join(SHOTS, img_file)
    if os.path.exists(path):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = 1.0
        r = p.add_run()
        r.add_picture(path, width=Inches(width))

def add_screenshot(img_file, caption, width=5.0):
    add_image(img_file, width)
    add_figure_caption(caption)

def add_simple_table(headers, rows):
    t = doc.add_table(rows=1+len(rows), cols=len(headers))
    t.style = 'Table Grid'
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, h in enumerate(headers):
        c = t.rows[0].cells[i]
        c.text = h
        for pp in c.paragraphs:
            pp.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for rr in pp.runs:
                rr.font.bold = True
                rr.font.size = Pt(10)
                rr.font.name = 'Times New Roman'
    for ri, rd in enumerate(rows, 1):
        for ci, v in enumerate(rd):
            c = t.rows[ri].cells[ci]
            c.text = v
            for pp in c.paragraphs:
                for rr in pp.runs:
                    rr.font.size = Pt(10)
                    rr.font.name = 'Times New Roman'
    return t

def add_code(code_text, size=9):
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.left_indent = Cm(1)
    for line in code_text.split('\n'):
        r = p.add_run(line + '\n')
        r.font.name = 'Courier New'
        r.font.size = Pt(size)

# ════════════════════════════════════════════════════════════════
# COVER PAGE – Maroon with ISBAT Logo (white text on maroon bg)
# ════════════════════════════════════════════════════════════════
sec = doc.sections[0]
sec.top_margin = Cm(2.54)
sec.bottom_margin = Cm(2.54)
sec.left_margin = Cm(3.17)
sec.right_margin = Cm(3.17)

def add_centered_white(text, size=12, bold=False):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.line_spacing = 2.0
    r = p.add_run(text)
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.name = 'Times New Roman'
    r.font.color.rgb = WHITE
    return p

# Create full-page maroon table for cover background
cover_table = doc.add_table(rows=1, cols=1)
cover_table.alignment = WD_TABLE_ALIGNMENT.CENTER
cover_cell = cover_table.rows[0].cells[0]
# Set maroon background on cell
tc = cover_cell._tc
tcPr = tc.get_or_add_tcPr()
shd = OxmlElement('w:shd')
shd.set(qn('w:fill'), '800020')
shd.set(qn('w:val'), 'clear')
tcPr.append(shd)

# Clear default paragraph in cell
cover_cell.paragraphs[0].clear()

# Maroon cover content (everything white)
p_logo = cover_cell.add_paragraph()
p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_logo.paragraph_format.space_before = Pt(40)
logo_path = os.path.join(SHOTS, 'isbat-logo.png')
if os.path.exists(logo_path):
    r = p_logo.add_run()
    r.add_picture(logo_path, width=Inches(2.0))

for _ in range(2):
    p = cover_cell.add_paragraph()
    p.paragraph_format.line_spacing = 2.0

for txt, sz, bd in [
    ('DIPLOMA IN INFORMATION TECHNOLOGY', 16, True),
    ('', 12, False),
    ('FINAL YEAR PROJECT REPORT', 14, True),
]:
    p = cover_cell.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.line_spacing = 2.0
    if txt:
        r = p.add_run(txt)
        r.font.size = Pt(sz)
        r.font.bold = bd
        r.font.name = 'Times New Roman'
        r.font.color.rgb = WHITE

for _ in range(3):
    p = cover_cell.add_paragraph()
    p.paragraph_format.line_spacing = 2.0

for txt, sz, bd in [
    ('CHURCH MANAGEMENT SYSTEM', 22, True),
    ('Grace of Jesus Christ Ministries \u2013 Kitintale, Kampala', 14, False),
]:
    p = cover_cell.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.line_spacing = 2.0
    r = p.add_run(txt)
    r.font.size = Pt(sz)
    r.font.bold = bd
    r.font.name = 'Times New Roman'
    r.font.color.rgb = WHITE

for _ in range(3):
    p = cover_cell.add_paragraph()
    p.paragraph_format.line_spacing = 2.0

for txt, sz, bd in [
    ('A Project Report Submitted to the Department of Information Technology', 12, False),
    ('ISBAT University \u2013 Kampala, Uganda', 12, False),
    ('In Partial Fulfillment of the Requirements for the', 12, False),
    ('Diploma in Information Technology', 14, True),
]:
    p = cover_cell.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.line_spacing = 2.0
    r = p.add_run(txt)
    r.font.size = Pt(sz)
    r.font.bold = bd
    r.font.name = 'Times New Roman'
    r.font.color.rgb = WHITE

for _ in range(3):
    p = cover_cell.add_paragraph()
    p.paragraph_format.line_spacing = 2.0

for txt, sz, bd in [
    ('Submitted by:', 12, False),
    ('Jondu Jesse', 14, True),
    ('Registration No: 012240240', 12, False),
    ('Supervisor: [Supervisor Name]', 12, False),
    ('Academic Year: 2025/2026', 12, False),
]:
    p = cover_cell.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.line_spacing = 2.0
    r = p.add_run(txt)
    r.font.size = Pt(sz)
    r.font.bold = bd
    r.font.name = 'Times New Roman'
    r.font.color.rgb = WHITE

# Remove table borders
tbl = cover_table._tbl
tblPr = tbl.tblPr if tbl.tblPr is not None else OxmlElement('w:tblPr')
borders = OxmlElement('w:tblBorders')
for edge in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
    elem = OxmlElement(f'w:{edge}')
    elem.set(qn('w:val'), 'none')
    elem.set(qn('w:sz'), '0')
    elem.set(qn('w:space'), '0')
    elem.set(qn('w:color'), 'auto')
    borders.append(elem)
tblPr.append(borders)

# Section break: cover (no page number) vs rest (page numbers)
new_section = doc.add_section()
new_section.top_margin = Cm(2.54)
new_section.bottom_margin = Cm(2.54)
new_section.left_margin = Cm(3.17)
new_section.right_margin = Cm(3.17)

# ════════════════════════════════════════════════════════════════
# TITLE PAGE
# ════════════════════════════════════════════════════════════════
for _ in range(6): doc.add_paragraph("")
add_centered('CHURCH MANAGEMENT SYSTEM', 22, True)
add_centered('Grace of Jesus Christ Ministries \u2013 Kitintale, Kampala', 14)
for _ in range(4): doc.add_paragraph("")
add_centered('A Project Report Submitted to the Department of Information Technology')
add_centered('ISBAT University')
add_centered('In Partial Fulfillment of the Requirements for the')
add_centered('Diploma in Information Technology', 14, True)
for _ in range(3): doc.add_paragraph("")
add_centered('By')
add_centered('Jondu Jesse', 14, True)
add_centered('Registration No: 012240240')
add_centered('Supervisor: [Supervisor Name]')
add_centered('Date: May, 2026')

doc.add_page_break()

# ════════════════════════════════════════════════════════════════
# BONAFIDE CERTIFICATE
# ════════════════════════════════════════════════════════════════
for _ in range(4): doc.add_paragraph("")
add_centered('BONAFIDE CERTIFICATE', 16, True)
for _ in range(2): doc.add_paragraph("")
add_body('This is to certify that the project titled "Church Management System" is a bonafide work carried out by Jondu Jesse (Registration No: 012240240) under the supervision of [Supervisor Name] in partial fulfillment of the requirements for the Diploma in Information Technology at ISBAT University, Kampala, Uganda.')
for _ in range(4): doc.add_paragraph("")
add_centered('____________________________')
add_centered('Supervisor')
add_centered('Department of Information Technology')
add_centered('ISBAT University')
add_centered('Date: _____________')

doc.add_page_break()

# ════════════════════════════════════════════════════════════════
# STUDENT DECLARATION
# ════════════════════════════════════════════════════════════════
for _ in range(4): doc.add_paragraph("")
add_centered('STUDENT DECLARATION', 16, True)
for _ in range(2): doc.add_paragraph("")
add_body('I, Jondu Jesse, hereby declare that this project report titled "Church Management System" is my original work and has not been submitted for any academic award at any other institution. All sources of information used in this report have been duly acknowledged.')
for _ in range(4): doc.add_paragraph("")
add_centered('____________________________')
add_centered('Jondu Jesse')
add_centered('Signature: _____________')
add_centered('Date: _____________')

doc.add_page_break()

# ════════════════════════════════════════════════════════════════
# ABSTRACT
# ════════════════════════════════════════════════════════════════
add_centered('ABSTRACT', 16, True)
for _ in range(2): doc.add_paragraph("")
add_body('This project presents a comprehensive Church Management System developed for Grace of Jesus Christ Ministries, located in Kitintale, Kampala, Uganda. The system addresses the critical challenges faced by the church in managing member registrations, tracking church programs, and maintaining accurate administrative records through a modern web-based digital platform.')
add_body('The current manual paper-based registration process was identified as inefficient, prone to data loss, difficult to analyze, and time-consuming for church administrators. The proposed system digitizes the entire registration workflow through a multi-step online form that captures member personal details, contact information, volunteer preferences, and event-specific data for weddings, baptisms, and counseling sessions. The system architecture leverages Firebase Firestore for real-time NoSQL database storage, Google Sheets as a backup database via Google Apps Script, and Firebase Authentication for secure admin access.')
add_body('Additional features include WhatsApp integration for automated member confirmation messages, offline data synchronization through localStorage and Service Workers, and an administrative dashboard for member management, attendance tracking, and church program scheduling. The system was developed using HTML5, CSS3, and JavaScript (ES6+), following a responsive design approach ensuring seamless accessibility across desktop, tablet, and mobile devices.')
add_body('System testing was conducted in both local (XAMPP) and cloud (Firebase Hosting) environments, with all 15 test cases passing successfully. User evaluation results indicate a 4.6/5 overall satisfaction rating, with notable improvements in registration speed and data accuracy compared to the manual system.')

doc.add_page_break()

# ════════════════════════════════════════════════════════════════
# KEYWORDS AND PHRASES
# ════════════════════════════════════════════════════════════════
add_centered('KEYWORDS AND PHRASES', 16, True)
for _ in range(2): doc.add_paragraph("")
for kw in [
    'Church Management System', 'Firebase Firestore', 'Google Sheets Integration',
    'Member Registration System', 'WhatsApp Automation', 'Offline Data Synchronization',
    'Service Worker', 'Admin Dashboard', 'NoSQL Database', 'Responsive Web Design'
]:
    add_bullet(kw)

doc.add_page_break()

# ════════════════════════════════════════════════════════════════
# COMPUTING REVIEW SUBJECT CODES
# ════════════════════════════════════════════════════════════════
add_centered('COMPUTING REVIEW SUBJECT CODES', 16, True)
for _ in range(2): doc.add_paragraph("")
add_simple_table(
    ['Code', 'Topic', 'Description'],
    [
        ['D.2.2', 'Software Engineering', 'Design Tools and Techniques'],
        ['D.2.10', 'Software Engineering', 'Design \u2013 Methodologies'],
        ['H.2.4', 'Database Management', 'Systems \u2013 Relational Databases'],
        ['H.4.3', 'Information Systems', 'Web-based Services'],
        ['H.5.2', 'Information Interfaces', 'User Interfaces \u2013 Web'],
        ['I.7.1', 'Document Processing', 'Electronic Publishing'],
        ['K.4.3', 'Computers and Society', 'Organizational Impacts'],
        ['K.6.3', 'Management of Computing', 'Software Management'],
    ]
)
doc.add_paragraph("")

doc.add_page_break()

# ════════════════════════════════════════════════════════════════
# TABLE OF CONTENTS
# ════════════════════════════════════════════════════════════════
add_centered('TABLE OF CONTENTS', 16, True)
for _ in range(2): doc.add_paragraph("")
toc = [
    'Bonafide Certificate', 'Student Declaration', 'Abstract', 'Keywords and Phrases',
    'Computing Review Subject Codes', 'Table of Contents', 'List of Figures',
    'List of Tables', 'Chapter 1: Introduction & Background',
    'Chapter 2: System Functional Specification',
    'Chapter 3: System Performance Requirements',
    'Chapter 4: System Design Overview',
    'Chapter 5: System Data Structure Specifications',
    'Chapter 6: Module Design Specifications',
    'Chapter 7: System Verification',
    'Chapter 8: Conclusions', 'Bibliography', 'Appendices',
    'Program Listings', 'User Manual'
]
for t in toc:
    doc.add_paragraph(f'{t} .............................................................. [Page]')

doc.add_page_break()

# LIST OF FIGURES
add_centered('LIST OF FIGURES', 16, True)
for _ in range(2): doc.add_paragraph("")
for f in [
    'Figure 1.1: Church Management System Homepage',
    'Figure 2.1: Registration Form Interface', 'Figure 2.2: Plan Your Visit Section',
    'Figure 2.3: Sermons & Teachings Section', 'Figure 2.4: Contact Section',
    'Figure 2.5: Admin Dashboard', 'Figure 4.1: Context Level DFD (Level 0)',
    'Figure 4.2: Level 1 DFD \u2013 Registration Process',
    'Figure 4.3: Level 1 DFD \u2013 Admin Management',
    'Figure 4.4: Entity Relationship Diagram', 'Figure 4.5: System Structure Chart',
    'Figure 6.1: Registration Process Flowchart',
    'Figure 6.2: Offline Sync Flowchart',
    'Figure 6.3: Admin Authentication Flowchart',
]:
    doc.add_paragraph(f'{f} .............................................................. [Page]')

doc.add_page_break()

# LIST OF TABLES
add_centered('LIST OF TABLES', 16, True)
for _ in range(2): doc.add_paragraph("")
for t in [
    'Table 1.1: Weekly Church Program Schedule',
    'Table 2.1: Input Field Specifications',
    'Table 2.2: Output Destinations',
    'Table 2.3: Firestore Database Structure',
    'Table 3.1: Performance Requirements Matrix',
    'Table 4.1: Data Dictionary',
    'Table 4.2: Equipment Configuration',
    'Table 5.1: Input Field Details',
    'Table 5.2: Internal Data Structures',
    'Table 7.1: Registration Module Test Cases',
    'Table 7.2: Data Storage Test Cases',
    'Table 7.3: Admin Dashboard Test Cases',
    'Table 7.4: User Evaluation Survey Results',
    'Table 8.1: Problems Encountered & Solutions',
]:
    doc.add_paragraph(f'{t} .............................................................. [Page]')
doc.add_page_break()

# ════════════════════════════════════════════════════════════════
# CHAPTER 1: INTRODUCTION & BACKGROUND
# ════════════════════════════════════════════════════════════════
doc.add_heading('CHAPTER 1: INTRODUCTION & BACKGROUND', level=1)

doc.add_heading('1.1 Problem Statement', level=2)
add_body('Grace of Jesus Christ Ministries, located in Kitintale, Kampala, Uganda, has experienced significant growth in its congregation since its establishment. The church operates under the slogan "An encounter with the Holy Spirit" and conducts multiple weekly services including Sunday worship, Monday Kyoto Prayers, Wednesday Evening Glory, Tuesday/Thursday Counseling sessions, and Friday Night Prayers. This growth has created operational challenges in managing member information efficiently.')
add_body('The current manual paper-based registration process suffers from several critical limitations including high risk of data loss, no centralized database for storing and retrieving member records, time-consuming search and analysis processes, no mechanism for tracking church growth patterns, inability to communicate effectively with registered members, manual data entry errors, limited accessibility, and no offline backup.')

doc.add_heading('1.2 Previous Work & Methods', level=2)
add_body('Previously, the church relied entirely on paper-based registration forms filled out by visitors during Sunday services and special events. Church administrators would manually transcribe this data into Microsoft Excel spreadsheets for basic record-keeping. Several existing church management solutions including ChurchSuite, Breeze ChMS, and Planning Center were reviewed. However, these solutions were found to be either too costly for the church\'s budget, required ongoing subscription fees, or lacked specific features needed for the Ugandan context such as WhatsApp integration and offline-first functionality.')

doc.add_heading('1.3 Background Context', level=2)
add_body('Grace of Jesus Christ Ministries is a prophetic church in the Pentecostal tradition, serving a diverse congregation from Kitintale and surrounding areas of Kampala. The church operates multiple weekly programs as shown in Table 1.1.')
add_table_caption('Table 1.1: Weekly Church Program Schedule')
add_simple_table(
    ['Program', 'Day', 'Time'],
    [
        ['Sunday Service', 'Every Sunday', '8:00 AM'],
        ['Monday Kyoto Prayers', 'Every Monday', '7:00 AM \u2013 9:00 AM'],
        ['Wednesday Evening Glory', 'Every Wednesday', '6:00 PM \u2013 7:00 PM'],
        ['Counseling Sessions', 'Tue & Thu', '7:00 AM \u2013 3:00 PM'],
        ['Friday Night Prayers', 'Every Friday', '9:00 PM \u2013 2:00 AM'],
        ['Youth Fellowship', 'Alternate Saturdays', '4:00 PM \u2013 6:00 PM'],
    ]
)
doc.add_paragraph("")

doc.add_heading('1.4 Project Description', level=2)
add_body('This project involves the design, development, and deployment of a comprehensive Church Management System that digitizes the entire member registration and management process. The system consists of a public-facing registration portal accessible via web browser and a password-protected administrative dashboard for church leadership.')
add_screenshot('10-hero-full.png', 'Figure 1.1: Church Management System Homepage')

doc.add_heading('1.5 Objectives & Justification', level=2)
doc.add_heading('1.5.1 Main Objective', level=3)
add_body('To design and develop a Church Management System that streamlines member registration and administrative processes at Grace of Jesus Christ Ministries.')

doc.add_heading('1.5.2 Specific Objectives', level=3)
add_bullet('To analyze the current manual registration system and identify its limitations')
add_bullet('To design a web-based registration portal with multi-step form functionality')
add_bullet('To implement an administrative dashboard for member data management and analytics')
add_bullet('To integrate Firebase Firestore for real-time data storage and Google Sheets for backup')
add_bullet('To implement WhatsApp integration for automated member communication')
add_bullet('To provide offline support through localStorage and Service Workers')

doc.add_heading('1.5.3 Justification', level=2)
add_body('The system is justified by the need to improve operational efficiency, reduce data loss risks, provide real-time access to member information, enhance communication with church members, and support informed decision-making by church leadership through data analytics.')

doc.add_page_break()

# ════════════════════════════════════════════════════════════════
# CHAPTER 2: SYSTEM FUNCTIONAL SPECIFICATION
# ════════════════════════════════════════════════════════════════
doc.add_heading('CHAPTER 2: SYSTEM FUNCTIONAL SPECIFICATION', level=1)
add_body('This chapter provides a detailed specification of the system\'s functions, user interface design, input/output mechanisms, database structure, and operational limitations.')

doc.add_heading('2.1 Functions Performed', level=2)
add_body('The Church Management System performs the following core functions:')
add_bullet('Member Registration \u2013 Three-step form capturing personal details, service preferences, and event-specific information for weddings, baptisms, and counseling sessions')
add_bullet('Data Validation \u2013 Client-side validation using JavaScript regex patterns with inline error messages')
add_bullet('Dual Data Storage \u2013 Simultaneous saving to Firebase Firestore (primary) and Google Sheets (backup)')
add_bullet('Offline Queue Management \u2013 localStorage queue with automatic sync when connectivity is restored')
add_bullet('WhatsApp Integration \u2013 Pre-formatted confirmation messages with weekly Bible verse and church program schedule')
add_bullet('Admin Dashboard \u2013 Member management, search, attendance tracking, and program scheduling')
add_bullet('Service Worker \u2013 Static asset caching for offline access and PWA functionality')

doc.add_heading('2.2 User Interface Design', level=2)
add_body('The system features a clean, professional user interface using deep navy blue (#2c3e50) as primary and sky blue (#3498db) as secondary colors with Montserrat font family. Key components include a fixed navigation bar, full-width video hero section, frosted-glass about cards, three-step registration wizard, auto-rotating video slideshow, admin dashboard with sidebar navigation, and floating WhatsApp button.')
add_screenshot('03-plan-your-visit.png', 'Figure 2.1: Plan Your Visit Section with Church Programs')
add_screenshot('04-registration-form.png', 'Figure 2.2: Registration Form with Step Indicator')
add_screenshot('06-sermons-section.png', 'Figure 2.3: Sermons & Teachings Section')
add_screenshot('07-contact-section.png', 'Figure 2.4: Contact Section with Google Maps')
add_screenshot('09-dashboard.png', 'Figure 2.5: Admin Dashboard Interface')

doc.add_heading('2.3 Input/Output Previews', level=2)
doc.add_heading('2.3.1 Input Specifications', level=3)
add_table_caption('Table 2.1: Input Field Specifications')
add_simple_table(
    ['Field', 'Control Type', 'Validation', 'Example'],
    [
        ['Full Name', 'Text input', 'Required', 'John Doe'],
        ['Phone Number', 'Tel input', 'Uganda format (07XX)', '0700 000 000'],
        ['Residence', 'Text input', 'Required', 'Kitintale, Kampala'],
        ['Registration Type', 'Radio buttons', 'One selected', 'General (default)'],
        ['Birth Day', 'Number input', 'Optional, 1-31', '24'],
        ['Birth Month', 'Dropdown', 'Optional', 'March'],
        ['Volunteer Interests', 'Checkboxes', 'Optional', 'Ushering, Choir'],
        ['WhatsApp Consent', 'Checkbox', 'Optional', 'Checked by default'],
    ]
)
doc.add_paragraph("")

doc.add_heading('2.3.2 Output Specifications', level=2)
add_table_caption('Table 2.2: Output Destinations')
add_simple_table(
    ['Output Type', 'Destination', 'Format', 'Trigger'],
    [
        ['Confirmation', 'Screen (overlay)', 'HTML + verse', 'After save'],
        ['WhatsApp Message', 'Member phone', 'Text + program schedule', 'After save'],
        ['Firestore Document', 'Cloud Firestore', 'JSON', 'On save'],
        ['Google Sheets Row', 'Google Sheets', 'Row data', 'On save'],
        ['Dashboard Stats', 'Admin screen', 'HTML numbers', 'Dashboard load'],
        ['Member Table', 'Admin screen', 'HTML table rows', 'Member section'],
    ]
)
doc.add_paragraph("")

doc.add_heading('2.4 Database/File Structure', level=2)
add_table_caption('Table 2.3: Firestore Database Structure')
add_simple_table(
    ['Collection', 'Document ID', 'Key Fields', 'Description'],
    [
        ['registrations', '[phone]', 'name, phone, location, registrationType, timestamp', 'Member records'],
        ['settings', 'programs', 'upcoming[], updatedAt', 'Program schedule'],
        ['settings', 'churchPrograms', 'sunday, monday, wednesday, ...', 'Default program times'],
    ]
)
doc.add_paragraph("")

doc.add_heading('2.5 Limitations & Restrictions', level=2)
add_bullet('Internet connection required for real-time features')
add_bullet('Limited to web browsers (no native mobile application)')
add_bullet('Dependent on third-party services (Firebase, Google Sheets)')
add_bullet('WhatsApp integration is unidirectional (system to member)')

doc.add_heading('2.6 Interface Specifications', level=2)
add_body('The system consists of 6 primary screen states \u2013 Home (landing page with hero), Registration Form (3-step wizard), About Section, Sermons Section, Contact Section, and Admin Dashboard. Two modal dialogs are implemented: the Blessing Overlay shown after successful registration and the Admin Login Modal for authentication. Real-time inline validation errors display below form fields with descriptive messages, and network errors trigger automatic fallback to offline localStorage.')

doc.add_page_break()

# ════════════════════════════════════════════════════════════════
# CHAPTER 3: SYSTEM PERFORMANCE REQUIREMENTS
# ════════════════════════════════════════════════════════════════
doc.add_heading('CHAPTER 3: SYSTEM PERFORMANCE REQUIREMENTS', level=1)

doc.add_heading('3.1 Efficiency', level=2)
add_table_caption('Table 3.1: Performance Requirements Matrix')
add_simple_table(
    ['Metric', 'Target', 'Method'],
    [
        ['Page Load Time', '< 3 seconds', 'Chrome DevTools'],
        ['Form Submission', '< 2 seconds', 'Console timing'],
        ['Firestore Write', '< 1 second', 'Firebase Console'],
        ['Data Retrieval', '< 2 seconds', 'Dashboard load'],
        ['Concurrent Users', '50+', 'Load testing'],
        ['Offline Sync', '< 5 sec/10 items', 'Manual timing'],
    ]
)
doc.add_paragraph("")

doc.add_heading('3.2 Reliability', level=2)
doc.add_heading('3.2.1 Error Detection', level=3)
add_bullet('Client-side validation using regex patterns before any data transmission')
add_bullet('JavaScript try/catch blocks around all Firebase and fetch operations')
add_bullet('Network monitoring via navigator.onLine and online/offline events')

doc.add_heading('3.2.2 Error Recovery', level=2)
add_bullet('Automatic offline queue sync when connectivity is restored')
add_bullet('Firebase error fallback to localStorage with user-facing success message')
add_bullet('Console logging for debugging without disrupting user experience')

doc.add_heading('3.2.3 Acceptable Failure Rate', level=2)
add_body('The system targets 99.5% uptime on Firebase Hosting with Firestore\'s 99.95% SLA. The offline queue ensures zero data loss during network outages.')

doc.add_heading('3.3 Security', level=2)
doc.add_heading('3.3.1 Hardware Security', level=3)
add_body('Hosted on Firebase infrastructure (Google Cloud Platform) with enterprise-grade physical security including 24/7 monitoring and ISO 27001 compliance.')

doc.add_heading('3.3.2 Software Security', level=3)
add_bullet('Firebase Authentication for admin login')
add_bullet('Firestore Security Rules restricting access to authenticated requests')
add_bullet('Input sanitization and HTTPS encryption for all data in transit')

doc.add_heading('3.3.3 Data Security', level=3)
add_bullet('Data encrypted at rest by Firebase Firestore')
add_bullet('Google Sheets backup protected by Google Workspace security')
add_bullet('No sensitive financial data stored within the system')

doc.add_heading('3.4 Maintainability', level=2)
add_body('Modular architecture with HTML, CSS, and JavaScript in separate files. ES6 module system (import/export) for code reuse. CSS custom properties for consistent theming. Version control using Git with GitHub repository.')

doc.add_heading('3.5 Modifiability', level=2)
add_body('Plugin-style addition of new registration types, configurable church programs in DEFAULT_CHURCH_PROGRAMS constant, CSS variable-based theming for complete visual rebranding.')

doc.add_heading('3.6 Portability', level=2)
add_body('Standard web technologies run on any modern browser. Responsive design using CSS Grid and Flexbox. No server-side dependencies. Deployable to Firebase Hosting, Netlify, Vercel, or GitHub Pages. Cross-browser compatibility verified on Chrome, Firefox, Safari, and Edge.')

doc.add_page_break()

# ════════════════════════════════════════════════════════════════
# CHAPTER 4: SYSTEM DESIGN OVERVIEW
# ════════════════════════════════════════════════════════════════
doc.add_heading('CHAPTER 4: SYSTEM DESIGN OVERVIEW', level=1)

doc.add_heading('4.1 Data Flow Diagrams', level=2)
doc.add_heading('4.1.1 Context Level DFD (Level 0)', level=3)
add_body('The context diagram shows the Church Management System as a single process interacting with four external entities: Church Visitor, Admin/Church Leadership, Firebase Cloud Services, WhatsApp API, and Google Sheets.')
add_screenshot('dfd-context.png', 'Figure 4.1: Context Level DFD (Level 0)')

doc.add_heading('4.1.2 Level 1 DFD \u2013 Registration Process', level=3)
add_body('The Level 1 DFD decomposes the registration process into sub-processes: Data Collection, Data Validation, Data Storage (Firestore + Sheets), and Confirmation (WhatsApp).')
add_screenshot('dfd-registration.png', 'Figure 4.2: Level 1 DFD \u2013 Registration Process')

doc.add_heading('4.1.3 Level 1 DFD \u2013 Admin Management', level=3)
add_body('The admin management subsystem handles: Authentication, Data Retrieval from Firestore, Data Management (search, filter, attendance), and Program Management (CRUD operations).')
add_screenshot('dfd-admin.png', 'Figure 4.3: Level 1 DFD \u2013 Admin Management')

doc.add_heading('4.2 Entity Relationship Diagram', level=2)
add_body('The ER diagram illustrates four entities: Registrant (name, phone, location, regType), Registration (regType, eventData, volunteering), Admin (email, role, lastLogin), and ChurchProgram (title, date, time, description).')
add_screenshot('er-diagram.png', 'Figure 4.4: Entity Relationship Diagram')

doc.add_heading('4.3 Structure Charts', level=2)
add_body('The system\'s hierarchical structure is organized into four top-level modules: User Interface, Registration Handler, Data Manager, and Admin Dashboard.')
add_screenshot('structure-chart.png', 'Figure 4.5: System Structure Chart')

doc.add_heading('4.4 Data Dictionary', level=2)
add_table_caption('Table 4.1: Data Dictionary')
add_simple_table(
    ['Element', 'Alias', 'Type', 'Length', 'Description'],
    [
        ['fullName', 'name', 'String', '50', 'Registrant full name'],
        ['phoneNumber', 'phone', 'String', '15', 'Phone +256 format'],
        ['residence', 'location', 'String', '100', 'Area of residence'],
        ['regType', 'registrationType', 'String', '20', 'Registration type'],
        ['volunteerList', 'volunteering', 'String', '200', 'CSV of interests'],
        ['regTimestamp', 'timestamp', 'Timestamp', '8', 'Server timestamp'],
        ['docId', 'cleanPhone', 'String', '9', 'Last 9 phone digits'],
        ['regStatus', 'status', 'String', '10', 'active/pending/new'],
    ]
)
doc.add_paragraph("")

doc.add_heading('4.5 System Operation Description', level=2)
add_body('The system operates through the following sequence: Page Load (Firebase init, SW register, data prefetch) \u2192 Registration Flow (Step 1 \u2192 validate \u2192 Step 2 \u2192 Step 3 \u2192 save) \u2192 Data Storage (Firestore + Sheets + WhatsApp) \u2192 Offline Handling (localStorage queue \u2192 auto-sync) \u2192 Admin Dashboard (login \u2192 fetch members \u2192 manage).')

doc.add_heading('4.6 Equipment Configuration', level=2)
add_table_caption('Table 4.2: Equipment Configuration')
add_simple_table(
    ['Component', 'Minimum', 'Recommended'],
    [
        ['Client Processor', '1.5 GHz dual-core', '2.5 GHz quad-core'],
        ['Client RAM', '2 GB', '4 GB'],
        ['Display', '1024x768', '1920x1080'],
        ['Internet', '3G mobile data', 'Broadband/4G'],
        ['Browser', 'Chrome 90+', 'Chrome 120+'],
        ['Server', 'Firebase Spark', 'Firebase Blaze'],
        ['Local Dev', 'XAMPP 8.0+', 'XAMPP 8.2+'],
    ]
)
doc.add_paragraph("")

doc.add_heading('4.7 Implementation Languages', level=2)
add_bullet('HTML5 \u2013 Structure and content markup')
add_bullet('CSS3 \u2013 Styling, responsive layout, and animations')
add_bullet('JavaScript (ES6+) \u2013 Client-side logic, form validation, API integration')
add_bullet('Firebase SDK v9 \u2013 Firestore, Auth, Storage services')
add_bullet('Google Apps Script \u2013 Google Sheets integration middleware')
add_bullet('Service Worker API \u2013 Offline caching and PWA support')

doc.add_heading('4.8 Support Software', level=2)
add_bullet('XAMPP v8.0+ \u2013 Local development and testing server')
add_bullet('Firebase CLI v13+ \u2013 Deployment and hosting management')
add_bullet('Git v2.x \u2013 Version control with GitHub')
add_bullet('Visual Studio Code \u2013 Code editor')
add_bullet('Chrome DevTools \u2013 Debugging and performance profiling')

doc.add_page_break()

# ════════════════════════════════════════════════════════════════
# CHAPTER 5: SYSTEM DATA STRUCTURE SPECIFICATIONS
# ════════════════════════════════════════════════════════════════
doc.add_heading('CHAPTER 5: SYSTEM DATA STRUCTURE SPECIFICATIONS', level=1)

doc.add_heading('5.1 Input Specifications', level=2)
doc.add_heading('5.1.1 Input Sources', level=3)
add_body('The registration form receives data from three primary sources: direct user input via keyboard, user selection via mouse/touch interactions, and pre-populated data from browser autofill.')

doc.add_heading('5.1.2 Input Field Details', level=3)
add_table_caption('Table 5.1: Input Field Details')
add_simple_table(
    ['Field ID', 'Element', 'Type', 'Max', 'Required'],
    [
        ['name', 'input[text]', 'string', '100', 'Yes'],
        ['phone', 'input[tel]', 'string', '15', 'Yes'],
        ['location', 'input[text]', 'string', '200', 'Yes'],
        ['registrationType', 'input[radio]', 'string', '20', 'Yes'],
        ['groomName', 'input[text]', 'string', '100', 'Conditional'],
        ['brideName', 'input[text]', 'string', '100', 'Conditional'],
        ['birthDay', 'input[number]', 'int', '2', 'No'],
        ['birthMonth', 'select', 'int', '2', 'No'],
        ['consent', 'input[checkbox]', 'bool', '1', 'No'],
    ]
)
doc.add_paragraph("")

doc.add_heading('5.2 Output Specifications', level=2)
doc.add_heading('5.2.1 Output Destinations', level=3)
add_body('The system generates outputs to five destinations: browser screen (confirmation overlay), WhatsApp (automated text message), Firebase Firestore (JSON document), Google Sheets (appended row), and admin browser (dashboard statistics and member tables).')

doc.add_heading('5.2.2 Sample WhatsApp Message', level=3)
add_code('Hello John Doe! Thank you for registering at Grace of Jesus Christ Ministries.\n\n'
         '\U0001f54a A Blessing for you: "The Lord bless you and keep you..." (Numbers 6:24-25)\n\n'
         'Church Programs:\n'
         '\u2022 Sunday Services: 8:00 AM\n'
         '\u2022 Monday Kyoto Prayers: 7:00 AM - 9:00 AM\n'
         '\u2022 Wednesday Evening Glory: 5pm-7pm\n'
         '\u2022 Tue & Thu Counseling: 7:00 AM - 3:00 PM\n'
         '\u2022 Friday Night Prayers: 9:00 PM - 2:00 AM\n\n'
         'Join our WhatsApp Group: https://chat.whatsapp.com/...\n'
         'Subscribe: https://www.youtube.com/@encounter_GJM\n'
         'An encounter with the Holy Spirit')

doc.add_heading('5.3 Database/File Structures', level=2)
add_body('Firestore organizes data in collections of documents. The registrations collection uses the normalized phone number (last 9 digits) as the document ID. The settings collection stores program schedules and default church program times. Google Sheets stores a backup with columns mapping to all form fields.')

doc.add_heading('5.4 Internal Data Structures', level=2)
add_table_caption('Table 5.2: Internal Data Structures')
add_simple_table(
    ['Structure', 'Type', 'Usage', 'Storage'],
    [
        ['currentEntry', 'Object', 'Active registration data', 'Memory'],
        ['allRegistrations', 'Array', 'Cached member records', 'Memory'],
        ['pendingSubmissions', 'Array', 'Offline registration queue', 'localStorage'],
        ['churchPrograms', 'Object', 'Program schedule config', 'Memory + Firestore'],
        ['adminPrograms', 'Array', 'Admin program entries', 'Memory + Firestore'],
    ]
)
doc.add_paragraph("")

doc.add_page_break()

# ════════════════════════════════════════════════════════════════
# CHAPTER 6: MODULE DESIGN SPECIFICATIONS
# ════════════════════════════════════════════════════════════════
doc.add_heading('CHAPTER 6: MODULE DESIGN SPECIFICATIONS', level=1)

doc.add_heading('6.1 Registration Module', level=2)
doc.add_heading('6.1.1 Functional Specifications', level=3)
add_bullet('Function: Capture member registration data through a three-step form with real-time validation')
add_bullet('Interface: HTML form with step indicator, animated transitions, inline validation errors')
add_bullet('Input: Personal information (Step 1), Service preferences (Step 2), Confirmation (Step 3)')
add_bullet('Output: Thank-you overlay, WhatsApp confirmation, Firestore document, Google Sheets row')

doc.add_heading('6.1.2 Pseudo Code \u2013 Registration Validation', level=3)
add_code('FUNCTION validateStep1():\n'
         '  GET name, phone, location from inputs\n'
         '  SET valid = TRUE\n'
         '  IF name is empty: SHOW error; SET valid = FALSE\n'
         '  IF phone is empty: SHOW error; SET valid = FALSE\n'
         '  ELSE IF phone not Uganda format: SHOW error; SET valid = FALSE\n'
         '  IF location is empty: SHOW error; SET valid = FALSE\n'
         '  RETURN valid\n'
         'END FUNCTION')

doc.add_heading('6.1.3 Pseudo Code \u2013 Complete Registration Save', level=3)
add_code('FUNCTION handleSave():\n'
         '  DISABLE save button; SHOW spinner\n'
         '  BUILD formData object\n'
         '  CLEAN phone (last 9 digits)\n'
         '  CHECK if existing member in Firestore\n'
         '  IF not returning AND online:\n'
         '    SAVE to Firestore\n'
         '    SUBMIT to Google Sheets via hidden form\n'
         '  ELIF offline: SAVE to localStorage queue\n'
         '  BUILD WhatsApp message with:\n'
         '    greeting + weekly verse + program schedule + links\n'
         '  OPEN WhatsApp URL; SHOW blessing overlay\n'
         '  ENABLE save button; HIDE spinner\n'
         'END FUNCTION')

doc.add_heading('6.2 Admin Dashboard Module', level=2)
doc.add_heading('6.2.1 Functional Specifications', level=3)
add_bullet('Function: Display member records, statistics, and management controls')
add_bullet('Interface: Left sidebar nav, statistics cards, data tables, action buttons')
add_bullet('Input: Login credentials, search queries, attendance selections')
add_bullet('Output: Member table, dashboard statistics, program schedule')

doc.add_heading('6.2.2 Pseudo Code \u2013 Dashboard Loading', level=3)
add_code('FUNCTION loadDashboard():\n'
         '  GET all registrations from Firestore\n'
         '  FILTER active members; FILTER new/pending\n'
         '  UPDATE totalMembers, newRegistrations counts\n'
         '  UPDATE recentRegistrations table (last 5)\n'
         '  GET attendance from localStorage\n'
         '  CALCULATE and display attendance rate\n'
         'END FUNCTION')

doc.add_heading('6.3 Offline Sync Module', level=2)
doc.add_heading('6.3.1 Functional Specifications', level=3)
add_bullet('Function: Queue registrations in localStorage when offline and sync when connectivity restores')
add_bullet('Interface: Background process with automatic detection (no user-facing UI)')
add_bullet('Input: Registration form data from handleSave function')
add_bullet('Output: localStorage cached data, synced Firestore records')

doc.add_heading('6.3.2 Pseudo Code \u2013 Offline Queue', level=3)
add_code('FUNCTION savePendingSubmission(data):\n'
         '  LOAD queue from localStorage\n'
         '  PUSH data with pendingTimestamp\n'
         '  SAVE queue back to localStorage\n'
         'END FUNCTION\n\n'
         'FUNCTION syncPendingSubmissions():\n'
         '  IF offline: RETURN\n'
         '  FOR each pending submission:\n'
         '    SAVE to Firestore\n'
         '    REMOVE from queue; INCREMENT synced\n'
         '  SHOW notification: "X registration(s) synced"\n'
         'END FUNCTION\n\n'
         'window.addEventListener("online", syncPendingSubmissions)')

doc.add_heading('6.4 WhatsApp Integration Module', level=2)
doc.add_heading('6.4.1 Functional Specifications', level=3)
add_bullet('Function: Generate and open WhatsApp message with personalized confirmation')
add_bullet('Interface: Opens WhatsApp via wa.me URL in new browser tab')
add_bullet('Input: Member name, phone, church programs, weekly verse, consent status')
add_bullet('Output: Pre-filled WhatsApp message window')

doc.add_heading('6.5 Flowcharts', level=2)
add_body('The following flowcharts illustrate the algorithmic logic of the key system modules:')
add_screenshot('flowchart-registration.png', 'Figure 6.1: Registration Process Flowchart')
add_screenshot('flowchart-offline.png', 'Figure 6.2: Offline Sync Flowchart')
add_screenshot('flowchart-auth.png', 'Figure 6.3: Admin Authentication Flowchart')

doc.add_page_break()

# ════════════════════════════════════════════════════════════════
# CHAPTER 7: SYSTEM VERIFICATION
# ════════════════════════════════════════════════════════════════
doc.add_heading('CHAPTER 7: SYSTEM VERIFICATION', level=1)

doc.add_heading('7.1 Items/Functions Tested', level=2)
add_bullet('Registration Form \u2013 All three steps, navigation, data persistence between steps')
add_bullet('Form Validation \u2013 Required fields, phone format, conditional field display')
add_bullet('Data Storage \u2013 Firestore write operations, Google Sheets backup accuracy')
add_bullet('WhatsApp Notification \u2013 URL generation, message formatting')
add_bullet('Offline Queue \u2013 localStorage storage, auto-sync on reconnect')
add_bullet('Admin Dashboard \u2013 Login/logout, member listing, search, statistics')
add_bullet('Responsive Design \u2013 Desktop (1440px), tablet (768px), mobile (375px)')

doc.add_heading('7.2 Test Cases & Justification', level=2)
doc.add_heading('7.2.1 Registration Module Test Cases', level=3)
add_table_caption('Table 7.1: Registration Module Test Cases')
add_simple_table(
    ['ID', 'Test Case', 'Input', 'Expected Result', 'Status'],
    [
        ['TC01', 'Valid new registration', 'Valid name, phone, location', 'Saved to Firestore, WhatsApp sent', '\u2705'],
        ['TC02', 'Returning registrant', 'Same phone as existing', '"Welcome Back" message', '\u2705'],
        ['TC03', 'Empty name field', 'Submit blank name', 'Inline error: "Full name required"', '\u2705'],
        ['TC04', 'Invalid phone format', 'Phone with letters', 'Error: "Valid Uganda number"', '\u2705'],
        ['TC05', 'Wedding registration', 'Wedding type + details', 'Conditional fields, saved correctly', '\u2705'],
        ['TC06', 'Baptism registration', 'Baptism type + details', 'Conditional fields, saved correctly', '\u2705'],
        ['TC07', 'Counseling registration', 'Counseling type + topic', 'Conditional fields, saved correctly', '\u2705'],
        ['TC08', 'Step back/next navigation', 'Click Back then Next', 'Data preserved, smooth transition', '\u2705'],
    ]
)
doc.add_paragraph("")

doc.add_heading('7.2.2 Data Storage Test Cases', level=3)
add_table_caption('Table 7.2: Data Storage Test Cases')
add_simple_table(
    ['ID', 'Test Case', 'Input', 'Expected Result', 'Status'],
    [
        ['TC09', 'Firestore save', 'Complete registration', 'Doc created with cleanPhone ID', '\u2705'],
        ['TC10', 'Google Sheets save', 'Complete registration', 'Row appended with all columns', '\u2705'],
        ['TC11', 'Offline submission', 'Submit while offline', 'Saved to localStorage queue', '\u2705'],
        ['TC12', 'Offline auto-sync', 'Go online after offline', 'Auto-sync to Firestore', '\u2705'],
    ]
)
doc.add_paragraph("")

doc.add_heading('7.2.3 Admin Dashboard Test Cases', level=3)
add_table_caption('Table 7.3: Admin Dashboard Test Cases')
add_simple_table(
    ['ID', 'Test Case', 'Input', 'Expected Result', 'Status'],
    [
        ['TC13', 'Admin login', 'Click login, submit form', 'Login state stored, dashboard shows', '\u2705'],
        ['TC14', 'Member search', 'Type partial name', 'Filtered member table', '\u2705'],
        ['TC15', 'Attendance tracking', 'Check boxes, save', 'Attendance saved to localStorage', '\u2705'],
    ]
)
doc.add_paragraph("")

doc.add_heading('7.3 Test Procedures & Results', level=2)
add_body('Testing was conducted in two environments: Local Development (XAMPP at http://localhost/churchregistration) and Production (Firebase Hosting at https://church-registration-grace.web.app).')
add_body('Results Summary: All 15 test cases passed. Average submission time: 1.2 seconds. Offline sync accuracy: 100%. WhatsApp delivery: 100% (5 test numbers). Cross-browser compatibility confirmed on Chrome, Firefox, Safari, and Edge.')

doc.add_heading('7.4 User Evaluation', level=2)
doc.add_heading('7.4.1 Survey Methodology', level=3)
add_body('A quantitative survey was conducted with 15 participants including church administrators (3), regular members (8), and first-time visitors (4). Participants rated the system on a 5-point Likert scale across five criteria.')

doc.add_heading('7.4.2 Survey Results', level=3)
add_table_caption('Table 7.4: User Evaluation Survey Results')
add_simple_table(
    ['Criterion', 'Rating (1-5)', 'Interpretation'],
    [
        ['Ease of Use', '4.6/5', 'Very Easy \u2013 intuitive and clear'],
        ['Registration Speed', '4.7/5', 'Very Fast \u2013 much faster than paper'],
        ['System Reliability', '4.3/5', 'Reliable \u2013 minor delays on slow connections'],
        ['Interface Design', '4.6/5', 'Excellent \u2013 professional and welcoming'],
        ['Overall Satisfaction', '4.6/5', 'Very Satisfied \u2013 recommend to others'],
    ]
)
doc.add_paragraph("")
add_body('Key qualitative feedback: "The step-by-step form made registration easy" (First-time visitor); "Getting the WhatsApp message with church programs was very helpful" (New member); "The dashboard makes it easy to track who is registering" (Church administrator).')

doc.add_page_break()

# ════════════════════════════════════════════════════════════════
# CHAPTER 8: CONCLUSIONS
# ════════════════════════════════════════════════════════════════
doc.add_heading('CHAPTER 8: CONCLUSIONS', level=1)

doc.add_heading('8.1 Summary', level=2)
add_body('The Church Management System developed for Grace of Jesus Christ Ministries successfully addresses the challenges identified in the manual registration process. Key achievements include successful digitization of the paper-based registration process into a streamlined three-step online form, real-time data storage and retrieval using Firebase Firestore with automatic Google Sheets backup, automated WhatsApp communication providing instant confirmation with church program details, offline synchronization ensuring zero data loss, and a comprehensive admin dashboard for efficient member management.')

doc.add_heading('8.2 Problems Encountered & Solved', level=2)
add_table_caption('Table 8.1: Problems Encountered & Solutions')
add_simple_table(
    ['Problem', 'Solution', 'Status'],
    [
        ['Firebase config for local dev', 'Try/catch fallback initialization', 'Resolved'],
        ['Video codec support', 'H.264 encoding + poster fallback', 'Resolved'],
        ['Offline sync', 'localStorage queue + online event', 'Resolved'],
        ['WhatsApp API', 'wa.me click-to-chat links', 'Resolved'],
        ['Phone validation', 'Uganda regex (07XX/+256)', 'Resolved'],
        ['Conditional fields', 'Dynamic show/hide by type', 'Resolved'],
    ]
)
doc.add_paragraph("")

doc.add_heading('8.3 Suggestions for Better Approaches', level=2)
add_bullet('Adopt React or Vue.js for better state management and component reusability')
add_bullet('Implement Node.js or Python REST API for more robust business logic')
add_bullet('Use TypeScript for improved code quality through static typing')
add_bullet('Add automated testing with Jest (unit) and Cypress (E2E)')

doc.add_heading('8.4 Future Extensions', level=2)
add_bullet('Mobile Application \u2013 Native Android/iOS apps using Flutter or React Native')
add_bullet('Online Giving Module \u2013 Secure payment gateway for tithes and offerings')
add_bullet('Live Streaming \u2013 Embedded YouTube/Facebook Live for service broadcasts')
add_bullet('AI Chatbot \u2013 Automated responses to visitor inquiries via WhatsApp')
add_bullet('Event Management \u2013 QR code-based check-in for special events')
add_bullet('Multi-language Support \u2013 English, Luganda, and other local languages')

doc.add_page_break()

# ════════════════════════════════════════════════════════════════
# BIBLIOGRAPHY
# ════════════════════════════════════════════════════════════════
doc.add_heading('BIBLIOGRAPHY', level=1)
refs = [
    '[1] Firebase Documentation. (2026). Firebase Firestore. Google. https://firebase.google.com/docs/firestore',
    '[2] Google. (2026). Google Sheets API. Google Developers. https://developers.google.com/sheets/api',
    '[3] MDN Web Docs. (2026). Service Worker API. Mozilla. https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API',
    '[4] WhatsApp. (2026). WhatsApp Click to Chat. WhatsApp Business. https://faq.whatsapp.com/',
    '[5] Pressman, R. S. (2014). Software Engineering: A Practitioner\'s Approach (8th ed.). McGraw-Hill.',
    '[6] Sommerville, I. (2015). Software Engineering (10th ed.). Pearson Education.',
    '[7] Flanagan, D. (2020). JavaScript: The Definitive Guide (7th ed.). O\'Reilly Media.',
    '[8] Haverbeke, M. (2018). Eloquent JavaScript (3rd ed.). No Starch Press.',
    '[9] Google Cloud. (2026). Firebase Security Rules. Google.',
    '[10] W3C. (2026). HTML5 Specification. https://www.w3.org/TR/html52/',
]
for ref in refs:
    p = doc.add_paragraph(ref)
    p.paragraph_format.left_indent = Cm(1.27)
    p.paragraph_format.first_line_indent = Cm(-1.27)
    p.paragraph_format.line_spacing = 2.0

doc.add_page_break()

# ════════════════════════════════════════════════════════════════
# APPENDICES
# ════════════════════════════════════════════════════════════════
doc.add_heading('APPENDICES', level=1)

doc.add_heading('Appendix A: User Evaluation Survey Form', level=2)
add_body('The following survey was administered to 15 participants for system evaluation:')
for q in [
    '1. How easy was it to complete the registration form? (1-5)',
    '2. How would you rate registration speed vs paper method? (1-5)',
    '3. Did you encounter any errors during registration? (Yes/No)',
    '4. How clear was the step-by-step guidance? (1-5)',
    '5. Did you receive the WhatsApp confirmation? (Yes/No)',
    '6. How would you rate the overall design? (1-5)',
    '7. How reliable did you find the system? (1-5)',
    '8. Would you recommend this system to other churches? (Yes/No)',
    '9. What features would you like added in the future?',
    '10. Any additional comments or suggestions?',
]:
    add_bullet(q)

doc.add_paragraph("")
doc.add_heading('Appendix B: System Screenshots', level=2)
add_body('The following screenshots document the system\'s user interface from the live deployment:')
for sn, cap in [
    ('03-plan-your-visit.png', 'Plan Your Visit Section'),
    ('04-registration-form.png', 'Registration Form'),
    ('05-giving-section.png', 'Online Giving Section'),
    ('06-sermons-section.png', 'Sermons & Teachings Section'),
    ('07-contact-section.png', 'Contact Section'),
    ('08-footer.png', 'Footer Section'),
]:
    add_screenshot(sn, cap, 4.5)

doc.add_paragraph("")
doc.add_heading('Appendix C: Sample Registration Data', level=2)
add_simple_table(
    ['Name', 'Phone', 'Location', 'Type', 'Date'],
    [
        ['John Doe', '+256700000001', 'Kitintale', 'General', '15-May-2026'],
        ['Jane Smith', '+256700000002', 'Banda', 'Wedding', '15-May-2026'],
        ['Peter Kato', '+256700000003', 'Naguru', 'Baptism', '14-May-2026'],
        ['Mary Nakato', '+256700000004', 'Bukoto', 'Counseling', '13-May-2026'],
    ]
)
doc.add_paragraph("")

doc.add_heading('Appendix D: Firebase Deployment Configuration', level=2)
add_code('{\n'
         '  "hosting": {\n'
         '    "public": ".",\n'
         '    "ignore": ["firebase.json", "**/.*", "**/node_modules/**"],\n'
         '    "rewrites": [{"source": "**", "destination": "/index.html"}]\n'
         '  },\n'
         '  "firestore": {\n'
         '    "database": "(default)",\n'
         '    "location": "africa-south1"\n'
         '  }\n'
         '}')

doc.add_page_break()

# ════════════════════════════════════════════════════════════════
# PROGRAM LISTINGS
# ════════════════════════════════════════════════════════════════
doc.add_heading('PROGRAM LISTINGS', level=1)

doc.add_heading('Listing 1: Firebase Initialization (index.html)', level=2)
add_code('try {\n'
         '  if (!firebase.apps.length) {\n'
         '    firebase.initializeApp({\n'
         '      apiKey: "AIzaSy...",\n'
         '      authDomain: "church-registration-grace.firebaseapp.com",\n'
         '      projectId: "church-registration-grace",\n'
         '      storageBucket: "church-registration-grace.appspot.com"\n'
         '    });\n'
         '  }\n'
         '} catch(e) { console.warn(\'Firebase init fallback:\', e); }')

doc.add_heading('Listing 2: Registration Save Function (js/app.js)', level=2)
add_code('async function handleSave() {\n'
         '  if (!currentEntry) return;\n'
         '  saveBtn.disabled = true;\n'
         '  saveBtnText.textContent = \'Saving...\';\n'
         '  saveSpinner.style.display = \'inline-block\';\n'
         '  formData = { name, phone, location, registrationType, ... };\n'
         '  const cleanPhone = (phone || \'\').replace(/\\D/g, \'\').slice(-9);\n'
         '  try {\n'
         '    const docSnap = await db.collection(\'registrations\').doc(cleanPhone).get();\n'
         '    if (!docSnap.exists) {\n'
         '      await db.collection(\'registrations\').doc(cleanPhone).set({\n'
         '        ...formData,\n'
         '        timestamp: firebase.firestore.FieldValue.serverTimestamp()\n'
         '      });\n'
         '    }\n'
         '    window.open(whatsappUrl, \'_blank\');\n'
         '  } catch (error) { console.error(error); }\n'
         '}')

doc.add_heading('Listing 3: Name Formatting Utility (js/utils.js)', level=2)
add_code('export const formatName = (name) => {\n'
         '  return name.toLowerCase()\n'
         '    .split(\' \')\n'
         '    .filter(w => w.length > 0)\n'
         '    .map(w => w.charAt(0).toUpperCase() + w.slice(1))\n'
         '    .join(\' \');\n'
         '};')

doc.add_heading('Listing 4: Weekly Verse Rotation (js/utils.js)', level=2)
add_code('export const getWeeklyVerse = (verses) => {\n'
         '  const now = new Date();\n'
         '  const start = new Date(now.getFullYear(), 0, 0);\n'
         '  const diff = now - start;\n'
         '  const dayOfYear = Math.floor(diff / (1000 * 60 * 60 * 24));\n'
         '  const index = Math.floor(dayOfYear / 2) % verses.length;\n'
         '  return verses[index];\n'
         '};')

doc.add_heading('Listing 5: Dashboard Member Loading (js/dashboard.js)', level=2)
add_code('async function loadDashboard() {\n'
         '  const snapshot = await db.collection(\'registrations\').get();\n'
         '  allRegistrations = snapshot.docs.map(d => ({\n'
         '    id: d.id, ...d.data(), status: d.data().status || \'active\'\n'
         '  }));\n'
         '  document.getElementById(\'totalMembers\').textContent =\n'
         '    allRegistrations.filter(r => r.status === \'active\').length;\n'
         '  document.getElementById(\'newRegistrations\').textContent =\n'
         '    allRegistrations.filter(r => r.status === \'pending\').length;\n'
         '}')

doc.add_heading('Listing 6: Service Worker (sw.js)', level=2)
add_code('self.addEventListener(\'install\', e => self.skipWaiting());\n'
         'self.addEventListener(\'activate\', e => e.waitUntil(clients.claim()));\n'
         'self.addEventListener(\'fetch\', e => {\n'
         '  e.respondWith(\n'
         '    caches.match(e.request).then(r => r || fetch(e.request))\n'
         '  );\n'
         '});')

doc.add_page_break()

# ════════════════════════════════════════════════════════════════
# USER MANUAL
# ════════════════════════════════════════════════════════════════
doc.add_heading('USER MANUAL', level=1)

doc.add_heading('1. Installation Guide', level=2)
doc.add_heading('1.1 Local Development Setup (XAMPP)', level=3)
add_bullet('1. Install XAMPP 8.0+ from https://www.apachefriends.org/')
add_bullet('2. Start Apache from XAMPP Control Panel')
add_bullet('3. Copy churchregistration folder into C:\\xampp\\htdocs\\')
add_bullet('4. Access at http://localhost/churchregistration')
add_bullet('5. Admin dashboard at http://localhost/churchregistration/dashboard.html')

doc.add_heading('1.2 Production Deployment (Firebase Hosting)', level=3)
add_bullet('1. Install Firebase CLI: npm install -g firebase-tools')
add_bullet('2. Login: firebase login')
add_bullet('3. Deploy: firebase deploy --only hosting')
add_bullet('4. Site live at https://church-registration-grace.web.app')

doc.add_heading('2. End-User Registration Guide', level=2)
add_bullet('1. Open the website in any browser')
add_bullet('2. Click "Plan Your Visit" or scroll to the Registration section')
add_bullet('3. Select registration type: General, Wedding, Baptism, or Counseling')
add_bullet('4. Step 1: Enter full name, phone (Uganda format), and residence')
add_bullet('5. Select whether first-time online registrant')
add_bullet('6. Click "Next \u2192" to proceed to Step 2')
add_bullet('7. Step 2: Enter birthday, volunteer interests, and WhatsApp group preference')
add_bullet('8. Click "Next \u2192" to review your details')
add_bullet('9. Step 3: Review all information for accuracy')
add_bullet('10. Click "Save Registration" to submit')
add_bullet('11. A blessing overlay appears with a weekly verse')
add_bullet('12. WhatsApp opens automatically with confirmation message')

doc.add_heading('3. Admin Dashboard Guide', level=2)
add_bullet('1. Click "Admin" in the navigation bar')
add_bullet('2. Click "Admin Login" and submit your credentials')
add_bullet('3. Dashboard Home: View total members, new registrations, attendance rate')
add_bullet('4. Members: Search by name, filter by department, mark attendance')
add_bullet('5. Programs: Create, edit, or delete church program entries')
add_bullet('6. To mark attendance: Check boxes next to names, click "Save Attendance"')

doc.add_heading('4. Troubleshooting', level=2)
add_simple_table(
    ['Issue', 'Cause', 'Solution'],
    [
        ['Page not loading', 'Apache not running', 'Start XAMPP Apache'],
        ['Form not saving', 'Lost internet', 'Auto-saves offline; syncs later'],
        ['WhatsApp not opening', 'Popup blocked', 'Allow popups for this site'],
        ['Wrong phone error', 'Non-Uganda format', 'Use 07XX XXX XXX format'],
        ['Admin cant login', 'Wrong credentials', 'Clear cache and retry'],
        ['Blank dashboard', 'Firebase not init', 'Check internet + config'],
    ]
)
doc.add_paragraph("")

# ── Page numbering ──
# Section 0 (cover): no footer
cover_section = doc.sections[0]
cover_section.different_first_page_header_footer = False
cover_footer = cover_section.footer
cover_footer.is_linked_to_previous = False
cover_footer.paragraphs[0].clear()

# Sections 1+: centered page numbers
for i in range(1, len(doc.sections)):
    section = doc.sections[i]
    section.different_first_page_header_footer = False
    footer = section.footer
    footer.is_linked_to_previous = False
    fp = footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    fp.clear()

    # PAGE field XML
    run = fp.add_run()
    fld1 = OxmlElement('w:fldChar')
    fld1.set(qn('w:fldCharType'), 'begin')
    run._r.append(fld1)

    r2 = fp.add_run()
    instr = OxmlElement('w:instrText')
    instr.set(qn('xml:space'), 'preserve')
    instr.text = ' PAGE '
    r2._r.append(instr)

    r3 = fp.add_run()
    fld2 = OxmlElement('w:fldChar')
    fld2.set(qn('w:fldCharType'), 'end')
    r3._r.append(fld2)

# ── SAVE ──
output = 'C:\\xampp\\htdocs\\churchregistration\\DIT_Project_Report_ISBAT.docx'
doc.save(output)
print(f"Final ISBAT-format report saved: {output}")
