# AMF3 Protocol Reference

Action Message Format (AMF3) protocol details for Evony communication.

## AMF3 Type Markers

| Marker | Value | Description |
|--------|-------|-------------|
| UNDEFINED | 0x00 | Undefined value |
| NULL | 0x01 | Null value |
| FALSE | 0x02 | Boolean false |
| TRUE | 0x03 | Boolean true |
| INTEGER | 0x04 | 29-bit integer |
| DOUBLE | 0x05 | 64-bit float |
| STRING | 0x06 | UTF-8 string |
| XML_DOC | 0x07 | XML document |
| DATE | 0x08 | Date object |
| ARRAY | 0x09 | Array |
| OBJECT | 0x0A | Object |
| XML | 0x0B | XML string |
| BYTEARRAY | 0x0C | Byte array |

## Integer Encoding (U29)

AMF3 uses variable-length integer encoding:

```
1 byte:  0xxxxxxx                    (0-127)
2 bytes: 1xxxxxxx 0xxxxxxx           (128-16383)
3 bytes: 1xxxxxxx 1xxxxxxx 0xxxxxxx  (16384-2097151)
4 bytes: 1xxxxxxx 1xxxxxxx 1xxxxxxx xxxxxxxx (2097152-536870911)
```

### Reference Bit
The low bit indicates reference vs value:
- `0` = Reference to previously seen value
- `1` = Inline value follows

## String Encoding

```python
def write_string(s: str) -> bytes:
    encoded = s.encode('utf-8')
    length = len(encoded)
    
    if length == 0:
        return bytes([0x01])  # Empty string marker
    
    # Length << 1 | 1 (inline flag)
    return write_u29((length << 1) | 1) + encoded
```

## Object Encoding

### Dynamic Object
```
0x0A                    # Object marker
0x0B                    # Dynamic class, 0 sealed members
[class name string]     # Class name (or empty)
[key string, value]*    # Dynamic properties
0x01                    # Empty string = end of object
```

### Example: Command Object
```python
{
    "cmd": "army.newArmy",
    "params": {"cityId": 123},
    "sessionKey": "abc123"
}
```

Encoded:
```
0A                      # Object marker
0B                      # Dynamic class
01                      # Empty class name
07 63 6D 64             # "cmd" key
06 ...                  # "army.newArmy" value
...
01                      # End marker
```

## Array Encoding

```python
def write_array(arr: list) -> bytes:
    result = bytes([0x09])  # Array marker
    length = len(arr)
    result += write_u29((length << 1) | 1)  # Length with inline flag
    result += bytes([0x01])  # Empty key (dense array)
    for item in arr:
        result += write_value(item)
    return result
```

## Evony Packet Structure

### Request Packet
```
┌────────────────────────────────────────┐
│ AMF3 Envelope                          │
├────────────────────────────────────────┤
│ Version: 0x00 0x03 (AMF3)              │
│ Header Count: 0x00 0x00                │
│ Message Count: 0x00 0x01               │
├────────────────────────────────────────┤
│ Message                                │
├────────────────────────────────────────┤
│ Target URI: "null"                     │
│ Response URI: "/1"                     │
│ Length: [4 bytes]                      │
├────────────────────────────────────────┤
│ Body (AMF3 Object)                     │
├────────────────────────────────────────┤
│ {                                      │
│   "cmd": "command.name",               │
│   "params": {...},                     │
│   "sessionKey": "...",                 │
│   "signature": "md5..."                │
│ }                                      │
└────────────────────────────────────────┘
```

### Response Packet
```
┌────────────────────────────────────────┐
│ AMF3 Envelope                          │
├────────────────────────────────────────┤
│ Version: 0x00 0x03                     │
│ Header Count: 0x00 0x00                │
│ Message Count: 0x00 0x01               │
├────────────────────────────────────────┤
│ Message                                │
├────────────────────────────────────────┤
│ Target URI: "/1/onResult"              │
│ Response URI: "null"                   │
│ Length: [4 bytes]                      │
├────────────────────────────────────────┤
│ Body (AMF3 Object)                     │
├────────────────────────────────────────┤
│ {                                      │
│   "ok": 1,                             │
│   "msg": "success",                    │
│   "data": {...}                        │
│ }                                      │
└────────────────────────────────────────┘
```

## Python AMF Implementation

```python
import struct
from io import BytesIO

class AMF3Writer:
    def __init__(self):
        self.stream = BytesIO()
        self.string_refs = []
        self.object_refs = []
    
    def write_u29(self, value: int) -> None:
        if value < 0x80:
            self.stream.write(bytes([value]))
        elif value < 0x4000:
            self.stream.write(bytes([
                (value >> 7) | 0x80,
                value & 0x7F
            ]))
        elif value < 0x200000:
            self.stream.write(bytes([
                (value >> 14) | 0x80,
                (value >> 7) | 0x80,
                value & 0x7F
            ]))
        else:
            self.stream.write(bytes([
                (value >> 22) | 0x80,
                (value >> 15) | 0x80,
                (value >> 8) | 0x80,
                value & 0xFF
            ]))
    
    def write_string(self, s: str) -> None:
        if s in self.string_refs:
            idx = self.string_refs.index(s)
            self.write_u29(idx << 1)  # Reference
        else:
            self.string_refs.append(s)
            encoded = s.encode('utf-8')
            self.write_u29((len(encoded) << 1) | 1)
            self.stream.write(encoded)
    
    def write_object(self, obj: dict) -> None:
        self.stream.write(bytes([0x0A]))  # Object marker
        self.stream.write(bytes([0x0B]))  # Dynamic class
        self.stream.write(bytes([0x01]))  # Empty class name
        
        for key, value in obj.items():
            self.write_string(key)
            self.write_value(value)
        
        self.stream.write(bytes([0x01]))  # End marker
    
    def write_value(self, value) -> None:
        if value is None:
            self.stream.write(bytes([0x01]))
        elif isinstance(value, bool):
            self.stream.write(bytes([0x03 if value else 0x02]))
        elif isinstance(value, int):
            self.stream.write(bytes([0x04]))
            self.write_u29(value)
        elif isinstance(value, float):
            self.stream.write(bytes([0x05]))
            self.stream.write(struct.pack('>d', value))
        elif isinstance(value, str):
            self.stream.write(bytes([0x06]))
            self.write_string(value)
        elif isinstance(value, dict):
            self.write_object(value)
        elif isinstance(value, list):
            self.write_array(value)
```

## Useful Libraries

| Language | Library | Notes |
|----------|---------|-------|
| Python | PyAMF | Most complete |
| Python | Py3AMF | Python 3 fork |
| JavaScript | amf.js | Browser compatible |
| Java | BlazeDS | Adobe official |
| C# | FluorineFx | .NET implementation |

## Wireshark Filter

```
# Capture AMF traffic
tcp.port == 80 and http.content_type contains "amf"

# Or on game port
tcp.port == 443 and data.len > 0
```
