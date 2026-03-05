"""
渲染系统增强模块
提供2D图形渲染、粒子效果、光影处理等功能
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Callable
from enum import Enum
import math
import random
import colorsys


class RenderLayer(Enum):
    BACKGROUND = 0
    TERRAIN = 1
    OBJECTS = 2
    CHARACTERS = 3
    EFFECTS = 4
    UI = 5
    OVERLAY = 6


class BlendMode(Enum):
    NORMAL = "normal"
    ADDITIVE = "additive"
    MULTIPLY = "multiply"
    SCREEN = "screen"
    OVERLAY = "overlay"


class ParticleType(Enum):
    SPARKLE = "sparkle"
    RAIN = "rain"
    SNOW = "snow"
    LEAF = "leaf"
    DUST = "dust"
    FIRE = "fire"
    SMOKE = "smoke"
    BUBBLE = "bubble"
    STAR = "star"
    HEART = "heart"


@dataclass
class Color:
    r: int
    g: int
    b: int
    a: float = 1.0
    
    def to_hex(self) -> str:
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}"
    
    def to_rgb(self) -> Tuple[int, int, int]:
        return (self.r, self.g, self.b)
    
    def to_rgba(self) -> Tuple[int, int, int, float]:
        return (self.r, self.g, self.b, self.a)
    
    def with_alpha(self, alpha: float) -> 'Color':
        return Color(self.r, self.g, self.b, alpha)
    
    def lighten(self, amount: float = 0.2) -> 'Color':
        h, l, s = colorsys.rgb_to_hls(self.r/255, self.g/255, self.b/255)
        l = min(1.0, l + amount)
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        return Color(int(r*255), int(g*255), int(b*255), self.a)
    
    def darken(self, amount: float = 0.2) -> 'Color':
        h, l, s = colorsys.rgb_to_hls(self.r/255, self.g/255, self.b/255)
        l = max(0.0, l - amount)
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        return Color(int(r*255), int(g*255), int(b*255), self.a)
    
    @classmethod
    def from_hex(cls, hex_str: str) -> 'Color':
        hex_str = hex_str.lstrip('#')
        return cls(int(hex_str[0:2], 16), int(hex_str[2:4], 16), int(hex_str[4:6], 16))
    
    @classmethod
    def random(cls) -> 'Color':
        return cls(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


@dataclass
class Vector2:
    x: float
    y: float
    
    def __add__(self, other: 'Vector2') -> 'Vector2':
        return Vector2(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: 'Vector2') -> 'Vector2':
        return Vector2(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar: float) -> 'Vector2':
        return Vector2(self.x * scalar, self.y * scalar)
    
    def __truediv__(self, scalar: float) -> 'Vector2':
        return Vector2(self.x / scalar, self.y / scalar)
    
    def length(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2)
    
    def normalize(self) -> 'Vector2':
        l = self.length()
        if l == 0:
            return Vector2(0, 0)
        return self / l
    
    def dot(self, other: 'Vector2') -> float:
        return self.x * other.x + self.y * other.y
    
    def angle(self) -> float:
        return math.atan2(self.y, self.x)
    
    def rotate(self, angle: float) -> 'Vector2':
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        return Vector2(
            self.x * cos_a - self.y * sin_a,
            self.x * sin_a + self.y * cos_a
        )
    
    @classmethod
    def from_angle(cls, angle: float, length: float = 1.0) -> 'Vector2':
        return cls(math.cos(angle) * length, math.sin(angle) * length)


@dataclass
class Particle:
    position: Vector2
    velocity: Vector2
    acceleration: Vector2
    color: Color
    size: float
    life: float
    max_life: float
    particle_type: ParticleType
    rotation: float = 0.0
    rotation_speed: float = 0.0
    scale_start: float = 1.0
    scale_end: float = 0.0
    alpha_start: float = 1.0
    alpha_end: float = 0.0
    
    def update(self, dt: float) -> bool:
        self.velocity = self.velocity + self.acceleration * dt
        self.position = self.position + self.velocity * dt
        self.rotation += self.rotation_speed * dt
        self.life -= dt
        
        return self.life > 0
    
    def get_progress(self) -> float:
        return 1.0 - (self.life / self.max_life)
    
    def get_current_scale(self) -> float:
        progress = self.get_progress()
        return self.scale_start + (self.scale_end - self.scale_start) * progress
    
    def get_current_alpha(self) -> float:
        progress = self.get_progress()
        return self.alpha_start + (self.alpha_end - self.alpha_start) * progress


@dataclass
class ParticleEmitter:
    position: Vector2
    particle_type: ParticleType
    emission_rate: float
    max_particles: int
    lifetime_range: Tuple[float, float]
    speed_range: Tuple[float, float]
    size_range: Tuple[float, float]
    color_range: Tuple[Color, Color]
    direction_range: Tuple[float, float]
    spread: float = 0.0
    gravity: Vector2 = field(default_factory=lambda: Vector2(0, 0))
    is_active: bool = True
    particles: List[Particle] = field(default_factory=list)
    emission_accumulator: float = 0.0
    
    def update(self, dt: float):
        if self.is_active:
            self.emission_accumulator += self.emission_rate * dt
            
            while self.emission_accumulator >= 1.0 and len(self.particles) < self.max_particles:
                self._emit_particle()
                self.emission_accumulator -= 1.0
        
        self.particles = [p for p in self.particles if p.update(dt)]
    
    def _emit_particle(self):
        angle = random.uniform(self.direction_range[0], self.direction_range[1])
        angle += random.uniform(-self.spread, self.spread)
        
        speed = random.uniform(self.speed_range[0], self.speed_range[1])
        velocity = Vector2.from_angle(angle, speed)
        
        life = random.uniform(self.lifetime_range[0], self.lifetime_range[1])
        size = random.uniform(self.size_range[0], self.size_range[1])
        
        t = random.random()
        color = Color(
            int(self.color_range[0].r + (self.color_range[1].r - self.color_range[0].r) * t),
            int(self.color_range[0].g + (self.color_range[1].g - self.color_range[0].g) * t),
            int(self.color_range[0].b + (self.color_range[1].b - self.color_range[0].b) * t)
        )
        
        particle = Particle(
            position=Vector2(self.position.x, self.position.y),
            velocity=velocity,
            acceleration=self.gravity,
            color=color,
            size=size,
            life=life,
            max_life=life,
            particle_type=self.particle_type,
            rotation=random.uniform(0, 2 * math.pi),
            rotation_speed=random.uniform(-2, 2)
        )
        
        self.particles.append(particle)
    
    def get_particle_count(self) -> int:
        return len(self.particles)
    
    def burst(self, count: int = 10):
        for _ in range(count):
            if len(self.particles) < self.max_particles:
                self._emit_particle()


@dataclass
class LightSource:
    position: Vector2
    radius: float
    color: Color
    intensity: float
    flicker: float = 0.0
    flicker_speed: float = 1.0
    time: float = 0.0
    
    def update(self, dt: float):
        self.time += dt * self.flicker_speed
    
    def get_current_intensity(self) -> float:
        if self.flicker > 0:
            flicker_value = math.sin(self.time * 10) * self.flicker
            return max(0.1, self.intensity + flicker_value)
        return self.intensity


@dataclass
class ShadowCaster:
    position: Vector2
    size: Vector2
    opacity: float = 0.5
    
    def get_shadow_polygon(self, light_pos: Vector2, light_radius: float) -> List[Vector2]:
        return []


class Renderer:
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.layers: Dict[RenderLayer, List] = {layer: [] for layer in RenderLayer}
        self.particle_emitters: List[ParticleEmitter] = []
        self.lights: List[LightSource] = []
        self.ambient_light: Color = Color(255, 255, 255, 0.3)
        self.background_color: Color = Color(135, 206, 235)
        self.camera_position: Vector2 = Vector2(0, 0)
        self.camera_zoom: float = 1.0
        self.time: float = 0.0
    
    def update(self, dt: float):
        self.time += dt
        
        for emitter in self.particle_emitters:
            emitter.update(dt)
        
        for light in self.lights:
            light.update(dt)
    
    def add_particle_emitter(self, emitter: ParticleEmitter):
        self.particle_emitters.append(emitter)
    
    def remove_particle_emitter(self, emitter: ParticleEmitter):
        if emitter in self.particle_emitters:
            self.particle_emitters.remove(emitter)
    
    def add_light(self, light: LightSource):
        self.lights.append(light)
    
    def remove_light(self, light: LightSource):
        if light in self.lights:
            self.lights.remove(light)
    
    def clear_layer(self, layer: RenderLayer):
        self.layers[layer].clear()
    
    def clear_all(self):
        for layer in self.layers:
            self.layers[layer].clear()
        self.particle_emitters.clear()
        self.lights.clear()
    
    def world_to_screen(self, world_pos: Vector2) -> Vector2:
        return (world_pos - self.camera_position) * self.camera_zoom + Vector2(self.width/2, self.height/2)
    
    def screen_to_world(self, screen_pos: Vector2) -> Vector2:
        return (screen_pos - Vector2(self.width/2, self.height/2)) / self.camera_zoom + self.camera_position
    
    def is_visible(self, pos: Vector2, margin: float = 100) -> bool:
        screen_pos = self.world_to_screen(pos)
        return (-margin < screen_pos.x < self.width + margin and 
                -margin < screen_pos.y < self.height + margin)
    
    def get_light_at_position(self, pos: Vector2) -> Color:
        total_r, total_g, total_b = 0.0, 0.0, 0.0
        total_intensity = self.ambient_light.a
        
        for light in self.lights:
            distance = (light.position - pos).length()
            if distance < light.radius:
                intensity = light.get_current_intensity() * (1 - distance / light.radius)
                total_r += light.color.r * intensity
                total_g += light.color.g * intensity
                total_b += light.color.b * intensity
                total_intensity += intensity
        
        if total_intensity > 0:
            return Color(
                int(min(255, total_r / total_intensity)),
                int(min(255, total_g / total_intensity)),
                int(min(255, total_b / total_intensity)),
                min(1.0, total_intensity)
            )
        
        return self.ambient_light
    
    def create_rain_effect(self, intensity: float = 1.0) -> ParticleEmitter:
        return ParticleEmitter(
            position=Vector2(self.width / 2, -50),
            particle_type=ParticleType.RAIN,
            emission_rate=100 * intensity,
            max_particles=500,
            lifetime_range=(0.5, 1.0),
            speed_range=(300, 400),
            size_range=(2, 4),
            color_range=(Color(150, 200, 255, 0.6), Color(100, 150, 200, 0.4)),
            direction_range=(math.pi * 0.6, math.pi * 0.6),
            spread=0.2,
            gravity=Vector2(0, 500)
        )
    
    def create_snow_effect(self, intensity: float = 1.0) -> ParticleEmitter:
        return ParticleEmitter(
            position=Vector2(self.width / 2, -50),
            particle_type=ParticleType.SNOW,
            emission_rate=30 * intensity,
            max_particles=200,
            lifetime_range=(3.0, 5.0),
            speed_range=(20, 50),
            size_range=(3, 6),
            color_range=(Color(255, 255, 255, 0.9), Color(240, 248, 255, 0.7)),
            direction_range=(math.pi / 2, math.pi / 2),
            spread=0.5,
            gravity=Vector2(0, 30)
        )
    
    def create_fire_effect(self, position: Vector2, size: float = 1.0) -> ParticleEmitter:
        return ParticleEmitter(
            position=position,
            particle_type=ParticleType.FIRE,
            emission_rate=50 * size,
            max_particles=100,
            lifetime_range=(0.3, 0.8),
            speed_range=(50, 100),
            size_range=(5 * size, 15 * size),
            color_range=(Color(255, 200, 50), Color(255, 100, 0)),
            direction_range=(-math.pi/2 - 0.3, -math.pi/2 + 0.3),
            spread=0.3,
            gravity=Vector2(0, -50)
        )
    
    def create_sparkle_effect(self, position: Vector2, count: int = 20) -> ParticleEmitter:
        emitter = ParticleEmitter(
            position=position,
            particle_type=ParticleType.SPARKLE,
            emission_rate=0,
            max_particles=count,
            lifetime_range=(0.5, 1.5),
            speed_range=(30, 80),
            size_range=(2, 5),
            color_range=(Color(255, 255, 100), Color(255, 255, 255)),
            direction_range=(0, 2 * math.pi),
            spread=math.pi
        )
        emitter.burst(count)
        return emitter
    
    def get_all_particles(self) -> List[Particle]:
        particles = []
        for emitter in self.particle_emitters:
            particles.extend(emitter.particles)
        return particles
    
    def get_render_data(self) -> Dict:
        return {
            "time": self.time,
            "camera": {
                "x": self.camera_position.x,
                "y": self.camera_position.y,
                "zoom": self.camera_zoom
            },
            "background": self.background_color.to_hex(),
            "ambient_light": self.ambient_light.to_hex(),
            "particle_count": sum(e.get_particle_count() for e in self.particle_emitters),
            "light_count": len(self.lights)
        }


class AnimationSystem:
    
    @dataclass
    class Animation:
        name: str
        frames: List[Dict]
        duration: float
        loop: bool = True
        current_frame: int = 0
        elapsed: float = 0.0
        is_playing: bool = False
        on_complete: Optional[Callable] = None
        
        def update(self, dt: float) -> bool:
            if not self.is_playing:
                return False
            
            self.elapsed += dt
            frame_duration = self.duration / len(self.frames)
            
            if self.elapsed >= frame_duration:
                self.elapsed -= frame_duration
                self.current_frame += 1
                
                if self.current_frame >= len(self.frames):
                    if self.loop:
                        self.current_frame = 0
                    else:
                        self.is_playing = False
                        if self.on_complete:
                            self.on_complete()
                        return True
            
            return False
        
        def get_current_frame(self) -> Dict:
            return self.frames[self.current_frame]
        
        def play(self):
            self.is_playing = True
            self.current_frame = 0
            self.elapsed = 0.0
        
        def pause(self):
            self.is_playing = False
        
        def reset(self):
            self.current_frame = 0
            self.elapsed = 0.0
            self.is_playing = False
    
    def __init__(self):
        self.animations: Dict[str, 'AnimationSystem.Animation'] = {}
        self.active_animations: List[str] = []
    
    def create_animation(self, name: str, frames: List[Dict], duration: float, 
                         loop: bool = True) -> 'AnimationSystem.Animation':
        animation = self.Animation(
            name=name,
            frames=frames,
            duration=duration,
            loop=loop
        )
        self.animations[name] = animation
        return animation
    
    def play(self, name: str, on_complete: Callable = None):
        if name in self.animations:
            animation = self.animations[name]
            animation.on_complete = on_complete
            animation.play()
            if name not in self.active_animations:
                self.active_animations.append(name)
    
    def stop(self, name: str):
        if name in self.animations:
            self.animations[name].pause()
            if name in self.active_animations:
                self.active_animations.remove(name)
    
    def update(self, dt: float):
        completed = []
        for name in self.active_animations:
            if name in self.animations:
                if self.animations[name].update(dt):
                    completed.append(name)
        
        for name in completed:
            if name in self.active_animations:
                self.active_animations.remove(name)
    
    def get_animation(self, name: str) -> Optional['AnimationSystem.Animation']:
        return self.animations.get(name)
    
    def create_sprite_animation(self, name: str, sprite_names: List[str], 
                                frame_duration: float = 0.1, loop: bool = True):
        frames = [{"sprite": s} for s in sprite_names]
        return self.create_animation(name, frames, frame_duration * len(frames), loop)
    
    def create_color_animation(self, name: str, colors: List[str], 
                               duration: float = 1.0, loop: bool = True):
        frames = [{"color": c} for c in colors]
        return self.create_animation(name, frames, duration, loop)
    
    def create_position_animation(self, name: str, positions: List[Tuple[float, float]], 
                                  duration: float = 1.0, loop: bool = True):
        frames = [{"x": p[0], "y": p[1]} for p in positions]
        return self.create_animation(name, frames, duration, loop)


class ShaderEffect:
    
    def __init__(self, name: str):
        self.name = name
        self.parameters: Dict[str, any] = {}
        self.enabled: bool = True
    
    def set_parameter(self, name: str, value: any):
        self.parameters[name] = value
    
    def get_parameter(self, name: str, default: any = None) -> any:
        return self.parameters.get(name, default)
    
    def apply(self, color: Color, position: Vector2, time: float) -> Color:
        return color


class GrayscaleEffect(ShaderEffect):
    
    def __init__(self):
        super().__init__("grayscale")
        self.set_parameter("intensity", 1.0)
    
    def apply(self, color: Color, position: Vector2, time: float) -> Color:
        intensity = self.get_parameter("intensity", 1.0)
        gray = int(0.299 * color.r + 0.587 * color.g + 0.114 * color.b)
        return Color(
            int(color.r + (gray - color.r) * intensity),
            int(color.g + (gray - color.g) * intensity),
            int(color.b + (gray - color.b) * intensity),
            color.a
        )


class WaveEffect(ShaderEffect):
    
    def __init__(self):
        super().__init__("wave")
        self.set_parameter("amplitude", 10.0)
        self.set_parameter("frequency", 1.0)
        self.set_parameter("speed", 1.0)
    
    def apply(self, color: Color, position: Vector2, time: float) -> Color:
        amplitude = self.get_parameter("amplitude", 10.0)
        frequency = self.get_parameter("frequency", 1.0)
        speed = self.get_parameter("speed", 1.0)
        
        offset = math.sin(position.x * frequency * 0.1 + time * speed) * amplitude
        
        return Color(
            max(0, min(255, color.r + int(offset))),
            max(0, min(255, color.g + int(offset))),
            max(0, min(255, color.b + int(offset))),
            color.a
        )


class GlowEffect(ShaderEffect):
    
    def __init__(self):
        super().__init__("glow")
        self.set_parameter("intensity", 0.5)
        self.set_parameter("color", Color(255, 255, 200))
    
    def apply(self, color: Color, position: Vector2, time: float) -> Color:
        intensity = self.get_parameter("intensity", 0.5)
        glow_color = self.get_parameter("color", Color(255, 255, 200))
        
        pulse = (math.sin(time * 3) + 1) / 2 * intensity
        
        return Color(
            min(255, int(color.r + glow_color.r * pulse)),
            min(255, int(color.g + glow_color.g * pulse)),
            min(255, int(color.b + glow_color.b * pulse)),
            color.a
        )


class PostProcessor:
    
    def __init__(self):
        self.effects: List[ShaderEffect] = []
    
    def add_effect(self, effect: ShaderEffect):
        self.effects.append(effect)
    
    def remove_effect(self, effect: ShaderEffect):
        if effect in self.effects:
            self.effects.remove(effect)
    
    def process(self, color: Color, position: Vector2, time: float) -> Color:
        result = color
        for effect in self.effects:
            if effect.enabled:
                result = effect.apply(result, position, time)
        return result
    
    def clear_effects(self):
        self.effects.clear()
