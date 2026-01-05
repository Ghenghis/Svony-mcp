# Evony Protocol Commands Reference

Complete command reference extracted from 36 command classes.

## Command Categories

### Army Commands
| Command | Description | Parameters |
|---------|-------------|------------|
| `army.getArmyByCity` | Get armies in city | cityId |
| `army.getInjuredTroop` | Get injured troops | cityId |
| `army.getMyArmyInfo` | Get army info | armyId |
| `army.newArmy` | Create new army | cityId, heroId, troops[] |
| `army.disbandArmy` | Disband army | armyId |
| `army.setArmyGoOut` | Send army out | armyId, targetX, targetY |

### Troop Commands
| Command | Description | Parameters |
|---------|-------------|------------|
| `troop.produceTroop` | Train troops | cityId, troopType, num |
| `troop.cancelProduceTroop` | Cancel training | cityId, troopType |
| `troop.disbandTroop` | Disband troops | cityId, troopType, num |
| `troop.getProduceQueue` | Get training queue | cityId |

### Building Commands
| Command | Description | Parameters |
|---------|-------------|------------|
| `castle.newBuilding` | Build structure | cityId, positionId, typeId |
| `castle.upgradeBuilding` | Upgrade building | cityId, positionId |
| `castle.destructBuilding` | Destroy building | cityId, positionId |
| `castle.speedUpBuilding` | Speed up build | cityId, positionId, itemId |

### Hero Commands
| Command | Description | Parameters |
|---------|-------------|------------|
| `hero.tryGetSeizedHero` | Get captured heroes | - |
| `hero.releaseHero` | Release hero | heroId |
| `hero.fireHero` | Dismiss hero | heroId |
| `hero.promoteHero` | Promote hero | heroId |
| `hero.resetAttrPoint` | Reset stats | heroId |
| `hero.addAttrPoint` | Add stat points | heroId, attrType, num |

### Resource Commands
| Command | Description | Parameters |
|---------|-------------|------------|
| `castle.getResourceProduceData` | Get production | cityId |
| `city.taxRate` | Set tax rate | cityId, rate |
| `city.workRate` | Set comfort rate | cityId, rate |

### Alliance Commands
| Command | Description | Parameters |
|---------|-------------|------------|
| `alliance.getMemberList` | Get members | allianceId |
| `alliance.invite` | Invite player | playerName |
| `alliance.kick` | Kick member | memberId |
| `alliance.setTitle` | Set rank | memberId, title |

### Attack Commands
| Command | Description | Parameters |
|---------|-------------|------------|
| `army.attackOtherPlayer` | Attack player | armyId, targetCityId |
| `army.attackNpc` | Attack NPC | armyId, fieldId |
| `army.attackValley` | Attack valley | armyId, fieldId |
| `army.scout` | Scout target | armyId, targetX, targetY |

### Market Commands
| Command | Description | Parameters |
|---------|-------------|------------|
| `shop.buy` | Buy item | itemId, num |
| `shop.sell` | Sell item | itemId, num |
| `trade.createTrade` | Create trade | resourceType, amount, price |
| `trade.cancelTrade` | Cancel trade | tradeId |

## Command Structure

### Request Format
```json
{
  "cmd": "army.newArmy",
  "params": {
    "cityId": 12345,
    "heroId": 67890,
    "troops": [
      {"type": 1, "num": 1000},
      {"type": 2, "num": 500}
    ]
  },
  "sessionKey": "abc123...",
  "signature": "md5hash..."
}
```

### Response Format
```json
{
  "ok": 1,
  "msg": "success",
  "data": {
    "armyId": 99999,
    "status": "marching"
  }
}
```

## Troop Types

| ID | Name | Food Cost | Time (s) |
|----|------|-----------|----------|
| 1 | Worker | 50 | 15 |
| 2 | Warrior | 100 | 30 |
| 3 | Scout | 150 | 45 |
| 4 | Pikeman | 200 | 60 |
| 5 | Swordsman | 250 | 90 |
| 6 | Archer | 350 | 120 |
| 7 | Cavalry | 500 | 180 |
| 8 | Cataphract | 700 | 240 |
| 9 | Transporter | 300 | 90 |
| 10 | Ballista | 1000 | 300 |
| 11 | Battering Ram | 1500 | 360 |
| 12 | Catapult | 3000 | 450 |

## Building Types

| ID | Name | Max Level |
|----|------|-----------|
| 1 | Cottage | 9 |
| 2 | Barracks | 9 |
| 3 | Warehouse | 9 |
| 4 | Walls | 10 |
| 5 | Inn | 9 |
| 6 | Town Hall | 10 |
| 7 | Feasting Hall | 9 |
| 8 | Embassy | 9 |
| 9 | Marketplace | 9 |
| 10 | Academy | 9 |
| 11 | Rally Point | 10 |
| 12 | Beacon Tower | 9 |
| 13 | Forge | 9 |
| 14 | Workshop | 9 |
| 15 | Relief Station | 9 |
| 16 | Stable | 9 |

## Error Codes

| Code | Meaning |
|------|---------|
| -1 | General error |
| -2 | Invalid session |
| -3 | Permission denied |
| -4 | Insufficient resources |
| -5 | Invalid parameters |
| -6 | Rate limited |
| -7 | Target not found |
| -8 | Already in progress |
