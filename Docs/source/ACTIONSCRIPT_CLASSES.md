# ActionScript Class Reference

Complete index of Evony client ActionScript classes organized by package.

---

## 📦 Package Structure

```
com.evony/
├── client/
│   └── action/           # Command implementations
│       ├── ActionFactory.as
│       ├── ArmyCommands.as
│       ├── CastleCommands.as
│       ├── TroopCommands.as
│       ├── HeroCommand.as
│       ├── InteriorCommands.as
│       ├── MailCommands.as
│       ├── AllianceCommands.as
│       ├── TechCommands.as
│       ├── ColonyCommands.as
│       ├── StratagemCommands.as
│       ├── TruceCommands.as
│       └── ...
│
├── net/
│   └── client/
│       └── GameClient.as # Network client
│
├── common/
│   ├── Sender.as         # Sender interface
│   ├── module/
│   │   └── army/         # Army data classes
│   └── paramBeans/       # Parameter beans
│
├── eum/
│   └── TroopEumDefine.as # Troop definitions
│
└── SenderImpl.as         # Sender implementation
```

---

## 🔧 com.evony.client.action

### ActionFactory.as
Central factory for all game commands.

```actionscript
package com.evony.client.action {
    public class ActionFactory {
        // Command instances
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
        
        // Getters
        public function getArmyCommands():ArmyCommands;
        public function getTroopCommands():TroopCommands;
        public function getCastleCommands():CastleCommands;
        public function getHeroCommand():HeroCommand;
        // ... etc
    }
}
```

### ArmyCommands.as
Army operations.

```actionscript
package com.evony.client.action {
    import com.evony.common.paramBeans.NewArmyParam;
    
    public class ArmyCommands {
        internal var sender:Sender;
        
        // Callbacks
        public var _newArmy_callback:Function;
        public var _callBackArmy_callback:Function;
        public var _disbandArmy_callback:Function;
        public var _exerciseArmy_callback:Function;
        public var _disbandInjuredTroop_callback:Function;
        public var _setAllowAllianceArmy_callback:Function;
        public var _getStayAllianceArmys_callback:Function;
        
        // Methods
        public function newArmy(param:NewArmyParam, callback:Function=null):CommandResponse {
            this._newArmy_callback = callback;
            if (this.sender != null) {
                sender.sendMessage("army.newArmy", param);
            }
            return null;
        }
        
        public function callBackArmy(armyId:int, cityId:int, callback:Function=null):CommandResponse {
            this._callBackArmy_callback = callback;
            if (this.sender != null) {
                sender.sendMessage("army.callBackArmy", {"armyId": armyId, ...});
            }
            return null;
        }
    }
}
```

### TroopCommands.as
Troop training and management.

```actionscript
package com.evony.client.action {
    import com.evony.common.paramBeans.*;
    
    public class TroopCommands {
        // Callbacks
        public var _produceTroop_callback:Function;
        public var _accTroopProduce_callback:Function;
        public var _cancelTroopProduce_callback:Function;
        public var _disbandTroop_callback:Function;
        
        // Methods
        public function produceTroop(cityId:int, troopType:int, num:int):void;
        public function cancelTroopProduce(cityId:int, troopType:int):void;
        public function disbandTroop(cityId:int, troopType:int, num:int):void;
        public function accTroopProduce(cityId:int, itemId:int):void;
    }
}
```

### CastleCommands.as
Building operations.

```actionscript
package com.evony.client.action {
    public class CastleCommands {
        // Callbacks
        public var _cancelBuildingQueue_callback:Function;
        public var _speedUpBuildCommand_callback:Function;
        public var _destructBuilding_callback:Function;
        public var _newBuilding_callback:Function;
        public var _upgradeBuilding_callback:Function;
        
        // Methods
        public function newBuilding(cityId:int, positionId:int, typeId:int):void;
        public function upgradeBuilding(cityId:int, positionId:int):void;
        public function destructBuilding(cityId:int, positionId:int):void;
        public function speedUpBuild(cityId:int, positionId:int, itemId:int):void;
        public function cancelBuilding(cityId:int, positionId:int):void;
    }
}
```

### HeroCommand.as
Hero management.

```actionscript
package com.evony.client.action {
    public class HeroCommand {
        // Callbacks
        public var _callBackHero_callback:Function;
        public var _fireHero_callback:Function;
        public var _promoteHero_callback:Function;
        public var _addAttrPoint_callback:Function;
        public var _resetAttrPoint_callback:Function;
        
        // Methods
        public function callBackHero(heroId:int, cityId:int, callback:Function=null):CommandResponse {
            this._callBackHero_callback = callback;
            if (this.sender != null) {
                sender.sendMessage("hero.callBackHero", {...});
            }
            return null;
        }
        
        public function dischargeChief(cityId:int):void;
        public function fireHero(heroId:int):void;
        public function promoteHero(heroId:int):void;
        public function addAttrPoint(heroId:int, attrType:int, num:int):void;
        public function resetAttrPoint(heroId:int):void;
    }
}
```

### InteriorCommands.as
City interior management.

```actionscript
package com.evony.client.action {
    public class InteriorCommands {
        public function pacifyPeople(cityId:int):void {
            if (this.sender != null) {
                sender.sendMessage("interior.pacifyPeople", {"cityId": cityId});
            }
        }
        
        public function setTaxRate(cityId:int, rate:int):void;
        public function setComfortRate(cityId:int, rate:int):void;
    }
}
```

---

## 📡 com.evony.net

### GameClient.as
Main network client.

```actionscript
package com.evony.net.client {
    public class GameClient {
        private var amfObj:Object;
        private var processedCount:int;
        private var serverPort:int;
        private var lock:Boolean = false;
        private var readed:int = 0;
        
        public function connect(host:String, port:int):void;
        public function sendMessage(cmd:String, params:Object):void;
        public function disconnect():void;
    }
}
```

---

## 📨 com.evony

### SenderImpl.as
Sender implementation.

```actionscript
package com.evony {
    import com.evony.common.Sender;
    import com.evony.net.client.GameClient;
    
    public class SenderImpl implements Sender {
        private var client:GameClient;
        
        public function sendMessage(cmd:String, params:Object):void {
            client.sendMessage(cmd, params);
        }
    }
}
```

---

## 📊 ResponseDispatcher

Event dispatcher for server responses.

```actionscript
package com.evony {
    public class ResponseDispatcher {
        // Event constants
        public static const TROOP_CANCEL_TROOP_PRODUCE:String = "troop.cancelTroopProduce";
        public static const TROOP_CHECK_IDLE_BARRACK:String = "troop.checkIdleBarrack";
        public static const ARMY_GET_STAY_ALLIANCE_ARMYS:String = "army.getStayAllianceArmys";
        public static const ALLIANCE_SET_ALL_INFO_FOR_ALLIANCE:String = "alliance.setAllInfoForAlliance";
        public static const ALLIANCE_CANCELADD_USERTO_ALLIANCE:String = "alliance.cancelAddUserToAlliance";
        
        // Callbacks
        private var onAcademyResearchUpdate:Function = null;
        private var onQuestCompleteTipResponse:Function = null;
        private var onNewReport:Function = null;
        
        // Singleton
        public static function getInstance():ResponseDispatcher;
        
        // Event handling
        public function addEventListener(type:String, listener:Function):void;
        public function removeEventListener(type:String, listener:Function):void;
    }
}
```

### Usage in UI Components
```actionscript
// From Embassy.as
private function init():void {
    ResponseDispatcher.getInstance().addEventListener(
        ResponseDispatcher.ARMY_GET_STAY_ALLIANCE_ARMYS, 
        onGetStayAllianceArmys
    );
}

// From Introduct.as
private function init():void {
    ResponseDispatcher.getInstance().addEventListener(
        ResponseDispatcher.ALLIANCE_SET_ALL_INFO_FOR_ALLIANCE, 
        onSetAllInfoForAlliance
    );
}

// From InviteMember.as
ResponseDispatcher.getInstance().addEventListener(
    ResponseDispatcher.ALLIANCE_CANCELADD_USERTO_ALLIANCE, 
    onCancleAddUserToAlliance
);
```

---

## 🎖️ com.evony.eum

### TroopEumDefine.as
Troop type definitions.

```actionscript
package com.evony.eum {
    import flash.xml.XMLNode;
    import flash.xml.XMLDocument;
    
    public class TroopEumDefine {
        // Troop type constants
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

## 📦 com.evony.common.module.army

Army response classes.

### StayAllianceReponse.as
```actionscript
package com.evony.common.module.army {
    public class StayAllianceReponse {
        // Alliance army stay response data
    }
}
```

### TroopParamResponse.as
```actionscript
package com.evony.common.module.army {
    public class TroopParamResponse {
        // Troop parameter response data
    }
}
```

---

## 🔍 Key Classes for Hacking

| Class | Purpose | Key Methods |
|-------|---------|-------------|
| `ActionFactory` | Command factory | `getArmyCommands()`, `getTroopCommands()` |
| `ArmyCommands` | Army ops | `newArmy()`, `callBackArmy()` |
| `TroopCommands` | Troop training | `produceTroop()`, `disbandTroop()` |
| `CastleCommands` | Building | `newBuilding()`, `upgradeBuilding()` |
| `HeroCommand` | Heroes | `callBackHero()`, `dischargeChief()` |
| `GameClient` | Network | `sendMessage()`, `connect()` |
| `SenderImpl` | Message sender | `sendMessage()` |
| `ResponseDispatcher` | Events | `addEventListener()` |

---

## 🎯 Exploitation Points

### Command Interception
```actionscript
// Hook into sender to intercept commands
class ExploitSender extends SenderImpl {
    override public function sendMessage(cmd:String, params:Object):void {
        // Log or modify command
        trace("Command: " + cmd);
        trace("Params: " + JSON.stringify(params));
        
        // Modify params for exploit
        if (cmd == "troop.produceTroop") {
            params.num = 6135037; // Overflow threshold
        }
        
        super.sendMessage(cmd, params);
    }
}
```

### Response Interception
```actionscript
// Hook into ResponseDispatcher
ResponseDispatcher.getInstance().addEventListener(
    "troop.produceTroop.response",
    function(event:Object):void {
        // Analyze response
        trace("Response: " + JSON.stringify(event));
    }
);
```

---

*Extracted from RAG: 7,469 AS files indexed*
