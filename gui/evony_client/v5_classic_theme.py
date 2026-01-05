"""
Evony Client GUI v5 - Classic Medieval Theme
Authentic Evony Age II medieval aesthetic
"""

import tkinter as tk
from tkinter import ttk
from dataclasses import dataclass
from datetime import datetime
from typing import List

@dataclass
class CityData:
    id: int; name: str; x: int; y: int; population: int = 0; loyalty: int = 100
    gold: int = 0; food: int = 0; lumber: int = 0; stone: int = 0; iron: int = 0

@dataclass
class TroopData:
    worker: int = 0; warrior: int = 0; scout: int = 0; pikeman: int = 0
    swordsman: int = 0; archer: int = 0; cavalry: int = 0; cataphract: int = 0
    transporter: int = 0; ballista: int = 0; ram: int = 0; catapult: int = 0

class ClassicTheme:
    # Parchment/Medieval colors
    BG_PARCHMENT = "#f4e4bc"
    BG_DARK_WOOD = "#3d2914"
    BG_LIGHT_WOOD = "#5c3d1e"
    BG_PANEL = "#e8d4a8"
    BG_HEADER = "#8b4513"
    
    TEXT_DARK = "#2a1a0a"
    TEXT_LIGHT = "#f0e6d2"
    TEXT_GOLD = "#b8860b"
    TEXT_RED = "#8b0000"
    TEXT_GREEN = "#228b22"
    TEXT_BLUE = "#191970"
    
    ACCENT_GOLD = "#daa520"
    ACCENT_BRONZE = "#cd853f"
    ACCENT_RED = "#a52a2a"
    
    BORDER = "#5c4033"
    BUTTON_BG = "#8b7355"
    BUTTON_ACTIVE = "#a08060"
    
    FONT_MEDIEVAL = ("Times New Roman", 12)
    FONT_TITLE = ("Times New Roman", 16, "bold")
    FONT_HEADER = ("Times New Roman", 12, "bold")
    FONT_SMALL = ("Times New Roman", 10)

class ClassicResourceBar(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=ClassicTheme.BG_HEADER, **kwargs)
        self._labels = {}
        self._create_widgets()
        
    def _create_widgets(self):
        # Decorative border
        border = tk.Frame(self, bg=ClassicTheme.ACCENT_GOLD, height=2)
        border.pack(fill=tk.X, side=tk.BOTTOM)
        
        resources = [("Gold", 0), ("Food", 0), ("Lumber", 0), ("Stone", 0), ("Iron", 0)]
        
        for name, val in resources:
            frame = tk.Frame(self, bg=ClassicTheme.BG_HEADER)
            frame.pack(side=tk.LEFT, padx=12, pady=6)
            
            tk.Label(frame, text=f"{name}:", bg=ClassicTheme.BG_HEADER,
                    fg=ClassicTheme.ACCENT_GOLD, font=ClassicTheme.FONT_SMALL).pack(side=tk.LEFT)
            lbl = tk.Label(frame, text="0", bg=ClassicTheme.BG_HEADER,
                          fg=ClassicTheme.TEXT_LIGHT, font=ClassicTheme.FONT_MEDIEVAL)
            lbl.pack(side=tk.LEFT, padx=3)
            self._labels[name] = lbl
            
        # Kingdom crest placeholder
        crest = tk.Label(self, text="⚔ EVONY ⚔", bg=ClassicTheme.BG_HEADER,
                        fg=ClassicTheme.ACCENT_GOLD, font=ClassicTheme.FONT_TITLE)
        crest.pack(side=tk.RIGHT, padx=20)
        
    def update(self, gold, food, lumber, stone, iron):
        self._labels["Gold"].config(text=f"{gold:,}")
        self._labels["Food"].config(text=f"{food:,}")
        self._labels["Lumber"].config(text=f"{lumber:,}")
        self._labels["Stone"].config(text=f"{stone:,}")
        self._labels["Iron"].config(text=f"{iron:,}")

class ClassicCityScroll(tk.Frame):
    def __init__(self, parent, on_change=None, **kwargs):
        super().__init__(parent, bg=ClassicTheme.BG_PANEL, **kwargs)
        self._cities = []
        self._selected = None
        self._on_change = on_change
        self._btns = {}
        
        # Scroll decoration
        tk.Label(self, text="~ Your Domains ~", bg=ClassicTheme.BG_PANEL,
                fg=ClassicTheme.TEXT_DARK, font=ClassicTheme.FONT_HEADER).pack(pady=5)
        
        self._btn_frame = tk.Frame(self, bg=ClassicTheme.BG_PANEL)
        self._btn_frame.pack(fill=tk.X, padx=10, pady=5)
        
    def set_cities(self, cities):
        self._cities = cities
        for b in self._btns.values(): b.destroy()
        self._btns.clear()
        
        for c in cities:
            btn = tk.Button(self._btn_frame, text=f"⛫ {c.name} ({c.x},{c.y})",
                           bg=ClassicTheme.BUTTON_BG, fg=ClassicTheme.TEXT_LIGHT,
                           activebackground=ClassicTheme.BUTTON_ACTIVE,
                           font=ClassicTheme.FONT_MEDIEVAL, relief=tk.RIDGE, bd=2,
                           command=lambda x=c: self._select(x.id))
            btn.pack(side=tk.LEFT, padx=3, pady=3)
            self._btns[c.id] = btn
        if cities: self._select(cities[0].id)
        
    def _select(self, cid):
        self._selected = cid
        for i, b in self._btns.items():
            b.config(bg=ClassicTheme.ACCENT_BRONZE if i == cid else ClassicTheme.BUTTON_BG)
        if self._on_change: self._on_change(cid)

class ClassicTroopScroll(tk.Frame):
    TROOPS = ["Worker", "Warrior", "Scout", "Pikeman", "Swordsman", "Archer",
              "Cavalry", "Cataphract", "Transporter", "Ballista", "Ram", "Catapult"]
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=ClassicTheme.BG_PARCHMENT, relief=tk.SUNKEN, bd=3, **kwargs)
        self._labels = {}
        self._create_widgets()
        
    def _create_widgets(self):
        # Ornate header
        header = tk.Frame(self, bg=ClassicTheme.BG_DARK_WOOD)
        header.pack(fill=tk.X)
        tk.Label(header, text="⚔ Army Roster ⚔", bg=ClassicTheme.BG_DARK_WOOD,
                fg=ClassicTheme.ACCENT_GOLD, font=ClassicTheme.FONT_TITLE).pack(pady=8)
        
        # Column headers
        cols_frame = tk.Frame(self, bg=ClassicTheme.BG_LIGHT_WOOD)
        cols_frame.pack(fill=tk.X)
        
        for col in ["Unit Type", "Available", "Total"]:
            tk.Label(cols_frame, text=col, bg=ClassicTheme.BG_LIGHT_WOOD,
                    fg=ClassicTheme.TEXT_LIGHT, font=ClassicTheme.FONT_HEADER,
                    width=15).pack(side=tk.LEFT, padx=5, pady=5)
        
        # Troop rows
        rows = tk.Frame(self, bg=ClassicTheme.BG_PARCHMENT)
        rows.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        for i, troop in enumerate(self.TROOPS):
            bg = ClassicTheme.BG_PARCHMENT if i % 2 == 0 else ClassicTheme.BG_PANEL
            row = tk.Frame(rows, bg=bg)
            row.pack(fill=tk.X, pady=1)
            
            tk.Label(row, text=f"• {troop}", bg=bg, fg=ClassicTheme.TEXT_DARK,
                    font=ClassicTheme.FONT_MEDIEVAL, width=15, anchor=tk.W).pack(side=tk.LEFT, padx=5)
            
            labels = []
            for _ in range(2):
                lbl = tk.Label(row, text="0", bg=bg, fg=ClassicTheme.TEXT_DARK,
                              font=ClassicTheme.FONT_MEDIEVAL, width=15)
                lbl.pack(side=tk.LEFT, padx=5)
                labels.append(lbl)
            self._labels[troop.lower()] = labels
            
    def update(self, troops):
        for name in ["worker", "warrior", "scout", "pikeman", "swordsman", "archer",
                     "cavalry", "cataphract", "transporter", "ballista", "ram", "catapult"]:
            if name in self._labels:
                val = f"{getattr(troops, name):,}"
                self._labels[name][0].config(text=val)
                self._labels[name][1].config(text=val)

class ClassicMapScroll(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=ClassicTheme.BG_PARCHMENT, relief=tk.SUNKEN, bd=3, **kwargs)
        self._create_widgets()
        
    def _create_widgets(self):
        header = tk.Frame(self, bg=ClassicTheme.BG_DARK_WOOD)
        header.pack(fill=tk.X)
        tk.Label(header, text="⚜ Kingdom Map ⚜", bg=ClassicTheme.BG_DARK_WOOD,
                fg=ClassicTheme.ACCENT_GOLD, font=ClassicTheme.FONT_TITLE).pack(pady=8)
        
        # Compass decoration
        compass = tk.Label(self, text="🧭 N", bg=ClassicTheme.BG_PARCHMENT,
                          fg=ClassicTheme.TEXT_DARK, font=ClassicTheme.FONT_HEADER)
        compass.pack(anchor=tk.NE, padx=10, pady=5)
        
        # Map canvas with aged look
        self._canvas = tk.Canvas(self, bg="#e8dcc0", highlightthickness=2,
                                highlightbackground=ClassicTheme.BORDER)
        self._canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

class EvonyClientClassic(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Evony Age II - Classic Medieval Theme v5")
        self.geometry("1400x900")
        self.configure(bg=ClassicTheme.BG_PARCHMENT)
        
        self._cities = [
            CityData(1, "Camelot", 0, 0, 500000, 100, 44841205, 55050, 100000, 80000, 60000),
            CityData(2, "Avalon", 100, 100, 300000, 95, 20000000, 30000, 50000, 40000, 30000),
            CityData(3, "Sherwood", 200, 50, 250000, 90, 15000000, 25000, 45000, 35000, 25000),
        ]
        self._troops = TroopData(worker=1000000, warrior=500000, archer=1786706432,
                                 cavalry=100000, cataphract=50000)
        
        self._create_menu()
        self._create_ui()
        self._load_data()
        
    def _create_menu(self):
        menubar = tk.Menu(self, bg=ClassicTheme.BG_DARK_WOOD, fg=ClassicTheme.TEXT_LIGHT)
        
        game = tk.Menu(menubar, tearoff=0, bg=ClassicTheme.BG_LIGHT_WOOD, fg=ClassicTheme.TEXT_LIGHT)
        game.add_command(label="Connect to Realm")
        game.add_command(label="Leave Realm")
        game.add_separator()
        game.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="Kingdom", menu=game)
        
        view = tk.Menu(menubar, tearoff=0, bg=ClassicTheme.BG_LIGHT_WOOD, fg=ClassicTheme.TEXT_LIGHT)
        view.add_command(label="Castle View")
        view.add_command(label="World Map")
        view.add_command(label="Battle Reports")
        menubar.add_cascade(label="View", menu=view)
        
        self.config(menu=menubar)
        
    def _create_ui(self):
        # Header
        self._resources = ClassicResourceBar(self)
        self._resources.pack(fill=tk.X)
        
        # City selector
        self._cities_bar = ClassicCityScroll(self, on_change=self._on_city)
        self._cities_bar.pack(fill=tk.X, padx=10, pady=5)
        
        # Main content
        main = tk.Frame(self, bg=ClassicTheme.BG_PARCHMENT)
        main.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left - Troops
        left = tk.Frame(main, bg=ClassicTheme.BG_PARCHMENT)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        self._troops_scroll = ClassicTroopScroll(left)
        self._troops_scroll.pack(fill=tk.X, pady=(0, 10))
        
        self._map_scroll = ClassicMapScroll(left)
        self._map_scroll.pack(fill=tk.BOTH, expand=True)
        
        # Status
        status = tk.Frame(self, bg=ClassicTheme.BG_DARK_WOOD)
        status.pack(fill=tk.X, side=tk.BOTTOM)
        tk.Label(status, text="✓ Connected to Realm", bg=ClassicTheme.BG_DARK_WOOD,
                fg=ClassicTheme.TEXT_GREEN, font=ClassicTheme.FONT_SMALL).pack(side=tk.LEFT, padx=10, pady=5)
        tk.Label(status, text="Classic Medieval Theme v5", bg=ClassicTheme.BG_DARK_WOOD,
                fg=ClassicTheme.ACCENT_GOLD, font=ClassicTheme.FONT_SMALL).pack(side=tk.RIGHT, padx=10)
        
    def _load_data(self):
        self._cities_bar.set_cities(self._cities)
        self._troops_scroll.update(self._troops)
        if self._cities:
            c = self._cities[0]
            self._resources.update(c.gold, c.food, c.lumber, c.stone, c.iron)
            
    def _on_city(self, cid):
        for c in self._cities:
            if c.id == cid:
                self._resources.update(c.gold, c.food, c.lumber, c.stone, c.iron)
                break

def main():
    app = EvonyClientClassic()
    app.mainloop()

if __name__ == "__main__":
    main()
