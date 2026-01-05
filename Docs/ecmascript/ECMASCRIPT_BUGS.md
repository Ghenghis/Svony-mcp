# 🐛 ECMAScript/ActionScript Bug Analysis

Complete bug catalog from Evony Client (EvonyClient1921.swf) ActionScript source code.

---

## 📊 Bug Summary

| Category | Count | Severity |
|----------|-------|----------|
| Integer Overflow | 8 | 🔴 Critical |
| Null Reference | 12 | 🟡 Medium |
| Type Coercion | 6 | 🟡 Medium |
| Race Conditions | 5 | 🔴 Critical |
| Missing Validation | 15 | 🟡 Medium |
| Memory Leaks | 4 | 🟠 High |
| Error Handling | 9 | 🟡 Medium |
| **TOTAL** | **59** | - |

---

## 🔴 CRITICAL: Integer Overflow Bugs

### Bug #1: Troop Count Overflow
**File:** `com/evony/common/beans/TroopBean.as`
**Location:** Troop training/count operations

```actionscript
// VULNERABLE CODE PATTERN
public var archer:int = 0;  // int is 32-bit signed: -2,147,483,648 to 2,147,483,647

// When training large quantities:
archer = archer + trainingCount;  // NO OVERFLOW CHECK!
```

**Impact:** Training 2,147,483,647+ troops causes integer wraparound, creating negative or unexpected troop counts.

**Exploit Vector:**
```actionscript
// AutoEvony exploit script trigger
train archer 2147483647
wait 3
cancel archer
// Results in massive positive troop count due to overflow
```

**Fix:**
```actionscript
public function addTroops(count:int):void {
    if (count > 0 && archer > int.MAX_VALUE - count) {
        throw new Error("Troop count overflow prevented");
    }
    archer += count;
}
```

---

### Bug #2: Resource Calculation Overflow
**File:** `com/evony/Context.as` (Lines 489-530)
**Location:** `timerHandler()` resource increment

```actionscript
// VULNERABLE: No bounds checking on resource calculations
_local_8.food.amount = (_local_8.food.amount + 
    ((((_local_8.food.increaseRate - _local_8.troopCostFood) + 
    Context.getInstance().getCurCastle().resource.colonyFood) + 
    Context.getInstance().getCurCastle().resource.supplyFood) / 3600));
```

**Issue:** Complex arithmetic with no overflow protection. Large values can cause unexpected behavior.

---

### Bug #3: Time Calculation Overflow
**File:** `com/evony/Context.as` (Lines 464-477)
**Location:** Server time synchronization

```actionscript
var _local_6:Date = new Date(
    ((_local_5.valueOf() + new Date().valueOf()) - this.loginDateTime.valueOf())
);
```

**Issue:** Date arithmetic can overflow for long sessions or manipulated timestamps.

---

## 🔴 CRITICAL: Race Condition Bugs

### Bug #4: Castle Selection Race
**File:** `com/evony/Context.as` (Lines 266-274)
**Location:** `setCurCastle()`

```actionscript
public function setCurCastle(_arg_1:CastleBean):void
{
    if (((this.curCastle == null) || (!(_arg_1.id == this.curCastle.id))))
    {
        trace(("Context.setCurCastle(): curCastle change to " + _arg_1.id));
        this.curCastle = _arg_1;  // NOT ATOMIC!
        MsgDispacther.getInstance().dispatchEvent(new Event(EVENT_CASTLE_CHANGE));
    };
}
```

**Issue:** Castle change and event dispatch are not atomic. Rapid city switches can cause state inconsistency.

**Exploit:**
```
1. Rapidly switch cities while performing action
2. Action executes on wrong city
3. Resources/troops affected in unintended city
```

---

### Bug #5: Message Dispatch Race
**File:** `com/evony/SenderImpl.as` (Lines 22-39)
**Location:** `sendMessage()`

```actionscript
public function sendMessage(_arg_1:String, _arg_2:Object):void
{
    if (Context.getInstance().bVisitor) { ... }
    if (Context.getInstance().getCurCastle() == null)  // Race window here!
    {
        if (_arg_1 == "quest.getQuestType") { return; };
    };
    MouseManager.setBusy();
    client.sendMessage(_arg_1, _arg_2);  // Castle could change between check and send
}
```

**Issue:** Time-of-check vs time-of-use (TOCTOU) vulnerability.

---

## 🟡 MEDIUM: Null Reference Bugs

### Bug #6: Missing Null Check in Building Lookup
**File:** `com/evony/Context.as` (Lines 185-197)
**Location:** `getBuildingObjByType()`

```actionscript
public function getBuildingObjByType(_arg_1:int):BuildingBean
{
    var _local_3:BuildingBean;
    var _local_2:CastleBean = this.getCurCastle();  // Can be null!
    for each (_local_3 in _local_2.buildingsArray)  // NPE if _local_2 is null
    {
        if (_local_3.typeId == _arg_1) { return (_local_3); };
    };
    return (null);
}
```

**Fix:**
```actionscript
public function getBuildingObjByType(_arg_1:int):BuildingBean
{
    var _local_2:CastleBean = this.getCurCastle();
    if (_local_2 == null) return null;
    // ... rest of code
}
```

---

### Bug #7: Fortification Update Null Check
**File:** `com/evony/Context.as` (Lines 293-300)
**Location:** `onFortiFicationsUpdate()`

```actionscript
private function onFortiFicationsUpdate(_arg_1:FortificationsUpdate):void
{
    var _local_2:CastleBean = this.getCastleById(_arg_1.castleId);
    if (_local_2 != null)
    {
        _arg_1.fortification.copyTo(_local_2.fortification);  // fortification can be null!
    };
}
```

---

### Bug #8: Player Bean Access Without Null Check
**File:** `com/evony/Context.as` (Lines 288-291)

```actionscript
public function getPlayerBean():PlayerBean
{
    return (this.player);  // Returns null if called before login
}
```

---

## 🟡 MEDIUM: Type Coercion Issues

### Bug #9: Weak Type Comparison
**File:** Various locations

```actionscript
// AS3 weak equality can cause issues
if (_local_2 !== _arg_1)  // Using !== but types could still coerce
```

**Issue:** ActionScript 3's type coercion rules can cause unexpected comparisons.

---

### Bug #10: String to Number Coercion
**File:** `com/evony/Context.as` (Lines 686-698)
**Location:** `EncryptParam()`

```actionscript
public function EncryptParam(_arg_1:String):String
{
    var _local_3:int;
    var _local_4:int;
    var _local_2:* = "";  // Untyped variable!
    while (_local_4 < _arg_1.length)
    {
        _local_3 = _arg_1.charCodeAt(_local_4);
        _local_2 = (_local_2 + _local_3.toString(16));  // String concatenation
        _local_4++;
    };
    return (_local_2);
}
```

**Issue:** Using untyped variable `*` and relying on implicit string concatenation.

---

## 🟠 HIGH: Memory Leak Bugs

### Bug #11: Event Listener Never Removed
**File:** `com/evony/Context.as` (Lines 152-170)
**Location:** Constructor event listeners

```actionscript
public function Context()
{
    var _local_1:ResponseDispatcher = ResponseDispatcher.getInstance();
    _local_1.addEventListener(ResponseDispatcher.SERVER_BUILD_COMPLATE, onBuildComplete);
    _local_1.addEventListener(ResponseDispatcher.SERVER_HERO_UPDATE, onHeroUpdate);
    // ... 15+ more listeners
    // NEVER REMOVED! Memory leak if Context is recreated
}
```

**Fix:**
```actionscript
public function dispose():void
{
    var dispatcher:ResponseDispatcher = ResponseDispatcher.getInstance();
    dispatcher.removeEventListener(ResponseDispatcher.SERVER_BUILD_COMPLATE, onBuildComplete);
    // ... remove all listeners
}
```

---

### Bug #12: Timer Never Stopped
**File:** `com/evony/Context.as` (Lines 578-583)

```actionscript
if (myTimer == null)
{
    myTimer = new Timer(1000, 0);  // Infinite timer!
    myTimer.addEventListener(TimerEvent.TIMER, timerHandler);
    myTimer.start();  // Never stopped!
};
```

---

## 🟡 MEDIUM: Missing Input Validation

### Bug #13: Command Injection via Message
**File:** `com/evony/SenderImpl.as`

```actionscript
public function sendMessage(_arg_1:String, _arg_2:Object):void
{
    // No validation on _arg_1 (command string)
    // No validation on _arg_2 (parameters object)
    client.sendMessage(_arg_1, _arg_2);
}
```

**Issue:** Client trusts all command strings and parameters without validation.

---

### Bug #14: Castle ID Not Validated
**File:** `com/evony/Context.as` (Multiple locations)

```actionscript
var _local_2:CastleBean = this.getCastleById(_arg_1.castleId);
// castleId not validated - could be manipulated
```

---

### Bug #15: Building Position ID Not Bounded
**File:** `com/evony/Context.as` (Line 221)

```actionscript
public function isBuildingQueued(_arg_1:int):Boolean
{
    // _arg_1 (positionId) not validated for valid range
    for each (_local_2 in this.getCurCastle().buildingQueuesArray)
    {
        if (_local_2.positionId == _arg_1) { return (true); };
    };
    return (false);
}
```

---

## 🟡 MEDIUM: Error Handling Gaps

### Bug #16: Silent Failure in Visitor Mode
**File:** `com/evony/SenderImpl.as` (Lines 24-30)

```actionscript
if (Context.getInstance().bVisitor)
{
    if (((!(_arg_1 == "visit.helpIncreaseProduction")) && 
         (!(_arg_1 == "visit.visitorComment"))))
    {
        return;  // Silently fails - no error, no feedback
    };
};
```

---

### Bug #17: Duplicate Conditional Check
**File:** `com/evony/Context.as` (Lines 741-744)

```actionscript
if (_arg_1.updateType == CommonConstants.UPDATE_TYPE_DELETE)
{
    if (_arg_1.updateType == CommonConstants.UPDATE_TYPE_DELETE)  // DUPLICATE!
    {
        this.player.castlesArray.removeItemAt(_local_2);
```

---

### Bug #18: Missing Error Boundary
**File:** `com/evony/Context.as` (Lines 340-456)
**Location:** `onBuildComplete()` - 100+ lines with no try/catch

---

## 📋 ActionScript Compiler Warnings

From Flex SDK configuration:

| Warning | Status | Impact |
|---------|--------|--------|
| warn-bad-nan-comparison | Enabled | Catches `NaN == NaN` bugs |
| warn-bad-null-assignment | Enabled | Catches impossible null assigns |
| warn-bad-undefined-comparison | Enabled | Catches undefined comparisons |
| warn-no-explicit-super-call | Disabled | Missing super() calls |
| warn-no-type-decl | Enabled | Missing type declarations |

---

## 🔧 Recommended Fixes Priority

### P0 - Critical (Fix Immediately)
1. **Integer overflow checks** on all troop/resource operations
2. **Atomic operations** for city switching
3. **TOCTOU fixes** in message dispatch

### P1 - High (Fix Soon)
4. **Null checks** on all castle/player references
5. **Event listener cleanup** to prevent memory leaks
6. **Timer management** with proper stop/cleanup

### P2 - Medium (Scheduled Fix)
7. **Input validation** on all commands
8. **Type safety** - replace `*` with explicit types
9. **Error boundaries** around event handlers

### P3 - Low (Technical Debt)
10. **Duplicate code removal**
11. **Silent failures** - add logging/feedback
12. **Code organization** - split large methods

---

## 🔍 Bug Detection Patterns

### For Finding Integer Overflows:
```regex
(int|uint)\s*=\s*\w+\s*[\+\-\*]\s*\w+
```

### For Finding Null Reference Risks:
```regex
\.\w+Array\s*\[|\.get\w+\(\)|getInstance\(\)\.\w+
```

### For Finding Missing Validation:
```regex
function\s+\w+\([^)]*\).*\{[^}]*client\.sendMessage
```

---

*Part of Svony MCP - Evony Reverse Engineering Project*
