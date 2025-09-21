import pygame
import math
import random
from settings import *

class Particle:
    def __init__(self, x, y, color, velocity_x=0, velocity_y=0, size=2, life=60):
        self.x = x
        self.y = y
        self.color = color
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.size = size
        self.life = life
        self.max_life = life
        
    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.velocity_y += 0.1  # gravity
        self.life -= 1
        
    def draw(self, screen):
        if self.life > 0:
            alpha = int(255 * (self.life / self.max_life))
            color = (*self.color, alpha)
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)

class ModernButton:
    def __init__(self, x, y, width, height, text, primary_color=(46, 125, 50), secondary_color=(76, 175, 80), text_color=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.primary_color = primary_color
        self.secondary_color = secondary_color
        self.text_color = text_color
        self.is_hovered = False
        self.animation_time = 0
        
    def draw(self, screen, font):
        # Animate button size and glow effect
        self.animation_time += 0.1
        glow_intensity = math.sin(self.animation_time) * 0.3 + 0.7
        
        if self.is_hovered:
            # Create glowing effect
            glow_rect = pygame.Rect(self.rect.x - 5, self.rect.y - 5, self.rect.width + 10, self.rect.height + 10)
            glow_color = (*self.secondary_color, int(50 * glow_intensity))
            pygame.draw.rect(screen, self.secondary_color, glow_rect, border_radius=15)
            
            # Slight scale effect
            scale = 1.05
            scaled_rect = pygame.Rect(
                self.rect.x - (self.rect.width * (scale - 1)) // 2,
                self.rect.y - (self.rect.height * (scale - 1)) // 2,
                self.rect.width * scale,
                self.rect.height * scale
            )
            pygame.draw.rect(screen, self.secondary_color, scaled_rect, border_radius=12)
        else:
            pygame.draw.rect(screen, self.primary_color, self.rect, border_radius=12)
        
        # Draw gradient effect
        gradient_surface = pygame.Surface((self.rect.width, self.rect.height))
        gradient_surface.set_alpha(100)
        for i in range(self.rect.height):
            alpha = int(255 * (1 - i / self.rect.height))
            color = (*self.secondary_color, alpha)
            pygame.draw.line(gradient_surface, self.secondary_color, (0, i), (self.rect.width, i))
        screen.blit(gradient_surface, self.rect)
        
        # Draw button border
        border_color = (255, 255, 255, 100) if self.is_hovered else (255, 255, 255, 50)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2, border_radius=12)
        
        # Draw text with shadow
        text_surface = font.render(self.text, True, (0, 0, 0))
        text_shadow_rect = text_surface.get_rect(center=(self.rect.centerx + 2, self.rect.centery + 2))
        screen.blit(text_surface, text_shadow_rect)
        
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                return True
        return False

class StartScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font_large = pygame.font.Font(None, 96)
        self.font_medium = pygame.font.Font(None, 56)
        self.font_small = pygame.font.Font(None, 32)
        
        # Animation variables
        self.time = 0
        self.particles = []
        self.title_glow_intensity = 0
        
        # Create modern button
        button_width = 280
        button_height = 80
        center_x = SCREEN_WIDTH // 2 - button_width // 2
        center_y = SCREEN_HEIGHT // 2 + 40
        
        self.play_button = ModernButton(
            center_x, center_y, button_width, button_height, "Start!",
            primary_color=(25, 118, 210),  # Beautiful blue
            secondary_color=(41, 182, 246),  # Lighter blue
            text_color=(255, 255, 255)
        )
        
        # Color scheme - Modern dark theme with blue accents
        self.bg_colors = [
            (18, 18, 18),    # Very dark gray
            (25, 25, 35),    # Dark blue-gray
            (35, 35, 50),    # Medium blue-gray
        ]
        
    def create_particles(self):
        """Create floating particles for ambiance"""
        if random.random() < 0.3:  # 30% chance per frame
            x = random.randint(0, SCREEN_WIDTH)
            y = SCREEN_HEIGHT + 10
            color = random.choice([
                (41, 182, 246),   # Light blue
                (156, 39, 176),   # Purple
                (76, 175, 80),    # Green
                (255, 193, 7),    # Amber
            ])
            velocity_x = random.uniform(-1, 1)
            velocity_y = random.uniform(-3, -1)
            size = random.randint(2, 4)
            life = random.randint(60, 120)
            
            self.particles.append(Particle(x, y, color, velocity_x, velocity_y, size, life))
    
    def handle_events(self, events):
        for event in events:
            if self.play_button.handle_event(event):
                return GAME_STATE_PLAYING
        return GAME_STATE_MENU
    
    def draw_gradient_background(self):
        """Draw a beautiful gradient background"""
        for y in range(SCREEN_HEIGHT):
            # Create vertical gradient from dark to slightly lighter
            ratio = y / SCREEN_HEIGHT
            color = (
                int(self.bg_colors[0][0] + (self.bg_colors[1][0] - self.bg_colors[0][0]) * ratio),
                int(self.bg_colors[0][1] + (self.bg_colors[1][1] - self.bg_colors[0][1]) * ratio),
                int(self.bg_colors[0][2] + (self.bg_colors[1][2] - self.bg_colors[0][2]) * ratio)
            )
            pygame.draw.line(self.screen, color, (0, y), (SCREEN_WIDTH, y))
    
    def draw_animated_title(self):
        """Draw the main title with glow effect"""
        self.title_glow_intensity = (math.sin(self.time * 0.02) + 1) * 0.5  # 0 to 1
        
        # Title text
        title = "RIN PLATFORMER"
        
        # Draw glow effect
        glow_size = int(8 + self.title_glow_intensity * 4)
        for i in range(glow_size, 0, -1):
            alpha = int(50 * self.title_glow_intensity * (1 - i / glow_size))
            glow_color = (41, 182, 246, alpha)
            glow_text = self.font_large.render(title, True, (41, 182, 246))
            glow_rect = glow_text.get_rect(center=(SCREEN_WIDTH // 2 + i, SCREEN_HEIGHT // 2 - 120 + i))
            self.screen.blit(glow_text, glow_rect)
        
        # Main title with shadow
        shadow_text = self.font_large.render(title, True, (0, 0, 0))
        shadow_rect = shadow_text.get_rect(center=(SCREEN_WIDTH // 2 + 4, SCREEN_HEIGHT // 2 - 120 + 4))
        self.screen.blit(shadow_text, shadow_rect)
        
        # Main title
        main_text = self.font_large.render(title, True, (255, 255, 255))
        main_rect = main_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 120))
        self.screen.blit(main_text, main_rect)
        
        # Subtitle with fade effect
        subtitle_alpha = int(200 + 55 * math.sin(self.time * 0.03))
        subtitle_text = self.font_medium.render("Adventure Awaits", True, (156, 39, 176))
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(subtitle_text, subtitle_rect)
    
    def draw_decorative_elements(self):
        """Draw floating geometric shapes and patterns"""
        # Animated circles
        for i in range(5):
            x = 200 + i * 200
            y = 150 + math.sin(self.time * 0.02 + i) * 30
            radius = 30 + math.sin(self.time * 0.03 + i) * 10
            
            # Semi-transparent circle
            circle_surface = pygame.Surface((radius * 2, radius * 2))
            circle_surface.set_alpha(30)
            pygame.draw.circle(circle_surface, (41, 182, 246), (radius, radius), radius)
            self.screen.blit(circle_surface, (x - radius, y - radius))
        
        # Floating lines
        for i in range(3):
            start_x = 100 + i * 400
            end_x = start_x + 100
            y = 100 + math.sin(self.time * 0.01 + i * 2) * 50
            color = (41, 182, 246, 100)
            pygame.draw.line(self.screen, (41, 182, 246), (start_x, y), (end_x, y), 3)
    
    def draw_controls(self):
        """Draw control instructions with modern styling"""
        controls = [
            ("WASD / Arrow Keys", "Move"),
            ("SPACE", "Jump"),
            ("Don't fall off!", "Survive")
        ]
        
        start_y = SCREEN_HEIGHT // 2 + 180
        for i, (action, description) in enumerate(controls):
            y_pos = start_y + i * 50
            
            # Action text (left aligned)
            action_text = self.font_small.render(action, True, (255, 193, 7))
            action_rect = action_text.get_rect(center=(SCREEN_WIDTH // 2 - 80, y_pos))
            self.screen.blit(action_text, action_rect)
            
            # Description text (right aligned)
            desc_text = self.font_small.render(description, True, (200, 200, 200))
            desc_rect = desc_text.get_rect(center=(SCREEN_WIDTH // 2 + 80, y_pos))
            self.screen.blit(desc_text, desc_rect)
    
    def draw(self):
        # Update animation time
        self.time += 1
        
        # Create particles
        self.create_particles()
        
        # Update particles
        self.particles = [p for p in self.particles if p.life > 0]
        for particle in self.particles:
            particle.update()
        
        # Draw gradient background
        self.draw_gradient_background()
        
        # Draw decorative elements
        self.draw_decorative_elements()
        
        # Draw particles
        for particle in self.particles:
            particle.draw(self.screen)
        
        # Draw animated title
        self.draw_animated_title()
        
        # Draw controls
        self.draw_controls()
        
        # Draw play button
        self.play_button.draw(self.screen, self.font_medium)

class GameOverScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font_large = pygame.font.Font(None, 96)
        self.font_medium = pygame.font.Font(None, 56)
        self.font_small = pygame.font.Font(None, 32)
        
        # Animation variables
        self.time = 0
        self.particles = []
        self.title_shake_intensity = 0
        
        # Create modern buttons
        button_width = 240
        button_height = 70
        center_x = SCREEN_WIDTH // 2 - button_width // 2
        restart_y = SCREEN_HEIGHT // 2 + 60
        quit_y = SCREEN_HEIGHT // 2 + 150
        
        self.restart_button = ModernButton(
            center_x, restart_y, button_width, button_height, "TRY AGAIN",
            primary_color=(76, 175, 80),   # Green
            secondary_color=(139, 195, 74), # Light green
            text_color=(255, 255, 255)
        )
        
        self.quit_button = ModernButton(
            center_x, quit_y, button_width, button_height, "MAIN MENU",
            primary_color=(244, 67, 54),   # Red
            secondary_color=(255, 138, 101), # Light red
            text_color=(255, 255, 255)
        )
        
        # Color scheme - Dark theme with red/orange accents
        self.bg_colors = [
            (20, 20, 20),    # Very dark
            (30, 20, 25),    # Dark red-gray
            (40, 25, 30),    # Medium red-gray
        ]
        
        # Create initial dramatic particles
        self.create_dramatic_particles()
    
    def create_dramatic_particles(self):
        """Create dramatic particle explosion effect"""
        center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100
        
        for _ in range(50):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(3, 8)
            velocity_x = math.cos(angle) * speed
            velocity_y = math.sin(angle) * speed
            
            color = random.choice([
                (244, 67, 54),    # Red
                (255, 152, 0),    # Orange
                (255, 193, 7),    # Amber
                (156, 39, 176),   # Purple
            ])
            
            size = random.randint(3, 6)
            life = random.randint(40, 80)
            
            self.particles.append(Particle(
                center_x, center_y, color, velocity_x, velocity_y, size, life
            ))
    
    def create_ambient_particles(self):
        """Create ongoing ambient particles"""
        if random.random() < 0.2:  # 20% chance per frame
            x = random.randint(0, SCREEN_WIDTH)
            y = SCREEN_HEIGHT + 10
            color = random.choice([
                (244, 67, 54),    # Red
                (255, 152, 0),    # Orange
                (255, 193, 7),    # Amber
            ])
            velocity_x = random.uniform(-1, 1)
            velocity_y = random.uniform(-2, -0.5)
            size = random.randint(2, 4)
            life = random.randint(60, 120)
            
            self.particles.append(Particle(x, y, color, velocity_x, velocity_y, size, life))
    
    def handle_events(self, events):
        for event in events:
            if self.restart_button.handle_event(event):
                return GAME_STATE_PLAYING
            elif self.quit_button.handle_event(event):
                return "quit"
        return GAME_STATE_GAME_OVER
    
    def draw_gradient_background(self):
        """Draw a dramatic gradient background"""
        for y in range(SCREEN_HEIGHT):
            ratio = y / SCREEN_HEIGHT
            color = (
                int(self.bg_colors[0][0] + (self.bg_colors[1][0] - self.bg_colors[0][0]) * ratio),
                int(self.bg_colors[0][1] + (self.bg_colors[1][1] - self.bg_colors[0][1]) * ratio),
                int(self.bg_colors[0][2] + (self.bg_colors[1][2] - self.bg_colors[0][2]) * ratio)
            )
            pygame.draw.line(self.screen, color, (0, y), (SCREEN_WIDTH, y))
    
    def draw_animated_title(self):
        """Draw the game over title with shake effect"""
        self.title_shake_intensity = max(0, self.title_shake_intensity - 0.5)
        
        # Calculate shake offset
        shake_x = random.uniform(-self.title_shake_intensity, self.title_shake_intensity)
        shake_y = random.uniform(-self.title_shake_intensity, self.title_shake_intensity)
        
        title = "GAME OVER"
        title_x = SCREEN_WIDTH // 2 + shake_x
        title_y = SCREEN_HEIGHT // 2 - 120 + shake_y
        
        # Draw dramatic glow effect
        glow_intensity = (math.sin(self.time * 0.05) + 1) * 0.5
        glow_size = int(12 + glow_intensity * 8)
        
        for i in range(glow_size, 0, -1):
            alpha = int(80 * glow_intensity * (1 - i / glow_size))
            glow_text = self.font_large.render(title, True, (244, 67, 54))
            glow_rect = glow_text.get_rect(center=(title_x + i, title_y + i))
            self.screen.blit(glow_text, glow_rect)
        
        # Draw multiple shadow layers for depth
        for i in range(6, 0, -1):
            shadow_text = self.font_large.render(title, True, (0, 0, 0))
            shadow_rect = shadow_text.get_rect(center=(title_x + i, title_y + i))
            self.screen.blit(shadow_text, shadow_rect)
        
        # Main title
        main_text = self.font_large.render(title, True, (255, 255, 255))
        main_rect = main_text.get_rect(center=(title_x, title_y))
        self.screen.blit(main_text, main_rect)
        
        # Subtitle with pulsing effect
        pulse = (math.sin(self.time * 0.04) + 1) * 0.5
        subtitle_text = self.font_medium.render("Don't give up!", True, (255, 193, 7))
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60))
        self.screen.blit(subtitle_text, subtitle_rect)
    
    def draw_decorative_elements(self):
        """Draw dramatic decorative elements"""
        # Animated lightning-like lines
        for i in range(3):
            start_x = 100 + i * 400
            end_x = start_x + 150
            y = 80 + math.sin(self.time * 0.03 + i * 3) * 40
            
            # Create jagged lightning effect
            points = [(start_x, y)]
            segments = 8
            for j in range(1, segments):
                seg_x = start_x + (end_x - start_x) * j / segments
                seg_y = y + random.uniform(-20, 20)
                points.append((seg_x, seg_y))
            points.append((end_x, y))
            
            pygame.draw.lines(self.screen, (244, 67, 54), False, points, 3)
        
        # Floating embers
        for i in range(8):
            x = 150 + i * 150
            y = 200 + math.sin(self.time * 0.02 + i) * 60
            radius = 15 + math.sin(self.time * 0.04 + i) * 5
            
            # Semi-transparent circle
            circle_surface = pygame.Surface((radius * 2, radius * 2))
            circle_surface.set_alpha(40)
            pygame.draw.circle(circle_surface, (255, 152, 0), (radius, radius), radius)
            self.screen.blit(circle_surface, (x - radius, y - radius))
    
    def draw_stats(self):
        """Draw game statistics or motivational text"""
        messages = [
            "Every failure is a step toward success",
            "The greatest glory is in rising every time we fall",
            "Challenge accepted, warrior!",
            "Your determination will prevail"
        ]
        
        # Cycle through messages
        message_index = (self.time // 120) % len(messages)
        message = messages[message_index]
        
        message_text = self.font_small.render(message, True, (200, 200, 200))
        message_rect = message_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        self.screen.blit(message_text, message_rect)
    
    def draw(self):
        # Update animation time
        self.time += 1
        
        # Create ambient particles
        self.create_ambient_particles()
        
        # Update particles
        self.particles = [p for p in self.particles if p.life > 0]
        for particle in self.particles:
            particle.update()
        
        # Draw gradient background
        self.draw_gradient_background()
        
        # Draw decorative elements
        self.draw_decorative_elements()
        
        # Draw particles
        for particle in self.particles:
            particle.draw(self.screen)
        
        # Draw animated title
        self.draw_animated_title()
        
        # Draw stats/motivational text
        self.draw_stats()
        
        # Draw buttons
        self.restart_button.draw(self.screen, self.font_medium)
        self.quit_button.draw(self.screen, self.font_medium)
