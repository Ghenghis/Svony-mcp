# 🚀 EPIC ENUM ACTION PLAN
## AutoEvony Complete Enum Bug Fix - Milestone Roadmap

**Document Version:** 1.0  
**Priority:** MAXIMUM - This is where ALL bugs originate  
**Target:** 100% enum consistency, zero bugs  
**Estimated Effort:** 5-7 days intensive work

---

# 📊 ENUM BUG SEVERITY MATRIX

```
┌─────────────────────────────────────────────────────────────────┐
│                    ENUM BUG SEVERITY MATRIX                      │
├─────────────┬──────────┬──────────┬──────────┬─────────────────┤
│ Category    │ CRITICAL │ HIGH     │ MEDIUM   │ LOW             │
├─────────────┼──────────┼──────────┼──────────┼─────────────────┤
│ Duplicates  │    2     │    2     │    0     │    0            │
│ Typos       │    0     │    3     │    5     │    2            │
│ Missing     │    0     │    2     │    3     │    4            │
│ Inconsistent│    1     │    2     │    0     │    1            │
├─────────────┼──────────┼──────────┼──────────┼─────────────────┤
│ TOTAL       │    3     │    9     │    8     │    7            │
└─────────────┴──────────┴──────────┴──────────┴─────────────────┘
                         GRAND TOTAL: 27 BUGS
```

---

# 🎯 MILESTONE BREAKDOWN

## MILESTONE 1: CRITICAL DUPLICATE RESOLUTION
**Timeline:** Day 1 (4-6 hours)  
**Risk Level:** 🔴 CRITICAL  
**Dependencies:** None - Start here

### Task 1.1: Fix ErrorCode -52 Duplicate
**Files Affected:**
- `source_code/ErrorCode.as`
- `source_code/ErrorCode_1.as`
- `source_code/ErrorCode_2.as`

**Current State:**
```actionscript
// BOTH have same code -52 - THIS IS A BUG
public static const ALLIANCE_NOT_FOUND:int = -52;
public static const SUPPORT_NOT_ZERO:int = -52;  // DUPLICATE!
```

**Fix Required:**
```actionscript
// Keep ALLIANCE_NOT_FOUND at -52
public static const ALLIANCE_NOT_FOUND:int = -52;

// Assign new unique code to SUPPORT_NOT_ZERO
public static const SUPPORT_NOT_ZERO:int = -60;  // NEW UNIQUE CODE
```

**RAG Queries to Run:**
```python
evony_search("SUPPORT_NOT_ZERO usage", k=30)
evony_search("error == -52", k=30)
evony_search("ALLIANCE_NOT_FOUND handling", k=30)
```

**Validation Steps:**
1. Find all usages of SUPPORT_NOT_ZERO
2. Find all usages of ALLIANCE_NOT_FOUND
3. Ensure no code relies on them being the same
4. Update all switch/case statements
5. Update error message handlers
6. Test both error conditions separately

**Estimated Impact:** 10-20 code locations

---

### Task 1.2: Consolidate NpcHeroBean Versions
**Files Affected:**
- `source_code/NpcHeroBean.as` (PRIMARY)
- `source_code/NpcHeroBean_1.as` (REMOVE)
- `source_code/NpcHeroBean_2.as` (REMOVE)

**Current State (Inconsistent):**
```actionscript
// NpcHeroBean.as:
CATCH_STATUS = 1
GENERAL_NPC_HERO = 0
HIRED_STATUS = 2

// NpcHeroBean_1.as:
FREE_STATUS = 0
CATCH_STATUS = 1
HIRED_STATUS = 2

// NpcHeroBean_2.as:
HIRED_STATUS = 2
FREE_STATUS = 0
// MISSING CATCH_STATUS!
```

**Fix Required - Unified Definition:**
```actionscript
// MASTER NpcHeroBean.as - ALL constants defined
package com.evony.common.beans
{
    public class NpcHeroBean implements IEventDispatcher 
    {
        // NPC Hero Status Constants - COMPLETE SET
        public static const FREE_STATUS:int = 0;      // Available in inn
        public static const CATCH_STATUS:int = 1;     // Captured by player
        public static const HIRED_STATUS:int = 2;     // Hired by player
        
        // NPC Hero Type Constants
        public static const GENERAL_NPC_HERO:int = 0; // Standard NPC hero
        public static const SPECIAL_NPC_HERO:int = 1; // Special/event hero
        
        // ... rest of class
    }
}
```

**RAG Queries to Run:**
```python
evony_search("NpcHeroBean import", k=50)
evony_search("NpcHeroBean_1 usage", k=30)
evony_search("NpcHeroBean_2 usage", k=30)
evony_search("FREE_STATUS NpcHero", k=30)
evony_search("CATCH_STATUS NpcHero", k=30)
```

**Validation Steps:**
1. Map all imports of each NpcHeroBean version
2. Identify which version is used where
3. Create migration script to update imports
4. Ensure all status checks use correct constants
5. Remove duplicate files
6. Update all references

**Estimated Impact:** 50-100 code locations

---

### Task 1.3: Resolve GENERAL_NPC_HERO vs FREE_STATUS Conflict
**Issue:** Both equal 0, used interchangeably but mean different things

**Current State:**
```actionscript
GENERAL_NPC_HERO = 0  // This is a TYPE, not a STATUS
FREE_STATUS = 0       // This is a STATUS
```

**Fix Required - Separate Concerns:**
```actionscript
// STATUS constants (current hero state)
public static const STATUS_FREE:int = 0;
public static const STATUS_CAPTURED:int = 1;
public static const STATUS_HIRED:int = 2;

// TYPE constants (hero classification)
public static const TYPE_GENERAL:int = 0;
public static const TYPE_SPECIAL:int = 1;
public static const TYPE_HISTORIC:int = 2;
```

**RAG Queries to Run:**
```python
evony_search("GENERAL_NPC_HERO comparison", k=30)
evony_search("npcHero.type ==", k=30)
evony_search("npcHero.status ==", k=30)
```

---

## MILESTONE 2: HIGH SEVERITY TYPO FIXES
**Timeline:** Day 2 (3-4 hours)  
**Risk Level:** 🟠 HIGH  
**Dependencies:** Milestone 1 complete

### Task 2.1: Fix FieldConstants Typos
**Files Affected:**
- `source_code/FieldConstants.as`
- `source_code/FieldConstants_1.as`
- `source_code/FieldConstants_2.as`

**Current State:**
```actionscript
public static const STAUTS_OCCUPIED:int = 2;  // TYPO!
public static const STAUTS_CASTLE:int = 3;    // TYPO!
```

**Fix Required:**
```actionscript
public static const STATUS_OCCUPIED:int = 2;  // FIXED
public static const STATUS_CASTLE:int = 3;    // FIXED

// Add missing status
public static const STATUS_FREE:int = 0;
public static const STATUS_PENDING:int = 1;   // Was missing!
```

**Migration Script:**
```python
# find_and_replace.py
replacements = [
    ("STAUTS_OCCUPIED", "STATUS_OCCUPIED"),
    ("STAUTS_CASTLE", "STATUS_CASTLE"),
]

for old, new in replacements:
    # Find all usages
    results = evony_search(f"{old}", k=100)
    print(f"Found {len(results)} usages of {old}")
    
    # Generate replacement commands
    for r in results:
        print(f"  {r['file']}: Replace {old} → {new}")
```

**RAG Queries to Run:**
```python
evony_search("STAUTS_OCCUPIED", k=50)
evony_search("STAUTS_CASTLE", k=50)
evony_search("field.status ==", k=50)
```

**Estimated Impact:** 30-50 code locations

---

### Task 2.2: Fix ObjConstants Typo
**Files Affected:**
- `source_code/ObjConstants.as`
- `source_code/ObjConstants_1.as`
- `source_code/ObjConstants_2.as`

**Current State:**
```actionscript
public static const PACKAGE_STATUS_AVAIBLE:int = 2;  // TYPO!
```

**Fix Required:**
```actionscript
public static const PACKAGE_STATUS_AVAILABLE:int = 2;  // FIXED

// Also add missing statuses
public static const PACKAGE_STATUS_UNKNOWN:int = 0;
public static const PACKAGE_STATUS_LOCKED:int = 1;
public static const PACKAGE_STATUS_AVAILABLE:int = 2;
public static const PACKAGE_STATUS_NOT_MET:int = 3;
public static const PACKAGE_STATUS_CLAIMED:int = 4;
public static const PACKAGE_STATUS_USED:int = 5;
```

**RAG Queries to Run:**
```python
evony_search("PACKAGE_STATUS_AVAIBLE", k=50)
evony_search("package.status ==", k=30)
```

**Estimated Impact:** 15-25 code locations

---

### Task 2.3: Resolve HeroConstants Duplicates
**Files Affected:**
- `source_code/HeroConstants.as`
- `source_code/HeroConstants_1.as`
- `source_code/HeroConstants_2.as`
- `source_code/CityStateConstants.as`
- `source_code/CityStateConstants_1.as`

**Current State - Duplicate Definitions:**
```actionscript
// HeroConstants.as
HERO_FREE_STATU = 0
HERO_CHIEF_STATU = 1
HERO_DEFEND_STATU = 2
HERO_MARCH_STATU = 3
HERO_SEIZED_STATU = 4
HERO_BACK_STATU = 5
HERO_FLEE_STATU = 6
HERO_FLEE_STATU2 = 7  // WHY TWO FLEE STATES?

// CityStateConstants.as - DUPLICATE!
HERO_STATUS_DEFEND = 2
HERO_STATUS_MARCH = 3
HERO_STATUS_CAPTIVE = 4
```

**Fix Required - Single Source of Truth:**
```actionscript
// HeroConstants.as - MASTER DEFINITION
package com.evony.common.constants
{
    public class HeroConstants
    {
        // Hero Status (note: fixed typo STATU → STATUS)
        public static const HERO_STATUS_FREE:int = 0;
        public static const HERO_STATUS_MAYOR:int = 1;    // Was CHIEF
        public static const HERO_STATUS_DEFENDING:int = 2;
        public static const HERO_STATUS_MARCHING:int = 3;
        public static const HERO_STATUS_CAPTURED:int = 4; // Was SEIZED
        public static const HERO_STATUS_RETURNING:int = 5; // Was BACK
        public static const HERO_STATUS_FLEEING:int = 6;
        // REMOVED HERO_FLEE_STATU2 - merged into FLEEING
        
        // Legacy aliases (for backward compatibility)
        public static const HERO_FREE_STATU:int = HERO_STATUS_FREE;
        public static const HERO_CHIEF_STATU:int = HERO_STATUS_MAYOR;
        // ... etc
    }
}

// CityStateConstants.as - REMOVE hero constants, use HeroConstants instead
```

**RAG Queries to Run:**
```python
evony_search("HERO_FLEE_STATU2 usage", k=30)
evony_search("HERO_FLEE_STATU comparison", k=30)
evony_search("hero.status == 6", k=30)
evony_search("hero.status == 7", k=30)
```

**Key Question to Answer:** What is HERO_FLEE_STATU2 (7) used for differently than HERO_FLEE_STATU (6)?

**Estimated Impact:** 100+ code locations

---

## MILESTONE 3: MEDIUM SEVERITY FIXES
**Timeline:** Day 3 (3-4 hours)  
**Risk Level:** 🟡 MEDIUM  
**Dependencies:** Milestones 1-2 complete

### Task 3.1: Fix ColonyConstants Typos
```actionscript
// Current (WRONG)
ABADON_REASON_OCCUPY = 1
ABADON_REASON_GIVEUP = 2

// Fixed
ABANDON_REASON_OCCUPY = 1
ABANDON_REASON_GIVEUP = 2
```

### Task 3.2: Fix CommonConstants Typos
```actionscript
// Current (WRONG)
UNFURL_ACHIEVMENT = 115

// Fixed
UNFURL_ACHIEVEMENT = 115
```

### Task 3.3: Fix FieldConstants Production Typos
```actionscript
// Current (WRONG)
PRODUCE_SWAP_BASE = 3
PRODUCE_SWAP_RATE = 2

// Fixed
PRODUCE_SWAMP_BASE = 3
PRODUCE_SWAMP_RATE = 2
```

### Task 3.4: Fix HeroConstants Suffix Typos
```actionscript
// All *_STATU constants should be *_STATUS
// Already handled in Task 2.3
```

### Task 3.5: Document ArmyConstants Missing Codes
**Current State:**
```actionscript
CAN_SEND_ARMY = 0
// Codes 1-16 MISSING
CANT_COLONIZE_SUZERAIN_ALLIANCE = 17
```

**Fix Required - Document or Add:**
```actionscript
public static const CAN_SEND_ARMY:int = 0;
public static const CANT_SEND_NO_HERO:int = 1;
public static const CANT_SEND_NO_TROOPS:int = 2;
public static const CANT_SEND_ATTACK_FRESHMAN:int = 3;
public static const CANT_SEND_STILL_FRESHMAN:int = 4;
public static const CANT_SEND_ATTACK_ANTIBATTLE:int = 5;
// ... find and document 6-16
public static const CANT_COLONIZE_SUZERAIN_ALLIANCE:int = 17;
```

**RAG Queries to Run:**
```python
evony_search("CANT_SEND error army", k=50)
evony_search("sendArmy error code", k=30)
evony_search("army return code 1 2 3", k=30)
```

### Task 3.6: Fix ErrorCode Missing -56
**RAG Query:**
```python
evony_search("error -56", k=30)
evony_search("error code 56", k=30)
```

### Task 3.7: Fix ErrorCode UNSUPPORT Grammar
```actionscript
// Current
TOWNHALL_LEVEL_UNSUPPORT = -48

// Fixed
TOWNHALL_LEVEL_UNSUPPORTED = -48
```

---

## MILESTONE 4: TFConstants GAP ANALYSIS
**Timeline:** Day 4 (2-3 hours)  
**Risk Level:** 🟡 MEDIUM  
**Dependencies:** Milestones 1-3 complete

### Task 4.1: Document Troop ID Gap
**Current State:**
```
Troop IDs:    2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13
Fort IDs:     20, 21, 22, 23, 24, 25
Gap:          0, 1, 14-19 UNUSED
```

**Questions to Answer:**
1. Why do troop IDs start at 2 not 0?
2. What are IDs 0 and 1 reserved for?
3. Why the gap 14-19 between troops and forts?
4. Are there hidden unit types?

**RAG Queries to Run:**
```python
evony_search("troop type 0", k=30)
evony_search("troop type 1", k=30)
evony_search("TFConstants type 14", k=30)
evony_search("unit type array index", k=30)
```

**Potential Finding:** IDs 0,1 might be reserved for:
- 0 = None/Empty
- 1 = Hero (not a troop but needs ID)?

---

## MILESTONE 5: LOW SEVERITY CLEANUP
**Timeline:** Day 5 (2-3 hours)  
**Risk Level:** 🟢 LOW  
**Dependencies:** Milestones 1-4 complete

### Task 5.1: Standardize Naming Conventions
**Pattern to Apply:**
```
Constants: UPPER_SNAKE_CASE
Status values: STATUS_* prefix
Type values: TYPE_* prefix
Error codes: ERROR_* or negative integers
```

### Task 5.2: Add Missing Constants
```actionscript
// MailConstants - add missing
MAIL_SEND = 0
MAIL_RECEIVE = 1  // exists
MAIL_DELETE = 2

// TradeConstants - add if needed
TRADE_TYPE_GOLD = 4
```

### Task 5.3: Document All Gaps
Create `ENUM_GAP_DOCUMENTATION.md` with:
- All known ID gaps
- Reasons (if known)
- Recommendations

---

## MILESTONE 6: VALIDATION & TESTING
**Timeline:** Day 6-7 (4-6 hours)  
**Risk Level:** 🔴 CRITICAL  
**Dependencies:** All previous milestones

### Task 6.1: Create Enum Validation Script
```python
# enum_validator.py
"""
Validates all enum constants for:
1. No duplicate values within same class
2. No typos (spell check)
3. Consistent naming conventions
4. No gaps in sequential IDs
5. Cross-file consistency
"""

class EnumValidator:
    def __init__(self, rag):
        self.rag = rag
        self.issues = []
    
    def check_duplicates(self, class_name):
        """Find duplicate values in enum class"""
        results = self.rag.search(f"{class_name} public static const", k=100)
        values = {}
        for r in results:
            # Extract constant name and value
            # Check for duplicates
            pass
    
    def check_typos(self, constants):
        """Spell check constant names"""
        common_typos = {
            "STAUTS": "STATUS",
            "AVAIBLE": "AVAILABLE",
            "ABADON": "ABANDON",
            "ACHIEVMENT": "ACHIEVEMENT",
            "STATU": "STATUS",
            "UNSUPPORT": "UNSUPPORTED",
        }
        # ...
    
    def check_gaps(self, constants):
        """Find gaps in sequential IDs"""
        # ...
    
    def validate_all(self):
        """Run all validations"""
        classes = [
            "ErrorCode", "TFConstants", "HeroConstants",
            "FieldConstants", "ObjConstants", "ArmyConstants",
            # ... all enum classes
        ]
        for cls in classes:
            self.check_duplicates(cls)
            # ...
```

### Task 6.2: Create Regression Test Suite
```python
# test_enums.py
"""
Test cases for all enum constants
"""

def test_error_codes_unique():
    """Ensure no duplicate error codes"""
    assert ErrorCode.ALLIANCE_NOT_FOUND != ErrorCode.SUPPORT_NOT_ZERO
    
def test_hero_status_complete():
    """Ensure all hero states are defined"""
    assert hasattr(HeroConstants, 'HERO_STATUS_FREE')
    assert hasattr(HeroConstants, 'HERO_STATUS_MAYOR')
    # ...

def test_troop_types_sequential():
    """Verify troop type IDs are documented"""
    # ...
```

### Task 6.3: Generate Fix Report
```markdown
# ENUM FIX REPORT
Generated: [DATE]

## Summary
- Total bugs found: 27
- Bugs fixed: 27
- Tests passing: 100%

## Changes Made
| File | Changes | Lines Modified |
|------|---------|----------------|
| ErrorCode.as | Fixed -52 duplicate | 2 |
| FieldConstants.as | Fixed STAUTS typos | 4 |
| ... | ... | ... |

## Backward Compatibility
- Legacy aliases added for: [list]
- Breaking changes: [none/list]
```

---

# 📋 DAILY EXECUTION CHECKLIST

## Day 1 Checklist
- [ ] Complete Task 1.1: Fix ErrorCode -52 duplicate
- [ ] Complete Task 1.2: Consolidate NpcHeroBean versions
- [ ] Complete Task 1.3: Resolve GENERAL_NPC_HERO vs FREE_STATUS
- [ ] Run RAG validation queries
- [ ] Document all changes
- [ ] Commit with detailed message

## Day 2 Checklist
- [ ] Complete Task 2.1: Fix FieldConstants typos
- [ ] Complete Task 2.2: Fix ObjConstants typo
- [ ] Complete Task 2.3: Resolve HeroConstants duplicates
- [ ] Update all affected imports
- [ ] Run tests
- [ ] Commit changes

## Day 3 Checklist
- [ ] Complete Tasks 3.1-3.7: Medium severity fixes
- [ ] Document all changes
- [ ] Commit changes

## Day 4 Checklist
- [ ] Complete Milestone 4: TFConstants gap analysis
- [ ] Document findings
- [ ] Commit documentation

## Day 5 Checklist
- [ ] Complete Milestone 5: Low severity cleanup
- [ ] Standardize naming
- [ ] Add missing constants
- [ ] Commit changes

## Day 6-7 Checklist
- [ ] Create enum_validator.py
- [ ] Create test_enums.py
- [ ] Run full validation
- [ ] Generate fix report
- [ ] Final commit
- [ ] Push to repository

---

# 🔍 RAG QUERY REFERENCE

## Discovery Queries
```python
# Find all constant definitions
evony_search("public static const int", k=100)

# Find specific constant usage
evony_search("{CONSTANT_NAME} usage", k=50)

# Find switch/case statements
evony_search("switch status case", k=50)

# Find comparison operations
evony_search("== {VALUE}", k=30)
```

## Validation Queries
```python
# Check for typos
evony_search("STAUTS AVAIBLE ABADON", k=50)

# Find duplicates
evony_search("const int = -52", k=30)

# Find inconsistencies
evony_search("HeroConstants CityStateConstants HERO", k=30)
```

---

# 📊 PROGRESS TRACKING

```
MILESTONE 1: [░░░░░░░░░░] 0% - CRITICAL DUPLICATES
MILESTONE 2: [░░░░░░░░░░] 0% - HIGH TYPOS
MILESTONE 3: [░░░░░░░░░░] 0% - MEDIUM FIXES
MILESTONE 4: [░░░░░░░░░░] 0% - GAP ANALYSIS
MILESTONE 5: [░░░░░░░░░░] 0% - LOW CLEANUP
MILESTONE 6: [░░░░░░░░░░] 0% - VALIDATION

OVERALL:     [░░░░░░░░░░] 0%
```

---

*EPIC ENUM ACTION PLAN v1.0*  
*Total Tasks: 20*  
*Estimated Duration: 5-7 days*  
*Expected Outcome: Zero enum bugs, 100% consistency*
