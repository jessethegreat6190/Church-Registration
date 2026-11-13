import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle
import matplotlib.patches as mpatches
import os

OUT_DIR = 'C:\\xampp\\htdocs\\churchregistration\\report_screenshots'

def setup_fig(title=None):
    fig, ax = plt.subplots(1, 1, figsize=(10, 7))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.axis('off')
    if title:
        ax.set_title(title, fontsize=16, fontweight='bold', pad=15)
    return fig, ax

def add_box(ax, x, y, w, h, text, color='#d4e6f1', edge='#2c3e50', fontsize=10):
    box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1", facecolor=color, edgecolor=edge, linewidth=2)
    ax.add_patch(box)
    ax.text(x + w/2, y + h/2, text, ha='center', va='center', fontsize=fontsize, fontweight='bold', color='#2c3e50')

def add_arrow(ax, x1, y1, x2, y2, label=''):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', lw=1.5, color='#2c3e50'))
    if label:
        mx, my = (x1+x2)/2, (y1+y2)/2
        ax.text(mx, my+0.15, label, ha='center', va='bottom', fontsize=8, color='#555')

def add_external(ax, x, y, text, fontsize=10):
    ax.text(x, y, text, ha='center', va='center', fontsize=fontsize,
            fontweight='bold', color='#2c3e50',
            bbox=dict(boxstyle='square,pad=0.3', facecolor='#f9e79f', edgecolor='#2c3e50', linewidth=2))

def add_process(ax, x, y, text, fontsize=9):
    ax.text(x, y, text, ha='center', va='center', fontsize=fontsize,
            fontweight='bold', color='#2c3e50',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#d4e6f1', edgecolor='#2c3e50', linewidth=2))

def add_data_store(ax, x, y, text, fontsize=9):
    # Cylinder-like for data store
    rect = mpatches.FancyBboxPatch((x-0.8, y-0.3), 1.6, 0.6, boxstyle="round,pad=0.05",
                                    facecolor='#d5f5e3', edgecolor='#2c3e50', linewidth=2)
    ax.add_patch(rect)
    ax.text(x, y, text, ha='center', va='center', fontsize=fontsize,
            fontweight='bold', color='#2c3e50')

# ═══ 1. CONTEXT LEVEL DFD ═══
fig, ax = setup_fig('Figure 4.1: Context Level DFD (Level 0)')

# System in center
add_box(ax, 3.5, 2.5, 3, 2, 'Church\nManagement\nSystem', '#d4e6f1', '#2c3e50', 12)

# External entities
add_external(ax, 8.5, 5.5, 'Church Visitor\n(Registrant)')
add_external(ax, 1.5, 5.5, 'Admin\n(Church Leadership)')
add_external(ax, 8.5, 1.5, 'WhatsApp API')
add_external(ax, 1.5, 1.5, 'Google Sheets')

# Flow labels
add_arrow(ax, 6.5, 4.5, 8.5, 5.3, 'Registration data')
add_arrow(ax, 8.5, 5.7, 6.5, 4.5, 'Confirmation')
add_arrow(ax, 1.5, 5.3, 3.5, 4.5, 'Admin credentials')
add_arrow(ax, 3.5, 4.5, 1.5, 5.3, 'Member data')
add_arrow(ax, 6.5, 3.5, 8.5, 1.7, 'WhatsApp msg')
add_arrow(ax, 3.5, 2.5, 1.5, 1.7, 'Backup data')
add_arrow(ax, 1.5, 1.3, 3.5, 2.5, 'Confirm')

# Firebase external entity at top
add_external(ax, 5, 6.5, 'Firebase\nFirestore')

add_arrow(ax, 5, 4.5, 5, 6.2, 'Save/Read')

plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, 'dfd-context.png'), dpi=150, bbox_inches='tight')
plt.close()
print("1. DFD Context Level done")

# ═══ 2. LEVEL 1 DFD – REGISTRATION ═══
fig, ax = setup_fig('Figure 4.2: Level 1 DFD – Registration Process')

add_external(ax, 1.5, 6.5, 'Church Visitor')
add_external(ax, 8.5, 6.5, 'WhatsApp')

add_process(ax, 3.5, 5, '1.1 Collect\nPersonal Info', 8)
add_process(ax, 6.5, 5, '1.2 Validate\nForm Data', 8)
add_process(ax, 3.5, 3, '1.3 Save to\nFirestore', 8)
add_process(ax, 6.5, 3, '1.4 Send\nWhatsApp', 8)

add_data_store(ax, 2, 1.5, 'Firestore DB')
add_data_store(ax, 5, 1.5, 'Google Sheets')
add_data_store(ax, 8, 1.5, 'localStorage\n(Offline)')

add_arrow(ax, 1.5, 6.2, 3.5, 5.3, 'Personal data')
add_arrow(ax, 3.5, 4.7, 6.5, 5.3, 'Validated data')
add_arrow(ax, 6.5, 4.7, 3.5, 3.3, 'Passed')
add_arrow(ax, 6.5, 4.7, 6.5, 3.3, 'Failed')
add_arrow(ax, 3.5, 2.7, 2, 1.8, 'Write')
add_arrow(ax, 3.5, 2.7, 5, 1.8, 'Backup')
add_arrow(ax, 6.5, 2.7, 8, 1.8, 'Queue')
add_arrow(ax, 6.5, 2.7, 8.5, 3.3, 'Confirm msg')

ax.text(6.5, 4.3, '(redirect)', ha='center', fontsize=7, color='#999')

plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, 'dfd-registration.png'), dpi=150, bbox_inches='tight')
plt.close()
print("2. DFD Registration done")

# ═══ 3. LEVEL 1 DFD – ADMIN ═══
fig, ax = setup_fig('Figure 4.3: Level 1 DFD – Admin Management')

add_external(ax, 1.5, 6.5, 'Administrator')
add_external(ax, 8.5, 6.5, 'Firebase\nAuth')

add_process(ax, 3.5, 5, '2.1 Authenticate\nAdmin', 8)
add_process(ax, 6.5, 5, '2.2 Fetch\nMember Data', 8)
add_process(ax, 3.5, 3, '2.3 Display\nDashboard', 8)
add_process(ax, 6.5, 3, '2.4 Manage\nRecords', 8)

add_data_store(ax, 5, 1.5, 'Firestore DB')

add_arrow(ax, 1.5, 6.2, 3.5, 5.3, 'Credentials')
add_arrow(ax, 3.5, 4.7, 6.5, 5.3, 'Session token')
add_arrow(ax, 6.5, 4.7, 3.5, 3.3, 'Member data')
add_arrow(ax, 3.5, 2.7, 5, 1.8, 'Read')
add_arrow(ax, 6.5, 4.7, 8.5, 6.2, 'Verify')
add_arrow(ax, 9, 6.2, 9, 5, 'OK/')
add_arrow(ax, 6.5, 2.7, 5, 1.8, 'Write')
add_arrow(ax, 3, 5.3, 1.5, 5.8, 'Login')
add_arrow(ax, 1.5, 5.8, 3, 5.3, '')

plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, 'dfd-admin.png'), dpi=150, bbox_inches='tight')
plt.close()
print("3. DFD Admin done")

# ═══ 4. ENTITY RELATIONSHIP DIAGRAM ═══
fig, ax = setup_fig('Figure 4.4: Entity Relationship Diagram')

# Entities (rectangles)
def draw_entity(ax, x, y, name, attrs, color='#d4e6f1'):
    rect = FancyBboxPatch((x-1.5, y-0.8), 3, 1.6, boxstyle="round,pad=0.1", facecolor=color, edgecolor='#2c3e50', linewidth=2)
    ax.add_patch(rect)
    ax.text(x, y+0.3, name, ha='center', va='center', fontsize=11, fontweight='bold', color='#2c3e50')
    ax.text(x, y-0.3, '\n'.join(attrs), ha='center', va='center', fontsize=7, color='#555')

draw_entity(ax, 2, 5, 'REGISTRANT', ['name (PK)', 'phone', 'location', 'regType', 'birthDay', 'birthMonth', 'timestamp'])
draw_entity(ax, 8, 5, 'REGISTRATION', ['regType (PK)', 'eventData', 'volunteering', 'consent', 'referredBy', 'status'])
draw_entity(ax, 2, 2, 'ADMIN', ['email (PK)', 'role', 'lastLogin'])
draw_entity(ax, 8, 2, 'CHURCH\nPROGRAM', ['title', 'date', 'time', 'description', 'icon'])

# Relationships
add_arrow(ax, 3.5, 5.5, 6.5, 5.5, 'has')
add_arrow(ax, 3.5, 3.5, 3.5, 2.5, 'manages')
add_arrow(ax, 8, 4, 8, 3.2, 'schedules')

ax.text(5, 5.8, '1', ha='center', fontsize=9, fontweight='bold')
ax.text(6.8, 5.8, '*', ha='center', fontsize=9, fontweight='bold')
ax.text(3, 3.8, '1', ha='center', fontsize=9, fontweight='bold')
ax.text(3, 2.2, '*', ha='center', fontsize=9, fontweight='bold')
ax.text(8.5, 3.6, '1', ha='center', fontsize=9, fontweight='bold')
ax.text(8.5, 3, '*', ha='center', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, 'er-diagram.png'), dpi=150, bbox_inches='tight')
plt.close()
print("4. ER Diagram done")

# ════════════════════════════════════════════
# PROPER FLOWCHART SYMBOLS
#   Oval = Start / End (terminator)
#   Rectangle = Process  
#   Diamond = Decision
#   Parallelogram = Data I/O
# ════════════════════════════════════════════

def terminal(ax, x, y, w, h, text):
    """Oval start/end symbol"""
    ellipse = mpatches.Ellipse((x, y), w, h, facecolor='#aed6f1', edgecolor='#2c3e50', linewidth=2)
    ax.add_patch(ellipse)
    ax.text(x, y, text, ha='center', va='center', fontsize=8, fontweight='bold', color='#2c3e50')

def proc(ax, x, y, w, h, text):
    """Rectangle process symbol"""
    rect = FancyBboxPatch((x-w/2, y-h/2), w, h, boxstyle="round,pad=0.05",
                          facecolor='#d4e6f1', edgecolor='#2c3e50', linewidth=2)
    ax.add_patch(rect)
    ax.text(x, y, text, ha='center', va='center', fontsize=8, fontweight='bold', color='#2c3e50')

def decis(ax, x, y, w, h, text):
    """Diamond decision symbol"""
    d = mpatches.Polygon([
        [x, y+h/2], [x+w/2, y], [x, y-h/2], [x-w/2, y]
    ], closed=True, facecolor='#f9e79f', edgecolor='#2c3e50', linewidth=2)
    ax.add_patch(d)
    ax.text(x, y, text, ha='center', va='center', fontsize=8, fontweight='bold', color='#2c3e50')

def arr(ax, x1, y1, x2, y2, label=''):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', lw=1.8, color='#2c3e50'))
    if label:
        mx, my = (x1+x2)/2, (y1+y2)/2
        ax.text(mx+0.15, my, label, fontsize=8, color='#c0392b' if label=='No' else '#27ae60',
                fontweight='bold')

# ═══ 5. FLOWCHART – REGISTRATION ═══
fig, ax = setup_fig('Figure 6.1: Registration Process Flowchart')

SW, SH = 1.8, 0.5  # standard process width/height
DW, DH = 1.6, 0.7  # decision width/height
TW, TH = 1.4, 0.6  # terminal width/height

terminal(ax, 5, 6.2, TW, TH, 'START')

proc(ax, 5, 5.1, SW, SH, 'Fill Step 1:\nName, Phone, Location')

decis(ax, 5, 4.0, DW, DH, 'Valid?')

arr(ax, 5, 5.9, 5, 5.5)
arr(ax, 5, 4.8, 5, 4.45, 'Yes')
arr(ax, 5, 3.55, 5, 2.65, 'Yes')
arr(ax, 3, 4.3, 5, 4.1, 'No')
arr(ax, 3, 3.4, 3, 2.9)

# Invalid branch
proc(ax, 3, 3.75, SW, SH, 'Show inline\nerrors')
arr(ax, 4.2, 4.0, 3.9, 3.75, 'No')

# Step 2
decis(ax, 5, 2.65, DW, DH, 'First\nTime?')
proc(ax, 3, 2.2, SW, SH, 'Fill Step 2:\nPreferences')
proc(ax, 7, 2.2, SW, SH, 'Review Step 3:\nConfirm')
arr(ax, 5, 2.3, 3, 2.5, 'Yes')
arr(ax, 5, 2.3, 7, 2.5, 'No')
arr(ax, 3, 1.9, 3, 1.4)
arr(ax, 7, 1.9, 7, 1.4)

# Final save
proc(ax, 5, 1.4, SW+0.2, SH+0.1, 'Save to Firestore\n+ Google Sheets')
proc(ax, 5, 0.65, SW, SH, 'Open WhatsApp\nConfirmation')
terminal(ax, 5, 0, TW, TH, 'END')

arr(ax, 3, 1.4, 5, 1.7)
arr(ax, 7, 1.4, 5, 1.7)
arr(ax, 5, 1.1, 5, 0.9)
arr(ax, 5, 0.4, 5, 0.3)

plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, 'flowchart-registration.png'), dpi=150, bbox_inches='tight')
plt.close()
print("5. Registration Flowchart done")

# ═══ 6. FLOWCHART – OFFLINE SYNC ═══
fig, ax = setup_fig('Figure 6.2: Offline Sync Flowchart')

SW, SH = 1.8, 0.5
DW, DH = 1.8, 0.7
TW, TH = 1.6, 0.6

terminal(ax, 5, 6.2, TW, TH, 'User submits\nregistration')

decis(ax, 5, 5.1, DW, DH, 'Internet\nAvailable?')

proc(ax, 2.5, 4.1, SW, SH, 'Save to\nlocalStorage\nQueue')
proc(ax, 7.5, 4.1, SW, SH, 'Save to\nFirestore\n+ Google Sheets')

decis(ax, 5, 3.0, DW, DH, 'Online\nEvent\nFired?')

proc(ax, 5, 2.0, SW, SH, 'Read queue\nfrom localStorage')

decis(ax, 5, 1.1, DW, DH, 'Queue\nEmpty?')

terminal(ax, 5, 0.2, TW, TH, 'Sync\nComplete')

arr(ax, 5, 5.9, 5, 5.55)
arr(ax, 5, 4.65, 2.5, 4.4, 'No')
arr(ax, 5, 4.65, 7.5, 4.4, 'Yes')
arr(ax, 2.5, 3.8, 5, 3.35, 'Wait')
arr(ax, 7.5, 3.8, 5, 3.35, '')
arr(ax, 5, 2.65, 5, 2.3, 'Yes')
arr(ax, 5, 1.75, 5, 1.45, 'No')
arr(ax, 5, 0.75, 5, 0.5, 'Yes')

ax.annotate('Auto-sync\nloop', xy=(6.5, 2.7), fontsize=7, color='#7f8c8d', ha='center',
            style='italic')
ax.plot([5.9, 6.5, 6.5, 5.9], [2.65, 2.65, 3.35, 3.35], '--', color='#7f8c8d', lw=1)

plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, 'flowchart-offline.png'), dpi=150, bbox_inches='tight')
plt.close()
print("6. Offline Sync Flowchart done")

# ═══ 7. FLOWCHART – ADMIN AUTH ═══
fig, ax = setup_fig('Figure 6.3: Admin Authentication Flowchart')

SW, SH = 1.8, 0.5
DW, DH = 1.6, 0.7
TW, TH = 1.4, 0.6

terminal(ax, 5, 6.5, TW, TH, 'Admin opens\nDashboard')

decis(ax, 5, 5.4, DW, DH, 'Logged\nIn?')

proc(ax, 5, 4.3, SW, SH, 'Show Dashboard\nwith Member Data')
terminal(ax, 5, 3.4, TW, TH, 'End')

proc(ax, 2, 4.3, SW, SH, 'Show\nLogin Modal')
proc(ax, 2, 3.3, SW, SH, 'Enter\nCredentials')
decis(ax, 2, 2.3, DW, DH, 'Valid?')
proc(ax, 2, 1.3, SW, SH, 'Store Session\nin localStorage')
terminal(ax, 2, 0.4, TW, TH, 'Redirect to\nDashboard')

arr(ax, 5, 6.2, 5, 5.85)
arr(ax, 5, 5.0, 5, 4.6, 'Yes')
arr(ax, 5, 4.0, 5, 3.7)
arr(ax, 5, 5.0, 2, 4.6, 'No')
arr(ax, 2, 4.0, 2, 3.6)
arr(ax, 2, 3.0, 2, 2.65, 'Submit')
arr(ax, 2, 1.95, 2, 1.6, 'Yes')
arr(ax, 2, 1.0, 2, 0.7)
arr(ax, 2.8, 2.3, 4.2, 3.3, 'No')

plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, 'flowchart-auth.png'), dpi=150, bbox_inches='tight')
plt.close()
print("7. Auth Flowchart done")

# ═══ 8. STRUCTURE CHART ═══
fig, ax = setup_fig('Figure 4.5: System Structure Chart')

def module_box(ax, x, y, text, w=2.5, h=0.6, color='#d4e6f1'):
    rect = FancyBboxPatch((x-w/2, y-h/2), w, h, boxstyle="round,pad=0.05",
                           facecolor=color, edgecolor='#2c3e50', linewidth=1.5)
    ax.add_patch(rect)
    ax.text(x, y, text, ha='center', va='center', fontsize=8, fontweight='bold', color='#2c3e50')

# Top level
module_box(ax, 5, 6.2, 'CHURCH MANAGEMENT SYSTEM', 4, 0.7, '#2c3e50')
ax.text(5, 6.2, 'CHURCH MANAGEMENT SYSTEM', ha='center', va='center', fontsize=9, fontweight='bold', color='white')

# Level 1 modules
for i, (name, x) in enumerate([('USER\nINTERFACE', 1.5), ('REGISTRATION\nHANDLER', 4), ('DATA\nMANAGER', 6.5), ('ADMIN\nDASHBOARD', 9)]):
    module_box(ax, x, 5, name, 2.2, 0.8)
    ax.plot([5, x], [5.85, 5.4], 'k-', lw=1.5)

# Level 2 sub-modules
ui_mods = [('Navbar\nHero\nAbout', 0.5), ('Registration\nForm', 1.5), ('Contact\nFooter', 2.5)]
reg_mods = [('Step\nNavigation', 3.2), ('Form\nValidation', 4), ('Data\nAssembly', 4.8)]
data_mods = [('Firestore\nService', 5.8), ('Google\nSheets', 6.5), ('Offline\nQueue', 7.2)]
admin_mods = [('Auth', 8.2), ('Member\nMgmt', 9), ('Analytics', 9.8)]

for mods, parent_x in [(ui_mods, 1.5), (reg_mods, 4), (data_mods, 6.5), (admin_mods, 9)]:
    for name, x in mods:
        module_box(ax, x, 3.8, name, 1.5, 0.6, '#ebf5fb')
        ax.plot([parent_x, x], [4.6, 4.1], 'k-', lw=1)

plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, 'structure-chart.png'), dpi=150, bbox_inches='tight')
plt.close()
print("8. Structure Chart done")

print("\nAll 8 diagrams created!")
