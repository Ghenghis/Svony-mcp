# Evony Knowledge RAG System v2

## Professional Retrieval-Augmented Generation for Evony Reverse Engineering

### Features

- **Hybrid Search**: BM25 lexical + semantic embeddings with rank fusion
- **166,043 Indexed Chunks** from curated dataset
- **55,871 Code Symbols** indexed for definition lookup
- **Policy-Based Access**: Research/Forensics/Full Access modes
- **Multi-Interface**: CLI, HTTP API, MCP Server
- **LM Studio Integration**: OpenAI-compatible for any local LLM
- **Windsurf IDE Integration**: Native MCP tools

---

## Quick Start

### 1. Start the API Server
```batch
EVONY_RAG_V2_API.bat
```

### 2. Or Use Interactive CLI
```batch
EVONY_RAG_V2_CLI.bat
```

### 3. Or Enable in Windsurf
Add to `~/.codeium/windsurf/mcp_config.json`:
```json
{
  "mcpServers": {
    "evony-knowledge": {
      "command": "python",
      "args": ["-m", "evony_rag.mcp_server_v2"],
      "cwd": "c:\\Users\\Admin\\Downloads\\Evony_Decrypted"
    }
  }
}
```

---

## Architecture

```
┌─────────────────────────────────────────────┐
│              USER INTERFACES                 │
│  CLI    │    HTTP API    │    MCP Server    │
└─────────┴────────────────┴──────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────┐
│              RAG ENGINE v2                   │
│  Query Router → Policy Engine → Generator   │
└─────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────┐
│             HYBRID SEARCH                    │
│  BM25 (Lexical) + Embeddings (Semantic)     │
│           → Reciprocal Rank Fusion          │
└─────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────┐
│              INDEX LAYER                     │
│  166k chunks │ 55k symbols │ 384-dim vectors│
└─────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────┐
│           CURATED DATASET                    │
│  8,957 files across 6 categories            │
└─────────────────────────────────────────────┘
```

---

## Documentation

| Document | Description |
|----------|-------------|
| [ARCHITECTURE.md](ARCHITECTURE.md) | System design and data flow |
| [API_REFERENCE.md](API_REFERENCE.md) | Complete API documentation |
| [MCP_TOOLS_REFERENCE.md](MCP_TOOLS_REFERENCE.md) | Windsurf MCP tools |
| [TRAINING_GUIDE.md](TRAINING_GUIDE.md) | Fine-tuning with Unsloth |
| [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | Common issues and fixes |
| [QUICK_REFERENCE.md](QUICK_REFERENCE.md) | Cheat sheet |

---

## Query Modes

| Mode | Description | Categories |
|------|-------------|------------|
| `research` | Default safe mode | All except exploits |
| `forensics` | Strict analysis | Code, protocol, docs only |
| `full_access` | Everything | Including exploits |

---

## MCP Tools (7)

| Tool | Purpose |
|------|---------|
| `evony.search` | Hybrid search with scores |
| `evony.answer` | RAG answer with citations |
| `evony.open` | Get file content |
| `evony.symbol` | Find symbol definitions |
| `evony.trace` | Multi-hop concept tracing |
| `evony.mode` | Get/set query mode |
| `evony.stats` | System statistics |

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/chat/completions` | POST | OpenAI-compatible |
| `/v1/rag/search` | POST | Retrieval only |
| `/v1/rag/answer` | POST | Answer + citations |
| `/v1/rag/symbol` | POST | Symbol lookup |
| `/v1/rag/trace` | POST | Multi-hop trace |
| `/v1/rag/open` | POST | File content |
| `/modes` | GET | List modes |
| `/mode` | POST | Set mode |
| `/stats` | GET | Statistics |

---

## CLI Commands

```
/mode [name]       Get/set mode
/find <query>      Search only
/symbol <name>     Find symbol
/trace <topic>     Multi-hop trace
/open <path>       View file
/stats             Statistics
/nollm             Toggle LLM
/quit              Exit
```

---

## Example Queries

```
What is ACTION_KEY used for?
How does army.newArmy work?
What parameters does troop.produceTroop accept?
/symbol ACTION_KEY
/trace encryption
/mode full_access
```

---

## File Structure

```
evony_rag/
├── __init__.py           # Package init
├── config.py             # Configuration
├── embeddings.py         # Vector indexing (v1)
├── hybrid_search.py      # BM25 + embeddings (v2)
├── policy.py             # Policy engine
├── query_router.py       # Safety filters (v1)
├── rag_engine.py         # RAG engine (v1)
├── rag_v2.py             # Enhanced RAG (v2)
├── mcp_server.py         # MCP server (v1)
├── mcp_server_v2.py      # Enhanced MCP (v2)
├── lmstudio_api.py       # HTTP API (v1)
├── api_v2.py             # Enhanced API (v2)
├── cli.py                # CLI (v1)
├── cli_v2.py             # Enhanced CLI (v2)
├── requirements.txt      # Dependencies
├── index/                # Stored indexes
└── docs/                 # Documentation
```

---

## Dependencies

```
sentence-transformers>=2.2.0
numpy>=1.24.0
requests>=2.28.0
aiohttp>=3.8.0
pyyaml>=6.0
tqdm>=4.65.0
```

---

## LM Studio Setup

1. Load model: `qwen3-vl-8b-instruct-abliterated-v2.0`
2. Context length: 8K-16K (80K available)
3. Port: 1234 (default)
4. GPU: Full offload for best performance

---

## Training (Optional)

After RAG is working well, fine-tune for better vocabulary:

```batch
SETUP_EVONY_AI.bat    # Install Unsloth
TRAIN_EVONY_AI.bat    # Train (~2-3 hours)
CHAT_EVONY_AI.bat     # Test
```

See [TRAINING_GUIDE.md](TRAINING_GUIDE.md) for details.
