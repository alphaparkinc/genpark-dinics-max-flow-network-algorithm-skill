import sys
import json
from client import DinicMaxFlow

def handle_request(req):
    method = req.get("method")
    params = req.get("params", {})
    req_id = req.get("id")

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "dinic_max_flow",
                        "description": "Compute maximum network flow using Dinic's blocking flow algorithm",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "num_nodes": {"type": "integer"},
                                "edges": {
                                    "type": "array",
                                    "items": {"type": "array", "items": {"type": "number"}}
                                },
                                "source": {"type": "integer"},
                                "sink": {"type": "integer"}
                            },
                            "required": ["num_nodes", "edges", "source", "sink"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {})
        if name == "dinic_max_flow":
            g = DinicMaxFlow(args["num_nodes"])
            for u, v, cap in args["edges"]:
                g.add_edge(int(u), int(v), float(cap))
            mf = g.compute_max_flow(int(args["source"]), int(args["sink"]))
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps({"source": args["source"], "sink": args["sink"], "max_flow": mf})}]}}
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    for line in sys.stdin:
        if line.strip():
            req = json.loads(line)
            res = handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
