# 📚 ECMAScript/ActionScript Documentation

Complete reverse engineering documentation for Evony Client ActionScript codebase.

---

## 📁 Contents

| File | Description |
|------|-------------|
| [ECMASCRIPT_BUGS.md](ECMASCRIPT_BUGS.md) | Complete bug catalog with 59 identified issues |
| [BUG_FLOW_DIAGRAM.svg](BUG_FLOW_DIAGRAM.svg) | Visual bug flow and fix diagram |
| [ACTIONSCRIPT_CLASSES.md](ACTIONSCRIPT_CLASSES.md) | Class index with bug annotations |
| [FIX_PATTERNS.md](FIX_PATTERNS.md) | Standardized fix patterns for common bugs |
| [ECMASCRIPT_EXTRACTION.md](ECMASCRIPT_EXTRACTION.md) | Extraction methodology for patch-ready slices |
| [WORK_PACKETS.md](WORK_PACKETS.md) | 5 work packets with patches and tests |
| [EXTRACTION_FLOW.svg](EXTRACTION_FLOW.svg) | Visual extraction pipeline diagram |

---

## 🎯 Key Findings

### Critical Vulnerabilities (P0)
1. **Integer Overflow** - Troop counts can wrap around at INT32_MAX
2. **Race Conditions** - Castle switching not atomic
3. **TOCTOU Bugs** - Time-of-check-time-of-use in message dispatch

### Exploitable Bugs
- Train 2,147,483,647 archers → overflow → massive troop count
- Rapid city switch during action → wrong city affected
- Timer manipulation → resource calculation exploits

### Code Quality Issues
- 15+ event listeners never removed (memory leaks)
- Infinite timer without stop mechanism
- 100+ line methods without error handling
- Typos in class names (`MsgDispacther`, `BUILD_COMPLATE`)

---

## 📊 Bug Statistics

```
Category            Count   Severity
─────────────────────────────────────
Integer Overflow       8    🔴 Critical
Race Conditions        5    🔴 Critical
Null References       12    🟡 Medium
Type Coercion          6    🟡 Medium
Missing Validation    15    🟡 Medium
Memory Leaks           4    🟠 High
Error Handling         9    🟡 Medium
─────────────────────────────────────
TOTAL                 59
```

---

## 🔍 Source Files Analyzed

### Core (`com/evony/`)
- `Context.as` - 1,329 lines - Global state
- `SenderImpl.as` - 46 lines - Message sending
- `MsgDispacther.as` - 67 lines - Event dispatch
- `GameConfig.as` - Configuration
- `PreContext.as` - Pre-login context
- `Coordinate.as` - Map coordinates

### Network (`com/evony/net/`)
- `GameClient.as` - Main network client
- `ResponseDispatcher.as` - Response routing

### Data Beans (`com/evony/common/beans/`)
- `CastleBean.as` - Castle data
- `TroopBean.as` - Troop counts
- `PlayerBean.as` - Player data
- `BuildingBean.as` - Building data
- `HeroBean.as` - Hero data
- `ItemBean.as` - Item data
- `FieldBean.as` - Map field data

### Views (`view/`)
- `MainWin.as` - Main window
- `castle/TownView.as` - Inner city
- `castle/CityView.as` - Outer city
- `ChatFrame.as` - Chat panel

---

## 🛠️ Tools Used

| Tool | Purpose |
|------|---------|
| AS3 Sorcerer | SWF decompilation |
| FFDec | Alternative decompiler |
| RABCDAsm | ABC bytecode analysis |
| Svony RAG | Code search and analysis |

---

## 🔗 Related Documentation

- [EXPLOITS.md](../exploits/EXPLOITS.md) - Full exploit documentation
- [COMMANDS.md](../protocols/COMMANDS.md) - Protocol commands
- [AMF_PROTOCOL.md](../protocols/AMF_PROTOCOL.md) - AMF serialization
- [MASTER_REFERENCE.md](../MASTER_REFERENCE.md) - Complete reference

---

*Part of Svony MCP - Evony Reverse Engineering Project*
