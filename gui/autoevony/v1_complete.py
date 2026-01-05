"""
AutoEvony/RoboEvony Bot GUI v1 - Complete with Full Styling
1:1 Recreation of RoboEvony Bot Interface (from ROBOEVONY_FEATURE_ANALYSIS.md)
For testing and reverse engineering purposes
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass, field
from datetime import datetime
import json
import threading

# =============================================================================
# DATA MODELS
# =============================================================================

@dataclass
class AccountData:
    email: str
    server: str
    proxy: str = ""
    auto_login: bool = False

@dataclass
class CityData:
    id: int
    name: str
    x: int
    y: int
    population: int = 0
    loyalty: int = 100
    gold: int = 0
    food: int = 0
    lumber: int = 0
    stone: int = 0
    iron: int = 0

@dataclass
class TroopData:
    worker: int = 0
    warrior: int = 0
    scout: int = 0
    pikeman: int = 0
    swordsman: int = 0
    archer: int = 0
    cavalry: int = 0
    cataphract: int = 0
    transporter: int = 0
    ballista: int = 0
    ram: int = 0
    catapult: int = 0

@dataclass
class HeroData:
    id: int
    name: str
    level: int
    politics: int
    attack: int
    intelligence: int
    status: str = "Idle"
    energy: int = 100

@dataclass
class ArmyData:
    id: int
    hero: str
    target: str
    mission: str
    troops: TroopData
    remain_time: str

@dataclass
class ItemData:
    name: str
    description: str
    count: int
    price: int = 0

@dataclass 
class ValleyData:
    x: int
    y: int
    type: str
    level: int
    distance: float

# =============================================================================
# THEME CONFIGURATION - RoboEvony Dark Blue Theme
# =============================================================================

class RoboEvonyTheme:
    """RoboEvony Dark Blue Theme"""
    BG_DARK = "#0a0a1a"
    BG_MEDIUM = "#0f1428"
    BG_LIGHT = "#1a2040"
    BG_PANEL = "#12182d"
    BG_INPUT = "#0d1220"
    
    TEXT_PRIMARY = "#e0e0e0"
    TEXT_SECONDARY = "#8090a0"
    TEXT_GOLD = "#ffd700"
    TEXT_GREEN = "#00dd66"
    TEXT_RED = "#ff4444"
    TEXT_BLUE = "#4499ff"
    TEXT_YELLOW = "#ffff00"
    TEXT_CYAN = "#00ffff"
    
    ACCENT_GOLD = "#c9a227"
    ACCENT_BLUE = "#2266aa"
    ACCENT_GREEN = "#228844"
    ACCENT_RED = "#882222"
    
    BORDER_COLOR = "#2a3a5a"
    BUTTON_BG = "#1a3060"
    BUTTON_HOVER = "#2a4080"
    BUTTON_ACTIVE = "#3a50a0"
    BUTTON_RED = "#802020"
    BUTTON_GREEN = "#206020"
    
    TAB_ACTIVE = "#00aa44"
    TAB_INACTIVE = "#1a3050"
    
    FONT_TITLE = ("Arial", 14, "bold")
    FONT_HEADER = ("Arial", 11, "bold")
    FONT_NORMAL = ("Arial", 10)
    FONT_SMALL = ("Arial", 9)
    FONT_MONO = ("Consolas", 10)
    FONT_SCRIPT = ("Consolas", 9)

# =============================================================================
# HEADER BAR COMPONENT
# =============================================================================

class HeaderBar(tk.Frame):
    """Top header with alliance, server, resources, stats"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=RoboEvonyTheme.BG_DARK, **kwargs)
        self._create_widgets()
        
    def _create_widgets(self):
        # Left section - Alliance & Server
        left = tk.Frame(self, bg=RoboEvonyTheme.BG_DARK)
        left.pack(side=tk.LEFT, padx=10)
        
        self._alliance_label = tk.Label(left, text="Alliance: Borg",
                                         bg=RoboEvonyTheme.BG_DARK, fg=RoboEvonyTheme.TEXT_GOLD,
                                         font=RoboEvonyTheme.FONT_HEADER)
        self._alliance_label.pack(side=tk.LEFT, padx=(0, 20))
        
        self._server_label = tk.Label(left, text="Server: Parapet (cc2)",
                                       bg=RoboEvonyTheme.BG_DARK, fg=RoboEvonyTheme.TEXT_PRIMARY,
                                       font=RoboEvonyTheme.FONT_NORMAL)
        self._server_label.pack(side=tk.LEFT)
        
        # Center section - Resources
        center = tk.Frame(self, bg=RoboEvonyTheme.BG_DARK)
        center.pack(side=tk.LEFT, expand=True, padx=20)
        
        self._pop_label = self._create_stat("Pop:", "1,227", RoboEvonyTheme.TEXT_PRIMARY, center)
        self._gold_label = self._create_stat("Gold:", "44,841,205", RoboEvonyTheme.TEXT_GOLD, center)
        self._food_label = self._create_stat("Food:", "380", RoboEvonyTheme.TEXT_GREEN, center)
        self._honor_label = self._create_stat("Honor:", "267,009,832", RoboEvonyTheme.TEXT_BLUE, center)
        
        # Right section - Time & Controls
        right = tk.Frame(self, bg=RoboEvonyTheme.BG_DARK)
        right.pack(side=tk.RIGHT, padx=10)
        
        self._time_label = tk.Label(right, text="00:00:00",
                                     bg=RoboEvonyTheme.BG_DARK, fg=RoboEvonyTheme.TEXT_CYAN,
                                     font=RoboEvonyTheme.FONT_HEADER)
        self._time_label.pack(side=tk.LEFT, padx=10)
        
        # Control buttons
        self._pause_btn = tk.Button(right, text="⏸", bg=RoboEvonyTheme.BUTTON_BG,
                                    fg=RoboEvonyTheme.TEXT_PRIMARY, width=3,
                                    font=RoboEvonyTheme.FONT_NORMAL)
        self._pause_btn.pack(side=tk.LEFT, padx=2)
        
        self._refresh_btn = tk.Button(right, text="🔄", bg=RoboEvonyTheme.BUTTON_BG,
                                      fg=RoboEvonyTheme.TEXT_PRIMARY, width=3,
                                      font=RoboEvonyTheme.FONT_NORMAL)
        self._refresh_btn.pack(side=tk.LEFT, padx=2)
        
        self._logout_btn = tk.Button(right, text="Logout", bg=RoboEvonyTheme.BUTTON_RED,
                                     fg=RoboEvonyTheme.TEXT_PRIMARY,
                                     font=RoboEvonyTheme.FONT_SMALL)
        self._logout_btn.pack(side=tk.LEFT, padx=5)
        
        self._update_time()
        
    def _create_stat(self, label: str, value: str, color: str, parent) -> tk.Label:
        frame = tk.Frame(parent, bg=RoboEvonyTheme.BG_DARK)
        frame.pack(side=tk.LEFT, padx=8)
        
        tk.Label(frame, text=label, bg=RoboEvonyTheme.BG_DARK,
                fg=RoboEvonyTheme.TEXT_SECONDARY, font=RoboEvonyTheme.FONT_SMALL).pack(side=tk.LEFT)
        val_label = tk.Label(frame, text=value, bg=RoboEvonyTheme.BG_DARK,
                            fg=color, font=RoboEvonyTheme.FONT_NORMAL)
        val_label.pack(side=tk.LEFT, padx=(2, 0))
        return val_label
        
    def _update_time(self):
        now = datetime.now().strftime("%H:%M:%S")
        self._time_label.config(text=now)
        self.after(1000, self._update_time)

# =============================================================================
# CITY TABS COMPONENT
# =============================================================================

class CityTabBar(tk.Frame):
    """Multi-city tabs with coordinates"""
    
    def __init__(self, parent, on_city_change: Optional[Callable] = None, **kwargs):
        super().__init__(parent, bg=RoboEvonyTheme.BG_MEDIUM, **kwargs)
        self._cities: List[CityData] = []
        self._selected_city: Optional[int] = None
        self._on_city_change = on_city_change
        self._tab_buttons: Dict[int, tk.Button] = {}
        
    def set_cities(self, cities: List[CityData]):
        self._cities = cities
        self._rebuild_tabs()
        
    def _rebuild_tabs(self):
        for btn in self._tab_buttons.values():
            btn.destroy()
        self._tab_buttons.clear()
        
        for city in self._cities:
            btn = tk.Button(
                self,
                text=f"{city.name[:3]}({city.x},{city.y})",
                bg=RoboEvonyTheme.TAB_INACTIVE,
                fg=RoboEvonyTheme.TEXT_PRIMARY,
                activebackground=RoboEvonyTheme.BUTTON_ACTIVE,
                activeforeground=RoboEvonyTheme.TEXT_PRIMARY,
                relief=tk.FLAT,
                font=RoboEvonyTheme.FONT_SMALL,
                padx=6, pady=3,
                command=lambda c=city: self._select_city(c.id)
            )
            btn.pack(side=tk.LEFT, padx=1, pady=3)
            self._tab_buttons[city.id] = btn
            
        if self._cities and self._selected_city is None:
            self._select_city(self._cities[0].id)
            
    def _select_city(self, city_id: int):
        self._selected_city = city_id
        
        for cid, btn in self._tab_buttons.items():
            if cid == city_id:
                btn.config(bg=RoboEvonyTheme.TAB_ACTIVE)
            else:
                btn.config(bg=RoboEvonyTheme.TAB_INACTIVE)
                
        if self._on_city_change:
            self._on_city_change(city_id)

# =============================================================================
# SCRIPT EDITOR COMPONENT
# =============================================================================

class ScriptEditor(tk.Frame):
    """Script editor with syntax highlighting"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=RoboEvonyTheme.BG_PANEL, **kwargs)
        self._create_widgets()
        
    def _create_widgets(self):
        # Toolbar
        toolbar = tk.Frame(self, bg=RoboEvonyTheme.BG_PANEL)
        toolbar.pack(fill=tk.X, pady=2)
        
        # Tab buttons
        self._goals_btn = tk.Button(toolbar, text="Goals", bg=RoboEvonyTheme.TAB_ACTIVE,
                                    fg=RoboEvonyTheme.TEXT_PRIMARY, font=RoboEvonyTheme.FONT_SMALL)
        self._goals_btn.pack(side=tk.LEFT, padx=2)
        
        self._script_btn = tk.Button(toolbar, text="Script", bg=RoboEvonyTheme.TAB_INACTIVE,
                                     fg=RoboEvonyTheme.TEXT_PRIMARY, font=RoboEvonyTheme.FONT_SMALL)
        self._script_btn.pack(side=tk.LEFT, padx=2)
        
        # Right side buttons
        tk.Button(toolbar, text="Run", bg=RoboEvonyTheme.BUTTON_GREEN,
                 fg=RoboEvonyTheme.TEXT_PRIMARY, font=RoboEvonyTheme.FONT_SMALL,
                 command=self._run_script).pack(side=tk.RIGHT, padx=2)
        
        tk.Button(toolbar, text="Stop", bg=RoboEvonyTheme.BUTTON_RED,
                 fg=RoboEvonyTheme.TEXT_PRIMARY, font=RoboEvonyTheme.FONT_SMALL,
                 command=self._stop_script).pack(side=tk.RIGHT, padx=2)
        
        tk.Button(toolbar, text="Load", bg=RoboEvonyTheme.BUTTON_BG,
                 fg=RoboEvonyTheme.TEXT_PRIMARY, font=RoboEvonyTheme.FONT_SMALL,
                 command=self._load_script).pack(side=tk.RIGHT, padx=2)
        
        tk.Button(toolbar, text="Save", bg=RoboEvonyTheme.BUTTON_BG,
                 fg=RoboEvonyTheme.TEXT_PRIMARY, font=RoboEvonyTheme.FONT_SMALL,
                 command=self._save_script).pack(side=tk.RIGHT, padx=2)
        
        # Script text area with line numbers
        editor_frame = tk.Frame(self, bg=RoboEvonyTheme.BG_INPUT)
        editor_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Line numbers
        self._line_numbers = tk.Text(editor_frame, width=4, bg=RoboEvonyTheme.BG_DARK,
                                     fg=RoboEvonyTheme.TEXT_SECONDARY,
                                     font=RoboEvonyTheme.FONT_SCRIPT, state=tk.DISABLED,
                                     padx=5)
        self._line_numbers.pack(side=tk.LEFT, fill=tk.Y)
        
        # Script text
        self._script_text = tk.Text(editor_frame, bg=RoboEvonyTheme.BG_INPUT,
                                    fg=RoboEvonyTheme.TEXT_PRIMARY,
                                    font=RoboEvonyTheme.FONT_SCRIPT,
                                    insertbackground=RoboEvonyTheme.TEXT_PRIMARY,
                                    wrap=tk.NONE)
        self._script_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(editor_frame, command=self._script_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self._script_text.config(yscrollcommand=scrollbar.set)
        
        # Bind events for line numbers
        self._script_text.bind('<KeyRelease>', self._update_line_numbers)
        self._script_text.bind('<MouseWheel>', self._update_line_numbers)
        
        # Load sample script
        self._load_sample_script()
        
    def _load_sample_script(self):
        sample = '''setarray gltcctv ["Atlantis", "Babylon", "Carthage"]
label totalcount
set fullmsg null
# Glitch triggering number
set glitchnumber 2147483647

loop city $gltcctv
    echo "Processing city: $city"
    
    # Check food levels
    if $food < 1000000
        echo "FOOD LOW in $city"
    endif
    
    # Train troops
    train archer 100000
    wait 5
endloop

echo "Script complete"
'''
        self._script_text.insert('1.0', sample)
        self._update_line_numbers()
        
    def _update_line_numbers(self, event=None):
        lines = self._script_text.get('1.0', tk.END).count('\n')
        line_numbers = '\n'.join(str(i) for i in range(1, lines + 1))
        self._line_numbers.config(state=tk.NORMAL)
        self._line_numbers.delete('1.0', tk.END)
        self._line_numbers.insert('1.0', line_numbers)
        self._line_numbers.config(state=tk.DISABLED)
        
    def _run_script(self):
        pass  # Override
        
    def _stop_script(self):
        pass  # Override
        
    def _save_script(self):
        pass  # Override
        
    def _load_script(self):
        pass  # Override

# =============================================================================
# TROOP TABLE COMPONENT
# =============================================================================

class TroopTable(tk.Frame):
    """Full troop table with all columns from RoboEvony"""
    
    TROOP_TYPES = [
        "worker", "warrior", "scout", "pikeman", "swordsman", "archer",
        "cavalry", "cataphract", "transporter", "ballista", "ram", "catapult"
    ]
    
    COLUMNS = ["Type", "Avail", "Total", "Training", "Queue", "Goal", "Remain", "Reinf."]
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=RoboEvonyTheme.BG_PANEL, **kwargs)
        self._create_widgets()
        
    def _create_widgets(self):
        # Title
        title_frame = tk.Frame(self, bg=RoboEvonyTheme.BG_LIGHT)
        title_frame.pack(fill=tk.X)
        
        tk.Label(title_frame, text="Troops", bg=RoboEvonyTheme.BG_LIGHT,
                fg=RoboEvonyTheme.TEXT_GOLD, font=RoboEvonyTheme.FONT_HEADER).pack(side=tk.LEFT, padx=5)
        
        # Header
        header_frame = tk.Frame(self, bg=RoboEvonyTheme.BG_LIGHT)
        header_frame.pack(fill=tk.X)
        
        col_widths = [10, 12, 12, 10, 8, 8, 8, 8]
        for i, (col, width) in enumerate(zip(self.COLUMNS, col_widths)):
            lbl = tk.Label(header_frame, text=col,
                          bg=RoboEvonyTheme.BG_LIGHT, fg=RoboEvonyTheme.TEXT_GOLD,
                          font=RoboEvonyTheme.FONT_SMALL, width=width, anchor=tk.CENTER)
            lbl.grid(row=0, column=i, padx=1, pady=2)
            
        # Rows
        self._rows_frame = tk.Frame(self, bg=RoboEvonyTheme.BG_PANEL)
        self._rows_frame.pack(fill=tk.BOTH, expand=True)
        
        self._row_labels: Dict[str, List[tk.Label]] = {}
        
        for row_idx, troop_type in enumerate(self.TROOP_TYPES):
            row_bg = RoboEvonyTheme.BG_PANEL if row_idx % 2 == 0 else RoboEvonyTheme.BG_MEDIUM
            labels = []
            
            # Type name with icon representation
            type_lbl = tk.Label(self._rows_frame, text=troop_type.capitalize(),
                               bg=row_bg, fg=RoboEvonyTheme.TEXT_PRIMARY,
                               font=RoboEvonyTheme.FONT_SMALL, width=10, anchor=tk.W)
            type_lbl.grid(row=row_idx, column=0, padx=1, pady=1, sticky=tk.W)
            labels.append(type_lbl)
            
            # Value columns
            for col_idx in range(1, len(self.COLUMNS)):
                val_lbl = tk.Label(self._rows_frame, text="0",
                                  bg=row_bg, fg=RoboEvonyTheme.TEXT_PRIMARY,
                                  font=RoboEvonyTheme.FONT_SMALL,
                                  width=col_widths[col_idx], anchor=tk.E)
                val_lbl.grid(row=row_idx, column=col_idx, padx=1, pady=1)
                labels.append(val_lbl)
                
            self._row_labels[troop_type] = labels
            
    def update_troops(self, troops: TroopData):
        data = {
            "worker": troops.worker, "warrior": troops.warrior,
            "scout": troops.scout, "pikeman": troops.pikeman,
            "swordsman": troops.swordsman, "archer": troops.archer,
            "cavalry": troops.cavalry, "cataphract": troops.cataphract,
            "transporter": troops.transporter, "ballista": troops.ballista,
            "ram": troops.ram, "catapult": troops.catapult,
        }
        
        for troop_type, count in data.items():
            if troop_type in self._row_labels:
                # Update Avail and Total (cols 1 and 2)
                self._row_labels[troop_type][1].config(text=f"{count:,}")
                self._row_labels[troop_type][2].config(text=f"{count:,}")

# =============================================================================
# HERO TABLE COMPONENT
# =============================================================================

class HeroTable(tk.Frame):
    """Hero management table"""
    
    COLUMNS = ["View", "Hero", "Status", "Level", "Type", "Base", "Energy", "Recall", "Fire"]
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=RoboEvonyTheme.BG_PANEL, **kwargs)
        self._heroes: List[HeroData] = []
        self._create_widgets()
        
    def _create_widgets(self):
        # Title
        title_frame = tk.Frame(self, bg=RoboEvonyTheme.BG_LIGHT)
        title_frame.pack(fill=tk.X)
        
        tk.Label(title_frame, text="Heroes", bg=RoboEvonyTheme.BG_LIGHT,
                fg=RoboEvonyTheme.TEXT_GOLD, font=RoboEvonyTheme.FONT_HEADER).pack(side=tk.LEFT, padx=5)
        
        # Header
        header_frame = tk.Frame(self, bg=RoboEvonyTheme.BG_LIGHT)
        header_frame.pack(fill=tk.X)
        
        for col in self.COLUMNS:
            tk.Label(header_frame, text=col, bg=RoboEvonyTheme.BG_LIGHT,
                    fg=RoboEvonyTheme.TEXT_GOLD, font=RoboEvonyTheme.FONT_SMALL,
                    width=8).pack(side=tk.LEFT, padx=1)
                    
        # Hero list (scrollable)
        self._hero_frame = tk.Frame(self, bg=RoboEvonyTheme.BG_PANEL)
        self._hero_frame.pack(fill=tk.BOTH, expand=True)
        
    def set_heroes(self, heroes: List[HeroData]):
        self._heroes = heroes
        
        for widget in self._hero_frame.winfo_children():
            widget.destroy()
            
        for i, hero in enumerate(heroes):
            row_bg = RoboEvonyTheme.BG_PANEL if i % 2 == 0 else RoboEvonyTheme.BG_MEDIUM
            row = tk.Frame(self._hero_frame, bg=row_bg)
            row.pack(fill=tk.X, pady=1)
            
            # View button
            tk.Button(row, text="👁", bg=RoboEvonyTheme.BUTTON_BG,
                     fg=RoboEvonyTheme.TEXT_PRIMARY, width=4,
                     font=RoboEvonyTheme.FONT_SMALL).pack(side=tk.LEFT, padx=1)
            
            # Hero name
            tk.Label(row, text=hero.name, bg=row_bg, fg=RoboEvonyTheme.TEXT_PRIMARY,
                    font=RoboEvonyTheme.FONT_SMALL, width=10, anchor=tk.W).pack(side=tk.LEFT, padx=1)
            
            # Status
            status_color = RoboEvonyTheme.TEXT_GREEN if hero.status == "Idle" else RoboEvonyTheme.TEXT_YELLOW
            tk.Label(row, text=hero.status, bg=row_bg, fg=status_color,
                    font=RoboEvonyTheme.FONT_SMALL, width=8).pack(side=tk.LEFT, padx=1)
            
            # Level
            tk.Label(row, text=str(hero.level), bg=row_bg, fg=RoboEvonyTheme.TEXT_GOLD,
                    font=RoboEvonyTheme.FONT_SMALL, width=6).pack(side=tk.LEFT, padx=1)
            
            # Type (Attack focused)
            tk.Label(row, text="Atk", bg=row_bg, fg=RoboEvonyTheme.TEXT_RED,
                    font=RoboEvonyTheme.FONT_SMALL, width=6).pack(side=tk.LEFT, padx=1)
            
            # Base stats
            tk.Label(row, text=f"{hero.politics}/{hero.attack}/{hero.intelligence}",
                    bg=row_bg, fg=RoboEvonyTheme.TEXT_PRIMARY,
                    font=RoboEvonyTheme.FONT_SMALL, width=10).pack(side=tk.LEFT, padx=1)
            
            # Energy
            tk.Label(row, text=f"{hero.energy}%", bg=row_bg, fg=RoboEvonyTheme.TEXT_BLUE,
                    font=RoboEvonyTheme.FONT_SMALL, width=6).pack(side=tk.LEFT, padx=1)
            
            # Recall button
            tk.Button(row, text="Recall", bg=RoboEvonyTheme.BUTTON_BG,
                     fg=RoboEvonyTheme.TEXT_PRIMARY,
                     font=RoboEvonyTheme.FONT_SMALL).pack(side=tk.LEFT, padx=1)
            
            # Fire button
            tk.Button(row, text="Fire", bg=RoboEvonyTheme.BUTTON_RED,
                     fg=RoboEvonyTheme.TEXT_PRIMARY,
                     font=RoboEvonyTheme.FONT_SMALL).pack(side=tk.LEFT, padx=1)

# =============================================================================
# NEW ARMY DIALOG
# =============================================================================

class NewArmyDialog(tk.Toplevel):
    """Army deployment dialog"""
    
    def __init__(self, parent, heroes: List[HeroData], **kwargs):
        super().__init__(parent, **kwargs)
        
        self.title("New Army")
        self.geometry("600x700")
        self.configure(bg=RoboEvonyTheme.BG_DARK)
        
        self._heroes = heroes
        self._create_widgets()
        
    def _create_widgets(self):
        # City selector
        top_frame = tk.Frame(self, bg=RoboEvonyTheme.BG_DARK)
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(top_frame, text="City:", bg=RoboEvonyTheme.BG_DARK,
                fg=RoboEvonyTheme.TEXT_PRIMARY).pack(side=tk.LEFT)
        self._city_combo = ttk.Combobox(top_frame, values=["Atlantis(0,0)", "Babylon(100,100)"])
        self._city_combo.pack(side=tk.LEFT, padx=5)
        self._city_combo.current(0)
        
        tk.Label(top_frame, text="Dispatch: 0 / 375,000", bg=RoboEvonyTheme.BG_DARK,
                fg=RoboEvonyTheme.TEXT_SECONDARY).pack(side=tk.RIGHT)
        
        # Target coordinates
        target_frame = tk.Frame(self, bg=RoboEvonyTheme.BG_DARK)
        target_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(target_frame, text="Target X:", bg=RoboEvonyTheme.BG_DARK,
                fg=RoboEvonyTheme.TEXT_PRIMARY).pack(side=tk.LEFT)
        self._x_entry = tk.Entry(target_frame, width=6, bg=RoboEvonyTheme.BG_INPUT,
                                fg=RoboEvonyTheme.TEXT_PRIMARY)
        self._x_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Label(target_frame, text="Y:", bg=RoboEvonyTheme.BG_DARK,
                fg=RoboEvonyTheme.TEXT_PRIMARY).pack(side=tk.LEFT)
        self._y_entry = tk.Entry(target_frame, width=6, bg=RoboEvonyTheme.BG_INPUT,
                                fg=RoboEvonyTheme.TEXT_PRIMARY)
        self._y_entry.pack(side=tk.LEFT, padx=5)
        
        # Mission type
        tk.Label(target_frame, text="Mission:", bg=RoboEvonyTheme.BG_DARK,
                fg=RoboEvonyTheme.TEXT_PRIMARY).pack(side=tk.LEFT, padx=(20, 5))
        self._mission_combo = ttk.Combobox(target_frame, 
                                           values=["Attack", "Scout", "Transport", "Reinforce"])
        self._mission_combo.pack(side=tk.LEFT)
        self._mission_combo.current(0)
        
        # Hero selector
        hero_frame = tk.Frame(self, bg=RoboEvonyTheme.BG_DARK)
        hero_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(hero_frame, text="Hero:", bg=RoboEvonyTheme.BG_DARK,
                fg=RoboEvonyTheme.TEXT_PRIMARY).pack(side=tk.LEFT)
        
        hero_names = [f"{h.name} ({h.level}) {h.politics}/{h.attack}/{h.intelligence}" 
                     for h in self._heroes]
        self._hero_combo = ttk.Combobox(hero_frame, values=hero_names, width=30)
        self._hero_combo.pack(side=tk.LEFT, padx=5)
        if hero_names:
            self._hero_combo.current(0)
            
        # Troop selection grid
        troop_frame = tk.LabelFrame(self, text="Troops", bg=RoboEvonyTheme.BG_PANEL,
                                    fg=RoboEvonyTheme.TEXT_GOLD)
        troop_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        troop_types = ["Worker", "Warrior", "Scout", "Pikeman", "Swordsman", "Archer",
                      "Cavalry", "Cataphract", "Transport", "Ballista", "Ram", "Catapult"]
        
        self._troop_entries = {}
        for i, troop in enumerate(troop_types):
            row = i // 3
            col = i % 3
            
            frame = tk.Frame(troop_frame, bg=RoboEvonyTheme.BG_PANEL)
            frame.grid(row=row, column=col, padx=5, pady=3, sticky=tk.W)
            
            tk.Label(frame, text=troop, bg=RoboEvonyTheme.BG_PANEL,
                    fg=RoboEvonyTheme.TEXT_PRIMARY, width=10, anchor=tk.W).pack(side=tk.LEFT)
            
            entry = tk.Entry(frame, width=12, bg=RoboEvonyTheme.BG_INPUT,
                           fg=RoboEvonyTheme.TEXT_PRIMARY)
            entry.pack(side=tk.LEFT)
            entry.insert(0, "0")
            self._troop_entries[troop.lower()] = entry
            
        # Clear button
        tk.Button(troop_frame, text="Clear All", bg=RoboEvonyTheme.BUTTON_BG,
                 fg=RoboEvonyTheme.TEXT_PRIMARY, command=self._clear_troops).grid(
                     row=4, column=2, pady=10)
        
        # Preset management
        preset_frame = tk.Frame(self, bg=RoboEvonyTheme.BG_DARK)
        preset_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(preset_frame, text="Preset:", bg=RoboEvonyTheme.BG_DARK,
                fg=RoboEvonyTheme.TEXT_PRIMARY).pack(side=tk.LEFT)
        self._preset_combo = ttk.Combobox(preset_frame, values=["Default", "Scout", "Full Attack"])
        self._preset_combo.pack(side=tk.LEFT, padx=5)
        
        tk.Button(preset_frame, text="Save Preset", bg=RoboEvonyTheme.BUTTON_BG,
                 fg=RoboEvonyTheme.TEXT_PRIMARY).pack(side=tk.LEFT, padx=5)
        
        # Deploy button
        tk.Button(self, text="Deploy Army", bg=RoboEvonyTheme.BUTTON_GREEN,
                 fg=RoboEvonyTheme.TEXT_PRIMARY, font=RoboEvonyTheme.FONT_HEADER,
                 command=self._deploy).pack(pady=20)
                 
    def _clear_troops(self):
        for entry in self._troop_entries.values():
            entry.delete(0, tk.END)
            entry.insert(0, "0")
            
    def _deploy(self):
        self.destroy()

# =============================================================================
# LOG PANEL COMPONENT
# =============================================================================

class LogPanel(tk.Frame):
    """Multi-tab log panel"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=RoboEvonyTheme.BG_PANEL, **kwargs)
        self._create_widgets()
        
    def _create_widgets(self):
        # Tab bar
        tabs = tk.Frame(self, bg=RoboEvonyTheme.BG_MEDIUM)
        tabs.pack(fill=tk.X)
        
        tab_names = ["Log", "City Log", "War Log", "Maps", "Account", "Snippets"]
        self._tab_buttons = {}
        
        for name in tab_names:
            btn = tk.Button(tabs, text=name, bg=RoboEvonyTheme.TAB_INACTIVE,
                          fg=RoboEvonyTheme.TEXT_PRIMARY, font=RoboEvonyTheme.FONT_SMALL,
                          relief=tk.FLAT, padx=8, pady=2)
            btn.pack(side=tk.LEFT, padx=1, pady=2)
            self._tab_buttons[name] = btn
            
        self._tab_buttons["Log"].config(bg=RoboEvonyTheme.TAB_ACTIVE)
        
        # Log text area
        self._log_text = tk.Text(self, bg=RoboEvonyTheme.BG_INPUT,
                                fg=RoboEvonyTheme.TEXT_PRIMARY,
                                font=RoboEvonyTheme.FONT_SMALL,
                                height=8, state=tk.DISABLED)
        self._log_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Configure tags for colors
        self._log_text.tag_configure("normal", foreground=RoboEvonyTheme.TEXT_PRIMARY)
        self._log_text.tag_configure("warning", foreground=RoboEvonyTheme.TEXT_YELLOW)
        self._log_text.tag_configure("error", foreground=RoboEvonyTheme.TEXT_RED)
        self._log_text.tag_configure("success", foreground=RoboEvonyTheme.TEXT_GREEN)
        self._log_text.tag_configure("info", foreground=RoboEvonyTheme.TEXT_BLUE)
        
    def log(self, message: str, level: str = "normal"):
        self._log_text.config(state=tk.NORMAL)
        timestamp = datetime.now().strftime("%H:%M:%S")
        self._log_text.insert(tk.END, f"[{timestamp}] {message}\n", level)
        self._log_text.see(tk.END)
        self._log_text.config(state=tk.DISABLED)

# =============================================================================
# CHAT PANEL COMPONENT
# =============================================================================

class ChatPanel(tk.Frame):
    """Chat panel with channel tabs"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=RoboEvonyTheme.BG_PANEL, **kwargs)
        self._create_widgets()
        
    def _create_widgets(self):
        # Channel tabs
        tabs = tk.Frame(self, bg=RoboEvonyTheme.BG_MEDIUM)
        tabs.pack(fill=tk.X)
        
        channels = ["Alliance", "Private", "World", "System", "Commands"]
        for ch in channels:
            btn = tk.Button(tabs, text=ch, bg=RoboEvonyTheme.TAB_INACTIVE,
                          fg=RoboEvonyTheme.TEXT_PRIMARY, font=RoboEvonyTheme.FONT_SMALL,
                          relief=tk.FLAT, padx=6, pady=2)
            btn.pack(side=tk.LEFT, padx=1, pady=2)
            
        # Chat display
        self._chat_text = tk.Text(self, bg=RoboEvonyTheme.BG_INPUT,
                                 fg=RoboEvonyTheme.TEXT_PRIMARY,
                                 font=RoboEvonyTheme.FONT_SMALL,
                                 height=6, state=tk.DISABLED)
        self._chat_text.pack(fill=tk.BOTH, expand=True, pady=2)
        
        # Input
        input_frame = tk.Frame(self, bg=RoboEvonyTheme.BG_PANEL)
        input_frame.pack(fill=tk.X)
        
        self._chat_entry = tk.Entry(input_frame, bg=RoboEvonyTheme.BG_INPUT,
                                   fg=RoboEvonyTheme.TEXT_PRIMARY)
        self._chat_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        tk.Button(input_frame, text="Send", bg=RoboEvonyTheme.BUTTON_BG,
                 fg=RoboEvonyTheme.TEXT_PRIMARY).pack(side=tk.RIGHT, padx=2)

# =============================================================================
# ITEMS PANEL COMPONENT
# =============================================================================

class ItemsPanel(tk.Frame):
    """Items/inventory panel"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=RoboEvonyTheme.BG_PANEL, **kwargs)
        self._create_widgets()
        
    def _create_widgets(self):
        # Tabs
        tabs = tk.Frame(self, bg=RoboEvonyTheme.BG_MEDIUM)
        tabs.pack(fill=tk.X)
        
        tab_names = ["Mail", "Alliance", "Statistics", "Historic Heroes", 
                    "Legendary Hero", "Items", "Reports"]
        for name in tab_names:
            btn = tk.Button(tabs, text=name, bg=RoboEvonyTheme.TAB_INACTIVE,
                          fg=RoboEvonyTheme.TEXT_PRIMARY, font=RoboEvonyTheme.FONT_SMALL,
                          relief=tk.FLAT, padx=4, pady=2)
            btn.pack(side=tk.LEFT, padx=1)
            
        # Items table header
        header = tk.Frame(self, bg=RoboEvonyTheme.BG_LIGHT)
        header.pack(fill=tk.X, pady=(5, 0))
        
        cols = ["Name", "Description", "Price", "Count", "Action"]
        widths = [15, 25, 8, 8, 8]
        
        for col, width in zip(cols, widths):
            tk.Label(header, text=col, bg=RoboEvonyTheme.BG_LIGHT,
                    fg=RoboEvonyTheme.TEXT_GOLD, font=RoboEvonyTheme.FONT_SMALL,
                    width=width).pack(side=tk.LEFT, padx=2)
                    
        # Items list (scrollable)
        self._items_frame = tk.Frame(self, bg=RoboEvonyTheme.BG_PANEL)
        self._items_frame.pack(fill=tk.BOTH, expand=True)
        
        # Sample items
        items = [
            ItemData("Speaker", "Broadcast message", 100, 5),
            ItemData("City_Teleporter", "Move city", 500, 2),
            ItemData("Delicate_gem", "Hero upgrade", 200, 10),
            ItemData("Bernini's_Hammer", "Instant build", 300, 3),
        ]
        self.set_items(items)
        
    def set_items(self, items: List[ItemData]):
        for widget in self._items_frame.winfo_children():
            widget.destroy()
            
        for i, item in enumerate(items):
            row_bg = RoboEvonyTheme.BG_PANEL if i % 2 == 0 else RoboEvonyTheme.BG_MEDIUM
            row = tk.Frame(self._items_frame, bg=row_bg)
            row.pack(fill=tk.X, pady=1)
            
            tk.Label(row, text=item.name, bg=row_bg, fg=RoboEvonyTheme.TEXT_PRIMARY,
                    font=RoboEvonyTheme.FONT_SMALL, width=15, anchor=tk.W).pack(side=tk.LEFT, padx=2)
            tk.Label(row, text=item.description, bg=row_bg, fg=RoboEvonyTheme.TEXT_SECONDARY,
                    font=RoboEvonyTheme.FONT_SMALL, width=25, anchor=tk.W).pack(side=tk.LEFT, padx=2)
            tk.Label(row, text=str(item.price), bg=row_bg, fg=RoboEvonyTheme.TEXT_GOLD,
                    font=RoboEvonyTheme.FONT_SMALL, width=8).pack(side=tk.LEFT, padx=2)
            tk.Label(row, text=str(item.count), bg=row_bg, fg=RoboEvonyTheme.TEXT_PRIMARY,
                    font=RoboEvonyTheme.FONT_SMALL, width=8).pack(side=tk.LEFT, padx=2)
            tk.Button(row, text="View", bg=RoboEvonyTheme.BUTTON_BG,
                     fg=RoboEvonyTheme.TEXT_PRIMARY, font=RoboEvonyTheme.FONT_SMALL).pack(side=tk.LEFT, padx=2)

# =============================================================================
# MAIN AUTOEVONY BOT GUI
# =============================================================================

class AutoEvonyBotGUI(tk.Tk):
    """Complete AutoEvony/RoboEvony Bot 1:1 Recreation"""
    
    def __init__(self):
        super().__init__()
        
        self.title("AutoEvony Bot - Complete Recreation v1")
        self.geometry("1400x950")
        self.configure(bg=RoboEvonyTheme.BG_DARK)
        
        # Configure styles
        self._configure_styles()
        
        # Mock data
        self._cities = self._create_mock_cities()
        self._troops = TroopData(
            worker=1000000, warrior=500000, scout=100000,
            pikeman=200000, swordsman=150000, archer=1786706432,
            cavalry=100000, cataphract=50000, transporter=75000,
            ballista=10000, ram=5000, catapult=2000
        )
        self._heroes = self._create_mock_heroes()
        
        # Create UI
        self._create_menu()
        self._create_main_layout()
        
        # Load data
        self._load_initial_data()
        
    def _configure_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure(".", background=RoboEvonyTheme.BG_DARK, foreground=RoboEvonyTheme.TEXT_PRIMARY)
        
    def _create_mock_cities(self) -> List[CityData]:
        return [
            CityData(1, "Atlantis", 0, 0, 500000, 100, 44841205, 55050, 100000, 80000, 60000),
            CityData(2, "Babylon", 796, 7, 300000, 95, 20000000, 30000, 50000, 40000, 30000),
            CityData(3, "Borg", 790, 796, 250000, 90, 15000000, 25000, 45000, 35000, 25000),
            CityData(4, "Friesland", 799, 9, 200000, 88, 10000000, 20000, 40000, 30000, 20000),
            CityData(5, "Fallbrook", 0, 799, 180000, 92, 8000000, 18000, 35000, 28000, 18000),
            CityData(6, "Hindenburg", 8, 7, 150000, 85, 6000000, 15000, 30000, 25000, 15000),
            CityData(7, "Jerusalem", 300, 700, 120000, 80, 4000000, 12000, 25000, 20000, 12000),
            CityData(8, "Mojave", 793, 796, 100000, 78, 3000000, 10000, 20000, 18000, 10000),
        ]
        
    def _create_mock_heroes(self) -> List[HeroData]:
        return [
            HeroData(1, "Queen", 100, 85, 754, 85, "Idle", 100),
            HeroData(2, "LeifEricson", 95, 70, 680, 90, "Idle", 95),
            HeroData(3, "NancyWard", 88, 90, 550, 75, "Mayor", 100),
            HeroData(4, "HenryIV", 92, 65, 720, 80, "Attacking", 45),
            HeroData(5, "Tess", 85, 75, 620, 70, "Idle", 88),
            HeroData(6, "Ansel", 78, 80, 580, 65, "Idle", 92),
            HeroData(7, "Armstrong", 82, 60, 700, 85, "Idle", 100),
            HeroData(8, "Murphy", 75, 85, 540, 60, "Scouting", 30),
        ]
        
    def _create_menu(self):
        menubar = tk.Menu(self, bg=RoboEvonyTheme.BG_DARK, fg=RoboEvonyTheme.TEXT_PRIMARY)
        
        # Bot menu
        bot_menu = tk.Menu(menubar, tearoff=0, bg=RoboEvonyTheme.BG_MEDIUM, fg=RoboEvonyTheme.TEXT_PRIMARY)
        bot_menu.add_command(label="Connect", command=self._on_connect)
        bot_menu.add_command(label="Disconnect", command=self._on_disconnect)
        bot_menu.add_separator()
        bot_menu.add_command(label="Settings", command=self._show_settings)
        bot_menu.add_separator()
        bot_menu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="Bot", menu=bot_menu)
        
        # City menu
        city_menu = tk.Menu(menubar, tearoff=0, bg=RoboEvonyTheme.BG_MEDIUM, fg=RoboEvonyTheme.TEXT_PRIMARY)
        city_menu.add_command(label="New Army", command=self._show_new_army)
        city_menu.add_command(label="Recall All", command=self._recall_all)
        city_menu.add_separator()
        city_menu.add_command(label="View Buildings", command=self._view_buildings)
        city_menu.add_command(label="View Troops", command=self._view_troops)
        menubar.add_cascade(label="City", menu=city_menu)
        
        # Scripts menu
        scripts_menu = tk.Menu(menubar, tearoff=0, bg=RoboEvonyTheme.BG_MEDIUM, fg=RoboEvonyTheme.TEXT_PRIMARY)
        scripts_menu.add_command(label="Load Script", command=self._load_script)
        scripts_menu.add_command(label="Save Script", command=self._save_script)
        scripts_menu.add_separator()
        scripts_menu.add_command(label="Run", command=self._run_script)
        scripts_menu.add_command(label="Stop", command=self._stop_script)
        menubar.add_cascade(label="Scripts", menu=scripts_menu)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0, bg=RoboEvonyTheme.BG_MEDIUM, fg=RoboEvonyTheme.TEXT_PRIMARY)
        tools_menu.add_command(label="Calculator", command=self._show_calculator)
        tools_menu.add_command(label="Troop Glitch", command=self._show_glitch_tool)
        tools_menu.add_command(label="Map Scanner", command=self._show_map_scanner)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        
        self.config(menu=menubar)
        
    def _create_main_layout(self):
        # Header bar
        self._header = HeaderBar(self)
        self._header.pack(fill=tk.X, padx=5, pady=5)
        
        # City tabs
        self._city_tabs = CityTabBar(self, on_city_change=self._on_city_change)
        self._city_tabs.pack(fill=tk.X, padx=5)
        
        # Main content - 3 columns
        main_frame = tk.Frame(self, bg=RoboEvonyTheme.BG_DARK)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left panel - Script Editor
        left_panel = tk.Frame(main_frame, bg=RoboEvonyTheme.BG_PANEL, width=350)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5))
        left_panel.pack_propagate(False)
        
        self._script_editor = ScriptEditor(left_panel)
        self._script_editor.pack(fill=tk.BOTH, expand=True)
        
        # Center panel - Troops + Heroes
        center_panel = tk.Frame(main_frame, bg=RoboEvonyTheme.BG_DARK)
        center_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # City info bar
        city_info = tk.Frame(center_panel, bg=RoboEvonyTheme.BG_PANEL)
        city_info.pack(fill=tk.X, pady=(0, 5))
        
        self._city_name_label = tk.Label(city_info, text="Atlantis",
                                         bg=RoboEvonyTheme.BG_PANEL, fg=RoboEvonyTheme.TEXT_GOLD,
                                         font=RoboEvonyTheme.FONT_HEADER)
        self._city_name_label.pack(side=tk.LEFT, padx=10)
        
        self._coords_label = tk.Label(city_info, text="(0,0) Friesland",
                                      bg=RoboEvonyTheme.BG_PANEL, fg=RoboEvonyTheme.TEXT_SECONDARY)
        self._coords_label.pack(side=tk.LEFT)
        
        self._city_resources = tk.Label(city_info, text="Food: 55,050 | Gold: -13,350 | Loyalty: 100%",
                                        bg=RoboEvonyTheme.BG_PANEL, fg=RoboEvonyTheme.TEXT_PRIMARY)
        self._city_resources.pack(side=tk.RIGHT, padx=10)
        
        # Troop table
        self._troop_table = TroopTable(center_panel)
        self._troop_table.pack(fill=tk.X, pady=(0, 5))
        
        # Hero table  
        self._hero_table = HeroTable(center_panel)
        self._hero_table.pack(fill=tk.BOTH, expand=True)
        
        # Right panel - Chat
        right_panel = tk.Frame(main_frame, bg=RoboEvonyTheme.BG_PANEL, width=280)
        right_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0))
        right_panel.pack_propagate(False)
        
        self._chat_panel = ChatPanel(right_panel)
        self._chat_panel.pack(fill=tk.BOTH, expand=True)
        
        # Bottom area - Log + Items
        bottom_frame = tk.Frame(self, bg=RoboEvonyTheme.BG_DARK)
        bottom_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Log panel
        log_frame = tk.Frame(bottom_frame, bg=RoboEvonyTheme.BG_PANEL)
        log_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        self._log_panel = LogPanel(log_frame)
        self._log_panel.pack(fill=tk.BOTH, expand=True)
        
        # Items panel
        items_frame = tk.Frame(bottom_frame, bg=RoboEvonyTheme.BG_PANEL, width=500)
        items_frame.pack(side=tk.RIGHT, fill=tk.Y)
        items_frame.pack_propagate(False)
        
        self._items_panel = ItemsPanel(items_frame)
        self._items_panel.pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        status_bar = tk.Frame(self, bg=RoboEvonyTheme.BG_MEDIUM)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        
        self._status_label = tk.Label(status_bar, text="● Disconnected",
                                      bg=RoboEvonyTheme.BG_MEDIUM, fg=RoboEvonyTheme.TEXT_RED,
                                      font=RoboEvonyTheme.FONT_SMALL)
        self._status_label.pack(side=tk.LEFT, padx=10, pady=2)
        
        self._script_status = tk.Label(status_bar, text="Script: Stopped",
                                       bg=RoboEvonyTheme.BG_MEDIUM, fg=RoboEvonyTheme.TEXT_SECONDARY)
        self._script_status.pack(side=tk.RIGHT, padx=10, pady=2)
        
    def _load_initial_data(self):
        self._city_tabs.set_cities(self._cities)
        self._troop_table.update_troops(self._troops)
        self._hero_table.set_heroes(self._heroes)
        
        # Log some startup messages
        self._log_panel.log("AutoEvony Bot v1.0 started", "info")
        self._log_panel.log("Loading configuration...", "normal")
        self._log_panel.log("Ready to connect", "success")
        
    def _on_city_change(self, city_id: int):
        for city in self._cities:
            if city.id == city_id:
                self._city_name_label.config(text=city.name)
                self._coords_label.config(text=f"({city.x},{city.y})")
                self._city_resources.config(
                    text=f"Food: {city.food:,} | Gold: {city.gold:,} | Loyalty: {city.loyalty}%"
                )
                break
                
    def _on_connect(self):
        self._status_label.config(text="● Connected", fg=RoboEvonyTheme.TEXT_GREEN)
        self._log_panel.log("Connected to server", "success")
        
    def _on_disconnect(self):
        self._status_label.config(text="● Disconnected", fg=RoboEvonyTheme.TEXT_RED)
        self._log_panel.log("Disconnected from server", "warning")
        
    def _show_settings(self):
        pass
        
    def _show_new_army(self):
        dialog = NewArmyDialog(self, self._heroes)
        dialog.grab_set()
        
    def _recall_all(self):
        self._log_panel.log("Recalling all armies...", "info")
        
    def _view_buildings(self):
        pass
        
    def _view_troops(self):
        pass
        
    def _load_script(self):
        pass
        
    def _save_script(self):
        pass
        
    def _run_script(self):
        self._script_status.config(text="Script: Running", fg=RoboEvonyTheme.TEXT_GREEN)
        self._log_panel.log("Script started", "success")
        
    def _stop_script(self):
        self._script_status.config(text="Script: Stopped", fg=RoboEvonyTheme.TEXT_SECONDARY)
        self._log_panel.log("Script stopped", "warning")
        
    def _show_calculator(self):
        pass
        
    def _show_glitch_tool(self):
        pass
        
    def _show_map_scanner(self):
        pass


# =============================================================================
# ENTRY POINT
# =============================================================================

def main():
    app = AutoEvonyBotGUI()
    app.mainloop()

if __name__ == "__main__":
    main()
