"""
颜色自定义系统模块
允许玩家自定义游戏元素的颜色
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum
import colorsys


class ColorCategory(Enum):
    BUILDING = "building"
    FURNITURE = "furniture"
    FENCE = "fence"
    CLOTHING = "clothing"
    CROP = "crop"
    ANIMAL = "animal"
    UI = "ui"


@dataclass
class ColorPalette:
    name: str
    primary: str
    secondary: str
    accent: str
    background: str
    text: str
    
    def get_all_colors(self) -> Dict[str, str]:
        return {
            "primary": self.primary,
            "secondary": self.secondary,
            "accent": self.accent,
            "background": self.background,
            "text": self.text
        }


@dataclass
class CustomColor:
    color_id: str
    name: str
    hex_value: str
    rgb_value: Tuple[int, int, int]
    category: ColorCategory
    is_unlocked: bool = True
    unlock_level: int = 1
    price: int = 0
    
    def get_display_name(self) -> str:
        return f"{self.name}"
    
    def get_preview_emoji(self) -> str:
        return "🎨"


class ColorRegistry:
    
    DEFAULT_COLORS = {
        "red": CustomColor("red", "红色", "#FF0000", (255, 0, 0), ColorCategory.BUILDING),
        "blue": CustomColor("blue", "蓝色", "#0000FF", (0, 0, 255), ColorCategory.BUILDING),
        "green": CustomColor("green", "绿色", "#00FF00", (0, 255, 0), ColorCategory.BUILDING),
        "yellow": CustomColor("yellow", "黄色", "#FFFF00", (255, 255, 0), ColorCategory.BUILDING),
        "orange": CustomColor("orange", "橙色", "#FFA500", (255, 165, 0), ColorCategory.BUILDING),
        "purple": CustomColor("purple", "紫色", "#800080", (128, 0, 128), ColorCategory.BUILDING),
        "pink": CustomColor("pink", "粉色", "#FFC0CB", (255, 192, 203), ColorCategory.CLOTHING),
        "cyan": CustomColor("cyan", "青色", "#00FFFF", (0, 255, 255), ColorCategory.BUILDING),
        "brown": CustomColor("brown", "棕色", "#8B4513", (139, 69, 19), ColorCategory.FURNITURE),
        "gray": CustomColor("gray", "灰色", "#808080", (128, 128, 128), ColorCategory.BUILDING),
        "white": CustomColor("white", "白色", "#FFFFFF", (255, 255, 255), ColorCategory.CLOTHING),
        "black": CustomColor("black", "黑色", "#000000", (0, 0, 0), ColorCategory.CLOTHING),
        "gold": CustomColor("gold", "金色", "#FFD700", (255, 215, 0), ColorCategory.UI, unlock_level=5),
        "silver": CustomColor("silver", "银色", "#C0C0C0", (192, 192, 192), ColorCategory.UI, unlock_level=3),
        "bronze": CustomColor("bronze", "铜色", "#CD7F32", (205, 127, 50), ColorCategory.UI, unlock_level=4),
    }
    
    SPECIAL_COLORS = {
        "rainbow": CustomColor("rainbow", "彩虹", "#FF0000", (255, 0, 0), ColorCategory.UI, unlock_level=10, price=5000),
        "neon_green": CustomColor("neon_green", "霓虹绿", "#39FF14", (57, 255, 20), ColorCategory.BUILDING, unlock_level=7, price=2000),
        "neon_pink": CustomColor("neon_pink", "霓虹粉", "#FF10F0", (255, 16, 240), ColorCategory.CLOTHING, unlock_level=7, price=2000),
        "pastel_blue": CustomColor("pastel_blue", "淡蓝", "#ADD8E6", (173, 216, 230), ColorCategory.BUILDING, unlock_level=6, price=1500),
        "pastel_pink": CustomColor("pastel_pink", "淡粉", "#FFD1DC", (255, 209, 220), ColorCategory.CLOTHING, unlock_level=6, price=1500),
        "forest_green": CustomColor("forest_green", "森林绿", "#228B22", (34, 139, 34), ColorCategory.FENCE, unlock_level=5, price=1000),
        "ocean_blue": CustomColor("ocean_blue", "海洋蓝", "#006994", (0, 105, 148), ColorCategory.BUILDING, unlock_level=5, price=1000),
        "sunset_orange": CustomColor("sunset_orange", "日落橙", "#FD5E53", (253, 94, 83), ColorCategory.BUILDING, unlock_level=8, price=2500),
        "midnight_purple": CustomColor("midnight_purple", "午夜紫", "#280137", (40, 1, 55), ColorCategory.BUILDING, unlock_level=9, price=3000),
        "cherry_blossom": CustomColor("cherry_blossom", "樱花粉", "#FFB7C5", (255, 183, 197), ColorCategory.CLOTHING, unlock_level=8, price=2500),
    }
    
    PRESET_PALETTES = {
        "nature": ColorPalette(
            name="自然",
            primary="#228B22",
            secondary="#8B4513",
            accent="#FFD700",
            background="#F5F5DC",
            text="#2F4F4F"
        ),
        "ocean": ColorPalette(
            name="海洋",
            primary="#006994",
            secondary="#40E0D0",
            accent="#FFD700",
            background="#E0FFFF",
            text="#000080"
        ),
        "sunset": ColorPalette(
            name="日落",
            primary="#FF6347",
            secondary="#FFD700",
            accent="#FF4500",
            background="#FFF8DC",
            text="#8B0000"
        ),
        "forest": ColorPalette(
            name="森林",
            primary="#2E8B57",
            secondary="#556B2F",
            accent="#8FBC8F",
            background="#F0FFF0",
            text="#006400"
        ),
        "royal": ColorPalette(
            name="皇家",
            primary="#4169E1",
            secondary="#FFD700",
            accent="#800080",
            background="#F8F8FF",
            text="#191970"
        ),
        "cherry": ColorPalette(
            name="樱花",
            primary="#FFB7C5",
            secondary="#FF69B4",
            accent="#FFD700",
            background="#FFF0F5",
            text="#C71585"
        ),
        "midnight": ColorPalette(
            name="午夜",
            primary="#191970",
            secondary="#4B0082",
            accent="#9400D3",
            background="#1A1A2E",
            text="#E6E6FA"
        ),
        "autumn": ColorPalette(
            name="秋天",
            primary="#D2691E",
            secondary="#FF8C00",
            accent="#FFD700",
            background="#FAFAD2",
            text="#8B4513"
        ),
    }
    
    @classmethod
    def get_color(cls, color_id: str) -> Optional[CustomColor]:
        if color_id in cls.DEFAULT_COLORS:
            return cls.DEFAULT_COLORS[color_id]
        return cls.SPECIAL_COLORS.get(color_id)
    
    @classmethod
    def get_all_colors(cls) -> Dict[str, CustomColor]:
        all_colors = cls.DEFAULT_COLORS.copy()
        all_colors.update(cls.SPECIAL_COLORS)
        return all_colors
    
    @classmethod
    def get_colors_by_category(cls, category: ColorCategory) -> List[CustomColor]:
        return [c for c in cls.get_all_colors().values() if c.category == category]
    
    @classmethod
    def get_palette(cls, palette_name: str) -> Optional[ColorPalette]:
        return cls.PRESET_PALETTES.get(palette_name)
    
    @classmethod
    def get_all_palettes(cls) -> Dict[str, ColorPalette]:
        return cls.PRESET_PALETTES.copy()
    
    @classmethod
    def get_unlocked_colors(cls, player_level: int) -> List[CustomColor]:
        result = []
        for color in cls.get_all_colors().values():
            if player_level >= color.unlock_level:
                result.append(color)
        return result


class ColorCustomizationSystem:
    
    def __init__(self):
        self.applied_colors: Dict[str, str] = {}
        self.owned_colors: List[str] = list(ColorRegistry.DEFAULT_COLORS.keys())
        self.current_palette: Optional[str] = None
        self.custom_palettes: Dict[str, ColorPalette] = {}
    
    def apply_color(self, target: str, color_id: str) -> Tuple[bool, str]:
        color = ColorRegistry.get_color(color_id)
        if not color:
            return False, "未知的颜色"
        
        if color_id not in self.owned_colors:
            return False, "你还没有解锁这个颜色"
        
        self.applied_colors[target] = color_id
        return True, f"成功将 {target} 的颜色改为 {color.name}"
    
    def purchase_color(self, color_id: str, player_money: int) -> Tuple[bool, str, int]:
        color = ColorRegistry.get_color(color_id)
        if not color:
            return False, "未知的颜色", 0
        
        if color_id in self.owned_colors:
            return False, "你已经拥有这个颜色了", 0
        
        if color.price > player_money:
            return False, f"金币不足，需要 {color.price} 金币", 0
        
        self.owned_colors.append(color_id)
        return True, f"成功购买 {color.name}！", color.price
    
    def apply_palette(self, palette_name: str) -> Tuple[bool, str]:
        palette = ColorRegistry.get_palette(palette_name)
        if not palette:
            palette = self.custom_palettes.get(palette_name)
        
        if not palette:
            return False, "未知的调色板"
        
        self.current_palette = palette_name
        self.applied_colors["primary"] = palette.primary
        self.applied_colors["secondary"] = palette.secondary
        self.applied_colors["accent"] = palette.accent
        self.applied_colors["background"] = palette.background
        self.applied_colors["text"] = palette.text
        
        return True, f"成功应用 {palette.name} 调色板"
    
    def create_custom_palette(self, name: str, primary: str, secondary: str, 
                              accent: str, background: str, text: str) -> Tuple[bool, str]:
        if not self._is_valid_hex_color(primary):
            return False, "主色格式无效"
        
        palette = ColorPalette(
            name=name,
            primary=primary,
            secondary=secondary,
            accent=accent,
            background=background,
            text=text
        )
        
        self.custom_palettes[name] = palette
        return True, f"成功创建自定义调色板 {name}"
    
    def _is_valid_hex_color(self, color: str) -> bool:
        if not color.startswith('#'):
            return False
        if len(color) != 7:
            return False
        try:
            int(color[1:], 16)
            return True
        except ValueError:
            return False
    
    def get_color_for_target(self, target: str) -> str:
        color_id = self.applied_colors.get(target)
        if color_id:
            color = ColorRegistry.get_color(color_id)
            if color:
                return color.hex_value
        return "#FFFFFF"
    
    def get_current_theme(self) -> Dict[str, str]:
        if self.current_palette:
            palette = ColorRegistry.get_palette(self.current_palette)
            if palette:
                return palette.get_all_colors()
            palette = self.custom_palettes.get(self.current_palette)
            if palette:
                return palette.get_all_colors()
        
        return {
            "primary": self.get_color_for_target("primary") or "#4CAF50",
            "secondary": self.get_color_for_target("secondary") or "#2196F3",
            "accent": self.get_color_for_target("accent") or "#FF9800",
            "background": self.get_color_for_target("background") or "#FFFFFF",
            "text": self.get_color_for_target("text") or "#333333"
        }
    
    def get_owned_colors(self) -> List[CustomColor]:
        return [ColorRegistry.get_color(cid) for cid in self.owned_colors if ColorRegistry.get_color(cid)]
    
    def unlock_color_by_level(self, player_level: int) -> List[str]:
        newly_unlocked = []
        for color_id, color in ColorRegistry.get_all_colors().items():
            if color_id not in self.owned_colors and player_level >= color.unlock_level and color.price == 0:
                self.owned_colors.append(color_id)
                newly_unlocked.append(color.name)
        return newly_unlocked
    
    def get_save_data(self) -> Dict:
        return {
            "applied_colors": self.applied_colors,
            "owned_colors": self.owned_colors,
            "current_palette": self.current_palette,
            "custom_palettes": {
                name: {
                    "name": p.name,
                    "primary": p.primary,
                    "secondary": p.secondary,
                    "accent": p.accent,
                    "background": p.background,
                    "text": p.text
                }
                for name, p in self.custom_palettes.items()
            }
        }
    
    def load_save_data(self, data: Dict):
        self.applied_colors = data.get("applied_colors", {})
        self.owned_colors = data.get("owned_colors", list(ColorRegistry.DEFAULT_COLORS.keys()))
        self.current_palette = data.get("current_palette")
        
        self.custom_palettes = {}
        for name, p_data in data.get("custom_palettes", {}).items():
            self.custom_palettes[name] = ColorPalette(
                name=p_data["name"],
                primary=p_data["primary"],
                secondary=p_data["secondary"],
                accent=p_data["accent"],
                background=p_data["background"],
                text=p_data["text"]
            )
