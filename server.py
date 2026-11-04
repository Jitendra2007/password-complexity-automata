"""
AutomataGuard Local Web Server
Runs the Password Complexity Validator (DFA Automata) website locally.
Usage: python server.py
"""

import http.server
import socketserver
import webbrowser
import os
import sys

DEFAULT_PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def log_message(self, format, *args):
        # Clean terminal logging
        sys.stderr.write(f"[{self.log_date_time_string()}] {format % args}\n")

def find_available_port(start_port=8080, max_attempts=20):
    import socket
    for port in range(start_port, start_port + max_attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('127.0.0.1', port)) != 0:
                return port
    return start_port

if __name__ == "__main__":
    port = find_available_port(DEFAULT_PORT)
    url = f"http://localhost:{port}/index.html"
    
    print("=" * 68)
    print("  ★ AUTOMATAGUARD · DFA PASSWORD COMPLEXITY & NLP TOKENIZER ★")
    print("  Theory of Computation (TOC) & Formal Language Engineering")
    print("=" * 68)
    print(f"\n[+] Local Server running at : {url}")
    print(f"[+] Root Workspace Directory: {DIRECTORY}")
    print("[+] Launching default browser automatically...")
    print("\n[i] Press Ctrl+C in this terminal window to stop the server.\n" + "-" * 68)

    webbrowser.open(url)

    socketserver.TCPServer.allow_reuse_address = True
    try:
        with socketserver.TCPServer(("", port), QuietHandler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[!] Server stopped cleanly. Have a great demo!")
