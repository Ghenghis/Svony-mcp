# Scripts & Automation Index

Organized collection of AutoEvony/RoboEvony scripts by use case.

## 📁 Script Categories

### 🏰 City Building & Development
Scripts for automating city construction and upgrades.

| Script | Purpose | Key Commands |
|--------|---------|--------------|
| `[script]-Viscount.txt` | Build to Viscount rank | `Build be:5:1`, `Research ar:1` |
| `New_City_Script_v1.0` | New city setup | Building queue, research order |

**Key Commands:**
```
Build be:5:1,e:5:1      # Build barracks L5, embassy L5
Build fh:9:1,r:10:1     # Feasting hall L9, rally L10
Research ar:1           # Archery L1
Research con:8          # Construction L8
```

---

### ⚔️ Attack & Combat
Scripts for automated attacking and farming.

| Script | Purpose | Key Commands |
|--------|---------|--------------|
| `Multi_Attack.txt` | Multi-target attacks | `attack`, `scout` |
| `spam_script_v13.2.txt` | Rapid attack spam | Timed attacks |

**Key Commands:**
```
attack x:y              # Attack coordinates
scout x:y               # Scout coordinates
wave a:1000,w:500       # Send wave with troops
```

---

### 🌾 Resource Farming
Scripts for NPC farming and resource collection.

| Script | Purpose | Targets |
|--------|---------|---------|
| `NPC_Farming.txt` | Automated NPC hits | L5-L10 NPCs |
| `Valley_Farming.txt` | Valley captures | Resource valleys |

**Key Commands:**
```
farm npc:5              # Farm L5 NPCs
farm valley:food        # Farm food valleys
collect                 # Collect all resources
```

---

### 🎖️ Troop Training
Scripts for troop production automation.

| Script | Purpose | Troop Types |
|--------|---------|-------------|
| `TroopTraining.txt` | Continuous training | All types |
| `Archer_Builder.txt` | Mass archers | Archers only |

**Key Commands:**
```
troop a:300             # Train 300 archers
troop w:1000            # Train 1000 warriors
queue a:10000           # Queue 10k archers
```

---

### 💰 Economy & Trade
Scripts for market and resource management.

| Script | Purpose | Operations |
|--------|---------|------------|
| `Trade_Bot.txt` | Market automation | Buy/sell |
| `Tax_Collector.txt` | Tax optimization | Tax rate cycling |

**Key Commands:**
```
sell food:1000000       # Sell 1M food
buy iron:500000         # Buy 500k iron
tax 20                  # Set tax to 20%
comfort 100             # Set comfort to 100%
```

---

## 🔧 Script Syntax Reference

### Variables
```
$varname = value        # Set variable
%varname%               # Use variable
```

### Conditionals
```
if (condition)          # If statement
  commands
endif

if (c.cm.resource.food.amount < 1000000)
  collect
endif
```

### Loops
```
loop 10                 # Loop 10 times
  commands
endloop

while (condition)
  commands
endwhile
```

### Labels & Goto
```
label start             # Define label
goto start              # Jump to label
```

### Timing
```
wait 5                  # Wait 5 seconds
sleep 1000              # Sleep 1000ms
schedule 12:00          # Schedule for noon
```

---

## 📊 Command Reference

### City Commands
| Command | Parameters | Description |
|---------|------------|-------------|
| `build` | type:level | Build structure |
| `upgrade` | posId | Upgrade building |
| `demolish` | posId | Destroy building |

### Army Commands
| Command | Parameters | Description |
|---------|------------|-------------|
| `attack` | x:y | Attack coordinates |
| `scout` | x:y | Scout target |
| `recall` | armyId | Recall army |
| `reinforce` | cityId | Send reinforcements |

### Troop Commands
| Command | Parameters | Description |
|---------|------------|-------------|
| `troop` | type:count | Train troops |
| `cancel` | type | Cancel training |
| `disband` | type:count | Disband troops |

### Resource Commands
| Command | Parameters | Description |
|---------|------------|-------------|
| `collect` | - | Collect all |
| `tax` | rate | Set tax rate |
| `comfort` | rate | Set comfort |

---

## 🎯 Example Scripts

### Basic City Builder
```
; New city setup script
config hero:11,fasthero:50

; Phase 1: Essential buildings
Build th:3,c:5:3
Build b:1,w:1,f:1,s:1
Build be:5:1

; Phase 2: Research
Research ar:5,mil:5
Research con:6,met:3

; Phase 3: Troops
troop w:500
troop a:1000
```

### NPC Farmer
```
; Continuous NPC farming
label farm_loop

; Check resources
if (c.cm.resource.food.amount > 500000)
  farm npc:5
endif

wait 300
goto farm_loop
```

### Attack Spam
```
; Multi-wave attack
set target_x 100
set target_y 200

loop 5
  wave a:5000,c:1000
  attack %target_x%:%target_y%
  wait 60
endloop
```
