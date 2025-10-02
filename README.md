# NanoGolf 🏌️‍♂️⛳

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)  
[![OpenGL](https://img.shields.io/badge/OpenGL-3.3-green.svg)](https://www.opengl.org/)  
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)  
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)]()

**NanoGolf** is a simple 3D mini-golf simulation game built from scratch in Python using **OpenGL 3.3** and **GLSL shaders**. This project demonstrates 3D graphics programming, physics simulation, collision detection, and interactive gameplay mechanics in a mini-golf experience.

##  Game Overview

Experience a challenging 3D mini-golf adventure featuring:
- **Two complete levels** with layouts and obstacles
- **Realistic physics simulation** with trajectory calculation, friction, and momentum
- **Dynamic camera system** that follows your ball
- **Power-based shot system** with visual feedback
- **collision detection** across multiple terrain zones
- **Score tracking and level progression**

### Gameplay Mechanics

- **Shot Power Control**: Hold `P` to charge your shot power (0-100%), with a visual power bar
- **Physics-Based Movement**: ball physics with exponential velocity decay
- **Multi-Level Progression**: Complete Level 1 to unlock Level 2 with advanced obstacles
- **Collision System**: Smart ball redirection based on collision angles and terrain
- **Level Teleportation**: Special portal system in Level 2 for strategic gameplay

##  Technical Features

###  Core Gameplay
- **Dynamic Power System**: Real-time power charging with visual feedback
- **Advanced Physics Engine**: Custom trajectory calculation with friction simulation
- **Multi-Level Architecture**: Seamless level transitions and object management
- **Score & Statistics Tracking**: Shot counting and level-based scoring system

###  3D Graphics & Rendering
- **OpenGL 3.3 Core Profile**: Modern OpenGL for optimal performance
- **Custom GLSL Shader Pipeline**: Multiple specialized shaders for different effects
- **3D Mesh Loading**: Support for OBJ format 3D models
- **Texture Management**: Efficient texture loading and binding system
- **Dynamic Lighting**: Shader-based lighting calculations

###  Advanced Systems
- **Camera Control System**: 3D camera with rotation, translation, and automatic following
- **Collision Detection**: Zone-based collision system with angle-dependent responses
- **UI/HUD Rendering**: 2D overlay system for game interface elements
- **Text Rendering**: Custom bitmap font rendering system
- **Object-Oriented Design**: Clean separation of concerns with modular architecture

##  Project Architecture

````
NanoGolf/
├──  Game Core
│   ├── main.py              # Game entry point & scene setup
│   ├── viewerGL.py          # Main game engine & rendering loop
│   └── cpe3d.py             # 3D transformations, camera & object classes
├──  Engine Components  
│   ├── glutils.py           # OpenGL utilities & shader management
│   ├── mesh.py              # 3D mesh loading & GPU buffer management
│   └── requirements.txt     # Python dependencies
├──  Assets
│   ├── IMG/                 # Textures & UI elements
│   │   ├── ball_red.png     # Ball texture
│   │   ├── grass.jpg        # Terrain texture
│   │   ├── bois.png         # Wood obstacle texture
│   │   ├── flag_blue.png    # Goal flag texture
│   │   └── ...              # Additional textures
│   ├── OBJ/                 # 3D models
│   │   ├── ball2.obj        # Golf ball mesh
│   │   ├── wall.obj         # Barrier walls
│   │   ├── hole_*.obj       # Various hole types
│   │   ├── windwill.obj     # Windmill obstacle
│   │   └── ...              # Additional 3D models
│   └── Shaders/             # GLSL shader programs
│       ├── shader.vert/frag # Main 3D rendering shaders
│       ├── gui.vert/frag    # UI text rendering shaders
│       └── bar.vert/frag    # Power bar shaders
└──  Development
    ├── mp1.py               # Multiprocessing utilities
    └── mp2.py               # Process communication tests
````

## System Requirements

### Minimum Requirements
- **OS**: Windows 10, macOS 10.14, or Linux (Ubuntu 18.04+)
- **Python**: 3.7+ (recommended: 3.9+)
- **Graphics**: OpenGL 3.3 compatible GPU
- **Memory**: 512MB RAM
- **Storage**: 50MB free space

### Recommended
- **Graphics**: Dedicated GPU with 1GB+ VRAM
- **Memory**: 2GB+ RAM for smooth performance
- **Display**: 1920x1080 resolution for optimal experience

## Installation & Setup

### Quick Start
```bash
# Clone the repository
git clone https://github.com/MaaatGrv/NanoGolf.git
cd NanoGolf

# Install dependencies
pip install -r requirements.txt

# Run the game
python main.py
```

### Detailed Setup

#### 1. **Environment Setup**
```bash
# Create virtual environment (recommended)
python3 -m venv nanogolf-env

# Activate virtual environment
# On Windows:
nanogolf-env\Scripts\activate
# On macOS/Linux:
source nanogolf-env/bin/activate
```

#### 2. **Dependency Installation**
```bash
# Install from requirements file
pip install -r requirements.txt

# Or install individually:
pip install PyOpenGL PyGLFW numpy Pillow pyrr
```

#### 3. **Verify Installation**
```bash
# Test OpenGL support
python -c "import OpenGL.GL as GL; print('OpenGL Version:', GL.glGetString(GL.GL_VERSION))"

# Launch game
python main.py
```

## Game Controls

### Basic Controls
| Input | Action |
|-------|---------|
| **Mouse** | Rotate and pan camera view |
| **Left/Right Arrow Keys** | Rotate ball direction |
| **P (Hold)** | Charge shot power (0-100%) |
| **P (Release)** | Execute shot with charged power |
| **Q** | Skip to next level (debug) |

### UI Interactions
| Element | Action |
|---------|---------|
| **Rejouer Button** | Restart current level |
| **Quitter Button** | Exit game |
| **Power Bar** | Visual feedback for shot strength |

### Advanced Techniques
- **Power Control**: Hold `P` longer for more powerful shots, but watch the power bar!
- **Direction Planning**: Use arrow keys to aim before charging your shot
- **Momentum Management**: Consider ball momentum for curved shots around obstacles

## Technical Architecture

### Core Engine Components

#### **ViewerGL Class** (`viewerGL.py`)
- **Main Game Loop**: Handles rendering, input, and game state
- **Physics Simulation**: Implements realistic ball trajectory and friction
- **Collision Detection**: Multi-zone collision system with intelligent responses
- **Camera Management**: Dynamic camera that follows ball movement
- **Level Management**: Handles level transitions and object spawning

#### **3D Graphics Pipeline** (`cpe3d.py`, `glutils.py`)
- **Object3D System**: Manages 3D transformations and rendering
- **Shader Management**: Loads and compiles GLSL shaders dynamically
- **Texture System**: Efficient texture loading and binding
- **Camera System**: Full 3D camera with matrix transformations

#### **Mesh Loading System** (`mesh.py`)
- **OBJ File Parser**: Custom implementation for 3D model loading
- **GPU Buffer Management**: Optimized vertex buffer and index buffer handling
- **Mesh Normalization**: Automatic scaling and centering of 3D models
- **Matrix Transformations**: Support for scaling, rotation, and translation

### Physics System

#### **Trajectory Calculation**
```python
# Exponential velocity decay formula
v0 = power * 0.8  # Initial velocity from shot power
f = 30.0         # Friction coefficient
m = 0.05         # Ball mass (kg)
Tau = m/f        # Time constant
distance = Tau * v0 * (exp(-t0/Tau) - exp(-t1/Tau))
```

#### **Collision Response**
- **Zone-Based Detection**: Different collision behaviors for different terrain areas
- **Angle-Dependent Response**: Ball direction changes based on collision angle
- **Boundary Enforcement**: Prevents ball from leaving playable area

## Shader System

### Available Shaders
- **`shader.vert/frag`**: Main 3D object rendering with lighting and textures
- **`gui.vert/frag`**: 2D UI text rendering with bitmap font support
- **`bar.vert/frag`**: Power bar with dynamic scaling effects
- **`barkac.vert/frag`**: UI background elements

### Shader Features
- **Vertex Transformations**: World, view, and projection matrix transformations
- **Texture Mapping**: Multi-texture support with UV coordinates
- **Dynamic Coloring**: Real-time color modifications for game elements

## Development Guide

### Extending the Game

#### **Adding New Levels**
```python
# In main.py, add new level objects:
def create_level_3():
    # Load new meshes
    obstacle = Mesh.load_obj('OBJ/new_obstacle.obj')
    # Set transformations
    tr = Transformation3D()
    tr.translation = pyrr.Vector3([x, y, z])
    # Add to level component list
    viewer.add_object_LV3(Object3D(...))
```

#### **Creating Custom Obstacles**
1. **3D Model**: Create OBJ file with your 3D modeling software
2. **Texture**: Add corresponding texture file to `IMG/` directory
3. **Integration**: Load in `main.py` with appropriate transformations
4. **Collision**: Add collision detection logic in `viewerGL.py`

#### **Modifying Physics**
```python
# In viewerGL.py, modify trajectory() method:
def trajectory(self):
    v0 = self.power * SPEED_MULTIPLIER  # Adjust speed
    f = FRICTION_COEFFICIENT           # Adjust friction
    # Modify calculation as needed
```

### Code Style Guidelines
- **PEP 8 Compliance**: Follow Python style guidelines
- **French Comments**: Original comments in French, new comments in English
- **Modular Design**: Keep functionality separated by concern
- **OpenGL Best Practices**: Minimize state changes, use VAOs efficiently

## Troubleshooting

### Common Issues

#### **"No module named 'OpenGL'" Error**
```bash
# Solution: Install PyOpenGL
pip install PyOpenGL PyOpenGL_accelerate
```

#### **GLFW Initialization Failed**
```bash
# On Ubuntu/Debian:
sudo apt-get install libglfw3-dev

# On macOS:
brew install glfw

# Verify installation:
python -c "import glfw; print('GLFW Version:', glfw.get_version())"
```

#### **Black Screen / No Rendering**
- **Check GPU Drivers**: Ensure OpenGL 3.3+ support
- **Verify Assets**: Confirm all files in `IMG/` and `OBJ/` directories exist
- **Console Output**: Check terminal for OpenGL error messages

#### **Performance Issues**
- **Reduce Window Size**: Modify window creation in `viewerGL.py`
- **Lower Texture Quality**: Use smaller texture files
- **Disable VSync**: Set `glfw.swap_interval(0)` in ViewerGL initialization

#### **Input Not Working**
- **Window Focus**: Ensure game window has keyboard focus
- **GLFW Version**: Update to latest PyGLFW version
- **Key Mapping**: Check if your keyboard layout affects key detection

## 📜 License & Credits

### License
This project is licensed under the [MIT License](LICENSE) - see the LICENSE file for details.
