"""
Demonstration of genpark-cross-file-symbol-dependency-graph-skill
"""

from client import SymbolDependencyGraphClient

def main():
    graph = SymbolDependencyGraphClient()

    files = {
        "auth.py": """
def hash_password(password):
    return "hashed_" + password

def verify_credentials(user, password):
    h = hash_password(password)
    return True
""",
        "service.py": """
from auth import verify_credentials

def login_endpoint(user, password):
    if verify_credentials(user, password):
        return "success"
    return "denied"
""",
        "admin.py": """
from service import login_endpoint

def admin_sudo_login(admin_user, secret):
    return login_endpoint(admin_user, secret)
"""
    }

    report = graph.index_files(files)
    print("=== INDEXED CODEBASE SYMBOLS ===")
    print(f"Indexed files: {report['indexed_files']}")
    print(f"Total symbols: {report['symbols_count']}")

    print("\n=== CALCULATING BLAST RADIUS FOR 'hash_password' ===")
    blast = graph.calculate_blast_radius("auth.py::hash_password")
    print(f"Target: {blast['target_symbol']}")
    print(f"Direct Callers: {blast['direct_callers']}")
    print(f"Transitive Affected: {blast['transitive_affected_symbols']}")
    print(f"Affected Files: {blast['affected_files']}")
    print(f"Blast Radius Score: {blast['blast_score']} / 100")

if __name__ == "__main__":
    main()
