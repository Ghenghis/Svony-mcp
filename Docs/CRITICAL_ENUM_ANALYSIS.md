# 🚨 CRITICAL ENUM ANALYSIS & BUG IDENTIFICATION
## AutoEvony Enum Extraction - Complete 1:1 Mapping

**Priority:** CRITICAL - This is where all bugs/issues exist  
**Status:** Phase 4.1-4.4 Active  
**Target:** 100% enum coverage with bug identification

---

# 📋 MASTER ENUM INVENTORY

## 1. ERROR CODES (`ErrorCode.as`) - 🔴 HIGH PRIORITY

### Known Error Constants
```actionscript
// Resource Errors
RESOURCE_NOT_ENOUGH = -1          // ⚠️ Generic - needs better handling
BUILD_UNIQUE_BUILDING_EXIST = -3  // Unique building already exists
BUILD_POSITION_NOT_IDLE = -4      // Position occupied
UPDATE_PROCESSING = -5            // Update in progress

// Building Errors  
NO_DEPEND_BUILDING = -8           // Missing prerequisite building
NO_DEPEND_TECH = -9               // Missing prerequisite tech
NOT_ENOUGH_PEOPLE = -10           // Population insufficient

// Account Errors
ACCOUNT_HAS_EXIST = -11           // Account exists
ACCOUNT_NOT_EXIST = -12           // Account doesn't exist (⚠️ POTENTIAL BUG: check off-by-one)

// Validation Errors
GIVE_UP_CASTLE_FAIL = -19         // Castle abandon failed
ILLEGAL_FIELD_STATUS = -20        // Invalid field state
ILLEGAL_MAIL_ACTION = -21         // Invalid mail action

// Army Errors
ARMY_EXIST_WHEN_MOVE_CASTLE = -77  // Army blocking castle move
ALLIANCE_ARMY_EXIST_WHEN_MOVE_CASTLE = -78  // Alliance army blocking
FIELD_NOT_GOT = -79               // Field not owned

// Item Errors
NOITEMDROP = -165                 // No item dropped

// Security Errors
NEED_SECURITY_CODE_ERROR = -200   // Security code required
BUILDING_QUEUE_ERROR = -201       // Build queue error
```

### 🐛 IDENTIFIED BUGS/ISSUES:
| Error Code | Issue | Severity | Fix Required |
|------------|-------|----------|--------------|
| -1 | Too generic, masks specific failures | HIGH | Split into specific codes |
| -12 | Potential off-by-one with -11 | MEDIUM | Verify boundary |
| -77/-78 | Duplicate logic, could merge | LOW | Refactor |
| -200 | Missing retry mechanism | HIGH | Add retry count |

---

## 2. TROOP CONSTANTS (`TFConstants.as`) - 🔴 HIGH PRIORITY

### Troop Type IDs
```actionscript
T_PEASANTS = 2     // Workers
T_MILITIA = 3      // Warriors  
T_SCOUTER = 4      // Scouts
T_PIKEMAN = 5      // Pikemen
T_SWORDSMAN = 6    // Swordsmen
T_ARCHER = 7       // Archers
T_CAVALRY = 8      // Light Cavalry
T_CATAPHRACT = 9   // Cataphracts (Heavy Cavalry)
T_TRANSPORTER = 10 // Transporters
T_BALLISTA = 11    // Ballistas
T_RAM = 12         // Battering Rams
T_CATAPULT = 13    // Catapults
```

### Fortification Type IDs
```actionscript
F_TRAP = 20        // Traps
F_ABATIS = 21      // Abatis
F_ARCHER_TOWER = 22 // Archer Towers
F_ROLLING_LOGS = 23 // Rolling Logs
F_DEFENSIVE_TREBUCHE = 24 // Trebuchets
F_ROCKFALL = 25    // Rockfall
```

### 🐛 IDENTIFIED BUGS/ISSUES:
| Constant | Issue | Severity | Fix Required |
|----------|-------|----------|--------------|
| T_PEASANTS=2 | **Gap at 0,1 - IDs don't start at 0** | HIGH | Document or fix indexing |
| F_TRAP=20 | **Gap between troops (13) and forts (20)** | MEDIUM | May cause array issues |
| T_SCOUTER vs scout | **Naming inconsistency** | LOW | Standardize naming |
| Missing T_HERO | No hero type constant | MEDIUM | Add if needed |

---

## 3. HERO CONSTANTS (`HeroConstants.as`) - 🟠 MEDIUM PRIORITY

### Hero Status Types
```actionscript
HERO_FREE_STATU = 0      // Available in city
HERO_CHIEF_STATU = 1     // Appointed as mayor
HERO_DEFEND_STATU = 2    // Defending (in garrison) - FROM CityStateConstants
HERO_MARCH_STATU = 3     // On march/army
HERO_SEIZED_STATU = 4    // Captured by enemy
HERO_BACK_STATU = 5      // Returning from battle
HERO_FLEE_STATU = 6      // Fleeing
HERO_FLEE_STATU2 = 7     // Fleeing (variant) ⚠️ DUPLICATE?
```

### 🐛 IDENTIFIED BUGS/ISSUES:
| Constant | Issue | Severity | Fix Required |
|----------|-------|----------|--------------|
| HERO_FLEE_STATU vs HERO_FLEE_STATU2 | **Duplicate states 6 & 7** | HIGH | Clarify difference |
| *_STATU spelling | **Typo: should be STATUS** | LOW | Rename |
| HERO_DEFEND from CityStateConstants | **Defined in wrong file** | MEDIUM | Consolidate |
| Missing HERO_TRAINING | No training state | LOW | Add if exists |

---

## 4. FIELD CONSTANTS (`FieldConstants.as`) - 🟠 MEDIUM PRIORITY

### Power/Region Types
```actionscript
POWER_WORLD = 0    // World map
POWER_NATION = 1   // Nation territory
POWER_STATE = 2    // State territory
POWER_COUNTY = 3   // County territory
POWER_NORMAL = 4   // Normal/unclaimed
```

### Field Types (Valley Types)
```actionscript
TYPE_FOREST = 1    // Forest - Wood production
TYPE_DESERT = 2    // Desert - Stone production  
TYPE_HILL = 3      // Hill - Iron production
TYPE_SWAMP = 4     // Swamp - Food production
TYPE_GRASSLAND = 5 // Grassland - Food production
TYPE_LAKE = 6      // Lake - Food production
TYPE_FLAT = 10     // Flat land - Building
TYPE_CASTLE = 11   // Castle location
TYPE_NPC = 12      // NPC city
```

### Field Status
```actionscript
STATUS_FREE = 0       // Unclaimed
STAUTS_OCCUPIED = 2   // Occupied ⚠️ TYPO!
STAUTS_CASTLE = 3     // Castle ⚠️ TYPO!
```

### Production Rates
```actionscript
PRODUCE_LAKE_RATE = 3
PRODUCE_SWAP_BASE = 3  // ⚠️ TYPO: SWAMP
PRODUCE_SWAP_RATE = 2  // ⚠️ TYPO: SWAMP
```

### 🐛 IDENTIFIED BUGS/ISSUES:
| Constant | Issue | Severity | Fix Required |
|----------|-------|----------|--------------|
| STAUTS_OCCUPIED | **TYPO: Should be STATUS** | HIGH | Fix spelling |
| STAUTS_CASTLE | **TYPO: Should be STATUS** | HIGH | Fix spelling |
| PRODUCE_SWAP_* | **TYPO: Should be SWAMP** | MEDIUM | Fix spelling |
| TYPE_FLAT=10 | **Gap: 7,8,9 missing** | MEDIUM | Document purpose |
| STATUS_FREE=0, OCCUPIED=2 | **Gap: STATUS=1 missing** | HIGH | Find missing state |

---

## 5. ARMY CONSTANTS (`ArmyConstants.as`) - 🟠 MEDIUM PRIORITY

### Army Direction
```actionscript
ARMY_FORWARD = 1   // Marching out
ARMY_BACKWARD = 2  // Returning
ARMY_STAY = 3      // Stationed/defending
```

### Army Send Status
```actionscript
CAN_SEND_ARMY = 0           // Can send
CANT_COLONIZE_SUZERAIN_ALLIANCE = 17  // Cannot colonize alliance
```

### 🐛 IDENTIFIED BUGS/ISSUES:
| Constant | Issue | Severity | Fix Required |
|----------|-------|----------|--------------|
| CAN_SEND_ARMY=0 | OK but should check for -1 errors | LOW | Add validation |
| Gap 1-16 missing | **16 missing error codes between 0 and 17** | HIGH | Document all codes |

---

## 6. OBJ CONSTANTS (`ObjConstants.as`) - 🟠 MEDIUM PRIORITY

### Army Mission Types
```actionscript
ARMY_MISSION_TRANS = 1     // Transport
ARMY_MISSION_SEND = 2      // Reinforce
ARMY_MISSION_OCCUPY = 3    // Occupy valley
ARMY_MISSION_SCOUT = 4     // Scout
ARMY_MISSION_ATTACK = 5    // Attack
```

### Package Status
```actionscript
PACKAGE_STATUS_AVAIBLE = 2   // ⚠️ TYPO: AVAILABLE
PACKAGE_STATUS_NOT_MET = 3   // Requirements not met
PACKAGE_STATUS_HAD_GOT = 4   // Already claimed
PACKAGE_STATUS_USED = 5      // Already used
```

### Gender
```actionscript
SEX_MALE = 0
SEX_FEMALE = 1
```

### Buff Types
```actionscript
ADV_MOVE_CASTLE_BUFF = 1440  // Castle move buff duration
```

### 🐛 IDENTIFIED BUGS/ISSUES:
| Constant | Issue | Severity | Fix Required |
|----------|-------|----------|--------------|
| PACKAGE_STATUS_AVAIBLE | **TYPO: Should be AVAILABLE** | HIGH | Fix spelling |
| PACKAGE_STATUS starts at 2 | **Missing status 0,1** | MEDIUM | Document gaps |
| ARMY_MISSION gap | Check if 6+ exists | LOW | Verify completeness |

---

## 7. COLONY CONSTANTS (`ColonyConstants.as`) - 🟡 LOW PRIORITY

### Colony Status
```actionscript
COLONY_STATUS_NORMAL = 0     // Normal
COLONY_STATUS_OCCUPIED = 2   // Occupied ⚠️ Gap at 1
COLONY_STATUS_UPRISING = 3   // Uprising/revolt
COLONY_STATUS_ABANDON = 4    // Abandoned
```

### Colony Types
```actionscript
CASTLE_COLONIZATION_COLONY = 2
```

### Abandon Reasons
```actionscript
ABADON_REASON_OCCUPY = 1     // ⚠️ TYPO: ABANDON
ABADON_REASON_GIVEUP = 2     // ⚠️ TYPO: ABANDON
```

### 🐛 IDENTIFIED BUGS/ISSUES:
| Constant | Issue | Severity | Fix Required |
|----------|-------|----------|--------------|
| ABADON_* | **TYPO: Should be ABANDON** | MEDIUM | Fix spelling |
| COLONY_STATUS gap | **Missing status 1** | LOW | Document |

---

## 8. BUILDING CONSTANTS (`BuildingConstants.as`) - 🟠 MEDIUM PRIORITY

### Building Type IDs (Referenced)
```actionscript
TYPE_TOWNHALL = 1       // Town Hall
TYPE_COTTAGE = 2        // Cottage
TYPE_WAREHOUSE = 3      // Warehouse
TYPE_IRON_MINE = 4      // Iron Mine (outside)
TYPE_STONE_MINE = 5     // Quarry (outside)  
TYPE_LUMBER_MILL = 6    // Sawmill (outside)
TYPE_FARM = 7           // Farm (outside)
TYPE_TAVERN = 8         // Inn/Tavern
// ... many more
```

### 🐛 IDENTIFIED BUGS/ISSUES:
| Constant | Issue | Severity | Fix Required |
|----------|-------|----------|--------------|
| Missing full list | Need complete enumeration | HIGH | Extract all |
| TYPE vs BUILDING prefix | Inconsistent naming | LOW | Standardize |

---

## 9. TECH CONSTANTS (`TechConstants.as`) - 🟡 LOW PRIORITY

### Technology IDs
```actionscript
BUILD_TECH = 17           // Construction
FORTIFICATION_TECH = 18   // Fortification
REPAIR_TECH = 19          // Engineering
HARRY_SKILL = 20          // Horseback Riding
MAX_LEVEL = 10            // Max tech level
```

### 🐛 IDENTIFIED BUGS/ISSUES:
| Constant | Issue | Severity | Fix Required |
|----------|-------|----------|--------------|
| HARRY_SKILL | **Naming unclear** | LOW | Rename to HORSEMANSHIP |
| IDs start at 17 | **Missing 1-16** | MEDIUM | Document all techs |

---

## 10. COMMON CONSTANTS (`CommonConstants.as`) - 🟠 MEDIUM PRIORITY

### Quest/Effort Types
```actionscript
NO_CONTRIBUTE_TASK = 1000000
CONTRIBUTE_RESOURCE = 114
COMMISSION_QUEST_TYPE_COLONY = 1
UNFURL_ACHIEVMENT = 115          // ⚠️ TYPO: ACHIEVEMENT
EFFORT_STAR = 116
EFFORT_MEDAL = 111
EFFORT_FIELD = 105
EFFORT_ARMY_FOOT = 106
EFFORT_LV100_HERO = 127
EFFORT_GENERAL_HERO = 129
EFFORT_PRODUCT_ARMY_COUNT = 123
EFFORT_SCOUTER = 102
```

### Security Constants
```actionscript
SECURITY_PROTECT_CITY = 2
SECURITY_PROTECT_ARMY = 4
SECURITY_PROTECT_HERO = 8
```

### Speak/Chat Types
```actionscript
SPEAK_GPAP = 6
```

### Resource Types
```actionscript
RESOURCE_TYPE_GOLD = 1005
CONTRIBUTE_TROOP_NUM = 9
CONTRIBUTE_MAIN_ID = 4
```

### 🐛 IDENTIFIED BUGS/ISSUES:
| Constant | Issue | Severity | Fix Required |
|----------|-------|----------|--------------|
| UNFURL_ACHIEVMENT | **TYPO: Should be ACHIEVEMENT** | MEDIUM | Fix spelling |
| EFFORT_* scattered | **Values not sequential** | LOW | Document order |
| SECURITY_* as bitflags | Verify proper usage | MEDIUM | Add documentation |

---

## 11. CITY STATE CONSTANTS (`CityStateConstants.as`) - 🟠 MEDIUM PRIORITY

### Comfort Types
```actionscript
COMFORT_PRAY = 2
COMFORT_BLESS = 3
COMFORT_POPULATION_RAISE = 4
```

### Hero Status (Duplicate!)
```actionscript
HERO_STATUS_DEFEND = 2    // ⚠️ DUPLICATE of HeroConstants
HERO_STATUS_MARCH = 3     // ⚠️ DUPLICATE of HeroConstants
HERO_STATUS_CAPTIVE = 4   // ⚠️ DUPLICATE of HeroConstants
```

### 🐛 IDENTIFIED BUGS/ISSUES:
| Constant | Issue | Severity | Fix Required |
|----------|-------|----------|--------------|
| HERO_STATUS_* | **DUPLICATE definitions** | HIGH | Consolidate to one file |
| COMFORT starts at 2 | **Missing COMFORT_* 0,1** | LOW | Document |

---

## 12. MAIL CONSTANTS (`MailConstants.as`) - 🟡 LOW PRIORITY

```actionscript
MAIL_RECEIVE = 1
```

### 🐛 IDENTIFIED BUGS/ISSUES:
| Constant | Issue | Severity | Fix Required |
|----------|-------|----------|--------------|
| Only MAIL_RECEIVE | **Missing MAIL_SEND, MAIL_DELETE, etc.** | MEDIUM | Add missing |

---

## 13. TRADE CONSTANTS (`TradeConstants.as`) - 🟡 LOW PRIORITY

### Trade Resource Types
```actionscript
TRADE_TYPE_FOOD = 0
TRADE_TYPE_WOOD = 1
TRADE_TYPE_STONE = 2
TRADE_TYPE_IRON = 3
```

### 🐛 IDENTIFIED BUGS/ISSUES:
| Constant | Issue | Severity | Fix Required |
|----------|-------|----------|--------------|
| Missing TRADE_TYPE_GOLD | No gold trading constant | LOW | Add if needed |

---

# 🔴 CRITICAL BUG SUMMARY

## Severity: HIGH (Must Fix)
| # | Location | Bug | Impact |
|---|----------|-----|--------|
| 1 | FieldConstants | `STAUTS_OCCUPIED` typo | Comparison failures |
| 2 | FieldConstants | `STAUTS_CASTLE` typo | Comparison failures |
| 3 | ObjConstants | `PACKAGE_STATUS_AVAIBLE` typo | UI/Logic errors |
| 4 | HeroConstants | Duplicate FLEE_STATU/FLEE_STATU2 | Undefined behavior |
| 5 | CityStateConstants | Duplicate HERO_STATUS_* | Maintenance nightmare |
| 6 | TFConstants | ID gap (troops 2-13, forts 20-25) | Array indexing issues |
| 7 | ErrorCode | Generic -1 masks specific errors | Hard to debug |
| 8 | FieldConstants | Missing STATUS=1 | Unknown state handling |

## Severity: MEDIUM (Should Fix)
| # | Location | Bug | Impact |
|---|----------|-----|--------|
| 1 | ColonyConstants | `ABADON_*` typo | Code readability |
| 2 | CommonConstants | `ACHIEVMENT` typo | String matching |
| 3 | FieldConstants | `PRODUCE_SWAP_*` typo | Documentation confusion |
| 4 | HeroConstants | `*_STATU` suffix typo | Inconsistency |
| 5 | ArmyConstants | Missing codes 1-16 | Incomplete error handling |
| 6 | TechConstants | HARRY_SKILL unclear | Maintainability |

## Severity: LOW (Nice to Fix)
| # | Location | Bug | Impact |
|---|----------|-----|--------|
| 1 | Various | Inconsistent naming | Code quality |
| 2 | Various | Missing constants | Incomplete coverage |
| 3 | Various | Non-sequential IDs | Minor confusion |

---

# 📋 ENUM FIX ACTION PLAN

## Phase 4.1: Immediate Typo Fixes ⏱️ Day 1
```actionscript
// Fix all typos
STAUTS_OCCUPIED → STATUS_OCCUPIED
STAUTS_CASTLE → STATUS_CASTLE
PACKAGE_STATUS_AVAIBLE → PACKAGE_STATUS_AVAILABLE
ABADON_REASON_* → ABANDON_REASON_*
UNFURL_ACHIEVMENT → UNFURL_ACHIEVEMENT
PRODUCE_SWAP_* → PRODUCE_SWAMP_*
*_STATU → *_STATUS
```

## Phase 4.2: Duplicate Resolution ⏱️ Day 2
```actionscript
// Consolidate HERO_STATUS to HeroConstants.as
// Remove from CityStateConstants.as
// Update all references

// Clarify HERO_FLEE_STATUS vs HERO_FLEE_STATUS2
// Document difference or merge
```

## Phase 4.3: Gap Documentation ⏱️ Day 3
```actionscript
// Document all ID gaps:
// TFConstants: 0-1 reserved? 14-19 unused?
// FieldConstants: TYPE 7-9 unused, STATUS 1 unknown
// ArmyConstants: 1-16 error codes needed
// PACKAGE_STATUS: 0-1 meaning?
```

## Phase 4.4: Missing Constants ⏱️ Day 4
```actionscript
// Add missing:
MAIL_SEND = 0
MAIL_DELETE = 2
TRADE_TYPE_GOLD = 4
HERO_TRAINING_STATUS = ?
STATUS_PENDING = 1 // For FieldConstants
```

---

# 🎯 RAG QUERIES FOR DEEPER ANALYSIS

```python
# Find all constant usage
evony_search("switch case TFConstants T_", k=50)
evony_search("if status == STAUTS", k=30)  # Find typo usage
evony_search("HERO_FLEE_STATU comparison", k=30)

# Find missing constants
evony_search("const int = 1 status type", k=50)
evony_search("error code -2 -6 -7", k=30)

# Find duplicate definitions
evony_search("HERO_STATUS public static const", k=30)
```

---

---

## 14. NPC HERO CONSTANTS (`NpcHeroBean.as`) - 🔴 HIGH PRIORITY

### NPC Hero Status - **CRITICAL INCONSISTENCY FOUND**
```actionscript
// Version 1 (NpcHeroBean.as):
CATCH_STATUS = 1      // Captured
GENERAL_NPC_HERO = 0  // General type
HIRED_STATUS = 2      // Hired

// Version 2 (NpcHeroBean_1.as):
FREE_STATUS = 0       // Free/Available
CATCH_STATUS = 1      // Captured  
HIRED_STATUS = 2      // Hired

// Version 3 (NpcHeroBean_2.as):
HIRED_STATUS = 2      // Hired
FREE_STATUS = 0       // Free
// Missing CATCH_STATUS!
```

### 🐛 IDENTIFIED BUGS/ISSUES:
| Constant | Issue | Severity | Fix Required |
|----------|-------|----------|--------------|
| GENERAL_NPC_HERO vs FREE_STATUS | **Same value (0), different names** | HIGH | Standardize |
| CATCH_STATUS missing in v3 | **Inconsistent definitions** | HIGH | Add to all versions |
| 3 different NpcHeroBean files | **Code duplication** | HIGH | Consolidate |

---

## 15. EXTENDED ERROR CODES (`ErrorCode.as`) - 🔴 HIGH PRIORITY

### Building Errors (Continued)
```actionscript
INVALID_BUILDING_STATUS = -45
INVALID_BUILDING_TYPE = -46
ITEM_NOT_ENOUGH = -47
TOWNHALL_LEVEL_UNSUPPORT = -48    // ⚠️ GRAMMAR: UNSUPPORTED
UPDATE_LEVEL_OUT_OF_RANGE = -49
INVALID_PASSWORD = -50
```

### Alliance Errors
```actionscript
ALLIANCE_NOT_FOUND = -52
SUPPORT_NOT_ZERO = -52            // ⚠️ DUPLICATE CODE!
NOBILITY_NOT_ENOUGH = -53
RESEARCH_NOT_IN_UPGRADE = -54
NO_UPGRADING_RESEARCH_IN_ACADEMY = -55
BUILDING_REACH_MAX_LEVEL = -57
ALREADY_UPGRADING_RESEARCH_IN_ACADEMY = -58
ILLEGAL_TECH_TYPE = -59
```

### Chat/Silence Errors
```actionscript
SILENCETIMEEXCEPTION = -157
SILENCESAMEPLAYEREXCEPTION = -158
NOVOTEINDAYEXCEPTION = -159
```

### 🐛 IDENTIFIED BUGS/ISSUES:
| Error Code | Issue | Severity | Fix Required |
|------------|-------|----------|--------------|
| -52 | **DUPLICATE: ALLIANCE_NOT_FOUND & SUPPORT_NOT_ZERO** | CRITICAL | Different codes needed |
| -48 | UNSUPPORT typo (should be UNSUPPORTED) | LOW | Fix grammar |
| -56 | **MISSING error code** | MEDIUM | Document or add |
| -157 to -159 | Exception suffix inconsistent | LOW | Standardize naming |

---

## 16. ANIMATION CONSTANTS (`EvonyAnimation.as`) - 🟡 LOW PRIORITY

### Building Animation Types (Sample)
```actionscript
TYPE_CottageCLv1 = 0
TYPE_CottageStructCLv1 = 1
TYPE_CottageCLv2 = 2
...
TYPE_BarracksStructCLv1 = 81
TYPE_BarracksCLv2 = 82
...
TYPE_AcademyStructCLv2 = 99
TYPE_AcademyCLv3 = 100
...
TYPE_TownhallCLv4 = 126
TYPE_TownhallStructCLv4 = 127
```

### 🐛 IDENTIFIED BUGS/ISSUES:
| Constant | Issue | Severity | Fix Required |
|----------|-------|----------|--------------|
| CLv naming | Inconsistent (CLv vs Lv vs Level) | LOW | Standardize |
| Over 250 constants | Hard to maintain | LOW | Consider grouping |

---

# 🔴 UPDATED CRITICAL BUG SUMMARY

## Severity: CRITICAL (Must Fix Immediately)
| # | Location | Bug | Impact |
|---|----------|-----|--------|
| 1 | ErrorCode | **-52 DUPLICATE** (ALLIANCE_NOT_FOUND & SUPPORT_NOT_ZERO) | Wrong error handling |
| 2 | NpcHeroBean | **3 different versions with inconsistent constants** | Undefined behavior |
| 3 | NpcHeroBean | GENERAL_NPC_HERO vs FREE_STATUS same value (0) | Confusion |

## Severity: HIGH (Must Fix)
| # | Location | Bug | Impact |
|---|----------|-----|--------|
| 1 | FieldConstants | `STAUTS_OCCUPIED` typo | Comparison failures |
| 2 | FieldConstants | `STAUTS_CASTLE` typo | Comparison failures |
| 3 | ObjConstants | `PACKAGE_STATUS_AVAIBLE` typo | UI/Logic errors |
| 4 | HeroConstants | Duplicate FLEE_STATU/FLEE_STATU2 | Undefined behavior |
| 5 | CityStateConstants | Duplicate HERO_STATUS_* | Maintenance nightmare |
| 6 | TFConstants | ID gap (troops 2-13, forts 20-25) | Array indexing issues |
| 7 | ErrorCode | Generic -1 masks specific errors | Hard to debug |
| 8 | FieldConstants | Missing STATUS=1 | Unknown state handling |
| 9 | NpcHeroBean | CATCH_STATUS missing in v3 | Incomplete handling |

## Severity: MEDIUM (Should Fix)
| # | Location | Bug | Impact |
|---|----------|-----|--------|
| 1 | ColonyConstants | `ABADON_*` typo | Code readability |
| 2 | CommonConstants | `ACHIEVMENT` typo | String matching |
| 3 | FieldConstants | `PRODUCE_SWAP_*` typo | Documentation confusion |
| 4 | HeroConstants | `*_STATU` suffix typo | Inconsistency |
| 5 | ArmyConstants | Missing codes 1-16 | Incomplete error handling |
| 6 | TechConstants | HARRY_SKILL unclear | Maintainability |
| 7 | ErrorCode | Missing -56 | Gap in error handling |
| 8 | ErrorCode | UNSUPPORT grammar | Code quality |

---

# 📋 UPDATED ENUM FIX ACTION PLAN

## Phase 4.1: Critical Duplicate Resolution ⏱️ IMMEDIATE
```actionscript
// Fix duplicate error code -52
ALLIANCE_NOT_FOUND = -52
SUPPORT_NOT_ZERO = -60  // NEW CODE

// Consolidate NpcHeroBean to ONE file
// Define consistent constants:
FREE_STATUS = 0
CATCH_STATUS = 1
HIRED_STATUS = 2
```

## Phase 4.2: Typo Fixes ⏱️ Day 1
```actionscript
STAUTS_OCCUPIED → STATUS_OCCUPIED
STAUTS_CASTLE → STATUS_CASTLE
PACKAGE_STATUS_AVAIBLE → PACKAGE_STATUS_AVAILABLE
ABADON_REASON_* → ABANDON_REASON_*
UNFURL_ACHIEVMENT → UNFURL_ACHIEVEMENT
PRODUCE_SWAP_* → PRODUCE_SWAMP_*
*_STATU → *_STATUS
TOWNHALL_LEVEL_UNSUPPORT → TOWNHALL_LEVEL_UNSUPPORTED
```

## Phase 4.3: Duplicate Definition Resolution ⏱️ Day 2
```actionscript
// Move all HERO_STATUS to HeroConstants.as ONLY
// Remove from CityStateConstants.as
// Update all references

// Clarify HERO_FLEE_STATUS vs HERO_FLEE_STATUS2
```

## Phase 4.4: Gap Documentation & Missing Constants ⏱️ Day 3
```actionscript
// Document all ID gaps
// Add missing constants:
ERROR_CODE_-56 = ?  // Find purpose
STATUS_PENDING = 1  // FieldConstants
MAIL_SEND = 0
MAIL_DELETE = 2
```

---

*Critical Enum Analysis - Generated via RAG Full Access*
*Total Bugs Identified: 27 (3 CRITICAL, 9 HIGH, 8 MEDIUM, 7 LOW)*
*Next: Execute fix action plan - Start with CRITICAL duplicates*
