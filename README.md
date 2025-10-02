# NanoGolf 🏌️‍♂️⛳

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)  
[![OpenGL](https://img.shields.io/badge/OpenGL-Rendering-green.svg)](https://www.opengl.org/)  
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)  

NanoGolf is a lightweight 3D mini-golf / golf simulation project written in Python, integrating **OpenGL** and **GLSL shaders**.  
It’s a fun demo showcasing mesh rendering, shaders, and interactive controls.

## ✨ Features

- 3D mesh rendering (terrain, obstacles)  
- Custom GLSL shaders for visual effects  
- Interactive camera & ball physics  
- Collision detection & simple physics  
- Modular design for meshes, shaders, and gameplay  

## 📂 Project Structure

````
NanoGolf/
├── IMG/                 # Textures & images
├── OBJ/                 # 3D mesh files
├── Shaders/             # GLSL shader programs
├── cpe3d.py             # Core 3D / camera utilities
├── glutils.py           # OpenGL helpers
├── mesh.py              # Mesh loader
├── viewerGL.py          # Rendering loop
├── main.py              # Game entry point
└── mp1.py / mp2.py      # Extra modules / experiments
````

## ⚙️ Dependencies

- Python 3.x  
- [PyOpenGL](https://pypi.org/project/PyOpenGL/)  
- [GLFW](https://www.glfw.org/) (via PyGLFW)  
- [NumPy](https://numpy.org/)  
- [Pillow](https://pypi.org/project/Pillow/) (for textures)

## 🚀 Installation & Setup

1. Clone the repo:
 ```bash
 git clone https://github.com/MaaatGrv/NanoGolf.git
 cd NanoGolf
```
2. (Optional) Create a virtual environment:

 ```bash
 python3 -m venv venv
 source venv/bin/activate   # Linux / macOS
 # venv\Scripts\activate    # Windows
 ```

3. Install dependencies:

 ```bash
 pip install -r requirements.txt
 ```

*(If missing, install manually: `pip install PyOpenGL PyGLFW numpy Pillow`)*

4. Run:

 ```bash
 python main.py
 ```

## 🎮 Controls

* **Mouse** → Rotate / pan camera
* **W / A / S / D** → Move camera
* **Space / Click** → Launch the ball
* **R** → Reset ball / level
* **Esc / Q** → Quit


## 🛠️ Development Notes / TODOs

* Improve power bar UI & HUD
* Add more levels & obstacles
* Polish physics & collisions
* Add sounds & particle effects
* Performance optimizations


## 📜 License

This project is licensed under the [MIT License](LICENSE)
