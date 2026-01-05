# 📜 AUTOEVONY SCRIPT COMMAND REFERENCE
## Complete Script Language Documentation

**Version:** 1.0  
**Source Files:** `Script.as`, `ScriptCmd.as`, `Commands.as`  
**Compatibility:** RoboEvony, AutoEvony, RE Borg

---

# 📋 TABLE OF CONTENTS

1. [Script Basics](#script-basics)
2. [Variable Commands](#variable-commands)
3. [Control Flow](#control-flow)
4. [Military Commands](#military-commands)
5. [City Commands](#city-commands)
6. [Hero Commands](#hero-commands)
7. [Resource Commands](#resource-commands)
8. [Alliance Commands](#alliance-commands)
9. [Utility Commands](#utility-commands)
10. [Advanced Features](#advanced-features)
11. [Type System](#type-system)
12. [Expression Syntax](#expression-syntax)
13. [Common Patterns](#common-patterns)

---

# 1. SCRIPT BASICS

## 1.1 Script File Format
```
# Comments start with # or //
// This is also a comment

# Scripts are plain text files (.txt, .re)
# Commands are executed line by line
# Whitespace is generally ignored
```

## 1.2 Variable Syntax
```
%variableName%           # Variable reference
${expression}$           # Expression evaluation
$c.property$             # City state property access
{condition}              # Condition evaluation
```

## 1.3 Script Structure
```
# 1. Variable declarations
set myVar value

# 2. Array declarations  
setarray myArr ["item1", "item2"]

# 3. Labels for control flow
label myLabel

# 4. Commands and logic
if {condition} goto myLabel
```

---

# 2. VARIABLE COMMANDS

## 2.1 Basic Variables

### `set` - Set Variable
```
set variableName value
set count 100
set heroName "MyHero"
set target 500,300
```

### `setvar` - Set Variable (Alias)
```
setvar variableName value
```

### `getvar` - Get Variable Value
```
getvar result variableName
```

## 2.2 Array Operations

### `setarray` / `setarr` - Create Array
```
setarray myArray ["value1", "value2", "value3"]
setarr coords "100,100 200,200 300,300"
setarray troopTypes ["wo", "w", "s", "p", "sw", "a", "c", "cata"]
```

### `getindexof` - Find Index in Array
```
getindexof resultVar arrayName searchValue
getindexof idx cities "MyCastle"
```

### Array Access
```
%arrayName[{%index%}]%      # Access by index
%arrayName.length%           # Get array length
```

## 2.3 Type Reference (from ScriptCmd.as)
```actionscript
TYPENAMES = [
    "String",        # Text values
    "Boolean",       # true/false
    "Number",        # Decimal numbers
    "int",           # Integer numbers
    "Coordinate",    # x,y format
    "Resource",      # Resource type
    "Fortification", # Fort type
    "Troop",         # Troop specification
    "*"              # Any type
]
```

---

# 3. CONTROL FLOW

## 3.1 Labels

### `label` - Define Jump Target
```
label myLabelName
label startLoop
label exitScript
```

## 3.2 Jumps

### `goto` - Unconditional Jump
```
goto labelName
goto startLoop
```

### `return` - Return from Subroutine
```
return
```

## 3.3 Conditionals

### `if` - Conditional Execution
```
# Basic if
if {condition} command

# If with goto
if {%count%>10} goto nextSection

# Complex conditions
if {%var1%==%var2%} goto match
if {%level%>=5} train archer 1000
if {{%a%==1}&&{%b%==2}} goto both
if {{%a%==1}||{%b%==2}} goto either
```

### `iferror` - Error Checking
```
iferror expression goto errorLabel
iferror $%mapObj%.userName$ goto waitForDetail
```

## 3.4 Loops

### `loop` - Repeat Command
```
loop count command
loop 10 train worker 100
loop 5 attack 500,300 myHero a:1000
```

### Manual Loop Pattern
```
set i 0
label loopStart
# ... loop body ...
set i {%i%+1}
if {%i%<%max%} goto loopStart
```

## 3.5 Waiting

### `sleep` - Pause Execution
```
sleep seconds
sleep 1
sleep 0.5
sleep 60
```

### `wait` - Wait for Condition
```
wait condition
```

---

# 4. MILITARY COMMANDS

## 4.1 Attack Commands

### `attack` - Send Attack
```
attack x,y heroName troopSpec
attack 500,300 MyHero a:10000,c:5000
attack %targetCoord% %heroName% %troops%
```

### Troop Specification Format
```
troopType:count,troopType:count
a:10000,c:5000,cata:1000

# Troop Abbreviations:
wo   = Worker (Peasant)
w    = Warrior (Militia)
s    = Scout
p    = Pikeman
sw   = Swordsman
a    = Archer
c    = Cavalry
cata = Cataphract
t    = Transporter
b    = Ballista
r    = Battering Ram
cp   = Catapult
```

### `qattack` - Quick Attack
```
qattack x,y heroName troopSpec
```

## 4.2 Scouting

### `scout` - Send Scout
```
scout x,y heroName troopSpec
scout 500,300 none s:1
scout %targetCoord% %scoutHero% s:10
```

## 4.3 Reinforcement

### `reinforce` - Send Reinforcement
```
reinforce x,y heroName troopSpec
reinforce 400,400 DefenseHero p:50000,a:50000
```

### `send` - Generic Send
```
send x,y heroName troopSpec
```

## 4.4 Transport

### `transport` - Send Resources
```
transport x,y heroName resourceSpec
transport 500,300 TransHero food:1000000,wood:500000
```

## 4.5 Recall

### `recall` - Recall Army
```
recall armyId
recall %armyId%
```

## 4.6 Advanced Evasion

### `advevasion` - Configure Evasion
```
advevasion troopConfig heroName layerConfig
advevasion wo:1,w:1,s:-1,p:1,sw:-1,a:1,c:1,cata:1,b:-1,r:-1,cp:-1 none p:%pLayer%,sw:1,c:%cLayer%,cata:0

# Config values:
#  1  = Include this troop type
# -1  = Exclude this troop type
#  0  = Neutral/default
```

## 4.7 Colony Operations

### `colonize` - Colonize Target
```
colonize x,y heroName troopSpec
```

### `qcolony` - Quick Colony
```
qcolony operation target
```

---

# 5. CITY COMMANDS

## 5.1 Training

### `train` - Train Troops
```
train troopType amount
train archer 10000
train worker 50000
train %troopType% %amount%
```

### Troop Type Names
```
worker / peasant / wo
warrior / militia / w
scout / s
pikeman / pike / p
swordsman / sword / sw
archer / a
cavalry / cav / c
cataphract / phract / cata
transporter / trans / t
ballista / bal / b
batteringram / ram / r
catapult / cat / cp
```

## 5.2 Building

### `build` - Construct Building
```
build buildingType
build barracks
build cottage
```

### `upgrade` - Upgrade Building
```
upgrade buildingType
upgrade townhall
```

### `demolish` - Demolish Building
```
demolish buildingType positionId
```

## 5.3 Research

### `research` - Start Research
```
research techName
research archery
research military_science
```

## 5.4 Fortifications

### `buildfort` - Build Fortification
```
buildfort fortType amount
buildfort trap 10000
buildfort abatis 5000
```

### Fortification Types
```
trap
abatis
archertower / at
rollinglogs / logs
trebuchet / treb
rockfall
```

## 5.5 City Management

### `comfort` - Comfort Population
```
comfort type
comfort praying
comfort blessing
comfort population_raise
```

### `levy` - Collect Levy
```
levy resourceType
levy gold
levy food
```

### `taxrate` - Set Tax Rate
```
taxrate percentage
taxrate 20
```

---

# 6. HERO COMMANDS

## 6.1 Hero Management

### `hirehero` - Hire Hero from Inn
```
hirehero heroName
```

### `firehero` - Dismiss Hero
```
firehero heroName
```

### `appointmayor` - Set City Mayor
```
appointmayor heroName
appointmayor none
```

## 6.2 Hero Equipment

### `wearequip` - Equip Item
```
wearequip heroName itemId
```

### `removeequip` - Unequip Item
```
removeequip heroName slot
```

## 6.3 Hero Attributes

### `resetpoint` - Reset Attribute Points
```
resetpoint heroName
```

### `addpoint` - Add Attribute Point
```
addpoint heroName attribute amount
addpoint MyHero attack 10
```

## 6.4 Hero Lookup

### `findHeroById` - Find Hero
```
$c.findHeroById(%heroIndex%)$
$c.findHeroById(h).attack$
$c.findHeroById(h).name$
```

---

# 7. RESOURCE COMMANDS

## 7.1 Resource Transfer

### `dumpresource` - Send Resources Away
```
dumpresource x,y resourceSpec
dumpresource 500,300 food:all,wood:all
```

### `keepresource` - Keep Minimum Resources
```
keepresource resourceSpec
keepresource food:100000,wood:50000
```

## 7.2 Troop Transfer

### `dumptroop` - Send Troops Away
```
dumptroop x,y troopSpec
```

### `keeptroop` - Keep Minimum Troops
```
keeptroop troopSpec
keeptroop a:10000,c:5000
```

## 7.3 Resource Types
```
food / f
wood / w / lumber
stone / s / rock
iron / i / ore
gold / g
```

---

# 8. ALLIANCE COMMANDS

## 8.1 Alliance Info

### `getallianceinfo` - Get Alliance Data
```
getallianceinfo
```

## 8.2 Alliance Army

### `alliancearmy` - Alliance Army Operations
```
alliancearmy command params
```

---

# 9. UTILITY COMMANDS

## 9.1 Output

### `echo` - Print Message
```
echo "Message text"
echo "Current count: %count%"
echo "Hero: $c.cm.heroes[0].name$"
```

### `setsilence` - Toggle Output
```
setsilence true
setsilence false
```

## 9.2 Map Operations

### `getmapdetail` - Get Field Info
```
set mapObj c.getMapDetail(%fieldId%)
```

### `findnpc` - Find NPC Targets
```
findnpc level range
findnpc 5 100
```

## 9.3 Timing

### `gettime` - Get Current Time
```
gettime resultVar
```

### `settimer` - Set Timer
```
settimer name duration
```

## 9.4 Script Control

### `stop` - Stop Script
```
stop
```

### `exit` - Exit Script
```
exit
```

### `includeurl` - Include Remote Script
```
includeurl http://server:port/script/name
includeurl http://localhost:8088/epic/overflow_chain
```

---

# 10. ADVANCED FEATURES

## 10.1 City State Access

### `$c.property$` - CityState Properties
```
$c.castle.name$              # Castle name
$c.castle.fieldId$           # Field ID
$c.castle.resource.food$     # Food amount
$c.cm.heroes.length$         # Hero count
$c.cm.heroes[0].name$        # First hero name
$c.cm.buildings[0].level$    # First building level
```

### `$m_city.property$` - Multi-City Access
```
$m_city.castle.name$
$m_city.allCities[{%y%}].castle.name$
```

## 10.2 Action Factory Access

### `$c.af.command()$` - Direct Commands
```
$c.af.getEquipmentCommands().WearAllEquipmenttech(hero)$
$c.af.getTroopCommands().produceTroop(type, count)$
```

## 10.3 Value Functions

### `c.getValue()` - Get Computed Value
```
$c.getValue(Coordinate,%coordString%)$
$c.getValue(Resource,%resourceString%)$
```

## 10.4 Boolean Expressions
```
{%var%==value}       # Equals
{%var%!=value}       # Not equals
{%var%>value}        # Greater than
{%var%<value}        # Less than
{%var%>=value}       # Greater or equal
{%var%<=value}       # Less or equal

# Compound expressions
{{%a%==1}&&{%b%==2}} # AND
{{%a%==1}||{%b%==2}} # OR
!{%condition%}        # NOT
```

---

# 11. TYPE SYSTEM

## 11.1 Parameter Types

| Type | Format | Example |
|------|--------|---------|
| String | "text" or text | "MyHero", MyHero |
| Boolean | true/false | true, false |
| Number | decimal | 3.14, 100.5 |
| int | integer | 100, -50 |
| Coordinate | x,y | 500,300 |
| Resource | type:amount | food:1000000 |
| Fortification | type:amount | trap:10000 |
| Troop | type:count | a:10000,c:5000 |

## 11.2 Troop Type Mapping

| ID | Short | Full Name |
|----|-------|-----------|
| 2 | wo | Worker/Peasant |
| 3 | w | Warrior/Militia |
| 4 | s | Scout |
| 5 | p | Pikeman |
| 6 | sw | Swordsman |
| 7 | a | Archer |
| 8 | c | Cavalry |
| 9 | cata | Cataphract |
| 10 | t | Transporter |
| 11 | b | Ballista |
| 12 | r | Battering Ram |
| 13 | cp | Catapult |

---

# 12. EXPRESSION SYNTAX

## 12.1 Variable Substitution
```
%varName%                    # Simple variable
%array[{%index%}]%          # Array access
%object.property%            # Property access
```

## 12.2 Expression Evaluation
```
${expression}$               # Evaluate expression
$c.castle.name$              # CityState access
$m_city.property$            # Multi-city access
```

## 12.3 Arithmetic
```
{%a%+%b%}                    # Addition
{%a%-%b%}                    # Subtraction
{%a%*%b%}                    # Multiplication
{%a%/%b%}                    # Division
{%a%+1}                      # Increment
```

## 12.4 String Operations
```
# Concatenation via echo
echo "%var1% and %var2%"
```

---

# 13. COMMON PATTERNS

## 13.1 Loop Through Array
```
set i 0
label arrayLoop
set currentItem %myArray[{%i%}]%
echo "Processing: %currentItem%"
# ... process item ...
set i {%i%+1}
if {%i%<%myArray.length%} goto arrayLoop
echo "Done processing array"
```

## 13.2 Loop Through Cities
```
setarr cities %castles%
set y 0
label allCityLoop
echo "Processing: $m_city.allCities[{%y%}].castle.name$"
# ... city operations ...
set y {%y%+1}
if {%y%<%cities.length%} goto allCityLoop
```

## 13.3 Wait For Response
```
set mapObj c.getMapDetail(%fieldId%)
label waitForDetail
sleep 0.1
iferror $%mapObj%.userName$ goto waitForDetail
set userName $%mapObj%.userName$
```

## 13.4 Hero Loop
```
set h 0
label loop_hero_prep
if ((c.findHeroById(h).attack) > 0) goto loop_level_up
echo "Processing hero: {$c.cm.heroes[%h%].name$}"
# ... hero operations ...
set h {%h%+1}
if {%h%<$c.cm.heroes.length$} goto loop_hero_prep
```

## 13.5 Batch Operations with Delay
```
set batchCount 0
label batchLoop
# ... operation ...
set batchCount {%batchCount%+1}
if {%batchCount%>=10} goto batchPause
goto nextItem

label batchPause
sleep 2
set batchCount 0
goto nextItem
```

## 13.6 Error Handling
```
set success false
label tryOperation
# ... risky operation ...
set success true
goto afterError

label handleError
echo "Error occurred, retrying..."
sleep 5
goto tryOperation

label afterError
if {%success%==false} goto handleError
```

---

# 📊 COMMAND SUMMARY

## Total Commands: 75+

| Category | Count | Examples |
|----------|-------|----------|
| Variable | 8 | set, setvar, setarray, getindexof |
| Control Flow | 10 | label, goto, if, iferror, loop, sleep |
| Military | 12 | attack, scout, reinforce, transport, colonize |
| City | 15 | train, build, upgrade, research, comfort |
| Hero | 8 | hirehero, firehero, appointmayor, wearequip |
| Resource | 6 | dumpresource, keepresource, dumptroop |
| Alliance | 3 | getallianceinfo, alliancearmy |
| Utility | 10 | echo, setsilence, stop, includeurl |
| Advanced | 5+ | $c.af.command()$, getValue() |

---

*AutoEvony Script Reference v1.0*  
*Extracted from: Script.as, ScriptCmd.as, Commands.as*  
*Compatible with: RoboEvony, AutoEvony, RE Borg*
