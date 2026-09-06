"""
Cross-File Symbol Dependency Graph and Change Blast Radius Calculator.
Zero external dependencies, standard library only.
"""

import ast
from typing import Dict, List, Any, Optional, Set

class SymbolDependencyGraphClient:
    """
    Indexes multi-file codebase symbol declarations, imports, and caller-callee invocations.
    Calculates change blast radius (upstream callers and downstream dependencies).
    """

    def __init__(self):
        self.symbol_table = {}
        self.call_graph = {}
        self.import_graph = {}

    def index_files(self, file_contents: Dict[str, str]) -> Dict[str, Any]:
        """
        Indexes dictionary of {filepath: source_code}.
        Extracts declared functions, classes, imports, and call sites.
        """
        self.symbol_table.clear()
        self.call_graph.clear()
        self.import_graph.clear()

        for filepath, code in file_contents.items():
            self.import_graph[filepath] = []
            try:
                tree = ast.parse(code)
            except SyntaxError:
                continue

            # 1. Imports
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        self.import_graph[filepath].append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    mod = node.module or ""
                    self.import_graph[filepath].append(mod)

            # 2. Symbol definitions and calls
            class SymbolVisitor(ast.NodeVisitor):
                def __init__(self, current_file, parent_client):
                    self.file = current_file
                    self.parent = parent_client
                    self.current_scope = None

                def visit_FunctionDef(self, node):
                    sym_id = f"{self.file}::{node.name}"
                    self.parent.symbol_table[sym_id] = {
                        "file": self.file,
                        "name": node.name,
                        "type": "function",
                        "line": getattr(node, "lineno", 0)
                    }
                    old_scope = self.current_scope
                    self.current_scope = sym_id
                    self.generic_visit(node)
                    self.current_scope = old_scope

                def visit_ClassDef(self, node):
                    sym_id = f"{self.file}::{node.name}"
                    self.parent.symbol_table[sym_id] = {
                        "file": self.file,
                        "name": node.name,
                        "type": "class",
                        "line": getattr(node, "lineno", 0)
                    }
                    old_scope = self.current_scope
                    self.current_scope = sym_id
                    self.generic_visit(node)
                    self.current_scope = old_scope

                def visit_Call(self, node):
                    callee_name = ""
                    if isinstance(node.func, ast.Name):
                        callee_name = node.func.id
                    elif isinstance(node.func, ast.Attribute):
                        callee_name = node.func.attr

                    if callee_name and self.current_scope:
                        if self.current_scope not in self.parent.call_graph:
                            self.parent.call_graph[self.current_scope] = set()
                        self.parent.call_graph[self.current_scope].add(callee_name)

                    self.generic_visit(node)

            visitor = SymbolVisitor(filepath, self)
            visitor.visit(tree)

        # Convert sets to lists
        serializable_call_graph = {k: list(v) for k, v in self.call_graph.items()}

        return {
            "indexed_files": len(file_contents),
            "symbols_count": len(self.symbol_table),
            "symbols": list(self.symbol_table.keys()),
            "call_graph": serializable_call_graph
        }

    def calculate_blast_radius(self, modified_symbol: str) -> Dict[str, Any]:
        """
        Calculates blast radius of modifying a specific symbol.
        Finds all direct and transitive upstream callers affected.
        """
        # Find which declared symbols call this modified_symbol (either by full ID or simple name)
        simple_name = modified_symbol.split("::")[-1]

        direct_callers = set()
        for caller, callees in self.call_graph.items():
            if simple_name in callees or modified_symbol in callees:
                direct_callers.add(caller)

        # Transitive search
        visited = set(direct_callers)
        queue = list(direct_callers)

        while queue:
            curr = queue.pop(0)
            curr_simple = curr.split("::")[-1]
            for caller, callees in self.call_graph.items():
                if curr_simple in callees or curr in callees:
                    if caller not in visited:
                        visited.add(caller)
                        queue.append(caller)

        affected_files = list(set(s.split("::")[0] for s in visited))

        return {
            "target_symbol": modified_symbol,
            "direct_callers": list(direct_callers),
            "transitive_affected_symbols": list(visited),
            "affected_files": affected_files,
            "blast_score": min(100.0, len(visited) * 15.0 + len(affected_files) * 20.0)
        }
