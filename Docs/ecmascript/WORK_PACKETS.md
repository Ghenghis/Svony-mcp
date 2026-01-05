# 📦 ECMAScript Work Packets

Patch-ready extraction bundles for Evony Client ActionScript modules.

---

## WP-001: Network Payload Builder

### Overview
| Field | Value |
|-------|-------|
| **ID** | WP-001-PAYLOAD-BUILDER |
| **Purpose** | Build command packets from dynamic objects |
| **Risk Level** | 🟡 Medium |
| **Patch Complexity** | Low |

### Primary Files
```
com/evony/SenderImpl.as          [46 lines]
  └─ Tags: GENERIC_MAP, SINGLETON_ACCESS
  └─ Entry: sendMessage(cmd:String, params:Object):void

com/evony/net/client/GameClient.as  [~500 lines]
  └─ Tags: SOCKET_IO, BYTE_ARRAY, AMF_SERIALIZE
  └─ Entry: sendMessage(cmd:String, params:Object):void
```

### Dependencies
```yaml
required:
  - com/evony/common/Sender.as        # Interface - must implement
  - com/evony/Context.as              # State - getInstance(), getCurCastle()
  - com/evony/common/MouseManager.as  # UI - setBusy()

optional_stubs:
  - flash/net/Socket.as               # Can mock for testing
```

### Data Contract
```actionscript
// INPUT
cmd: String
  format: "namespace.action"
  examples: ["troop.train", "castle.upgrade", "hero.levelUp"]
  
params: Object
  required: { castleId: int }
  optional: { 
    count: int,           // Troop count - OVERFLOW RISK
    heroId: int,          // Hero identifier
    targetX: int,         // Map coordinates
    targetY: int,
    buildingId: int,
    positionId: int
  }

// OUTPUT
AMF ByteArray → Socket
```

### Patch Plan
```diff
--- a/com/evony/SenderImpl.as
+++ b/com/evony/SenderImpl.as
@@ -22,6 +22,20 @@
         public function sendMessage(_arg_1:String, _arg_2:Object):void
         {
+            // === PATCH: Validation Layer ===
+            if (!validateCommand(_arg_1)) {
+                trace("[BLOCKED] Invalid command: " + _arg_1);
+                return;
+            }
+            if (!validateParams(_arg_2)) {
+                trace("[BLOCKED] Invalid params for: " + _arg_1);
+                return;
+            }
+            // Log for debugging/analysis
+            trace("[SEND] " + _arg_1 + " " + JSON.stringify(_arg_2));
+            // === END PATCH ===
+
             if (Context.getInstance().bVisitor)
```

### Caller Impact
| Caller | File | Impact |
|--------|------|--------|
| `TroopCommands.train()` | `com/evony/client/action/TroopCommands.as` | ✅ None |
| `BuildingCommands.upgrade()` | `com/evony/client/action/BuildingCommands.as` | ✅ None |
| `HeroCommand.levelUp()` | `com/evony/client/action/HeroCommand.as` | ✅ None |
| `ArmyCommands.send()` | `com/evony/client/action/ArmyCommands.as` | ✅ None |

### Regression Tests
```actionscript
public function testValidCommand():void {
    var result:Boolean = validateCommand("troop.train");
    assert(result == true, "Valid command should pass");
}

public function testEmptyCommand():void {
    var result:Boolean = validateCommand("");
    assert(result == false, "Empty command should fail");
}

public function testOverflowParams():void {
    var params:Object = {castleId: 1, count: 2147483648};
    var result:Boolean = validateParams(params);
    assert(result == false, "Overflow count should fail");
}
```

---

## WP-002: Response Dispatcher

### Overview
| Field | Value |
|-------|-------|
| **ID** | WP-002-RESPONSE-DISPATCHER |
| **Purpose** | Route server responses to handlers |
| **Risk Level** | 🔴 High |
| **Patch Complexity** | Medium |

### Primary Files
```
com/evony/client/response/ResponseDispatcher.as  [~400 lines]
  └─ Tags: EVENT_DISPATCH, HANDLER_MAP
  └─ Entry: dispatchResponse(type:String, data:Object):void

com/evony/Context.as:152-170  [Event listeners]
  └─ Tags: LISTENER_REGISTRATION
```

### Event Constants
```actionscript
// Response types routed by dispatcher
SERVER_BUILD_COMPLATE        → onBuildComplete
SERVER_HERO_UPDATE           → onHeroUpdate
SERVER_RESOURCE_UPDATE       → onResourceUpdate
SERVER_PLAYER_INFO_UPDATE    → onPlayerInfoUpdate
SERVER_ITEM_UPDATE           → onItemUpdate
SERVER_SELF_ARMYS_UPDATE     → onSelfArmysUpdate
SERVER_ENEMY_ARMYS_UPDATE    → onEnemyArmysUpdate
SERVER_FRIEND_ARMYS_UPDATE   → onFriendArmysUpdate
SERVER_TROOP_UPDATE          → onTroopUpdate
SERVER_FORTIFICATIONS_UPDATE → onFortiFicationsUpdate
SERVER_CASTLE_FIELD_UPDATE   → onCastleFieldUpdate
SERVER_TRADES_UPDATE         → onTradesUpdate
SERVER_TRANSING_TRADE_UPDATE → onTransingTradeUpdate
SERVER_PLAYER_BUFF_UPDATE    → onPlayerBuffUpdate
SERVER_CASTLE_UPDATE         → onCastleUpdate
SERVER_COLONY_UPDATE         → onColonyUpdate
SERVER_MERCENARY_UPDATE      → onMercenaryUpdate
SERVER_BUILDING_QUEUE_UPDATE → onBuildingQueueUpdate
```

### Data Contract
```actionscript
// INPUT (from server)
type: String   // Event constant
data: Object   // AMF-decoded response
  {
    castleId: int,
    updateType: int,  // ADD=1, UPDATE=2, DELETE=3
    bean: Object,     // Type-specific data
    ...
  }

// OUTPUT
Event dispatched to registered handlers
```

### Patch Plan
```diff
--- a/com/evony/client/response/ResponseDispatcher.as
+++ b/com/evony/client/response/ResponseDispatcher.as
@@ -50,6 +50,15 @@
         public function dispatchResponse(type:String, data:Object):void
         {
+            // === PATCH: Response Validation ===
+            try {
+                validateResponse(type, data);
+            } catch (e:Error) {
+                trace("[INVALID RESPONSE] " + type + ": " + e.message);
+                return;
+            }
+            // === END PATCH ===
+
             var event:* = createEvent(type, data);
             dispatchEvent(event);
         }
```

### Reflection Risk
⚠️ **Medium** - Event type strings are literals, but handlers are looked up dynamically via event system.

---

## WP-003: AMF Serializer

### Overview
| Field | Value |
|-------|-------|
| **ID** | WP-003-AMF-SERIALIZER |
| **Purpose** | Serialize/deserialize AMF packets |
| **Risk Level** | 🔴 High |
| **Patch Complexity** | High |

### Primary Files
```
mx/messaging/messages/CommandMessage.as
mx/messaging/messages/CommandMessageExt.as
  └─ Tags: EXTERNAL_INTERFACE, BYTE_ARRAY

Python equivalent:
  pyamf/amf3.py
  └─ writeByteArray(), readObject()
```

### AMF Type Markers
```
0x00  undefined
0x01  null
0x02  false
0x03  true
0x04  integer
0x05  double
0x06  string
0x07  xml-doc
0x08  date
0x09  array
0x0A  object
0x0B  xml
0x0C  bytearray
```

### Data Contract
```actionscript
// INPUT (ActionScript objects)
var cmd:Object = {
    operation: "troop.train",
    castleId: 12345,
    params: {troopType: 6, count: 100}
};

// OUTPUT (ByteArray)
[0x0A]  // object marker
[0x0B]  // traits
[string: "operation"]
[string: "troop.train"]
[string: "castleId"]
[0x04][int: 12345]
...
```

### Patch Points
- Add overflow checks during serialization
- Validate object shapes before encoding
- Log serialized payloads for analysis

---

## WP-004: Context State Manager

### Overview
| Field | Value |
|-------|-------|
| **ID** | WP-004-CONTEXT-STATE |
| **Purpose** | Global application state |
| **Risk Level** | 🟡 Medium |
| **Patch Complexity** | Medium |

### Primary Files
```
com/evony/Context.as  [1329 lines]
  └─ Tags: SINGLETON, STATE_MACHINE, EVENT_DISPATCH
  └─ Key methods:
     - getInstance():Context
     - getCurCastle():CastleBean
     - getPlayerBean():PlayerBean
     - setCurCastle(castle:CastleBean):void
```

### State Variables
```actionscript
// Critical state (race condition targets)
private var curCastle:CastleBean = null;
private var player:PlayerBean;

// Security-sensitive
public var password:String = "";
public var userName:String = "";

// Session
private var timeDiff:Number;
private var loginDateTime:Date;
```

### Patch Plan
```diff
--- a/com/evony/Context.as
+++ b/com/evony/Context.as
@@ -266,9 +266,18 @@
         public function setCurCastle(_arg_1:CastleBean):void
         {
+            // === PATCH: Atomic castle change ===
+            if (_changingCastle) {
+                trace("[BLOCKED] Castle change already in progress");
+                return;
+            }
+            _changingCastle = true;
+            
             if (((this.curCastle == null) || (!(_arg_1.id == this.curCastle.id))))
             {
                 trace(("Context.setCurCastle(): curCastle change to " + _arg_1.id));
                 this.curCastle = _arg_1;
                 MsgDispacther.getInstance().dispatchEvent(new Event(EVENT_CASTLE_CHANGE));
             };
+            
+            _changingCastle = false;
+            // === END PATCH ===
         }
```

---

## WP-005: Troop Bean (Overflow Target)

### Overview
| Field | Value |
|-------|-------|
| **ID** | WP-005-TROOP-BEAN |
| **Purpose** | Troop count storage |
| **Risk Level** | 🔴 Critical |
| **Patch Complexity** | Low |

### Primary Files
```
com/evony/common/beans/TroopBean.as
  └─ Tags: DATA_MODEL, OVERFLOW_VULNERABLE
  └─ All properties: int type (32-bit signed)
```

### Vulnerable Properties
```actionscript
public var worker:int;      // Can overflow
public var warrior:int;     // Can overflow
public var scout:int;       // Can overflow
public var pikeman:int;     // Can overflow
public var swordsman:int;   // Can overflow
public var archer:int;      // PRIMARY EXPLOIT TARGET
public var cavalry:int;     // Can overflow
public var cataphract:int;  // Can overflow
public var transporter:int; // Can overflow
public var ballista:int;    // Can overflow
public var ram:int;         // Can overflow
public var catapult:int;    // Can overflow
```

### Patch Plan
```diff
--- a/com/evony/common/beans/TroopBean.as
+++ b/com/evony/common/beans/TroopBean.as
@@ -10,6 +10,14 @@
+        // === PATCH: Safe setters with overflow check ===
+        public function setArcher(value:int):Boolean {
+            if (value < 0) {
+                trace("[OVERFLOW] Negative archer count rejected: " + value);
+                return false;
+            }
+            this.archer = value;
+            return true;
+        }
+        // === END PATCH ===
+
         public var archer:int = 0;
```

---

## 📋 Work Packet Summary

| ID | Module | Files | Risk | Status |
|----|--------|-------|------|--------|
| WP-001 | Payload Builder | 3 | 🟡 | Ready |
| WP-002 | Response Dispatcher | 2 | 🔴 | Ready |
| WP-003 | AMF Serializer | 4 | 🔴 | Ready |
| WP-004 | Context State | 1 | 🟡 | Ready |
| WP-005 | Troop Bean | 1 | 🔴 | Ready |

---

*Part of Svony MCP - Evony Reverse Engineering Project*
