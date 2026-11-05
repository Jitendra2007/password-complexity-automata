import fitz
import os

pdf_path = r"c:\Users\tsapa\Desktop\toc\Password_Complexity_Validator_Report.pdf"
screenshots_dir = r"c:\Users\tsapa\Desktop\toc\docs\screenshots"

doc = fitz.open()

# A4 dimensions in points: 595.32 x 841.92
PAGE_WIDTH = 595.32
PAGE_HEIGHT = 841.92
MARGIN_LEFT = 36.0
MARGIN_RIGHT = 36.0
USABLE_WIDTH = PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT # 523.32 pt

# ==========================================
# PAGE 1: TEXT REPORT
# ==========================================
page1 = doc.new_page(width=PAGE_WIDTH, height=PAGE_HEIGHT)

# In PyMuPDF, built-in standard Helvetica / Helvetica-Bold are available and match Aptos/Arial standard sizing
FONT_TITLE = "helv"
FONT_BOLD = "hebo"

cursor_y = 50.0

# Title
page1.insert_text((MARGIN_LEFT, cursor_y), "TITLE OF THE PROJECT :", fontname=FONT_BOLD, fontsize=13.0)
cursor_y += 24.0
page1.insert_text((MARGIN_LEFT + 20.0, cursor_y), "PASSWORD COMPLEXITY VALIDATOR USING FINITE AUTOMATA AND NLP", fontname=FONT_BOLD, fontsize=12.5)
cursor_y += 28.0

# Teammates
page1.insert_text((MARGIN_LEFT, cursor_y), "Teammates:", fontname=FONT_BOLD, fontsize=13.0)
cursor_y += 20.0
page1.insert_text((MARGIN_LEFT, cursor_y), "24EU04xxx – T. Jaya Surya Jitendra", fontname=FONT_TITLE, fontsize=12.0)
cursor_y += 18.0
page1.insert_text((MARGIN_LEFT, cursor_y), "24EU04xxx – [Teammate 2]", fontname=FONT_TITLE, fontsize=12.0)
cursor_y += 18.0
page1.insert_text((MARGIN_LEFT, cursor_y), "24EU04xxx – [Teammate 3]", fontname=FONT_TITLE, fontsize=12.0)
cursor_y += 28.0

# Project Description Heading
page1.insert_text((MARGIN_LEFT, cursor_y), "Project Description:", fontname=FONT_BOLD, fontsize=13.0)
cursor_y += 10.0

desc_p1 = (
    "Our project is a Password Complexity Validator that helps users evaluate and verify the strength and compliance "
    "of passwords based on strict character complexity and length requirements. It uses Natural Language Processing (NLP) "
    "lexical scanning techniques to parse input text, classify characters into alphabet equivalence classes (uppercase letters, "
    "lowercase letters, numeric digits, and special characters), and verify that the string meets a minimum length requirement of at least 8 characters."
)

desc_p2 = (
    "Automata Theory concepts, especially Deterministic Finite Automata (DFA) and Regular Languages, form the mathematical "
    "architecture of this project. Instead of vulnerable backtracking regular expression engines that are prone to ReDoS (Regular "
    "Expression Denial of Service) attacks, our project models password validation as a Product Automaton with 16 character-complexity "
    "states (a 4-bit Boolean hypercube) and 9 length-tracking states (totaling 144 product states). The language is formally proven "
    "to be a Chomsky Type-3 Regular Language through the closure of regular languages under finite intersection. We developed the "
    "project using Python for the backend automata state engine, and HTML5, CSS3, and JavaScript for the responsive interactive user interface."
)

desc_p3 = (
    "Users can enter passwords, observe real-time state transitions through the 16-state lattice, inspect active 4-bit register LED status "
    "indicators, and trace transitions step-by-step. The tool also displays useful cryptographic metrics such as Shannon entropy, "
    "estimated brute-force resistance time, alphabet pool size, a complete 16-state transition matrix table, and an automated verification test runner."
)

desc_p4 = (
    "The main aim of this project is to eliminate ReDoS vulnerabilities, guarantee deterministic O(n) linear-time execution with O(1) "
    "memory complexity, and provide students and faculty with an intuitive visual demonstration of formal language theory applied to modern cyber security."
)

for p_text in [desc_p1, desc_p2, desc_p3, desc_p4]:
    rect = fitz.Rect(MARGIN_LEFT, cursor_y, MARGIN_LEFT + USABLE_WIDTH, cursor_y + 120.0)
    # insert_textbox calculates exact height
    h = page1.insert_textbox(rect, p_text, fontname=FONT_TITLE, fontsize=10.5, lineheight=1.28)
    # The return value from insert_textbox is the remaining unused space, or we can measure lines
    # Let's approximate line height: ~13.5 pt per line
    num_lines = len(p_text) // 90 + 1
    cursor_y += num_lines * 13.6 + 6.0

cursor_y += 8.0

# Project Outputs Heading
page1.insert_text((MARGIN_LEFT, cursor_y), "Project Outputs", fontname=FONT_BOLD, fontsize=13.0)
cursor_y += 18.0

outputs = [
    ("1. Real-time DFA State Tracking: ", "Displays the current state (q_bits, L_k) dynamically as symbols are scanned."),
    ("2. 4-Bit State Register Visualizer: ", "Shows live binary bitmask values (u, l, d, s) for Uppercase, Lowercase, Digit, and Special characters."),
    ("3. 16-State Boolean Lattice Visualizer: ", "A 5-tier graphical state machine featuring hardware-inspired LED status indicators."),
    ("4. Step-by-Step Transition Debugger: ", "Allows users to step forward and backward symbol-by-symbol to inspect delta(q, char) transitions."),
    ("5. Acceptance / Rejection Status: ", "Instantly determines language membership (L_valid), reaching accepting state q1111 with length >= 8."),
    ("6. 16-State Transition Matrix Table: ", "Complete formal transition function matrix with live active row highlighting and search filtering."),
    ("7. Shannon Entropy & Brute-Force Estimator: ", "Displays password entropy (in bits), alphabet pool size, and crack resistance time."),
    ("8. Transition Trace Table & JSON Export: ", "Full sequential execution trace table with one-click JSON export."),
    ("9. Academic Test Suite Runner: ", "Automated 10-case verification test suite testing boundary conditions with 100% accuracy."),
    ("10. Educational Theory & NLP Hub: ", "Formal 5-tuple mathematical definition, regular language closure proofs, and ReDoS comparison.")
]

for bold_prefix, desc_text in outputs:
    # Prefix
    page1.insert_text((MARGIN_LEFT + 8.0, cursor_y), bold_prefix, fontname=FONT_BOLD, fontsize=10.0)
    prefix_w = fitz.get_text_length(bold_prefix, fontname=FONT_BOLD, fontsize=10.0)
    page1.insert_text((MARGIN_LEFT + 8.0 + prefix_w, cursor_y), desc_text, fontname=FONT_TITLE, fontsize=10.0)
    cursor_y += 15.0

# ==========================================
# PAGE 2: SCREENSHOTS 1 & 2
# ==========================================
page2 = doc.new_page(width=PAGE_WIDTH, height=PAGE_HEIGHT)

img1_path = os.path.join(screenshots_dir, "screenshot1_simulator.png")
img2_path = os.path.join(screenshots_dir, "screenshot2_table.png")

rect_img1 = fitz.Rect(MARGIN_LEFT, 36.0, MARGIN_LEFT + USABLE_WIDTH, 36.0 + 345.0)
rect_img2 = fitz.Rect(MARGIN_LEFT, 410.0, MARGIN_LEFT + USABLE_WIDTH, 410.0 + 345.0)

if os.path.exists(img1_path):
    page2.insert_image(rect_img1, filename=img1_path)

if os.path.exists(img2_path):
    page2.insert_image(rect_img2, filename=img2_path)

# ==========================================
# PAGE 3: SCREENSHOT 3 & SUMMARY
# ==========================================
page3 = doc.new_page(width=PAGE_WIDTH, height=PAGE_HEIGHT)

img3_path = os.path.join(screenshots_dir, "screenshot3_testsuite.png")
rect_img3 = fitz.Rect(MARGIN_LEFT, 36.0, MARGIN_LEFT + USABLE_WIDTH, 36.0 + 345.0)

if os.path.exists(img3_path):
    page3.insert_image(rect_img3, filename=img3_path)

# Optional project summary / repository link on page 3 below image
page3.insert_text((MARGIN_LEFT, 420.0), "Project Implementation & Verification Summary:", fontname=FONT_BOLD, fontsize=13.0)

summary_p = (
    "The project was verified against all standard positive and negative test cases. The test suite results shown above "
    "demonstrate that the Deterministic Finite Automaton accurately identifies valid language members (satisfying all four character "
    "classes and length >= 8) while rejecting all strings with missing components or insufficient length with 100% precision.\n\n"
    "• Formal DFA 5-Tuple: M = (Q, Sigma, delta, q0, F)\n"
    "• Total Product States: 144 states (16 complexity states x 9 length states)\n"
    "• Time Complexity: O(n) strictly linear time (guaranteed zero backtracking)\n"
    "• Space Complexity: O(1) auxiliary space (4-bit bitmask register)\n"
    "• GitHub Repository: https://github.com/Jitendra2007/password-complexity-automata"
)

rect_sum = fitz.Rect(MARGIN_LEFT, 440.0, MARGIN_LEFT + USABLE_WIDTH, 700.0)
page3.insert_textbox(rect_sum, summary_p, fontname=FONT_TITLE, fontsize=10.5, lineheight=1.35)

# Save document
doc.save(pdf_path)
doc.close()
print(f"Successfully generated PDF: {pdf_path}")
