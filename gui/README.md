# 🎮 Evony GUI Recreations

Complete 1:1 GUI implementations for both Evony Client and AutoEvony Bot.
**10 total versions** - 5 for each application, including complete and skeleton versions.

---

## 📁 Folder Structure

```
gui/
├── evony_client/           # Evony Age II Client GUIs
│   ├── v1_complete.py      # Full dark theme with all components
│   ├── v2_skeleton.py      # Structure only, empty callbacks
│   ├── v3_gold_theme.py    # Gold/Yellow theme variant
│   ├── v4_modern_theme.py  # Modern dark with emoji icons
│   └── v5_classic_theme.py # Medieval parchment aesthetic
│
├── autoevony/              # AutoEvony/RoboEvony Bot GUIs
│   ├── v1_complete.py      # Full RoboEvony recreation
│   ├── v2_skeleton.py      # Structure only, for extending
│   ├── v3_green_theme.py   # Matrix/hacker green theme
│   ├── v4_purple_theme.py  # Cyberpunk purple neon
│   └── v5_minimal.py       # Clean minimal white theme
│
└── README.md               # This file
```

---

## 🖥️ Evony Client Versions

### v1_complete.py - Full Dark Theme
- **Complete** 1:1 recreation with all components
- Resource bar, city tabs, troop table, buildings, heroes, map, chat
- Dark blue theme matching original Evony
- **Use for:** Testing, reference implementation

### v2_skeleton.py - Skeleton Version
- Structure only with empty method callbacks
- All components defined but not implemented
- **Use for:** Extending with custom functionality

### v3_gold_theme.py - Gold Theme
- Alternative gold/yellow color scheme
- Matches RoboEvony gold theme variant
- **Use for:** Theme variation testing

### v4_modern_theme.py - Modern Theme
- Clean modern dark design with emoji icons
- Card-based layout with Segoe UI fonts
- **Use for:** Modern UI testing

### v5_classic_theme.py - Medieval Theme
- Authentic medieval parchment aesthetic
- Times New Roman fonts, wood textures
- **Use for:** Thematic testing

---

## 🤖 AutoEvony Bot Versions

### v1_complete.py - Full RoboEvony Recreation
- **Complete** 1:1 recreation from ROBOEVONY_FEATURE_ANALYSIS.md
- Script editor with syntax highlighting
- Troop table, hero management, army deployment
- Log panel, chat, items inventory
- **78 features** from original RoboEvony
- **Use for:** Bot testing, feature reference

### v2_skeleton.py - Skeleton Version
- Structure only with override methods
- All panels defined but empty
- **Use for:** Building custom bot implementations

### v3_green_theme.py - Matrix Theme
- Hacker-style green-on-black
- Terminal-style log output
- Overflow value highlighting
- **Use for:** Exploit development, glitch testing

### v4_purple_theme.py - Cyberpunk Theme
- Neon purple aesthetic
- Modern cyberpunk styling
- **Use for:** Alternative UI testing

### v5_minimal.py - Minimal Theme
- Clean white minimal design
- Lightweight and efficient
- **Use for:** Performance testing, simple workflows

---

## 🚀 Running the GUIs

```bash
# Run any version directly
python gui/evony_client/v1_complete.py
python gui/autoevony/v1_complete.py

# Or import and extend
from gui.evony_client.v2_skeleton import EvonyClientSkeleton

class MyClient(EvonyClientSkeleton):
    def on_connect(self):
        # Custom implementation
        pass
```

---

## 📊 Component Coverage

### Evony Client Components
| Component | v1 | v2 | v3 | v4 | v5 |
|-----------|----|----|----|----|-----|
| Resource Bar | ✅ | 📦 | ✅ | ✅ | ✅ |
| City Tabs | ✅ | 📦 | ✅ | ✅ | ✅ |
| Troop Table | ✅ | 📦 | ✅ | ✅ | ✅ |
| Building Panel | ✅ | 📦 | ❌ | ❌ | ❌ |
| Hero Panel | ✅ | 📦 | ❌ | ❌ | ❌ |
| Map View | ✅ | 📦 | ❌ | ✅ | ✅ |
| Chat Panel | ✅ | 📦 | ❌ | ❌ | ❌ |

### AutoEvony Bot Components
| Component | v1 | v2 | v3 | v4 | v5 |
|-----------|----|----|----|----|-----|
| Header Bar | ✅ | 📦 | ✅ | ✅ | ✅ |
| City Tabs | ✅ | 📦 | ✅ | ✅ | ✅ |
| Script Editor | ✅ | 📦 | ✅ | ✅ | ✅ |
| Troop Table | ✅ | 📦 | ✅ | ✅ | ✅ |
| Hero Table | ✅ | 📦 | ❌ | ❌ | ❌ |
| Log Panel | ✅ | 📦 | ✅ | ✅ | ✅ |
| Chat Panel | ✅ | 📦 | ❌ | ❌ | ❌ |
| Items Panel | ✅ | 📦 | ❌ | ❌ | ❌ |
| Army Dialog | ✅ | 📦 | ❌ | ❌ | ❌ |

**Legend:** ✅ Complete | 📦 Skeleton | ❌ Not in version

---

## 🎨 Theme Colors Reference

| Theme | Primary BG | Text | Accent |
|-------|-----------|------|--------|
| Dark Blue (v1) | #1a1a2e | #e8e8e8 | #ffd700 |
| Gold (v3) | #1a1a0a | #f0e8d0 | #d4a520 |
| Modern (v4) | #121212 | #ffffff | #2196f3 |
| Classic (v5) | #f4e4bc | #2a1a0a | #daa520 |
| Green (v3) | #0a0a0a | #00ff00 | #00dd00 |
| Purple (v4) | #0d0014 | #e0d0ff | #9933ff |
| Minimal (v5) | #ffffff | #333333 | #007bff |

---

## 📝 Mock Data Included

All versions include mock data for testing:
- **Cities:** 2-8 cities with coordinates
- **Troops:** 12 troop types with counts
- **Heroes:** 4-8 heroes with stats
- **Buildings:** 15 building types
- **Resources:** Gold, food, lumber, stone, iron

---

## 🔧 Extending the Skeleton Versions

```python
from gui.autoevony.v2_skeleton import AutoEvonySkeleton, TroopData

class MyBot(AutoEvonySkeleton):
    def on_connect(self):
        # Connect to real server
        self._connected = True
        self._log_panel.log("Connected!")
        
    def run_script(self):
        # Execute bot script
        script = self._script_editor.get_script()
        self._execute(script)
        
    def send_command(self, cmd, params):
        # Send AMF command to server
        return self._connection.send(cmd, params)

if __name__ == "__main__":
    bot = MyBot()
    bot.mainloop()
```

---

*Part of Svony MCP - Evony Reverse Engineering Project*
