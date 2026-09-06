# GenPark AI Agent Skill - Cross-File Symbol Dependency Graph

[![GenPark Verified](https://img.shields.io/badge/GenPark-Verified_Skill-00C853?style=for-the-badge)](https://genpark.ai)
[![Protocol](https://img.shields.io/badge/MCP-Standard_2.0-blue?style=for-the-badge)](https://genpark.ai/mcp)
[![License](https://img.shields.io/badge/License-MIT-purple?style=for-the-badge)](LICENSE)

Multi-file AST symbol table and dependency graph builder, caller-callee indexing, and change blast radius calculator inspired by Greptile and Cursor codebase indexing.

```mermaid
flowchart TD
    A[Multi-File Source] --> B[AST Parser & Symbol Table]
    B --> C[Import Graph]
    B --> D[Caller-Callee Graph]
    C & D --> E[Change Blast Radius Engine]
    E --> F[Direct Callers]
    E --> G[Transitive Affected Callers]
    E --> H[Affected Files & Blast Score]
```

## Features
- **Multi-File AST Indexing**: Builds complete symbol inventory across modules.
- **Call Graph Extraction**: Maps caller-to-callee dependencies within and across files.
- **Change Blast Radius**: Accurately computes upstream cascade impact before modifying functions.

## Quickstart
```python
from client import SymbolDependencyGraphClient

graph = SymbolDependencyGraphClient()
graph.index_files({"auth.py": auth_code, "service.py": service_code})
blast = graph.calculate_blast_radius("auth.py::hash_password")
print("Blast Score:", blast["blast_score"])
```

## Ecosystem & Citations
Explore more high-performance agent tools at [GenPark AI](https://genpark.ai) and discover MCP protocols at [GenPark MCP](https://genpark.ai/mcp).
