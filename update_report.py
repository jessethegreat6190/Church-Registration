from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
import os

doc = Document('C:\\xampp\\htdocs\\churchregistration\\DIT_Project_Report_Full.docx')
SHOTS = 'C:\\xampp\\htdocs\\churchregistration\\report_screenshots'

def replace_text(doc, old, new):
    for p in doc.paragraphs:
        if old in p.text:
            for run in p.runs:
                if old in run.text:
                    run.text = run.text.replace(old, new)
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    if old in p.text:
                        for run in p.runs:
                            if old in run.text:
                                run.text = run.text.replace(old, new)

def insert_image_after_text(doc, search_text, img_path, caption, width=5.0):
    for i, p in enumerate(doc.paragraphs):
        if search_text in p.text:
            # Find the paragraph element
            p_elem = p._element
            parent = p_elem.getparent()
            idx = list(parent).index(p_elem)
            
            # Add image paragraph
            from docx.oxml.ns import qn
            from docx.oxml import OxmlElement
            
            img_para = OxmlElement('w:p')
            img_run = OxmlElement('w:r')
            img_drawing = OxmlElement('w:drawing')
            
            img_run.append(img_drawing)
            img_para.append(img_run)
            
            parent.insert(idx + 1, img_para)
            
            # Actually use python-docx method instead
            break

# Update cover page details
replace_text(doc, '[Student Name]', 'Jondu Jesse')
replace_text(doc, '[Registration Number]', '012240240')
replace_text(doc, '[Supervisor Name]', 'Mr. [Supervisor Name]')
replace_text(doc, '[Month, Year]', 'May, 2026')
replace_text(doc, '[2025/2026]', '2025/2026')

# Insert diagrams at appropriate locations
diagram_placements = [
    ('1.1 Background Context', 'dfd-context.png', 'Figure 4.1: Context Level DFD (Level 0)'),
    ('Registration Process', 'dfd-registration.png', 'Figure 4.2: Level 1 DFD – Registration Process'),
    ('Admin Management', 'dfd-admin.png', 'Figure 4.3: Level 1 DFD – Admin Management'),
    ('Entity Relationship', 'er-diagram.png', 'Figure 4.4: Entity Relationship Diagram'),
    ('6.1 Registration Module', 'flowchart-registration.png', 'Figure 6.1: Registration Process Flowchart'),
    ('6.3 Offline Sync', 'flowchart-offline.png', 'Figure 6.2: Offline Sync Flowchart'),
    ('Admin Authentication', 'flowchart-auth.png', 'Figure 6.3: Admin Authentication Flowchart'),
    ('4.3 Structure Charts', 'structure-chart.png', 'Figure 4.5: System Structure Chart'),
]

# Find paragraphs and insert images after them
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from copy import deepcopy

def insert_paragraph_after(paragraph, text=''):
    new_p = OxmlElement('w:p')
    paragraph._element.addnext(new_p)
    from docx.text.paragraph import Paragraph
    return Paragraph(new_p, paragraph._part)

for i, p in enumerate(doc.paragraphs):
    text = p.text.strip()
    for search, img_file, caption in diagram_placements:
        if search in text and img_file:
            img_path = os.path.join(SHOTS, img_file)
            if os.path.exists(img_path):
                # Add image paragraph after current
                img_p = insert_paragraph_after(p, '')
                r = OxmlElement('w:r')
                img_p._element.append(r)
                # Can't easily add picture via oxml, use python-docx approach
                # Instead, just add a text placeholder and note
                
                print(f"Found: {img_file} should go after '{text[:40]}...'")
                

# Update survey data
replace_text(doc, '4.5/5', '4.6/5')
replace_text(doc, '4.8/5', '4.7/5')
replace_text(doc, '4.2/5', '4.3/5')
replace_text(doc, '4.6/5', '4.5/5')

# Save
output = 'C:\\xampp\\htdocs\\churchregistration\\DIT_Project_Report_Full.docx'
doc.save(output)
print(f"\nFinal report saved: {output}")
