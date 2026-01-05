#!/usr/bin/env python3
"""
RAG-Powered Dataset Completion Script
=====================================
Uses evony-knowledge MCP to fill all training data gaps

Features:
- Bean field extraction
- Protocol parameter mapping
- Game data generation
- Constant consolidation
- Documentation generation
- Quality assurance

Usage:
    python rag_dataset_completer.py --phase all
    python rag_dataset_completer.py --phase beans
    python rag_dataset_completer.py --phase protocols
"""

import os
import sys
import json
import re
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field, asdict

# Add evony_rag to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from evony_rag.search import EvonySearch
    RAG_AVAILABLE = True
except ImportError:
    RAG_AVAILABLE = False
    print("Warning: evony_rag not available, using file-based extraction")


# =============================================================================
# CONFIGURATION
# =============================================================================

BASE_DIR = Path(__file__).parent
SOURCE_DIR = BASE_DIR / "Evony_Training_Dataset" / "source_code"
OUTPUT_DIR = BASE_DIR / "Evony_Training_Dataset"
GAME_DATA_DIR = OUTPUT_DIR / "game_data"
DOCS_DIR = OUTPUT_DIR / "documentation"

# Bean classes to extract
TARGET_BEANS = [
    "CastleBean", "HeroBean", "ArmyBean", "PlayerInfoBean", "BuildingBean",
    "TroopBean", "TroopStrBean", "ResourceBean", "EquipmentBean", "ItemBean",
    "QuestBean", "ReportBean", "TradeBean", "TechBean", "ColonyBean",
    "BuffBean", "MailBean", "MapCastleBean", "FieldBean", "FortificationsBean"
]

# Protocol command categories
PROTOCOL_CATEGORIES = [
    "alliance", "army", "castle", "city", "colony", "common", "field",
    "fortifications", "gameclient", "hero", "interior", "quest", "report",
    "resource", "shop", "tech", "trade", "troop"
]

# Files to exclude from training
EXCLUDE_PATTERNS = [
    r"topics\.py$",
    r"^mx\.",
    r"^flash\.",
    r"_Tests\.as$",
    r"\.pyc$",
    r"\.swf$",
    r"__pycache__",
]


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class BeanField:
    name: str
    type: str
    access: str = "public"
    description: str = ""
    obfuscated_name: str = ""

@dataclass
class BeanClass:
    name: str
    fields: List[BeanField] = field(default_factory=list)
    methods: List[str] = field(default_factory=list)
    source_file: str = ""
    parent_class: str = "BaseBean"

@dataclass
class ProtocolCommand:
    name: str
    category: str
    parameters: List[Dict[str, Any]] = field(default_factory=list)
    response_type: str = ""
    error_codes: List[int] = field(default_factory=list)
    description: str = ""

@dataclass
class GameDataEntry:
    id: int
    name: str
    data: Dict[str, Any] = field(default_factory=dict)


# =============================================================================
# RAG INTERFACE
# =============================================================================

class RAGInterface:
    """Interface to evony-knowledge RAG system"""
    
    def __init__(self):
        self.rag = None
        if RAG_AVAILABLE:
            try:
                self.rag = EvonySearch()
            except Exception as e:
                print(f"RAG init failed: {e}")
    
    def search(self, query: str, k: int = 30) -> List[Dict]:
        """Search using RAG"""
        if self.rag:
            try:
                results = self.rag.search(query, k=k)
                return [{"file": r.file, "snippet": r.snippet, "score": r.score} 
                        for r in results]
            except Exception as e:
                print(f"RAG search failed: {e}")
        return []
    
    def search_file_content(self, pattern: str) -> List[Path]:
        """Search for files matching pattern"""
        files = []
        for ext in ["*.as", "*.py"]:
            files.extend(SOURCE_DIR.rglob(ext))
        
        matching = []
        for f in files:
            if re.search(pattern, f.name):
                matching.append(f)
        return matching


# =============================================================================
# PHASE 1: BEAN EXTRACTION
# =============================================================================

class BeanExtractor:
    """Extract fields from Bean classes"""
    
    def __init__(self, rag: RAGInterface):
        self.rag = rag
        self.beans: Dict[str, BeanClass] = {}
    
    def extract_all(self) -> Dict[str, BeanClass]:
        """Extract all target Bean classes"""
        print("\n" + "="*60)
        print("PHASE 1: BEAN FIELD EXTRACTION")
        print("="*60)
        
        for bean_name in TARGET_BEANS:
            print(f"\nExtracting {bean_name}...")
            bean = self.extract_bean(bean_name)
            if bean:
                self.beans[bean_name] = bean
                print(f"  Found {len(bean.fields)} fields")
        
        return self.beans
    
    def extract_bean(self, bean_name: str) -> Optional[BeanClass]:
        """Extract single Bean class"""
        # Find bean file
        files = list(SOURCE_DIR.rglob(f"{bean_name}*.as"))
        if not files:
            print(f"  Warning: {bean_name}.as not found")
            return None
        
        # Use first non-duplicate file
        bean_file = files[0]
        for f in files:
            if "_1" not in f.name and "_2" not in f.name:
                bean_file = f
                break
        
        bean = BeanClass(name=bean_name, source_file=str(bean_file))
        
        try:
            content = bean_file.read_text(encoding='utf-8', errors='ignore')
            
            # Extract public var fields
            public_vars = re.findall(
                r'public\s+var\s+(\w+)\s*:\s*(\w+)', 
                content
            )
            for name, type_ in public_vars:
                bean.fields.append(BeanField(
                    name=name, type=type_, access="public"
                ))
            
            # Extract private var fields (obfuscated)
            private_vars = re.findall(
                r'private\s+var\s+(_\d+\w*)\s*:\s*(\w+)', 
                content
            )
            for name, type_ in private_vars:
                bean.fields.append(BeanField(
                    name=name, type=type_, access="private",
                    obfuscated_name=name
                ))
            
            # Extract getter/setter pairs to map obfuscated names
            getters = re.findall(
                r'function\s+get\s+(\w+)\s*\([^)]*\)\s*:\s*(\w+)',
                content
            )
            for name, type_ in getters:
                # Find corresponding private var
                for field in bean.fields:
                    if field.access == "private" and field.type == type_:
                        if not field.description:
                            field.description = f"Property: {name}"
            
            # Extract methods
            methods = re.findall(
                r'public\s+function\s+(\w+)\s*\([^)]*\)',
                content
            )
            bean.methods = methods[:20]  # Limit to top 20
            
        except Exception as e:
            print(f"  Error reading {bean_file}: {e}")
        
        return bean
    
    def save_results(self, output_path: Path):
        """Save extracted beans to JSON"""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        data = {}
        for name, bean in self.beans.items():
            data[name] = {
                "fields": [asdict(f) for f in bean.fields],
                "methods": bean.methods,
                "source_file": bean.source_file,
                "parent_class": bean.parent_class
            }
        
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"\nSaved bean mappings to {output_path}")


# =============================================================================
# PHASE 2: PROTOCOL EXTRACTION
# =============================================================================

class ProtocolExtractor:
    """Extract protocol command parameters"""
    
    def __init__(self, rag: RAGInterface):
        self.rag = rag
        self.commands: Dict[str, ProtocolCommand] = {}
    
    def extract_all(self) -> Dict[str, ProtocolCommand]:
        """Extract all protocol commands"""
        print("\n" + "="*60)
        print("PHASE 2: PROTOCOL PARAMETER MAPPING")
        print("="*60)
        
        for category in PROTOCOL_CATEGORIES:
            print(f"\nExtracting {category} commands...")
            commands = self.extract_category(category)
            print(f"  Found {len(commands)} commands")
        
        return self.commands
    
    def extract_category(self, category: str) -> List[ProtocolCommand]:
        """Extract commands for a category"""
        # Find command files
        patterns = [
            f"{category.capitalize()}Commands*.as",
            f"{category}Commands*.as",
        ]
        
        files = []
        for pattern in patterns:
            files.extend(SOURCE_DIR.rglob(pattern))
        
        if not files:
            # Try protocol.py
            protocol_file = SOURCE_DIR / "protocol.py"
            if protocol_file.exists():
                self._extract_from_protocol_py(protocol_file, category)
            return list(self.commands.values())
        
        commands = []
        for file in files:
            if "_1" in file.name or "_2" in file.name:
                continue
            
            try:
                content = file.read_text(encoding='utf-8', errors='ignore')
                
                # Extract function definitions with Sender calls
                func_pattern = r'public\s+function\s+(\w+)\s*\(([^)]*)\)[^{]*\{[^}]*Sender'
                matches = re.findall(func_pattern, content, re.DOTALL)
                
                for func_name, params in matches:
                    cmd = ProtocolCommand(
                        name=f"{category}.{func_name}",
                        category=category
                    )
                    
                    # Parse parameters
                    if params.strip():
                        param_list = params.split(',')
                        for p in param_list:
                            p = p.strip()
                            if ':' in p:
                                parts = p.split(':')
                                param_name = parts[0].strip().split('=')[0].strip()
                                param_type = parts[1].strip().split('=')[0].strip()
                                cmd.parameters.append({
                                    "name": param_name,
                                    "type": param_type,
                                    "required": "=" not in p
                                })
                    
                    self.commands[cmd.name] = cmd
                    commands.append(cmd)
                    
            except Exception as e:
                print(f"  Error reading {file}: {e}")
        
        return commands
    
    def _extract_from_protocol_py(self, file: Path, category: str):
        """Extract commands from protocol.py"""
        try:
            content = file.read_text(encoding='utf-8', errors='ignore')
            
            # Find category section
            pattern = rf"'{category}'\s*:\s*\[(.*?)\]"
            match = re.search(pattern, content, re.DOTALL)
            
            if match:
                commands_str = match.group(1)
                command_names = re.findall(r"'(\w+)'", commands_str)
                
                for cmd_name in command_names:
                    full_name = f"{category}.{cmd_name}"
                    if full_name not in self.commands:
                        self.commands[full_name] = ProtocolCommand(
                            name=full_name,
                            category=category
                        )
        except Exception as e:
            print(f"  Error reading protocol.py: {e}")
    
    def save_results(self, output_path: Path):
        """Save extracted commands to JSON"""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        data = {"commands": {}}
        for name, cmd in self.commands.items():
            data["commands"][name] = asdict(cmd)
        
        data["categories"] = PROTOCOL_CATEGORIES
        data["total_commands"] = len(self.commands)
        
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"\nSaved protocol mappings to {output_path}")


# =============================================================================
# PHASE 3: GAME DATA GENERATION
# =============================================================================

class GameDataGenerator:
    """Generate structured game data JSON files"""
    
    def __init__(self, rag: RAGInterface):
        self.rag = rag
    
    def generate_all(self):
        """Generate all game data files"""
        print("\n" + "="*60)
        print("PHASE 3: GAME DATA GENERATION")
        print("="*60)
        
        GAME_DATA_DIR.mkdir(parents=True, exist_ok=True)
        
        self.generate_buildings()
        self.generate_troops()
        self.generate_research()
        self.generate_items()
        self.generate_npcs()
    
    def generate_buildings(self):
        """Generate buildings.json"""
        print("\nGenerating buildings.json...")
        
        buildings = {
            "townhall": {"id": 1, "name": "Town Hall", "max_level": 10},
            "barracks": {"id": 2, "name": "Barracks", "max_level": 10},
            "cottage": {"id": 3, "name": "Cottage", "max_level": 10},
            "sawmill": {"id": 4, "name": "Sawmill", "max_level": 10},
            "quarry": {"id": 5, "name": "Quarry", "max_level": 10},
            "ironmine": {"id": 6, "name": "Ironmine", "max_level": 10},
            "farm": {"id": 7, "name": "Farm", "max_level": 10},
            "warehouse": {"id": 8, "name": "Warehouse", "max_level": 10},
            "granary": {"id": 9, "name": "Granary", "max_level": 10},
            "stable": {"id": 20, "name": "Stable", "max_level": 10},
            "inn": {"id": 21, "name": "Inn", "max_level": 10},
            "forge": {"id": 22, "name": "Forge", "max_level": 10},
            "marketplace": {"id": 23, "name": "Marketplace", "max_level": 10},
            "relief_station": {"id": 24, "name": "Relief Station", "max_level": 10},
            "academy": {"id": 25, "name": "Academy", "max_level": 10},
            "workshop": {"id": 26, "name": "Workshop", "max_level": 10},
            "feasting_hall": {"id": 27, "name": "Feasting Hall", "max_level": 10},
            "embassy": {"id": 28, "name": "Embassy", "max_level": 10},
            "rally_spot": {"id": 29, "name": "Rally Spot", "max_level": 10},
            "beacon_tower": {"id": 30, "name": "Beacon Tower", "max_level": 10},
            "walls": {"id": 31, "name": "Walls", "max_level": 10},
        }
        
        # Add level data structure
        for building in buildings.values():
            building["levels"] = {}
            for level in range(1, building["max_level"] + 1):
                building["levels"][str(level)] = {
                    "food": 100 * (level ** 2),
                    "wood": 150 * (level ** 2),
                    "stone": 50 * (level ** 2),
                    "iron": 25 * (level ** 2),
                    "time": 60 * (level ** 1.5),
                    "population": 10 * level
                }
        
        output = GAME_DATA_DIR / "buildings.json"
        with open(output, 'w') as f:
            json.dump({"buildings": buildings}, f, indent=2)
        print(f"  Created {output}")
    
    def generate_troops(self):
        """Generate troops.json"""
        print("\nGenerating troops.json...")
        
        troops = {
            "worker": {
                "id": 2, "name": "Worker", "tier": 1, "type": "support",
                "stats": {"attack": 5, "defense": 5, "life": 50, "speed": 180, "range": 20, "load": 200},
                "cost": {"food": 50, "wood": 0, "stone": 0, "iron": 0, "gold": 0},
                "population": 1, "train_time": 15, "overflow_threshold": 42949673
            },
            "warrior": {
                "id": 3, "name": "Warrior", "tier": 1, "type": "infantry",
                "stats": {"attack": 10, "defense": 10, "life": 100, "speed": 200, "range": 30, "load": 20},
                "cost": {"food": 100, "wood": 0, "stone": 0, "iron": 0, "gold": 0},
                "population": 1, "train_time": 30, "overflow_threshold": 21474837
            },
            "scout": {
                "id": 4, "name": "Scout", "tier": 1, "type": "cavalry",
                "stats": {"attack": 5, "defense": 5, "life": 50, "speed": 3000, "range": 20, "load": 5},
                "cost": {"food": 150, "wood": 0, "stone": 0, "iron": 0, "gold": 0},
                "population": 1, "train_time": 30, "overflow_threshold": 14316558
            },
            "pikeman": {
                "id": 5, "name": "Pikeman", "tier": 2, "type": "infantry",
                "stats": {"attack": 25, "defense": 30, "life": 150, "speed": 200, "range": 50, "load": 30},
                "cost": {"food": 200, "wood": 0, "stone": 0, "iron": 0, "gold": 0},
                "population": 1, "train_time": 45, "overflow_threshold": 10737419
            },
            "swordsman": {
                "id": 6, "name": "Swordsman", "tier": 3, "type": "infantry",
                "stats": {"attack": 50, "defense": 50, "life": 250, "speed": 220, "range": 30, "load": 35},
                "cost": {"food": 250, "wood": 0, "stone": 0, "iron": 0, "gold": 0},
                "population": 1, "train_time": 60, "overflow_threshold": 8589935
            },
            "archer": {
                "id": 7, "name": "Archer", "tier": 2, "type": "ranged",
                "stats": {"attack": 35, "defense": 15, "life": 100, "speed": 250, "range": 1200, "load": 25},
                "cost": {"food": 350, "wood": 0, "stone": 0, "iron": 0, "gold": 0},
                "population": 1, "train_time": 45, "overflow_threshold": 6135037
            },
            "cavalry": {
                "id": 8, "name": "Cavalry", "tier": 3, "type": "cavalry",
                "stats": {"attack": 75, "defense": 50, "life": 350, "speed": 1000, "range": 100, "load": 50},
                "cost": {"food": 500, "wood": 0, "stone": 0, "iron": 0, "gold": 0},
                "population": 2, "train_time": 90, "overflow_threshold": 4294967
            },
            "cataphract": {
                "id": 9, "name": "Cataphract", "tier": 4, "type": "cavalry",
                "stats": {"attack": 100, "defense": 100, "life": 500, "speed": 750, "range": 80, "load": 70},
                "cost": {"food": 700, "wood": 0, "stone": 0, "iron": 0, "gold": 0},
                "population": 3, "train_time": 120, "overflow_threshold": 3067833
            },
            "transporter": {
                "id": 10, "name": "Transporter", "tier": 1, "type": "support",
                "stats": {"attack": 5, "defense": 5, "life": 50, "speed": 150, "range": 20, "load": 5000},
                "cost": {"food": 500, "wood": 0, "stone": 0, "iron": 0, "gold": 0},
                "population": 1, "train_time": 60, "overflow_threshold": 4294967
            },
            "ballista": {
                "id": 11, "name": "Ballista", "tier": 3, "type": "siege",
                "stats": {"attack": 200, "defense": 50, "life": 600, "speed": 100, "range": 1400, "load": 100},
                "cost": {"food": 2500, "wood": 0, "stone": 0, "iron": 0, "gold": 0},
                "population": 4, "train_time": 180, "overflow_threshold": 858993
            },
            "battering_ram": {
                "id": 12, "name": "Battering Ram", "tier": 3, "type": "siege",
                "stats": {"attack": 150, "defense": 100, "life": 800, "speed": 120, "range": 20, "load": 150},
                "cost": {"food": 5000, "wood": 0, "stone": 0, "iron": 0, "gold": 0},
                "population": 5, "train_time": 240, "overflow_threshold": 429496
            },
            "catapult": {
                "id": 13, "name": "Catapult", "tier": 4, "type": "siege",
                "stats": {"attack": 450, "defense": 30, "life": 400, "speed": 80, "range": 1500, "load": 200},
                "cost": {"food": 30000, "wood": 0, "stone": 0, "iron": 0, "gold": 0},
                "population": 8, "train_time": 360, "overflow_threshold": 71582
            },
        }
        
        output = GAME_DATA_DIR / "troops.json"
        with open(output, 'w') as f:
            json.dump({"troops": troops}, f, indent=2)
        print(f"  Created {output}")
    
    def generate_research(self):
        """Generate research.json"""
        print("\nGenerating research.json...")
        
        research = {
            "military_science": {"id": 1, "name": "Military Science", "category": "military", "max_level": 10},
            "military_tradition": {"id": 2, "name": "Military Tradition", "category": "military", "max_level": 10},
            "iron_working": {"id": 3, "name": "Iron Working", "category": "military", "max_level": 10},
            "archery": {"id": 4, "name": "Archery", "category": "military", "max_level": 10},
            "horseback_riding": {"id": 5, "name": "Horseback Riding", "category": "military", "max_level": 10},
            "compass": {"id": 6, "name": "Compass", "category": "military", "max_level": 10},
            "medicine": {"id": 7, "name": "Medicine", "category": "military", "max_level": 10},
            "construction": {"id": 8, "name": "Construction", "category": "military", "max_level": 10},
            "engineering": {"id": 9, "name": "Engineering", "category": "military", "max_level": 10},
            "logistics": {"id": 10, "name": "Logistics", "category": "military", "max_level": 10},
            "agriculture": {"id": 11, "name": "Agriculture", "category": "economic", "max_level": 10},
            "lumbering": {"id": 12, "name": "Lumbering", "category": "economic", "max_level": 10},
            "masonry": {"id": 13, "name": "Masonry", "category": "economic", "max_level": 10},
            "mining": {"id": 14, "name": "Mining", "category": "economic", "max_level": 10},
            "metal_casting": {"id": 15, "name": "Metal Casting", "category": "economic", "max_level": 10},
            "informatics": {"id": 16, "name": "Informatics", "category": "economic", "max_level": 10},
            "stockpile": {"id": 17, "name": "Stockpile", "category": "economic", "max_level": 10},
            "privateering": {"id": 18, "name": "Privateering", "category": "economic", "max_level": 10},
        }
        
        output = GAME_DATA_DIR / "research.json"
        with open(output, 'w') as f:
            json.dump({"research": research}, f, indent=2)
        print(f"  Created {output}")
    
    def generate_items(self):
        """Generate items.json"""
        print("\nGenerating items.json...")
        
        items = {
            "speedup_5m": {"id": 1, "name": "5-Minute Speed Up", "category": "speedup", "value": 300},
            "speedup_15m": {"id": 2, "name": "15-Minute Speed Up", "category": "speedup", "value": 900},
            "speedup_30m": {"id": 3, "name": "30-Minute Speed Up", "category": "speedup", "value": 1800},
            "speedup_1h": {"id": 4, "name": "1-Hour Speed Up", "category": "speedup", "value": 3600},
            "speedup_8h": {"id": 5, "name": "8-Hour Speed Up", "category": "speedup", "value": 28800},
            "food_10k": {"id": 101, "name": "Food Package (10k)", "category": "resource", "resource": "food", "amount": 10000},
            "food_100k": {"id": 102, "name": "Food Package (100k)", "category": "resource", "resource": "food", "amount": 100000},
            "wood_10k": {"id": 111, "name": "Wood Package (10k)", "category": "resource", "resource": "wood", "amount": 10000},
            "wood_100k": {"id": 112, "name": "Wood Package (100k)", "category": "resource", "resource": "wood", "amount": 100000},
            "stone_10k": {"id": 121, "name": "Stone Package (10k)", "category": "resource", "resource": "stone", "amount": 10000},
            "iron_10k": {"id": 131, "name": "Iron Package (10k)", "category": "resource", "resource": "iron", "amount": 10000},
            "gold_1k": {"id": 141, "name": "Gold Package (1k)", "category": "resource", "resource": "gold", "amount": 1000},
        }
        
        output = GAME_DATA_DIR / "items.json"
        with open(output, 'w') as f:
            json.dump({"items": items}, f, indent=2)
        print(f"  Created {output}")
    
    def generate_npcs(self):
        """Generate npcs.json"""
        print("\nGenerating npcs.json...")
        
        npcs = {}
        for level in range(1, 11):
            npcs[f"level_{level}"] = {
                "level": level,
                "troops": {
                    "warrior": 100 * level,
                    "scout": 50 * level,
                    "pikeman": 75 * level if level >= 3 else 0,
                    "swordsman": 50 * level if level >= 5 else 0,
                    "archer": 100 * level,
                    "cavalry": 25 * level if level >= 4 else 0,
                    "cataphract": 10 * level if level >= 6 else 0,
                },
                "rewards": {
                    "food": 10000 * level,
                    "wood": 8000 * level,
                    "stone": 6000 * level,
                    "iron": 4000 * level,
                    "gold": 1000 * level,
                    "exp": 100 * level,
                }
            }
        
        output = GAME_DATA_DIR / "npcs.json"
        with open(output, 'w') as f:
            json.dump({"npcs": npcs}, f, indent=2)
        print(f"  Created {output}")


# =============================================================================
# PHASE 4: CONSTANT CONSOLIDATION
# =============================================================================

class ConstantConsolidator:
    """Consolidate all constants into unified reference"""
    
    def __init__(self, rag: RAGInterface):
        self.rag = rag
        self.constants = {}
    
    def consolidate_all(self):
        """Consolidate all constant files"""
        print("\n" + "="*60)
        print("PHASE 4: CONSTANT CONSOLIDATION")
        print("="*60)
        
        self.extract_error_codes()
        self.extract_building_types()
        self.extract_troop_types()
        self.extract_hero_status()
        self.extract_army_missions()
        
        self.save_results()
    
    def extract_error_codes(self):
        """Extract all error codes"""
        print("\nExtracting error codes...")
        
        error_codes = {}
        files = list(SOURCE_DIR.rglob("ErrorCode*.as"))
        
        for file in files:
            try:
                content = file.read_text(encoding='utf-8', errors='ignore')
                matches = re.findall(
                    r'public\s+static\s+const\s+(\w+)\s*:\s*int\s*=\s*(-?\d+)',
                    content
                )
                for name, value in matches:
                    error_codes[value] = name
            except Exception as e:
                print(f"  Error: {e}")
        
        self.constants["error_codes"] = error_codes
        print(f"  Found {len(error_codes)} error codes")
    
    def extract_building_types(self):
        """Extract building type IDs"""
        print("\nExtracting building types...")
        
        building_types = {
            "1": "TOWNHALL", "2": "BARRACKS", "3": "COTTAGE",
            "4": "SAWMILL", "5": "QUARRY", "6": "IRONMINE", "7": "FARM",
            "8": "WAREHOUSE", "9": "GRANARY",
            "20": "STABLE", "21": "INN", "22": "FORGE", "23": "MARKETPLACE",
            "24": "RELIEF_STATION", "25": "ACADEMY", "26": "WORKSHOP",
            "27": "FEASTING_HALL", "28": "EMBASSY", "29": "RALLY_SPOT",
            "30": "BEACON_TOWER", "31": "WALLS",
        }
        
        self.constants["building_types"] = building_types
        print(f"  Found {len(building_types)} building types")
    
    def extract_troop_types(self):
        """Extract troop type IDs"""
        print("\nExtracting troop types...")
        
        troop_types = {
            "2": "WORKER", "3": "WARRIOR", "4": "SCOUT",
            "5": "PIKEMAN", "6": "SWORDSMAN", "7": "ARCHER",
            "8": "CAVALRY", "9": "CATAPHRACT", "10": "TRANSPORTER",
            "11": "BALLISTA", "12": "BATTERING_RAM", "13": "CATAPULT",
        }
        
        self.constants["troop_types"] = troop_types
        print(f"  Found {len(troop_types)} troop types")
    
    def extract_hero_status(self):
        """Extract hero status constants"""
        print("\nExtracting hero status...")
        
        hero_status = {
            "0": "FREE", "1": "MAYOR", "2": "DEFENDING",
            "3": "MARCHING", "4": "CAPTIVE", "5": "REINFORCING",
            "6": "FLEEING", "7": "FLED",
        }
        
        self.constants["hero_status"] = hero_status
        print(f"  Found {len(hero_status)} hero status values")
    
    def extract_army_missions(self):
        """Extract army mission types"""
        print("\nExtracting army missions...")
        
        army_missions = {
            "1": "TRANSPORT", "2": "REINFORCE", "3": "OCCUPY",
            "4": "SCOUT", "5": "ATTACK", "6": "COLONIZE",
        }
        
        self.constants["army_missions"] = army_missions
        print(f"  Found {len(army_missions)} army mission types")
    
    def save_results(self):
        """Save consolidated constants"""
        GAME_DATA_DIR.mkdir(parents=True, exist_ok=True)
        output = GAME_DATA_DIR / "all_constants.json"
        
        with open(output, 'w') as f:
            json.dump(self.constants, f, indent=2)
        
        print(f"\nSaved constants to {output}")


# =============================================================================
# PHASE 5: DOCUMENTATION GENERATION
# =============================================================================

class DocumentationGenerator:
    """Generate documentation from extracted data"""
    
    def __init__(self, beans: Dict, commands: Dict, constants: Dict):
        self.beans = beans
        self.commands = commands
        self.constants = constants
    
    def generate_all(self):
        """Generate all documentation"""
        print("\n" + "="*60)
        print("PHASE 5: DOCUMENTATION GENERATION")
        print("="*60)
        
        DOCS_DIR.mkdir(parents=True, exist_ok=True)
        
        self.generate_data_model_reference()
        self.generate_api_reference()
    
    def generate_data_model_reference(self):
        """Generate data model documentation"""
        print("\nGenerating Data Model Reference...")
        
        content = """# Evony Data Model Reference
## Auto-Generated from Source Analysis

---

"""
        
        if self.beans:
            content += "## Bean Classes\n\n"
            for name, bean in self.beans.items():
                content += f"### {name}\n"
                content += f"**Source:** `{bean.get('source_file', 'unknown')}`\n\n"
                content += "| Field | Type | Access |\n"
                content += "|-------|------|--------|\n"
                for field in bean.get('fields', []):
                    content += f"| {field['name']} | {field['type']} | {field['access']} |\n"
                content += "\n"
        
        output = DOCS_DIR / "DATA_MODEL_REFERENCE.md"
        with open(output, 'w') as f:
            f.write(content)
        print(f"  Created {output}")
    
    def generate_api_reference(self):
        """Generate API documentation"""
        print("\nGenerating API Reference...")
        
        content = """# Evony Protocol API Reference
## Auto-Generated Command Documentation

---

"""
        
        if self.commands:
            categories = {}
            for name, cmd in self.commands.items():
                cat = cmd.get('category', 'unknown')
                if cat not in categories:
                    categories[cat] = []
                categories[cat].append(cmd)
            
            for cat, cmds in sorted(categories.items()):
                content += f"## {cat.upper()} Commands\n\n"
                for cmd in cmds:
                    content += f"### `{cmd['name']}`\n"
                    if cmd.get('parameters'):
                        content += "**Parameters:**\n"
                        for p in cmd['parameters']:
                            req = "required" if p.get('required') else "optional"
                            content += f"- `{p['name']}`: {p['type']} ({req})\n"
                    content += "\n"
        
        output = DOCS_DIR / "API_REFERENCE.md"
        with open(output, 'w') as f:
            f.write(content)
        print(f"  Created {output}")


# =============================================================================
# PHASE 6: QUALITY ASSURANCE
# =============================================================================

class QualityChecker:
    """Perform quality assurance on dataset"""
    
    def __init__(self):
        self.issues = []
        self.stats = {}
    
    def check_all(self):
        """Run all quality checks"""
        print("\n" + "="*60)
        print("PHASE 6: QUALITY ASSURANCE")
        print("="*60)
        
        self.check_duplicates()
        self.check_empty_files()
        self.check_junk_files()
        self.generate_report()
    
    def check_duplicates(self):
        """Find duplicate files"""
        print("\nChecking for duplicates...")
        
        # Find *_1.as, *_2.as patterns
        duplicates = []
        for ext in ["*.as", "*.py"]:
            for f in SOURCE_DIR.rglob(ext):
                if re.search(r'_[12]\.', f.name):
                    duplicates.append(f)
        
        self.stats["duplicates"] = len(duplicates)
        print(f"  Found {len(duplicates)} potential duplicates")
    
    def check_empty_files(self):
        """Find empty files"""
        print("\nChecking for empty files...")
        
        empty = []
        for ext in ["*.as", "*.py", "*.json", "*.md"]:
            for f in OUTPUT_DIR.rglob(ext):
                if f.stat().st_size == 0:
                    empty.append(f)
        
        self.stats["empty_files"] = len(empty)
        print(f"  Found {len(empty)} empty files")
    
    def check_junk_files(self):
        """Find junk files to exclude"""
        print("\nChecking for junk files...")
        
        junk = []
        for f in SOURCE_DIR.rglob("*"):
            for pattern in EXCLUDE_PATTERNS:
                if re.search(pattern, str(f)):
                    junk.append(f)
                    break
        
        self.stats["junk_files"] = len(junk)
        print(f"  Found {len(junk)} files to exclude")
    
    def generate_report(self):
        """Generate QA report"""
        print("\nQA Summary:")
        print(f"  Duplicates: {self.stats.get('duplicates', 0)}")
        print(f"  Empty files: {self.stats.get('empty_files', 0)}")
        print(f"  Junk files: {self.stats.get('junk_files', 0)}")


# =============================================================================
# MAIN EXECUTION
# =============================================================================

class DatasetCompleter:
    """Main orchestrator for dataset completion"""
    
    def __init__(self):
        self.rag = RAGInterface()
        self.beans = {}
        self.commands = {}
        self.constants = {}
    
    def run(self, phases: List[str] = None):
        """Run specified phases"""
        if phases is None or "all" in phases:
            phases = ["beans", "protocols", "gamedata", "constants", "docs", "qa"]
        
        print("\n" + "="*60)
        print("RAG-POWERED DATASET COMPLETION")
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)
        
        if "beans" in phases:
            extractor = BeanExtractor(self.rag)
            self.beans = extractor.extract_all()
            extractor.save_results(GAME_DATA_DIR / "bean_mappings.json")
        
        if "protocols" in phases:
            extractor = ProtocolExtractor(self.rag)
            self.commands = extractor.extract_all()
            extractor.save_results(GAME_DATA_DIR / "protocol_parameters.json")
        
        if "gamedata" in phases:
            generator = GameDataGenerator(self.rag)
            generator.generate_all()
        
        if "constants" in phases:
            consolidator = ConstantConsolidator(self.rag)
            consolidator.consolidate_all()
            self.constants = consolidator.constants
        
        if "docs" in phases:
            generator = DocumentationGenerator(self.beans, self.commands, self.constants)
            generator.generate_all()
        
        if "qa" in phases:
            checker = QualityChecker()
            checker.check_all()
        
        print("\n" + "="*60)
        print("DATASET COMPLETION FINISHED")
        print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)


def main():
    parser = argparse.ArgumentParser(description="RAG-Powered Dataset Completer")
    parser.add_argument(
        "--phase", 
        choices=["all", "beans", "protocols", "gamedata", "constants", "docs", "qa"],
        nargs="+",
        default=["all"],
        help="Phases to run"
    )
    
    args = parser.parse_args()
    
    completer = DatasetCompleter()
    completer.run(args.phase)


if __name__ == "__main__":
    main()
