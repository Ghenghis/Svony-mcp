"""
AutoEvony Bot GUI v4 - Purple/Cyberpunk Theme
Neon purple aesthetic for bot operations
"""

import tkinter as tk
from dataclasses import dataclass
from datetime import datetime
from typing import List

@dataclass
class CityData:
    id: int; name: str; x: int; y: int; population: int = 0; gold: int = 0; food: int = 0

@dataclass
class TroopData:
    worker: int = 0; warrior: int = 0; scout: int = 0; pikeman: int = 0
    swordsman: int = 0; archer: int = 0; cavalry: int = 0; cataphract: int = 0
    transporter: int = 0; ballista: int = 0; ram: int = 0; catapult: int = 0

class PurpleTheme:
    BG_DARK = "#0d0014"
    BG_MED = "#1a0a2e"
    BG_LIGHT = "#2d1b4e"
    BG_PANEL = "#1f0f35"
    
    TEXT_PRIMARY = "#e0d0ff"
    TEXT_PURPLE = "#cc66ff"
    TEXT_PINK = "#ff66cc"
    TEXT_CYAN = "#66ffff"
    TEXT_GREEN = "#66ff99"
    TEXT_DIM = "#8866aa"
    
    ACCENT = "#9933ff"
    BORDER = "#4422aa"
    BUTTON = "#3311aa"
    BUTTON_ACTIVE = "#5522cc"
    
    FONT = ("Segoe UI", 10)
    FONT_BOLD = ("Segoe UI", 10, "bold")
    FONT_TITLE = ("Segoe UI", 14, "bold")
    FONT_MONO = ("Consolas", 10)

class PurpleHeader(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=PurpleTheme.BG_DARK, **kwargs)
        
        # Left
        left = tk.Frame(self, bg=PurpleTheme.BG_DARK)
        left.pack(side=tk.LEFT, padx=10, pady=8)
        tk.Label(left, text="◈ AUTOEVONY", bg=PurpleTheme.BG_DARK,
                fg=PurpleTheme.TEXT_PURPLE, font=PurpleTheme.FONT_TITLE).pack(side=tk.LEFT)
        self._status = tk.Label(left, text="● ONLINE", bg=PurpleTheme.BG_DARK,
                               fg=PurpleTheme.TEXT_GREEN, font=PurpleTheme.FONT)
        self._status.pack(side=tk.LEFT, padx=20)
        
        # Resources
        center = tk.Frame(self, bg=PurpleTheme.BG_DARK)
        center.pack(side=tk.LEFT, expand=True)
        
        self._res = {}
        for name, color in [("Gold", PurpleTheme.TEXT_PINK), ("Food", PurpleTheme.TEXT_GREEN),
                            ("Honor", PurpleTheme.TEXT_CYAN)]:
            f = tk.Frame(center, bg=PurpleTheme.BG_DARK)
            f.pack(side=tk.LEFT, padx=15)
            tk.Label(f, text=name, bg=PurpleTheme.BG_DARK, fg=PurpleTheme.TEXT_DIM,
                    font=PurpleTheme.FONT).pack()
            lbl = tk.Label(f, text="0", bg=PurpleTheme.BG_DARK, fg=color, font=PurpleTheme.FONT_BOLD)
            lbl.pack()
            self._res[name] = lbl
            
        # Time
        self._time = tk.Label(self, text="00:00:00", bg=PurpleTheme.BG_DARK,
                             fg=PurpleTheme.TEXT_PURPLE, font=PurpleTheme.FONT_BOLD)
        self._time.pack(side=tk.RIGHT, padx=20)
        self._tick()
        
    def _tick(self):
        self._time.config(text=datetime.now().strftime("%H:%M:%S"))
        self.after(1000, self._tick)

class PurpleCities(tk.Frame):
    def __init__(self, parent, on_change=None, **kwargs):
        super().__init__(parent, bg=PurpleTheme.BG_MED, **kwargs)
        self._cities = []
        self._sel = None
        self._cb = on_change
        self._btns = {}
        
    def set_cities(self, cities):
        self._cities = cities
        for b in self._btns.values(): b.destroy()
        self._btns.clear()
        for c in cities:
            b = tk.Button(self, text=f"◇ {c.name}", bg=PurpleTheme.BUTTON,
                         fg=PurpleTheme.TEXT_PRIMARY, font=PurpleTheme.FONT,
                         relief=tk.FLAT, padx=10, pady=4,
                         command=lambda x=c: self._select(x.id))
            b.pack(side=tk.LEFT, padx=3, pady=5)
            self._btns[c.id] = b
        if cities: self._select(cities[0].id)
        
    def _select(self, cid):
        self._sel = cid
        for i, b in self._btns.items():
            b.config(bg=PurpleTheme.ACCENT if i == cid else PurpleTheme.BUTTON)
        if self._cb: self._cb(cid)

class PurpleScript(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=PurpleTheme.BG_PANEL, **kwargs)
        
        # Header
        h = tk.Frame(self, bg=PurpleTheme.BG_LIGHT)
        h.pack(fill=tk.X)
        tk.Label(h, text="◈ Script Engine", bg=PurpleTheme.BG_LIGHT,
                fg=PurpleTheme.TEXT_PURPLE, font=PurpleTheme.FONT_BOLD).pack(side=tk.LEFT, padx=10, pady=5)
        
        for txt, clr in [("▶ RUN", PurpleTheme.TEXT_GREEN), ("■ STOP", PurpleTheme.TEXT_PINK)]:
            tk.Button(h, text=txt, bg=PurpleTheme.BUTTON, fg=clr, font=PurpleTheme.FONT,
                     relief=tk.FLAT).pack(side=tk.RIGHT, padx=3, pady=3)
        
        # Editor
        self._txt = tk.Text(self, bg=PurpleTheme.BG_DARK, fg=PurpleTheme.TEXT_PRIMARY,
                           font=PurpleTheme.FONT_MONO, insertbackground=PurpleTheme.TEXT_PURPLE)
        self._txt.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self._txt.insert('1.0', '''# Purple AutoEvony Script
# Exploit mode enabled

loop city $allcities
    echo "Processing: $city"
    train archer 2147483647
    wait 5
    cancel archer
endloop

echo "Complete"
''')

class PurpleTroops(tk.Frame):
    TROOPS = ["Worker", "Warrior", "Scout", "Pikeman", "Swordsman", "Archer",
              "Cavalry", "Cataphract", "Transporter", "Ballista", "Ram", "Catapult"]
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=PurpleTheme.BG_PANEL, **kwargs)
        self._labels = {}
        
        tk.Label(self, text="◈ Troop Overview", bg=PurpleTheme.BG_PANEL,
                fg=PurpleTheme.TEXT_PURPLE, font=PurpleTheme.FONT_BOLD).pack(anchor=tk.W, padx=10, pady=8)
        
        grid = tk.Frame(self, bg=PurpleTheme.BG_PANEL)
        grid.pack(fill=tk.X, padx=10, pady=5)
        
        for i, troop in enumerate(self.TROOPS):
            row, col = i // 4, i % 4
            cell = tk.Frame(grid, bg=PurpleTheme.BG_LIGHT, padx=8, pady=6)
            cell.grid(row=row, column=col, padx=3, pady=3, sticky="nsew")
            
            tk.Label(cell, text=troop, bg=PurpleTheme.BG_LIGHT, fg=PurpleTheme.TEXT_DIM,
                    font=PurpleTheme.FONT).pack(anchor=tk.W)
            lbl = tk.Label(cell, text="0", bg=PurpleTheme.BG_LIGHT, fg=PurpleTheme.TEXT_PRIMARY,
                          font=PurpleTheme.FONT_BOLD)
            lbl.pack(anchor=tk.W)
            self._labels[troop.lower()] = lbl
            grid.columnconfigure(col, weight=1)
            
    def update(self, troops):
        for name in [t.lower() for t in self.TROOPS]:
            if name in self._labels:
                val = getattr(troops, name, 0)
                color = PurpleTheme.TEXT_PINK if val > 2000000000 else PurpleTheme.TEXT_PRIMARY
                self._labels[name].config(text=f"{val:,}", fg=color)

class PurpleLog(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=PurpleTheme.BG_PANEL, **kwargs)
        
        tk.Label(self, text="◈ Activity Log", bg=PurpleTheme.BG_PANEL,
                fg=PurpleTheme.TEXT_PURPLE, font=PurpleTheme.FONT_BOLD).pack(anchor=tk.W, padx=10, pady=5)
        
        self._log = tk.Text(self, bg=PurpleTheme.BG_DARK, fg=PurpleTheme.TEXT_PRIMARY,
                           font=PurpleTheme.FONT_MONO, height=6, state=tk.DISABLED)
        self._log.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
    def log(self, msg, color=None):
        self._log.config(state=tk.NORMAL)
        self._log.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] {msg}\n")
        self._log.see(tk.END)
        self._log.config(state=tk.DISABLED)

class AutoEvonyPurple(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AutoEvony - Purple Cyberpunk v4")
        self.geometry("1400x900")
        self.configure(bg=PurpleTheme.BG_DARK)
        
        self._cities = [
            CityData(1, "Neon", 0, 0, 500000, 44841205, 55050),
            CityData(2, "Chrome", 100, 100, 300000, 20000000, 30000),
            CityData(3, "Cyber", 200, 50, 250000, 15000000, 25000),
        ]
        self._troops = TroopData(worker=1000000, warrior=500000, archer=2147483647)
        
        self._create_ui()
        self._load_data()
        
    def _create_ui(self):
        self._header = PurpleHeader(self)
        self._header.pack(fill=tk.X)
        
        self._cities_bar = PurpleCities(self, on_change=self._on_city)
        self._cities_bar.pack(fill=tk.X, padx=5)
        
        main = tk.Frame(self, bg=PurpleTheme.BG_DARK)
        main.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        left = tk.Frame(main, bg=PurpleTheme.BG_PANEL, width=380)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5))
        left.pack_propagate(False)
        self._script = PurpleScript(left)
        self._script.pack(fill=tk.BOTH, expand=True)
        
        center = tk.Frame(main, bg=PurpleTheme.BG_DARK)
        center.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self._troops_panel = PurpleTroops(center)
        self._troops_panel.pack(fill=tk.X, pady=(0, 5))
        self._log = PurpleLog(center)
        self._log.pack(fill=tk.BOTH, expand=True)
        
        status = tk.Frame(self, bg=PurpleTheme.BG_MED)
        status.pack(fill=tk.X, side=tk.BOTTOM)
        tk.Label(status, text="◈ Purple Cyberpunk Theme v4", bg=PurpleTheme.BG_MED,
                fg=PurpleTheme.TEXT_DIM, font=PurpleTheme.FONT).pack(side=tk.RIGHT, padx=10, pady=3)
        
    def _load_data(self):
        self._cities_bar.set_cities(self._cities)
        self._troops_panel.update(self._troops)
        self._log.log("AutoEvony Purple v4 initialized")
        self._log.log("Exploit engine ready")
        
    def _on_city(self, cid):
        self._log.log(f"Selected city: {cid}")

def main():
    app = AutoEvonyPurple()
    app.mainloop()

if __name__ == "__main__":
    main()
