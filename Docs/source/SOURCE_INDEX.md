# Source Code Index by Use Case

Organized index of source code files categorized by functionality.

## 📁 Categories

### 🔐 Encryption & Security
Files related to encryption keys, signatures, and security.

| File | Purpose | Key Functions |
|------|---------|---------------|
| `ALL_ENCRYPTION_KEYS.py` | Master key reference | All keys consolidated |
| `hub_ultimate.py` | Signature generation | `generate_signature()` |
| `exploit_engine.py` | Security analysis | `generate_signature()` |
| `mega_toolkit.py` | Key extraction | `ENCRYPTION_KEYS` dict |

**Key Snippets:**
```python
ACTION_KEY = "TAO_{313-894*&*($*#-FDIU(430}-{facebook_dioe(&*%$l}"
USER_INFO_KEY = "IUGI_md5_key_{djfiji3*4930}-{fjdi3284$9dlld}"
API_KEY = "9f758e2deccbe6244f734371b9642eda"
```

---

### 📡 Protocol & Commands
Files implementing game protocol and commands.

| File | Purpose | Commands |
|------|---------|----------|
| `borg_toolkit.py` | 301+ commands | All categories |
| `protocol_commands.py` | Command registry | `get_all_commands()` |
| `SenderImpl.as` | Packet sender | Network layer |
| `GameClient.as` | Game connection | Session management |

**Command Categories:**
- Army (newArmy, attack, scout)
- Troop (produce, cancel, disband)
- Building (new, upgrade, destroy)
- Hero (fire, promote, addAttr)
- Resource (tax, comfort, collect)

---

### 📦 AMF Serialization
Files handling AMF protocol encoding/decoding.

| File | Purpose | Format |
|------|---------|--------|
| `amf3.py` | AMF3 codec | Binary |
| `amf3_2.py` | AMF3 types | Constants |
| `amf0_2.py` | AMF0 codec | Legacy |
| `SerializationFilter.as` | AS3 serializer | Object mapping |

**AMF Type Markers:**
```python
TYPE_UNDEFINED = 0x00
TYPE_NULL = 0x01
TYPE_FALSE = 0x02
TYPE_TRUE = 0x03
TYPE_INTEGER = 0x04
TYPE_DOUBLE = 0x05
TYPE_STRING = 0x06
TYPE_OBJECT = 0x0A
```

---

### 💥 Exploits & Vulnerabilities
Files documenting and implementing exploits.

| File | Purpose | Exploit Type |
|------|---------|--------------|
| `exploits.py` | Exploit library | Multiple |
| `glitch_calculator.py` | Overflow calc | Integer overflow |
| `mega_toolkit.py` | Overflow script | Troop glitch |

**Overflow Thresholds:**
```python
THRESHOLDS = {
    "archer": 6135037,      # 350 food
    "worker": 42949673,     # 50 food
    "catapult": 715828,     # 3000 food
    "cavalry": 4294968,     # 500 food
}
```

---

### 🤖 Automation & Bots
Files for bot integration and automation.

| File | Purpose | Bot Type |
|------|---------|----------|
| `automation.py` | Full automation | Generic |
| `scheduler.py` | Task scheduling | Cron-like |
| `watcher.py` | File monitoring | Hot reload |
| `server.py` | Script server | AutoEvony |

**Script Server Port:** 8088
```python
# AutoEvony integration
includeurl http://localhost:8088/epic/overflow_chain
```

---

### 🖥️ GUI & Interface
Files implementing user interfaces.

| File | Purpose | Framework |
|------|---------|-----------|
| `gui.py` | Main GUI | Tkinter |
| `hub_ultimate.py` | Ultimate toolkit | Tkinter |
| `evony_mega_toolkit.py` | Mega toolkit | Tkinter |

**GUI Features:**
- Multi-city tabs
- Troop management
- Resource monitoring
- Script editor

---

### 🔍 Analysis & Extraction
Files for data extraction and analysis.

| File | Purpose | Output |
|------|---------|--------|
| `extractor.py` | Data extractor | JSON |
| `complete_extraction.py` | Full extraction | All data |
| `symbol_extractor.py` | Symbol index | 55k symbols |

---

## 📊 File Statistics

| Category | Files | Lines | Purpose |
|----------|-------|-------|---------|
| Source Code | 7,469 | ~500k | ActionScript, Python |
| Protocol | 85 | ~15k | Documentation |
| Scripts | 106 | ~8k | AutoEvony/RoboEvony |
| Keys | 1,230 | ~50k | Config, JSON |
| Exploits | 26 | ~5k | Vulnerability docs |

---

## 🔎 Search by Use Case

### "I want to understand the protocol"
```
evony_search("protocol command structure AMF")
evony_search("packet serialization format")
```

### "I want to find encryption keys"
```
evony_search("ACTION_KEY USER_INFO_KEY API_KEY")
evony_search("MD5 signature generation")
```

### "I want to find exploits"
```
evony_search("integer overflow threshold")
evony_search("race condition exploit")
```

### "I want to automate tasks"
```
evony_search("AutoEvony script syntax")
evony_search("bot automation farming")
```

### "I want to analyze network traffic"
```
evony_search("AMF3 deserialize packet")
evony_search("Wireshark filter game traffic")
```

---

## 🗂️ Directory Structure

```
source_code/
├── 📂 ActionScript/           # Decompiled AS3
│   ├── com/evony/             # Core game classes
│   ├── com/evony/client/      # Client implementations
│   └── com/evony/net/         # Network layer
│
├── 📂 Python/                 # Python tools
│   ├── amf*.py                # AMF codecs
│   ├── *_toolkit.py           # Toolkits
│   └── exploit*.py            # Exploit tools
│
└── 📂 Scripts/                # Bot scripts
    ├── *.txt                  # AutoEvony scripts
    └── *.docx                 # Documentation
```
