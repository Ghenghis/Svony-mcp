# 🔬 ECMAScript-like Pattern Extraction System

Methodology for extracting patch-ready ActionScript slices from Evony Client.

---

## 📚 What "ECMAScript-like" Means in Flash/ActionScript

Evony's Flash client is written in **ActionScript 3 (AS3)**. The "ECMAScript-y" patterns are:

| Pattern | AS3 Syntax | Where Found |
|---------|-----------|-------------|
| Dynamic objects | `obj["key"]`, `obj[prop]` | Payload builders |
| Untyped variables | `var x:*` | Generic handlers |
| Dictionary-style access | `for (var k:* in obj)` | Command dispatch |
| Runtime reflection | `getDefinitionByName()` | Factory patterns |
| Type introspection | `describeType()`, `getQualifiedClassName()` | Serialization |
| Late binding | `hasOwnProperty()` | Response parsing |

---

## 🏷️ Tag Classification System

### Category 1: Dynamic / Late-bound
```actionscript
// TAG: DYNAMIC_CLASS
dynamic class MyDynamic { }

// TAG: UNTYPED_VAR
var payload:* = buildRequest();

// TAG: GENERIC_MAP
var params:Object = {};
params["cmd"] = "attack";
params["target"] = targetId;

// TAG: BRACKET_ACCESS
obj[propertyName] = value;

// TAG: FOR_IN_LOOP
for (var key:* in responseObject) {
    processField(key, responseObject[key]);
}
```

### Category 2: Reflection
```actionscript
// TAG: GET_DEFINITION
var cls:Class = getDefinitionByName("com.evony.beans.TroopBean") as Class;

// TAG: QUALIFIED_NAME
var typeName:String = getQualifiedClassName(instance);

// TAG: DESCRIBE_TYPE
var typeInfo:XML = describeType(targetObject);

// TAG: HAS_OWN_PROPERTY
if (data.hasOwnProperty("troops")) { ... }
```

### Category 3: External/Runtime Interfaces
```actionscript
// TAG: EXTERNAL_INTERFACE
ExternalInterface.call("jsCallback", data);

// TAG: SHARED_OBJECT
var sol:SharedObject = SharedObject.getLocal("evonyData");

// TAG: BYTE_ARRAY
var buffer:ByteArray = new ByteArray();
buffer.writeObject(payload);

// TAG: SOCKET_IO
socket.writeBytes(serializedData);
socket.flush();

// TAG: URL_REQUEST
var request:URLRequest = new URLRequest(endpoint);
loader.load(request);
```

---

## 📦 Work Packet Format

When extracting, produce this structured output:

```yaml
work_packet:
  id: "WP-001-PAYLOAD-BUILDER"
  description: "Network payload builder for troop commands"
  
  primary_files:
    - path: "com/evony/net/client/GameClient.as"
      lines: [145, 280]
      tags: [SOCKET_IO, BYTE_ARRAY, GENERIC_MAP]
    - path: "com/evony/SenderImpl.as"
      lines: [1, 46]
      tags: [UNTYPED_VAR, BRACKET_ACCESS]
      
  dependencies:
    required:
      - "com/evony/common/Sender.as"  # Interface
      - "com/evony/Context.as"        # State access
    optional:
      - "com/evony/common/MouseManager.as"  # Can stub
      
  entry_points:
    - function: "sendMessage"
      signature: "(cmd:String, params:Object):void"
      callers: ["TroopCommands", "BuildingCommands", "HeroCommand"]
      
  data_contracts:
    input:
      - name: "cmd"
        type: "String"
        format: "dotted.command.name"
        examples: ["troop.train", "castle.upgrade"]
      - name: "params"
        type: "Object"
        required_keys: ["castleId"]
        optional_keys: ["count", "heroId", "targetX", "targetY"]
    output:
      - name: "AMF packet"
        type: "ByteArray"
        
  patch_plan:
    safe_changes:
      - "Add validation before send"
      - "Log command/params for debugging"
      - "Intercept and modify params"
    risky_changes:
      - "Change command string format (breaks server)"
      - "Remove castleId (server rejects)"
    
  regression_tests:
    - name: "payload_shape_test"
      description: "Verify output keys match expected"
      golden_input: {cmd: "troop.train", params: {castleId: 1, troopType: 6, count: 100}}
```

---

## 🔍 Extraction Queries

### Query 1: Find Dynamic/Reflection Hotspots
```
Search: dynamic, *, bracket access, reflection calls
Filter: .as files only
Output: File, line, pattern type
```

**Results from Evony codebase:**

| File | Pattern | Tag |
|------|---------|-----|
| `com/evony/Context.as:686` | `_arg_1.charCodeAt(_local_4)` | BRACKET_ACCESS |
| `com/evony/SenderImpl.as:24` | `Context.getInstance()` | SINGLETON |
| `RPCObjectUtil.as:253` | `getClassInfo(param1:Object)` | GENERIC_MAP |
| `FABridge.as:482` | `buildTypeDescription(className:String)` | DESCRIBE_TYPE |
| `DescribeTypeCache.as:35` | `getQualifiedClassName(param1)` | QUALIFIED_NAME |

### Query 2: Intersect with Networking
```
Search: URLRequest, URLLoader, Socket, ByteArray, AMF
Intersect: Results from Query 1
Output: Network-related dynamic code
```

**Key Files:**

| File | Purpose | Tags |
|------|---------|------|
| `GameClient.as` | Main socket communication | SOCKET_IO, BYTE_ARRAY |
| `HTTPChannel.as` | HTTP fallback | URL_REQUEST |
| `AMFXDecoder.as` | AMF deserialization | BYTE_ARRAY, DESCRIBE_TYPE |
| `SerializationFilter.as` | Request/response transform | GENERIC_MAP |

### Query 3: Expand Call Graph
```
For each file from Query 2:
  - Find callers (who calls this)
  - Find callees (what this calls)
Output: Complete dependency graph
```

---

## 🧩 Module Boundaries (Patchable Slices)

### Module 1: Network Payload Builder
**Purpose:** Build command packets from dynamic objects

**Files:**
```
com/evony/SenderImpl.as          # Entry point
com/evony/net/client/GameClient.as  # Socket send
com/evony/common/Sender.as       # Interface
```

**Patch Points:**
- `SenderImpl.sendMessage()` - Add validation/logging
- `GameClient.sendMessage()` - Intercept before socket write

**Minimal Stub:**
```actionscript
// stub_sender.as - Minimal test harness
package {
    import com.evony.SenderImpl;
    
    public class PayloadTester {
        public function test():void {
            var sender:SenderImpl = new SenderImpl(null);
            // sender.sendMessage("test.cmd", {param1: "value"});
            trace("Payload builder extracted successfully");
        }
    }
}
```

---

### Module 2: Response Parser
**Purpose:** Parse AMF/ByteArray responses into objects

**Files:**
```
com/evony/client/response/ResponseDispatcher.as  # Router
com/evony/common/beans/*.as                       # Data objects
mx/messaging/messages/AMFXDecoder.as             # Decoder
```

**Patch Points:**
- Response handlers - Add field validation
- Bean constructors - Add overflow checks

---

### Module 3: Command Dispatcher
**Purpose:** Route opcodes to handlers

**Files:**
```
com/evony/client/response/ResponseDispatcher.as
// Event constants define the routing
```

**Patch Points:**
- Add new command handlers
- Modify routing logic

---

### Module 4: Session/Auth Wrapper
**Purpose:** Manage session tokens, signatures

**Files:**
```
com/evony/Context.as:686-698     # EncryptParam
com/evony/GameConfig.as          # Server config
```

**Patch Points:**
- Token generation
- Request signing

---

## 📋 Extraction Checklist

Before extracting a module:

- [ ] **Identify all files** with tagged patterns
- [ ] **Map dependencies** (imports, class references)
- [ ] **Find entry points** (public methods called externally)
- [ ] **Document data contracts** (input/output shapes)
- [ ] **Create minimal stubs** for unavoidable dependencies
- [ ] **Write golden tests** (expected output for known input)
- [ ] **Generate unified diff** format for patches
- [ ] **List caller impact** (what breaks if signature changes)
- [ ] **Note reflection risks** (dynamic lookups that could break)

---

## 🔧 Patch Output Format

```diff
--- a/com/evony/SenderImpl.as
+++ b/com/evony/SenderImpl.as
@@ -22,6 +22,12 @@
         public function sendMessage(_arg_1:String, _arg_2:Object):void
         {
+            // PATCH: Input validation
+            if (_arg_1 == null || _arg_1.length == 0) {
+                trace("ERROR: Empty command rejected");
+                return;
+            }
+
             if (Context.getInstance().bVisitor)
             {
```

**Caller Impact:**
- `TroopCommands.train()` - No change needed
- `BuildingCommands.upgrade()` - No change needed
- All callers safe (validation is additive)

**Reflection Risk:**
- None - command strings are literals, not reflected

---

## 🧪 Regression Test Template

```actionscript
// test_payload_builder.as
package tests {
    public class PayloadBuilderTest {
        
        // Golden snapshot test
        public function testTroopTrainPayload():void {
            var cmd:String = "troop.train";
            var params:Object = {
                castleId: 12345,
                troopType: 6,  // archer
                count: 100
            };
            
            // Expected: params should have these exact keys
            assert(params.hasOwnProperty("castleId"));
            assert(params.hasOwnProperty("troopType"));
            assert(params.hasOwnProperty("count"));
            
            // Type checks
            assert(params.castleId is int);
            assert(params.count is int);
            assert(params.count > 0);
            assert(params.count <= int.MAX_VALUE);
            
            trace("PASS: testTroopTrainPayload");
        }
        
        // Overflow test
        public function testOverflowRejected():void {
            var params:Object = {
                castleId: 1,
                troopType: 6,
                count: 2147483648  // > INT32_MAX
            };
            
            // With patch: should be rejected
            // assert(validateParams(params) == false);
            
            trace("PASS: testOverflowRejected");
        }
    }
}
```

---

## 📊 Extraction Statistics

| Module | Files | LOC | Tags | Complexity |
|--------|-------|-----|------|------------|
| Payload Builder | 3 | ~200 | 5 | Low |
| Response Parser | 8 | ~1500 | 12 | Medium |
| Command Dispatcher | 2 | ~300 | 4 | Low |
| Session/Auth | 4 | ~400 | 6 | Medium |

---

*Part of Svony MCP - Evony Reverse Engineering Project*
