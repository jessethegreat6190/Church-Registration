from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR_TYPE
from pptx.oxml.ns import qn
from lxml import etree
import os

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# Color scheme
DARK_BLUE = RGBColor(0x2C, 0x3E, 0x50)
BLUE = RGBColor(0x34, 0x98, 0xDB)
LIGHT_BLUE = RGBColor(0x5D, 0xAE, 0xE0)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_GRAY = RGBColor(0xEC, 0xF0, 0xF1)
GOLD = RGBColor(0xD4, 0xA8, 0x43)
DARK_GRAY = RGBColor(0x33, 0x33, 0x33)

def add_background(slide, color):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_shape(slide, left, top, width, height, color, alpha=None):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    if alpha is not None:
        solidFill = shape.fill._fill
        srgbClr = solidFill.find('.//{http://schemas.openxmlformats.org/drawingml/2006/main}srgbClr')
        if srgbClr is not None:
            alpha_elem = etree.SubElement(srgbClr, '{http://schemas.openxmlformats.org/drawingml/2006/main}alpha')
            alpha_elem.set('val', str(int(alpha * 1000)))
    return shape

def add_text_box(slide, left, top, width, height, text, font_size=18, color=DARK_GRAY, bold=False, alignment=PP_ALIGN.LEFT, font_name='Calibri'):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.color.rgb = color
    p.font.bold = bold
    p.font.name = font_name
    p.alignment = alignment
    return txBox

def add_bullet_list(slide, left, top, width, height, items, font_size=16, color=DARK_GRAY, spacing=Pt(8)):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.text = item
        p.font.size = Pt(font_size)
        p.font.color.rgb = color
        p.font.name = 'Calibri'
        p.space_after = spacing
        p.level = 0
    return txBox

# SLIDE 1: Title Slide
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide, DARK_BLUE)
add_shape(slide, Inches(0), Inches(3.2), Inches(13.333), Inches(0.06), GOLD)
add_text_box(slide, Inches(1), Inches(1.5), Inches(11.333), Inches(1.5),
             "Church Registration System", 44, WHITE, True, PP_ALIGN.CENTER)
add_text_box(slide, Inches(1), Inches(3.5), Inches(11.333), Inches(1),
             "Grace of Jesus Christ Ministries – Kitintale, Kampala", 28, LIGHT_BLUE, False, PP_ALIGN.CENTER)
add_text_box(slide, Inches(1), Inches(5), Inches(11.333), Inches(0.8),
             "A Modern Digital Solution for Church Member Management", 20, GOLD, False, PP_ALIGN.CENTER)

# SLIDE 2: About
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide, WHITE)
add_shape(slide, Inches(0), Inches(0), Inches(13.333), Inches(1.2), DARK_BLUE)
add_text_box(slide, Inches(0.8), Inches(0.25), Inches(11), Inches(0.8),
             "About", 36, WHITE, True)
add_shape(slide, Inches(0.8), Inches(1.6), Inches(0.08), Inches(0.6), GOLD)
add_text_box(slide, Inches(1.2), Inches(1.6), Inches(11), Inches(0.6),
             "Project Overview", 24, DARK_BLUE, True)
items = [
    "• Grace of Jesus Christ Ministries is a prophetic church located in Kitintale, Kampala, Uganda",
    "• The church slogan: \"An encounter with the Holy Spirit\"",
    "• Holds Sunday services, prayer meetings, counseling sessions, and special events",
    "• Experienced rapid growth, making manual registration processes inefficient",
    "• This project digitizes the entire registration and member management workflow",
    "• Built with modern web technologies: HTML5, CSS3, JavaScript, Firebase, and Google Sheets"
]
add_bullet_list(slide, Inches(1.2), Inches(2.4), Inches(10.5), Inches(4.5), items, 18, DARK_GRAY, Pt(12))

# SLIDE 3: Abstract
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide, WHITE)
add_shape(slide, Inches(0), Inches(0), Inches(13.333), Inches(1.2), DARK_BLUE)
add_text_box(slide, Inches(0.8), Inches(0.25), Inches(11), Inches(0.8),
             "Abstract", 36, WHITE, True)
add_shape(slide, Inches(0.8), Inches(1.6), Inches(0.08), Inches(0.6), GOLD)
add_text_box(slide, Inches(1.2), Inches(1.6), Inches(11), Inches(0.6),
             "Summary", 24, DARK_BLUE, True)
abstract_text = (
    "This project presents a comprehensive Church Registration System designed to replace the "
    "manual, paper-based registration process at Grace of Jesus Christ Ministries. The system "
    "provides a multi-step online registration portal for church visitors and members, coupled "
    "with an administrative dashboard for church leadership to manage member data, track church "
    "growth, and organize events.\n\n"
    "The system leverages Firebase Firestore for real-time data storage, Google Sheets as a "
    "backup database, and includes offline support through localStorage and Service Workers. "
    "Additional features include WhatsApp integration for automated confirmations, media library "
    "management, and church program scheduling."
)
add_text_box(slide, Inches(1.2), Inches(2.5), Inches(10.5), Inches(4),
             abstract_text, 18, DARK_GRAY, False, PP_ALIGN.LEFT)

# SLIDE 4: Existing System
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide, WHITE)
add_shape(slide, Inches(0), Inches(0), Inches(13.333), Inches(1.2), DARK_BLUE)
add_text_box(slide, Inches(0.8), Inches(0.25), Inches(11), Inches(0.8),
             "Existing System", 36, WHITE, True)
add_shape(slide, Inches(0.8), Inches(1.6), Inches(0.08), Inches(0.6), GOLD)
add_text_box(slide, Inches(1.2), Inches(1.6), Inches(11), Inches(0.6),
             "Current Manual Process", 24, DARK_BLUE, True)
items = [
    "• Paper-based registration books at the church entrance",
    "• Manual data entry into spreadsheets by church administrators",
    "• No centralized database for member information",
    "• Difficult to track attendance, growth trends, or member engagement",
    "• High risk of data loss, duplication, or errors",
    "• No automated communication with registered members",
    "• Time-consuming reporting and data retrieval processes",
    "• Limited accessibility – only available physically at the church"
]
add_bullet_list(slide, Inches(1.2), Inches(2.4), Inches(10.5), Inches(4.5), items, 18, DARK_GRAY, Pt(12))

# SLIDE 5: Proposed System
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide, WHITE)
add_shape(slide, Inches(0), Inches(0), Inches(13.333), Inches(1.2), DARK_BLUE)
add_text_box(slide, Inches(0.8), Inches(0.25), Inches(11), Inches(0.8),
             "Proposed System", 36, WHITE, True)
add_shape(slide, Inches(0.8), Inches(1.6), Inches(0.08), Inches(0.6), GOLD)
add_text_box(slide, Inches(1.2), Inches(1.6), Inches(11), Inches(0.6),
             "Digital Solution", 24, DARK_BLUE, True)
items = [
    "• Multi-step online registration form accessible via web browsers",
    "• Real-time data storage using Firebase Firestore",
    "• Google Sheets integration as backup database",
    "• Admin dashboard for member management, analytics, and reporting",
    "• Automated WhatsApp confirmation messages after registration",
    "• Offline support with localStorage and Service Worker caching",
    "• Media library for sermons, events, and church photos",
    "• Church program scheduling and event management",
    "• Responsive design for mobile, tablet, and desktop access"
]
add_bullet_list(slide, Inches(1.2), Inches(2.4), Inches(10.5), Inches(4.5), items, 18, DARK_GRAY, Pt(12))

# SLIDE 6: Advantages
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide, WHITE)
add_shape(slide, Inches(0), Inches(0), Inches(13.333), Inches(1.2), BLUE)
add_text_box(slide, Inches(0.8), Inches(0.25), Inches(11), Inches(0.8),
             "Advantages", 36, WHITE, True)
add_shape(slide, Inches(0.8), Inches(1.6), Inches(0.08), Inches(0.6), GOLD)
items = [
    "• Efficient Data Management – Instant storage, retrieval, and updating of member records",
    "• Accessibility – Register from anywhere with internet access",
    "• Data Security – Encrypted storage with Firebase security rules",
    "• Automated Communication – WhatsApp integration for instant confirmations",
    "• Analytics & Reporting – Real-time statistics on church growth and attendance",
    "• Offline Support – Registrations saved locally and synced when online",
    "• Scalability – System grows with the church without performance issues",
    "• Cost-Effective – Free tier Firebase and Google Sheets reduce hosting costs",
    "• User-Friendly – Intuitive interface requiring minimal training"
]
add_bullet_list(slide, Inches(1.2), Inches(2.4), Inches(10.5), Inches(4.5), items, 18, DARK_GRAY, Pt(12))

# SLIDE 7: Disadvantages
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide, WHITE)
add_shape(slide, Inches(0), Inches(0), Inches(13.333), Inches(1.2), RGBColor(0xE7, 0x4C, 0x3C))
add_text_box(slide, Inches(0.8), Inches(0.25), Inches(11), Inches(0.8),
             "Disadvantages", 36, WHITE, True)
add_shape(slide, Inches(0.8), Inches(1.6), Inches(0.08), Inches(0.6), GOLD)
items = [
    "• Internet Dependency – Requires internet connection for real-time features",
    "• Learning Curve – Church staff need training to use the admin dashboard",
    "• Third-Party Reliance – Depends on Firebase and Google services availability",
    "• Initial Setup Cost – Requires configuration of Firebase project and Google Sheets API",
    "• Data Migration – Existing paper records need to be digitized manually",
    "• Limited Offline Features – Some features unavailable without internet",
    "• Maintenance – Regular updates and monitoring required for optimal performance"
]
add_bullet_list(slide, Inches(1.2), Inches(2.4), Inches(10.5), Inches(4.5), items, 18, DARK_GRAY, Pt(12))

# SLIDE 8: Software Requirements
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide, WHITE)
add_shape(slide, Inches(0), Inches(0), Inches(13.333), Inches(1.2), DARK_BLUE)
add_text_box(slide, Inches(0.8), Inches(0.25), Inches(11), Inches(0.8),
             "Software Requirements", 36, WHITE, True)
add_shape(slide, Inches(0.8), Inches(1.6), Inches(0.08), Inches(0.6), GOLD)

# Frontend
add_text_box(slide, Inches(1.2), Inches(2.4), Inches(4.5), Inches(0.5),
             "Frontend", 22, BLUE, True)
frontend_items = [
    "• HTML5, CSS3, JavaScript (ES6+)",
    "• Responsive design with CSS Grid/Flexbox",
    "• FontAwesome icons",
    "• Google Fonts (Montserrat)",
    "• Service Workers for offline support"
]
add_bullet_list(slide, Inches(1.2), Inches(3), Inches(4.5), Inches(3), frontend_items, 16, DARK_GRAY, Pt(8))

# Backend & Database
add_text_box(slide, Inches(7), Inches(2.4), Inches(5), Inches(0.5),
             "Backend & Database", 22, BLUE, True)
backend_items = [
    "• Firebase Firestore (NoSQL database)",
    "• Firebase Authentication (Admin login)",
    "• Firebase Storage (Media files)",
    "• Google Sheets API (Backup storage)",
    "• Google Apps Script (Sheet integration)",
    "• WhatsApp Business API (Messaging)"
]
add_bullet_list(slide, Inches(7), Inches(3), Inches(5), Inches(3), backend_items, 16, DARK_GRAY, Pt(8))

# Development Tools
add_text_box(slide, Inches(1.2), Inches(5.2), Inches(4.5), Inches(0.5),
             "Development Tools", 22, BLUE, True)
tools_items = [
    "• XAMPP (Local server)",
    "• Git & GitHub (Version control)",
    "• VS Code (Code editor)",
    "• Chrome DevTools (Debugging)"
]
add_bullet_list(slide, Inches(1.2), Inches(5.8), Inches(4.5), Inches(2), tools_items, 16, DARK_GRAY, Pt(8))

# SLIDE 9: About Project
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide, WHITE)
add_shape(slide, Inches(0), Inches(0), Inches(13.333), Inches(1.2), DARK_BLUE)
add_text_box(slide, Inches(0.8), Inches(0.25), Inches(11), Inches(0.8),
             "About Project", 36, WHITE, True)
add_shape(slide, Inches(0.8), Inches(1.6), Inches(0.08), Inches(0.6), GOLD)
items = [
    "• Project Name: Church Registration System",
    "• Organization: Grace of Jesus Christ Ministries",
    "• Location: Kitintale, Kampala, Uganda",
    "• Technology Stack: Firebase, Google Sheets, Vanilla JavaScript",
    "• Development Environment: XAMPP (Local), Firebase Hosting (Production)",
    "• Repository: github.com/jessethegreat6190/Church-Registration",
    "• Key Features: Multi-step registration, admin dashboard, WhatsApp integration, offline sync",
    "• Target Users: Church visitors, members, and administrators",
    "• Status: Fully functional and deployed"
]
add_bullet_list(slide, Inches(1.2), Inches(2.4), Inches(10.5), Inches(4.5), items, 18, DARK_GRAY, Pt(12))

# SLIDE 10: System Architecture
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide, WHITE)
add_shape(slide, Inches(0), Inches(0), Inches(13.333), Inches(1.2), DARK_BLUE)
add_text_box(slide, Inches(0.8), Inches(0.25), Inches(11), Inches(0.8),
             "System Architecture", 36, WHITE, True)
add_shape(slide, Inches(0.8), Inches(1.6), Inches(0.08), Inches(0.6), GOLD)

# Architecture diagram boxes
boxes = [
    (Inches(0.8), Inches(2.2), Inches(3), Inches(1.2), "User Interface\n(HTML/CSS/JS)", BLUE),
    (Inches(5.2), Inches(2.2), Inches(3), Inches(1.2), "Firebase Services\n(Auth, Firestore, Storage)", RGBColor(0xFF, 0xA7, 0x26)),
    (Inches(9.5), Inches(2.2), Inches(3), Inches(1.2), "Google Sheets\n(Backup Database)", RGBColor(0x0F, 0x9D, 0x58)),
    (Inches(0.8), Inches(4.2), Inches(3), Inches(1.2), "Admin Dashboard\n(Gold Theme)", GOLD),
    (Inches(5.2), Inches(4.2), Inches(3), Inches(1.2), "WhatsApp API\n(Automated Messages)", RGBColor(0x25, 0xD3, 0x66)),
    (Inches(9.5), Inches(4.2), Inches(3), Inches(1.2), "Service Worker\n(Offline Support)", RGBColor(0x9B, 0x59, 0xB6)),
]

for left, top, width, height, text, color in boxes:
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    tf = shape.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(16)
    p.font.color.rgb = WHITE
    p.font.bold = True
    p.alignment = PP_ALIGN.CENTER
    tf.paragraphs[0].space_before = Pt(10)

# Arrows – proper connector lines with arrowheads
def add_connector_arrow(slide, x1, y1, x2, y2, color=DARK_GRAY, width=Pt(2)):
    conn = slide.shapes.add_connector(MSO_CONNECTOR_TYPE.STRAIGHT, x1, y1, x2, y2)
    conn.line.color.rgb = color
    conn.line.width = width
    ln = conn.line._ln
    tail = etree.SubElement(ln, qn('a:tailEnd'))
    tail.set('type', 'triangle')
    tail.set('w', 'med')
    tail.set('len', 'med')
    return conn

# Row 1 arrows (UI → Firebase, Firebase → Sheets)
add_connector_arrow(slide, Inches(3.8), Inches(2.8), Inches(5.2), Inches(2.8))
add_connector_arrow(slide, Inches(8.2), Inches(2.8), Inches(9.5), Inches(2.8))

# Row 2 arrows (Admin → WhatsApp, WhatsApp → Service Worker)
add_connector_arrow(slide, Inches(3.8), Inches(4.8), Inches(5.2), Inches(4.8))
add_connector_arrow(slide, Inches(8.2), Inches(4.8), Inches(9.5), Inches(4.8))

# ── Flowchart helpers ──
FC_FILLS = {
    'terminal': RGBColor(0xAE, 0xD6, 0xF1),
    'process':  RGBColor(0xD4, 0xE6, 0xF1),
    'decision': RGBColor(0xF9, 0xE7, 0x9F),
}
FC_EDGE = DARK_BLUE

def fc_shape(slide, shape_type, left, top, width, height, fill_key):
    s = slide.shapes.add_shape(shape_type, left, top, width, height)
    s.fill.solid()
    s.fill.fore_color.rgb = FC_FILLS[fill_key]
    s.line.color.rgb = FC_EDGE
    s.line.width = Pt(1.5)
    return s

def fc_text(shape, text, size=10, bold=True):
    tf = shape.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(size)
    p.font.bold = bold
    p.font.color.rgb = DARK_BLUE
    p.font.name = 'Calibri'
    p.alignment = PP_ALIGN.CENTER
    return tf

def fc_arrow(slide, x1, y1, x2, y2, color=DARK_BLUE, width=Pt(1.5)):
    conn = slide.shapes.add_connector(MSO_CONNECTOR_TYPE.STRAIGHT, x1, y1, x2, y2)
    conn.line.color.rgb = color
    conn.line.width = width
    ln = conn.line._ln
    tail = etree.SubElement(ln, qn('a:tailEnd'))
    tail.set('type', 'triangle')
    tail.set('w', 'med')
    tail.set('len', 'med')
    return conn

def fc_label(slide, x, y, text, color=RGBColor(0xC0, 0x39, 0x2B)):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(0.6), Inches(0.3))
    p = tb.text_frame.paragraphs[0]
    p.text = text
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = color
    p.font.name = 'Calibri'
    p.alignment = PP_ALIGN.CENTER

def new_fc_slide(prs, title, fig_num):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, WHITE)
    add_shape(slide, Inches(0), Inches(0), Inches(13.333), Inches(1.0), DARK_BLUE)
    add_text_box(slide, Inches(0.8), Inches(0.15), Inches(11), Inches(0.7), title, 32, WHITE, True)
    add_shape(slide, Inches(0.8), Inches(1.2), Inches(0.08), Inches(0.5), GOLD)
    add_text_box(slide, Inches(1.2), Inches(1.2), Inches(11), Inches(0.5),
                 f"Figure {fig_num}: {title}", 18, DARK_BLUE, False)
    return slide

# SLIDE 11: Registration Process Flowchart
slide = new_fc_slide(prs, "Registration Process Flowchart", "6.1")
# Coordinates (center-x=6.67)
FC = 6.67  # center
# Row 1: START
s1 = fc_shape(slide, MSO_SHAPE.OVAL, Inches(FC-0.9), Inches(1.9), Inches(1.8), Inches(0.5), 'terminal')
fc_text(s1, "START", 10)
# Row 2: Fill Step 1
s2 = fc_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(FC-1.2), Inches(2.65), Inches(2.4), Inches(0.5), 'process')
fc_text(s2, "Fill Step 1:\nName, Phone, Location", 9)
# Row 3: Valid?
s3 = fc_shape(slide, MSO_SHAPE.DIAMOND, Inches(FC-0.8), Inches(3.45), Inches(1.6), Inches(0.6), 'decision')
fc_text(s3, "Valid?", 10)
# No branch: Show errors
s_no = fc_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(2.5), Inches(3.45), Inches(1.8), Inches(0.5), 'process')
fc_text(s_no, "Show inline\nerrors", 9)
# Row 4: First Time?
s4 = fc_shape(slide, MSO_SHAPE.DIAMOND, Inches(FC-0.8), Inches(4.35), Inches(1.6), Inches(0.6), 'decision')
fc_text(s4, "First\nTime?", 10)
# Yes -> Step 2 / No -> Review
s5 = fc_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(3.8), Inches(5.2), Inches(2.0), Inches(0.5), 'process')
fc_text(s5, "Fill Step 2:\nPreferences", 9)
s6 = fc_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.5), Inches(5.2), Inches(2.0), Inches(0.5), 'process')
fc_text(s6, "Review Step 3:\nConfirm Details", 9)
# Row 5: Save
s7 = fc_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(FC-1.3), Inches(6.0), Inches(2.6), Inches(0.5), 'process')
fc_text(s7, "Save to Firestore\n+ Google Sheets", 9)
# Row 6: Open WhatsApp + Oval END (compressed)
s8 = fc_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(FC-1.1), Inches(6.7), Inches(2.2), Inches(0.4), 'process')
fc_text(s8, "Open WhatsApp", 8)

# Arrows
fc_arrow(slide, Inches(FC), Inches(2.4), Inches(FC), Inches(2.65))
fc_arrow(slide, Inches(FC), Inches(3.15), Inches(FC), Inches(3.45))
fc_arrow(slide, Inches(FC), Inches(4.05), Inches(FC), Inches(4.35))
fc_arrow(slide, Inches(FC), Inches(4.95), Inches(3.8), Inches(5.2))
fc_arrow(slide, Inches(FC), Inches(4.95), Inches(7.5), Inches(5.2))
fc_arrow(slide, Inches(FC-4.17), Inches(3.7), Inches(FC-4.17+0.6), Inches(3.55))
fc_arrow(slide, Inches(4.8), Inches(5.7), Inches(FC-1.3+0.3), Inches(6.0))
fc_arrow(slide, Inches(8.5), Inches(5.7), Inches(FC+1.3-0.3), Inches(6.0))
fc_arrow(slide, Inches(FC), Inches(6.5), Inches(FC), Inches(6.7))
# Labels
fc_label(slide, FC+0.5, 3.7, "Yes", RGBColor(0x27, 0xAE, 0x60))
fc_label(slide, FC-2.8, 3.4, "No", RGBColor(0xC0, 0x39, 0x2B))
fc_label(slide, FC-1.5, 4.7, "Yes", RGBColor(0x27, 0xAE, 0x60))
fc_label(slide, FC+1.2, 4.65, "No", RGBColor(0xC0, 0x39, 0x2B))

# SLIDE 12: Offline Sync Flowchart
slide = new_fc_slide(prs, "Offline Sync Flowchart", "6.2")
# Row 1
s1 = fc_shape(slide, MSO_SHAPE.OVAL, Inches(FC-1.0), Inches(1.9), Inches(2.0), Inches(0.5), 'terminal')
fc_text(s1, "User submits\nregistration", 9)
# Row 2
s2 = fc_shape(slide, MSO_SHAPE.DIAMOND, Inches(FC-0.9), Inches(2.7), Inches(1.8), Inches(0.6), 'decision')
fc_text(s2, "Internet\nAvailable?", 9)
# Row 3 branches
s3a = fc_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(2.8), Inches(3.6), Inches(2.2), Inches(0.55), 'process')
fc_text(s3a, "Save to\nlocalStorage Queue", 9)
s3b = fc_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.3), Inches(3.6), Inches(2.2), Inches(0.55), 'process')
fc_text(s3b, "Save to Firestore\n+ Google Sheets", 9)
# Row 4
s4 = fc_shape(slide, MSO_SHAPE.DIAMOND, Inches(FC-0.9), Inches(4.55), Inches(1.8), Inches(0.6), 'decision')
fc_text(s4, "Online\nEvent Fired?", 8)
# Row 5
s5 = fc_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(FC-1.2), Inches(5.45), Inches(2.4), Inches(0.5), 'process')
fc_text(s5, "Read queue\nfrom localStorage", 9)
# Row 6
s6 = fc_shape(slide, MSO_SHAPE.DIAMOND, Inches(FC-0.9), Inches(6.2), Inches(1.8), Inches(0.55), 'decision')
fc_text(s6, "Queue\nEmpty?", 9)
# END
s7 = fc_shape(slide, MSO_SHAPE.OVAL, Inches(FC-0.9), Inches(6.95), Inches(1.8), Inches(0.4), 'terminal')
fc_text(s7, "Sync Complete", 9)

# Arrows
fc_arrow(slide, Inches(FC), Inches(2.4), Inches(FC), Inches(2.7))
fc_arrow(slide, Inches(FC), Inches(3.3), Inches(3.9), Inches(3.6))
fc_arrow(slide, Inches(FC), Inches(3.3), Inches(9.4), Inches(3.6))
fc_arrow(slide, Inches(3.9), Inches(4.15), Inches(FC-0.9), Inches(4.55))
fc_arrow(slide, Inches(9.4), Inches(4.15), Inches(FC+0.9), Inches(4.55))
fc_arrow(slide, Inches(FC), Inches(5.15), Inches(FC), Inches(5.45))
fc_arrow(slide, Inches(FC), Inches(5.95), Inches(FC), Inches(6.2))
fc_arrow(slide, Inches(FC), Inches(6.75), Inches(FC), Inches(6.95))
# Labels
fc_label(slide, FC-1.8, 3.0, "No", RGBColor(0xC0, 0x39, 0x2B))
fc_label(slide, FC+1.0, 3.0, "Yes", RGBColor(0x27, 0xAE, 0x60))
fc_label(slide, FC-1.8, 4.75, "Yes", RGBColor(0x27, 0xAE, 0x60))
fc_label(slide, FC-1.8, 6.35, "Yes", RGBColor(0x27, 0xAE, 0x60))

# SLIDE 13: Admin Auth Flowchart
slide = new_fc_slide(prs, "Admin Authentication Flowchart", "6.3")
# Row 1
s1 = fc_shape(slide, MSO_SHAPE.OVAL, Inches(FC-1.0), Inches(1.9), Inches(2.0), Inches(0.5), 'terminal')
fc_text(s1, "Admin opens\nDashboard", 9)
# Row 2
s2 = fc_shape(slide, MSO_SHAPE.DIAMOND, Inches(FC-0.9), Inches(2.7), Inches(1.8), Inches(0.6), 'decision')
fc_text(s2, "Logged\nIn?", 10)
# Yes branch
s3y = fc_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(FC-1.2), Inches(3.6), Inches(2.4), Inches(0.5), 'process')
fc_text(s3y, "Show Dashboard\nwith Member Data", 9)
s4y = fc_shape(slide, MSO_SHAPE.OVAL, Inches(FC-0.8), Inches(4.35), Inches(1.6), Inches(0.45), 'terminal')
fc_text(s4y, "End", 9)
# No branch
s3n = fc_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(3.2), Inches(3.6), Inches(1.8), Inches(0.5), 'process')
fc_text(s3n, "Show\nLogin Modal", 9)
s4n = fc_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(3.2), Inches(4.4), Inches(1.8), Inches(0.5), 'process')
fc_text(s4n, "Enter\nCredentials", 9)
s5n = fc_shape(slide, MSO_SHAPE.DIAMOND, Inches(3.2), Inches(5.2), Inches(1.6), Inches(0.6), 'decision')
fc_text(s5n, "Valid?", 10)
s6n = fc_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(3.2), Inches(6.1), Inches(1.8), Inches(0.5), 'process')
fc_text(s6n, "Store Session\nin localStorage", 9)
s7n = fc_shape(slide, MSO_SHAPE.OVAL, Inches(3.2), Inches(6.85), Inches(1.6), Inches(0.4), 'terminal')
fc_text(s7n, "Redirect to\nDashboard", 8)

# Arrows
fc_arrow(slide, Inches(FC), Inches(2.4), Inches(FC), Inches(2.7))
fc_arrow(slide, Inches(FC), Inches(3.3), Inches(FC-1.2+0.3), Inches(3.6))
fc_arrow(slide, Inches(FC), Inches(3.3), Inches(3.2+1.8-0.3), Inches(3.6))
fc_arrow(slide, Inches(FC), Inches(4.1), Inches(FC), Inches(4.35))
fc_arrow(slide, Inches(4.1), Inches(4.1), Inches(4.1), Inches(4.4))
fc_arrow(slide, Inches(4.1), Inches(4.9), Inches(3.2+0.8), Inches(5.2))
fc_arrow(slide, Inches(3.2+0.8), Inches(5.8), Inches(3.2+0.8), Inches(6.1))
fc_arrow(slide, Inches(4.1), Inches(6.6), Inches(4.0), Inches(6.85))
# No loop
fc_arrow(slide, Inches(3.2-0.5), Inches(5.2), Inches(2.2), Inches(4.7))
# Labels
fc_label(slide, FC+0.8, 3.05, "No", RGBColor(0xC0, 0x39, 0x2B))
fc_label(slide, FC-1.5, 3.1, "Yes", RGBColor(0x27, 0xAE, 0x60))
fc_label(slide, 2.7, 5.4, "No", RGBColor(0xC0, 0x39, 0x2B))
fc_label(slide, 3.8, 5.4, "Yes", RGBColor(0x27, 0xAE, 0x60))

# SLIDE 14: Conclusion
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide, WHITE)
add_shape(slide, Inches(0), Inches(0), Inches(13.333), Inches(1.2), DARK_BLUE)
add_text_box(slide, Inches(0.8), Inches(0.25), Inches(11), Inches(0.8),
             "Conclusion", 36, WHITE, True)
add_shape(slide, Inches(0.8), Inches(1.6), Inches(0.08), Inches(0.6), GOLD)
conclusion_text = (
    "The Church Registration System successfully addresses the challenges faced by Grace of Jesus "
    "Christ Ministries in managing member data and church operations. By transitioning from a "
    "manual, paper-based system to a modern digital solution, the church now benefits from:\n\n"
    "• Streamlined registration process accessible online\n"
    "• Centralized, secure database with real-time access\n"
    "• Automated communication through WhatsApp integration\n"
    "• Comprehensive admin dashboard for data management and analytics\n"
    "• Offline support ensuring no data is lost during connectivity issues\n\n"
    "This system positions the church for sustainable growth and improved member engagement while "
    "reducing administrative overhead and minimizing data loss risks."
)
add_text_box(slide, Inches(1.2), Inches(2.4), Inches(10.5), Inches(4.5),
             conclusion_text, 18, DARK_GRAY, False, PP_ALIGN.LEFT)

# SLIDE 15: Future Work
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide, WHITE)
add_shape(slide, Inches(0), Inches(0), Inches(13.333), Inches(1.2), DARK_BLUE)
add_text_box(slide, Inches(0.8), Inches(0.25), Inches(11), Inches(0.8),
             "Future Work", 36, WHITE, True)
add_shape(slide, Inches(0.8), Inches(1.6), Inches(0.08), Inches(0.6), GOLD)
items = [
    "• Mobile App Development – Native Android/iOS applications for easier access",
    "• SMS Integration – Alternative messaging for users without WhatsApp",
    "• Advanced Analytics – Predictive insights on church growth and attendance patterns",
    "• Online Giving Module – Secure payment gateway for tithes and offerings",
    "• Live Streaming Integration – Embedded YouTube/Facebook live services",
    "• Multi-Language Support – English, Luganda, and other local languages",
    "• Event Ticketing – QR code-based check-in for special church events",
    "• Volunteer Management – Module for tracking and scheduling church volunteers",
    "• AI Chatbot – Automated responses to common visitor inquiries"
]
add_bullet_list(slide, Inches(1.2), Inches(2.4), Inches(10.5), Inches(4.5), items, 18, DARK_GRAY, Pt(12))

# Save
output_path = os.path.join(os.path.dirname(__file__), "Church_Registration_Presentation.pptx")
prs.save(output_path)
print(f"Presentation saved to: {output_path}")
