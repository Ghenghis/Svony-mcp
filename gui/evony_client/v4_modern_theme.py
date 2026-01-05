"""
Evony Client GUI v4 - Modern Dark Theme
Clean, minimalist design with improved UX
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

class ModernTheme:
    BG_PRIMARY = "#121212"
    BG_SECONDARY = "#1e1e1e"
    BG_TERTIARY = "#2d2d2d"
    BG_CARD = "#252525"
    
    TEXT_PRIMARY = "#ffffff"
    TEXT_SECONDARY = "#b0b0b0"
    TEXT_ACCENT = "#64b5f6"
    TEXT_SUCCESS = "#81c784"
    TEXT_WARNING = "#ffb74d"
    TEXT_ERROR = "#e57373"
    
    ACCENT_BLUE = "#2196f3"
    ACCENT_GREEN = "#4caf50"
    ACCENT_PURPLE = "#7c4dff"
    
    BORDER = "#404040"
    BUTTON_BG = "#333333"
    BUTTON_HOVER = "#424242"
    
    FONT_TITLE = ("Segoe UI", 16, "bold")
    FONT_HEADER = ("Segoe UI", 12, "bold")
    FONT_NORMAL = ("Segoe UI", 10)
    FONT_SMALL = ("Segoe UI", 9)

class ModernResourceBar(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=ModernTheme.BG_SECONDARY, **kwargs)
        self._labels = {}
        self._create_widgets()
        
    def _create_widgets(self):
        resources = [("💰", "Gold", 0, ModernTheme.TEXT_WARNING),
                     ("🌾", "Food", 0, ModernTheme.TEXT_SUCCESS),
                     ("🪵", "Wood", 0, ModernTheme.TEXT_SECONDARY),
                     ("🪨", "Stone", 0, ModernTheme.TEXT_SECONDARY),
                     ("⚙️", "Iron", 0, ModernTheme.TEXT_SECONDARY)]
        
        for icon, name, val, color in resources:
            frame = tk.Frame(self, bg=ModernTheme.BG_SECONDARY)
            frame.pack(side=tk.LEFT, padx=15, pady=8)
            tk.Label(frame, text=f"{icon} {name}", bg=ModernTheme.BG_SECONDARY,
                    fg=ModernTheme.TEXT_SECONDARY, font=ModernTheme.FONT_SMALL).pack(anchor=tk.W)
            lbl = tk.Label(frame, text="0", bg=ModernTheme.BG_SECONDARY,
                          fg=color, font=ModernTheme.FONT_HEADER)
            lbl.pack(anchor=tk.W)
            self._labels[name] = lbl
            
        # Time on right
        time_frame = tk.Frame(self, bg=ModernTheme.BG_SECONDARY)
        time_frame.pack(side=tk.RIGHT, padx=20)
        self._time = tk.Label(time_frame, text="00:00:00", bg=ModernTheme.BG_SECONDARY,
                             fg=ModernTheme.TEXT_ACCENT, font=ModernTheme.FONT_HEADER)
        self._time.pack()
        self._update_time()
        
    def _update_time(self):
        self._time.config(text=datetime.now().strftime("%H:%M:%S"))
        self.after(1000, self._update_time)
        
    def update(self, gold, food, lumber, stone, iron):
        self._labels["Gold"].config(text=f"{gold:,}")
        self._labels["Food"].config(text=f"{food:,}")
        self._labels["Wood"].config(text=f"{lumber:,}")
        self._labels["Stone"].config(text=f"{stone:,}")
        self._labels["Iron"].config(text=f"{iron:,}")

class ModernCitySelector(tk.Frame):
    def __init__(self, parent, on_change=None, **kwargs):
        super().__init__(parent, bg=ModernTheme.BG_PRIMARY, **kwargs)
        self._cities = []
        self._selected = None
        self._on_change = on_change
        self._btns = {}
        
    def set_cities(self, cities):
        self._cities = cities
        for b in self._btns.values(): b.destroy()
        self._btns.clear()
        
        for c in cities:
            btn = tk.Button(self, text=f"📍 {c.name}", bg=ModernTheme.BUTTON_BG,
                           fg=ModernTheme.TEXT_PRIMARY, font=ModernTheme.FONT_NORMAL,
                           relief=tk.FLAT, padx=12, pady=6, cursor="hand2",
                           command=lambda x=c: self._select(x.id))
            btn.pack(side=tk.LEFT, padx=4, pady=8)
            self._btns[c.id] = btn
        if cities: self._select(cities[0].id)
        
    def _select(self, cid):
        self._selected = cid
        for i, b in self._btns.items():
            b.config(bg=ModernTheme.ACCENT_BLUE if i == cid else ModernTheme.BUTTON_BG)
        if self._on_change: self._on_change(cid)

class ModernTroopCard(tk.Frame):
    TROOPS = ["Worker", "Warrior", "Scout", "Pikeman", "Swordsman", "Archer",
              "Cavalry", "Cataphract", "Transporter", "Ballista", "Ram", "Catapult"]
    ICONS = ["👷", "⚔️", "🔍", "🗡️", "🛡️", "🏹", "🐎", "🏇", "📦", "🎯", "🔨", "💥"]
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=ModernTheme.BG_CARD, **kwargs)
        self._labels = {}
        self._create_widgets()
        
    def _create_widgets(self):
        tk.Label(self, text="🎖️ TROOPS", bg=ModernTheme.BG_CARD,
                fg=ModernTheme.TEXT_ACCENT, font=ModernTheme.FONT_HEADER).pack(anchor=tk.W, padx=15, pady=10)
        
        grid = tk.Frame(self, bg=ModernTheme.BG_CARD)
        grid.pack(fill=tk.BOTH, padx=15, pady=5)
        
        for i, (troop, icon) in enumerate(zip(self.TROOPS, self.ICONS)):
            row, col = i // 4, i % 4
            cell = tk.Frame(grid, bg=ModernTheme.BG_TERTIARY, padx=10, pady=8)
            cell.grid(row=row, column=col, padx=3, pady=3, sticky="nsew")
            
            tk.Label(cell, text=f"{icon} {troop}", bg=ModernTheme.BG_TERTIARY,
                    fg=ModernTheme.TEXT_SECONDARY, font=ModernTheme.FONT_SMALL).pack(anchor=tk.W)
            lbl = tk.Label(cell, text="0", bg=ModernTheme.BG_TERTIARY,
                          fg=ModernTheme.TEXT_PRIMARY, font=ModernTheme.FONT_NORMAL)
            lbl.pack(anchor=tk.W)
            self._labels[troop.lower()] = lbl
            grid.columnconfigure(col, weight=1)
            
    def update(self, troops):
        for name in ["worker", "warrior", "scout", "pikeman", "swordsman", "archer",
                     "cavalry", "cataphract", "transporter", "ballista", "ram", "catapult"]:
            if name in self._labels:
                self._labels[name].config(text=f"{getattr(troops, name):,}")

class ModernMapView(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=ModernTheme.BG_CARD, **kwargs)
        self._create_widgets()
        
    def _create_widgets(self):
        header = tk.Frame(self, bg=ModernTheme.BG_CARD)
        header.pack(fill=tk.X, padx=15, pady=10)
        
        tk.Label(header, text="🗺️ MAP", bg=ModernTheme.BG_CARD,
                fg=ModernTheme.TEXT_ACCENT, font=ModernTheme.FONT_HEADER).pack(side=tk.LEFT)
        
        coords = tk.Frame(header, bg=ModernTheme.BG_CARD)
        coords.pack(side=tk.RIGHT)
        tk.Label(coords, text="X:", bg=ModernTheme.BG_CARD, fg=ModernTheme.TEXT_SECONDARY).pack(side=tk.LEFT)
        tk.Entry(coords, width=5, bg=ModernTheme.BG_TERTIARY, fg=ModernTheme.TEXT_PRIMARY,
                insertbackground=ModernTheme.TEXT_PRIMARY).pack(side=tk.LEFT, padx=2)
        tk.Label(coords, text="Y:", bg=ModernTheme.BG_CARD, fg=ModernTheme.TEXT_SECONDARY).pack(side=tk.LEFT, padx=(10,0))
        tk.Entry(coords, width=5, bg=ModernTheme.BG_TERTIARY, fg=ModernTheme.TEXT_PRIMARY,
                insertbackground=ModernTheme.TEXT_PRIMARY).pack(side=tk.LEFT, padx=2)
        
        self._canvas = tk.Canvas(self, bg=ModernTheme.BG_PRIMARY, highlightthickness=0)
        self._canvas.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))

class EvonyClientModern(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Evony Age II - Modern Theme v4")
        self.geometry("1400x900")
        self.configure(bg=ModernTheme.BG_PRIMARY)
        
        self._cities = [
            CityData(1, "Atlantis", 0, 0, 500000, 100, 44841205, 55050, 100000, 80000, 60000),
            CityData(2, "Babylon", 100, 100, 300000, 95, 20000000, 30000, 50000, 40000, 30000),
        ]
        self._troops = TroopData(worker=1000000, warrior=500000, archer=1786706432,
                                 cavalry=100000, cataphract=50000)
        
        self._create_menu()
        self._create_ui()
        self._load_data()
        
    def _create_menu(self):
        menubar = tk.Menu(self, bg=ModernTheme.BG_SECONDARY, fg=ModernTheme.TEXT_PRIMARY)
        
        game = tk.Menu(menubar, tearoff=0, bg=ModernTheme.BG_TERTIARY, fg=ModernTheme.TEXT_PRIMARY)
        game.add_command(label="Connect")
        game.add_command(label="Disconnect")
        game.add_separator()
        game.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="Game", menu=game)
        
        view = tk.Menu(menubar, tearoff=0, bg=ModernTheme.BG_TERTIARY, fg=ModernTheme.TEXT_PRIMARY)
        view.add_command(label="City View")
        view.add_command(label="Map View")
        view.add_command(label="Reports")
        menubar.add_cascade(label="View", menu=view)
        
        self.config(menu=menubar)
        
    def _create_ui(self):
        self._resources = ModernResourceBar(self)
        self._resources.pack(fill=tk.X)
        
        self._city_selector = ModernCitySelector(self, on_change=self._on_city)
        self._city_selector.pack(fill=tk.X, padx=10)
        
        main = tk.Frame(self, bg=ModernTheme.BG_PRIMARY)
        main.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        left = tk.Frame(main, bg=ModernTheme.BG_PRIMARY)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        self._troops_card = ModernTroopCard(left)
        self._troops_card.pack(fill=tk.X, pady=(0, 10))
        
        self._map = ModernMapView(left)
        self._map.pack(fill=tk.BOTH, expand=True)
        
        # Status
        status = tk.Frame(self, bg=ModernTheme.BG_SECONDARY)
        status.pack(fill=tk.X, side=tk.BOTTOM)
        tk.Label(status, text="● Connected", bg=ModernTheme.BG_SECONDARY,
                fg=ModernTheme.TEXT_SUCCESS, font=ModernTheme.FONT_SMALL).pack(side=tk.LEFT, padx=10, pady=5)
        tk.Label(status, text="Modern Theme v4", bg=ModernTheme.BG_SECONDARY,
                fg=ModernTheme.TEXT_SECONDARY, font=ModernTheme.FONT_SMALL).pack(side=tk.RIGHT, padx=10)
        
    def _load_data(self):
        self._city_selector.set_cities(self._cities)
        self._troops_card.update(self._troops)
        if self._cities:
            c = self._cities[0]
            self._resources.update(c.gold, c.food, c.lumber, c.stone, c.iron)
            
    def _on_city(self, cid):
        for c in self._cities:
            if c.id == cid:
                self._resources.update(c.gold, c.food, c.lumber, c.stone, c.iron)
                break

def main():
    app = EvonyClientModern()
    app.mainloop()

if __name__ == "__main__":
    main()
