# 📚 SVONY MASTER REFERENCE

Complete extraction from RAG: 166,043 chunks, 55,871 symbols, 301+ commands.

---

## 🔐 ALL ENCRYPTION KEYS

### Primary Keys (Verified)
```python
# From ALL_ENCRYPTION_KEYS.py, hub_ultimate.py, protocol_injector.py

# Primary Action Key - Signs ALL game commands
ACTION_KEY = "TAO_{313-894*&*($*#-FDIU(430}-{facebook_dioe(&*%$l}"

# Secondary Action Key (SL variant)
ACTION_KEY_SL = "TAO_{313-894*&*($*#-FDIU(430}_SL"

# User Info Key - Double MD5 for user lookup
USER_INFO_KEY = "IUGI_md5_key_{djfiji3*4930}-{fjdi3284$9dlld}"

# API Key - API signature
API_KEY = "9f758e2deccbe6244f734371b9642eda"

# XOR Key - Data obfuscation
XOR_KEY = 0xAA  # 170 decimal

# Login Salt
LOGIN_SALT = "evony"

# Game Key
GAME_KEY = "EvonyGameKey2009"
```

### Static Keys
```python
# From SOURCE_COMPLETENESS_ANALYSIS.md
STATIC_KEYS = {
    'game': 'EvonyGameKey2009',
    'network': 'EvonyNetKey2009',
    'resource': 'EvonyResKey2009',
    'config': 'EvonyConfigKey2009',
    'data': 'EvonyDataKey2009',
}

# Salts
SALTS = {
    'password': 'evony',
    'session': 'evony_session_salt',
}
```

### Signature Functions
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

def xor_encrypt(data: bytes) -> bytes:
    """XOR encrypt/decrypt"""
    return bytes(b ^ XOR_KEY for b in data)

def create_login_hash(username: str, password: str) -> str:
    """Create login hash"""
    md5_pass = hashlib.md5(password.encode()).hexdigest()
    return hashlib.md5((username + md5_pass + LOGIN_SALT).encode()).hexdigest()

def extended_action_signature(action: str, sex: str, datetime: str,
                              username: str, server_id: str, speed_type: str,
                              pfid: str) -> str:
    """Extended action signature (from ALL_ENCRYPTION_KEYS.py)"""
    data = action + sex + datetime + username + server_id + speed_type + pfid
    return hashlib.md5((data + ACTION_KEY_SL).encode()).hexdigest()
```

### Item Keys (From RAG)
```python
ITEM_KEYS = [
    "player.key.newyear",
    "player.key.easter_package",
    "player.key.special.chest",
]
```

---

## 📡 ALL PROTOCOL COMMANDS (301+)

### Command Categories
| Category | Count | Description |
|----------|-------|-------------|
| `alliance` | 31 | Create, join, manage alliances |
| `army` | 14 | Move troops, call back, exercise |
| `capital` | 7 | Levy resources, taxes |
| `castle` | 19 | Build, upgrade, demolish |
| `celeb` | 5 | Celebrity/events |
| `city` | 12 | City management |
| `common` | 8 | Common operations |
| `field` | 6 | Field/map operations |
| `fortifications` | 4 | Wall defenses |
| `friend` | 7 | Social features |
| `gamble` | 3 | Gambling/lottery |
| `hero` | 15 | Hero management |
| `interior` | 8 | City interior |
| `mail` | 9 | Mail system |
| `map` | 11 | Map exploration |
| `player` | 14 | Player data |
| `quest` | 6 | Quest system |
| `rank` | 5 | Rankings |
| `report` | 7 | Battle reports |
| `shop` | 8 | Item shop |
| `stratagem` | 4 | Stratagems |
| `tech` | 6 | Research |
| `trade` | 9 | Market/trade |
| `troop` | 12 | Troop training |
| **TOTAL** | **301+** | |

### Army Commands (14)
```python
ARMY_COMMANDS = [
    'army.callBackArmy',
    'army.cureInjuredTroop',
    'army.disbandFleeTroop',
    'army.disbandInjuredTroop',
    'army.exerciseArmy',
    'army.getInjuredTroop',
    'army.getStayAllianceArmys',
    'army.newArmy',
    'army.setAllowAllianceArmy',
    'army.setArmyGoOut',
    'army.speedupArmyAtHome',
    'army.speedupArmyAtTarget',
    'army.createArmy',
    'army.disbandArmy',
]
```

### Troop Commands (12)
```python
TROOP_COMMANDS = [
    'troop.produceTroop',
    'troop.cancelTroopProduce',
    'troop.disbandTroop',
    'troop.accTroopProduce',
    'troop.getTroopProduceList',
    'troop.checkIdleBarrack',
    'troop.getProduceQueue',
    'troop.speedUpTroop',
    'troop.train',
    'troop.cancel',
    'troop.disband',
    'troop.queue',
]
```

### Castle Commands (19)
```python
CASTLE_COMMANDS = [
    'castle.newBuilding',
    'castle.upgradeBuilding',
    'castle.destructBuilding',
    'castle.demolishBuildingQueue',
    'castle.speedUpBuild',
    'castle.cancelBuilding',
    'castle.getCastleFieldInfo',
    'castle.getAvailableBuildingListInside',
    'castle.getAvailableBuildingListOutside',
    'castle.setBuildingQueue',
    'castle.moveCastle',
    'castle.renameCastle',
    'castle.abandonCastle',
    'castle.getCastleInfo',
    'castle.getBuildingState',
    'castle.getCoordinates',
    'castle.setWallDefense',
    'castle.repairWall',
    'castle.upgradeWall',
]
```

### Hero Commands (15)
```python
HERO_COMMANDS = [
    'hero.callBackHero',
    'hero.fireHero',
    'hero.promoteHero',
    'hero.addAttrPoint',
    'hero.resetAttrPoint',
    'hero.dischargeChief',
    'hero.hireHero',
    'hero.recruitHero',
    'hero.getHeroList',
    'hero.setMayor',
    'hero.removeMayor',
    'hero.equipItem',
    'hero.unequipItem',
    'hero.levelUp',
    'hero.getHeroInfo',
]
```

### Interior Commands (8)
```python
INTERIOR_COMMANDS = [
    'interior.pacifyPeople',
    'interior.setTaxRate',
    'interior.setComfortRate',
    'interior.levy',
    'interior.getResourceInfo',
    'interior.collectTax',
    'interior.setProduction',
    'interior.getInteriorInfo',
]
```

### Alliance Commands (31)
```python
ALLIANCE_COMMANDS = [
    'alliance.createAlliance',
    'alliance.joinAlliance',
    'alliance.leaveAlliance',
    'alliance.kickMember',
    'alliance.promoteMember',
    'alliance.demoteMember',
    'alliance.setAllInfoForAlliance',
    'alliance.getAllianceArmyReport',
    'alliance.getAllianceEventList',
    'alliance.cancelAddUserToAlliance',
    'alliance.getInfo',
    'alliance.getMemberList',
    # ... 19 more
]
```

### Mail Commands (9)
```python
MAIL_COMMANDS = [
    'mail.getAllTVMsg',
    'mail.sendMail',
    'mail.readMail',
    'mail.deleteMail',
    'mail.getMail',
    'mail.markRead',
    'mail.getMailList',
    'mail.reply',
    'mail.forward',
]
```

### Map Commands (11)
```python
MAP_COMMANDS = [
    'map.scout',
    'map.getRegion',
    'map.getTile',
    'map.getCoords',
    'map.searchPlayer',
    'map.searchAlliance',
    'map.getNPCInfo',
    'map.getValleyInfo',
    'map.attack',
    'map.occupy',
    'map.abandon',
]
```

---

## 💥 EXPLOIT REFERENCE

### Integer Overflow Thresholds
```python
INT32_MAX = 2147483647

# From exploit_engine.py, exploits.py
TROOP_DATA = {
    1: {'name': 'Worker',      'abbrev': 'wo',  'food': 50,   'threshold': 42949673},
    2: {'name': 'Warrior',     'abbrev': 'w',   'food': 100,  'threshold': 21474837},
    3: {'name': 'Scout',       'abbrev': 's',   'food': 150,  'threshold': 14316558},
    4: {'name': 'Pikeman',     'abbrev': 'p',   'food': 200,  'threshold': 10737419},
    5: {'name': 'Swordsman',   'abbrev': 'sw',  'food': 250,  'threshold': 8589935},
    6: {'name': 'Archer',      'abbrev': 'a',   'food': 350,  'threshold': 6135037},
    7: {'name': 'Cavalry',     'abbrev': 'c',   'food': 800,  'threshold': 2684355},
    8: {'name': 'Cataphract',  'abbrev': 'ca',  'food': 1500, 'threshold': 1431656},
    9: {'name': 'Transporter', 'abbrev': 't',   'food': 500,  'threshold': 4294968},
    10: {'name': 'Ballista',   'abbrev': 'ba',  'food': 2500, 'threshold': 858994},
    11: {'name': 'Ram',        'abbrev': 'r',   'food': 4000, 'threshold': 536871},
    12: {'name': 'Catapult',   'abbrev': 'cat', 'food': 6000, 'threshold': 357914},
}

def calculate_threshold(food_cost: int) -> int:
    """Calculate overflow threshold"""
    return (INT32_MAX // food_cost) + 1
```

### Troop Consumption Rates
```python
# From exploit_manager.py, game_logic.py, ALL_ENCRYPTION_KEYS.py
TROOP_CONSUMPTION = {
    "worker": 1,
    "warrior": 2,
    "scout": 3,
    "pikeman": 4,
    "swordsman": 6,
    "archer": 6,
    "cavalry": 10,
    "cataphract": 17,
    "transporter": 5,
    "ballista": 10,
    "ram": 15,
    "catapult": 20,
}
```

### Overflow Exploit Mechanism
```python
# From exploits.py
"""
TROOP OVERFLOW EXPLOIT (Known working 2009-2012)

When training troops:
  total_cost = troop_count × food_cost

If total_cost > INT32_MAX:
  - Value wraps to negative
  - Canceling production "refunds" the negative cost
  - Result: RESOURCE GAIN

Steps:
1. Queue troops at overflow threshold + 1
2. Server calculates negative cost
3. Cancel production
4. Receive "refund" of negative amount = GAIN
"""

def execute_overflow(troop_type: int, quantity: int) -> dict:
    """Execute overflow exploit"""
    food_cost = TROOP_DATA[troop_type]['food']
    raw = food_cost * quantity
    wrapped = raw & 0xFFFFFFFF
    if wrapped > INT32_MAX:
        wrapped -= 0x100000000
    return {
        "overflow": raw > INT32_MAX,
        "wrapped": wrapped,
        "gain": abs(wrapped) if wrapped < 0 else 0
    }
```

### Food Flip Glitch
```python
# From food_glitch_analyzer.py
"""
FOOD FLIP GLITCH

Food resets to 0 when exceeding 999M
Safe max: 485M food

SAFE_TROOP_LIMIT = 700,000,000 per type to avoid 3x flip
"""
```

### Known Vulnerable Functions
```python
# From exploit_discovery.py
VULNERABLE_FUNCTIONS = [
    "commissionTransfer",  # 2B troop transfer exploit
    "thunderRaid",         # Race condition
    "reinforceValley",     # Resource duplication
    "trainTroop",          # Integer overflow
    "cancelTroop",         # Refund exploit
    "disbandTroop",        # Resource recovery
]
```

---

## 🎮 ACTIONSCRIPT CLASSES

### ActionFactory (Command Factory)
```actionscript
// From ActionFactory.as - Central command registration
package com.evony.client.action {
    public class ActionFactory {
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
        private var colonyCommands:ColonyCommands;
        private var stratagemCommands:StratagemCommands;
        private var truceCommands:TruceCommands;
    }
}
```

### ResponseDispatcher Constants
```actionscript
// From ResponseDispatcher.as, ResponseDispatcher_1.as
public static const TROOP_CANCEL_TROOP_PRODUCE:String = "troop.cancelTroopProduce";
public static const TROOP_CHECK_IDLE_BARRACK:String = "troop.checkIdleBarrack";
public static const ARMY_GET_STAY_ALLIANCE_ARMYS:String = "army.getStayAllianceArmys";
public static const ALLIANCE_SET_ALL_INFO_FOR_ALLIANCE:String = "alliance.setAllInfoForAlliance";
public static const ALLIANCE_CANCELADD_USERTO_ALLIANCE:String = "alliance.cancelAddUserToAlliance";
public static const CASTLE_DEMOLISH_BUILDING_QUEUE:String = "castle.demolishBuildingQueue";
public static const CASTLE_DESTRUCT_BUILDING:String = "castle.destructBuilding";
public static const CASTLE_GET_AVAILABLE_BUILDING_LIST_INSIDE:String = "castle.getAvailableBuildingListInside";
public static const CASTLE_GET_AVAILABLE_BUILDING_LIST_OUTSIDE:String = "castle.getAvailableBuildingListOutside";
```

### Data Beans
```actionscript
// Key data classes from com.evony.common.beans
HeroBean.as         // Hero attributes
PlayerInfoBean.as   // Player data  
ResourceBean.as     // Resources
TroopBean.as        // Troop definitions
MapCastleBean.as    // Map objects
MailBean.as         // Mail system
ReportBean.as       // Battle reports
CastleBean.as       // Castle data
BuffBean.as         // Buffs/effects
```

### TroopEumDefine Constants
```actionscript
// From TroopEumDefine.as
package com.evony.eum {
    public class TroopEumDefine {
        public static const WORKER:int = 1;
        public static const WARRIOR:int = 2;
        public static const SCOUT:int = 3;
        public static const PIKEMAN:int = 4;
        public static const SWORDSMAN:int = 5;
        public static const ARCHER:int = 6;
        public static const CAVALRY:int = 7;
        public static const CATAPHRACT:int = 8;
        public static const TRANSPORTER:int = 9;
        public static const BALLISTA:int = 10;
        public static const RAM:int = 11;
        public static const CATAPULT:int = 12;
    }
}
```

---

## 🤖 AUTOEVONY SCRIPT COMMANDS

### Configuration
```
config hero:11,fasthero:50,trade:1,dumping:1,herominattack:50,junkhero:7
distancepolicy 20 20 20 20 20
resourcelimits 250000 400000 250000 200000
maintown
```

### Building
```
Build be:5:1,e:5:1      ; Beacon L5, Embassy L5
Build fh:9:1,r:10:1     ; Feasting Hall L9, Rally L10
Build c:3:7,s:3:13      ; Cottages, Stables
```

### Research
```
Research ar:5,mil:5     ; Archery, Military Science
Research con:8,met:3    ; Construction, Metal Casting
```

### Troops
```
troop a:1000            ; 1000 archers
troop a:6135037         ; OVERFLOW THRESHOLD!
```

### Control Flow
```
label start
if (c.cm.resource.food.amount < 1000000)
  collect
endif
goto start

loop 10
  farm npc:5
  wait 60
endloop
```

### Script Variables
```
$c.castle.id$                    ; Castle ID
$c.cm.resource.food.amount$      ; Food amount
$c.af.getTroopCommands()$        ; ActionFactory
$m_city.castle.name$             ; City name
```

### External Scripts
```
includeurl http://localhost:8088/overflow_chain
```

---

## 📊 GAME DATA

### Building IDs
| Abbr | Building | ID |
|------|----------|-----|
| `th` | Town Hall | 1 |
| `b` | Barracks | 2 |
| `c` | Cottage | 3 |
| `w` | Workshop | 4 |
| `a` | Academy | 5 |
| `f` | Forge | 6 |
| `m` | Market | 7 |
| `t` | Warehouse | 8 |
| `e` | Embassy | 9 |
| `r` | Rally Point | 10 |
| `fh` | Feasting Hall | 11 |
| `be` | Beacon | 12 |
| `inn` | Inn | 13 |
| `wa` | Walls | 14 |

### Fortification IDs
```python
FORTIFICATIONS = {
    'abatis': 1000,
    'arrowTower': 2000,
    'rollingLog': 3000,
    'trapHole': 4000,
    'wall': 5000,
}
```

### Buff Types
```python
BUFF_TYPES = {
    'PlayerIncArmyAttachBuff': "Enhances army Attack by 20%",
    # ... more buffs
}
```

---

## 🔧 PYTHON CLIENT

```python
import socket
import struct
import hashlib
from pyamf import amf3

class EvonyClient:
    """Complete Evony client implementation"""
    
    ACTION_KEY = "TAO_{313-894*&*($*#-FDIU(430}-{facebook_dioe(&*%$l}"
    
    def __init__(self, server: str = 'cc2'):
        self.host = f"{server}.evony.com"
        self.port = 443
        self.sock = None
        self.session_key = None
        
    def connect(self):
        """Connect to game server (RAW TCP, no SSL)"""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(30)
        self.sock.connect((self.host, self.port))
        self.sock.send(b"gameClient\x00")
        
    def send_command(self, cmd: str, params: dict) -> dict:
        """Send AMF command with signature"""
        sig = hashlib.md5((cmd + str(params) + self.ACTION_KEY).encode()).hexdigest()
        data = {"cmd": cmd, "params": params, "sig": sig, "sessionKey": self.session_key}
        
        encoder = amf3.Encoder()
        encoder.writeElement(data)
        encoded = encoder.stream.getvalue()
        
        packet = struct.pack('>L', len(encoded)) + encoded
        self.sock.sendall(packet)
        return self.receive()
        
    def receive(self) -> dict:
        """Receive AMF response"""
        size = struct.unpack('>L', self.sock.recv(4))[0]
        body = b''
        while len(body) < size:
            body += self.sock.recv(size - len(body))
        return amf3.Decoder(body).readElement()
        
    # Convenience methods
    def train_troops(self, city_id: int, troop_type: int, count: int):
        return self.send_command("troop.produceTroop", 
            {"cityId": city_id, "troopType": troop_type, "num": count})
            
    def cancel_troops(self, city_id: int, troop_type: int):
        return self.send_command("troop.cancelTroopProduce",
            {"cityId": city_id, "troopType": troop_type})
            
    def new_army(self, city_id: int, hero_id: int, troops: list):
        return self.send_command("army.newArmy",
            {"cityId": city_id, "heroId": hero_id, "troops": troops})
            
    def overflow_exploit(self, city_id: int, troop_type: int = 6):
        """Execute overflow exploit (archer default)"""
        threshold = TROOP_DATA[troop_type]['threshold']
        self.train_troops(city_id, troop_type, threshold)
        import time; time.sleep(2)
        return self.cancel_troops(city_id, troop_type)
```

---

## 📁 SOURCE FILE INDEX

### Key Python Files
| File | Purpose |
|------|---------|
| `ALL_ENCRYPTION_KEYS.py` | All encryption keys |
| `hub_ultimate.py` | Ultimate toolkit |
| `exploit_engine.py` | Exploit framework |
| `protocol_injector.py` | Protocol injection |
| `mega_toolkit.py` | Mega toolkit |
| `borg_toolkit.py` | 301+ commands |
| `exploits.py` | Exploit implementations |
| `game_logic.py` | Game mechanics |

### Key ActionScript Files
| File | Purpose |
|------|---------|
| `ActionFactory.as` | Command factory |
| `ArmyCommands.as` | Army operations |
| `TroopCommands.as` | Troop training |
| `CastleCommands.as` | Building ops |
| `HeroCommand.as` | Hero management |
| `ResponseDispatcher.as` | Event dispatch |
| `GameClient.as` | Network client |
| `SenderImpl.as` | Message sender |
| `TroopEumDefine.as` | Troop constants |

### Key Documentation
| File | Purpose |
|------|---------|
| `COMMAND_REFERENCE.md` | Full command list |
| `GLITCH_MECHANICS.md` | Overflow details |
| `SOURCE_COMPLETENESS_ANALYSIS.md` | Source inventory |
| `DEFINITIVE_SOURCE_VERIFICATION.md` | Key verification |

---

*Master reference extracted from RAG: 166,043 chunks, 55,871 symbols*
*Sources: EvonyClient1921.swf, AutoEvony2.swf, 16MB scripts, 9MB client*
