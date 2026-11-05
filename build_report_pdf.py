import fitz
import os
import shutil

primary_path = r"c:\Users\tsapa\Desktop\toc\Password_Complexity_Validator_Report.pdf"
v2_path = r"c:\Users\tsapa\Desktop\toc\Password_Complexity_Validator_Report_v2.pdf"
final_path = r"c:\Users\tsapa\Desktop\toc\Password_Complexity_Validator_Report_Print_Ready.pdf"
temp_path = r"c:\Users\tsapa\Desktop\toc\temp_report_build.pdf"
screenshots_dir = r"c:\Users\tsapa\Desktop\toc\docs\screenshots"

doc = fitz.open()

# A4 Dimensions in points: 595.32 x 841.92
PAGE_WIDTH = 595.32
PAGE_HEIGHT = 841.92
BORDER_MARGIN = 24.0
MARGIN_LEFT = 36.0
MARGIN_RIGHT = 36.0
USABLE_WIDTH = PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT # 523.32 pt

BORDER_RECT = fitz.Rect(BORDER_MARGIN, BORDER_MARGIN, PAGE_WIDTH - BORDER_MARGIN, PAGE_HEIGHT - BORDER_MARGIN)

FONT_TITLE = "helv"
FONT_BOLD = "hebo"

def draw_heading_with_underline(page, text, x, y, fontsize=13.0):
    page.insert_text((x, y), text, fontname=FONT_BOLD, fontsize=fontsize)
    text_w = fitz.get_text_length(text, fontname=FONT_BOLD, fontsize=fontsize)
    # Draw underline line
    page.draw_line(fitz.Point(x, y + 2.5), fitz.Point(x + text_w, y + 2.5), color=(0, 0, 0), width=0.75)
    return text_w

# ==========================================
# PAGE 1: TEXT REPORT
# ==========================================
page1 = doc.new_page(width=PAGE_WIDTH, height=PAGE_HEIGHT)
# Draw Page Border
page1.draw_rect(BORDER_RECT, color=(0, 0, 0), width=1.0)

cursor_y = 48.0

# Title
draw_heading_with_underline(page1, "TITLE OF THE PROJECT :", MARGIN_LEFT, cursor_y, fontsize=13.0)
cursor_y += 24.0

page1.insert_text((MARGIN_LEFT + 20.0, cursor_y), "PASSWORD COMPLEXITY VALIDATOR USING FINITE AUTOMATA AND NLP", fontname=FONT_BOLD, fontsize=12.0)
cursor_y += 28.0

# Teammates Heading
draw_heading_with_underline(page1, "Teammates:", MARGIN_LEFT, cursor_y, fontsize=13.0)
cursor_y += 18.0

teammates = [
    "25EU04918 - Tsapala Jaya Surya Jitendra",
    "24EU04210 - Chanumolu Megha Surya",
    "24EU04226 - Kata Bhavani Prasad"
]
for tm in teammates:
    page1.insert_text((MARGIN_LEFT, cursor_y), tm, fontname=FONT_TITLE, fontsize=11.5)
    cursor_y += 17.0

cursor_y += 12.0

# Project Description Heading
draw_heading_with_underline(page1, "Project Description:", MARGIN_LEFT, cursor_y, fontsize=13.0)
cursor_y += 10.0

desc_paragraphs = [
    "Our project is a Password Complexity Validator that helps users evaluate and verify the strength and compliance "
    "of passwords based on strict character complexity and length requirements. It uses Natural Language Processing (NLP) "
    "lexical scanning techniques to parse input text, classify characters into alphabet equivalence classes (uppercase letters, "
    "lowercase letters, numeric digits, and special characters), and verify that the string meets a minimum length requirement of at least 8 characters.",

    "Automata Theory concepts, especially Deterministic Finite Automata (DFA) and Regular Languages, form the mathematical "
    "architecture of this project. Instead of vulnerable backtracking regular expression engines that are prone to ReDoS (Regular "
    "Expression Denial of Service) attacks, our project models password validation as a Product Automaton with 16 character-complexity "
    "states (a 4-bit Boolean hypercube) and 9 length-tracking states (totaling 144 product states). The language is formally proven "
    "to be a Chomsky Type-3 Regular Language through the closure of regular languages under finite intersection. We developed the "
    "project using Python for the backend automata state engine, and HTML5, CSS3, and JavaScript for the responsive interactive user interface.",

    "Users can enter passwords, observe real-time state transitions through the 16-state lattice, inspect active 4-bit register LED status "
    "indicators, and trace transitions step-by-step. The tool also displays useful cryptographic metrics such as Shannon entropy, "
    "estimated brute-force resistance time, alphabet pool size, a complete 16-state transition matrix table, and an automated verification test runner.",

    "The main aim of this project is to eliminate ReDoS vulnerabilities, guarantee deterministic O(n) linear-time execution with O(1) "
    "memory complexity, and provide students and faculty with an intuitive visual demonstration of formal language theory applied to modern cyber security."
]

for p in desc_paragraphs:
    # 520pt width wraps cleanly well before right border
    rect = fitz.Rect(MARGIN_LEFT, cursor_y, MARGIN_LEFT + USABLE_WIDTH, cursor_y + 120.0)
    # Line spacing 1.25, font 10pt
    rc = page1.insert_textbox(rect, p, fontname=FONT_TITLE, fontsize=10.0, lineheight=1.25)
    # Estimate height consumed
    num_lines = (len(p) // 95) + 1
    cursor_y += (num_lines * 12.5) + 6.0

cursor_y += 6.0

# Project Outputs Heading
draw_heading_with_underline(page1, "Project Outputs", MARGIN_LEFT, cursor_y, fontsize=13.0)
cursor_y += 18.0

outputs = [
    ("1. DFA State Tracking: ", "Displays real-time state transitions (q_bits, L_k) as symbols are scanned."),
    ("2. 4-Bit Register: ", "Shows live binary bitmask values for Upper, Lower, Digit, and Special classes."),
    ("3. 16-State Lattice: ", "5-tier graphical state machine featuring active LED status indicators."),
    ("4. Step Debugger: ", "Allows users to step forward and backward symbol-by-symbol through delta transitions."),
    ("5. Acceptance Status: ", "Validates language membership, reaching accepting state q1111 (length >= 8)."),
    ("6. Transition Matrix: ", "Complete formal delta transition table with active row highlighting and search."),
    ("7. Shannon Entropy: ", "Displays password entropy (in bits), alphabet pool size, and crack resistance time."),
    ("8. Trace Table & JSON: ", "Full sequential execution trace log table with one-click JSON export."),
    ("9. Automated Test Suite: ", "10-case verification test suite testing boundary conditions with 100% accuracy.")
]

for bold_prefix, desc_text in outputs:
    page1.insert_text((MARGIN_LEFT + 14.0, cursor_y), bold_prefix, fontname=FONT_BOLD, fontsize=10.0)
    prefix_w = fitz.get_text_length(bold_prefix, fontname=FONT_BOLD, fontsize=10.0)
    page1.insert_text((MARGIN_LEFT + 14.0 + prefix_w, cursor_y), desc_text, fontname=FONT_TITLE, fontsize=10.0)
    cursor_y += 16.0

# ==========================================
# PAGE 2: SCREENSHOTS 1 & 2
# ==========================================
page2 = doc.new_page(width=PAGE_WIDTH, height=PAGE_HEIGHT)
# Draw Page Border
page2.draw_rect(BORDER_RECT, color=(0, 0, 0), width=1.0)

img1_path = os.path.join(screenshots_dir, "screenshot1_simulator.png")
img2_path = os.path.join(screenshots_dir, "screenshot2_table.png")

rect_img1 = fitz.Rect(MARGIN_LEFT, 36.0, MARGIN_LEFT + USABLE_WIDTH, 36.0 + 345.0)
rect_img2 = fitz.Rect(MARGIN_LEFT, 408.0, MARGIN_LEFT + USABLE_WIDTH, 408.0 + 345.0)

if os.path.exists(img1_path):
    page2.insert_image(rect_img1, filename=img1_path)
    # Draw neat thin border around image
    page2.draw_rect(rect_img1, color=(0.2, 0.2, 0.2), width=0.5)

if os.path.exists(img2_path):
    page2.insert_image(rect_img2, filename=img2_path)
    page2.draw_rect(rect_img2, color=(0.2, 0.2, 0.2), width=0.5)

# ==========================================
# PAGE 3: SCREENSHOT 3 & SPECIFICATIONS
# ==========================================
page3 = doc.new_page(width=PAGE_WIDTH, height=PAGE_HEIGHT)
# Draw Page Border
page3.draw_rect(BORDER_RECT, color=(0, 0, 0), width=1.0)

img3_path = os.path.join(screenshots_dir, "screenshot3_testsuite.png")
rect_img3 = fitz.Rect(MARGIN_LEFT, 36.0, MARGIN_LEFT + USABLE_WIDTH, 36.0 + 345.0)

if os.path.exists(img3_path):
    page3.insert_image(rect_img3, filename=img3_path)
    page3.draw_rect(rect_img3, color=(0.2, 0.2, 0.2), width=0.5)

draw_heading_with_underline(page3, "Project Implementation & Verification Summary:", MARGIN_LEFT, 415.0, fontsize=12.5)

summary_p = (
    "The project was verified against all standard positive and negative test cases. The test suite results shown above "
    "demonstrate that the Deterministic Finite Automaton accurately identifies valid language members (satisfying all four character "
    "classes and length >= 8) while rejecting all strings with missing components or insufficient length with 100% precision.\n\n"
    "- Formal DFA 5-Tuple: M = (Q, Sigma, delta, q0, F)\n"
    "- Total Product States: 144 states (16 complexity states x 9 length states)\n"
    "- Time Complexity: O(n) strictly linear time (guaranteed zero backtracking)\n"
    "- Space Complexity: O(1) auxiliary space (4-bit bitmask register)\n"
    "- GitHub Repository: https://github.com/Jitendra2007/password-complexity-automata"
)

rect_sum = fitz.Rect(MARGIN_LEFT, 430.0, MARGIN_LEFT + USABLE_WIDTH, 680.0)
page3.insert_textbox(rect_sum, summary_p, fontname=FONT_TITLE, fontsize=10.0, lineheight=1.35)

# Save to temp path first
doc.save(temp_path)
doc.close()

# Save to all paths that are unlocked
shutil.copyfile(temp_path, final_path)
print(f"Generated: {final_path}")

try:
    shutil.copyfile(temp_path, v2_path)
    print(f"Updated: {v2_path}")
except Exception as e:
    print(f"v2 locked: {e}")

try:
    shutil.copyfile(temp_path, primary_path)
    print(f"Updated: {primary_path}")
except Exception as e:
    print(f"Primary locked by viewer: {e}")

if os.path.exists(temp_path):
    os.remove(temp_path)
