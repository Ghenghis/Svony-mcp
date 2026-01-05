# 🔧 ECMAScript Bug Fix Patterns

Standardized fix patterns for common ActionScript bugs in Evony Client.

---

## Pattern 1: Integer Overflow Protection

### Problem
```actionscript
// VULNERABLE
public var troops:int = 0;
troops = troops + amount;  // Can overflow at 2,147,483,647
```

### Solution
```actionscript
// SAFE - With bounds checking
public function addTroops(amount:int):Boolean {
    // Check for positive overflow
    if (amount > 0 && troops > int.MAX_VALUE - amount) {
        trace("ERROR: Troop overflow prevented");
        return false;
    }
    // Check for negative overflow
    if (amount < 0 && troops < int.MIN_VALUE - amount) {
        trace("ERROR: Troop underflow prevented");
        return false;
    }
    troops += amount;
    return true;
}

// Alternative: Use Number type for large values
public var troopsLarge:Number = 0;  // 64-bit floating point
```

### Utility Function
```actionscript
public class SafeMath {
    public static function safeAdd(a:int, b:int):int {
        if (b > 0 && a > int.MAX_VALUE - b) return int.MAX_VALUE;
        if (b < 0 && a < int.MIN_VALUE - b) return int.MIN_VALUE;
        return a + b;
    }
    
    public static function safeMult(a:int, b:int):int {
        if (a == 0 || b == 0) return 0;
        var result:Number = Number(a) * Number(b);
        if (result > int.MAX_VALUE) return int.MAX_VALUE;
        if (result < int.MIN_VALUE) return int.MIN_VALUE;
        return int(result);
    }
}
```

---

## Pattern 2: Null Guard Clauses

### Problem
```actionscript
// VULNERABLE
public function processBuilding(typeId:int):void {
    var castle:CastleBean = getCurCastle();
    for each (var b:BuildingBean in castle.buildingsArray) {  // NPE!
        // ...
    }
}
```

### Solution
```actionscript
// SAFE - Early return pattern
public function processBuilding(typeId:int):BuildingBean {
    var castle:CastleBean = getCurCastle();
    if (castle == null) {
        trace("WARNING: No current castle");
        return null;
    }
    
    if (castle.buildingsArray == null) {
        trace("WARNING: No buildings array");
        return null;
    }
    
    for each (var b:BuildingBean in castle.buildingsArray) {
        if (b != null && b.typeId == typeId) {
            return b;
        }
    }
    return null;
}
```

### Utility Function
```actionscript
public class NullGuard {
    public static function requireNonNull(obj:Object, name:String):Object {
        if (obj == null) {
            throw new Error("Required object is null: " + name);
        }
        return obj;
    }
    
    public static function getOrDefault(obj:Object, defaultValue:Object):Object {
        return obj != null ? obj : defaultValue;
    }
}
```

---

## Pattern 3: Atomic State Changes

### Problem
```actionscript
// VULNERABLE - Race condition
public function setCurCastle(castle:CastleBean):void {
    if (this.curCastle == null || castle.id != this.curCastle.id) {
        this.curCastle = castle;  // State change
        dispatchEvent(new Event(EVENT_CASTLE_CHANGE));  // Event after
        // Race window between assignment and event!
    }
}
```

### Solution
```actionscript
// SAFE - Atomic operation with lock
private var _changingCastle:Boolean = false;

public function setCurCastle(castle:CastleBean):void {
    if (_changingCastle) {
        trace("WARNING: Castle change already in progress");
        return;
    }
    
    if (this.curCastle == null || castle.id != this.curCastle.id) {
        _changingCastle = true;
        try {
            var oldCastle:CastleBean = this.curCastle;
            this.curCastle = castle;
            
            // Dispatch with both old and new values
            dispatchEvent(new CastleChangeEvent(
                EVENT_CASTLE_CHANGE, oldCastle, castle
            ));
        } finally {
            _changingCastle = false;
        }
    }
}
```

---

## Pattern 4: TOCTOU Fix

### Problem
```actionscript
// VULNERABLE - Time-of-check-time-of-use
public function sendMessage(cmd:String, params:Object):void {
    if (getCurCastle() == null) {  // Check
        return;
    }
    // ... other code ...
    client.sendMessage(cmd, params);  // Use - castle could be null now!
}
```

### Solution
```actionscript
// SAFE - Capture value at check time
public function sendMessage(cmd:String, params:Object):void {
    var castle:CastleBean = getCurCastle();  // Capture once
    if (castle == null) {
        trace("WARNING: No castle, message not sent: " + cmd);
        return;
    }
    
    // Add castle ID to params to ensure correct targeting
    params.castleId = castle.id;
    
    client.sendMessage(cmd, params);
}
```

---

## Pattern 5: Event Listener Cleanup

### Problem
```actionscript
// VULNERABLE - Memory leak
public function Context() {
    var rd:ResponseDispatcher = ResponseDispatcher.getInstance();
    rd.addEventListener(SERVER_UPDATE, onUpdate);  // Never removed!
}
```

### Solution
```actionscript
// SAFE - Dispose pattern
public class Context {
    private var _listeners:Array = [];
    
    public function Context() {
        var rd:ResponseDispatcher = ResponseDispatcher.getInstance();
        addManagedListener(rd, SERVER_UPDATE, onUpdate);
    }
    
    private function addManagedListener(
        target:IEventDispatcher, 
        type:String, 
        handler:Function
    ):void {
        target.addEventListener(type, handler);
        _listeners.push({target: target, type: type, handler: handler});
    }
    
    public function dispose():void {
        for each (var l:Object in _listeners) {
            l.target.removeEventListener(l.type, l.handler);
        }
        _listeners = [];
    }
}
```

---

## Pattern 6: Timer Management

### Problem
```actionscript
// VULNERABLE - Timer never stopped
private var timer:Timer;

public function start():void {
    timer = new Timer(1000, 0);  // Infinite
    timer.addEventListener(TimerEvent.TIMER, onTick);
    timer.start();
}
// No stop method!
```

### Solution
```actionscript
// SAFE - Managed timer
private var _timer:Timer;
private var _timerHandler:Function;

public function startTimer(interval:int):void {
    stopTimer();  // Clean up existing
    
    _timer = new Timer(interval, 0);
    _timerHandler = onTick;
    _timer.addEventListener(TimerEvent.TIMER, _timerHandler);
    _timer.start();
}

public function stopTimer():void {
    if (_timer != null) {
        _timer.stop();
        _timer.removeEventListener(TimerEvent.TIMER, _timerHandler);
        _timer = null;
        _timerHandler = null;
    }
}

public function dispose():void {
    stopTimer();
}
```

---

## Pattern 7: Error Boundaries

### Problem
```actionscript
// VULNERABLE - No error handling
private function onBuildComplete(event:BuildCompleteEvent):void {
    var castle:CastleBean = getCastleById(event.castleId);
    castle.buildingsArray.addItem(event.building);  // Could throw
    dispatchEvent(new Event(UPDATE));
    // 100+ more lines of unguarded code...
}
```

### Solution
```actionscript
// SAFE - Error boundary
private function onBuildComplete(event:BuildCompleteEvent):void {
    try {
        handleBuildComplete(event);
    } catch (e:Error) {
        trace("ERROR in onBuildComplete: " + e.message);
        trace(e.getStackTrace());
        // Optionally dispatch error event
        dispatchEvent(new ErrorEvent(ErrorEvent.ERROR, false, false, e.message));
    }
}

private function handleBuildComplete(event:BuildCompleteEvent):void {
    var castle:CastleBean = getCastleById(event.castleId);
    if (castle == null) {
        throw new Error("Castle not found: " + event.castleId);
    }
    
    if (castle.buildingsArray == null) {
        castle.buildingsArray = new ArrayCollection();
    }
    
    castle.buildingsArray.addItem(event.building);
    dispatchEvent(new Event(UPDATE));
}
```

---

## Pattern 8: Input Validation

### Problem
```actionscript
// VULNERABLE - No validation
public function sendCommand(cmd:String, params:Object):void {
    client.send(cmd, params);  // Anything goes!
}
```

### Solution
```actionscript
// SAFE - Validated commands
private static const ALLOWED_COMMANDS:Array = [
    "castle.getInfo",
    "troop.train",
    "building.upgrade",
    // ... whitelist
];

public function sendCommand(cmd:String, params:Object):Boolean {
    // Validate command
    if (cmd == null || cmd.length == 0) {
        trace("ERROR: Empty command");
        return false;
    }
    
    if (ALLOWED_COMMANDS.indexOf(cmd) == -1) {
        trace("ERROR: Unknown command: " + cmd);
        return false;
    }
    
    // Validate params
    if (params == null) {
        params = {};
    }
    
    // Sanitize string params
    for (var key:String in params) {
        if (params[key] is String) {
            params[key] = sanitizeString(params[key]);
        }
    }
    
    client.send(cmd, params);
    return true;
}

private function sanitizeString(s:String):String {
    if (s == null) return "";
    // Remove control characters, limit length
    return s.replace(/[\x00-\x1F]/g, "").substr(0, 1000);
}
```

---

## Pattern 9: Type Safety

### Problem
```actionscript
// VULNERABLE - Untyped variable
var result:* = getData();  // Could be anything
var count:int = result.count;  // Runtime error if wrong type
```

### Solution
```actionscript
// SAFE - Explicit typing with checks
public function getCount():int {
    var data:Object = getData();
    
    if (data == null) {
        return 0;
    }
    
    if (!data.hasOwnProperty("count")) {
        trace("WARNING: Data missing 'count' property");
        return 0;
    }
    
    var count:* = data.count;
    if (!(count is int) && !(count is Number)) {
        trace("WARNING: count is not numeric: " + typeof(count));
        return 0;
    }
    
    return int(count);
}
```

---

## Quick Reference

| Bug Type | Fix Pattern | Key Technique |
|----------|-------------|---------------|
| Integer Overflow | Pattern 1 | Bounds checking before arithmetic |
| Null Reference | Pattern 2 | Early return guards |
| Race Condition | Pattern 3 | Lock flag + atomic operations |
| TOCTOU | Pattern 4 | Capture value at check time |
| Memory Leak | Pattern 5 | Managed listener array + dispose |
| Timer Leak | Pattern 6 | Stop + remove + null |
| Missing Error Handling | Pattern 7 | Try/catch wrapper |
| Missing Validation | Pattern 8 | Whitelist + sanitize |
| Type Coercion | Pattern 9 | Explicit type checks |

---

*Part of Svony MCP - Evony Reverse Engineering Project*
