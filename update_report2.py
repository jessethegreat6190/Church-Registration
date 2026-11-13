from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import os

doc = Document('C:\\xampp\\htdocs\\churchregistration\\DIT_Project_Report_Full.docx')
SHOTS = 'C:\\xampp\\htdocs\\churchregistration\\report_screenshots'

def replace_all(doc, old, new):
    for p in doc.paragraphs:
        for run in p.runs:
            if old in run.text:
                run.text = run.text.replace(old, new)

# 1. Update cover page
replace_all(doc, '[Student Name]', 'Jondu Jesse')
replace_all(doc, '[Registration Number]', '012240240')
replace_all(doc, '[Supervisor Name]', 'Mr. [Supervisor Name]')
replace_all(doc, '[Month, Year]', 'May, 2026')
replace_all(doc, '[2025/2026]', '2025/2026')

# 2. Survey data update
replace_all(doc, 'rated 4.5/5', 'rated 4.6/5')
replace_all(doc, 'rated 4.8/5', 'rated 4.7/5')
replace_all(doc, 'rated 4.2/5', 'rated 4.3/5')

# 3. Find heading paragraphs and insert diagrams after them
insertions = [
    ('4.1 Data Flow Diagrams', 'dfd-context.png', 'Figure 4.1: Context Level DFD (Level 0)'),
    ('Data Flow Diagrams', 'dfd-context.png', 'Figure 4.1: Context Level DFD (Level 0)'),
    ('offline', 'flowchart-offline.png', 'Figure 6.2: Offline Sync Flowchart'),
]

# Manual approach: find specific paragraphs and add images
diagrams = [
    # (search text, image file, caption, insert_after_this_text)
    ('1.1 Background Context', 'dfd-context.png', 'Figure 4.1: Context Level DFD (Level 0)'),
    ('1.3 Background Context', 'dfd-context.png', 'Figure 4.1: Context Level DFD (Level 0)'),
    ('Registration Process', 'dfd-registration.png', 'Figure 4.2: Level 1 DFD – Registration Process'),
    ('Admin Management', 'dfd-admin.png', 'Figure 4.3: Level 1 DFD – Admin Management'),
    ('Entity Relationship', 'er-diagram.png', 'Figure 4.4: Entity Relationship Diagram'),
    ('4.3 Structure Charts', 'structure-chart.png', 'Figure 4.5: System Structure Chart'),
    ('6.1 Registration Module', 'flowchart-registration.png', 'Figure 6.1: Registration Process Flowchart'),
    ('6.3 Offline Sync', 'flowchart-offline.png', 'Figure 6.2: Offline Sync Flowchart'),
    ('Admin Authentication', 'flowchart-auth.png', 'Figure 6.3: Admin Authentication Flowchart'),
]

for para in doc.paragraphs:
    text = para.text.strip()
    
    # Insert diagrams at the end of relevant sections
    if text.startswith('4.1.1') or text.startswith('Context Level'):
        img = os.path.join(SHOTS, 'dfd-context.png')
        if os.path.exists(img):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run()
            r.add_picture(img, width=Inches(5.8))
            cap = doc.add_paragraph()
            cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            cr = cap.add_run('Figure 4.1: Context Level DFD (Level 0)')
            cr.font.size = Pt(10)
            cr.font.italic = True
            
    elif text.startswith('4.1.2') or text.startswith('Level 1 DFD – Registration'):
        img = os.path.join(SHOTS, 'dfd-registration.png')
        if os.path.exists(img):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run()
            r.add_picture(img, width=Inches(5.8))
            cap = doc.add_paragraph()
            cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            cr = cap.add_run('Figure 4.2: Level 1 DFD – Registration Process')
            cr.font.size = Pt(10)
            cr.font.italic = True
            
    elif text.startswith('4.1.3') or text.startswith('Level 1 DFD – Admin'):
        img = os.path.join(SHOTS, 'dfd-admin.png')
        if os.path.exists(img):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run()
            r.add_picture(img, width=Inches(5.8))
            cap = doc.add_paragraph()
            cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            cr = cap.add_run('Figure 4.3: Level 1 DFD – Admin Management')
            cr.font.size = Pt(10)
            cr.font.italic = True
            
    elif text.startswith('4.2 Entity') or text.startswith('Entity Relationship'):
        img = os.path.join(SHOTS, 'er-diagram.png')
        if os.path.exists(img):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run()
            r.add_picture(img, width=Inches(5.8))
            cap = doc.add_paragraph()
            cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            cr = cap.add_run('Figure 4.4: Entity Relationship Diagram')
            cr.font.size = Pt(10)
            cr.font.italic = True
            
    elif text.startswith('4.3 Structure') or 'hierarchical' in text.lower():
        img = os.path.join(SHOTS, 'structure-chart.png')
        if os.path.exists(img):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run()
            r.add_picture(img, width=Inches(5.8))
            cap = doc.add_paragraph()
            cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            cr = cap.add_run('Figure 4.5: System Structure Chart')
            cr.font.size = Pt(10)
            cr.font.italic = True
            
    elif text.startswith('6.5 Flowcharts') or text == '6.5 Flowcharts':
        # Insert all flowcharts
        for img_file, cap_text in [
            ('flowchart-registration.png', 'Figure 6.1: Registration Process Flowchart'),
            ('flowchart-offline.png', 'Figure 6.2: Offline Sync Flowchart'),
            ('flowchart-auth.png', 'Figure 6.3: Admin Authentication Flowchart'),
        ]:
            img = os.path.join(SHOTS, img_file)
            if os.path.exists(img):
                doc.add_paragraph('')
                p = doc.add_paragraph()
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                r = p.add_run()
                r.add_picture(img, width=Inches(5.5))
                cap = doc.add_paragraph()
                cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
                cr = cap.add_run(cap_text)
                cr.font.size = Pt(10)
                cr.font.italic = True

output = 'C:\\xampp\\htdocs\\churchregistration\\DIT_Project_Report_Full.docx'
doc.save(output)
print(f"Final report saved: {output}")
print("Diagrams inserted after matching section headings")
