# AutomataGuard · Password Complexity Validator Using Finite Automata (DFA)

[![Python 3](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-emerald.svg)](LICENSE)
[![Theory of Computation](https://img.shields.io/badge/TOC-Chomsky%20Type--3%20Regular-purple.svg)]()
[![DFA](https://img.shields.io/badge/DFA-Deterministic%20Finite%20Automaton-cyan.svg)]()
[![NLP Lexical Tokenization](https://img.shields.io/badge/NLP-Lexical%20Scanner-orange.svg)]()

> An academic and interactive implementation of a **Deterministic Finite Automaton (DFA)** designed to validate password complexity based on formal language theory, regular language intersection, and NLP lexical tokenization.

---

## 📌 Project Overview & Objectives

In modern computer security and compiler design, pattern validation is often delegated to backtracking regular expressions (NFAs), which are vulnerable to **Regular Expression Denial of Service (ReDoS)** through catastrophic exponential backtracking $\mathcal{O}(2^n)$.

This project models and proves password validation as a strictly **Type-3 Regular Language** recognized by a **Deterministic Finite Automaton (DFA)**:
- **Linear Time Complexity:** $\mathcal{O}(n)$, guaranteed single-pass processing with zero backtracking.
- **Constant Space Complexity:** $\mathcal{O}(1)$ auxiliary space utilizing a compact 4-bit state register.
- **Formal Product State Space:** $16 \text{ complexity states} \times 9 \text{ length states} = 144 \text{ product states}$.
- **NLP / Compiler Connection:** Demonstrates how lexical scanners (e.g. Lex, Flex) classify symbols into alphabet equivalence classes ($\Sigma_U, \Sigma_L, \Sigma_D, \Sigma_S$).

---

## 🚀 Quick Start

### Method 1: Web Visualizer (Recommended)
Launch the interactive web application locally:
```bash
python server.py
```
> This automatically starts the local HTTP server and opens [`index.html`](index.html) in your default web browser.

Alternatively, you can double-click or open [`index.html`](index.html) directly in any modern browser without running a server.

### Method 2: Terminal CLI & Step-by-Step Transition Tracing
Run the command-line interface:
```bash
python cli_demo.py
```
* **Option 1:** Enter any password to view step-by-step transition delta logs $\delta(q_i, \text{char}) \to q_j$.
* **Option 2:** Print the complete 16-state mathematical transition table.
* **Option 3:** Run pre-configured boundary test cases.

---

## 🧠 Formal Mathematical Definition (5-Tuple)

The automaton is defined formally as:
$$M = (Q, \Sigma, \delta, q_0, F)$$

### 1. Alphabet ($\Sigma$)
Partitioned into 4 equivalence classes:
- $\Sigma_U = [A-Z]$ (Uppercase letters)
- $\Sigma_L = [a-z]$ (Lowercase letters)
- $\Sigma_D = [0-9]$ (Numeric digits)
- $\Sigma_S = [!@\#\$\%\^\&*\dots]$ (Special characters)

### 2. State Space ($Q$)
Product automaton $Q = Q_C \times Q_L$:
- $Q_C = \{0, 1\}^4$ representing the 16 boolean complexity states ($q_{0000}$ through $q_{1111}$).
- $Q_L = \{L_0, L_1, \dots, L_7, L_{8+}\}$ tracking string length up to 8.
- Total formal states: $|Q| = 16 \times 9 = 144$.

### 3. Start State ($q_0$)
$$q_0 = (q_{0000}, L_0)$$
No character classes observed, length $= 0$.

### 4. Accepting States ($F$)
$$F = \{(q_{1111}, L_{8+})\}$$
All 4 character classes observed AND length $\ge 8$.

### 5. Transition Function ($\delta$)
$$\delta(((u, l, d, s), L_k), c) = ((u \lor c \in \Sigma_U, l \lor c \in \Sigma_L, d \lor c \in \Sigma_D, s \lor c \in \Sigma_S), \min(k+1, 8))$$

### 6. Regular Language Intersection Proof
Let:
- $L_U = \Sigma^* \Sigma_U \Sigma^*$ (Contains at least one uppercase letter)
- $L_L = \Sigma^* \Sigma_L \Sigma^*$ (Contains at least one lowercase letter)
- $L_D = \Sigma^* \Sigma_D \Sigma^*$ (Contains at least one digit)
- $L_S = \Sigma^* \Sigma_S \Sigma^*$ (Contains at least one special character)
- $L_{\ge 8} = \Sigma^8 \Sigma^*$ (Length at least 8 characters)

By the **closure of regular languages under intersection**:
$$L_{\text{valid}} = L_U \cap L_L \cap L_D \cap L_S \cap L_{\ge 8}$$
$L_{\text{valid}}$ is strictly **Regular (Chomsky Type-3)**.

---

## 📂 Repository File Structure

```
├── index.html           # Interactive web visualizer & DFA simulator (HTML5/CSS3/JS)
├── server.py            # Local Python HTTP server with auto-port discovery
├── dfa_validator.py     # Pure Python implementation of the formal DFA 5-tuple
├── cli_demo.py          # Interactive terminal CLI with trace logging and test runner
├── .gitignore           # Git ignore configurations
├── README.md            # Main project documentation
└── docs/
    ├── TOC_Password_Validator_Report.md         # Comprehensive academic report & proofs
    └── Faculty_Presentation_Guide_and_Viva_Prep.md # Presentation script & top viva Q&A
```

---

## 🔬 Key Web Visualizer Features

1. **Real-time DFA Execution:** Immediate feedback on every keystroke with 4-bit register display.
2. **16-State Boolean Lattice:** Arranged into 5 tiers with hardware-inspired LED status indicators.
3. **Step-by-Step Debugger:** Step forward/backward through input characters to trace transitions.
4. **Transition Table Matrix:** Filterable 16-state matrix with active row highlighting.
5. **Shannon Entropy & Brute Force Estimator:** Calculates cryptographic entropy in bits and resistance time.
6. **Academic Batch Test Runner:** 10 pre-loaded boundary test cases with 100% classification accuracy.

---

## 📚 Academic Documentation & Viva Preparation

Comprehensive documentation for academic evaluations is included in the `docs/` folder:
- [TOC Academic Project Report](docs/TOC_Password_Validator_Report.md): Mathematical formulations, Chomsky hierarchy, and complexity analysis.
- [Faculty Presentation & Viva Prep](docs/Faculty_Presentation_Guide_and_Viva_Prep.md): 3-minute presentation script, demonstration checklist, and top 10 viva defense questions with answers.

---

## 📜 License
This project is open-source under the [MIT License](LICENSE).
