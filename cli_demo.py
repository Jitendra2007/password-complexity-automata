"""
Interactive Terminal Demo for Theory of Computation Assignment:
Password Complexity Validator Using Finite Automata (DFA)
"""

import sys
from dfa_validator import PasswordDFA, CharacterClass

def print_banner():
    print("*" * 72)
    print("*" + " " * 70 + "*")
    print("*    THEORY OF COMPUTATION (TOC) - AUTOMATA & FORMAL LANGUAGES         *")
    print("*    PROJECT: PASSWORD COMPLEXITY VALIDATOR USING DFA                  *")
    print("*" + " " * 70 + "*")
    print("*" * 72)
    print("\n[Theory Background]")
    print("- Model: Deterministic Finite Automaton (DFA) M = (Q, Σ, δ, q0, F)")
    print("- Alphabet Σ: Uppercase (Σ_U), Lowercase (Σ_L), Digits (Σ_D), Specials (Σ_S)")
    print("- States Q: 16 Complexity States (bitmask u|l|d|s) × 9 Length states (0..8+)")
    print("- Language L: { w ∈ Σ* | |w|>=8 and w contains >=1 of each class }\n")

def print_transition_table():
    validator = PasswordDFA(8)
    table = validator.get_transition_table_16()
    print("-" * 78)
    print(f"{'State':<8} | {'Meaning':<26} | {'On Upper':<9} | {'On Lower':<9} | {'On Digit':<9} | {'On Special':<9} | {'Final?'}")
    print("-" * 78)
    for row in table:
        flag = " [ACCEPT]" if row["is_final"] else ""
        print(f"{row['state_name']:<8} | {row['meaning']:<26} | {row['on_upper']:<9} | {row['on_lower']:<9} | {row['on_digit']:<9} | {row['on_special']:<9} | {flag}")
    print("-" * 78)

def test_password_interactively():
    validator = PasswordDFA(min_length=8)
    
    while True:
        print("\n" + "=" * 72)
        print("OPTIONS: ")
        print("  1. Validate a password (with step-by-step state transition trace)")
        print("  2. View DFA 16-State Transition Table")
        print("  3. Run pre-configured test suite")
        print("  4. Exit")
        print("=" * 72)
        
        choice = input("Enter choice (1-4): ").strip()
        
        if choice == "1":
            pwd = input("\nEnter password to test: ")
            res = validator.process(pwd)
            
            print("\n--- STEP-BY-STEP DFA TRANSITION TRACE ---")
            print(f"Initial State: q0 = ('0000', len=0)  [Nothing seen yet]\n")
            print(f"{'Step':<5} | {'Char':<6} | {'Type':<12} | {'Transition δ(Current, Char)':<32} | {'New State'}")
            print("-" * 72)
            
            for h in res["history"]:
                trans = f"δ(('{h['bits_from']}',{h['len_from']}), '{h['input_char']}')"
                to_st = f"('{h['bits_to']}', {h['len_to']})"
                print(f"{h['step']:<5} | '{h['input_char']}'{'' :<3} | {h['char_class']:<12} | {trans:<32} | -> {to_st}")
                
            print("-" * 72)
            print(f"Final State reached: {res['final_state']}")
            
            if res["is_accepted"]:
                print("\n>>> RESULT: ACCEPTED (Language Member) <<<")
                print("Proof: Automaton halted in accepting state F = ('1111', 8+).")
                print("All 4 regular language constraints and minimum length (8+) satisfied!")
            else:
                print("\n>>> RESULT: REJECTED (Non-Language Member) <<<")
                print("Proof: Automaton halted in non-accepting state.")
                print("Violated constraints:")
                for rule in res["missing_rules"]:
                    print(f"  [X] {rule}")
                    
        elif choice == "2":
            print("\n--- 16-STATE DFA COMPLEXITY TRANSITION TABLE ---")
            print("Encoding: (Uppercase, Lowercase, Digit, Special) as 4 bits")
            print_transition_table()
            
        elif choice == "3":
            tests = [
                ("abc", "Too short, only lowercase"),
                ("HelloWorld", "Upper & Lower, no digit/special, length >= 8"),
                ("Hello1234", "Upper, Lower, Digit, no special"),
                ("hello1234!", "Lower, Digit, Special, missing Uppercase"),
                ("HELLO1234!", "Upper, Digit, Special, missing Lowercase"),
                ("P@ssw0rd2026", "Valid: all 4 types + length >= 8")
            ]
            print("\n--- RUNNING PRECONFIGURED TEST SUITE ---")
            for p, desc in tests:
                r = validator.process(p)
                status = "ACCEPTED" if r["is_accepted"] else "REJECTED"
                print(f"\nPassword : '{p}'  ({desc})")
                print(f"Outcome  : [{status}] -> Final State: {r['final_state']}")
                if r["missing_rules"]:
                    print(f"Deficit  : {', '.join(r['missing_rules'])}")
                    
        elif choice == "4":
            print("\nExiting. Good luck with your Theory of Computation assignment!")
            break
        else:
            print("Invalid choice, please select 1, 2, 3, or 4.")

if __name__ == "__main__":
    print_banner()
    test_password_interactively()
