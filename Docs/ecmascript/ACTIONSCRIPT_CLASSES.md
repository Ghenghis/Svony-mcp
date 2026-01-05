# 📦 ActionScript Class Reference

Complete index of Evony Client ActionScript classes with bug annotations.

---

## 🏗️ Core Classes

### com.evony.Context
**File:** `com/evony/Context.as`
**Lines:** 1,329
**Purpose:** Global application state, castle/player management

| Method | Lines | Bugs | Severity |
|--------|-------|------|----------|
| `getInstance()` | 173-176 | Singleton pattern | ✅ OK |
| `getBuildingObjByType()` | 185-197 | Null reference | 🟡 Medium |
| `isBuildingQueued()` | 221-232 | Missing validation | 🟡 Medium |
| `setCurCastle()` | 266-274 | Race condition | 🔴 Critical |
| `onBuildComplete()` | 340-456 | Missing try/catch | 🟡 Medium |
| `timerHandler()` | 464-532 | Integer overflow | 🔴 Critical |
| `EncryptParam()` | 686-698 | Type safety | 🟡 Medium |

**Key State Variables:**
```actionscript
private static var instance:Context;
private var curCastle:CastleBean = null;
private var player:PlayerBean;
private var myTimer:Timer;
public var password:String = "";  // ⚠️ Security concern
public var userName:String = "";
```

---

### com.evony.SenderImpl
**File:** `com/evony/SenderImpl.as`
**Lines:** 46
**Purpose:** Message sending to server

| Method | Lines | Bugs | Severity |
|--------|-------|------|----------|
| `sendMessage()` | 22-40 | TOCTOU race | 🔴 Critical |

**Security Issues:**
- No command validation
- No parameter sanitization
- Silent failure in visitor mode

---

### com.evony.MsgDispacther
**File:** `com/evony/MsgDispacther.as`
**Lines:** 67
**Purpose:** Event dispatching, settings

**Note:** Class name has typo: "Dispac**th**er" instead of "Dispatcher"

---

### com.evony.GameConfig
**File:** `com/evony/GameConfig.as`
**Purpose:** Server configuration, constants

**Key Properties:**
- `serverID` - Server identifier
- `serverURL` - Connection endpoint
- `version` - Client version

---

## 📡 Network Classes

### com.evony.net.client.GameClient
**Purpose:** Main network communication

**Methods:**
- `connect()` - Establish connection
- `disconnect()` - Close connection
- `sendMessage()` - Send AMF command
- `onResponse()` - Handle server response

**Bugs:**
- Missing reconnect logic
- No timeout handling
- Silent connection failures

---

### com.evony.client.response.ResponseDispatcher
**Purpose:** Route server responses to handlers

**Events Dispatched:**
```actionscript
SERVER_BUILD_COMPLATE     // Typo: COMPLATE vs COMPLETE
SERVER_HERO_UPDATE
SERVER_RESOURCE_UPDATE
SERVER_PLAYER_INFO_UPDATE
SERVER_ITEM_UPDATE
SERVER_SELF_ARMYS_UPDATE
SERVER_ENEMY_ARMYS_UPDATE
SERVER_FRIEND_ARMYS_UPDATE
SERVER_TROOP_UPDATE
SERVER_FORTIFICATIONS_UPDATE
SERVER_CASTLE_FIELD_UPDATE
SERVER_TRADES_UPDATE
SERVER_TRANSING_TRADE_UPDATE
SERVER_PLAYER_BUFF_UPDATE
SERVER_CASTLE_UPDATE
SERVER_COLONY_UPDATE
SERVER_MERCENARY_UPDATE
SERVER_BUILDING_QUEUE_UPDATE
```

---

## 🏰 Data Bean Classes

### com.evony.common.beans.CastleBean
**Purpose:** Castle/city data container

**Properties:**
```actionscript
public var id:int;
public var name:String;
public var buildingsArray:ArrayCollection;
public var buildingQueuesArray:ArrayCollection;
public var troop:TroopBean;
public var fortification:FortificationBean;
public var resource:CastleResourceBean;
public var fieldsArray:ArrayCollection;
public var transingTradesArray:ArrayCollection;
```

---

### com.evony.common.beans.TroopBean
**Purpose:** Troop counts container

**Properties (all `int` - vulnerable to overflow):**
```actionscript
public var worker:int;
public var warrior:int;
public var scout:int;
public var pikeman:int;
public var swordsman:int;
public var archer:int;      // 🔴 Overflow exploitable
public var cavalry:int;
public var cataphract:int;
public var transporter:int;
public var ballista:int;
public var ram:int;
public var catapult:int;
```

---

### com.evony.common.beans.PlayerBean
**Purpose:** Player account data

**Properties:**
```actionscript
public var castlesArray:ArrayCollection;
public var selfArmysArray:ArrayCollection;
public var friendArmysArray:ArrayCollection;
public var itemsArray:ArrayCollection;
public var currentDateTime:String;
public var currentTime:Number;
public var mapSizeX:int;
public var mapSizeY:int;
```

---

### com.evony.common.beans.BuildingBean
**Purpose:** Building data

**Properties:**
```actionscript
public var positionId:int;
public var typeId:int;
public var name:String;
public var level:int;
public var status:int;
public var startTime:Number;
public var endTime:Number;
```

---

### com.evony.common.beans.HeroBean
**Purpose:** Hero data

**Properties:**
```actionscript
public var id:int;
public var name:String;
public var level:int;
public var politics:int;
public var attack:int;
public var intelligence:int;
public var status:String;
public var energy:int;
```

---

## 🎮 UI View Classes

### view.MainWin
**Purpose:** Main game window

### view.castle.TownView
**Purpose:** Inner city view
**Events:**
- `EVENT_BUILDING_DESTROY`
- `EVENT_BUILDING_COMPLETE`
- `EVENT_BUILDING_CREATED`
- `EVENT_BUILDING_UPDATE`

### view.castle.CityView
**Purpose:** Outer city view
**Events:** Same as TownView

### view.ChatFrame
**Purpose:** Chat interface

### view.AllWindows
**Purpose:** Window manager

---

## 🛠️ Utility Classes

### com.evony.common.CommonUtil
**Methods:**
- `arrayCopy()` - Copy array contents

### com.evony.util.UIUtil
**Methods:**
- `isBuildingDestroy()` - Check building state
- `isInnerBuilding()` - Check building position

### com.evony.common.MouseManager
**Methods:**
- `setBusy()` - Show busy cursor

---

## 📋 Constants Classes

### com.evony.common.constants.CommonConstants
```actionscript
public static const UPDATE_TYPE_ADD:int = 1;
public static const UPDATE_TYPE_UPDATE:int = 2;
public static const UPDATE_TYPE_DELETE:int = 3;
```

### com.evony.common.constants.BuildingConstants
Building type IDs and position constants

---

## 🔄 Event Classes

### com.evony.events.BuildingChangeEvent
### com.evony.events.BuildnewCastleEvent
### com.evony.common.server.events.*
- `BuildComplate` (typo)
- `SelfArmysUpdate`
- `EnemyArmysUpdate`
- `FriendArmysUpdate`
- `TroopUpdate`
- `FortificationsUpdate`
- `CastleFieldUpdate`
- `TradesUpdate`
- `TransingTradeUpdate`
- `PlayerBuffUpdate`
- `CastleUpdate`
- `ColonyUpdate`
- `MercenaryUpdate`
- `BuildingQueueUpdate`
- `ResourceUpdate`
- `PlayerInfoUpdate`
- `HeroUpdate`
- `ItemUpdate`

---

## 🐛 Common Code Smells

### 1. Obfuscated Variable Names
```actionscript
private var _1069971177useEnglish:Boolean;
private var _340524749showBuildingLevel:Boolean;
private var _633161435noAccountProtection:Boolean;
```
Decompiler artifacts - original names lost.

### 2. Typos in Constants/Classes
- `MsgDispacther` → `MsgDispatcher`
- `BUILD_COMPLATE` → `BUILD_COMPLETE`
- `caslteId` → `castleId`

### 3. Magic Numbers
```actionscript
if (positionId > 100)  // What is 100?
// Should be: if (positionId > INNER_BUILDING_POSITION)
```

### 4. Long Methods
`onBuildComplete()` - 116 lines, should be split

### 5. Deep Nesting
```actionscript
if (condition1) {
    if (condition2) {
        if (condition3) {
            // 4+ levels deep
        }
    }
}
```

---

*Part of Svony MCP - Evony Reverse Engineering Project*
