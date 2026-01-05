# 🚀 TRAINING DATA COMPLETION ACTION PLAN
## RAG-Powered Dataset Enhancement

**Goal:** Complete all gaps for professional training dataset  
**Current Coverage:** 58% → **Target:** 100%  
**Timeline:** 3-5 days with automation

---

# 📋 PHASE OVERVIEW

| Phase | Task | Days | Priority |
|-------|------|------|----------|
| 1 | Bean Field Extraction | 1 | CRITICAL |
| 2 | Protocol Parameter Mapping | 1 | CRITICAL |
| 3 | Game Data Generation | 1-2 | CRITICAL |
| 4 | Constant Consolidation | 0.5 | HIGH |
| 5 | Documentation Generation | 0.5-1 | HIGH |
| 6 | Quality Assurance | 0.5 | HIGH |

---

# PHASE 1: BEAN FIELD EXTRACTION

## Objective
Extract all fields from Bean classes with proper type mappings

## RAG Queries
```python
# Query 1: Find all Bean classes
evony_search("class extends BaseBean public var", k=100)

# Query 2: Extract field patterns
evony_search("public var private var _[0-9]+ getter setter", k=100)

# Query 3: Find obfuscated mappings
evony_search("Bindable propertyChange get set function", k=100)
```

## Target Beans (Priority Order)
1. CastleBean.as - Castle data
2. HeroBean.as - Hero data
3. ArmyBean.as - Army data
4. PlayerInfoBean.as - Player data
5. BuildingBean.as - Building data
6. TroopBean.as / TroopStrBean.as - Troop data
7. ResourceBean.as - Resources
8. EquipmentBean.as - Equipment
9. ItemBean.as - Items
10. QuestBean.as - Quests
11. ReportBean.as - Reports
12. TradeBean.as - Trade
13. TechBean.as - Research
14. ColonyBean.as - Colony
15. BuffBean.as - Buffs
16. MailBean.as - Mail
17. MapCastleBean.as - Map data

## Output Format
```json
{
  "CastleBean": {
    "fields": {
      "castleId": {"type": "int", "description": "Unique castle ID"},
      "name": {"type": "String", "description": "Castle name"},
      "fieldId": {"type": "int", "description": "Map field ID"},
      ...
    },
    "methods": [...],
    "source_file": "CastleBean.as"
  }
}
```

---

# PHASE 2: PROTOCOL PARAMETER MAPPING

## Objective
Map all protocol commands to their parameters and types

## RAG Queries
```python
# Query 1: Find all command definitions
evony_search("public function Sender.instance cmd", k=100)

# Query 2: Find parameter patterns
evony_search("function [a-zA-Z]+Command param params Array Object", k=100)

# Query 3: Find response handlers
evony_search("respMap ResponseDispatcher addEventListener", k=100)
```

## Command Categories to Extract
```
alliance (28 commands)
army (35 commands)
castle (25 commands)
city (15 commands)
colony (10 commands)
common (30 commands)
field (20 commands)
fortifications (10 commands)
hero (25 commands)
interior (15 commands)
quest (20 commands)
report (15 commands)
shop (20 commands)
tech (15 commands)
trade (15 commands)
troop (20 commands)
```

## Output Format
```json
{
  "commands": {
    "army.newArmy": {
      "category": "army",
      "parameters": [
        {"name": "cityId", "type": "int", "required": true},
        {"name": "heroId", "type": "int", "required": true},
        {"name": "troops", "type": "Object", "required": true},
        {"name": "targetX", "type": "int", "required": true},
        {"name": "targetY", "type": "int", "required": true}
      ],
      "response": "server.ArmyResponse",
      "errors": [-4, -50, -134]
    }
  }
}
```

---

# PHASE 3: GAME DATA GENERATION

## Objective
Create structured JSON files for all game data

## 3.1 Building Data
```python
# RAG Query
evony_search("building type level cost food wood stone iron time requirement", k=50)
```

### Output: `game_data/buildings.json`
```json
{
  "buildings": {
    "townhall": {
      "id": 1,
      "name": "Town Hall",
      "max_level": 10,
      "levels": {
        "1": {"food": 100, "wood": 200, "stone": 50, "iron": 0, "time": 60},
        "2": {"food": 200, "wood": 400, "stone": 100, "iron": 0, "time": 180},
        ...
      },
      "requirements": {"townhall": 0},
      "effects": {"unlock_buildings": true, "max_cities": 1}
    }
  }
}
```

## 3.2 Troop Data
```python
# RAG Query
evony_search("troop stats attack defense life speed range cost population train", k=50)
```

### Output: `game_data/troops.json`
```json
{
  "troops": {
    "worker": {
      "id": 2,
      "name": "Worker",
      "tier": 1,
      "type": "support",
      "stats": {
        "attack": 5, "defense": 5, "life": 50,
        "speed": 180, "range": 20, "load": 200
      },
      "cost": {"food": 50, "wood": 0, "stone": 0, "iron": 0, "gold": 0},
      "population": 1,
      "train_time": 15,
      "requirements": {"barracks": 1}
    }
  }
}
```

## 3.3 Research Data
```python
# RAG Query
evony_search("research tech requirement level academy cost effect bonus", k=50)
```

### Output: `game_data/research.json`
```json
{
  "research": {
    "military_science": {
      "id": 1,
      "name": "Military Science",
      "category": "military",
      "max_level": 10,
      "levels": {
        "1": {"food": 500, "wood": 500, "stone": 0, "iron": 200, "time": 300},
        ...
      },
      "requirements": {"academy": 1},
      "effects": {"troop_attack": "+1%"}
    }
  }
}
```

## 3.4 Item Data
```python
# RAG Query
evony_search("item type effect use consume equipment chest package", k=50)
```

## 3.5 NPC Data
```python
# RAG Query  
evony_search("npc level troops valley flat forest hill lake", k=50)
```

---

# PHASE 4: CONSTANT CONSOLIDATION

## Objective
Merge all constants into unified reference

## RAG Queries
```python
# Query 1: All constant files
evony_search("public static const int String", k=100)

# Query 2: Error codes
evony_search("ErrorCode public static const int = -", k=50)

# Query 3: Building/troop/item IDs
evony_search("Constants typeId buildingId troopId itemId", k=50)
```

## Output: `game_data/all_constants.json`
```json
{
  "error_codes": {
    "-1": "GENERAL_ERROR",
    "-2": "INVALID_PARAMS",
    ...
  },
  "building_types": {
    "1": "TOWNHALL",
    "2": "BARRACKS",
    ...
  },
  "troop_types": {
    "2": "WORKER",
    "3": "WARRIOR",
    ...
  },
  "item_types": {...},
  "quest_types": {...},
  "hero_status": {...},
  "army_mission": {...}
}
```

---

# PHASE 5: DOCUMENTATION GENERATION

## Objective
Auto-generate comprehensive documentation

## Documents to Create

### 5.1 API Reference
```markdown
# Evony Protocol API Reference
- All commands with parameters
- Response structures
- Error handling
```

### 5.2 Data Model Reference
```markdown
# Evony Data Model Reference
- All Bean classes
- Field descriptions
- Relationships
```

### 5.3 Game Mechanics Reference
```markdown
# Evony Game Mechanics Reference
- Combat formulas
- Resource formulas
- Progression curves
```

### 5.4 Bot Scripting Guide
```markdown
# AutoEvony Scripting Guide
- All commands
- Variable system
- Examples
```

---

# PHASE 6: QUALITY ASSURANCE

## 6.1 Data Validation
```python
# Validate JSON structure
# Check for duplicates
# Verify completeness
# Cross-reference accuracy
```

## 6.2 Junk Removal
```python
# Files to exclude from training:
EXCLUDE_PATTERNS = [
    "topics.py",           # Python docs
    "mx.*",                # Flex framework
    "flash.*",             # Flash framework  
    "*_Tests.as",          # Test files
    "*.pyc",               # Compiled Python
    "*.swf",               # Binary SWF
]
```

## 6.3 Deduplication
```python
# Remove duplicate Bean versions (*_1.as, *_2.as)
# Consolidate JSON account files
# Merge redundant documentation
```

---

# 🛠️ AUTOMATION SCRIPTS

## Script: rag_dataset_completer.py
```python
"""
RAG-Powered Dataset Completion Script
Uses evony-knowledge MCP to fill all gaps
"""

class DatasetCompleter:
    def __init__(self):
        self.rag = EvonyRAG()
        
    def extract_beans(self):
        """Phase 1: Extract all Bean fields"""
        pass
        
    def map_protocols(self):
        """Phase 2: Map all protocol commands"""
        pass
        
    def generate_game_data(self):
        """Phase 3: Generate structured game data"""
        pass
        
    def consolidate_constants(self):
        """Phase 4: Consolidate all constants"""
        pass
        
    def generate_docs(self):
        """Phase 5: Generate documentation"""
        pass
        
    def quality_check(self):
        """Phase 6: QA and cleanup"""
        pass
```

---

# 📊 SUCCESS METRICS

| Metric | Current | Target | Measurement |
|--------|---------|--------|-------------|
| Bean Coverage | 65% | 100% | Fields extracted / Total fields |
| Protocol Coverage | 85% | 100% | Commands documented / Total commands |
| Game Data Files | 0 | 7 | JSON files in game_data/ |
| Documentation Files | 0 | 5 | MD files in documentation/ |
| Data Quality Score | 70% | 95% | Validated / Total entries |
| Duplicate Ratio | 15% | <2% | Duplicates / Total files |

---

# 📅 EXECUTION TIMELINE

```
Day 1: Phase 1 (Beans) + Phase 2 (Protocols)
Day 2: Phase 3 (Game Data - Part 1)
Day 3: Phase 3 (Game Data - Part 2) + Phase 4 (Constants)
Day 4: Phase 5 (Documentation)
Day 5: Phase 6 (QA) + Final Review
```

---

# ✅ CHECKLIST

## Phase 1 - Bean Extraction
- [ ] CastleBean fields
- [ ] HeroBean fields
- [ ] ArmyBean fields
- [ ] All 17 target beans
- [ ] Field type mappings
- [ ] Output bean_mappings.json

## Phase 2 - Protocol Mapping
- [ ] Alliance commands
- [ ] Army commands
- [ ] All 16 categories
- [ ] Parameter types
- [ ] Response mappings
- [ ] Output protocol_parameters.json

## Phase 3 - Game Data
- [ ] buildings.json
- [ ] troops.json
- [ ] research.json
- [ ] items.json
- [ ] npcs.json
- [ ] quests.json
- [ ] events.json

## Phase 4 - Constants
- [ ] Error codes complete
- [ ] Building IDs complete
- [ ] Troop IDs complete
- [ ] All constants merged
- [ ] Output all_constants.json

## Phase 5 - Documentation
- [ ] API Reference
- [ ] Data Model Reference
- [ ] Game Mechanics Guide
- [ ] Scripting Guide
- [ ] README updates

## Phase 6 - QA
- [ ] JSON validation
- [ ] Duplicate removal
- [ ] Junk cleanup
- [ ] Coverage verification
- [ ] Final manifest update

---

*Training Data Action Plan v1.0*  
*Estimated Completion: 5 days*  
*Automation Level: 80% RAG-assisted*
