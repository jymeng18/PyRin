import pygame
import pytmx
from settings import *

class GameObject(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        # Remove the sprites_group reference - not needed

class PolygonCollisionObject:
    def __init__(self, x, y, points):
        self.x = x
        self.y = y
        # Convert Point objects to tuples if needed
        self.points = []
        for point in points:
            if hasattr(point, 'x') and hasattr(point, 'y'):
                # It's a Point object
                self.points.append((point.x - x, point.y - y))  # Convert to relative coordinates
            else:
                # It's already a tuple
                self.points.append(point)
        
        # Create a bounding rect for quick collision checks
        min_x = min(point[0] for point in self.points) + x
        min_y = min(point[1] for point in self.points) + y
        max_x = max(point[0] for point in self.points) + x
        max_y = max(point[1] for point in self.points) + y
        self.rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
    
    def point_in_triangle(self, px, py):
        """Check if a point is inside the triangle using barycentric coordinates"""
        # Convert points to absolute coordinates
        p1 = (self.points[0][0] + self.x, self.points[0][1] + self.y)
        p2 = (self.points[1][0] + self.x, self.points[1][1] + self.y)
        p3 = (self.points[2][0] + self.x, self.points[2][1] + self.y)
        
        # Calculate barycentric coordinates
        denom = (p2[1] - p3[1]) * (p1[0] - p3[0]) + (p3[0] - p2[0]) * (p1[1] - p3[1])
        if abs(denom) < 1e-10:  # Avoid division by zero
            return False
            
        a = ((p2[1] - p3[1]) * (px - p3[0]) + (p3[0] - p2[0]) * (py - p3[1])) / denom
        b = ((p3[1] - p1[1]) * (px - p3[0]) + (p1[0] - p3[0]) * (py - p3[1])) / denom
        c = 1 - a - b
        
        return a >= 0 and b >= 0 and c >= 0
    
    def collides_with_rect(self, rect):
        """Check if a rectangle collides with this triangle"""
        # First check bounding box collision
        if not self.rect.colliderect(rect):
            return False
        
        # Check if any corner of the rectangle is inside the triangle
        corners = [
            (rect.left, rect.top),
            (rect.right, rect.top),
            (rect.left, rect.bottom),
            (rect.right, rect.bottom)
        ]
        
        for corner in corners:
            if self.point_in_triangle(corner[0], corner[1]):
                return True
        
        # Check if any vertex of the triangle is inside the rectangle
        triangle_points = [
            (self.points[0][0] + self.x, self.points[0][1] + self.y),
            (self.points[1][0] + self.x, self.points[1][1] + self.y),
            (self.points[2][0] + self.x, self.points[2][1] + self.y)
        ]
        
        for point in triangle_points:
            if rect.collidepoint(point):
                return True
        
        return False