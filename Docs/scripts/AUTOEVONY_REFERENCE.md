# AutoEvony Script Reference

Complete scripting guide extracted from AutoEvony source and 16MB script archive.

---

## 📋 Script Structure

### Section Format
```
[sectionName]
commands...

[city1Goals]
config hero:11,fasthero:50,trade:1
distancepolicy 20 20 20 20 20
Build be:5:1
```

### Sections
| Section | Purpose |
|---------|---------|
| `[city1Goals]` - `[city10Goals]` | Per-city automation |
| `[globalSettings]` | Global configuration |
| `[attackSettings]` | Attack automation |
| `[spamSettings]` | Spam attack config |

---

## ⚙️ Configuration Commands

### `config` - City Configuration
```
config hero:11,fasthero:50,trade:1,dumping:1,herominattack:50,junkhero:7
```

| Parameter | Value | Description |
|-----------|-------|-------------|
| `hero` | 1-11 | Hero recruitment level |
| `fasthero` | int | Fast hero threshold |
| `herominattack` | int | Min attack for heroes |
| `junkhero` | int | Junk hero threshold |
| `trade` | 0/1 | Enable trading |
| `dumping` | 0/1 | Enable resource dumping |

### `distancepolicy` - NPC Farming Distance
```
distancepolicy 20 20 20 20 20
```
Format: `distancepolicy npc5 npc6 npc7 npc8 npc9`

### `resourcelimits` - Resource Thresholds
```
resourcelimits 250000 400000 250000 200000
```
Format: `resourcelimits food lumber stone iron`

### `maintown` - Mark as Main City
```
maintown
```

---

## 🏗️ Building Commands

### `Build` - Build/Upgrade Structure
```
Build be:5:1,e:5:1,fh:9:1,r:10:1
Build m:1:1,t:4:1,a:5:1
Build c:3:7,s:3:13,b:1:17
```

Format: `Build type:level:count,...`

### Building Abbreviations
| Abbr | Building | Abbr | Building |
|------|----------|------|----------|
| `th` | Town Hall | `c` | Cottage |
| `b` | Barracks | `s` | Stable |
| `a` | Armory | `w` | Workshop |
| `f` | Forge | `m` | Market |
| `t` | Warehouse | `e` | Embassy |
| `r` | Rally Point | `fh` | Feasting Hall |
| `be` | Beacon | `inn` | Inn |
| `ac` | Academy | `wa` | Walls |
| `fm` | Farm | `sa` | Sawmill |
| `st` | Stonemine | `ir` | Ironmine |

---

## 🔬 Research Commands

### `Research` - Start Research
```
Research ar:5,mil:5
Research con:8,met:3
Research lu:5,in:1
Research com:9
```

Format: `Research tech:level,...`

### Research Abbreviations
| Abbr | Technology | Abbr | Technology |
|------|------------|------|------------|
| `ar` | Archery | `mil` | Military Science |
| `met` | Metal Casting | `med` | Medicine |
| `con` | Construction | `eng` | Engineering |
| `lu` | Lumbering | `min` | Mining |
| `ag` | Agriculture | `in` | Informatics |
| `com` | Compass | `ho` | Horseback |
| `mt` | Military Tradition | `pri` | Privateering |

---

## ⚔️ Troop Commands

### `troop` - Train Troops
```
troop a:300
troop w:1000,p:500
troop a:6135037     ; Overflow threshold!
```

Format: `troop type:count,...`

### Troop Abbreviations
| Abbr | Troop | Cost | Overflow Threshold |
|------|-------|------|-------------------|
| `wo` | Worker | 50 | 42,949,673 |
| `w` | Warrior | 100 | 21,474,837 |
| `s` | Scout | 150 | 14,316,558 |
| `p` | Pikeman | 200 | 10,737,419 |
| `sw` | Swordsman | 250 | 8,589,935 |
| `a` | Archer | 350 | 6,135,037 |
| `c` | Cavalry | 800 | 2,684,355 |
| `ca` | Cataphract | 1500 | 1,431,656 |
| `t` | Transporter | 500 | 4,294,968 |
| `ba` | Ballista | 2500 | 858,994 |
| `r` | Ram | 4000 | 536,871 |
| `cat` | Catapult | 6000 | 357,914 |

---

## 👤 Hero Commands

### Hero Management
```
getspamhero attrib              ; Get spam hero
findhero attrib minLevel method ; Find/hire hero
spamheroes str                  ; Configure spam heroes
firehero                        ; Fire hero
```

### Hero Discharge (Script Variable)
```
set nv $c.af.getHeroCommand().dischargeChief(c.castle.id)$
```

---

## 🎯 Attack Commands

### Basic Attack
```
attack x:y
scout x:y
```

### Advanced Attack Script
```
label prep_atk_done
set nv $c.af.getHeroCommand().dischargeChief(c.castle.id)$
if (c.cm.resource.food.amount < food_lim) set j $c.af.getTroopCommands().disbandTroop(c.castleId,12,%rams2untrain%)$
```

---

## 📝 Variables & Expressions

### Set Variable
```
set varname value
set threshold 6135037
set target_x 100
```

### Use Variable
```
troop a:%threshold%
attack %target_x%:%target_y%
```

### Script Variables (Dynamic)
```
$c.castle.id$                           ; Castle ID
$c.cm.resource.food.amount$             ; Food amount
$c.af.getTroopCommands()$               ; Troop commands
$m_city.castle.name$                    ; City name
$m_city.allCities[0].cityManager$       ; City manager
```

---

## 🔄 Control Flow

### Labels & Goto
```
label start
; commands
goto start
```

### Conditional
```
if (c.cm.resource.food.amount < 1000000)
  collect
endif

if (condition)
  commands
else
  other_commands
endif
```

### Conditional Goals
```
condgoal {{$m_city.castle.name$==Flat}&&{$m_city.allCities[0].cityManager.resource.gold$>150000}} include countRespacks
```

### Loop
```
loop 10
  ; repeat 10 times
endloop

while (condition)
  ; repeat while true
endwhile
```

---

## 🌐 Include URL

Load external scripts from server:
```
includeurl http://localhost:8088/overflow_chain
includeurl http://server.com/script.txt
```

### Script Server (Python)
```python
# From script_server.py
# Serves scripts for AutoEvony 'includeurl' command
# Default port: 8088

from http.server import HTTPServer, SimpleHTTPRequestHandler

class ScriptHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/overflow_chain":
            script = """
troop a:6135037
wait 2
cancel a
"""
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(script.encode())

HTTPServer(('', 8088), ScriptHandler).serve_forever()
```

---

## 💥 Exploit Scripts

### Integer Overflow Chain
```
; OVERFLOW EXPLOIT - Archer
; Threshold: 6,135,037 archers (cost 350 food)

set threshold 6135037

label overflow_loop
troop a:%threshold%
wait 2
cancel a
; Net gain from overflow
goto overflow_loop
```

### Resource Dump Farming
```
; Dump resources to alt, farm NPCs

config dumping:1,trade:1
distancepolicy 15 15 15 15 15

label farm_loop
farm npc:5
wait 300
collect
goto farm_loop
```

---

## 📊 Complete Script Example

```
; VISCOUNT SPEED SCRIPT
; Builds to Viscount rank quickly

[city1Goals]
maintown
config hero:11,fasthero:30,herominattack:50,junkhero:7,dumping:1,trade:1
distancepolicy 20 20 20 20 20
resourcelimits 250000 400000 250000 200000

; Phase 1: Basic buildings
Build m:1:1
Build b:4:1,t:4:1,a:5:1,fh:9:1,r:1:1
Build c:3:7,s:3:13,b:1:17

; Phase 2: Military
Build be:5:1,e:5:1
Build fh:9:1,r:10:1
Build inn:5:1,m:3:1

; Phase 3: Research
Research ar:1
Research lu:5,in:1
Research con:8
Research met:5

; Phase 4: Troops
troop a:300

[city2Goals]
config hero:11,fasthero:50,trade:1
distancepolicy 20 20 20 20 20

Build m:1:1
Build t:2:1,a:5:1,fh:1:1,m:1:1,r:1:1
Build c:3:7,s:3:13,b:1:17
Build t:10:1
Research com:9

condgoal {{$m_city.castle.name$==Flat}&&{$m_city.allCities[0].cityManager.resource.gold$>150000}} include countRespacks
```

---

## 🔧 ActionFactory Integration

Scripts interact with game through ActionFactory:
```actionscript
// From ActionFactory.as
c.af.getTroopCommands().produceTroop(cityId, troopType, count)
c.af.getTroopCommands().cancelTroop(cityId, troopType)
c.af.getTroopCommands().disbandTroop(cityId, troopType, count)
c.af.getHeroCommand().dischargeChief(cityId)
c.af.getArmyCommands().newArmy(param)
```

### TroopCommands.as Methods
```actionscript
public var _produceTroop_callback:Function;
public var _accTroopProduce_callback:Function;
public var _cancelTroopProduce_callback:Function;
public var _disbandTroop_callback:Function;
```

### SenderImpl.as
```actionscript
// Sends commands to server
public function sendMessage(cmd:String, params:Object):void {
    client.sendMessage(cmd, params);
}
```

---

*Extracted from RAG: 106 scripts, 16MB archive*
