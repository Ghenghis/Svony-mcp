"""
AutoEvony Bot GUI v3 - Green/Matrix Theme
Hacker-style green-on-black aesthetic
"""

import tkinter as tk
from tkinter import ttk
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Callable

@dataclass
class CityData:
    id: int; name: str; x: int; y: int; population: int = 0; loyalty: int = 100
    gold: int = 0; food: int = 0; lumber: int = 0; stone: int = 0; iron: int = 0

@dataclass
class TroopData:
    worker: int = 0; warrior: int = 0; scout: int = 0; pikeman: int = 0
    swordsman: int = 0; archer: int = 0; cavalry: int = 0; cataphract: int = 0
    transporter: int = 0; ballista: int = 0; ram: int = 0; catapult: int = 0

@dataclass
class HeroData:
    id: int; name: str; level: int; politics: int; attack: int; intelligence: int
    status: str = "Idle"; energy: int = 100

class GreenTheme:
    BG_BLACK = "#0a0a0a"
    BG_DARK = "#0d1a0d"
    BG_PANEL = "#0f1f0f"
    BG_INPUT = "#050a05"
    
    TEXT_GREEN = "#00ff00"
    TEXT_DIM = "#00aa00"
    TEXT_BRIGHT = "#88ff88"
    TEXT_YELLOW = "#aaff00"
    TEXT_RED = "#ff3300"
    TEXT_CYAN = "#00ffaa"
    
    ACCENT = "#00dd00"
    BORDER = "#004400"
    BUTTON_BG = "#003300"
    BUTTON_ACTIVE = "#005500"
    
    FONT_MONO = ("Consolas", 10)
    FONT_MONO_BOLD = ("Consolas", 10, "bold")
    FONT_TITLE = ("Consolas", 14, "bold")
    FONT_SMALL = ("Consolas", 9)

class GreenHeader(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=GreenTheme.BG_BLACK, **kwargs)
        self._create_widgets()
        
    def _create_widgets(self):
        # Left - Status
        left = tk.Frame(self, bg=GreenTheme.BG_BLACK)
        left.pack(side=tk.LEFT, padx=10)
        
        self._status = tk.Label(left, text="[CONNECTED]", bg=GreenTheme.BG_BLACK,
                               fg=GreenTheme.TEXT_GREEN, font=GreenTheme.FONT_MONO_BOLD)
        self._status.pack(side=tk.LEFT)
        
        self._server = tk.Label(left, text="@cc2.evony.com:443", bg=GreenTheme.BG_BLACK,
                               fg=GreenTheme.TEXT_DIM, font=GreenTheme.FONT_MONO)
        self._server.pack(side=tk.LEFT, padx=10)
        
        # Center - Resources
        center = tk.Frame(self, bg=GreenTheme.BG_BLACK)
        center.pack(side=tk.LEFT, expand=True)
        
        self._res_labels = {}
        for name in ["GOLD", "FOOD", "POP", "HONOR"]:
            frame = tk.Frame(center, bg=GreenTheme.BG_BLACK)
            frame.pack(side=tk.LEFT, padx=15)
            tk.Label(frame, text=f"{name}:", bg=GreenTheme.BG_BLACK,
                    fg=GreenTheme.TEXT_DIM, font=GreenTheme.FONT_SMALL).pack(side=tk.LEFT)
            lbl = tk.Label(frame, text="0", bg=GreenTheme.BG_BLACK,
                          fg=GreenTheme.TEXT_GREEN, font=GreenTheme.FONT_MONO)
            lbl.pack(side=tk.LEFT, padx=2)
            self._res_labels[name] = lbl
            
        # Right - Time
        self._time = tk.Label(self, text="00:00:00", bg=GreenTheme.BG_BLACK,
                             fg=GreenTheme.TEXT_CYAN, font=GreenTheme.FONT_MONO_BOLD)
        self._time.pack(side=tk.RIGHT, padx=20)
        self._update_time()
        
    def _update_time(self):
        self._time.config(text=datetime.now().strftime("%H:%M:%S"))
        self.after(1000, self._update_time)

class GreenCityTabs(tk.Frame):
    def __init__(self, parent, on_change=None, **kwargs):
        super().__init__(parent, bg=GreenTheme.BG_DARK, **kwargs)
        self._cities = []
        self._selected = None
        self._on_change = on_change
        self._btns = {}
        
    def set_cities(self, cities):
        self._cities = cities
        for b in self._btns.values(): b.destroy()
        self._btns.clear()
        
        for c in cities:
            btn = tk.Button(self, text=f"[{c.name[:3]}:{c.x},{c.y}]",
                           bg=GreenTheme.BG_BLACK, fg=GreenTheme.TEXT_DIM,
                           activebackground=GreenTheme.BUTTON_ACTIVE,
                           activeforeground=GreenTheme.TEXT_GREEN,
                           font=GreenTheme.FONT_SMALL, relief=tk.FLAT,
                           command=lambda x=c: self._select(x.id))
            btn.pack(side=tk.LEFT, padx=2, pady=4)
            self._btns[c.id] = btn
        if cities: self._select(cities[0].id)
        
    def _select(self, cid):
        self._selected = cid
        for i, b in self._btns.items():
            b.config(fg=GreenTheme.TEXT_GREEN if i == cid else GreenTheme.TEXT_DIM,
                    bg=GreenTheme.BUTTON_BG if i == cid else GreenTheme.BG_BLACK)
        if self._on_change: self._on_change(cid)

class GreenScriptEditor(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=GreenTheme.BG_PANEL, **kwargs)
        self._create_widgets()
        
    def _create_widgets(self):
        # Header
        header = tk.Frame(self, bg=GreenTheme.BG_DARK)
        header.pack(fill=tk.X)
        
        tk.Label(header, text=">>> SCRIPT_EDITOR", bg=GreenTheme.BG_DARK,
                fg=GreenTheme.TEXT_GREEN, font=GreenTheme.FONT_MONO_BOLD).pack(side=tk.LEFT, padx=5)
        
        tk.Button(header, text="[RUN]", bg=GreenTheme.BUTTON_BG, fg=GreenTheme.TEXT_GREEN,
                 font=GreenTheme.FONT_SMALL, relief=tk.FLAT).pack(side=tk.RIGHT, padx=2)
        tk.Button(header, text="[STOP]", bg=GreenTheme.BUTTON_BG, fg=GreenTheme.TEXT_RED,
                 font=GreenTheme.FONT_SMALL, relief=tk.FLAT).pack(side=tk.RIGHT, padx=2)
        tk.Button(header, text="[LOAD]", bg=GreenTheme.BUTTON_BG, fg=GreenTheme.TEXT_DIM,
                 font=GreenTheme.FONT_SMALL, relief=tk.FLAT).pack(side=tk.RIGHT, padx=2)
        
        # Editor
        self._text = tk.Text(self, bg=GreenTheme.BG_INPUT, fg=GreenTheme.TEXT_GREEN,
                            font=GreenTheme.FONT_MONO, insertbackground=GreenTheme.TEXT_GREEN,
                            selectbackground=GreenTheme.BUTTON_BG)
        self._text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Sample script
        sample = '''# AutoEvony Exploit Script v3.0
# Target: INT32 overflow glitch
set glitch_num 2147483647

loop city $cities
    echo "[*] Processing: $city"
    
    if $food < 1000000
        echo "[!] LOW FOOD WARNING"
    endif
    
    # Trigger overflow
    train archer $glitch_num
    wait 3
    cancel archer
    
    echo "[+] Glitch complete"
endloop

echo "[*] Script finished"
'''
        self._text.insert('1.0', sample)

class GreenTroopMatrix(tk.Frame):
    TROOPS = ["worker", "warrior", "scout", "pikeman", "swordsman", "archer",
              "cavalry", "cataphract", "transporter", "ballista", "ram", "catapult"]
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=GreenTheme.BG_PANEL, **kwargs)
        self._labels = {}
        self._create_widgets()
        
    def _create_widgets(self):
        tk.Label(self, text=">>> TROOP_MATRIX", bg=GreenTheme.BG_PANEL,
                fg=GreenTheme.TEXT_GREEN, font=GreenTheme.FONT_MONO_BOLD).pack(anchor=tk.W, padx=5, pady=5)
        
        grid = tk.Frame(self, bg=GreenTheme.BG_PANEL)
        grid.pack(fill=tk.BOTH, padx=5, pady=5)
        
        # Header
        tk.Label(grid, text="TYPE", bg=GreenTheme.BG_PANEL, fg=GreenTheme.TEXT_DIM,
                font=GreenTheme.FONT_SMALL, width=12, anchor=tk.W).grid(row=0, column=0)
        tk.Label(grid, text="COUNT", bg=GreenTheme.BG_PANEL, fg=GreenTheme.TEXT_DIM,
                font=GreenTheme.FONT_SMALL, width=15, anchor=tk.E).grid(row=0, column=1)
        tk.Label(grid, text="STATUS", bg=GreenTheme.BG_PANEL, fg=GreenTheme.TEXT_DIM,
                font=GreenTheme.FONT_SMALL, width=10).grid(row=0, column=2)
        
        for i, troop in enumerate(self.TROOPS):
            tk.Label(grid, text=troop.upper(), bg=GreenTheme.BG_PANEL, fg=GreenTheme.TEXT_DIM,
                    font=GreenTheme.FONT_SMALL, width=12, anchor=tk.W).grid(row=i+1, column=0)
            
            lbl = tk.Label(grid, text="0", bg=GreenTheme.BG_PANEL, fg=GreenTheme.TEXT_GREEN,
                          font=GreenTheme.FONT_MONO, width=15, anchor=tk.E)
            lbl.grid(row=i+1, column=1)
            self._labels[troop] = lbl
            
            tk.Label(grid, text="[OK]", bg=GreenTheme.BG_PANEL, fg=GreenTheme.TEXT_GREEN,
                    font=GreenTheme.FONT_SMALL, width=10).grid(row=i+1, column=2)
            
    def update(self, troops):
        for name in self.TROOPS:
            if name in self._labels:
                val = getattr(troops, name, 0)
                # Highlight overflow values
                color = GreenTheme.TEXT_YELLOW if val > 2000000000 else GreenTheme.TEXT_GREEN
                self._labels[name].config(text=f"{val:,}", fg=color)

class GreenLogTerminal(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=GreenTheme.BG_PANEL, **kwargs)
        self._create_widgets()
        
    def _create_widgets(self):
        tk.Label(self, text=">>> LOG_OUTPUT", bg=GreenTheme.BG_PANEL,
                fg=GreenTheme.TEXT_GREEN, font=GreenTheme.FONT_MONO_BOLD).pack(anchor=tk.W, padx=5, pady=5)
        
        self._log = tk.Text(self, bg=GreenTheme.BG_INPUT, fg=GreenTheme.TEXT_GREEN,
                           font=GreenTheme.FONT_SMALL, height=8, state=tk.DISABLED)
        self._log.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self._log.tag_configure("info", foreground=GreenTheme.TEXT_GREEN)
        self._log.tag_configure("warn", foreground=GreenTheme.TEXT_YELLOW)
        self._log.tag_configure("error", foreground=GreenTheme.TEXT_RED)
        self._log.tag_configure("success", foreground=GreenTheme.TEXT_CYAN)
        
    def log(self, msg, level="info"):
        self._log.config(state=tk.NORMAL)
        ts = datetime.now().strftime("%H:%M:%S")
        prefix = {"info": "[*]", "warn": "[!]", "error": "[-]", "success": "[+]"}.get(level, "[*]")
        self._log.insert(tk.END, f"{ts} {prefix} {msg}\n", level)
        self._log.see(tk.END)
        self._log.config(state=tk.DISABLED)

class AutoEvonyGreen(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AutoEvony - Green Matrix Theme v3")
        self.geometry("1400x900")
        self.configure(bg=GreenTheme.BG_BLACK)
        
        self._cities = [
            CityData(1, "ATL", 0, 0, 500000, 100, 44841205, 55050, 100000, 80000, 60000),
            CityData(2, "BAB", 100, 100, 300000, 95, 20000000, 30000, 50000, 40000, 30000),
            CityData(3, "CTG", 200, 50, 250000, 90, 15000000, 25000, 45000, 35000, 25000),
        ]
        self._troops = TroopData(worker=1000000, warrior=500000, archer=2147483647,
                                 cavalry=100000, cataphract=50000)
        
        self._create_ui()
        self._load_data()
        
    def _create_ui(self):
        # Header
        self._header = GreenHeader(self)
        self._header.pack(fill=tk.X, padx=5, pady=5)
        
        # Cities
        self._city_tabs = GreenCityTabs(self, on_change=self._on_city)
        self._city_tabs.pack(fill=tk.X, padx=5)
        
        # Main
        main = tk.Frame(self, bg=GreenTheme.BG_BLACK)
        main.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left - Script
        left = tk.Frame(main, bg=GreenTheme.BG_PANEL, width=400)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5))
        left.pack_propagate(False)
        self._script = GreenScriptEditor(left)
        self._script.pack(fill=tk.BOTH, expand=True)
        
        # Center - Troops
        center = tk.Frame(main, bg=GreenTheme.BG_BLACK)
        center.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self._troops_matrix = GreenTroopMatrix(center)
        self._troops_matrix.pack(fill=tk.X, pady=(0, 5))
        self._log = GreenLogTerminal(center)
        self._log.pack(fill=tk.BOTH, expand=True)
        
        # Status
        status = tk.Frame(self, bg=GreenTheme.BG_DARK)
        status.pack(fill=tk.X, side=tk.BOTTOM)
        tk.Label(status, text="[READY] Green Matrix Theme v3", bg=GreenTheme.BG_DARK,
                fg=GreenTheme.TEXT_DIM, font=GreenTheme.FONT_SMALL).pack(side=tk.LEFT, padx=10, pady=3)
        
    def _load_data(self):
        self._city_tabs.set_cities(self._cities)
        self._troops_matrix.update(self._troops)
        self._log.log("AutoEvony v3.0 initialized", "success")
        self._log.log("Exploit engine loaded", "info")
        self._log.log("INT32_MAX = 2,147,483,647", "info")
        self._log.log("Ready for glitching", "success")
        
    def _on_city(self, cid):
        self._log.log(f"Switched to city ID: {cid}", "info")

def main():
    app = AutoEvonyGreen()
    app.mainloop()

if __name__ == "__main__":
    main()
