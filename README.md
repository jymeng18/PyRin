# PyRin

A beautiful 2D platformer game built with Python and Pygame featuring smooth character movement, advanced collision detection, and a polished user interface.

![Game Preview](https://img.shields.io/badge/Status-Playable-brightgreen)
![Python](https://img.shields.io/badge/Python-3.7+-blue)
![Pygame](https://img.shields.io/badge/Pygame-2.0+-red)


## 🚀 Getting Started

### Prerequisites
- Python 3.7 or higher
- Pygame 2.0 or higher
- pytmx library

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/PyRin.git
   cd PyRin
   ```

2. **Install dependencies**
   ```bash
   pip install pygame pytmx
   ```

3. **Run the game**
   ```bash
   python main.py
   ```

## 🎮 How to Play

### Controls
- **Movement**: `WASD` or `Arrow Keys`
- **Jump**: `Space` or `Up Arrow`
- **UI Navigation**: `Mouse` (click buttons)

### Gameplay
1. **Start Screen**: Click "START GAME" to begin
2. **Movement**: Use WASD or arrow keys to move your character
3. **Jumping**: Press Space to jump over obstacles
4. **Stamina**: Watch your stamina - running drains it, standing still recovers it
5. **Avoid Falling**: Don't fall off the map or you'll get a game over!
6. **Game Over**: Choose to "TRY AGAIN" or "QUIT"

## 🏗️ Project Structure

```
PyRin/
├── main.py              # Main game loop and state management
├── player.py            # Player character with animations and physics
├── level.py             # Level loading and tile management
├── collision.py         # Advanced collision detection system
├── objects.py           # Game objects and polygon collision
├── renderer.py          # Rendering system
├── ui.py               # User interface (start/game over screens)
├── settings.py         # Game configuration and constants
├── assets/             # Game assets
│   ├── MainCharacters/
│   │   └── Explorer/   # Character sprites
│   └── Map/           # Level files and tilesets
└── README.md          # This file
```

## 🛠️ Development

### Adding New Levels
1. Create a new `.tmx` file in `assets/Map/`
2. Update the level loading in `level.py`
3. Ensure collision objects are properly configured

### Adding New Animations
1. Add sprite sheets to `assets/MainCharacters/Explorer/`
2. Update the animation state logic in `player.py`
3. Modify the sprite loading system as needed

### Customizing UI
1. Modify colors and fonts in `ui.py`
2. Update button styles and layouts
3. Add new UI elements as needed


## 🙏 Acknowledgments

- **Pygame Community** - For the excellent game development framework
- **Tiled Map Editor** - For the powerful level design tool
- **Archon_Aspect** - Character sprites from [Midnight Forest](https://archon-aspect.itch.io/midnight-forest) on Itch.io
- **Open Source Libraries** - pytmx for TMX file support

---

**Enjoy playing Rin's 2D Platformer! 🎮**
