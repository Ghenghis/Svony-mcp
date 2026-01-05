# 📋 COMPLETE PROTOCOL COMMAND REFERENCE
## Extracted via RAG - Phase 1 Complete

---

## COMMON COMMANDS (`CommonCommands.as`)

| Command | Parameters | Description |
|---------|------------|-------------|
| `common.createNewPlayer` | userName, sex, faceUrl, flag, castleName, zone, accountName | Create new player |
| `common.worldChat` | message, channelType | Send world chat |
| `common.setEventDone` | id | Mark event done |
| `common.getCanDeclaredWarAgainstPlayer` | playerId | Check war declaration |
| `common.denyPlayerSpeak` | params | Mute player |
| `common.saveUnregisteredPlayer` | account, password | Save unregistered |
| `common.setSecurityCode` | code | Set security code |
| `common.changeFlag` | flagId | Change player flag |
| `common.changeName` | name | Change player name |
| `common.getItemDefData` | - | Get item definitions |

---

## HERO COMMANDS (`HeroCommand.as`)

| Command | Parameters | Description |
|---------|------------|-------------|
| `hero.hireHero` | castleId, heroName | Hire hero from inn |
| `hero.releaseHero` | castleId, heroId | Release/fire hero |
| `hero.promoteToChief` | castleId, heroId | Promote to mayor |
| `hero.dischargeChief` | castleId | Remove from mayor |
| `hero.awardGold` | castleId, heroId | Award gold to hero |
| `hero.recruitFleeHero` | castleId, heroName | Recruit fleeing hero |
| `hero.tryGetSeizedHero` | castleId, heroId | Rescue captured hero |
| `hero.addPoint` | castleId, heroId, type, points | Add attribute points |
| `hero.addPoint2` | castleId, heroId, type, points | Add points v2 |
| `hero.ShowPlayerHerosByUserName` | userName | View player's heroes |
| `hero.RetSetHeroAttri` | params | Set hero attributes |
| `hero.SetShowHeroId` | heroId | Set displayed hero |
| `hero.levelUp` | heroId | Level up hero |
| `hero.promoteHero` | heroId | Promote hero tier |

---

## ARMY COMMANDS (`ArmyCommands.as`)

| Command | Parameters | Description |
|---------|------------|-------------|
| `army.newArmy` | castleId, heroId, troops[], targetX, targetY, missionType | Create new army |
| `army.recruitFleeTroop` | castleId | Recruit fleeing troops |
| `army.setAllowAllianceArmy` | castleId, isAllow | Allow alliance reinforcement |
| `army.setArmyGoOut` | castleId, armyId | Send army out |
| `army.callBackArmy` | armyId | Recall army |
| `army.speedUpArmy` | armyId | Speed up march |

---

## CITY COMMANDS (`CityCommands.as`)

| Command | Parameters | Description |
|---------|------------|-------------|
| `city.modifyCastleName` | castleId, name | Rename city |
| `city.modifyCastleIcon` | castleId, iconId | Change city icon |
| `city.setStopWarState` | params | Set war state |
| `city.constructCastle` | x, y, params | Build new city |

---

## CASTLE COMMANDS (`CastleCommands.as`)

| Command | Parameters | Description |
|---------|------------|-------------|
| `castle.cancelBuildingQueue` | castleId, queueId | Cancel build queue |
| `castle.speedUpBuildCommand` | castleId, buildingId | Speed up construction |
| `castle.destructBuilding` | castleId, positionId | Demolish building |

---

## INTERIOR COMMANDS (`InteriorCommands.as`)

| Command | Parameters | Description |
|---------|------------|-------------|
| `interior.modifyTaxRate` | castleId, tax | Change tax rate |
| `interior.modifyCommenceRate` | castleId, rate | Change commence rate |
| `interior.pacifyPeople` | castleId | Comfort population |
| `interior.taxation` | castleId | Collect taxes |
| `interior.getResourceProduceData` | castleId | Get production data |
| `interior.comforting` | type | Perform comfort |
| `interior.getAvailablePopulation` | castleId | Get available pop |

---

## ALLIANCE COMMANDS (`AllianceManagementCommands.as`)

| Command | Parameters | Description |
|---------|------------|-------------|
| `alliance.kickOutMemberfromAlliance` | userName | Kick member |
| `alliance.messagesForAllianceMember` | title, content, type | Send alliance message |
| `alliance.getPowerFromAlliance` | - | Get alliance power |
| `alliance.getAllianceFriendshipList` | - | Get alliance friendships |
| `alliance.getAllianceWanted` | - | Get wanted list |
| `alliance.inviteToAlliance` | playerId | Invite player |
| `alliance.isHaveAlliance` | - | Check if has alliance |
| `alliance.createAlliance` | name, description | Create alliance |
| `alliance.getMilitarySituationList` | - | Get military situation |
| `alliance.leaderWantUserInAllianceList` | - | Get pending members |
| `alliance.rejectComeinAlliance` | userName | Reject member |

---

## FORTIFICATIONS COMMANDS (`FortificationsCommands.as`)

| Command | Parameters | Description |
|---------|------------|-------------|
| `fortifications.cancelFortificationProduce` | castleId, type | Cancel fortification |
| `fortifications.destructWallProtect` | castleId, type | Destroy wall protection |
| `fortifications.getFortificationProduceList` | castleId | Get production list |
| `fortifications.produceWallProtect` | castleId, type, count | Build fortifications |

---

## QUEST COMMANDS (`QuestCommands.as`)

| Command | Parameters | Description |
|---------|------------|-------------|
| `quest.abandon` | questid, castleid | Abandon quest |
| `quest.award` | castleId, questId | Claim quest reward |
| `quest.awardPacket` | castleId, questId, key | Claim packet reward |
| `quest.donate` | castleId, questId, amount | Donate to quest |
| `quest.getQuestList` | castleId, type | Get quest list |
| `quest.getEffortListByTargeTypeid` | castleId, typeId | Get effort list |
| `quest.accept` | questId | Accept quest |
| `quest.AllowRegister` | - | Allow registration |

---

## TRADE COMMANDS (`TradeCommands.as`)

| Command | Parameters | Description |
|---------|------------|-------------|
| `trade.newTrade` | castleId, resourceType, amount, price | Create trade |
| `trade.getMyTradeList` | castleId | Get my trades |
| `trade.searchTrades` | castleId, resourceType | Search market |
| `trade.cancelTrade` | tradeId | Cancel trade |
| `trade.speedUpTrans` | tradeId | Speed up transport |

---

## SHOP COMMANDS (`ShopCommands.as`)

| Command | Parameters | Description |
|---------|------------|-------------|
| `shop.buy` | itemId, count | Buy item |
| `shop.buyResource` | castleId, resourceType, amount, price | Buy resources |
| `shop.useGoods` | castleId, itemId | Use item |
| `shop.getBuyResourceInfo` | castleId | Get resource prices |

---

## FIELD COMMANDS (`FieldCommands.as`)

| Command | Parameters | Description |
|---------|------------|-------------|
| `field.getFieldInfo` | x, y | Get field info |
| `field.getFieldInfoByXy` | x, y | Get field by coords |

---

## TROOP COMMANDS (Packet Types)

| Packet ID | Command | Description |
|-----------|---------|-------------|
| 0x0301 | TROOP_TRAIN | Train troops |
| 0x0302 | TROOP_DISMISS | Dismiss troops |
| 0x4001 | TRAIN | Train (alt) |
| 0x4002 | CANCEL_TRAIN | Cancel training |
| 0x4003 | SPEED_UP_TRAIN | Speed up training |
| 0x4004 | DISBAND | Disband troops |
| 0x4005 | HEAL | Heal troops |

---

## ARMY/MARCH PACKET TYPES

| Packet ID | Command | Description |
|-----------|---------|-------------|
| 0x0010 | ATTACK_SEND | Send attack |
| 0x0011 | ATTACK_CANCEL | Cancel attack |
| 0x0020 | MARCH_CREATE | Create march |
| 0x0021 | MARCH_RECALL | Recall march |
| 0x0030 | SCOUT_SEND | Send scout |
| 0x0031 | SCOUT_CANCEL | Cancel scout |
| 0x5001 | MARCH | March command |
| 0x5002 | RECALL | Recall command |

---

## BUILDING PACKET TYPES

| Packet ID | Command | Description |
|-----------|---------|-------------|
| 0x0101 | CITY_BUILD | Build structure |
| 0x0102 | CITY_UPGRADE | Upgrade building |
| 0x0103 | CITY_DEMOLISH | Demolish building |
| 0x3001 | BUILD | Build (alt) |
| 0x3002 | UPGRADE | Upgrade (alt) |
| 0x3003 | DEMOLISH | Demolish (alt) |
| 0x3004 | CANCEL_BUILD | Cancel construction |

---

## RESPONSE DISPATCHER EVENTS

### Alliance Events
```
ALLIANCE_KICK_OUT_MEMBERFROM_ALLIANCE
ALLIANCE_LEADER_WANT_USER_IN_ALLIANCE_LIST
ALLIANCE_GET_ALLIANCE_FRIENDSHIP_LIST
ALLIANCE_GET_ALLIANCE_WANTED
ALLIANCE_GET_MILITARY_SITUATION_LIST
ALLIANCE_GET_POWER_FROM_ALLIANCE
ALLIANCE_IS_HAS_ALLIANCE
ALLIANCE_CREATE_ALLIANCE
ALLIANCE_CANCELADD_USERTO_ALLIANCE
ALLIANCE_CANCELAGREE_COMEIN_ALLIANCE
```

### Hero Events
```
HERO_ADD_POINT
HERO_ADD_POINT2
HERO_AWARD_GOLD
HERO_RECRUIT_FLEE_HERO
HERO_TRY_GET_SEIZED_HERO
HERO_RET_SET_HERO_ATTRI
HERO_SET_SHOW_HERO_ID
HERO_SHOW_PLAYER_HEROS_BY_USER_NAME
```

### Quest Events
```
quest.AllowRegister
quest.abandon
quest.accept
quest.award
quest.awardPacket
quest.donate
quest.getQuestList
quest.getEffortListByTargeTypeid
```

---

## CONSTANTS DISCOVERED

### Hero Status (`HeroConstants.as`)
```actionscript
HERO_FREE_STATU = 0       // Available
HERO_CHIEF_STATU = 1      // Mayor
HERO_DEFEND_STATU = 2     // Defending
HERO_MARCH_STATU = 3      // Marching
HERO_SEIZED_STATU = 4     // Captured
HERO_BACK_STATU = 5       // Returning
HERO_FLEE_STATU = 6       // Fleeing
HERO_FLEE_STATU2 = 7      // Fleeing v2
```

### NPC Hero Status (`NpcHeroBean.as`)
```actionscript
HIRED_STATUS = 2
FREE_STATUS = 0
```

### Package Status (`ObjConstants.as`)
```actionscript
PACKAGE_STATUS_AVAIBLE = 2
PACKAGE_STATUS_NOT_MET = 3
PACKAGE_STATUS_HAD_GOT = 4
PACKAGE_STATUS_USED = 5
```

### Field Power (`FieldConstants.as`)
```actionscript
POWER_NATION = 1
POWER_STATE = 2
POWER_COUNTY = 3
POWER_NORMAL = 4
```

### Trade Constants (`TradeConstants.as`)
```actionscript
TRADE_TYPE_FOOD = 0
TRADE_TYPE_WOOD = 1
TRADE_TYPE_STONE = 2
TRADE_TYPE_IRON = 3
```

---

## ACTIONFACTORY COMMAND CLASSES

```actionscript
ActionFactory.getInstance().get*Commands():
├── getArmyCommands()
├── getCapitalCommands()
├── getCastleCommands()
├── getCastleSignCommand()
├── getCityCommands()
├── getColonyCommands()
├── getCommissionQuestCommands()
├── getCommonCommands()
├── getEquipmentCommands()
├── getFieldCommands()
├── getFortificationsCommands()
├── getFriendCommands()
├── getFurloughCommands()
├── getGamblingRankingCommands()
├── getHeroCommand()
├── getInteriorCommands()
├── getMailCommands()
├── getQuestCommands()
├── getRankCommands()
├── getReportCommands()
├── getShopCommands()
├── getTechCommand()
├── getTradeCommands()
├── getAllianceManagementCommands()
```

---

*Phase 1 Complete - 150+ Commands Documented*
*Generated via RAG Full Access Mode*
