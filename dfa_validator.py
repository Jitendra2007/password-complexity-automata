"""
Password Complexity Validator Using Finite Automata (DFA)
Theory of Computation (TOC) & Pattern Matching Implementation

Formal Definition of the Automaton:
M = (Q, Sigma, delta, q0, F)
- Q: Set of states (16 complexity states x 9 length states = 144 product states)
- Sigma: Input alphabet (Uppercase, Lowercase, Digits, Special Characters)
- delta: Transition function Q x Sigma -> Q
- q0: Initial state (0000, len=0)
- F: Set of accepting states (1111, len>=8)
"""

from typing import Dict, List, Tuple, Any
import string

class CharacterClass:
    UPPERCASE = "UPPERCASE"
    LOWERCASE = "LOWERCASE"
    DIGIT = "DIGIT"
    SPECIAL = "SPECIAL"
    INVALID = "INVALID"

class PasswordDFA:
    def __init__(self, min_length: int = 8):
        self.min_length = min_length
        self.special_chars = set("!@#$%^&*()-_=+[]{}|;:'\",.<>?/`~\\")
        
        # 16 complexity states: (has_upper, has_lower, has_digit, has_special)
        # Encoded as 4-bit strings: '0000' to '1111'
        self.complexity_states = [f"{i:04b}" for i in range(16)]
        
        # Length states: 0, 1, 2, ..., min_length (where min_length means >= min_length)
        self.length_states = list(range(self.min_length + 1))
        
        # Product states: (complexity_state, length_state)
        self.Q = [(c, l) for c in self.complexity_states for l in self.length_states]
        self.q0 = ("0000", 0)
        self.F = [("1111", self.min_length)]
        
    def classify_char(self, char: str) -> str:
        """Lexical categorization (Alphabet mapping)."""
        if char.isupper():
            return CharacterClass.UPPERCASE
        elif char.islower():
            return CharacterClass.LOWERCASE
        elif char.isdigit():
            return CharacterClass.DIGIT
        elif char in self.special_chars:
            return CharacterClass.SPECIAL
        else:
            return CharacterClass.INVALID

    def delta(self, current_state: Tuple[str, int], char: str) -> Tuple[Tuple[str, int], str]:
        """
        State Transition Function: delta(q, a) -> q'
        Returns: (next_state, char_class)
        """
        c_state, l_state = current_state
        char_class = self.classify_char(char)
        
        u, l, d, s = [int(bit) for bit in c_state]
        
        if char_class == CharacterClass.UPPERCASE:
            u = 1
        elif char_class == CharacterClass.LOWERCASE:
            l = 1
        elif char_class == CharacterClass.DIGIT:
            d = 1
        elif char_class == CharacterClass.SPECIAL:
            s = 1
        else:
            # Trap state / invalid character (optional: could reject or treat as non-contributing)
            pass
            
        next_c_state = f"{u}{l}{d}{s}"
        next_l_state = min(l_state + 1, self.min_length)
        
        return (next_c_state, next_l_state), char_class

    def process(self, password: str) -> Dict[str, Any]:
        """
        Simulate the DFA by feeding the password string symbol by symbol.
        Traces the execution path through state transitions.
        """
        current_state = self.q0
        history = []
        
        for idx, char in enumerate(password):
            prev_state = current_state
            next_state, char_class = self.delta(current_state, char)
            history.append({
                "step": idx + 1,
                "input_char": char,
                "char_class": char_class,
                "from_state": prev_state,
                "to_state": next_state,
                "bits_from": prev_state[0],
                "bits_to": next_state[0],
                "len_from": prev_state[1],
                "len_to": next_state[1]
            })
            current_state = next_state
            
        c_final, l_final = current_state
        u, l, d, s = [bool(int(bit)) for bit in c_final]
        is_length_valid = (l_final >= self.min_length)
        is_accepted = (current_state in self.F)
        
        # Missing rules breakdown
        missing = []
        if not u:
            missing.append("At least 1 Uppercase letter (A-Z)")
        if not l:
            missing.append("At least 1 Lowercase letter (a-z)")
        if not d:
            missing.append("At least 1 Numeric digit (0-9)")
        if not s:
            missing.append("At least 1 Special character (!@#$%^&*)")
        if not is_length_valid:
            missing.append(f"Minimum length {self.min_length} characters (got {len(password)})")
            
        return {
            "password": password,
            "length": len(password),
            "final_state": current_state,
            "is_accepted": is_accepted,
            "history": history,
            "criteria": {
                "uppercase": u,
                "lowercase": l,
                "digit": d,
                "special": s,
                "length_valid": is_length_valid
            },
            "missing_rules": missing
        }

    def get_transition_table_16(self) -> List[Dict[str, str]]:
        """
        Returns the 16-state complexity transition table
        covering delta_c(q, input_class).
        """
        table = []
        for i in range(16):
            state = f"{i:04b}"
            u, l, d, s = [int(b) for b in state]
            
            # Transitions for each class
            on_upper = f"{1}{l}{d}{s}"
            on_lower = f"{u}{1}{d}{s}"
            on_digit = f"{u}{l}{1}{s}"
            on_special = f"{u}{l}{d}{1}"
            
            table.append({
                "state": state,
                "state_name": f"q_{state}",
                "meaning": self.describe_state(state),
                "on_upper": f"q_{on_upper}",
                "on_lower": f"q_{on_lower}",
                "on_digit": f"q_{on_digit}",
                "on_special": f"q_{on_special}",
                "is_final": (state == "1111")
            })
        return table

    def describe_state(self, state_bits: str) -> str:
        u, l, d, s = [bool(int(b)) for b in state_bits]
        met = []
        if u: met.append("Upper")
        if l: met.append("Lower")
        if d: met.append("Digit")
        if s: met.append("Special")
        return "{" + ", ".join(met) + "}" if met else "{Empty}"

if __name__ == "__main__":
    validator = PasswordDFA(min_length=8)
    test_passwords = [
        "pass",
        "Password",
        "Password1",
        "Password123!",
        "admin@2026",
        "ALLCAPS123!"
    ]
    
    print("=" * 60)
    print("DFA PASSWORD COMPLEXITY VALIDATOR - TEST SUITE")
    print("=" * 60)
    
    for pwd in test_passwords:
        result = validator.process(pwd)
        status = "ACCEPT [VALID]" if result["is_accepted"] else "REJECT [INVALID]"
        print(f"\nPassword: '{pwd}' -> {status}")
        print(f"Final State: {result['final_state']}")
        if result["missing_rules"]:
            print("Missing:", "; ".join(result["missing_rules"]))
        else:
            print("All criteria met!")
