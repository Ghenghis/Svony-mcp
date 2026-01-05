# 📊 DATASET GAPS REPORT
## Complete Training Data Audit

**Version:** 1.0  
**RAG Stats:** 166,043 chunks | 55,871 symbols  
**Categories:** source_code, keys, protocol, scripts, exploits

---

# 📈 CURRENT DATASET INVENTORY

## File Distribution

| Category | Files | Quality | Status |
|----------|-------|---------|--------|
| source_code | 7,469 | ✅ Excellent | Complete |
| keys | 1,230 | ✅ Good | Some duplicates |
| scripts | 106 | ✅ Good | Complete |
| protocol | 85 | ✅ Good | Complete |
| exploits | 26 | ✅ Good | Complete |
| documentation | 0 | ❌ Empty | **NEEDS DATA** |
| game_data | 0 | ❌ Empty | **NEEDS DATA** |
| tools | 0 | ❌ Empty | **NEEDS DATA** |
| metadata | 1 | ⚠️ Minimal | Needs expansion |

---

# 🔍 GAP ANALYSIS BY CATEGORY

## 1. PROTOCOL COMMANDS

### ✅ HAVE (Good Coverage)
- 246+ protocol commands documented in `protocol.py`
- 352 commands in `evony_command_center.py`
- Command categories: alliance, army, castle, city, colony, common, field, fortifications, gameclient, hero, interior, quest, report, resource, shop, tech, trade, troop

### ❌ MISSING
| Gap | Priority | Source Needed |
|-----|----------|---------------|
| Command parameter types | HIGH | Extract from AS3 files |
| Response structures | HIGH | ResponseDispatcher analysis |
| Error code mappings per command | MEDIUM | Cross-reference ErrorCode.as |
| Rate limits per command | MEDIUM | Server observation |
| Sequence diagrams | LOW | Manual documentation |

---

## 2. BEAN CLASSES (Data Structures)

### ✅ HAVE (Partial)
- CastleBean, HeroBean, ArmyBean, PlayerInfoBean
- EquipmentBean, ItemBean, TroopBean, BuffBean
- Various response beans

### ❌ MISSING FIELDS EXTRACTION
| Bean | Status | Missing |
|------|--------|---------|
| CastleBean | 70% | Private field mappings |
| HeroBean | 80% | Skill details |
| ArmyBean | 75% | Movement calculations |
| PlayerInfoBean | 60% | Premium features |
| EquipmentBean | 50% | Enhancement formulas |
| QuestBean | 40% | Reward structures |
| ReportBean | 50% | Battle calculations |
| TradeBean | 60% | Market formulas |
| TechBean | 40% | Research requirements |
| ColonyBean | 50% | Colonial mechanics |
| MapCastleBean | 70% | Scout data parsing |

---

## 3. CONSTANTS & ENUMS

### ✅ HAVE (Good)
- ErrorCode (200+ codes)
- TFConstants (troop/fort IDs)
- FieldConstants (map types)
- HeroConstants (status values)
- ObjConstants (mission types)
- BuildingConstants (partial)

### ❌ MISSING
| Constant File | Priority | Issue |
|---------------|----------|-------|
| BuildingConstants.as | HIGH | Not fully extracted |
| ItemConstants.as | HIGH | Item IDs incomplete |
| QuestConstants.as | MEDIUM | Quest types missing |
| BuffConstants.as | MEDIUM | Buff types incomplete |
| AchievementConstants.as | LOW | Not extracted |
| EventConstants.as | LOW | Not extracted |

---

## 4. GAME MECHANICS

### ✅ HAVE
- Battle mechanics (BATTLE_MECHANICS.md)
- Combat formulas (game_logic.py)
- Resource calculations (ResourceCalculator.as)
- Troop stats (TroopStats in game_logic.py)

### ❌ MISSING
| Mechanic | Priority | Details Needed |
|----------|----------|----------------|
| Building upgrade requirements | HIGH | Level-by-level costs |
| Research requirements | HIGH | Tech tree dependencies |
| Hero leveling formulas | HIGH | XP curves |
| Equipment enhancement | MEDIUM | Star upgrade costs |
| NPC troop compositions | MEDIUM | By level |
| Colony mechanics | MEDIUM | Loyalty decay |
| Market pricing formulas | MEDIUM | Supply/demand |
| Event mechanics | LOW | Special events |

---

## 5. AUTOEVONY SPECIFICS

### ✅ HAVE
- Script.as, ScriptCmd.as
- Commands.as (bot commands)
- 106 script examples
- CityState.as, CityManager.as

### ❌ MISSING
| Component | Priority | Details |
|-----------|----------|---------|
| Complete command list | HIGH | All 75+ commands fully documented |
| Variable type mappings | HIGH | $c.property$ paths |
| Error handling patterns | MEDIUM | Common error recovery |
| Advanced script patterns | MEDIUM | Complex automation |
| Configuration options | LOW | Bot settings |

---

## 6. SECURITY & ENCRYPTION

### ✅ HAVE
- All encryption keys documented
- Signature generation methods
- XOR encryption
- MD5 hashing

### ❌ MISSING
| Security Item | Priority | Status |
|---------------|----------|--------|
| AES key variations | MEDIUM | Partially documented |
| Session token structure | MEDIUM | Not fully mapped |
| Anti-cheat detection rules | HIGH | Needs expansion |
| Rate limit thresholds | HIGH | Server-side unknown |
| IP blocking rules | LOW | Not documented |

---

## 7. DOCUMENTATION

### ❌ EMPTY DIRECTORIES (Critical Gaps)

```
Evony_Training_Dataset/
├── documentation/    ← 0 ITEMS - NEEDS POPULATION
├── game_data/        ← 0 ITEMS - NEEDS POPULATION  
└── tools/            ← 0 ITEMS - NEEDS POPULATION
```

### Required Documentation
| Document | Priority | Content |
|----------|----------|---------|
| BUILDING_DATA.json | HIGH | All building types, costs, requirements |
| TROOP_DATA.json | HIGH | All troop stats, costs, training times |
| RESEARCH_DATA.json | HIGH | All tech requirements and effects |
| ITEM_DATA.json | MEDIUM | All items, effects, sources |
| QUEST_DATA.json | MEDIUM | Quest types, requirements, rewards |
| NPC_DATA.json | MEDIUM | NPC levels, troops, loot |
| EVENT_DATA.json | LOW | Special events, rewards |

---

# 📋 DATA QUALITY ISSUES

## 1. Duplicate Files
```
Found duplicate patterns:
- *_1.as, *_2.as variants (decompiler artifacts)
- Multiple JSON files per account
- Redundant documentation versions
```

## 2. Incomplete Extractions
```
Files with partial data:
- Bean classes with obfuscated field names
- Constants files with gaps in sequences
- Protocol files missing parameter details
```

## 3. Junk Data
```
Files to exclude from training:
- topics.py (Python documentation, not Evony)
- Flash framework files (mx.*, flash.*)
- Empty or boilerplate files
```

---

# 🎯 PRIORITY GAPS TO FILL

## P0 - CRITICAL (Must Have)
1. Building requirements (level 1-20 for all types)
2. Research requirements (all tech)
3. Complete Bean field mappings
4. All protocol command parameters
5. game_data/ directory population

## P1 - HIGH (Should Have)
1. Troop training formulas
2. Combat calculation details
3. Hero leveling curves
4. documentation/ directory population
5. Error code complete mapping

## P2 - MEDIUM (Nice to Have)
1. Market pricing formulas
2. Colony mechanics
3. Equipment enhancement
4. Event mechanics
5. tools/ directory with extraction scripts

## P3 - LOW (Optional)
1. Achievement system
2. UI element mappings
3. Localization strings
4. Animation constants
5. Sound effect mappings

---

# 📊 COVERAGE METRICS

```
┌─────────────────────────────────────────────────────────────────────┐
│                    TRAINING DATA COVERAGE                            │
├─────────────────────────────────────────────────────────────────────┤
│ Category              │ Current │ Target │ Gap    │ Priority       │
├───────────────────────┼─────────┼────────┼────────┼────────────────┤
│ Protocol Commands     │   85%   │  100%  │  15%   │ HIGH           │
│ Bean Classes          │   65%   │  100%  │  35%   │ HIGH           │
│ Constants/Enums       │   75%   │  100%  │  25%   │ HIGH           │
│ Game Mechanics        │   50%   │  100%  │  50%   │ CRITICAL       │
│ Script Commands       │   90%   │  100%  │  10%   │ MEDIUM         │
│ Security/Crypto       │   80%   │  100%  │  20%   │ MEDIUM         │
│ Documentation         │   20%   │  100%  │  80%   │ CRITICAL       │
│ Structured Game Data  │    0%   │  100%  │ 100%   │ CRITICAL       │
├───────────────────────┼─────────┼────────┼────────┼────────────────┤
│ OVERALL               │   58%   │  100%  │  42%   │                │
└───────────────────────┴─────────┴────────┴────────┴────────────────┘
```

---

# 🔧 REQUIRED EXTRACTION SCRIPTS

## Script 1: Bean Field Extractor
```python
# Extract all public/private fields from Bean classes
# Map obfuscated names to readable names
# Output: bean_mappings.json
```

## Script 2: Protocol Parameter Extractor
```python
# Extract parameter types from Command classes
# Map command -> parameters -> types
# Output: protocol_parameters.json
```

## Script 3: Game Data Generator
```python
# Generate structured JSON for:
# - Buildings, Troops, Research, Items
# Output: game_data/*.json
```

## Script 4: Constant Consolidator
```python
# Merge all *Constants.as files
# Resolve duplicates and gaps
# Output: all_constants.json
```

## Script 5: Documentation Generator
```python
# Generate markdown docs from source
# Auto-document all extracted data
# Output: documentation/*.md
```

---

*Dataset Gaps Report v1.0*  
*Current Coverage: 58%*  
*Target Coverage: 100%*  
*Estimated Work: 3-5 days with RAG automation*
