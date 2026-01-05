# 🔗 Complete Cross-Reference Documentation

Full mapping between all Evony systems: Protocol ↔ UI ↔ Logic ↔ AutoEvony.

---

## 1. Command → Handler → Event Map

### Troop Commands
| Command | Handler Class | Response Event | UI Update |
|---------|--------------|----------------|-----------|
| `troop.produceTroop` | `TroopCommands` | `SERVER_TROOP_UPDATE` | `TroopList.refresh()` |
| `troop.cancelProduce` | `TroopCommands` | `SERVER_TROOP_UPDATE` | `TroopList.refresh()` |
| `troop.dismissTroop` | `TroopCommands` | `SERVER_TROOP_UPDATE` | `TroopList.refresh()` |
| `troop.checkIdleBarrack` | `TroopCommands` | - | - |

### Building Commands
| Command | Handler Class | Response Event | UI Update |
|---------|--------------|----------------|-----------|
| `castle.upgradeBuilding` | `BuildingCommands` | `SERVER_BUILD_COMPLATE` | `TownView.refresh()` |
| `castle.destructBuilding` | `BuildingCommands` | `SERVER_BUILD_COMPLATE` | `TownView.refresh()` |
| `castle.cancelBuildCommand` | `BuildingCommands` | `SERVER_BUILDING_QUEUE_UPDATE` | `BuildingQueue.refresh()` |
| `castle.newBuilding` | `BuildingCommands` | `SERVER_BUILD_COMPLATE` | `TownView.refresh()` |

### Army Commands
| Command | Handler Class | Response Event | UI Update |
|---------|--------------|----------------|-----------|
| `army.newArmy` | `ArmyCommands` | `SERVER_SELF_ARMYS_UPDATE` | `ArmyList.refresh()` |
| `army.callBackArmy` | `ArmyCommands` | `SERVER_SELF_ARMYS_UPDATE` | `ArmyList.refresh()` |
| `army.setArmyGoOut` | `ArmyCommands` | `SERVER_SELF_ARMYS_UPDATE` | `ArmyList.refresh()` |

### Hero Commands
| Command | Handler Class | Response Event | UI Update |
|---------|--------------|----------------|-----------|
| `hero.hireHero` | `HeroCommand` | `SERVER_HERO_UPDATE` | `HeroList.refresh()` |
| `hero.fireHero` | `HeroCommand` | `SERVER_HERO_UPDATE` | `HeroList.refresh()` |
| `hero.levelUp` | `HeroCommand` | `SERVER_HERO_UPDATE` | `HeroDetail.refresh()` |
| `hero.addPoint` | `HeroCommand` | `SERVER_HERO_UPDATE` | `HeroDetail.refresh()` |
| `hero.tryGetSeizedHero` | `HeroCommand` | `SERVER_HERO_UPDATE` | `HeroList.refresh()` |

### Resource Commands
| Command | Handler Class | Response Event | UI Update |
|---------|--------------|----------------|-----------|
| `castle.getCoinsNeed` | `ResourceCommands` | - | `ResourceBar.update()` |
| `interior.taxRate` | `ResourceCommands` | `SERVER_RESOURCE_UPDATE` | `ResourceBar.update()` |
| `interior.modifyCommenceRate` | `ResourceCommands` | `SERVER_RESOURCE_UPDATE` | `ResourceBar.update()` |

---

## 2. AutoEvony Script → Protocol Map

### Training Commands
| AutoEvony | Protocol Call | Parameters |
|-----------|--------------|------------|
| `train a:1000` | `troop.produceTroop` | `{troopType:6, num:1000}` |
| `train w:500,s:200` | `troop.produceTroop` × 2 | Loop over types |
| `cancel a` | `troop.cancelProduce` | `{troopType:6}` |
| `dismiss a:100` | `troop.dismissTroop` | `{troopType:6, num:100}` |

### Building Commands
| AutoEvony | Protocol Call | Parameters |
|-----------|--------------|------------|
| `build barracks` | `castle.newBuilding` | `{typeId:1}` |
| `upgrade 1032` | `castle.upgradeBuilding` | `{positionId:1032}` |
| `demolish 1032` | `castle.destructBuilding` | `{positionId:1032}` |

### Army Commands
| AutoEvony | Protocol Call | Parameters |
|-----------|--------------|------------|
| `attack 100,200` | `army.newArmy` | `{targetX:100, targetY:200, missionType:1}` |
| `scout 100,200` | `army.newArmy` | `{missionType:3}` |
| `transport 100,200` | `army.newArmy` | `{missionType:4}` |
| `reinforce 100,200` | `army.newArmy` | `{missionType:2}` |
| `recall` | `army.callBackArmy` | `{armyId:X}` |

### Hero Commands
| AutoEvony | Protocol Call | Parameters |
|-----------|--------------|------------|
| `hire` | `hero.hireHero` | `{castleId:X}` |
| `fire %hero%` | `hero.fireHero` | `{heroId:X}` |
| `levelup %hero%` | `hero.levelUp` | `{heroId:X}` |

### Configuration Commands
| AutoEvony | Effect | Storage |
|-----------|--------|---------|
| `config npc:5` | Set NPC farm level | Local variable |
| `config valley:10` | Set valley target level | Local variable |
| `distancepolicy 30 5` | Set distance limits | Local variable |
| `keeptroop ...` | Set troop reserves | Local variable |

---

## 3. UI Component → Protocol Map

### Main Window Components
```
┌─────────────────────────────────────────────────────────┐
│ TopBar                                                   │
│  ├─ ResourceBar → interior.taxRate, castle.getCoinsNeed │
│  ├─ CitySelector → castle.enterCastle                   │
│  └─ BuffBar → (display only)                            │
├─────────────────────────────────────────────────────────┤
│ CityPanel                                               │
│  ├─ TownView → castle.upgradeBuilding, newBuilding     │
│  ├─ CityView → castle.upgradeBuilding, field ops       │
│  └─ MapView → map.getMapFieldInfo                      │
├─────────────────────────────────────────────────────────┤
│ SidePanel                                               │
│  ├─ HeroList → hero.*, army.newArmy                    │
│  ├─ TroopList → troop.produceTroop                     │
│  └─ QuestList → quest.getQuestType                     │
├─────────────────────────────────────────────────────────┤
│ ChatFrame → chat.*, mail.*                              │
└─────────────────────────────────────────────────────────┘
```

### Dialog → Protocol Map
| Dialog | Triggered By | Protocol Calls |
|--------|-------------|----------------|
| `TrainDialog` | Barracks click | `troop.produceTroop` |
| `UpgradeDialog` | Building click | `castle.upgradeBuilding` |
| `ArmyDialog` | Rally Point | `army.newArmy` |
| `HeroDialog` | Hero click | `hero.levelUp`, `hero.addPoint` |
| `ResearchDialog` | Academy | `tech.research` |
| `MarketDialog` | Market | `trade.newTrade` |
| `AllianceDialog` | Embassy | `alliance.*` |
| `MailDialog` | Feathermail | `mail.*` |

---

## 4. Event Flow Diagrams

### Train Troops Flow
```
User Click "Train"
       │
       ▼
TrainDialog.trainButton.click()
       │
       ▼
Sender.sendMessage("troop.produceTroop", {
  castleId: Context.getCurCastle().id,
  troopType: selectedType,
  num: inputCount
})
       │
       ▼
GameClient.sendAMF(packet)
       │
       ▼
[Server Processing]
       │
       ▼
ResponseDispatcher.dispatch(SERVER_TROOP_UPDATE)
       │
       ▼
Context.onTroopUpdate(event)
       │
       ▼
CastleBean.troop = newTroopBean
       │
       ▼
MsgDispatcher.dispatch(EVENT_TROOP_CHANGE)
       │
       ▼
TroopList.refresh()
```

### Building Upgrade Flow
```
User Click Building
       │
       ▼
TownView.onBuildingClick(positionId)
       │
       ▼
BuildingUpgradeDialog.show(building)
       │
       ▼
User Click "Upgrade"
       │
       ▼
Sender.sendMessage("castle.upgradeBuilding", {
  castleId: X,
  positionId: Y
})
       │
       ▼
[Server Processing]
       │
       ▼
ResponseDispatcher.dispatch(SERVER_BUILD_COMPLATE)
       │
       ▼
Context.onBuildComplete(event)
       │
       ├─► Building status = IN_PROGRESS
       │
       ├─► Context.timerHandler() tracks progress
       │
       └─► When complete: MsgDispatcher.dispatch(EVENT_BUILDING_UPDATE)
                 │
                 ▼
           TownView.refresh()
```

### Army March Flow
```
User Opens Rally Point
       │
       ▼
ArmyDialog.show()
       │
       ▼
User Selects:
  - Target coordinates
  - Mission type
  - Hero
  - Troops
  - Resources
       │
       ▼
Sender.sendMessage("army.newArmy", {
  castleId, heroId, targetX, targetY,
  missionType, troops, resource
})
       │
       ▼
[Server Processing]
       │
       ▼
ResponseDispatcher.dispatch(SERVER_SELF_ARMYS_UPDATE)
       │
       ▼
Context.onSelfArmysUpdate(event)
       │
       ├─► PlayerBean.selfArmysArray.addItem(army)
       │
       └─► Context.timerHandler() tracks march
                 │
                 ▼
           When arrived: SERVER_SELF_ARMYS_UPDATE (direction=2)
```

---

## 5. Data Flow Matrix

### Request Path
```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│    UI    │───►│  Sender  │───►│GameClient│───►│  Server  │
│Component │    │  Impl    │    │  Socket  │    │          │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
     │               │               │               │
     │  onClick()    │ sendMessage() │  writeAMF()   │
     │               │               │               │
     ▼               ▼               ▼               ▼
  Params          Validate       Serialize        Process
  Gather           Check           AMF           Command
```

### Response Path
```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  Server  │───►│GameClient│───►│ Response │───►│ Context  │
│          │    │  Socket  │    │Dispatcher│    │          │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
     │               │               │               │
     │   response    │  onData()     │dispatchEvent()│
     │               │               │               │
     ▼               ▼               ▼               ▼
  Generate       Deserialize    Route to        Update
  Response          AMF         Handler          State
                                    │
                                    ▼
                              ┌──────────┐
                              │    UI    │
                              │ Refresh  │
                              └──────────┘
```

---

## 6. State Dependencies

### Castle State Dependencies
```yaml
CastleBean:
  affects:
    - ResourceBar (resource display)
    - TroopList (troop counts)
    - BuildingView (building states)
    - HeroList (hero assignments)
  affected_by:
    - troop.* commands
    - castle.* commands
    - army.* commands
    - interior.* commands
```

### Player State Dependencies
```yaml
PlayerBean:
  affects:
    - AllCastlesView (castle list)
    - AlliancePanel (alliance info)
    - ProfileDialog (player stats)
    - InventoryPanel (items)
  affected_by:
    - castle.newCastle
    - alliance.* commands
    - item.* commands
    - buff.* commands
```

### Army State Dependencies
```yaml
ArmyBean:
  affects:
    - MapView (army markers)
    - ArmyPanel (march list)
    - TroopList (troop availability)
    - HeroList (hero availability)
  affected_by:
    - army.newArmy
    - army.callBackArmy
    - Context.timerHandler (progress)
```

---

## 7. Error Code Cross-Reference

| Error Code | Protocol Context | UI Message | Recovery Action |
|------------|-----------------|------------|-----------------|
| 1 | Generic failure | "Operation failed" | Retry |
| 100 | Invalid params | "Invalid input" | Fix input |
| 200 | Not enough resources | "Insufficient resources" | Wait/gather |
| 201 | Not enough gold | "Need more gold" | Tax/trade |
| 202 | Not enough food | "Need more food" | Farm |
| 300 | Building requirement | "Upgrade X first" | Upgrade prereq |
| 301 | Research requirement | "Research X first" | Research prereq |
| 400 | Hero busy | "Hero is busy" | Wait/use other |
| 401 | No hero available | "No hero available" | Hire/wait |
| 500 | Army limit reached | "Max armies deployed" | Wait for return |
| 600 | Cooldown active | "Please wait" | Wait |
| 700 | Target invalid | "Invalid target" | Choose new target |

---

## 8. Timing Cross-Reference

### Cooldowns
| Action | Cooldown | Bypass |
|--------|----------|--------|
| Train troops | Per barracks queue | Speed items |
| Upgrade building | Building queue | Speed items |
| Research | Single queue | Speed items |
| Send army | None (limit based) | - |
| Tax change | 15 minutes | - |

### Server Timers
| Timer | Interval | Purpose |
|-------|----------|---------|
| Resource tick | 6 minutes | Update resources |
| Army progress | 1 second | Update march % |
| Build progress | 1 second | Update build % |
| Session keepalive | 30 seconds | Maintain connection |

### Client Timers (Context.timerHandler)
| Check | Interval | Updates |
|-------|----------|---------|
| Resource calc | 1 second | ResourceBar |
| Army progress | 1 second | ArmyList |
| Build progress | 1 second | BuildingQueue |
| Buff expiry | 1 second | BuffBar |

---

## 9. Security Cross-Reference

### Encryption Points
| Layer | Method | Key | Purpose |
|-------|--------|-----|---------|
| Login | MD5 hash | LOGIN_SALT | Password hash |
| Request | MD5 signature | ACTION_KEY | Request signing |
| Payload | XOR | 0xAA | Data obfuscation |
| Session | Server-generated | - | Session token |

### Validation Points
| Location | Validation | Bypass Risk |
|----------|------------|-------------|
| Client send | Type check only | High - can modify |
| Server receive | Full validation | Low |
| Response parse | Minimal | Medium |

---

## 10. AutoEvony Variable Cross-Reference

| Variable | Source | Used In |
|----------|--------|---------|
| `%city%` | Current city index | All commands |
| `%hero%` | Current hero ID | Army, hero commands |
| `%coords%` | Target coordinates | Army commands |
| `%gold%` | Current gold | Conditionals |
| `%food%` | Current food | Conditionals |
| `%idle%` | Idle hero count | Conditionals |
| `%troops%` | Troop counts | Conditionals |

---

*Part of Svony MCP - Evony Reverse Engineering Project*
