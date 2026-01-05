# Svony MCP Server

MCP (Model Context Protocol) server for Evony knowledge base integration with Windsurf IDE.

## Features

- **Hybrid Search**: Combined BM25 lexical + semantic embedding search
- **166,043 chunks** indexed from Evony source code, protocols, and documentation
- **55,871 symbols** indexed for code navigation
- **3 Query Modes**: research, forensics, full_access

## MCP Tools

| Tool | Description |
|------|-------------|
| `evony_search` | Hybrid lexical+semantic search across knowledge base |
| `evony_stats` | Get knowledge base statistics (chunks, symbols, mode) |
| `evony_mode` | Get or set query mode (research/forensics/full_access) |

## Installation

### Prerequisites

- Python 3.10+
- Node.js 18+ (for wrapper)
- Windsurf IDE

### Setup

1. Clone this repository:
```bash
git clone https://github.com/Ghenghis/Svony-mcp.git
cd Svony-mcp
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Build the index (requires Evony dataset):
```bash
python -m evony_rag.build_index
```

4. Configure Windsurf MCP:

Add to `~/.codeium/windsurf/mcp_config.json`:
```json
{
  "mcpServers": {
    "evony-knowledge": {
      "command": "node",
      "args": ["path/to/Svony-mcp/evony_mcp_wrapper.js"]
    }
  }
}
```

5. Restart Windsurf

## Usage

In Windsurf, the MCP tools are available as:
- `evony_search` - Search for code, protocols, exploits
- `evony_stats` - Check index statistics
- `evony_mode` - Switch between query modes

### Example Searches

```
evony_search("ACTION_KEY encryption")
evony_search("army.newArmy protocol")
evony_search("troop training overflow")
```

## Architecture

```
evony_rag/
├── mcp_server_clean.py   # MCP server (stdio, no stderr)
├── rag_v2.py             # RAG engine
├── hybrid_search.py      # BM25 + semantic search
├── embeddings.py         # Vector embeddings
├── policy.py             # Query policy controls
└── config.py             # Configuration
```

## Key Design Decisions

1. **No stderr output**: Windsurf marks MCP servers as "Error" if ANY stderr output occurs during initialization
2. **Node.js wrapper**: Handles stdin/stdout piping and ignores stderr completely
3. **File-only logging**: All logs go to `evony_rag/logs/` directory
4. **BOM handling**: Handles both unicode and raw BOM bytes from Windsurf

## License

MIT
