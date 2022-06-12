from curses.textpad import rectangle
from viewerGL import ViewerGL
import glutils
from mesh import Mesh
from cpe3d import Object3D, Camera, Transformation3D, Text
import numpy as np
import OpenGL.GL as GL
import pyrr
import time
import glfw
from multiprocessing import Process, Queue, Pipe

def main():
    viewer = ViewerGL()

    viewer.set_camera(Camera())
    viewer.cam.transformation.rotation_euler = viewer.cam.transformation.rotation_euler.copy()
    viewer.cam.transformation.rotation_euler[pyrr.euler.index().yaw] = np.pi
    viewer.cam.transformation.rotation_center = viewer.cam.transformation.translation + viewer.cam.transformation.rotation_center
    viewer.cam.transformation.translation = viewer.cam.transformation.translation + pyrr.Vector3([0, 1, 9.6])

    program3d_id = glutils.create_program_from_file('shader.vert', 'shader.frag')
    programGUI_id = glutils.create_program_from_file('gui.vert', 'gui.frag')
    program2dbar_id = glutils.create_program_from_file('bar.vert', 'bar.frag')
    program2barkac_id = glutils.create_program_from_file('barkac.vert', 'barkac.frag')

    #Récupère Tr de Steg mais ne l'affiche pas
    m = Mesh.load_obj('stegosaurus.obj')
    m.normalize()
    m.apply_matrix(pyrr.matrix44.create_from_scale([2, 2, 2, 1]))
    tr = Transformation3D()
    tr.translation.y = +0.4
    tr.translation.z = -5
    tr.rotation_center.z = 0.2

    # Ajout de la balle
    m = Mesh.load_obj('ball2.obj')
    m.normalize()
    m.apply_matrix(pyrr.matrix44.create_from_scale([0.2, 0.2, 0.2, 1]))
    texture = glutils.load_texture('ball_red.png')
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, tr)
    viewer.add_object(o)

    # This is the front of the bar
    m = Mesh()
    Tx=1.5
    p0, p1, p2, p3 = [-2.-Tx, 4.4, 1], [-2.-Tx, 4.1, 1], [-6.-Tx, 4.1, 1], [-6.-Tx, 4.4, 1]
    n, c = [0, 1, 0], [1, 1, 1]
    t0, t1, t2, t3 = [0, 0], [1, 0], [1, 1], [0, 1]
    m.vertices = np.array([[p0 + n + c + t0], [p1 + n + c + t1], [p2 + n + c + t2], [p3 + n + c + t3]], np.float32)
    m.faces = np.array([[0, 1, 2], [0, 2, 3]], np.uint32)
    texture = glutils.load_texture('white.jpg')
    tr_bar = Transformation3D()
    tr_bar.translation.z = -5
    tr_bar.rotation_center.z = 0.2
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program2dbar_id, texture, tr_bar)
    viewer.add_object(o)

    # This is the back of the bar
    Tb=0.6 # Add translation to set it up
    T2=1.0
    m = Mesh()
    p0, p1, p2, p3 = [Tb, 5.1-T2, 1.1], [Tb, 4.7-T2, 1.1], [-5.3+Tb, 4.7-T2, 1.1], [-5.3+Tb, 5.1-T2, 1.1] # possibilité de mettre y=0
    n, c = [0, 1, 0], [1, 1, 1]
    t0, t1, t2, t3 = [0, 0], [1, 0], [1, 1], [0, 1]
    m.vertices = np.array([[p0 + n + c + t0], [p1 + n + c + t1], [p2 + n + c + t2], [p3 + n + c + t3]], np.float32)
    m.faces = np.array([[0, 1, 2], [0, 2, 3]], np.uint32)
    texture = glutils.load_texture('white.jpg')
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program2barkac_id, texture, tr)
    viewer.add_object(o)

    # Add a little white triangle in front
    m = Mesh()
    T = 0.1 
    p0, p1, p2, p3 = [-4, 5.05-T2-T, 0.9], [-4, 4.75-T2-T, 0.9], [-3.1, 4.75-T2-T, 0.9], [-3.1, 5.05-T2-T, 0.9]
    n, c = [0, 1, 0], [1, 1, 1]
    t0, t1, t2, t3 = [0, 0], [1, 0], [1, 1], [0, 1]
    m.vertices = np.array([[p0 + n + c + t0], [p1 + n + c + t1], [p2 + n + c + t2], [p3 + n + c + t3]], np.float32)
    m.faces = np.array([[0, 1, 2], [0, 2, 3]], np.uint32)
    texture = glutils.load_texture('white.jpg')
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program2barkac_id, texture, tr)
    viewer.add_object(o)

    #Add some buttons

    # New Game Button
    m=Mesh()
    p0, p1, p2, p3 = [3.1, 5.1-T2, 0.9], [3.1, 4.7-T2, 0.9], [2.2, 4.7-T2, 0.9], [2.2, 5.1-T2, 0.9]
    n, c = [0, 1, 0], [1, 1, 1]
    t0, t1, t2, t3 = [0, 0], [1, 0], [1, 1], [0, 1]
    m.vertices = np.array([[p0 + n + c + t0], [p1 + n + c + t1], [p2 + n + c + t2], [p3 + n + c + t3]], np.float32)
    m.faces = np.array([[0, 1, 2], [0, 2, 3]], np.uint32)
    texture = glutils.load_texture('white.jpg')
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program2barkac_id, texture, tr)
    viewer.add_object(o)

    # Quit Button
    m=Mesh()
    p0, p1, p2, p3 = [3.1, 4.6-T2, 0.9], [3.1, 4.2-T2, 0.9], [2.2, 4.2-T2, 0.9], [2.2, 4.6-T2, 0.9]
    n, c = [0, 1, 0], [1, 1, 1]
    t0, t1, t2, t3 = [0, 0], [1, 0], [1, 1], [0, 1]
    m.vertices = np.array([[p0 + n + c + t0], [p1 + n + c + t1], [p2 + n + c + t2], [p3 + n + c + t3]], np.float32)
    m.faces = np.array([[0, 1, 2], [0, 2, 3]], np.uint32)
    texture = glutils.load_texture('white.jpg')
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program2barkac_id, texture, tr)
    viewer.add_object(o)

    # Quit Button text
    vao = Text.initalize_geometry()
    texture = glutils.load_texture('fontB.jpg')
    o = Text('QUITTER', np.array([-0.97, 0.7], np.float32), np.array([-0.7, 0.83], np.float32), vao, 2, programGUI_id, texture)
    viewer.add_object(o)

    # New Game text
    vao = Text.initalize_geometry()
    texture = glutils.load_texture('fontB.jpg')
    o = Text('REJOUER', np.array([-0.98, 0.85], np.float32), np.array([-0.7, 0.98], np.float32), vao, 2, programGUI_id, texture)
    viewer.add_object(o)

    # Add a aim
    Pc=5 #Profondeur cible

    m=Mesh()
    p0, p1, p2, p3 = [-0.15, 0.5, Pc], [-0.15, 0.45, Pc], [0.15, 0.45, Pc], [0.15, 0.5, Pc]
    n, c = [0, 1, 0], [1, 1, 1]
    t0, t1, t2, t3 = [0, 0], [1, 0], [1, 1], [0, 1]
    m.vertices = np.array([[p0 + n + c + t0], [p1 + n + c + t1], [p2 + n + c + t2], [p3 + n + c + t3]], np.float32)
    m.faces = np.array([[0, 1, 2], [0, 2, 3]], np.uint32)
    texture = glutils.load_texture('white.jpg')
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program2barkac_id, texture, tr)
    viewer.add_object(o)

    m=Mesh()
    p0, p1, p2, p3 = [-0.025, 0.625, Pc], [-0.025, 0.325, Pc], [0.025, 0.325, Pc], [0.025, 0.625, Pc]
    n, c = [0, 1, 0], [1, 1, 1]
    t0, t1, t2, t3 = [0, 0], [1, 0], [1, 1], [0, 1]
    m.vertices = np.array([[p0 + n + c + t0], [p1 + n + c + t1], [p2 + n + c + t2], [p3 + n + c + t3]], np.float32)
    m.faces = np.array([[0, 1, 2], [0, 2, 3]], np.uint32)
    texture = glutils.load_texture('white.jpg')
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program2barkac_id, texture, tr)
    viewer.add_object(o)

    m = Mesh()
    p0, p1, p2, p3 = [-25, 0, -25], [25, 0, -25], [25, 0, 25], [-25, 0, 25]
    n, c = [0, 1, 0], [1, 1, 1]
    t0, t1, t2, t3 = [0, 0], [1, 0], [1, 1], [0, 1]
    m.vertices = np.array([[p0 + n + c + t0], [p1 + n + c + t1], [p2 + n + c + t2], [p3 + n + c + t3]], np.float32)
    m.faces = np.array([[0, 1, 2], [0, 2, 3]], np.uint32)
    texture = glutils.load_texture('grass.jpg')
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, Transformation3D())
    viewer.add_object(o)

    collision_box=[]

    m = Mesh.load_obj('wall.obj')
    m.normalize()
    m.apply_matrix(pyrr.matrix44.create_from_scale([2, 2, 2, 1])) #changer la taille de la sphere

    for i in range(3):
        tr = Transformation3D()
        tr.translation.y = 0.2
        tr.translation.z = -5
        tr.rotation_center.z = 0.2
        tr.translation.x = 4*i
        wmin=np.amin(m.vertices,axis=0)[:3]
        wmax=np.amax(m.vertices,axis=0)[:3]
        collision_box.append([wmin[0],wmin[2],wmin[0]+4*i,wmin[2]-5]) #recuperer les valeurs min  de notre objet
        collision_box.append([wmax[0],wmax[2],wmax[0]+4*i,wmax[2]-5]) #recuperer les valeurs max  de notre objet
        texture = glutils.load_texture('bois.png')
        o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, tr)
        viewer.add_object(o)
    
    m = Mesh.load_obj('hole_square.obj')
    m.normalize()
    m.apply_matrix(pyrr.matrix44.create_from_scale([2, 2, 2, 1])) #changer la taille de la sphere
    tr = Transformation3D()
    tr.translation.x = 12
    tr.translation.y = 0.2
    tr.translation.z = -5
    tr.rotation_center.z = -2
    texture = glutils.load_texture('bois.png')
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, tr)
    viewer.add_object(o)
    
    m = Mesh.load_obj('flag.obj')
    m.normalize()
    m.apply_matrix(pyrr.matrix44.create_from_scale([2, 2, 2, 1])) #changer la taille de la sphere
    tr = Transformation3D()
    tr.translation.x = 12
    tr.translation.y = 2

    tr.translation.z = -4.3
    tr.rotation_center.z = -2
    texture = glutils.load_texture('flag_blue.png')
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, tr)
    viewer.add_object(o)

    # Win Text
    vao = Text.initalize_geometry()
    texture = glutils.load_texture('fontB.jpg')
    o = Text('Felicitations',  np.array([-0.5, -0.2], np.float32), np.array([0.5, 0.3], np.float32), vao, 2, programGUI_id, texture)
    viewer.add_future_object(o)

    minaabb=np.amin(m.vertices,axis=0)[:3]
    maxaabb=np.amax(m.vertices,axis=0)[:3]
    AABB=[minaabb, maxaabb]
    CCDD=[[0,0,0],[0,0,0]]
    AABB[0][0]=AABB[0][0]+12
    AABB[1][0]=AABB[1][0]+12
    AABB[0][2]=AABB[0][2]-4.3
    AABB[1][2]=AABB[1][2]-4.3
    CCDD[0][0]=AABB[0][0]
    CCDD[1][0]=AABB[1][0]+2*(maxaabb[0]-12)
    CCDD[0][2]=AABB[0][2]+(minaabb[2]+4.3) 
    CCDD[1][2]=AABB[1][2]

    viewer.run(AABB,CCDD)

def menu():
    window = ViewerGL()
    window.set_camera(Camera)
    window.run()

if __name__ == '__main__':
    main()