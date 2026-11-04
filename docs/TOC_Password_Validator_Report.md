# Theory of Computation (TOC) Assignment Report
## Project Title: Password Complexity Validator Using Finite Automata (DFA)

---

## 1. Executive Summary & Problem Definition

In modern computer security, **Password Complexity Validation** ensures that user passwords resist brute-force and dictionary attacks. Standard enterprise policy requires passwords to satisfy:
1. **At least 1 uppercase letter** ($\Sigma_U = [A-Z]$)
2. **At least 1 lowercase letter** ($\Sigma_L = [a-z]$)
3. **At least 1 numeric digit** ($\Sigma_D = [0-9]$)
4. **At least 1 special character** ($\Sigma_S = [!@\#\$\%\^\&*\dots]$)
5. **A minimum length** of $8$ characters ($|w| \ge 8$)

The goal of this project is to model and implement this validator using **Formal Language Theory and Finite Automata**, demonstrating that password validation is an instance of a **Regular Language** recognized by a **Deterministic Finite Automaton (DFA)**.

---

## 2. Theoretical Foundations

### 2.1 The Chomsky Hierarchy Classification
According to Noam Chomsky's hierarchy of formal grammars, languages are divided into four tiers:
* **Type 3 (Regular Languages):** Recognizable by Finite State Automata (DFA/NFA) and expressible via Regular Expressions.
* **Type 2 (Context-Free Languages):** Recognizable by Pushdown Automata.
* **Type 1 (Context-Sensitive Languages):** Recognizable by Linear Bounded Automata.
* **Type 0 (Recursively Enumerable):** Recognizable by Turing Machines.

Because password complexity constraints require finite state memory (counting up to a finite bound of 1 for each category and 8 for length), the target language is strictly **Regular (Type 3)**.

### 2.2 Closure Properties of Regular Languages
Let:
- $L_U$: The set of strings containing at least one uppercase letter $= \Sigma^* \Sigma_U \Sigma^*$
- $L_L$: The set of strings containing at least one lowercase letter $= \Sigma^* \Sigma_L \Sigma^*$
- $L_D$: The set of strings containing at least one numeric digit $= \Sigma^* \Sigma_D \Sigma^*$
- $L_S$: The set of strings containing at least one special character $= \Sigma^* \Sigma_S \Sigma^*$
- $L_{\ge 8}$: The set of strings with length at least 8 $= \Sigma^8 \Sigma^*$

The target language $L_{\text{valid}}$ is:
$$L_{\text{valid}} = L_U \cap L_L \cap L_D \cap L_S \cap L_{\ge 8}$$

> [!NOTE]
> **Theorem:** Regular languages are **closed under intersection** ($L_1 \cap L_2$ is regular if $L_1, L_2$ are regular). Therefore, the intersection of these five regular languages is guaranteed to be regular and recognizable by a single product DFA.

---

## 3. Formal 5-Tuple Specification of the DFA

A Deterministic Finite Automaton (DFA) is defined formally as a 5-tuple:
$$M = (Q, \Sigma, \delta, q_0, F)$$

### 3.1 Input Alphabet ($\Sigma$)
$$\Sigma = \Sigma_U \cup \Sigma_L \cup \Sigma_D \cup \Sigma_S$$
Where:
- $\Sigma_U = \{A, B, C, \dots, Z\}$
- $\Sigma_L = \{a, b, c, \dots, z\}$
- $\Sigma_D = \{0, 1, 2, \dots, 9\}$
- $\Sigma_S = \{!, @, \#, \$, \%, \hat{}, \&, *, (, ), -, \_, =, +, [, ], \{, \}, |, ;, :, ', ", ,, ., <, >, ?, /, `, \sim, \backslash\}$

### 3.2 Set of States ($Q$)
We model the state using a product automaton:
$$Q = Q_C \times Q_L$$
1. **$Q_C$ (Complexity States):** $2^4 = 16$ states representing the 4-bit vector $(u, l, d, s) \in \{0, 1\}^4$:
   - $u \in \{0, 1\}$: whether at least one uppercase letter has been encountered.
   - $l \in \{0, 1\}$: whether at least one lowercase letter has been encountered.
   - $d \in \{0, 1\}$: whether at least one digit has been encountered.
   - $s \in \{0, 1\}$: whether at least one special character has been encountered.
2. **$Q_L$ (Length States):** $\{L_0, L_1, L_2, L_3, L_4, L_5, L_6, L_7, L_{8+}\}$ representing the length counter up to 8.

Total states in the product automaton:
$$|Q| = 16 \times 9 = 144 \text{ states}$$

### 3.3 Initial State ($q_0$)
$$q_0 = (q_{0000}, L_0)$$
Meaning: No character types seen yet, length $= 0$.

### 3.4 Set of Accepting / Final States ($F$)
$$F = \{(q_{1111}, L_{8+})\}$$
Meaning: All 4 character criteria have been observed AND the string length is at least 8.

### 3.5 Transition Function ($\delta$)
$$\delta: Q \times \Sigma \to Q$$
For a state $q = ((u, l, d, s), L_k)$ and an input symbol $c \in \Sigma$:

$$\delta(((u, l, d, s), L_k), c) = ((u', l', d', s'), \min(k+1, 8))$$

Where:
$$u' = \begin{cases} 1 & \text{if } c \in \Sigma_U \\ u & \text{otherwise} \end{cases}$$
$$l' = \begin{cases} 1 & \text{if } c \in \Sigma_L \\ l & \text{otherwise} \end{cases}$$
$$d' = \begin{cases} 1 & \text{if } c \in \Sigma_D \\ d & \text{otherwise} \end{cases}$$
$$s' = \begin{cases} 1 & \text{if } c \in \Sigma_S \\ s & \text{otherwise} \end{cases}$$

---

## 4. 16-State Complexity Transition Table

Below is the state transition sub-table for the 16 character-complexity states $Q_C$:

| State ($q$) | Bitmask | Meaning (Seen So Far) | On $\Sigma_U$ | On $\Sigma_L$ | On $\Sigma_D$ | On $\Sigma_S$ | Accepting? |
|:---:|:---:|:---|:---:|:---:|:---:|:---:|:---:|
| $q_0$ | `0000` | $\emptyset$ (Initial) | $q_8$ | $q_4$ | $q_2$ | $q_1$ | No |
| $q_1$ | `0001` | $\{Special\}$ | $q_9$ | $q_5$ | $q_3$ | $q_1$ | No |
| $q_2$ | `0010` | $\{Digit\}$ | $q_{10}$ | $q_6$ | $q_2$ | $q_3$ | No |
| $q_3$ | `0011` | $\{Digit, Special\}$ | $q_{11}$ | $q_7$ | $q_3$ | $q_3$ | No |
| $q_4$ | `0100` | $\{Lower\}$ | $q_{12}$ | $q_4$ | $q_6$ | $q_5$ | No |
| $q_5$ | `0101` | $\{Lower, Special\}$ | $q_{13}$ | $q_5$ | $q_7$ | $q_5$ | No |
| $q_6$ | `0110` | $\{Lower, Digit\}$ | $q_{14}$ | $q_6$ | $q_6$ | $q_7$ | No |
| $q_7$ | `0111` | $\{Lower, Digit, Special\}$ | $q_{15}$ | $q_7$ | $q_7$ | $q_7$ | No |
| $q_8$ | `1000` | $\{Upper\}$ | $q_8$ | $q_{12}$ | $q_{10}$ | $q_9$ | No |
| $q_9$ | `1001` | $\{Upper, Special\}$ | $q_9$ | $q_{13}$ | $q_{11}$ | $q_9$ | No |
| $q_{10}$ | `1010` | $\{Upper, Digit\}$ | $q_{10}$ | $q_{14}$ | $q_{10}$ | $q_{11}$ | No |
| $q_{11}$ | `1011` | $\{Upper, Digit, Special\}$ | $q_{11}$ | $q_{15}$ | $q_{11}$ | $q_{11}$ | No |
| $q_{12}$ | `1100` | $\{Upper, Lower\}$ | $q_{12}$ | $q_{12}$ | $q_{14}$ | $q_{13}$ | No |
| $q_{13}$ | `1101` | $\{Upper, Lower, Special\}$ | $q_{13}$ | $q_{13}$ | $q_{15}$ | $q_{13}$ | No |
| $q_{14}$ | `1110` | $\{Upper, Lower, Digit\}$ | $q_{14}$ | $q_{14}$ | $q_{14}$ | $q_{15}$ | No |
| **$q_{15}$** | **`1111`** | **$\{Upper, Lower, Digit, Special\}$** | **$q_{15}$** | **$q_{15}$** | **$q_{15}$** | **$q_{15}$** | **YES** |

> [!TIP]
> Notice that state $q_{15}$ (`1111`) is an **absorbing / sink state** for complexity: once all 4 criteria are satisfied, any subsequent valid character keeps the automaton in $q_{15}$.

---

## 5. State Transition Graph

```mermaid
flowchart TD
    q0000["q0000 (Start)"] -->|"Upper"| q1000["q1000 (U)"]
    q0000 -->|"Lower"| q0100["q0100 (L)"]
    q0000 -->|"Digit"| q0010["q0010 (D)"]
    q0000 -->|"Special"| q0001["q0001 (S)"]

    q1000 -->|"Lower"| q1100["q1100 (U,L)"]
    q1000 -->|"Digit"| q1010["q1010 (U,D)"]
    q1000 -->|"Special"| q1001["q1001 (U,S)"]

    q0100 -->|"Upper"| q1100
    q0100 -->|"Digit"| q0110["q0110 (L,D)"]
    q0100 -->|"Special"| q0101["q0101 (L,S)"]

    q1100 -->|"Digit"| q1110["q1110 (U,L,D)"]
    q1100 -->|"Special"| q1101["q1101 (U,L,S)"]

    q1110 -->|"Special"| q1111((("★ q1111 (ACCEPT)"))))
    q1101 -->|"Digit"| q1111
    q1011 -->|"Lower"| q1111
    q0111 -->|"Upper"| q1111

    q1111 -->|"Any valid char"| q1111
```

---

## 6. Connection to NLP & Lexical Analysis

### Why is this relevant to NLP / Computational Linguistics?
In **Natural Language Processing (NLP)** and compiler design:
1. **Lexical Analysis (Lexing / Tokenization):**
   Before parsing sentence syntax or semantics, a text stream is tokenized into lexical units (tokens). Tokenizers rely on **Finite Automata** (DFAs) to classify characters into character classes (alphabet, punctuation, numbers, whitespaces) in linear time $O(n)$.
2. **Regular Expressions & Morphology:**
   Morphological parsing (e.g., detecting prefixes, suffixes, stem identification) is implemented using Finite State Transducers (FSTs) and Finite State Automata (FSAs).
3. **Equivalence in Pattern Matching:**
   The DFA implemented here is equivalent to the formal Regular Expression with positive lookahead assertions:
   ```regex
   ^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_\-+=\[\]{}|;:'",.<>?/`~\\]).{8,}$
   ```

---

## 7. Complexity Analysis

| Metric | Complexity | Explanation |
|---|---|---|
| **Time Complexity** | $\mathcal{O}(n)$ | Where $n$ is the length of the input string. The DFA reads exactly one symbol per step with $\mathcal{O}(1)$ state lookup. |
| **Space Complexity** | $\mathcal{O}(1)$ | The number of states is strictly bounded ($144$ states). Auxiliary storage does not grow with input length. |
| **Backtracking** | None | DFAs are deterministic, requiring zero back-tracking compared to naive regular expression engines. |

---

## 8. Verification & Test Suite

| Test Input | Input Classes Present | Length | Final State | Outcome | Reason |
|---|---|---|---|---|---|
| `pass` | Lowercase | 4 | $(q_{0100}, L_4)$ | **REJECT** | Too short ($<8$), missing Upper, Digit, Special |
| `Password` | Upper, Lower | 8 | $(q_{1100}, L_{8+})$ | **REJECT** | Missing Digit, Special |
| `Password1` | Upper, Lower, Digit | 9 | $(q_{1110}, L_{8+})$ | **REJECT** | Missing Special character |
| `admin@2026` | Lower, Digit, Special | 10 | $(q_{0111}, L_{8+})$ | **REJECT** | Missing Uppercase letter |
| `ALLCAPS123!` | Upper, Digit, Special | 11 | $(q_{1011}, L_{8+})$ | **REJECT** | Missing Lowercase letter |
| **`Password123!`** | **Upper, Lower, Digit, Special** | **12** | **$(q_{1111}, L_{8+})$** | **ACCEPT** | **All 4 criteria met AND length $\ge 8$** |
| **`P@ssw0rd2026`** | **Upper, Lower, Digit, Special** | **12** | **$(q_{1111}, L_{8+})$** | **ACCEPT** | **All 4 criteria met AND length $\ge 8$** |

---

## 9. Deliverables in Project Workspace (`c:\Users\tsapa\Desktop\toc`)

1. **[`dfa_validator.py`](file:///c:/Users/tsapa/Desktop/toc/dfa_validator.py)**: Pure Python DFA engine modeling the formal 5-tuple $(Q, \Sigma, \delta, q_0, F)$ with step-by-step transition tracking.
2. **[`cli_demo.py`](file:///c:/Users/tsapa/Desktop/toc/cli_demo.py)**: Interactive command-line interface with step-by-step transition tracing and transition table inspector.
3. **[`index.html`](file:///c:/Users/tsapa/Desktop/toc/index.html)**: Interactive visual DFA Web Application showing real-time active state transitions, 16 state nodes, and live criteria validation.
4. **[`server.py`](file:///c:/Users/tsapa/Desktop/toc/server.py)**: One-command HTTP server runner (`python server.py`) to launch the web dashboard in the browser.
