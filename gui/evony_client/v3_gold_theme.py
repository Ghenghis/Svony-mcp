"""
Evony Client GUI v3 - Gold/Yellow Theme Variant
Alternative color scheme matching RoboEvony gold theme
"""

import tkinter as tk
from tkinter import ttk
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass
from datetime import datetime

# Import base components from v1
from v1_complete import (
    CityData, TroopData, HeroData, BuildingData,
    ResourceBar, CityTabs, TroopTable, BuildingPanel, 
    HeroPanel, MapView, ChatPanel
)

# =============================================================================
# GOLD THEME CONFIGURATION
# =============================================================================

class GoldTheme:
    """Evony Gold/Yellow Theme"""
    BG_DARK = "#1a1a0a"
    BG_MEDIUM = "#2a2810"
    BG_LIGHT = "#3a3818"
    BG_PANEL = "#252512"
    
    TEXT_PRIMARY = "#f0e8d0"
    TEXT_SECONDARY = "#a09878"
    TEXT_GOLD = "#ffd700"
    TEXT_GREEN = "#88cc44"
    TEXT_RED = "#dd4444"
    TEXT_BLUE = "#44aaff"
    
    ACCENT_GOLD = "#d4a520"
    ACCENT_BRONZE = "#cd7f32"
    ACCENT_GREEN = "#558822"
    
    BORDER_COLOR = "#4a4828"
    BUTTON_BG = "#3a3510"
    BUTTON_HOVER = "#4a4520"
    BUTTON_ACTIVE = "#5a5530"
    
    FONT_TITLE = ("Arial", 14, "bold")
    FONT_HEADER = ("Arial", 11, "bold")
    FONT_NORMAL = ("Arial", 10)
    FONT_SMALL = ("Arial", 9)

# =============================================================================
# THEMED COMPONENTS
# =============================================================================

class GoldResourceBar(tk.Frame):
    """Gold themed resource bar"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=GoldTheme.BG_DARK, **kwargs)
        self._create_widgets()
        
    def _create_widgets(self):
        resources = [
            ("Gold:", "0", GoldTheme.TEXT_GOLD),
            ("Food:", "0", GoldTheme.TEXT_GREEN),
            ("Lumber:", "0", GoldTheme.ACCENT_BRONZE),
            ("Stone:", "0", GoldTheme.TEXT_PRIMARY),
            ("Iron:", "0", GoldTheme.TEXT_SECONDARY),
        ]
        
        self._labels = {}
        for label, value, color in resources:
            frame = tk.Frame(self, bg=GoldTheme.BG_DARK)
            frame.pack(side=tk.LEFT, padx=10)
            
            tk.Label(frame, text=label, bg=GoldTheme.BG_DARK,
                    fg=GoldTheme.TEXT_SECONDARY, font=GoldTheme.FONT_SMALL).pack(side=tk.LEFT)
            val_lbl = tk.Label(frame, text=value, bg=GoldTheme.BG_DARK,
                              fg=color, font=GoldTheme.FONT_NORMAL)
            val_lbl.pack(side=tk.LEFT, padx=2)
            self._labels[label] = val_lbl
            
        # Time
        self._time_label = tk.Label(self, text="00:00:00", bg=GoldTheme.BG_DARK,
                                    fg=GoldTheme.TEXT_GOLD, font=GoldTheme.FONT_HEADER)
        self._time_label.pack(side=tk.RIGHT, padx=20)
        self._update_time()
        
    def _update_time(self):
        self._time_label.config(text=datetime.now().strftime("%H:%M:%S"))
        self.after(1000, self._update_time)
        
    def update_resources(self, gold, food, lumber, stone, iron, pop, max_pop):
        self._labels["Gold:"].config(text=f"{gold:,}")
        self._labels["Food:"].config(text=f"{food:,}")
        self._labels["Lumber:"].config(text=f"{lumber:,}")
        self._labels["Stone:"].config(text=f"{stone:,}")
        self._labels["Iron:"].config(text=f"{iron:,}")


class GoldCityTabs(tk.Frame):
    """Gold themed city tabs"""
    
    def __init__(self, parent, on_city_change=None, **kwargs):
        super().__init__(parent, bg=GoldTheme.BG_MEDIUM, **kwargs)
        self._cities = []
        self._selected = None
        self._on_change = on_city_change
        self._buttons = {}
        
    def set_cities(self, cities):
        self._cities = cities
        for btn in self._buttons.values():
            btn.destroy()
        self._buttons.clear()
        
        for city in cities:
            btn = tk.Button(self, text=f"{city.name}({city.x},{city.y})",
                           bg=GoldTheme.BUTTON_BG, fg=GoldTheme.TEXT_PRIMARY,
                           activebackground=GoldTheme.BUTTON_ACTIVE,
                           font=GoldTheme.FONT_SMALL, relief=tk.FLAT,
                           command=lambda c=city: self._select(c.id))
            btn.pack(side=tk.LEFT, padx=2, pady=4)
            self._buttons[city.id] = btn
            
        if cities:
            self._select(cities[0].id)
            
    def _select(self, city_id):
        self._selected = city_id
        for cid, btn in self._buttons.items():
            btn.config(bg=GoldTheme.ACCENT_GOLD if cid == city_id else GoldTheme.BUTTON_BG)
        if self._on_change:
            self._on_change(city_id)


class GoldTroopTable(tk.Frame):
    """Gold themed troop table"""
    
    TROOP_TYPES = ["Worker", "Warrior", "Scout", "Pikeman", "Swordsman", "Archer",
                   "Cavalry", "Cataphract", "Transporter", "Ballista", "Ram", "Catapult"]
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=GoldTheme.BG_PANEL, **kwargs)
        self._create_widgets()
        
    def _create_widgets(self):
        # Header
        header = tk.Frame(self, bg=GoldTheme.BG_LIGHT)
        header.pack(fill=tk.X)
        
        for col in ["Type", "Available", "Total", "Training"]:
            tk.Label(header, text=col, bg=GoldTheme.BG_LIGHT, fg=GoldTheme.TEXT_GOLD,
                    font=GoldTheme.FONT_HEADER, width=12).pack(side=tk.LEFT, padx=2)
                    
        self._rows = {}
        rows_frame = tk.Frame(self, bg=GoldTheme.BG_PANEL)
        rows_frame.pack(fill=tk.BOTH, expand=True)
        
        for i, troop in enumerate(self.TROOP_TYPES):
            bg = GoldTheme.BG_PANEL if i % 2 == 0 else GoldTheme.BG_MEDIUM
            row = tk.Frame(rows_frame, bg=bg)
            row.pack(fill=tk.X)
            
            labels = []
            tk.Label(row, text=troop, bg=bg, fg=GoldTheme.TEXT_PRIMARY,
                    font=GoldTheme.FONT_NORMAL, width=12, anchor=tk.W).pack(side=tk.LEFT, padx=2)
            
            for _ in range(3):
                lbl = tk.Label(row, text="0", bg=bg, fg=GoldTheme.TEXT_PRIMARY,
                              font=GoldTheme.FONT_NORMAL, width=12, anchor=tk.E)
                lbl.pack(side=tk.LEFT, padx=2)
                labels.append(lbl)
            self._rows[troop.lower()] = labels
            
    def update_troops(self, troops):
        data = {"worker": troops.worker, "warrior": troops.warrior, "scout": troops.scout,
                "pikeman": troops.pikeman, "swordsman": troops.swordsman, "archer": troops.archer,
                "cavalry": troops.cavalry, "cataphract": troops.cataphract,
                "transporter": troops.transporter, "ballista": troops.ballista,
                "ram": troops.ram, "catapult": troops.catapult}
        for name, count in data.items():
            if name in self._rows:
                self._rows[name][0].config(text=f"{count:,}")
                self._rows[name][1].config(text=f"{count:,}")


# =============================================================================
# MAIN GOLD THEME CLIENT
# =============================================================================

class EvonyClientGold(tk.Tk):
    """Evony Client with Gold Theme"""
    
    def __init__(self):
        super().__init__()
        self.title("Evony Age II - Gold Theme v3")
        self.geometry("1400x900")
        self.configure(bg=GoldTheme.BG_DARK)
        
        self._cities = [
            CityData(1, "Atlantis", 0, 0, 500000, 100, 44841205, 55050, 100000, 80000, 60000),
            CityData(2, "Babylon", 100, 100, 300000, 95, 20000000, 30000, 50000, 40000, 30000),
        ]
        self._troops = TroopData(worker=1000000, warrior=500000, archer=1786706432)
        
        self._create_ui()
        self._load_data()
        
    def _create_ui(self):
        # Resource bar
        self._resource_bar = GoldResourceBar(self)
        self._resource_bar.pack(fill=tk.X, padx=5, pady=5)
        
        # City tabs
        self._city_tabs = GoldCityTabs(self, on_city_change=self._on_city_change)
        self._city_tabs.pack(fill=tk.X, padx=5)
        
        # Main content
        main = tk.Frame(self, bg=GoldTheme.BG_DARK)
        main.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Troop table
        self._troop_table = GoldTroopTable(main)
        self._troop_table.pack(fill=tk.X, pady=5)
        
        # Map placeholder
        map_frame = tk.Frame(main, bg=GoldTheme.BG_PANEL)
        map_frame.pack(fill=tk.BOTH, expand=True)
        tk.Label(map_frame, text="Map View", bg=GoldTheme.BG_PANEL,
                fg=GoldTheme.TEXT_GOLD, font=GoldTheme.FONT_TITLE).pack(pady=20)
                
        # Status bar
        status = tk.Frame(self, bg=GoldTheme.BG_MEDIUM)
        status.pack(fill=tk.X, side=tk.BOTTOM)
        tk.Label(status, text="Gold Theme v3", bg=GoldTheme.BG_MEDIUM,
                fg=GoldTheme.TEXT_GOLD, font=GoldTheme.FONT_SMALL).pack(side=tk.RIGHT, padx=10)
                
    def _load_data(self):
        self._city_tabs.set_cities(self._cities)
        self._troop_table.update_troops(self._troops)
        if self._cities:
            c = self._cities[0]
            self._resource_bar.update_resources(c.gold, c.food, c.lumber, c.stone, c.iron, c.population, c.population+100000)
            
    def _on_city_change(self, city_id):
        for c in self._cities:
            if c.id == city_id:
                self._resource_bar.update_resources(c.gold, c.food, c.lumber, c.stone, c.iron, c.population, c.population+100000)
                break


def main():
    app = EvonyClientGold()
    app.mainloop()

if __name__ == "__main__":
    main()
