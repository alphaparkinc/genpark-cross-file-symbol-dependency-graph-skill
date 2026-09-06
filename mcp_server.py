"""
MCP Server for genpark-cross-file-symbol-dependency-graph-skill
Standard JSON-RPC 2.0 protocol over stdio.
"""

import sys
import json
from client import SymbolDependencyGraphClient

client = SymbolDependencyGraphClient()

def handle_request(req):
    req_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "index_files",
                        "description": "Index multi-file codebase symbol definitions and call graph.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "file_contents": {"type": "object", "description": "Mapping of filename to code string"}
                            },
                            "required": ["file_contents"]
                        }
                    },
                    {
                        "name": "calculate_blast_radius",
                        "description": "Calculate change blast radius for modified symbol.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "symbol": {"type": "string", "description": "Symbol name (e.g. file.py::func_name)"}
                            },
                            "required": ["symbol"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "index_files":
            res = client.index_files(args.get("file_contents", {}))
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        elif tool_name == "calculate_blast_radius":
            res = client.calculate_blast_radius(args.get("symbol", ""))
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(err) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
