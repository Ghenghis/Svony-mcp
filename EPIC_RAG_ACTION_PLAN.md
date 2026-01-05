# 🚀 EPIC RAG ACTION PLAN
## Complete Reverse Engineering of EvonyClient & AutoEvony

**Target:** 100% Documentation Coverage  
**Current:** 67% Coverage  
**Gap to Fill:** 33% (~1,847 files to analyze)

---

# 📋 MASTER EXECUTION CHECKLIST

## Pre-Flight Checklist
- [x] RAG System: 166,043 chunks indexed
- [x] Mode: full_access enabled
- [x] Symbols: 55,871 available
- [ ] All 6 phases executed
- [ ] Documentation complete
- [ ] All gaps filled

---

# 🔥 PHASE 1: PROTOCOL COMMAND EXTRACTION
**Goal:** Document 100% of all protocol commands with full parameters

## Step 1.1: Extract All Command Classes

### RAG Query Sequence:
```
QUERY 1: "Commands.as sendMessage sender public function"
QUERY 2: "ActionFactory getInstance get commands"
QUERY 3: "cmd params message protocol"
```

### Files to Fully Analyze:
| File | Priority | Status |
|------|----------|--------|
| CommonCommands.as | 🔴 HIGH | [ ] |
| TroopCommands.as | 🔴 HIGH | [ ] |
| CityCommands.as | 🔴 HIGH | [ ] |
| ArmyCommands.as | 🔴 HIGH | [ ] |
| HeroCommands.as | 🔴 HIGH | [ ] |
| AllianceCommands.as | 🟠 MED | [ ] |
| TradeCommands.as | 🟠 MED | [ ] |
| QuestCommands.as | 🟠 MED | [ ] |
| EquipmentCommands.as | 🟠 MED | [ ] |
| FieldCommands.as | 🟠 MED | [ ] |
| ShopCommands.as | 🟡 LOW | [ ] |
| MailCommands.as | 🟡 LOW | [ ] |
| ReportCommands.as | 🟡 LOW | [ ] |
| RankCommands.as | 🟡 LOW | [ ] |
| TechCommands.as | 🟡 LOW | [ ] |

### Interactive RAG Session - Commands:
```
// Run these queries in sequence:

evony_search("CommonCommands sendMessage function", k=30)
// Extract: command name, all parameters, types

evony_search("TroopCommands train dismiss upgrade", k=30)
// Extract: troop commands, army management

evony_search("ArmyCommands newArmy march attack", k=30)
// Extract: army creation, movement commands

evony_search("HeroCommands recruit discharge award", k=30)
// Extract: hero management commands

evony_search("AllianceCommands create join leave", k=30)
// Extract: alliance management
```

### Output Template - Command Documentation:
```markdown
## command.name (CMD_ID)

**Direction:** Client → Server / Server → Client

**Parameters:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| param1 | String | Yes | Description |
| param2 | int | No | Description |

**Response:**
| Field | Type | Description |
|-------|------|-------------|
| ok | int | Success flag |
| msg | String | Message |

**Example:**
```python
{
    "cmd": "command.name",
    "param1": "value",
    "param2": 123
}
```

**Exploits:**
- [ ] Validation bypass possible
- [ ] Integer overflow risk
- [ ] Race condition potential
```

---

## Step 1.2: Map Command IDs

### RAG Query:
```
evony_search("command ID cmd number protocol message type", k=50)
```

### Known Command ID Ranges:
| Range | Category | Count |
|-------|----------|-------|
| 10000-10999 | Login/Session | ~20 |
| 20000-20999 | City Management | ~50 |
| 30000-30999 | Troop/Army | ~40 |
| 40000-40999 | Hero | ~30 |
| 50000-50999 | Alliance | ~35 |
| 60000-60999 | Trade/Market | ~25 |
| 70000-70999 | Quest | ~20 |
| 80000-80999 | Mail/Report | ~30 |
| 90000-90999 | Shop/Items | ~40 |

### Action Items:
- [ ] Query each range for command details
- [ ] Document all command IDs
- [ ] Map to function names
- [ ] Extract all parameters

---

# 🔥 PHASE 2: BEAN/DATA STRUCTURE MAPPING
**Goal:** Document 100% of all Bean class fields

## Step 2.1: Extract All Bean Classes

### RAG Query Sequence:
```
QUERY 1: "Bean extends BaseBean public var"
QUERY 2: "com.evony.common.beans import"
QUERY 3: "Bean constructor this._arg_1"
```

### Bean Classes to Document:
| Bean | Fields Known | Fields Missing | Status |
|------|--------------|----------------|--------|
| PlayerBean | 15 | ~5 | [ ] |
| CastleBean | 20 | ~8 | [ ] |
| HeroBean | 18 | ~7 | [ ] |
| ArmyBean | 12 | ~4 | [ ] |
| TroopBean | 8 | ~2 | [ ] |
| ItemBean | 10 | ~5 | [ ] |
| EquipmentBean | 14 | ~6 | [ ] |
| BuffBean | 6 | ~4 | [ ] |
| BuildingBean | 10 | ~3 | [ ] |
| ResourceBean | 6 | ~2 | [ ] |
| AllianceBean | 12 | ~5 | [ ] |
| MailBean | 8 | ~3 | [ ] |
| ReportBean | 15 | ~5 | [ ] |
| QuestBean | 10 | ~4 | [ ] |
| TechBean | 8 | ~3 | [ ] |
| MapCastleBean | 10 | ~4 | [ ] |
| NpcBean | 6 | ~2 | [ ] |
| FortificationBean | 8 | ~3 | [ ] |

### Interactive RAG Session - Beans:
```
// Run these queries:

evony_search("PlayerBean public var playerInfo", k=30)
// Extract all player fields

evony_search("CastleBean public var resource building", k=30)
// Extract castle structure

evony_search("HeroBean public var attack defense politics", k=30)
// Extract hero attributes

evony_search("ArmyBean public var troop hero target", k=30)
// Extract army composition

evony_search("EquipmentBean public var gem star enhance", k=30)
// Extract equipment system
```

### Output Template - Bean Documentation:
```markdown
## BeanName

**Package:** com.evony.common.beans

**Fields:**
| Field | Type | Description | Range |
|-------|------|-------------|-------|
| field1 | int | Description | 0-100 |
| field2 | String | Description | - |
| field3 | Array | Description | - |

**Nested Beans:**
- SubBean1
- SubBean2

**Constructor:**
```actionscript
public function BeanName(data:Object) {
    this.field1 = data.field1;
    // ...
}
```

**Related Commands:**
- command.getBean
- command.updateBean
```

---

## Step 2.2: Extract All Constants/Enums

### RAG Query Sequence:
```
QUERY 1: "public static const TYPE ID STATUS"
QUERY 2: "Constants enum state flag"
QUERY 3: "case switch type id"
```

### Constants Files to Extract:
| File | Constants | Status |
|------|-----------|--------|
| ObjConstants.as | PACKAGE_STATUS_* | [ ] |
| FieldConstants.as | POWER_*, FIELD_* | [ ] |
| CityStateConstants.as | HERO_STATUS_* | [ ] |
| TroopConstants.as | TROOP_TYPE_* | [ ] |
| BuildingConstants.as | BUILDING_* | [ ] |
| ItemConstants.as | ITEM_TYPE_* | [ ] |
| QuestConstants.as | QUEST_* | [ ] |
| AllianceConstants.as | ALLIANCE_* | [ ] |

### Interactive RAG Session - Constants:
```
evony_search("ObjConstants public static const", k=30)
evony_search("FieldConstants POWER STATE COUNTY", k=30)
evony_search("CityStateConstants HERO STATUS", k=30)
evony_search("TroopConstants WORKER WARRIOR ARCHER", k=30)
```

---

# 🔥 PHASE 3: RESPONSE HANDLER DISCOVERY
**Goal:** Map 100% of server response handlers

## Step 3.1: Extract ResponseDispatcher Events

### RAG Query:
```
evony_search("ResponseDispatcher public static const", k=50)
evony_search("ResponseDispatcher addEventListener", k=50)
evony_search("onResponse callback handler function", k=50)
```

### Known Response Events:
```actionscript
// Login/Session
PLAYER_LOGIN_RESPONSE
PLAYER_LOGOUT_RESPONSE
SESSION_VALIDATE_RESPONSE

// City
CITY_GET_INFO_RESPONSE
CITY_UPDATE_RESPONSE
CITY_RESOURCE_UPDATE

// Troop
TROOP_PRODUCE_RESPONSE
TROOP_DISMISS_RESPONSE
TROOP_UPGRADE_RESPONSE

// Army
ARMY_NEW_RESPONSE
ARMY_RETURN_RESPONSE
ARMY_ATTACK_RESPONSE

// Hero
HERO_RECRUIT_RESPONSE
HERO_FIRE_RESPONSE
HERO_AWARD_RESPONSE

// Alliance
ALLIANCE_CREATE_RESPONSE
ALLIANCE_JOIN_RESPONSE
ALLIANCE_INFO_UPDATE

// More to discover...
```

### Interactive RAG Session - Handlers:
```
evony_search("ResponseDispatcher CITY CASTLE UPDATE", k=30)
evony_search("ResponseDispatcher TROOP ARMY HERO", k=30)
evony_search("ResponseDispatcher ALLIANCE MEMBER", k=30)
evony_search("ResponseDispatcher QUEST COMPLETE", k=30)
evony_search("ResponseDispatcher SHOP ITEM USE", k=30)
```

### Output Template - Handler Documentation:
```markdown
## ResponseDispatcher.EVENT_NAME

**Event Constant:** `ResponseDispatcher.EVENT_NAME`

**Triggered By:** command.name response

**Response Data:**
| Field | Type | Description |
|-------|------|-------------|
| ok | int | 1=success, 0=fail |
| data | Object | Response payload |

**Handler Example:**
```actionscript
ResponseDispatcher.getInstance().addEventListener(
    ResponseDispatcher.EVENT_NAME,
    onEventHandler
);

function onEventHandler(response:EventResponse):void {
    if (response.ok == 1) {
        // Handle success
    }
}
```
```

---

# 🔥 PHASE 4: SERVER VALIDATION RESEARCH
**Goal:** Discover all server-side validation rules

## Step 4.1: Extract Client-Side Checks (Server May Mirror)

### RAG Query:
```
evony_search("if check validate verify require", k=50)
evony_search("error fail invalid message alert", k=50)
evony_search("limit max min boundary threshold", k=50)
```

### Validation Categories:
| Category | Client Check | Server Check | Bypassable |
|----------|--------------|--------------|------------|
| Resource requirements | ✅ | ❓ | Maybe |
| Building requirements | ✅ | ❓ | Maybe |
| Troop limits | ✅ | ❓ | Maybe |
| Cooldowns | ✅ | ❓ | Maybe |
| Level requirements | ✅ | ❓ | Maybe |
| Permission checks | ✅ | ❓ | Maybe |
| Input validation | ✅ | ❓ | Maybe |

### Interactive RAG Session - Validation:
```
evony_search("if resource food gold wood iron", k=30)
evony_search("if level require building upgrade", k=30)
evony_search("if permission visitor owner", k=30)
evony_search("if cooldown timer delay wait", k=30)
evony_search("minimum maximum limit boundary", k=30)
```

### Testing Methodology:
```python
# Test each validation rule
for command in commands:
    # Test 1: Send without required params
    test_missing_params(command)
    
    # Test 2: Send with invalid values
    test_invalid_values(command)
    
    # Test 3: Send with overflow values
    test_overflow_values(command)
    
    # Test 4: Send during cooldown
    test_cooldown_bypass(command)
    
    # Test 5: Send without permissions
    test_permission_bypass(command)
```

---

# 🔥 PHASE 5: AUTOEVONY SCRIPT COMPLETION
**Goal:** Document 100% of AutoEvony scripting capabilities

## Step 5.1: Extract All Script Commands

### RAG Query:
```
evony_search("autoevony script command function", k=50)
evony_search("label goto if else loop", k=50)
evony_search("set get var variable", k=50)
```

### Script Command Categories:
| Category | Commands | Documented | Status |
|----------|----------|------------|--------|
| Flow Control | label, goto, if, else, loop | 90% | [ ] |
| Variables | set, get, setarr, getarr | 85% | [ ] |
| City | levy, comfort, build, upgrade | 95% | [ ] |
| Troops | train, dismiss, fortify | 90% | [ ] |
| Army | attack, scout, transport, reinforce | 85% | [ ] |
| NPC | qfarm, attacknpc, scan | 80% | [ ] |
| Hero | hirehero, firehero, awardhero | 75% | [ ] |
| Alliance | allianceinfo, sendtroops | 70% | [ ] |
| Advanced | includeurl, exec, eval | 60% | [ ] |

### Interactive RAG Session - Scripts:
```
evony_search("autoevony label goto loop while", k=30)
evony_search("autoevony train attack scout farm", k=30)
evony_search("autoevony includeurl script load", k=30)
evony_search("autoevony config option setting", k=30)
```

### Output Template - Script Command:
```markdown
## commandname

**Syntax:** `commandname param1 param2 [optional]`

**Parameters:**
| Param | Type | Description |
|-------|------|-------------|
| param1 | coords | Target location |
| param2 | int | Amount |

**Examples:**
```
commandname 100,200 5000
commandname $city 1000
```

**Notes:**
- Special behavior
- Limitations
- Related commands
```

---

# 🔥 PHASE 6: SECURITY/ANTI-CHEAT ANALYSIS
**Goal:** Discover all detection mechanisms

## Step 6.1: Client Integrity Checks

### RAG Query:
```
evony_search("security check integrity hash verify", k=30)
evony_search("detect cheat hack bot suspicious", k=30)
evony_search("timing rate limit flood spam", k=30)
```

### Known Detection Vectors:
| Vector | Implemented | Detected | Bypass |
|--------|-------------|----------|--------|
| Packet timing | ❓ | ❓ | ❓ |
| Request rate | ❓ | ❓ | ❓ |
| Value ranges | ❓ | ❓ | ❓ |
| Session validation | ✅ | ✅ | Maybe |
| Client version | ✅ | ✅ | Maybe |
| Behavioral analysis | ❓ | ❓ | ❓ |

### Interactive RAG Session - Security:
```
evony_search("session token validate expire", k=30)
evony_search("version client check update", k=30)
evony_search("ban block suspend detect", k=30)
evony_search("rate limit throttle delay", k=30)
```

---

# 📊 EXECUTION TRACKER

## Daily Progress Template:
```markdown
## Day X - [Date]

### Completed:
- [ ] Phase X.X: Description
- [ ] Queries run: X
- [ ] Items documented: X

### Discovered:
- New command: X
- New constant: X
- New handler: X

### Blockers:
- Issue: Description
- Solution: Pending

### Next:
- Phase X.X
- Focus area
```

## Weekly Milestone Tracker:
| Week | Target | Actual | % Complete |
|------|--------|--------|------------|
| 1 | Phase 1-2 | | |
| 2 | Phase 3-4 | | |
| 3 | Phase 5-6 | | |
| 4 | Review/Test | | |

---

# 🛠️ RAG QUERY TEMPLATES

## Quick Reference Queries:

### Find Commands:
```
evony_search("[Category]Commands sendMessage", k=30)
evony_search("cmd [command.name] params", k=20)
```

### Find Beans:
```
evony_search("[Name]Bean public var", k=30)
evony_search("extends BaseBean [name]", k=20)
```

### Find Constants:
```
evony_search("[Name]Constants public static const", k=30)
evony_search("const [NAME] int = ", k=20)
```

### Find Handlers:
```
evony_search("ResponseDispatcher [EVENT_NAME]", k=30)
evony_search("on[Event]Response handler", k=20)
```

### Find Validation:
```
evony_search("if [condition] return false", k=30)
evony_search("validate [field] check", k=20)
```

### Find Exploits:
```
evony_search("[type] overflow multiply cost", k=30)
evony_search("bypass check skip validation", k=20)
```

---

# 📁 OUTPUT FILES TO GENERATE

```
docs/
├── COMPLETE_COMMAND_REFERENCE.md      # Phase 1 output
├── COMMAND_ID_MAP.md                  # Phase 1 output
├── BEAN_FIELD_REFERENCE.md            # Phase 2 output
├── CONSTANTS_CATALOG.md               # Phase 2 output
├── RESPONSE_HANDLER_MAP.md            # Phase 3 output
├── SERVER_VALIDATION_RULES.md         # Phase 4 output
├── AUTOEVONY_SCRIPT_REFERENCE.md      # Phase 5 output
├── SECURITY_ANALYSIS.md               # Phase 6 output
└── FINAL_COVERAGE_REPORT.md           # Summary
```

---

# 🎯 SUCCESS CRITERIA

## Phase Completion Requirements:

### Phase 1 Complete When:
- [ ] All 15+ command classes documented
- [ ] All command IDs mapped
- [ ] All parameters extracted
- [ ] All responses documented

### Phase 2 Complete When:
- [ ] All 18+ bean classes documented
- [ ] All fields extracted
- [ ] All constants cataloged
- [ ] All enums mapped

### Phase 3 Complete When:
- [ ] All 50+ handlers mapped
- [ ] All response structures documented
- [ ] All event flows traced

### Phase 4 Complete When:
- [ ] All client validations extracted
- [ ] Server behavior tested
- [ ] Bypass methods documented

### Phase 5 Complete When:
- [ ] All script commands documented
- [ ] All variables listed
- [ ] All advanced features covered

### Phase 6 Complete When:
- [ ] All detection vectors identified
- [ ] Safe limits documented
- [ ] Evasion strategies noted

---

# 🚀 START EXECUTION

## First Session Commands:

```python
# Initialize RAG
from evony_rag.rag_v2 import EvonyRAGv2
rag = EvonyRAGv2()
rag.policy.set_mode("full_access")

# Phase 1.1 - Start with CommonCommands
results = rag.search_only("CommonCommands sendMessage public function", k=30)
for r in results:
    print(f"File: {r.file}")
    print(f"Snippet: {r.snippet[:200]}")
    print("---")

# Continue with each command class...
```

---

**READY TO EXECUTE? START WITH PHASE 1!**

*Action Plan Version: 1.0*
*Target Completion: 4 weeks*
*Current Status: READY*
