# 📐 Enterprise-Grade Data Schemas

Complete schema definitions for all Evony data structures.

---

## 1. Protocol Schemas

### 1.1 Command Request Schema
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "EvonyCommandRequest",
  "type": "object",
  "properties": {
    "cmd": {
      "type": "string",
      "pattern": "^[a-z]+\\.[a-zA-Z]+$",
      "description": "Command in namespace.action format"
    },
    "params": {
      "type": "object",
      "properties": {
        "castleId": {"type": "integer", "minimum": 0},
        "playerId": {"type": "integer", "minimum": 0}
      },
      "additionalProperties": true
    },
    "seq": {
      "type": "integer",
      "description": "Sequence number for request tracking"
    },
    "timestamp": {
      "type": "number",
      "description": "Unix timestamp in milliseconds"
    }
  },
  "required": ["cmd"]
}
```

### 1.2 Command Response Schema
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "EvonyCommandResponse",
  "type": "object",
  "properties": {
    "ok": {
      "type": "integer",
      "enum": [0, 1],
      "description": "1=success, 0=failure"
    },
    "errorCode": {
      "type": "integer",
      "description": "Error code if ok=0"
    },
    "errorMsg": {
      "type": "string",
      "description": "Human-readable error message"
    },
    "data": {
      "type": "object",
      "description": "Response payload"
    },
    "seq": {
      "type": "integer",
      "description": "Matching request sequence"
    }
  },
  "required": ["ok"]
}
```

### 1.3 AMF Packet Schema
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "AMFPacket",
  "type": "object",
  "properties": {
    "version": {
      "type": "integer",
      "enum": [0, 3],
      "description": "AMF version (0 or 3)"
    },
    "headers": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": {"type": "string"},
          "mustUnderstand": {"type": "boolean"},
          "value": {}
        }
      }
    },
    "bodies": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "target": {"type": "string"},
          "response": {"type": "string"},
          "value": {}
        }
      }
    }
  }
}
```

---

## 2. Game Entity Schemas

### 2.1 CastleBean Schema
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "CastleBean",
  "type": "object",
  "properties": {
    "id": {"type": "integer", "description": "Unique castle ID"},
    "name": {"type": "string", "maxLength": 20},
    "status": {"type": "integer", "enum": [0, 1, 2]},
    "x": {"type": "integer", "minimum": 0, "maximum": 799},
    "y": {"type": "integer", "minimum": 0, "maximum": 799},
    "powerlevel": {"type": "integer", "minimum": 1, "maximum": 10},
    "resource": {"$ref": "#/definitions/CastleResourceBean"},
    "troop": {"$ref": "#/definitions/TroopBean"},
    "fortification": {"$ref": "#/definitions/FortificationBean"},
    "buildingsArray": {
      "type": "array",
      "items": {"$ref": "#/definitions/BuildingBean"}
    },
    "buildingQueuesArray": {
      "type": "array",
      "items": {"$ref": "#/definitions/BuildingQueueBean"}
    },
    "fieldsArray": {
      "type": "array",
      "items": {"$ref": "#/definitions/FieldBean"}
    }
  },
  "definitions": {
    "CastleResourceBean": {
      "type": "object",
      "properties": {
        "gold": {"$ref": "#/definitions/ResourceAmount"},
        "food": {"$ref": "#/definitions/ResourceAmount"},
        "wood": {"$ref": "#/definitions/ResourceAmount"},
        "stone": {"$ref": "#/definitions/ResourceAmount"},
        "iron": {"$ref": "#/definitions/ResourceAmount"},
        "troopCostFood": {"type": "number"},
        "colonyFood": {"type": "number"},
        "supplyFood": {"type": "number"}
      }
    },
    "ResourceAmount": {
      "type": "object",
      "properties": {
        "amount": {"type": "number"},
        "maxAmount": {"type": "number"},
        "increaseRate": {"type": "number"}
      }
    },
    "TroopBean": {
      "type": "object",
      "properties": {
        "worker": {"type": "integer", "minimum": 0},
        "warrior": {"type": "integer", "minimum": 0},
        "scout": {"type": "integer", "minimum": 0},
        "pikeman": {"type": "integer", "minimum": 0},
        "swordsman": {"type": "integer", "minimum": 0},
        "archer": {"type": "integer", "minimum": 0},
        "cavalry": {"type": "integer", "minimum": 0},
        "cataphract": {"type": "integer", "minimum": 0},
        "transporter": {"type": "integer", "minimum": 0},
        "ballista": {"type": "integer", "minimum": 0},
        "ram": {"type": "integer", "minimum": 0},
        "catapult": {"type": "integer", "minimum": 0}
      }
    },
    "FortificationBean": {
      "type": "object",
      "properties": {
        "trap": {"type": "integer"},
        "abatis": {"type": "integer"},
        "archerTower": {"type": "integer"},
        "rollingLog": {"type": "integer"},
        "trebuche": {"type": "integer"}
      }
    },
    "BuildingBean": {
      "type": "object",
      "properties": {
        "positionId": {"type": "integer"},
        "typeId": {"type": "integer", "minimum": 0, "maximum": 35},
        "level": {"type": "integer", "minimum": 0, "maximum": 10},
        "status": {"type": "integer"},
        "startTime": {"type": "number"},
        "endTime": {"type": "number"},
        "name": {"type": "string"}
      }
    },
    "BuildingQueueBean": {
      "type": "object",
      "properties": {
        "positionId": {"type": "integer"},
        "typeId": {"type": "integer"},
        "endTime": {"type": "number"}
      }
    },
    "FieldBean": {
      "type": "object",
      "properties": {
        "id": {"type": "integer"},
        "typeId": {"type": "integer"},
        "level": {"type": "integer"}
      }
    }
  }
}
```

### 2.2 PlayerBean Schema
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "PlayerBean",
  "type": "object",
  "properties": {
    "playerId": {"type": "integer"},
    "name": {"type": "string"},
    "allianceId": {"type": "integer"},
    "allianceName": {"type": "string"},
    "prestige": {"type": "number"},
    "honor": {"type": "number"},
    "rank": {"type": "integer"},
    "title": {"type": "string"},
    "sex": {"type": "integer", "enum": [0, 1]},
    "flag": {"type": "string"},
    "castlesArray": {
      "type": "array",
      "items": {"$ref": "CastleBean"}
    },
    "itemsArray": {
      "type": "array",
      "items": {"$ref": "#/definitions/ItemBean"}
    },
    "buffsArray": {
      "type": "array",
      "items": {"$ref": "#/definitions/BuffBean"}
    }
  },
  "definitions": {
    "ItemBean": {
      "type": "object",
      "properties": {
        "itemId": {"type": "integer"},
        "count": {"type": "integer"},
        "itemDefId": {"type": "integer"}
      }
    },
    "BuffBean": {
      "type": "object",
      "properties": {
        "typeId": {"type": "string"},
        "value": {"type": "number"},
        "endTime": {"type": "number"}
      }
    }
  }
}
```

### 2.3 HeroBean Schema
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "HeroBean",
  "type": "object",
  "properties": {
    "id": {"type": "integer"},
    "name": {"type": "string", "maxLength": 16},
    "level": {"type": "integer", "minimum": 1, "maximum": 100},
    "experience": {"type": "number"},
    "status": {
      "type": "string",
      "enum": ["idle", "marching", "defending", "mayor", "captured"]
    },
    "power": {"type": "integer"},
    "politics": {"type": "integer"},
    "attack": {"type": "integer"},
    "intelligence": {"type": "integer"},
    "loyalty": {"type": "integer", "minimum": 0, "maximum": 100},
    "energy": {"type": "integer", "minimum": 0, "maximum": 100},
    "grade": {"type": "integer"},
    "itemSlots": {
      "type": "object",
      "properties": {
        "weapon": {"$ref": "#/definitions/EquipmentSlot"},
        "armor": {"$ref": "#/definitions/EquipmentSlot"},
        "helmet": {"$ref": "#/definitions/EquipmentSlot"},
        "accessory": {"$ref": "#/definitions/EquipmentSlot"}
      }
    }
  },
  "definitions": {
    "EquipmentSlot": {
      "type": "object",
      "properties": {
        "itemId": {"type": "integer"},
        "stars": {"type": "integer"},
        "enchant": {"type": "integer"}
      }
    }
  }
}
```

### 2.4 ArmyBean Schema
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "ArmyBean",
  "type": "object",
  "properties": {
    "armyId": {"type": "integer"},
    "playerId": {"type": "integer"},
    "playerName": {"type": "string"},
    "startPosName": {"type": "string"},
    "targetPosName": {"type": "string"},
    "startPos": {"$ref": "#/definitions/Coordinate"},
    "targetPos": {"$ref": "#/definitions/Coordinate"},
    "missionType": {
      "type": "integer",
      "enum": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
      "description": "1=attack,2=reinforce,3=scout,4=transport,5=camp..."
    },
    "direction": {
      "type": "integer",
      "enum": [1, 2],
      "description": "1=going, 2=returning"
    },
    "hero": {"$ref": "HeroBean"},
    "troop": {"$ref": "TroopBean"},
    "resource": {
      "type": "object",
      "properties": {
        "gold": {"type": "number"},
        "food": {"type": "number"},
        "wood": {"type": "number"},
        "stone": {"type": "number"},
        "iron": {"type": "number"}
      }
    },
    "startTime": {"type": "number"},
    "reachTime": {"type": "number"}
  },
  "definitions": {
    "Coordinate": {
      "type": "object",
      "properties": {
        "x": {"type": "integer", "minimum": 0, "maximum": 799},
        "y": {"type": "integer", "minimum": 0, "maximum": 799}
      }
    }
  }
}
```

---

## 3. Game Data Schemas

### 3.1 Building Definition Schema
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "BuildingDefinition",
  "type": "object",
  "properties": {
    "typeId": {"type": "integer"},
    "name": {"type": "string"},
    "category": {
      "type": "string",
      "enum": ["resource", "military", "defense", "special"]
    },
    "maxLevel": {"type": "integer", "default": 10},
    "isInner": {"type": "boolean"},
    "positionRange": {
      "type": "object",
      "properties": {
        "min": {"type": "integer"},
        "max": {"type": "integer"}
      }
    },
    "levels": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "level": {"type": "integer"},
          "costs": {
            "type": "object",
            "properties": {
              "gold": {"type": "integer"},
              "food": {"type": "integer"},
              "wood": {"type": "integer"},
              "stone": {"type": "integer"},
              "iron": {"type": "integer"},
              "time": {"type": "integer", "description": "seconds"}
            }
          },
          "requirements": {
            "type": "object",
            "properties": {
              "townhall": {"type": "integer"},
              "research": {"type": "array", "items": {"type": "string"}}
            }
          },
          "production": {
            "type": "object",
            "properties": {
              "resourceType": {"type": "string"},
              "rate": {"type": "number", "description": "per hour"}
            }
          },
          "capacity": {"type": "integer"},
          "effect": {"type": "string"}
        }
      }
    }
  }
}
```

### 3.2 Troop Definition Schema
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "TroopDefinition",
  "type": "object",
  "properties": {
    "typeId": {"type": "integer", "minimum": 0, "maximum": 11},
    "name": {"type": "string"},
    "tier": {"type": "integer", "minimum": 1, "maximum": 4},
    "category": {
      "type": "string",
      "enum": ["infantry", "ranged", "cavalry", "siege", "support"]
    },
    "training": {
      "type": "object",
      "properties": {
        "building": {"type": "string"},
        "buildingLevel": {"type": "integer"},
        "food": {"type": "integer"},
        "gold": {"type": "integer"},
        "population": {"type": "integer"},
        "time": {"type": "integer", "description": "seconds base"}
      }
    },
    "stats": {
      "type": "object",
      "properties": {
        "attack": {"type": "integer"},
        "defense": {"type": "integer"},
        "life": {"type": "integer"},
        "speed": {"type": "number"},
        "range": {"type": "integer"},
        "load": {"type": "integer"}
      }
    },
    "upkeep": {
      "type": "object",
      "properties": {
        "food": {"type": "number", "description": "per hour"}
      }
    },
    "requirements": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "type": {"type": "string", "enum": ["research", "building"]},
          "id": {"type": "string"},
          "level": {"type": "integer"}
        }
      }
    }
  }
}
```

### 3.3 Research Definition Schema
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "ResearchDefinition",
  "type": "object",
  "properties": {
    "techId": {"type": "string"},
    "name": {"type": "string"},
    "category": {
      "type": "string",
      "enum": ["military", "resource", "production", "defense"]
    },
    "maxLevel": {"type": "integer"},
    "levels": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "level": {"type": "integer"},
          "costs": {
            "type": "object",
            "properties": {
              "gold": {"type": "integer"},
              "food": {"type": "integer"},
              "wood": {"type": "integer"},
              "stone": {"type": "integer"},
              "iron": {"type": "integer"},
              "time": {"type": "integer"}
            }
          },
          "requirements": {
            "type": "object",
            "properties": {
              "academy": {"type": "integer"},
              "prerequisites": {
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "techId": {"type": "string"},
                    "level": {"type": "integer"}
                  }
                }
              }
            }
          },
          "effect": {
            "type": "object",
            "properties": {
              "stat": {"type": "string"},
              "modifier": {"type": "string", "enum": ["add", "multiply"]},
              "value": {"type": "number"}
            }
          }
        }
      }
    }
  }
}
```

---

## 4. Command Schemas (Examples)

### 4.1 troop.produceTroop
```json
{
  "command": "troop.produceTroop",
  "request": {
    "type": "object",
    "properties": {
      "castleId": {"type": "integer", "required": true},
      "troopType": {"type": "integer", "minimum": 0, "maximum": 11, "required": true},
      "num": {"type": "integer", "minimum": 1, "maximum": 2147483647, "required": true},
      "conscpipt": {"type": "boolean", "default": false}
    }
  },
  "response": {
    "type": "object",
    "properties": {
      "ok": {"type": "integer"},
      "packageId": {"type": "integer"},
      "coolDownTime": {"type": "number"}
    }
  }
}
```

### 4.2 army.newArmy
```json
{
  "command": "army.newArmy",
  "request": {
    "type": "object",
    "properties": {
      "castleId": {"type": "integer", "required": true},
      "heroId": {"type": "integer", "required": true},
      "targetX": {"type": "integer", "minimum": 0, "maximum": 799, "required": true},
      "targetY": {"type": "integer", "minimum": 0, "maximum": 799, "required": true},
      "missionType": {"type": "integer", "minimum": 1, "maximum": 10, "required": true},
      "troops": {
        "type": "string",
        "pattern": "^(\\d+,)+\\d+$",
        "description": "Comma-separated troop counts: w,wa,s,p,sw,a,c,ca,t,b,r,cp"
      },
      "resource": {
        "type": "string",
        "pattern": "^(\\d+,)+\\d+$",
        "description": "Comma-separated resources: g,f,w,s,i"
      }
    }
  },
  "response": {
    "type": "object",
    "properties": {
      "ok": {"type": "integer"},
      "armyId": {"type": "integer"}
    }
  }
}
```

### 4.3 castle.upgradeBuilding
```json
{
  "command": "castle.upgradeBuilding",
  "request": {
    "type": "object",
    "properties": {
      "castleId": {"type": "integer", "required": true},
      "positionId": {"type": "integer", "required": true}
    }
  },
  "response": {
    "type": "object",
    "properties": {
      "ok": {"type": "integer"},
      "errorCode": {"type": "integer"},
      "coolDownTime": {"type": "number"}
    }
  }
}
```

---

## 5. Event Schemas

### 5.1 Server Push Event Schema
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "ServerPushEvent",
  "type": "object",
  "properties": {
    "eventType": {
      "type": "string",
      "enum": [
        "SERVER_BUILD_COMPLATE",
        "SERVER_TROOP_UPDATE",
        "SERVER_RESOURCE_UPDATE",
        "SERVER_HERO_UPDATE",
        "SERVER_ITEM_UPDATE",
        "SERVER_SELF_ARMYS_UPDATE",
        "SERVER_ENEMY_ARMYS_UPDATE"
      ]
    },
    "updateType": {
      "type": "integer",
      "enum": [1, 2, 3],
      "description": "1=ADD, 2=UPDATE, 3=DELETE"
    },
    "castleId": {"type": "integer"},
    "data": {"type": "object"}
  }
}
```

---

## 6. Validation Rules

### Integer Bounds
```yaml
int32_max: 2147483647
int32_min: -2147483648
uint32_max: 4294967295

# Safe overflow thresholds
troop_overflow_threshold:
  archer: 6135037      # INT32_MAX / 350 + 1
  worker: 42949673     # INT32_MAX / 50 + 1
  catapult: 715828     # INT32_MAX / 3000 + 1
```

### String Lengths
```yaml
player_name: {min: 3, max: 20}
castle_name: {min: 1, max: 20}
hero_name: {min: 1, max: 16}
alliance_name: {min: 3, max: 20}
chat_message: {max: 200}
```

### Coordinate Bounds
```yaml
map_x: {min: 0, max: 799}
map_y: {min: 0, max: 799}
position_id_inner: {min: 1000, max: 1040}
position_id_outer: {min: 1, max: 40}
```

---

*Part of Svony MCP - Evony Reverse Engineering Project*
