# 🔍 RAG CAPABILITIES - 10 Things RAG Can Extract That You Can't

Complete extraction from 166,043 chunks demonstrating RAG's unique reverse engineering power.

---

## 1️⃣ FULL NETWORK SURFACE MAP

### What RAG Extracts
- **All URLs/domains/IPs**
- **API base paths, CDN paths, gateway hosts**
- **Environment switching (prod/test/dev)**
- **Fallback hosts, region routing**
- **Hardcoded ports, WebSocket endpoints, RTMP/AMF services**

### Extracted Data

```python
# From NCManager.as, Channel.as, URLUtil.as, MASTER_RESOURCE_INDEX.md
NETWORK_SURFACE = {
    # Game Servers
    "game_servers": {
        "cc2.evony.com": {"port": 443, "protocol": "TCP/AMF"},
        "cc3.evony.com": {"port": 443, "protocol": "TCP/AMF"},
        # ... more servers discovered via DNS enumeration
    },
    
    # Known Endpoints
    "endpoints": {
        "home": "http://www.evony.com",
        "user_services": "http://user.evony.com/index.do",
        "payment": "http://pay.evony.com",
        "api": "http://api.evony.com",
    },
    
    # RTMP fallback (from NCManager.as:946-962)
    "rtmp_fallback": {
        "enabled": True,
        "fallback_server": "rtmp://fallback.evony.com",
    },
    
    # Proxy support (from ProxySocket.as:31-42)
    "proxy": {
        "socks5_support": True,
        "domain_length_field": "ss5DomainLength",
    },
}
```

### Why It's Valuable
> **Gives you the "map" of where the client talks before you even sniff traffic.**

---

## 2️⃣ PROTOCOL & MESSAGE FORMAT FINGERPRINTS

### What RAG Extracts
- **Message serialization code (AMF0/AMF3, JSON, custom binary)**
- **Envelope fields (cmd/opcode, session, sequence, timestamps)**
- **Read/Write functions, byte order, length prefixes, compression flags**

### Extracted Data

```python
# From amf_codec.py, TESTING_SUITE_ARCHITECTURE.md, MISSING_TOOLS_REGISTRY.md
AMF3_TYPE_MARKERS = {
    0x00: 'UNDEFINED',
    0x01: 'NULL',
    0x02: 'FALSE',
    0x03: 'TRUE',
    0x04: 'INTEGER',
    0x05: 'DOUBLE',
    0x06: 'STRING',
    0x07: 'XML_DOC',
    0x08: 'DATE',
    0x09: 'ARRAY',
    0x0A: 'OBJECT',
    0x0B: 'XML',
    0x0C: 'BYTEARRAY',
    0x0D: 'VECTOR_INT',
    0x0E: 'VECTOR_UINT',
    0x0F: 'VECTOR_DOUBLE',
    0x10: 'VECTOR_OBJECT',
    0x11: 'DICTIONARY',
}

# Packet envelope (from evony_mega_toolkit.py:611-622)
PACKET_ENVELOPE = {
    "length_prefix": "4 bytes, big-endian uint32",
    "body_format": "AMF3 encoded",
    "fields": {
        "cmd": "string - command name",
        "params": "object - command parameters",
        "sessionKey": "string - session token",
    },
}

# From HTTPChannel.as:617-632
def decodePacket(event):
    """AMF packet decode from Connection.as"""
    raw = URLLoader(event.target).data
    # Parse AMF envelope...
```

### Query Example
> **"Show me how packets are encoded/decoded and where opcodes are assigned."**

---

## 3️⃣ COMMAND / OPCODE CATALOG WITH CALL SITES

### What RAG Extracts
- **Every command name/opcode + where it's sent from**
- **Parameters, required fields, defaults, constraints**
- **Response handlers tied to each command**

### Extracted Data (301+ Commands)

```python
# From master_suite.py, borg_toolkit.py, protocol_commands.py
COMMAND_CATALOG = {
    "army": {
        "newArmy": {
            "params": ["cityId", "heroId", "troops", "mission", "targetX", "targetY"],
            "risk": "HIGH",
            "call_site": "ArmyCommands.as:newArmy()",
            "response_handler": "ResponseDispatcher.ARMY_NEW_ARMY",
        },
        "callBackArmy": {
            "params": ["armyId", "cityId"],
            "risk": "LOW",
            "call_site": "ArmyCommands.as:callBackArmy()",
        },
    },
    "troop": {
        "produceTroop": {
            "params": ["cityId", "troopType", "num"],
            "constraints": {"num": "int32, overflow at threshold"},
            "risk": "CRITICAL - overflow exploit",
            "call_site": "TroopCommands.as:produceTroop()",
        },
        "cancelTroopProduce": {
            "params": ["cityId", "troopType"],
            "risk": "CRITICAL - refund exploit",
        },
    },
    # ... 301+ total commands
}

# Response handlers (from ResponseDispatcher.as:571+)
RESPONSE_HANDLERS = {
    "alliance.getAllianceArmyReport": "_resp_alliance_getAllianceArmyReport",
    "alliance.getAllianceEventList": "_resp_alliance_getAllianceEventList",
    "troop.cancelTroopProduce": "TROOP_CANCEL_TROOP_PRODUCE",
    "army.getStayAllianceArmys": "ARMY_GET_STAY_ALLIANCE_ARMYS",
}
```

### Query Example
> **"Generate complete command dictionary showing exact code paths."**

---

## 4️⃣ AUTHENTICATION & SESSION LIFECYCLE

### What RAG Extracts
- **Login flow, token/session keys, device identifiers**
- **Refresh/keepalive patterns, session renewal triggers**
- **"Invalid session" handling and re-auth behavior**

### Extracted Data

```python
# From auth_manager.py, PROTOCOL.md
SESSION_LIFECYCLE = {
    "login_flow": [
        "1. Hash password: MD5(password)",
        "2. Create login hash: MD5(username + pass_hash + 'evony')",
        "3. Send login request with email + loginHash",
        "4. Receive session token + player data",
    ],
    
    "token_types": {
        "SESSION": "Main session token",
        "REFRESH": "Token refresh token (secrets.token_hex(32))",
    },
    
    # From auth_manager.py:253-290
    "refresh_mechanism": {
        "method": "refresh_token(session_id, token_type)",
        "background_thread": True,
        "auto_refresh": "Before expiry",
    },
    
    # From PROTOCOL.md:225-240
    "keepalive": {
        "enabled": True,
        "interval": "periodic packets",
        "purpose": "maintain connection",
    },
    
    # Token generation (auth_manager.py:421-434)
    "token_generation": """
        token_data = f"{player_id}:{server_id}:{timestamp}:{random}"
        token_value = base64.b64encode(
            hashlib.sha256(token_data.encode()).digest()
        ).decode()
    """,
}
```

### Why It's Valuable
> **Explains what must be replicated (or safely mocked) in automation tooling.**

---

## 5️⃣ CRYPTOGRAPHY / SIGNING PIPELINE

### What RAG Extracts
- **HMAC/signature generation, request signing, secret handling**
- **AES/XXTEA/RC4-style routines, salt/IV logic**
- **Anti-tamper checks: checksum, integrity validation**

### Extracted Data

```python
# From ALL_ENCRYPTION_KEYS.py, hub_ultimate.py, exploit_engine.py
CRYPTO_PIPELINE = {
    "keys": {
        "ACTION_KEY": "TAO_{313-894*&*($*#-FDIU(430}-{facebook_dioe(&*%$l}",
        "ACTION_KEY_SL": "TAO_{313-894*&*($*#-FDIU(430}_SL",
        "USER_INFO_KEY": "IUGI_md5_key_{djfiji3*4930}-{fjdi3284$9dlld}",
        "API_KEY": "9f758e2deccbe6244f734371b9642eda",
        "XOR_KEY": 0xAA,
        "LOGIN_SALT": "evony",
        "GAME_KEY": "EvonyGameKey2009",
    },
    
    # Signature functions (hub_ultimate.py:681-692)
    "signature_functions": {
        "generate_signature": "MD5(data + ACTION_KEY)",
        "api_signature": "MD5(data + API_KEY)",
        "user_info_signature": "MD5(server + fbid + USER_INFO_KEY)",
        "xor_encrypt": "bytes(b ^ XOR_KEY for b in data)",
        "login_hash": "MD5(username + MD5(password) + LOGIN_SALT)",
    },
    
    # Extended signature (ALL_ENCRYPTION_KEYS.py:136-152)
    "extended_action_signature": {
        "inputs": ["action", "sex", "datetime", "username", "server_id", "speed_type", "pfid"],
        "formula": "MD5(concat(inputs) + ACTION_KEY_SL)",
    },
}
```

### Query Example
> **"Where is the request signature computed and what inputs does it use?"**

---

## 6️⃣ STATE MACHINE OF THE CLIENT

### What RAG Extracts
- **Event-driven flow: UI click → controller → network call → state update**
- **Model objects (city, troop, building, research) and update pipelines**
- **Background loops: timers, polling, push handlers**

### Extracted Data

```actionscript
// From Context.as, CastlePercent.as, Cities.as, GuideStep.as

// State update flow (Context.as:381-392)
function onBuildComplete():void {
    trace("Context.onBuildComplete():castleId=" + castleId);
    // Update buildingBean in Array
    Context.getBuildingArray()[arrayId] = buildingBean;
}

// Property change dispatch (CastlePercent.as:118-132)
public function set city(value:Object):void {
    var oldValue:Object = this._city;
    if (oldValue !== value) {
        this._city = value;
        dispatchEvent(PropertyChangeEvent.createUpdateEvent(
            this, "city", oldValue, value
        ));
    }
}

// Integrated state manager (exploits/advanced-exploit-system.md:145-164)
public class IntegratedStateManager {
    private var _cityStates:Object = {};
    private var _exploitStates:Object = {};
    
    public function validateState(cityId:int):Boolean {
        // State validation logic
    }
}
```

### Why It's Valuable
> **Converts spaghetti into an understandable "action graph" (great for bot design).**

---

## 7️⃣ RATE LIMITS, COOLDOWNS, ANTI-ABUSE RULES

### What RAG Extracts
- **Client-side throttles, cooldown timers, "too fast" guards**
- **Retry logic, exponential backoff, error-specific fallback**
- **"Humanization" code patterns (delays, jitter)**

### Extracted Data

```python
# From NPC_FARMING.md, anti_cheat.py, AI_AUTOMATION_MASTER_PLAN.md
RATE_LIMITS = {
    # Attack cooldowns (NPC_FARMING.md:358-376)
    "attack_cooldowns": {
        "per_city": "5 attacks per 5 minutes",
        "per_npc": "1 attack per 5 minutes (respawn time)",
        "server_limit": "100 requests per minute",
    },
    
    # Anti-cheat system (anti_cheat.py:210-233)
    "anti_cheat": {
        "burst_detection": True,
        "cooldown_after_burst_ms": "configurable",
        "action_history_tracking": True,
    },
    
    # Rate limit check (AI_AUTOMATION_MASTER_PLAN.md:637-650)
    "rate_limit_check": """
        def _check_rate_limit(self) -> bool:
            current_minute = int(time.time() / 60)
            if current_minute != self.last_minute:
                self.actions_this_minute = 0
                self.last_minute = current_minute
            return self.actions_this_minute < MAX_ACTIONS_PER_MINUTE
    """,
    
    # Bot detection avoidance
    "humanization": {
        "random_delays": True,
        "jitter": "0.5-2.0 seconds",
        "action_variance": True,
    },
}
```

### Why It's Valuable
> **Understand expected pacing and where detection triggers may exist.**

---

## 8️⃣ ERROR CODES & SERVER RESPONSE SEMANTICS

### What RAG Extracts
- **Enumerations/constants for error codes and meanings**
- **Branch logic for "ban/flag", "captcha", "invalid request"**
- **Recovery sequences tied to specific errors**

### Extracted Data

```actionscript
// From Channel_1.as:898-912, ResponseDispatcher.as

// Error handling (Channel_1.as)
override protected function statusHandler(message:IMessage):void {
    var errorMsg:ErrorMessage;
    var faultEvent:ChannelFaultEvent;
    var cmdMsg:CommandMessage = CommandMessage(message);
    
    // Handle different error types
    switch(errorMsg.faultCode) {
        case "invalid_session":
            // Trigger re-auth
            break;
        case "rate_limited":
            // Apply backoff
            break;
        case "banned":
            // Show ban message
            break;
    }
}

// Response dispatch map (ResponseDispatcher.as:571+)
respMap["alliance.getAllianceArmyReport"] = _resp_alliance_getAllianceArmyReport;
respMap["alliance.getAllianceEventList"] = _resp_alliance_getAllianceEventList;
// ... maps all responses to handlers
```

### Query Example
> **"What does error 1234 mean and what does the client do next?"**

---

## 9️⃣ EMBEDDED SCRIPTING / AUTOMATION HOOKS

### What RAG Extracts
- **Scripting languages (rule tables, JSON scripts)**
- **Macro systems, action queues, task runner structures**
- **AutoEvony patterns that mirror client calls**

### Extracted Data

```python
# From BOT_SCRIPTING.md, AI_AUTOMATION_MASTER_PLAN.md, scout.py

# AutoEvony script operators (BOT_SCRIPTING.md:111-134)
SCRIPT_OPERATORS = {
    ">": "Greater than",
    "<": "Less than",
    "==": "Equal to",
    "!=": "Not equal",
    ">=": "Greater or equal",
    "<=": "Less or equal",
}

# Automation task structure (AI_AUTOMATION_MASTER_PLAN.md:565-578)
@dataclass
class AutomationTask:
    id: str
    name: str
    priority: TaskPriority
    action: str
    parameters: Dict[str, Any]
    conditions: Dict[str, Any] = None
    max_retries: int = 3
    cooldown_seconds: float = 0

# ActionFactory integration (scout.py:1-15)
from actionfactory.builder import *
from actionfactory.quest import *
from actionfactory.items import *

# Command structure (MISSING_TOOLS_REGISTRY.md:325-344)
COMMANDS = {
    "train_troops": {
        "params": ["cityId", "troopType", "count"],
        "types": [int, str, int],
        "description": "Train troops in specified city",
    },
}
```

### Why It's Valuable
> **Builds a "bot primitive set" from real call patterns.**

---

## 🔟 DATA MODEL: IDs, TABLES, HIDDEN RULES

### What RAG Extracts
- **Constant tables: item IDs, building IDs, troop IDs, research IDs**
- **Hidden rule curves: cost formulas, time formulas, requirements**
- **Localization strings revealing feature flags or hidden endpoints**

### Extracted Data

```python
# From PROTOCOL.md, exploits.py, game_logic.py, TROOP_DATA.md

TROOP_DATA = {
    # ID | Name | Food Cost | Overflow Threshold
    1: {"name": "Worker", "food": 50, "threshold": 42949673},
    2: {"name": "Warrior", "food": 75, "threshold": 28633116},
    3: {"name": "Scout", "food": 150, "threshold": 14316558},
    4: {"name": "Pikeman", "food": 200, "threshold": 10737419},
    5: {"name": "Swordsman", "food": 250, "threshold": 8589935},
    6: {"name": "Archer", "food": 350, "threshold": 6135037},
    7: {"name": "Cavalry", "food": 800, "threshold": 2684355},
    8: {"name": "Cataphract", "food": 1500, "threshold": 1431656},
    9: {"name": "Transporter", "food": 500, "threshold": 4294968},
    10: {"name": "Ballista", "food": 2500, "threshold": 858994},
    11: {"name": "Ram", "food": 4000, "threshold": 536871},
    12: {"name": "Catapult", "food": 6000, "threshold": 357914},
}

# Training times (game_logic.py:589-602)
TROOP_STATS = {
    "worker": {"attack": 5, "defense": 5, "life": 50, "speed": 180, "train_time": 15},
    "warrior": {"attack": 10, "defense": 10, "life": 100, "speed": 200, "train_time": 30},
    # ...
}

# Building IDs
BUILDING_IDS = {
    1: "Town Hall", 2: "Barracks", 3: "Cottage", 4: "Workshop",
    5: "Academy", 6: "Forge", 7: "Market", 8: "Warehouse",
    9: "Embassy", 10: "Rally Point", 11: "Feasting Hall",
    12: "Beacon Tower", 13: "Inn", 14: "Walls",
}
```

### Query Example
> **"What command upgrades building X and what params does it need?"**

---

## 🎯 TOP 3 HIGHEST IMPACT RAG TASKS

| Rank | Task | Why |
|------|------|-----|
| 1 | **Opcode/command catalog + params + handlers** | Lets you send ANY command |
| 2 | **Auth/session/signing pipeline** | Required for ALL requests |
| 3 | **Serialize/deserialize + envelope format** | Understand ALL traffic |

> **These three let you reason about almost everything else.**

---

## 🔧 IDEAL RAG INDEXING STRUCTURE

For best results, RAG should extract **structured artifacts**, not just text:

```python
# Entity types to index
ENTITY_TYPES = {
    "network_send": "Function that sends network request",
    "opcode_constant": "Command/opcode with references",
    "signature_function": "Inputs/outputs + call graph edges",
    "response_handler": "Handler tied to command response",
    "state_update": "Model update function",
    "rate_limit": "Throttle/cooldown configuration",
}

# Query examples
QUERIES = [
    "Show all network sends and the opcode used",
    "Trace login() through to first authenticated request",
    "Find all places that compute or validate request signatures",
    "What error codes trigger session refresh?",
    "List all troop commands with overflow-vulnerable parameters",
]
```

---

## 📊 RAG STATS

| Metric | Value |
|--------|-------|
| **Total Chunks** | 166,043 |
| **Total Symbols** | 55,871 |
| **Commands Indexed** | 301+ |
| **Source Files** | 7,469 AS + 16MB scripts |
| **Keys Extracted** | 7 primary + 5 static |
| **Exploits Documented** | 12+ vectors |

---

*Extracted via Svony MCP RAG: Hybrid lexical + semantic search across 166k chunks*
