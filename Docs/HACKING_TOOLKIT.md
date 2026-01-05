# 🔓 SVONY HACKING TOOLKIT

Complete reverse engineering reference for Evony exploitation.

---

## 📊 RAG Index Summary

| Category | Items | Key Files |
|----------|-------|-----------|
| **Chunks** | 166,043 | All indexed content |
| **Symbols** | 55,871 | Functions, classes, vars |
| **Commands** | 301+ | Protocol commands |
| **AS Classes** | 7,469 | ActionScript source |
| **Scripts** | 106 | AutoEvony/RoboEvony |

---

## 🏗️ Client Architecture (EvonyClient1921.swf)

### Core Classes Discovered

```
com.evony/
├── ActionFactory.as          # Command factory - ALL commands registered here
│   ├── ArmyCommands          # Army operations
│   ├── TroopCommands         # Troop training
│   ├── CastleCommands        # Building operations
│   ├── HeroCommand           # Hero management
│   ├── InteriorCommands      # City interior
│   ├── MailCommands          # Mail system
│   ├── AllianceCommands      # Alliance ops
│   ├── FriendCommands        # Social features
│   ├── RankCommands          # Rankings
│   └── TechCommands          # Research
│
├── net/
│   ├── GameClient.as         # Main network client
│   ├── SocketHandler.as      # Raw socket handling
│   └── Sender.as             # Message sending
│
├── SenderImpl.as             # Sender implementation
│
└── eum/
    └── TroopEumDefine.as     # Troop type definitions
```

### ActionFactory Command Registration
```actionscript
// From ActionFactory.as - ALL commands initialized here
private var armyCommands:ArmyCommands;
private var troopCommands:TroopCommands;
private var castleCommands:CastleCommands;
private var heroCommand:HeroCommand;
private var interiorCommands:InteriorCommands;
private var mailCommands:MailCommands;
private var allianceCommands:AllianceCommands;
private var modifyCommands:ModifyCommands;
private var techCommands:TechCommands;
private var rankCommands:RankCommands;
private var friendCommands:FriendCommands;
private var furloughCommands:FurloughCommands;
private var gamblingRankingCommands:GamblingRankingCommands;
private var equipmenttechCommands:EquipmenttechCommands;
private var castleSignCommand:CastleSignCommand;
private var commissionQuestCommands:CommissionQuestCommands;
```

---

## 📡 Protocol Implementation

### Connection Flow
```
1. Connect to game server IP:443 (RAW TCP, no SSL)
2. Send "gameClient" identification string
3. Server responds with AMF handshake
4. Exchange AMF3 messages for all commands
```

### GameClient.as Key Properties
```actionscript
private var amfObj:Object;
private var processedCount:int;
private var serverPort:int;
private var lock:Boolean = false;
private var readed:int = 0;
```

### Sender Pattern
```actionscript
// From ArmyCommands.as
public function newArmy(_arg_1:NewArmyParam, _arg_2:Function=null):CommandResponse {
    this._newArmy_callback = _arg_2;
    if (this.sender != null) {
        sender.sendMessage("army.newArmy", _arg_1);
    }
    return null;
}

public function callBackArmy(_arg_1:int, _arg_2:int, _arg_3:Function=null):CommandResponse {
    this._callBackArmy_callback = _arg_3;
    if (this.sender != null) {
        sender.sendMessage("army.callBackArmy", {"armyId": _arg_1, ...});
    }
    return null;
}
```

---

## 🔐 Encryption Keys (Extracted)

```python
# From ALL_ENCRYPTION_KEYS.py

# Primary Action Key - Signs ALL commands
ACTION_KEY = "TAO_{313-894*&*($*#-FDIU(430}-{facebook_dioe(&*%$l}"

# Secondary Action Key  
ACTION_KEY_SL = "TAO_{313-894*&*($*#-FDIU(430}_SL"

# User Info Lookup Key
USER_INFO_KEY = "IUGI_md5_key_{djfiji3*4930}-{fjdi3284$9dlld}"

# API Key
API_KEY = "9f758e2deccbe6244f734371b9642eda"

# XOR Key for data obfuscation
XOR_KEY = 0xAA  # 170 decimal

# Login Salt
LOGIN_SALT = "evony"
```

### Signature Generation
```python
import hashlib

def generate_signature(data: str, key: str = ACTION_KEY) -> str:
    """Generate MD5 command signature"""
    return hashlib.md5((data + key).encode()).hexdigest()

def api_signature(data: str) -> str:
    """API request signature"""
    return hashlib.md5((data + API_KEY).encode()).hexdigest()

def user_info_signature(server: str, fbid: str) -> str:
    """User lookup signature"""
    return hashlib.md5((server + fbid + USER_INFO_KEY).encode()).hexdigest()
```

---

## 💥 Exploit Reference

### Integer Overflow (Troop Glitch)

```python
# Overflow Calculator
INT32_MAX = 2147483647

def calculate_threshold(troop_cost: int) -> int:
    """Calculate overflow threshold for troop type"""
    return (INT32_MAX // troop_cost) + 1

THRESHOLDS = {
    "worker":     calculate_threshold(50),    # 42,949,673
    "warrior":    calculate_threshold(100),   # 21,474,837
    "scout":      calculate_threshold(150),   # 14,316,558
    "pikeman":    calculate_threshold(200),   # 10,737,419
    "swordsman":  calculate_threshold(250),   # 8,589,935
    "archer":     calculate_threshold(350),   # 6,135,037
    "cavalry":    calculate_threshold(500),   # 4,294,968
    "cataphract": calculate_threshold(700),   # 3,067,834
    "transporter":calculate_threshold(300),   # 7,158,279
    "ballista":   calculate_threshold(1000),  # 2,147,484
    "ram":        calculate_threshold(1500),  # 1,431,656
    "catapult":   calculate_threshold(3000),  # 715,828
}

def exploit_overflow(troop_type: str, quantity: int) -> dict:
    """Calculate exploit result"""
    cost = {"archer": 350, "worker": 50, ...}[troop_type]
    raw = cost * quantity
    wrapped = raw & 0xFFFFFFFF
    if wrapped > INT32_MAX:
        wrapped -= 0x100000000
    return {
        "overflow": raw > INT32_MAX,
        "wrapped": wrapped,
        "gain": abs(wrapped) if wrapped < 0 else 0
    }
```

### Exploit Script (AutoEvony)
```
; OVERFLOW EXPLOIT SCRIPT
; Train archers at threshold to trigger overflow

set threshold 6135037
troop a:%threshold%
wait 2
cancel a
; Resources gained from overflow + refund
```

---

## 🤖 AutoEvony Script System

### ScriptCmd.as Structure
```actionscript
// From ScriptCmd_1.as
public class ScriptCmd {
    private var cmdName:String;
    private var cmdFunc:Function;
    private var params:Array;
    private var paramTypes:Array;
    private var nParamsRequired:int;
    
    public function ScriptCmd(name:String, func:Function, params:Array, ...) {
        this.cmdName = name;
        this.cmdFunc = func;
        this.params = params;
        // ...
    }
}
```

### Script.as Variable System
```actionscript
// From Script_1.as
// Variable substitution
param2 = this.subVarValues(param2, this.m_scriptVars);

// Array variable syntax: $("val1", "val2", "val3")
var _loc3_:Array = param2.substring(2).slice(0,-2).split(String("\", \""));
this.m_scriptVars[param1] = _loc3_;
```

### Script Commands Reference

| Command | Syntax | Description |
|---------|--------|-------------|
| `troop` | `troop a:1000` | Train troops |
| `build` | `build be:5:1` | Build structure |
| `research` | `research ar:5` | Research tech |
| `attack` | `attack x:y` | Attack coords |
| `scout` | `scout x:y` | Scout target |
| `farm` | `farm npc:5` | Farm NPCs |
| `wait` | `wait 5` | Wait seconds |
| `set` | `set var value` | Set variable |
| `if` | `if (condition)` | Conditional |
| `loop` | `loop 10` | Loop N times |
| `goto` | `goto label` | Jump to label |
| `label` | `label name` | Define label |

### Troop Abbreviations
| Abbr | Troop | Abbr | Troop |
|------|-------|------|-------|
| `wo` | Worker | `c` | Cavalry |
| `w` | Warrior | `ca` | Cataphract |
| `s` | Scout | `t` | Transporter |
| `p` | Pikeman | `ba` | Ballista |
| `sw` | Swordsman | `r` | Ram |
| `a` | Archer | `cat` | Catapult |

---

## 🔧 Python Client Implementation

```python
import socket
import struct
import pyamf
from pyamf import amf3

class EvonyClient:
    """Evony game client using AMF protocol"""
    
    def __init__(self, server: str = 'cc2'):
        self.server = server
        self.host = f"{server}.evony.com"
        self.port = 443
        self.sock = None
        self.session_key = None
        
    def connect(self):
        """Connect to game server"""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(30)
        self.sock.connect((self.host, self.port))
        # Send identification
        self.sock.send(b"gameClient\x00")
        
    def send_command(self, cmd: str, params: dict) -> dict:
        """Send AMF command"""
        # Build command object
        data = {
            "cmd": cmd,
            "params": params,
            "sessionKey": self.session_key,
        }
        # Add signature
        sig_data = cmd + str(sorted(params.items()))
        data["signature"] = generate_signature(sig_data)
        
        # Encode AMF
        encoder = amf3.Encoder()
        encoder.writeElement(data)
        encoded = encoder.stream.getvalue()
        
        # Send with length prefix
        packet = struct.pack('>L', len(encoded)) + encoded
        self.sock.sendall(packet)
        
        # Receive response
        return self.receive()
        
    def receive(self) -> dict:
        """Receive AMF response"""
        # Read length
        size_data = self.sock.recv(4)
        size = struct.unpack('>L', size_data)[0]
        
        # Read body
        body = b''
        while len(body) < size:
            body += self.sock.recv(size - len(body))
            
        # Decode AMF
        decoder = amf3.Decoder(body)
        return decoder.readElement()
        
    def train_troops(self, city_id: int, troop_type: int, count: int):
        """Train troops"""
        return self.send_command("troop.produceTroop", {
            "cityId": city_id,
            "troopType": troop_type,
            "num": count
        })
        
    def new_army(self, city_id: int, hero_id: int, troops: list):
        """Create new army"""
        return self.send_command("army.newArmy", {
            "cityId": city_id,
            "heroId": hero_id,
            "troops": troops
        })
```

---

## 📋 Command Reference (Key Commands)

### Army Commands (ArmyCommands.as)
| Method | Server Command | Parameters |
|--------|---------------|------------|
| `newArmy` | `army.newArmy` | cityId, heroId, troops[] |
| `callBackArmy` | `army.callBackArmy` | armyId, cityId |
| `disbandArmy` | `army.disbandArmy` | armyId |
| `exerciseArmy` | `army.exerciseArmy` | armyId |
| `getStayAllianceArmy` | `army.getStayAllianceArmy` | cityId |
| `disbandInjuredTroop` | `army.disbandInjuredTroop` | cityId, troopType, num |

### Castle Commands (CastleCommands.as)
| Method | Server Command | Parameters |
|--------|---------------|------------|
| `newBuilding` | `castle.newBuilding` | cityId, positionId, typeId |
| `upgradeBuilding` | `castle.upgradeBuilding` | cityId, positionId |
| `destructBuilding` | `castle.destructBuilding` | cityId, positionId |
| `speedUpBuildCommand` | `castle.speedUpBuild` | cityId, positionId, itemId |
| `cancelBuildingQueue` | `castle.cancelBuilding` | cityId, positionId |

### Hero Commands (HeroCommand.as)
| Method | Server Command | Parameters |
|--------|---------------|------------|
| `callBackHero` | `hero.callBackHero` | heroId, cityId |
| `fireHero` | `hero.fireHero` | heroId |
| `promoteHero` | `hero.promoteHero` | heroId |
| `addAttrPoint` | `hero.addAttrPoint` | heroId, attrType, num |
| `resetAttrPoint` | `hero.resetAttrPoint` | heroId |

### Mail Commands (MailCommands.as)
| Method | Server Command | Parameters |
|--------|---------------|------------|
| `getAllTVMsg` | `mail.getAllTVMsg` | - |
| `sendMail` | `mail.sendMail` | toName, subject, content |
| `readMail` | `mail.readMail` | mailId |
| `deleteMail` | `mail.deleteMail` | mailId |

---

## 🎯 Use Case Quick Reference

### "I want to send troops"
```python
evony_search("army.newArmy sendTroop troops parameter")
# Use: ArmyCommands.newArmy(cityId, heroId, troops[])
```

### "I want to train troops"  
```python
evony_search("troop.produceTroop train training queue")
# Use: TroopCommands.produceTroop(cityId, troopType, num)
```

### "I want to exploit overflow"
```python
evony_search("overflow threshold INT32_MAX troop cost")
# Threshold: 6,135,037 archers (cost=350)
```

### "I want to understand the protocol"
```python
evony_search("AMF3 packet serialize GameClient socket")
# See: GameClient.as, SenderImpl.as, amf3.py
```

### "I want to write scripts"
```python
evony_search("Script.as ScriptCmd command variable")
# See: Script_1.as, ScriptCmd_1.as
```

---

## 📁 File Index by Purpose

### Network Layer
- `GameClient.as` - Main client
- `SenderImpl.as` - Message sender
- `Connection.as` - Socket connection
- `evony_client_b61e3409.py` - Python implementation

### Command Layer
- `ActionFactory.as` - Command registration
- `ArmyCommands.as` - Army ops
- `CastleCommands.as` - Building ops
- `HeroCommand.as` - Hero management
- `TroopCommands.as` - Troop training

### Script Engine
- `Script.as` - Script parser
- `ScriptCmd.as` - Command definitions
- `script_engine.py` - Python implementation

### Exploits
- `exploit_engine.py` - Exploit framework
- `protocol_exploiter.py` - Protocol exploits
- `ALL_ENCRYPTION_KEYS.py` - Key extraction

---

*Generated from RAG index: 166,043 chunks, 55,871 symbols*
