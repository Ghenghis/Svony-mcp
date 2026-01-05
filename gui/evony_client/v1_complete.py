"""
Evony Client GUI v1 - Complete with Full Styling
1:1 Recreation of Evony Age II Flash Client Interface
For testing and reverse engineering purposes
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass
from datetime import datetime
import json

# =============================================================================
# DATA MODELS
# =============================================================================

@dataclass
class CityData:
    id: int
    name: str
    x: int
    y: int
    population: int
    loyalty: int
    gold: int
    food: int
    lumber: int
    stone: int
    iron: int

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

@dataclass
class BuildingData:
    id: int
    type_id: int
    name: str
    level: int
    position_id: int

# =============================================================================
# THEME CONFIGURATION
# =============================================================================

class EvonyTheme:
    """Evony Age II Dark Theme"""
    BG_DARK = "#1a1a2e"
    BG_MEDIUM = "#16213e"
    BG_LIGHT = "#0f3460"
    BG_PANEL = "#1f1f3d"
    
    TEXT_PRIMARY = "#e8e8e8"
    TEXT_SECONDARY = "#a0a0a0"
    TEXT_GOLD = "#ffd700"
    TEXT_GREEN = "#00ff88"
    TEXT_RED = "#ff4444"
    TEXT_BLUE = "#4488ff"
    
    ACCENT_GOLD = "#c9a227"
    ACCENT_BLUE = "#2a6fb0"
    ACCENT_GREEN = "#2e8b57"
    ACCENT_RED = "#8b2e2e"
    
    BORDER_COLOR = "#3d3d5c"
    BUTTON_BG = "#2a4a7a"
    BUTTON_HOVER = "#3a5a8a"
    BUTTON_ACTIVE = "#4a6a9a"
    
    FONT_TITLE = ("Arial", 14, "bold")
    FONT_HEADER = ("Arial", 11, "bold")
    FONT_NORMAL = ("Arial", 10)
    FONT_SMALL = ("Arial", 9)
    FONT_MONO = ("Consolas", 10)

# =============================================================================
# RESOURCE BAR COMPONENT
# =============================================================================

class ResourceBar(tk.Frame):
    """Top resource bar showing gold, food, lumber, stone, iron"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=EvonyTheme.BG_DARK, **kwargs)
        self._create_widgets()
        
    def _create_widgets(self):
        # Gold
        self._gold_frame = self._create_resource_display("Gold:", "0", EvonyTheme.TEXT_GOLD)
        self._gold_frame.pack(side=tk.LEFT, padx=10)
        
        # Food
        self._food_frame = self._create_resource_display("Food:", "0", EvonyTheme.TEXT_GREEN)
        self._food_frame.pack(side=tk.LEFT, padx=10)
        
        # Lumber
        self._lumber_frame = self._create_resource_display("Lumber:", "0", EvonyTheme.TEXT_PRIMARY)
        self._lumber_frame.pack(side=tk.LEFT, padx=10)
        
        # Stone
        self._stone_frame = self._create_resource_display("Stone:", "0", EvonyTheme.TEXT_PRIMARY)
        self._stone_frame.pack(side=tk.LEFT, padx=10)
        
        # Iron
        self._iron_frame = self._create_resource_display("Iron:", "0", EvonyTheme.TEXT_PRIMARY)
        self._iron_frame.pack(side=tk.LEFT, padx=10)
        
        # Population
        self._pop_frame = self._create_resource_display("Pop:", "0/0", EvonyTheme.TEXT_BLUE)
        self._pop_frame.pack(side=tk.LEFT, padx=10)
        
        # Time display
        self._time_label = tk.Label(
            self, text="00:00:00", 
            bg=EvonyTheme.BG_DARK, fg=EvonyTheme.TEXT_PRIMARY,
            font=EvonyTheme.FONT_HEADER
        )
        self._time_label.pack(side=tk.RIGHT, padx=20)
        self._update_time()
        
    def _create_resource_display(self, label: str, value: str, color: str) -> tk.Frame:
        frame = tk.Frame(self, bg=EvonyTheme.BG_DARK)
        
        lbl = tk.Label(frame, text=label, bg=EvonyTheme.BG_DARK, 
                       fg=EvonyTheme.TEXT_SECONDARY, font=EvonyTheme.FONT_SMALL)
        lbl.pack(side=tk.LEFT)
        
        val = tk.Label(frame, text=value, bg=EvonyTheme.BG_DARK,
                       fg=color, font=EvonyTheme.FONT_NORMAL)
        val.pack(side=tk.LEFT, padx=(2, 0))
        
        frame._value_label = val
        return frame
    
    def _update_time(self):
        now = datetime.now().strftime("%H:%M:%S")
        self._time_label.config(text=now)
        self.after(1000, self._update_time)
        
    def update_resources(self, gold: int, food: int, lumber: int, stone: int, iron: int, pop: int, max_pop: int):
        self._gold_frame._value_label.config(text=f"{gold:,}")
        self._food_frame._value_label.config(text=f"{food:,}")
        self._lumber_frame._value_label.config(text=f"{lumber:,}")
        self._stone_frame._value_label.config(text=f"{stone:,}")
        self._iron_frame._value_label.config(text=f"{iron:,}")
        self._pop_frame._value_label.config(text=f"{pop:,}/{max_pop:,}")

# =============================================================================
# CITY TABS COMPONENT
# =============================================================================

class CityTabs(tk.Frame):
    """Multi-city tab bar for quick switching"""
    
    def __init__(self, parent, on_city_change: Optional[Callable] = None, **kwargs):
        super().__init__(parent, bg=EvonyTheme.BG_MEDIUM, **kwargs)
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
                text=f"{city.name}({city.x},{city.y})",
                bg=EvonyTheme.BUTTON_BG,
                fg=EvonyTheme.TEXT_PRIMARY,
                activebackground=EvonyTheme.BUTTON_ACTIVE,
                activeforeground=EvonyTheme.TEXT_PRIMARY,
                relief=tk.FLAT,
                font=EvonyTheme.FONT_SMALL,
                padx=8, pady=4,
                command=lambda c=city: self._select_city(c.id)
            )
            btn.pack(side=tk.LEFT, padx=2, pady=4)
            self._tab_buttons[city.id] = btn
            
        if self._cities and self._selected_city is None:
            self._select_city(self._cities[0].id)
            
    def _select_city(self, city_id: int):
        self._selected_city = city_id
        
        for cid, btn in self._tab_buttons.items():
            if cid == city_id:
                btn.config(bg=EvonyTheme.ACCENT_GREEN, fg=EvonyTheme.TEXT_PRIMARY)
            else:
                btn.config(bg=EvonyTheme.BUTTON_BG, fg=EvonyTheme.TEXT_PRIMARY)
                
        if self._on_city_change:
            self._on_city_change(city_id)

# =============================================================================
# TROOP TABLE COMPONENT
# =============================================================================

class TroopTable(tk.Frame):
    """Troop display table with all columns"""
    
    TROOP_TYPES = [
        "Worker", "Warrior", "Scout", "Pikeman", "Swordsman", "Archer",
        "Cavalry", "Cataphract", "Transporter", "Ballista", "Ram", "Catapult"
    ]
    
    COLUMNS = ["Type", "Avail", "Total", "Training", "Queue", "Reinf."]
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=EvonyTheme.BG_PANEL, **kwargs)
        self._create_widgets()
        
    def _create_widgets(self):
        # Header
        header_frame = tk.Frame(self, bg=EvonyTheme.BG_LIGHT)
        header_frame.pack(fill=tk.X)
        
        for i, col in enumerate(self.COLUMNS):
            lbl = tk.Label(
                header_frame, text=col,
                bg=EvonyTheme.BG_LIGHT, fg=EvonyTheme.TEXT_GOLD,
                font=EvonyTheme.FONT_HEADER,
                width=12, anchor=tk.W
            )
            lbl.grid(row=0, column=i, padx=2, pady=4, sticky=tk.W)
            
        # Troop rows
        self._rows_frame = tk.Frame(self, bg=EvonyTheme.BG_PANEL)
        self._rows_frame.pack(fill=tk.BOTH, expand=True)
        
        self._row_labels: Dict[str, List[tk.Label]] = {}
        
        for row_idx, troop_type in enumerate(self.TROOP_TYPES):
            row_bg = EvonyTheme.BG_PANEL if row_idx % 2 == 0 else EvonyTheme.BG_MEDIUM
            labels = []
            
            # Type name
            type_lbl = tk.Label(
                self._rows_frame, text=troop_type,
                bg=row_bg, fg=EvonyTheme.TEXT_PRIMARY,
                font=EvonyTheme.FONT_NORMAL,
                width=12, anchor=tk.W
            )
            type_lbl.grid(row=row_idx, column=0, padx=2, pady=2, sticky=tk.W)
            labels.append(type_lbl)
            
            # Value columns
            for col_idx in range(1, len(self.COLUMNS)):
                val_lbl = tk.Label(
                    self._rows_frame, text="0",
                    bg=row_bg, fg=EvonyTheme.TEXT_PRIMARY,
                    font=EvonyTheme.FONT_NORMAL,
                    width=12, anchor=tk.E
                )
                val_lbl.grid(row=row_idx, column=col_idx, padx=2, pady=2, sticky=tk.E)
                labels.append(val_lbl)
                
            self._row_labels[troop_type.lower()] = labels
            
    def update_troops(self, troops: TroopData):
        data = {
            "worker": troops.worker,
            "warrior": troops.warrior,
            "scout": troops.scout,
            "pikeman": troops.pikeman,
            "swordsman": troops.swordsman,
            "archer": troops.archer,
            "cavalry": troops.cavalry,
            "cataphract": troops.cataphract,
            "transporter": troops.transporter,
            "ballista": troops.ballista,
            "ram": troops.ram,
            "catapult": troops.catapult,
        }
        
        for troop_type, count in data.items():
            if troop_type in self._row_labels:
                self._row_labels[troop_type][1].config(text=f"{count:,}")
                self._row_labels[troop_type][2].config(text=f"{count:,}")

# =============================================================================
# BUILDING PANEL COMPONENT
# =============================================================================

class BuildingPanel(tk.Frame):
    """Building list with levels"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=EvonyTheme.BG_PANEL, **kwargs)
        self._create_widgets()
        
    def _create_widgets(self):
        # Title
        title = tk.Label(
            self, text="Buildings",
            bg=EvonyTheme.BG_PANEL, fg=EvonyTheme.TEXT_GOLD,
            font=EvonyTheme.FONT_HEADER
        )
        title.pack(fill=tk.X, pady=(0, 5))
        
        # Scrollable building list
        self._canvas = tk.Canvas(self, bg=EvonyTheme.BG_PANEL, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self._canvas.yview)
        self._scrollable_frame = tk.Frame(self._canvas, bg=EvonyTheme.BG_PANEL)
        
        self._scrollable_frame.bind(
            "<Configure>",
            lambda e: self._canvas.configure(scrollregion=self._canvas.bbox("all"))
        )
        
        self._canvas.create_window((0, 0), window=self._scrollable_frame, anchor=tk.NW)
        self._canvas.configure(yscrollcommand=scrollbar.set)
        
        self._canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def set_buildings(self, buildings: List[BuildingData]):
        for widget in self._scrollable_frame.winfo_children():
            widget.destroy()
            
        for i, building in enumerate(buildings):
            row_bg = EvonyTheme.BG_PANEL if i % 2 == 0 else EvonyTheme.BG_MEDIUM
            
            row = tk.Frame(self._scrollable_frame, bg=row_bg)
            row.pack(fill=tk.X, pady=1)
            
            name_lbl = tk.Label(
                row, text=building.name,
                bg=row_bg, fg=EvonyTheme.TEXT_PRIMARY,
                font=EvonyTheme.FONT_NORMAL,
                width=20, anchor=tk.W
            )
            name_lbl.pack(side=tk.LEFT, padx=5)
            
            level_lbl = tk.Label(
                row, text=f"Lv.{building.level}",
                bg=row_bg, fg=EvonyTheme.TEXT_GOLD,
                font=EvonyTheme.FONT_NORMAL,
                width=8, anchor=tk.E
            )
            level_lbl.pack(side=tk.RIGHT, padx=5)

# =============================================================================
# HERO PANEL COMPONENT
# =============================================================================

class HeroPanel(tk.Frame):
    """Hero management panel"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=EvonyTheme.BG_PANEL, **kwargs)
        self._heroes: List[HeroData] = []
        self._create_widgets()
        
    def _create_widgets(self):
        # Title
        title = tk.Label(
            self, text="Heroes",
            bg=EvonyTheme.BG_PANEL, fg=EvonyTheme.TEXT_GOLD,
            font=EvonyTheme.FONT_HEADER
        )
        title.pack(fill=tk.X, pady=(0, 5))
        
        # Header
        header = tk.Frame(self, bg=EvonyTheme.BG_LIGHT)
        header.pack(fill=tk.X)
        
        cols = ["Name", "Lv", "Pol", "Atk", "Int", "Status"]
        widths = [12, 4, 4, 4, 4, 8]
        
        for col, width in zip(cols, widths):
            lbl = tk.Label(
                header, text=col,
                bg=EvonyTheme.BG_LIGHT, fg=EvonyTheme.TEXT_GOLD,
                font=EvonyTheme.FONT_SMALL,
                width=width
            )
            lbl.pack(side=tk.LEFT, padx=2)
            
        # Hero list
        self._hero_frame = tk.Frame(self, bg=EvonyTheme.BG_PANEL)
        self._hero_frame.pack(fill=tk.BOTH, expand=True)
        
    def set_heroes(self, heroes: List[HeroData]):
        self._heroes = heroes
        
        for widget in self._hero_frame.winfo_children():
            widget.destroy()
            
        for i, hero in enumerate(heroes):
            row_bg = EvonyTheme.BG_PANEL if i % 2 == 0 else EvonyTheme.BG_MEDIUM
            
            row = tk.Frame(self._hero_frame, bg=row_bg)
            row.pack(fill=tk.X, pady=1)
            
            # Name
            tk.Label(row, text=hero.name, bg=row_bg, fg=EvonyTheme.TEXT_PRIMARY,
                    font=EvonyTheme.FONT_SMALL, width=12, anchor=tk.W).pack(side=tk.LEFT, padx=2)
            
            # Level
            tk.Label(row, text=str(hero.level), bg=row_bg, fg=EvonyTheme.TEXT_GOLD,
                    font=EvonyTheme.FONT_SMALL, width=4).pack(side=tk.LEFT, padx=2)
            
            # Stats
            tk.Label(row, text=str(hero.politics), bg=row_bg, fg=EvonyTheme.TEXT_BLUE,
                    font=EvonyTheme.FONT_SMALL, width=4).pack(side=tk.LEFT, padx=2)
            tk.Label(row, text=str(hero.attack), bg=row_bg, fg=EvonyTheme.TEXT_RED,
                    font=EvonyTheme.FONT_SMALL, width=4).pack(side=tk.LEFT, padx=2)
            tk.Label(row, text=str(hero.intelligence), bg=row_bg, fg=EvonyTheme.TEXT_GREEN,
                    font=EvonyTheme.FONT_SMALL, width=4).pack(side=tk.LEFT, padx=2)
            
            # Status
            status_color = EvonyTheme.TEXT_GREEN if hero.status == "Idle" else EvonyTheme.TEXT_GOLD
            tk.Label(row, text=hero.status, bg=row_bg, fg=status_color,
                    font=EvonyTheme.FONT_SMALL, width=8).pack(side=tk.LEFT, padx=2)

# =============================================================================
# MAP VIEW COMPONENT
# =============================================================================

class MapView(tk.Frame):
    """Interactive map grid view"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=EvonyTheme.BG_PANEL, **kwargs)
        self._scale = 32
        self._center_x = 400
        self._center_y = 400
        self._create_widgets()
        
    def _create_widgets(self):
        # Controls
        controls = tk.Frame(self, bg=EvonyTheme.BG_PANEL)
        controls.pack(fill=tk.X, pady=5)
        
        tk.Label(controls, text="X:", bg=EvonyTheme.BG_PANEL, 
                fg=EvonyTheme.TEXT_PRIMARY).pack(side=tk.LEFT, padx=5)
        self._x_entry = tk.Entry(controls, width=5, bg=EvonyTheme.BG_MEDIUM,
                                 fg=EvonyTheme.TEXT_PRIMARY, insertbackground=EvonyTheme.TEXT_PRIMARY)
        self._x_entry.pack(side=tk.LEFT)
        self._x_entry.insert(0, "400")
        
        tk.Label(controls, text="Y:", bg=EvonyTheme.BG_PANEL,
                fg=EvonyTheme.TEXT_PRIMARY).pack(side=tk.LEFT, padx=5)
        self._y_entry = tk.Entry(controls, width=5, bg=EvonyTheme.BG_MEDIUM,
                                 fg=EvonyTheme.TEXT_PRIMARY, insertbackground=EvonyTheme.TEXT_PRIMARY)
        self._y_entry.pack(side=tk.LEFT)
        self._y_entry.insert(0, "400")
        
        go_btn = tk.Button(controls, text="Go", bg=EvonyTheme.BUTTON_BG,
                          fg=EvonyTheme.TEXT_PRIMARY, command=self._go_to_coords)
        go_btn.pack(side=tk.LEFT, padx=10)
        
        tk.Label(controls, text="Scale:", bg=EvonyTheme.BG_PANEL,
                fg=EvonyTheme.TEXT_PRIMARY).pack(side=tk.LEFT, padx=5)
        self._scale_slider = tk.Scale(controls, from_=8, to=64, orient=tk.HORIZONTAL,
                                      bg=EvonyTheme.BG_PANEL, fg=EvonyTheme.TEXT_PRIMARY,
                                      highlightthickness=0, command=self._on_scale_change)
        self._scale_slider.set(32)
        self._scale_slider.pack(side=tk.LEFT)
        
        # Map canvas
        self._canvas = tk.Canvas(self, bg=EvonyTheme.BG_DARK, highlightthickness=1,
                                highlightbackground=EvonyTheme.BORDER_COLOR)
        self._canvas.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self._canvas.bind("<Button-1>", self._on_click)
        self._canvas.bind("<Configure>", self._redraw)
        
    def _go_to_coords(self):
        try:
            self._center_x = int(self._x_entry.get())
            self._center_y = int(self._y_entry.get())
            self._redraw()
        except ValueError:
            pass
            
    def _on_scale_change(self, value):
        self._scale = int(value)
        self._redraw()
        
    def _on_click(self, event):
        # Calculate clicked tile
        pass
        
    def _redraw(self, event=None):
        self._canvas.delete("all")
        
        width = self._canvas.winfo_width()
        height = self._canvas.winfo_height()
        
        if width < 10 or height < 10:
            return
            
        # Draw grid
        tile_size = self._scale
        
        for x in range(0, width, tile_size):
            for y in range(0, height, tile_size):
                # Alternate colors for visibility
                if ((x // tile_size) + (y // tile_size)) % 2 == 0:
                    color = "#1a2a1a"
                else:
                    color = "#1a1a2a"
                    
                self._canvas.create_rectangle(
                    x, y, x + tile_size, y + tile_size,
                    fill=color, outline=EvonyTheme.BORDER_COLOR
                )

# =============================================================================
# CHAT PANEL COMPONENT
# =============================================================================

class ChatPanel(tk.Frame):
    """Chat panel with multiple channels"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=EvonyTheme.BG_PANEL, **kwargs)
        self._create_widgets()
        
    def _create_widgets(self):
        # Channel tabs
        tabs_frame = tk.Frame(self, bg=EvonyTheme.BG_MEDIUM)
        tabs_frame.pack(fill=tk.X)
        
        channels = ["Alliance", "World", "Private", "System"]
        self._channel_buttons = {}
        
        for channel in channels:
            btn = tk.Button(
                tabs_frame, text=channel,
                bg=EvonyTheme.BUTTON_BG, fg=EvonyTheme.TEXT_PRIMARY,
                font=EvonyTheme.FONT_SMALL, relief=tk.FLAT,
                padx=8, pady=2
            )
            btn.pack(side=tk.LEFT, padx=1, pady=2)
            self._channel_buttons[channel] = btn
            
        # Chat display
        self._chat_text = tk.Text(
            self, bg=EvonyTheme.BG_DARK, fg=EvonyTheme.TEXT_PRIMARY,
            font=EvonyTheme.FONT_SMALL, height=8, wrap=tk.WORD,
            state=tk.DISABLED
        )
        self._chat_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Chat entry
        entry_frame = tk.Frame(self, bg=EvonyTheme.BG_PANEL)
        entry_frame.pack(fill=tk.X)
        
        self._chat_entry = tk.Entry(
            entry_frame, bg=EvonyTheme.BG_MEDIUM, fg=EvonyTheme.TEXT_PRIMARY,
            insertbackground=EvonyTheme.TEXT_PRIMARY, font=EvonyTheme.FONT_SMALL
        )
        self._chat_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        send_btn = tk.Button(
            entry_frame, text="Send",
            bg=EvonyTheme.BUTTON_BG, fg=EvonyTheme.TEXT_PRIMARY,
            font=EvonyTheme.FONT_SMALL, command=self._send_message
        )
        send_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
    def _send_message(self):
        message = self._chat_entry.get()
        if message:
            self.add_message("You", message)
            self._chat_entry.delete(0, tk.END)
            
    def add_message(self, sender: str, message: str, color: str = None):
        self._chat_text.config(state=tk.NORMAL)
        timestamp = datetime.now().strftime("%H:%M:%S")
        self._chat_text.insert(tk.END, f"[{timestamp}] {sender}: {message}\n")
        self._chat_text.see(tk.END)
        self._chat_text.config(state=tk.DISABLED)

# =============================================================================
# MAIN EVONY CLIENT GUI
# =============================================================================

class EvonyClientGUI(tk.Tk):
    """Complete Evony Client 1:1 Recreation"""
    
    def __init__(self):
        super().__init__()
        
        self.title("Evony Age II - Client Recreation v1")
        self.geometry("1400x900")
        self.configure(bg=EvonyTheme.BG_DARK)
        
        # Apply theme
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
        self._buildings = self._create_mock_buildings()
        
        # Create UI
        self._create_menu()
        self._create_main_layout()
        
        # Load initial data
        self._load_initial_data()
        
    def _configure_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure(".", background=EvonyTheme.BG_DARK, foreground=EvonyTheme.TEXT_PRIMARY)
        style.configure("TFrame", background=EvonyTheme.BG_DARK)
        style.configure("TLabel", background=EvonyTheme.BG_DARK, foreground=EvonyTheme.TEXT_PRIMARY)
        style.configure("TButton", background=EvonyTheme.BUTTON_BG, foreground=EvonyTheme.TEXT_PRIMARY)
        
    def _create_mock_cities(self) -> List[CityData]:
        return [
            CityData(1, "Atlantis", 0, 0, 500000, 100, 44841205, 55050, 100000, 80000, 60000),
            CityData(2, "Babylon", 100, 100, 300000, 95, 20000000, 30000, 50000, 40000, 30000),
            CityData(3, "Carthage", 200, 50, 250000, 90, 15000000, 25000, 45000, 35000, 25000),
            CityData(4, "Damascus", 50, 200, 200000, 88, 10000000, 20000, 40000, 30000, 20000),
        ]
        
    def _create_mock_heroes(self) -> List[HeroData]:
        return [
            HeroData(1, "Queen", 100, 85, 754, 85, "Idle"),
            HeroData(2, "LeifEricson", 95, 70, 680, 90, "Idle"),
            HeroData(3, "NancyWard", 88, 90, 550, 75, "Mayor"),
            HeroData(4, "HenryIV", 92, 65, 720, 80, "Attacking"),
        ]
        
    def _create_mock_buildings(self) -> List[BuildingData]:
        buildings = []
        building_types = [
            (1, "Town Hall"), (2, "Cottage"), (3, "Barracks"), (4, "Academy"),
            (5, "Forge"), (6, "Workshop"), (7, "Relief Station"), (8, "Market"),
            (9, "Warehouse"), (10, "Embassy"), (11, "Rally Spot"), (12, "Beacon Tower"),
            (13, "Walls"), (14, "Feasting Hall"), (15, "Inn"),
        ]
        
        for i, (type_id, name) in enumerate(building_types):
            buildings.append(BuildingData(i, type_id, name, 10, i))
            
        return buildings
        
    def _create_menu(self):
        menubar = tk.Menu(self, bg=EvonyTheme.BG_DARK, fg=EvonyTheme.TEXT_PRIMARY)
        
        # Game menu
        game_menu = tk.Menu(menubar, tearoff=0, bg=EvonyTheme.BG_MEDIUM, fg=EvonyTheme.TEXT_PRIMARY)
        game_menu.add_command(label="Connect", command=self._on_connect)
        game_menu.add_command(label="Disconnect", command=self._on_disconnect)
        game_menu.add_separator()
        game_menu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="Game", menu=game_menu)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0, bg=EvonyTheme.BG_MEDIUM, fg=EvonyTheme.TEXT_PRIMARY)
        view_menu.add_command(label="City View", command=lambda: self._show_tab("city"))
        view_menu.add_command(label="Map View", command=lambda: self._show_tab("map"))
        view_menu.add_command(label="Reports", command=lambda: self._show_tab("reports"))
        menubar.add_cascade(label="View", menu=view_menu)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0, bg=EvonyTheme.BG_MEDIUM, fg=EvonyTheme.TEXT_PRIMARY)
        tools_menu.add_command(label="Calculator", command=self._show_calculator)
        tools_menu.add_command(label="Troop Simulator", command=self._show_troop_sim)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0, bg=EvonyTheme.BG_MEDIUM, fg=EvonyTheme.TEXT_PRIMARY)
        help_menu.add_command(label="About", command=self._show_about)
        menubar.add_cascade(label="Help", menu=help_menu)
        
        self.config(menu=menubar)
        
    def _create_main_layout(self):
        # Resource bar at top
        self._resource_bar = ResourceBar(self)
        self._resource_bar.pack(fill=tk.X, padx=5, pady=5)
        
        # City tabs
        self._city_tabs = CityTabs(self, on_city_change=self._on_city_change)
        self._city_tabs.pack(fill=tk.X, padx=5)
        
        # Main content area
        main_frame = tk.Frame(self, bg=EvonyTheme.BG_DARK)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left panel - Buildings + Heroes
        left_panel = tk.Frame(main_frame, bg=EvonyTheme.BG_PANEL, width=250)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5))
        left_panel.pack_propagate(False)
        
        self._building_panel = BuildingPanel(left_panel)
        self._building_panel.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        
        self._hero_panel = HeroPanel(left_panel)
        self._hero_panel.pack(fill=tk.BOTH, expand=True)
        
        # Center panel - Troops + Map
        center_panel = tk.Frame(main_frame, bg=EvonyTheme.BG_DARK)
        center_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Troop table
        self._troop_table = TroopTable(center_panel)
        self._troop_table.pack(fill=tk.X, pady=(0, 5))
        
        # Map view
        self._map_view = MapView(center_panel)
        self._map_view.pack(fill=tk.BOTH, expand=True)
        
        # Right panel - Chat
        right_panel = tk.Frame(main_frame, bg=EvonyTheme.BG_PANEL, width=300)
        right_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0))
        right_panel.pack_propagate(False)
        
        self._chat_panel = ChatPanel(right_panel)
        self._chat_panel.pack(fill=tk.BOTH, expand=True)
        
        # Bottom status bar
        status_bar = tk.Frame(self, bg=EvonyTheme.BG_MEDIUM)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        
        self._status_label = tk.Label(
            status_bar, text="Disconnected",
            bg=EvonyTheme.BG_MEDIUM, fg=EvonyTheme.TEXT_RED,
            font=EvonyTheme.FONT_SMALL
        )
        self._status_label.pack(side=tk.LEFT, padx=10, pady=2)
        
        self._server_label = tk.Label(
            status_bar, text="Server: --",
            bg=EvonyTheme.BG_MEDIUM, fg=EvonyTheme.TEXT_SECONDARY,
            font=EvonyTheme.FONT_SMALL
        )
        self._server_label.pack(side=tk.RIGHT, padx=10, pady=2)
        
    def _load_initial_data(self):
        self._city_tabs.set_cities(self._cities)
        self._troop_table.update_troops(self._troops)
        self._hero_panel.set_heroes(self._heroes)
        self._building_panel.set_buildings(self._buildings)
        
        if self._cities:
            city = self._cities[0]
            self._resource_bar.update_resources(
                city.gold, city.food, city.lumber, city.stone, city.iron,
                city.population, city.population + 100000
            )
            
    def _on_city_change(self, city_id: int):
        for city in self._cities:
            if city.id == city_id:
                self._resource_bar.update_resources(
                    city.gold, city.food, city.lumber, city.stone, city.iron,
                    city.population, city.population + 100000
                )
                break
                
    def _on_connect(self):
        self._status_label.config(text="Connected", fg=EvonyTheme.TEXT_GREEN)
        self._server_label.config(text="Server: cc2.evony.com")
        self._chat_panel.add_message("System", "Connected to server")
        
    def _on_disconnect(self):
        self._status_label.config(text="Disconnected", fg=EvonyTheme.TEXT_RED)
        self._server_label.config(text="Server: --")
        self._chat_panel.add_message("System", "Disconnected from server")
        
    def _show_tab(self, tab: str):
        pass
        
    def _show_calculator(self):
        pass
        
    def _show_troop_sim(self):
        pass
        
    def _show_about(self):
        messagebox.showinfo(
            "About",
            "Evony Client Recreation v1\n\n"
            "1:1 GUI recreation for testing purposes\n\n"
            "Part of Svony MCP Project"
        )


# =============================================================================
# ENTRY POINT
# =============================================================================

def main():
    app = EvonyClientGUI()
    app.mainloop()

if __name__ == "__main__":
    main()
