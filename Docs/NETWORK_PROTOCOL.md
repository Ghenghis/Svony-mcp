# 🌐 NETWORK PROTOCOL REFERENCE

Complete network protocol documentation extracted from RAG.

---

## 🔌 Connection Details

### Server Endpoints
```python
# From MASTER_RESOURCE_INDEX.md, evony_client.py
EVONY_SERVERS = {
    "cc2": {"host": "cc2.evony.com", "port": 443},
    "cc3": {"host": "cc3.evony.com", "port": 443},
    # ... more servers
}

# Known Endpoints
ENDPOINTS = {
    "home": "http://www.evony.com",
    "user": "http://user.evony.com/index.do",
    "pay": "http://pay.evony.com",
    "api": "http://api.evony.com",
}

# Connection: RAW TCP on port 443 (NOT SSL)
PORT = 443
```

### Connection Flow
```
# From PROTOCOL.md, EVONY_PROTOCOL.md

1. Client → Server: TCP connect to {server}.evony.com:443
2. Client → Server: "gameClient\x00" (identification)
3. Server → Client: AMF handshake response
4. Client → Server: VERSION_COMMAND
5. Server → Client: Version OK
6. Client → Server: LOGIN_COMMAND (email, password_hash)
7. Server → Client: Session token + player data
8. ... AMF3 command exchange ...
```

---

## 🔐 Authentication

### Login Flow
```python
# From auth_manager.py, PROTOCOL.md

# Step 1: Hash password
password_hash = md5(password.encode()).hexdigest()

# Step 2: Create login hash
login_hash = md5((username + password_hash + "evony").encode()).hexdigest()

# Step 3: Send login request
login_request = {
    "cmd": "login",
    "email": email,
    "passwordHash": login_hash,
    "server": server_id,
}

# Step 4: Receive session token
response = {
    "msg": "login success",
    "sessionKey": "abc123...",
    "player": {...}
}
```

### Password Hashing
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       PASSWORD HASHING                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   password  ──▶  MD5  ──▶  password_hash                                   │
│                                                                             │
│   username + password_hash + "evony"  ──▶  MD5  ──▶  login_hash           │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Session Management
```python
# From auth_manager.py
class SessionToken:
    token_value: str      # Base64 SHA256
    player_id: int
    server_id: str
    created_at: datetime
    expires_at: datetime
    
# Token generation
token_data = f"{player_id}:{server_id}:{timestamp}:{random}"
token_value = base64.b64encode(
    hashlib.sha256(token_data.encode()).digest()
).decode()

# Refresh token
refresh_token = secrets.token_hex(32)
```

---

## 📦 AMF Protocol

### Packet Structure
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         AMF PACKET STRUCTURE                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌──────────────┬──────────────────────────────────────────┐              │
│   │  Length (4B) │           AMF3 Encoded Body              │              │
│   │   Big-endian │                                          │              │
│   └──────────────┴──────────────────────────────────────────┘              │
│                                                                             │
│   Length = struct.pack('>L', len(body))                                    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### AMF3 Type Markers
```python
# From amf3.py, amf_codec.py
AMF3_TYPES = {
    0x00: 'undefined',
    0x01: 'null',
    0x02: 'false',
    0x03: 'true',
    0x04: 'integer',
    0x05: 'double',
    0x06: 'string',
    0x07: 'xml-doc',
    0x08: 'date',
    0x09: 'array',
    0x0A: 'object',
    0x0B: 'xml',
    0x0C: 'byte-array',
    0x0D: 'vector-int',
    0x0E: 'vector-uint',
    0x0F: 'vector-double',
    0x10: 'vector-object',
    0x11: 'dictionary',
}
```

### Encoder/Decoder
```python
# From amf_codec.py
class AMFDecoder:
    """Decodes AMF3 binary to Python"""
    
    def decode(self, data: bytes) -> AMFPacket:
        stream = io.BytesIO(data)
        # Read version (2 bytes)
        version = struct.unpack('>H', stream.read(2))[0]
        # Read header count
        header_count = struct.unpack('>H', stream.read(2))[0]
        # Read message count
        message_count = struct.unpack('>H', stream.read(2))[0]
        # Decode messages...
        
class AMFEncoder:
    """Encodes Python to AMF3 binary"""
    
    def encode(self, messages: List[Dict], version: int = 0) -> bytes:
        stream = io.BytesIO()
        # Write version
        stream.write(struct.pack('>H', version))
        # Write headers (0)
        stream.write(struct.pack('>H', 0))
        # Write message count
        stream.write(struct.pack('>H', len(messages)))
        # Encode messages...
```

---

## ⚡ Race Condition Exploits

### Mechanism
```
# From EXPLOITS.md, exploits.py

Normal flow:
1. Client sends "use item" request
2. Server validates item count
3. Server decrements item
4. Server applies effect

Exploit flow (multiple connections):
1. Client A sends "use item" request
2. Client B sends "use item" request (before A completes)
3. Both validated BEFORE either decremented
4. Item used twice, only decremented once!
```

### Implementation
```python
# From EXPLOITS.md
import threading

def send_use_item():
    client.send_command(
        "shop.useItem",
        {
            "castleId": YOUR_CASTLE,
            "itemId": 'player.item.speed.1hr',
            "num": 1
        }
    )

# Create 10 simultaneous threads
threads = [threading.Thread(target=send_use_item) for _ in range(10)]

# Start all simultaneously
for t in threads:
    t.start()

# Wait for all to complete
for t in threads:
    t.join()
```

### Race Condition Flow Diagram
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      RACE CONDITION EXPLOIT                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   Client A                    Server                    Client B            │
│   ─────────                   ──────                    ─────────           │
│       │                          │                          │               │
│       │──── use item ───────────▶│                          │               │
│       │                          │◀──── use item ───────────│               │
│       │                          │                          │               │
│       │            ┌─────────────┴─────────────┐            │               │
│       │            │ Both requests in flight   │            │               │
│       │            │ Server validates both     │            │               │
│       │            │ BEFORE decrementing       │            │               │
│       │            └─────────────┬─────────────┘            │               │
│       │                          │                          │               │
│       │◀──── success ────────────│                          │               │
│       │                          │──── success ─────────────▶               │
│       │                          │                          │               │
│       │            Result: Item used 2x, decremented 1x     │               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🛡️ Detection & Mitigation

### Server May Detect
```python
# From EXPLOITS.md
DETECTION_PATTERNS = [
    "Unusual packet patterns",
    "Too-fast request rates",
    "Known exploit signatures",
    "Multiple simultaneous connections",
    "Overflow values in parameters",
]
```

### Evasion Techniques
```python
# Use proxies for multiple connections
PROXIES = [
    "socks5://proxy1:1080",
    "socks5://proxy2:1080",
]

# Rate limiting
import time
MIN_DELAY = 0.5  # seconds between requests

# Randomize timing
import random
delay = MIN_DELAY + random.uniform(0, 0.5)
time.sleep(delay)

# Rotate signatures
def randomize_request(params):
    params['_nonce'] = random.randint(0, 999999)
    return params
```

---

## 📡 Complete Protocol Implementation

```python
import socket
import struct
import hashlib
import io
from typing import Dict, Any, Optional

class EvonyProtocol:
    """Complete Evony network protocol implementation"""
    
    ACTION_KEY = "TAO_{313-894*&*($*#-FDIU(430}-{facebook_dioe(&*%$l}"
    
    def __init__(self, server: str = 'cc2'):
        self.host = f"{server}.evony.com"
        self.port = 443
        self.sock: Optional[socket.socket] = None
        self.session_key: Optional[str] = None
        
    def connect(self):
        """Establish connection"""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(30)
        self.sock.connect((self.host, self.port))
        # Send identification
        self.sock.send(b"gameClient\x00")
        
    def login(self, email: str, password: str) -> Dict:
        """Authenticate and get session"""
        # Hash password
        pass_hash = hashlib.md5(password.encode()).hexdigest()
        login_hash = hashlib.md5(
            (email + pass_hash + "evony").encode()
        ).hexdigest()
        
        # Send login
        response = self.send_command("login", {
            "email": email,
            "passwordHash": login_hash,
        })
        
        if response.get("msg") == "login success":
            self.session_key = response.get("sessionKey")
            
        return response
        
    def send_command(self, cmd: str, params: Dict) -> Dict:
        """Send AMF command with signature"""
        # Generate signature
        sig_data = cmd + str(sorted(params.items()))
        signature = hashlib.md5(
            (sig_data + self.ACTION_KEY).encode()
        ).hexdigest()
        
        # Build message
        message = {
            "cmd": cmd,
            "params": params,
            "sig": signature,
        }
        if self.session_key:
            message["sessionKey"] = self.session_key
            
        # Encode AMF
        encoded = self._encode_amf(message)
        
        # Send with length prefix
        packet = struct.pack('>L', len(encoded)) + encoded
        self.sock.sendall(packet)
        
        # Receive response
        return self._receive()
        
    def _receive(self) -> Dict:
        """Receive and decode AMF response"""
        # Read length (4 bytes, big-endian)
        length_data = self._recv_exact(4)
        length = struct.unpack('>L', length_data)[0]
        
        # Read body
        body = self._recv_exact(length)
        
        # Decode AMF
        return self._decode_amf(body)
        
    def _recv_exact(self, n: int) -> bytes:
        """Receive exactly n bytes"""
        data = b''
        while len(data) < n:
            chunk = self.sock.recv(n - len(data))
            if not chunk:
                raise ConnectionError("Connection closed")
            data += chunk
        return data
        
    def _encode_amf(self, obj: Any) -> bytes:
        """Encode object to AMF3"""
        # Use pyamf or custom encoder
        from pyamf import amf3
        encoder = amf3.Encoder()
        encoder.writeElement(obj)
        return encoder.stream.getvalue()
        
    def _decode_amf(self, data: bytes) -> Any:
        """Decode AMF3 to object"""
        from pyamf import amf3
        decoder = amf3.Decoder(data)
        return decoder.readElement()
        
    # Convenience methods
    def train_troops(self, city_id: int, troop_type: int, count: int):
        return self.send_command("troop.produceTroop", {
            "cityId": city_id,
            "troopType": troop_type,
            "num": count
        })
        
    def overflow_exploit(self, city_id: int, troop_type: int = 6):
        """Execute integer overflow exploit"""
        thresholds = {6: 6135037, 7: 2684355, 8: 1431656}
        threshold = thresholds.get(troop_type, 6135037)
        
        # Train at overflow threshold
        self.train_troops(city_id, troop_type, threshold)
        
        # Wait briefly
        import time
        time.sleep(2)
        
        # Cancel for "refund"
        return self.send_command("troop.cancelTroopProduce", {
            "cityId": city_id,
            "troopType": troop_type
        })
        
    def race_condition_exploit(self, city_id: int, item_id: str, 
                                num_threads: int = 10):
        """Execute race condition exploit"""
        import threading
        
        results = []
        
        def use_item():
            try:
                result = self.send_command("shop.useItem", {
                    "castleId": city_id,
                    "itemId": item_id,
                    "num": 1
                })
                results.append(result)
            except Exception as e:
                results.append({"error": str(e)})
                
        # Create threads
        threads = [threading.Thread(target=use_item) 
                   for _ in range(num_threads)]
                   
        # Start all simultaneously
        for t in threads:
            t.start()
            
        # Wait for completion
        for t in threads:
            t.join()
            
        return results
```

---

## 📊 Response Data Structures

### Login Success Response
```json
{
    "msg": "login success",
    "sessionKey": "abc123...",
    "player": {
        "castles": [
            {
                "status": 0,
                "buildings": [
                    {"positionId": 1040, "typeId": 6, "level": 10, ...}
                ],
                "troops": {...},
                "resources": {...}
            }
        ],
        "heroes": [...],
        "items": [...],
        "alliance": {...}
    }
}
```

### Command Response
```json
{
    "ok": 1,
    "data": {...},
    "errorCode": 0,
    "errorMsg": ""
}
```

---

*Extracted from RAG: 166,043 chunks, network protocol documentation*
