# Tools & Utilities Index

Organized collection of reverse engineering tools by function.

## 🔧 Tool Categories

### 📦 AMF/Protocol Tools

| Tool | Purpose | Language |
|------|---------|----------|
| `PyAMF` | AMF serialization | Python |
| `Py3AMF` | Python 3 AMF | Python |
| `amf3.py` | AMF3 codec | Python |
| `FluorineFx` | .NET AMF library | C# |

**Usage Example:**
```python
from pyamf import amf3

# Decode AMF packet
decoder = amf3.Decoder(packet_data)
obj = decoder.readElement()

# Encode AMF packet
encoder = amf3.Encoder()
encoder.writeElement({"cmd": "army.newArmy", "params": {...}})
```

---

### 🔍 Flash Decompilers

| Tool | Purpose | Features |
|------|---------|----------|
| JPEXS FFDec | SWF decompiler | AS3, shapes, scripts |
| RABCDAsm | ABC assembler | Low-level bytecode |
| AS3 Sorcerer | AS3 decompiler | Clean output |

**FFDec Commands:**
```bash
# Export all scripts
ffdec -export script ./output game.swf

# Export specific class
ffdec -export script -class com.evony.GameClient ./output game.swf

# Deobfuscate
ffdec -deobfuscate game.swf output.swf
```

---

### 🌐 Network Analysis

| Tool | Purpose | Protocol |
|------|---------|----------|
| Wireshark | Packet capture | AMF/HTTP |
| Fiddler | HTTP proxy | AMF |
| Charles | HTTP proxy | SSL/AMF |

**Wireshark Filter:**
```
# Capture AMF traffic
http.content_type contains "amf"

# Game server traffic
tcp.port == 443 and ip.dst == game.evony.com
```

---

### 🔐 Encryption Tools

| Tool | Purpose | Algorithm |
|------|---------|-----------|
| `hashlib` | MD5 signatures | MD5 |
| `xor_tool.py` | XOR encryption | XOR 0xAA |

**Signature Generation:**
```python
import hashlib

ACTION_KEY = "TAO_{313-894*&*($*#-FDIU(430}-{facebook_dioe(&*%$l}"

def generate_signature(data: str) -> str:
    return hashlib.md5((data + ACTION_KEY).encode()).hexdigest()
```

---

### 🤖 Automation Bots

| Tool | Version | Features |
|------|---------|----------|
| AutoEvony | 2.x | Full automation |
| RoboEvony | 1.41 | GUI + scripts |

**Bot Integration:**
```python
# Connect to bot API
import socket
sock = socket.socket()
sock.connect(("localhost", 8088))

# Send command
sock.send(b"troop a:1000\n")
response = sock.recv(1024)
```

---

### 📊 Analysis Tools

| Tool | Purpose | Output |
|------|---------|--------|
| `exploit_engine.py` | Overflow calculator | Thresholds |
| `protocol_analyzer.py` | Command parser | Decoded packets |
| `symbol_extractor.py` | Symbol index | 55k symbols |

**Overflow Calculator:**
```python
def calculate_overflow(cost: int, quantity: int) -> dict:
    INT32_MAX = 2147483647
    raw = cost * quantity
    wrapped = raw & 0xFFFFFFFF
    if wrapped > INT32_MAX:
        wrapped -= 0x100000000
    return {
        "overflow": raw > INT32_MAX,
        "wrapped": wrapped,
        "exploit_viable": wrapped < 0
    }

# Example: Archers (cost=350)
result = calculate_overflow(350, 6135037)
# {'overflow': True, 'wrapped': -2147704346, 'exploit_viable': True}
```

---

## 🏗️ Toolkit Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            SVONY TOOLKIT STACK                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │
│   │   FFDec     │  │  Wireshark  │  │   PyAMF     │  │  RoboEvony  │       │
│   │ Decompiler  │  │  Capture    │  │   Codec     │  │    Bot      │       │
│   └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘       │
│          │                │                │                │              │
│          └────────────────┴────────────────┴────────────────┘              │
│                                    │                                        │
│                                    ▼                                        │
│                         ┌─────────────────────┐                            │
│                         │   SVONY MCP SERVER  │                            │
│                         │   (RAG + Search)    │                            │
│                         └─────────────────────┘                            │
│                                    │                                        │
│                                    ▼                                        │
│                         ┌─────────────────────┐                            │
│                         │   KNOWLEDGE BASE    │                            │
│                         │   166k chunks       │                            │
│                         └─────────────────────┘                            │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 📋 Quick Reference

### File Locations
| Type | Path |
|------|------|
| Source Code | `source_code/*.py`, `*.as` |
| Scripts | `scripts/*.txt` |
| Protocol Docs | `protocol/*.md` |
| Keys | `keys/*.md` |

### Common Operations

```bash
# Search for encryption
evony_search("ACTION_KEY MD5 signature")

# Find protocol commands
evony_search("army.newArmy protocol parameters")

# Research exploits
evony_search("integer overflow threshold")

# Analyze AMF
evony_search("AMF3 serialize deserialize packet")
```
