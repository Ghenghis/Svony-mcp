# Evony Knowledge RAG System

**Retrieval-Augmented Generation for Evony expertise**

## Why RAG First?

- ✅ **Traceability** - See exact file/line sources for every answer
- ✅ **Updatable** - Add new data without retraining
- ✅ **Controllable** - Blacklist categories, filter exploits
- ✅ **Fast** - No GPU needed for retrieval
- ✅ **Accurate** - Grounded in actual source material

## Quick Start

```bash
# 1. Install dependencies
SETUP_EVONY_RAG.bat

# 2. Choose your interface:
EVONY_RAG_CLI.bat      # Interactive CLI
EVONY_RAG_API.bat      # LM Studio compatible API  
EVONY_RAG_MCP.bat      # MCP server for Windsurf
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    EVONY KNOWLEDGE RAG                       │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐    ┌──────────────┐    ┌───────────────┐  │
│  │ Query Router│───▶│ Safety Filter│───▶│ Intent Detect │  │
│  └─────────────┘    └──────────────┘    └───────────────┘  │
│         │                                       │           │
│         ▼                                       ▼           │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              EMBEDDING INDEX                         │   │
│  │  - 8,900+ files indexed                             │   │
│  │  - sentence-transformers (local, no API)            │   │
│  │  - Chunked with line number tracking                │   │
│  └─────────────────────────────────────────────────────┘   │
│         │                                                   │
│         ▼                                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              RESPONSE GENERATOR                      │   │
│  │  - With citations (file:line)                       │   │
│  │  - Optional LM Studio integration                   │   │
│  │  - Standalone mode (no LLM needed)                  │   │
│  └─────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────┤
│  INTERFACES                                                 │
│  ┌─────────┐  ┌─────────────┐  ┌────────────────────────┐  │
│  │   CLI   │  │  HTTP API   │  │     MCP Server         │  │
│  │         │  │ (LM Studio) │  │    (Windsurf IDE)      │  │
│  └─────────┘  └─────────────┘  └────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Interfaces

### 1. CLI (`EVONY_RAG_CLI.bat`)

Interactive terminal interface:

```
[You]: How does the troop overflow glitch work?

[Evony Knowledge]:
The troop overflow exploit occurs when...

📚 Sources:
  📄 exploits/GLITCH_MECHANICS.md:45-89 (94%)
  📄 source_code/TroopController.as:234-267 (87%)

[intent: exploit_info | model: lmstudio]
```

Commands:
- `/find <query>` - Find relevant files
- `/stats` - Index statistics
- `/nollm` - Toggle LLM mode
- `/rebuild` - Rebuild index

### 2. HTTP API (`EVONY_RAG_API.bat`)

OpenAI-compatible API on `http://localhost:8766`:

```bash
# Chat completion (OpenAI-compatible)
curl http://localhost:8766/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "What is ACTION_KEY?"}]}'

# Direct RAG query
curl http://localhost:8766/query \
  -d '{"query": "army.newArmy parameters"}'

# Find files
curl http://localhost:8766/find \
  -d '{"query": "encryption", "top_k": 5}'
```

**LM Studio Integration:**
1. Run `EVONY_RAG_API.bat`
2. In LM Studio, set Custom API Base: `http://localhost:8766/v1`
3. Ask questions - RAG context is automatically injected

### 3. MCP Server (`EVONY_RAG_MCP.bat`)

For Windsurf IDE integration. Add to `~/.codeium/windsurf/mcp_config.json`:

```json
{
  "mcpServers": {
    "evony-knowledge": {
      "command": "python",
      "args": ["-m", "evony_rag.mcp_server"],
      "cwd": "c:\\Users\\Admin\\Downloads\\Evony_Decrypted"
    }
  }
}
```

**MCP Tools:**
- `evony_query` - Query with RAG and citations
- `evony_find_files` - Find relevant files
- `evony_get_file` - Get file contents
- `evony_stats` - Index statistics

## Safety Features

### Query Router
- Detects query intent (code_explain, protocol_info, exploit_info, etc.)
- Routes to appropriate categories
- Filters operational exploit requests

### Blocked Patterns
Operational requests like "step-by-step how to exploit" are blocked.
Educational explanations ("how does the overflow work") are allowed.

### Category Safety
```python
CATEGORIES = {
    "source_code": {"safe": True},
    "protocol": {"safe": True},
    "keys": {"safe": True},      # Educational
    "exploits": {"safe": False}, # Requires educational intent
}
```

## Knowledge Base

| Category | Files | Description |
|----------|-------|-------------|
| source_code | 7,469 | AS3/Python source |
| keys | 1,230 | Encryption keys |
| scripts | 106 | Bot scripts |
| protocol | 85 | Protocol docs |
| exploits | 26 | Glitch mechanics |

## Files

```
evony_rag/
├── __init__.py           # Package init
├── config.py             # Configuration
├── embeddings.py         # Vector index builder
├── query_router.py       # Query routing & safety
├── rag_engine.py         # Core RAG engine
├── mcp_server.py         # MCP server for Windsurf
├── lmstudio_api.py       # OpenAI-compatible API
├── cli.py                # Interactive CLI
└── requirements.txt      # Dependencies
```

## When to Fine-Tune

Fine-tuning is valuable *after* RAG when you want:
- Consistent Evony-specific vocabulary
- Better "house style" in responses
- Fewer retrieval calls for common questions

The curated training data (`Evony_Training_Data/`) is ready for LoRA fine-tuning when needed.
