# 🎯 RAG Extraction Action Plan

Complete task list for reverse engineering everything possible from Evony Client and AutoEvony.

---

## Phase 1: Protocol Complete Extraction (Priority: P0)

### Task 1.1: Command Catalog Extraction
**Query:** `sendMessage cmd params command handler`
**Output:** `COMMAND_CATALOG.md`

```yaml
extract:
  - All command strings (352+)
  - Parameter schemas per command
  - Return value structures
  - Handler method locations
  
format:
  command: "troop.produceTroop"
  params:
    castleId: {type: int, required: true}
    troopType: {type: int, required: true, range: [0,11]}
    num: {type: int, required: true, max: INT32_MAX}
  returns:
    ok: {type: int, values: [0,1]}
    errorCode: {type: int, optional: true}
  handler: "com.evony.client.action.TroopCommands.produceTroop"
```

### Task 1.2: Response Dispatcher Map
**Query:** `ResponseDispatcher SERVER_ addEventListener handler`
**Output:** `RESPONSE_MAP.md`

```yaml
extract:
  - All SERVER_* event constants
  - Handler method mappings
  - Event data structures
  - Dispatch flow
```

### Task 1.3: Error Code Dictionary
**Query:** `errorCode error result ok fail message`
**Output:** `ERROR_CODES.md`

```yaml
extract:
  - Numeric error codes
  - Error messages/strings
  - Recovery actions
  - Client-side handling
```

### Task 1.4: Session Lifecycle
**Query:** `login session token refresh disconnect reconnect`
**Output:** `SESSION_LIFECYCLE.md`

```yaml
extract:
  - Login sequence
  - Token generation
  - Session renewal
  - Disconnect handling
  - Reconnection flow
```

---

## Phase 2: Game Data Extraction (Priority: P0)

### Task 2.1: Building Data Tables
**Query:** `XMLBuilding building level cost time requirement upgrade`
**Output:** `BUILDING_DATA.md`

```yaml
extract:
  buildings:
    - typeId, name, description
    - levels: [1-10]
    - costs: {gold, food, wood, stone, iron, time}
    - requirements: {townhall_level, research}
    - production: {resource_type, rate_per_hour}
```

### Task 2.2: Troop Data Tables
**Query:** `XMLTroop troop type cost food time train attack defense`
**Output:** `TROOP_DATA_COMPLETE.md`

```yaml
extract:
  troops:
    - typeId: 0-11
    - name, description
    - costs: {food, gold, population, time}
    - stats: {attack, defense, life, speed, range, load}
    - requirements: {barracks_level, research}
    - upkeep: {food_per_hour}
```

### Task 2.3: Research Data Tables
**Query:** `XMLResearch research tech upgrade academy requirement`
**Output:** `RESEARCH_DATA.md`

```yaml
extract:
  research:
    - techId, name, category
    - levels: [1-10]
    - costs: {gold, food, wood, stone, iron, time}
    - requirements: {academy_level, prereq_tech}
    - effects: {stat_bonuses}
```

### Task 2.4: Item Data Tables
**Query:** `XMLItem item effect buff use apply chest package`
**Output:** `ITEM_DATA.md`

```yaml
extract:
  items:
    - itemId, name, description
    - type: {consumable, equipment, resource}
    - effects: [{stat, value, duration}]
    - source: {shop, quest, drop}
```

### Task 2.5: Hero Attribute System
**Query:** `HeroBean hero attribute politics attack intelligence level`
**Output:** `HERO_SYSTEM.md`

```yaml
extract:
  hero:
    - base_stats: {politics, attack, intelligence}
    - level_scaling
    - equipment_slots
    - skill_system
    - experience_curve
```

---

## Phase 3: UI Component Extraction (Priority: P1)

### Task 3.1: View Hierarchy Map
**Query:** `View Panel Window extends UIComponent addChild`
**Output:** `UI_HIERARCHY.md`

```yaml
extract:
  views:
    MainWin:
      children: [TopBar, CityPanel, MapPanel, ChatFrame]
    CityPanel:
      children: [BuildingGrid, TroopList, ResourceBar]
    # ... complete tree
```

### Task 3.2: Dialog Catalog
**Query:** `Dialog show popup modal close CTkToplevel`
**Output:** `DIALOG_CATALOG.md`

```yaml
extract:
  dialogs:
    - class_name
    - purpose
    - trigger_events
    - input_fields
    - action_buttons
```

### Task 3.3: Event Handler Index
**Query:** `addEventListener click MouseEvent handler callback`
**Output:** `EVENT_HANDLERS.md`

```yaml
extract:
  events:
    - component
    - event_type
    - handler_method
    - dispatch_chain
```

### Task 3.4: Style/Theme Definitions
**Query:** `styleName style CSS skin theme color font`
**Output:** `STYLES.md`

```yaml
extract:
  styles:
    - style_name
    - properties: {color, font, background}
    - components_using
```

---

## Phase 4: Game Logic Extraction (Priority: P1)

### Task 4.1: Resource Formulas
**Query:** `resource production increaseRate food wood stone iron gold`
**Output:** `RESOURCE_FORMULAS.md`

```yaml
extract:
  formulas:
    production_rate:
      base: building_level * coefficient
      bonus: research_bonus + buff_bonus
    consumption:
      troops: troop_count * upkeep_rate
    storage:
      capacity: warehouse_level * multiplier
```

### Task 4.2: Combat Calculations
**Query:** `attack defense damage combat battle round kill`
**Output:** `COMBAT_FORMULAS.md`

```yaml
extract:
  combat:
    damage_formula: (attack * multiplier) - (defense * reduction)
    round_sequence: [range_phase, melee_phase]
    buff_stacking: {additive, multiplicative}
    hero_contribution: base_stat * level_bonus
```

### Task 4.3: Movement/March Timing
**Query:** `march army travel distance speed time coordinate`
**Output:** `MARCH_TIMING.md`

```yaml
extract:
  march:
    base_speed: slowest_troop_speed
    distance: sqrt((x2-x1)^2 + (y2-y1)^2)
    time: distance / speed * terrain_modifier
```

### Task 4.4: Queue/Cooldown System
**Query:** `queue cooldown timer wait delay buildingQueue`
**Output:** `QUEUE_SYSTEM.md`

```yaml
extract:
  queues:
    building: {max_slots, speedup_items}
    training: {per_barracks, parallel}
    research: {single_queue, cancelable}
```

---

## Phase 5: Security/Crypto Extraction (Priority: P1)

### Task 5.1: Encryption Pipeline
**Query:** `encrypt decrypt XOR AES HMAC signature hash`
**Output:** `ENCRYPTION_PIPELINE.md`

```yaml
extract:
  pipeline:
    request_signing:
      - input: params_string
      - hash: MD5(params + ACTION_KEY)
      - output: signature header
    payload_encryption:
      - method: XOR with 0xAA
      - alternative: AES-128-ECB
```

### Task 5.2: Key Extraction Verification
**Query:** `ACTION_KEY API_KEY USER_INFO_KEY salt secret`
**Output:** `KEY_VERIFICATION.md`

```yaml
verify:
  ACTION_KEY: "TAO_{313-894..."  # Confirmed
  API_KEY: "9f758e2dec..."       # Confirmed  
  XOR_KEY: 0xAA                  # Confirmed
  LOGIN_SALT: "evony"            # Confirmed
```

### Task 5.3: Session Token Format
**Query:** `sessionKey token uid playerId server`
**Output:** `TOKEN_FORMAT.md`

```yaml
extract:
  token:
    format: "uid_timestamp_hash"
    generation: server_side
    validation: signature_check
    expiry: session_timeout
```

---

## Phase 6: AutoEvony Integration (Priority: P1)

### Task 6.1: Real Command Vocabulary
**Query:** `AutoEvony command script train attack build`
**Output:** `AUTOEVONY_COMMANDS.md`

```yaml
extract:
  commands:
    - command_name
    - syntax
    - parameters
    - underlying_protocol_call
    - examples
```

### Task 6.2: Variable System
**Query:** `setvar getvar variable array string int`
**Output:** `AUTOEVONY_VARIABLES.md`

```yaml
extract:
  variables:
    types: [int, string, array]
    scope: [local, global]
    special: [%city%, %hero%, %coords%]
```

### Task 6.3: Control Flow
**Query:** `if else loop while goto label call return`
**Output:** `AUTOEVONY_CONTROL.md`

```yaml
extract:
  control:
    conditionals: [if, else, endif]
    loops: [loop, endloop, while]
    jumps: [goto, label, call, return]
```

---

## Phase 7: Asset Extraction (Priority: P2)

### Task 7.1: SWF Sprite Extraction
**Source:** `Evony_Source/*.swf`
**Tool:** FFDec / RABCDAsm
**Output:** `assets/sprites/`

### Task 7.2: Sound Extraction
**Source:** `Evony_Source/*.swf`
**Output:** `assets/sounds/`

### Task 7.3: Animation Extraction
**Source:** `Evony_Source/*.swf`
**Output:** `assets/animations/`

---

## Phase 8: Cross-Reference Building (Priority: P2)

### Task 8.1: Command→Handler Map
```
troop.produceTroop → TroopCommands.produceTroop → ResponseDispatcher.SERVER_TROOP_UPDATE
```

### Task 8.2: UI→Protocol Map
```
TrainButton.click → Sender.sendMessage("troop.produceTroop") → SERVER_TROOP_UPDATE → TroopList.refresh
```

### Task 8.3: Script→Protocol Map
```
AutoEvony: train a:1000 → troop.produceTroop(troopType=6, num=1000)
```

---

## 📊 Execution Timeline

| Week | Phase | Tasks | Deliverables |
|------|-------|-------|--------------|
| 1 | Protocol | 1.1-1.4 | Command catalog, error codes |
| 2 | Game Data | 2.1-2.5 | All data tables |
| 3 | UI | 3.1-3.4 | Component hierarchy |
| 4 | Logic | 4.1-4.4 | All formulas |
| 5 | Security | 5.1-5.3 | Crypto documentation |
| 6 | AutoEvony | 6.1-6.3 | Bot integration specs |
| 7 | Assets | 7.1-7.3 | Extracted assets |
| 8 | X-Ref | 8.1-8.3 | Cross-reference docs |

---

## 🔧 RAG Query Templates

### Template 1: Symbol Extraction
```
Query: [ClassName] [methodName] function return
Output: Symbol definition with parameters and return type
```

### Template 2: Constant Extraction
```
Query: const static final [CONSTANT_NAME] value
Output: Constant value and usage locations
```

### Template 3: Flow Extraction
```
Query: [startFunction] → [middleFunction] → [endFunction]
Output: Call chain with data transformations
```

### Template 4: Schema Extraction
```
Query: [BeanClass] property var public private
Output: Object schema with all properties
```

---

## ✅ Completion Checklist

### Phase 1: Protocol ☐
- [ ] 1.1 Command Catalog
- [ ] 1.2 Response Map
- [ ] 1.3 Error Codes
- [ ] 1.4 Session Lifecycle

### Phase 2: Game Data ☐
- [ ] 2.1 Building Data
- [ ] 2.2 Troop Data
- [ ] 2.3 Research Data
- [ ] 2.4 Item Data
- [ ] 2.5 Hero System

### Phase 3: UI ☐
- [ ] 3.1 View Hierarchy
- [ ] 3.2 Dialog Catalog
- [ ] 3.3 Event Handlers
- [ ] 3.4 Styles

### Phase 4: Logic ☐
- [ ] 4.1 Resource Formulas
- [ ] 4.2 Combat Formulas
- [ ] 4.3 March Timing
- [ ] 4.4 Queue System

### Phase 5: Security ☐
- [ ] 5.1 Encryption Pipeline
- [ ] 5.2 Key Verification
- [ ] 5.3 Token Format

### Phase 6: AutoEvony ☐
- [ ] 6.1 Command Vocabulary
- [ ] 6.2 Variable System
- [ ] 6.3 Control Flow

### Phase 7: Assets ☐
- [ ] 7.1 Sprites
- [ ] 7.2 Sounds
- [ ] 7.3 Animations

### Phase 8: Cross-Reference ☐
- [ ] 8.1 Command→Handler
- [ ] 8.2 UI→Protocol
- [ ] 8.3 Script→Protocol

---

*Part of Svony MCP - Evony Reverse Engineering Project*
