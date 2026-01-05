# Svony Documentation

Comprehensive documentation for Evony reverse engineering and the Svony MCP server.

## Contents

### 📁 [keys/](keys/)
- **[ENCRYPTION_KEYS.md](keys/ENCRYPTION_KEYS.md)** - All encryption keys, signatures, and usage

### 📁 [protocols/](protocols/)
- **[COMMANDS.md](protocols/COMMANDS.md)** - Complete protocol command reference (301+ commands)
- **[AMF_PROTOCOL.md](protocols/AMF_PROTOCOL.md)** - AMF3 serialization format and packet structure

### 📁 [exploits/](exploits/)
- **[EXPLOITS.md](exploits/EXPLOITS.md)** - Documented vulnerabilities and exploit techniques

### 📁 [diagrams/](diagrams/)
- **[ARCHITECTURE.md](diagrams/ARCHITECTURE.md)** - System architecture and flow diagrams

## Quick Reference

### Encryption Keys
| Key | Purpose |
|-----|---------|
| ACTION_KEY | Command signatures |
| USER_INFO_KEY | Player lookup |
| API_KEY | API authentication |
| XOR_KEY | Data obfuscation |

### Overflow Thresholds
| Troop | Threshold |
|-------|-----------|
| Archer | 6,135,037 |
| Worker | 42,949,673 |
| Catapult | 715,828 |

### MCP Tools
| Tool | Description |
|------|-------------|
| `evony_search` | Hybrid search (166k chunks) |
| `evony_stats` | Index statistics |
| `evony_mode` | Query mode control |

## Data Sources

- **166,043 chunks** - Indexed content
- **55,871 symbols** - Code symbols
- **301+ commands** - Protocol commands
- **36 command classes** - Extracted from SWF

## Contributing

1. Search for relevant content: `evony_search("topic")`
2. Document findings in appropriate folder
3. Update this README
4. Commit and push

## License

MIT - Educational and research purposes only.
