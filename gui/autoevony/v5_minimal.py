"""
AutoEvony Bot GUI v5 - Minimal/Clean Theme
Simple, lightweight design for efficiency
"""

import tkinter as tk
from tkinter import ttk
from dataclasses import dataclass
from datetime import datetime
from typing import List

@dataclass
class CityData:
    id: int; name: str; x: int; y: int; gold: int = 0; food: int = 0

@dataclass
class TroopData:
    worker: int = 0; warrior: int = 0; scout: int = 0; pikeman: int = 0
    swordsman: int = 0; archer: int = 0; cavalry: int = 0; cataphract: int = 0
    transporter: int = 0; ballista: int = 0; ram: int = 0; catapult: int = 0

class MinimalTheme:
    BG = "#ffffff"
    BG_ALT = "#f5f5f5"
    BG_DARK = "#333333"
    TEXT = "#333333"
    TEXT_LIGHT = "#666666"
    TEXT_MUTED = "#999999"
    ACCENT = "#007bff"
    SUCCESS = "#28a745"
    WARNING = "#ffc107"
    DANGER = "#dc3545"
    BORDER = "#dee2e6"
    
    FONT = ("Segoe UI", 10)
    FONT_BOLD = ("Segoe UI", 10, "bold")
    FONT_TITLE = ("Segoe UI", 12, "bold")
    FONT_MONO = ("Consolas", 10)

class MinimalHeader(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=MinimalTheme.BG_DARK, **kwargs)
        
        tk.Label(self, text="AutoEvony", bg=MinimalTheme.BG_DARK,
                fg="#ffffff", font=MinimalTheme.FONT_TITLE).pack(side=tk.LEFT, padx=15, pady=10)
        
        self._status = tk.Label(self, text="● Connected", bg=MinimalTheme.BG_DARK,
                               fg=MinimalTheme.SUCCESS, font=MinimalTheme.FONT)
        self._status.pack(side=tk.LEFT, padx=20)
        
        self._time = tk.Label(self, text="00:00:00", bg=MinimalTheme.BG_DARK,
                             fg="#ffffff", font=MinimalTheme.FONT)
        self._time.pack(side=tk.RIGHT, padx=15)
        self._tick()
        
    def _tick(self):
        self._time.config(text=datetime.now().strftime("%H:%M:%S"))
        self.after(1000, self._tick)

class MinimalCities(tk.Frame):
    def __init__(self, parent, on_change=None, **kwargs):
        super().__init__(parent, bg=MinimalTheme.BG, **kwargs)
        self._cities = []
        self._sel = None
        self._cb = on_change
        self._btns = {}
        
        # Border
        tk.Frame(self, bg=MinimalTheme.BORDER, height=1).pack(fill=tk.X, side=tk.BOTTOM)
        
    def set_cities(self, cities):
        self._cities = cities
        for b in self._btns.values(): b.destroy()
        self._btns.clear()
        
        for c in cities:
            b = tk.Button(self, text=f"{c.name} ({c.x},{c.y})",
                         bg=MinimalTheme.BG, fg=MinimalTheme.TEXT,
                         font=MinimalTheme.FONT, relief=tk.FLAT, padx=15, pady=8,
                         activebackground=MinimalTheme.BG_ALT,
                         command=lambda x=c: self._select(x.id))
            b.pack(side=tk.LEFT)
            self._btns[c.id] = b
        if cities: self._select(cities[0].id)
        
    def _select(self, cid):
        self._sel = cid
        for i, b in self._btns.items():
            b.config(fg=MinimalTheme.ACCENT if i == cid else MinimalTheme.TEXT,
                    font=MinimalTheme.FONT_BOLD if i == cid else MinimalTheme.FONT)
        if self._cb: self._cb(cid)

class MinimalScript(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=MinimalTheme.BG, **kwargs)
        
        # Toolbar
        toolbar = tk.Frame(self, bg=MinimalTheme.BG_ALT)
        toolbar.pack(fill=tk.X)
        
        tk.Label(toolbar, text="Script", bg=MinimalTheme.BG_ALT,
                fg=MinimalTheme.TEXT, font=MinimalTheme.FONT_BOLD).pack(side=tk.LEFT, padx=10, pady=8)
        
        for txt, clr in [("Run", MinimalTheme.SUCCESS), ("Stop", MinimalTheme.DANGER)]:
            tk.Button(toolbar, text=txt, bg=MinimalTheme.BG, fg=clr,
                     font=MinimalTheme.FONT, relief=tk.FLAT, padx=12).pack(side=tk.RIGHT, padx=2, pady=4)
        
        # Editor
        self._txt = tk.Text(self, bg=MinimalTheme.BG, fg=MinimalTheme.TEXT,
                           font=MinimalTheme.FONT_MONO, relief=tk.FLAT,
                           highlightthickness=1, highlightcolor=MinimalTheme.BORDER,
                           highlightbackground=MinimalTheme.BORDER)
        self._txt.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self._txt.insert('1.0', '''# AutoEvony Minimal Script

loop city $cities
    echo "City: $city"
    train archer 100000
    wait 5
endloop
''')

class MinimalTroops(tk.Frame):
    TROOPS = ["Worker", "Warrior", "Scout", "Pikeman", "Swordsman", "Archer",
              "Cavalry", "Cataphract", "Transporter", "Ballista", "Ram", "Catapult"]
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=MinimalTheme.BG, **kwargs)
        self._labels = {}
        
        # Header
        header = tk.Frame(self, bg=MinimalTheme.BG_ALT)
        header.pack(fill=tk.X)
        tk.Label(header, text="Troops", bg=MinimalTheme.BG_ALT,
                fg=MinimalTheme.TEXT, font=MinimalTheme.FONT_BOLD).pack(side=tk.LEFT, padx=10, pady=8)
        
        # Grid
        grid = tk.Frame(self, bg=MinimalTheme.BG)
        grid.pack(fill=tk.X, padx=10, pady=10)
        
        for i, troop in enumerate(self.TROOPS):
            row, col = i // 4, i % 4
            cell = tk.Frame(grid, bg=MinimalTheme.BG)
            cell.grid(row=row, column=col, padx=5, pady=5, sticky="w")
            
            tk.Label(cell, text=troop, bg=MinimalTheme.BG, fg=MinimalTheme.TEXT_MUTED,
                    font=MinimalTheme.FONT).pack(anchor=tk.W)
            lbl = tk.Label(cell, text="0", bg=MinimalTheme.BG, fg=MinimalTheme.TEXT,
                          font=MinimalTheme.FONT_BOLD)
            lbl.pack(anchor=tk.W)
            self._labels[troop.lower()] = lbl
            grid.columnconfigure(col, weight=1)
            
    def update(self, troops):
        for name in [t.lower() for t in self.TROOPS]:
            if name in self._labels:
                val = getattr(troops, name, 0)
                color = MinimalTheme.DANGER if val > 2000000000 else MinimalTheme.TEXT
                self._labels[name].config(text=f"{val:,}", fg=color)

class MinimalLog(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=MinimalTheme.BG, **kwargs)
        
        header = tk.Frame(self, bg=MinimalTheme.BG_ALT)
        header.pack(fill=tk.X)
        tk.Label(header, text="Log", bg=MinimalTheme.BG_ALT,
                fg=MinimalTheme.TEXT, font=MinimalTheme.FONT_BOLD).pack(side=tk.LEFT, padx=10, pady=8)
        
        self._log = tk.Text(self, bg=MinimalTheme.BG_ALT, fg=MinimalTheme.TEXT,
                           font=MinimalTheme.FONT_MONO, height=6, relief=tk.FLAT,
                           state=tk.DISABLED)
        self._log.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
    def log(self, msg):
        self._log.config(state=tk.NORMAL)
        self._log.insert(tk.END, f"{datetime.now().strftime('%H:%M:%S')} - {msg}\n")
        self._log.see(tk.END)
        self._log.config(state=tk.DISABLED)

class AutoEvonyMinimal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AutoEvony - Minimal v5")
        self.geometry("1200x800")
        self.configure(bg=MinimalTheme.BG)
        
        self._cities = [
            CityData(1, "Alpha", 0, 0, 44841205, 55050),
            CityData(2, "Beta", 100, 100, 20000000, 30000),
            CityData(3, "Gamma", 200, 50, 15000000, 25000),
        ]
        self._troops = TroopData(worker=1000000, warrior=500000, archer=1786706432)
        
        self._create_ui()
        self._load_data()
        
    def _create_ui(self):
        self._header = MinimalHeader(self)
        self._header.pack(fill=tk.X)
        
        self._cities_bar = MinimalCities(self, on_change=self._on_city)
        self._cities_bar.pack(fill=tk.X)
        
        main = tk.Frame(self, bg=MinimalTheme.BG)
        main.pack(fill=tk.BOTH, expand=True)
        
        # Left
        left = tk.Frame(main, bg=MinimalTheme.BG, width=400)
        left.pack(side=tk.LEFT, fill=tk.Y)
        left.pack_propagate(False)
        self._script = MinimalScript(left)
        self._script.pack(fill=tk.BOTH, expand=True)
        
        # Separator
        tk.Frame(main, bg=MinimalTheme.BORDER, width=1).pack(side=tk.LEFT, fill=tk.Y)
        
        # Right
        right = tk.Frame(main, bg=MinimalTheme.BG)
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self._troops_panel = MinimalTroops(right)
        self._troops_panel.pack(fill=tk.X)
        tk.Frame(right, bg=MinimalTheme.BORDER, height=1).pack(fill=tk.X)
        self._log = MinimalLog(right)
        self._log.pack(fill=tk.BOTH, expand=True)
        
        # Footer
        footer = tk.Frame(self, bg=MinimalTheme.BG_ALT)
        footer.pack(fill=tk.X, side=tk.BOTTOM)
        tk.Label(footer, text="Minimal Theme v5", bg=MinimalTheme.BG_ALT,
                fg=MinimalTheme.TEXT_MUTED, font=MinimalTheme.FONT).pack(side=tk.RIGHT, padx=10, pady=5)
        
    def _load_data(self):
        self._cities_bar.set_cities(self._cities)
        self._troops_panel.update(self._troops)
        self._log.log("AutoEvony Minimal initialized")
        self._log.log("Ready")
        
    def _on_city(self, cid):
        self._log.log(f"Selected city {cid}")

def main():
    app = AutoEvonyMinimal()
    app.mainloop()

if __name__ == "__main__":
    main()
