# 🔍 RAG Query Reference

Complete query templates for extracting everything from Evony codebase.

---

## Query Categories

### Category 1: Protocol Extraction

```
# Get all commands
Query: sendMessage cmd params command
Mode: full_access
Output: Command strings with parameters

# Get response handlers
Query: ResponseDispatcher SERVER_ addEventListener onUpdate
Mode: full_access
Output: Event handler mappings

# Get error codes
Query: errorCode ok fail message error
Mode: full_access
Output: Error code definitions
```

### Category 2: Data Table Extraction

```
# Building data
Query: XMLBuilding building level cost time upgrade typeId
Mode: full_access
Output: Building definitions

# Troop data
Query: XMLTroop troop train cost food attack defense
Mode: full_access
Output: Troop definitions

# Research data
Query: XMLResearch research tech academy requirement effect
Mode: full_access
Output: Research tree

# Item data
Query: XMLItem item effect buff use apply itemId
Mode: full_access
Output: Item catalog
```

### Category 3: UI Component Extraction

```
# View hierarchy
Query: View Panel extends UIComponent addChild children
Mode: full_access
Output: Component tree

# Event handlers
Query: addEventListener MouseEvent click handler callback
Mode: full_access
Output: Event bindings

# Dialogs
Query: Dialog Window popup show close modal
Mode: full_access
Output: Dialog catalog
```

### Category 4: Game Logic Extraction

```
# Resource formulas
Query: resource increaseRate production food wood gold calculation
Mode: full_access
Output: Resource formulas

# Combat formulas
Query: attack defense damage combat battle round calculation
Mode: full_access
Output: Combat mechanics

# Movement formulas
Query: march speed distance time coordinate travel
Mode: full_access
Output: Movement calculations
```

### Category 5: Security Extraction

```
# Encryption keys
Query: ACTION_KEY API_KEY USER_INFO_KEY XOR_KEY salt secret
Mode: full_access
Output: Key values

# Encryption methods
Query: encrypt decrypt MD5 hash signature HMAC XOR
Mode: full_access
Output: Crypto functions

# Session handling
Query: session token login logout refresh disconnect
Mode: full_access
Output: Session lifecycle
```

### Category 6: AutoEvony Extraction

```
# Commands
Query: AutoEvony command train attack build script
Mode: full_access
Output: Script commands

# Variables
Query: setvar getvar variable %city% %hero% array
Mode: full_access
Output: Variable system

# Control flow
Query: if else loop while goto label call return
Mode: full_access
Output: Control structures
```

---

## Specific Symbol Queries

### Classes
```
Query: class Context extends singleton getInstance
Query: class GameClient Socket connect send receive
Query: class ResponseDispatcher addEventListener dispatch
Query: class CastleBean PlayerBean TroopBean HeroBean
```

### Methods
```
Query: function sendMessage params client
Query: function onBuildComplete event handler
Query: function timerHandler timer resource update
Query: function EncryptParam encrypt hash
```

### Constants
```
Query: const static UPDATE_TYPE_ADD DELETE UPDATE
Query: const SERVER_BUILD_COMPLATE TROOP_UPDATE
Query: const BUILDING_TYPE troop item
```

---

## Multi-Hop Trace Queries

### Login Flow Trace
```
Trace: login → authenticate → session → token → connected
Steps:
1. User enters credentials
2. Client hashes password
3. Send login command
4. Receive session token
5. Store session state
```

### Command Flow Trace
```
Trace: UI.click → Sender.sendMessage → GameClient.send → Server → Response → Context.update → UI.refresh
```

### Build Flow Trace
```
Trace: upgrade_button → castle.upgradeBuilding → SERVER_BUILD_COMPLATE → onBuildComplete → TownView.refresh
```

---

## Batch Extraction Queries

### Extract All Commands
```python
queries = [
    "troop.produceTroop params handler",
    "troop.cancelProduce params handler",
    "castle.upgradeBuilding params handler",
    "castle.newBuilding params handler",
    "army.newArmy params handler",
    "army.callBackArmy params handler",
    "hero.hireHero params handler",
    "hero.fireHero params handler",
    # ... 352 total
]
```

### Extract All Beans
```python
beans = [
    "CastleBean properties var public",
    "PlayerBean properties var public",
    "TroopBean properties var public",
    "HeroBean properties var public",
    "BuildingBean properties var public",
    "ArmyBean properties var public",
    "ItemBean properties var public",
    # ...
]
```

### Extract All Events
```python
events = [
    "SERVER_BUILD_COMPLATE handler",
    "SERVER_TROOP_UPDATE handler",
    "SERVER_RESOURCE_UPDATE handler",
    "SERVER_HERO_UPDATE handler",
    "SERVER_SELF_ARMYS_UPDATE handler",
    "SERVER_ENEMY_ARMYS_UPDATE handler",
    # ...
]
```

---

## Query Optimization Tips

### 1. Use Specific Terms
```
# Good
Query: troop.produceTroop castleId troopType num

# Bad (too broad)
Query: train troops
```

### 2. Include File Context
```
# Good
Query: Context.as timerHandler resource update

# Also Good
Query: com.evony.Context timerHandler
```

### 3. Combine Related Terms
```
# Good
Query: army.newArmy targetX targetY missionType troops

# Gets all related params in one query
```

### 4. Use Mode Appropriately
```
# Research mode for general exploration
evony_mode("research")

# Full access for exploit/key extraction
evony_mode("full_access")
```

---

## Expected Output Formats

### Command Definition
```yaml
command: "troop.produceTroop"
file: "com/evony/client/action/TroopCommands.as"
line: 45
params:
  - name: castleId
    type: int
    required: true
  - name: troopType
    type: int
    required: true
  - name: num
    type: int
    required: true
handler: "ResponseDispatcher.SERVER_TROOP_UPDATE"
```

### Bean Definition
```yaml
class: "CastleBean"
file: "com/evony/common/beans/CastleBean.as"
properties:
  - name: id
    type: int
  - name: name
    type: String
  - name: troop
    type: TroopBean
  - name: buildingsArray
    type: ArrayCollection
```

### Formula Definition
```yaml
formula: "resource_production"
file: "com/evony/Context.as"
line: 489-520
expression: |
  amount = base_amount + (increaseRate - troopCostFood + colonyFood + supplyFood) / 3600
variables:
  - increaseRate: from building production
  - troopCostFood: troop upkeep
  - colonyFood: from colonies
  - supplyFood: from allies
```

---

## Automated Extraction Script

```python
from evony_rag import EvonyRAGv2

rag = EvonyRAGv2()
rag.policy.set_mode("full_access")

# Extract all commands
commands = []
for cmd in COMMAND_LIST:
    results = rag.search_only(f"{cmd} params handler", k=5)
    commands.append({
        "command": cmd,
        "results": results
    })

# Extract all beans
beans = []
for bean in BEAN_LIST:
    results = rag.search_only(f"class {bean} properties var", k=5)
    beans.append({
        "class": bean,
        "results": results
    })

# Export to markdown
export_to_markdown(commands, "COMMAND_CATALOG.md")
export_to_markdown(beans, "BEAN_CATALOG.md")
```

---

*Part of Svony MCP - Evony Reverse Engineering Project*
