from matplotlib.pyplot import axis
from viewerGL import ViewerGL
import glutils
from mesh import Mesh
from cpe3d import Object3D, Camera, Transformation3D, Text
import numpy as np
import OpenGL.GL as GL
import pyrr
import time,glfw

def main():
    viewer = ViewerGL()



    viewer.set_camera(Camera())
    viewer.cam.transformation.translation.y = 2
    viewer.cam.transformation.rotation_center = viewer.cam.transformation.translation.copy()

    program3d_id = glutils.create_program_from_file('shader.vert', 'shader.frag')
    programGUI_id = glutils.create_program_from_file('gui.vert', 'gui.frag')

    collision_box=[]

    m = Mesh.load_obj('ball2.obj')
    m.normalize()
    m.apply_matrix(pyrr.matrix44.create_from_scale([0.2, 0.2, 0.2, 1])) #changer la taille de la sphere
    tr = Transformation3D()
    tr.translation.y = 0.4
    tr.translation.z = -5
    tr.rotation_center.z = 0.2
    texture = glutils.load_texture('ball_red.png')
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, tr)
    viewer.add_object(o)



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
    



    m = Mesh()
    p0, p1, p2, p3 = [-25, 0, -25], [25, 0, -25], [25, 0, 25], [-25, 0, 25]
    n, c = [0, 1, 0], [1, 1, 1]
    t0, t1, t2, t3 = [0, 0], [1, 0], [1, 1], [0, 1]
    m.vertices = np.array([[p0 + n + c + t0], [p1 + n + c + t1], [p2 + n + c + t2], [p3 + n + c + t3]], np.float32)
    m.faces = np.array([[0, 1, 2], [0, 2, 3]], np.uint32)
    texture = glutils.load_texture('grass.jpg')
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, Transformation3D())
    viewer.add_object(o)
    
    
    

    vao = Text.initalize_geometry()
    texture = glutils.load_texture('fontB.jpg')
    o = Text('Nano ', np.array([-0.8, 0.3], np.float32), np.array([0.8, 0.8], np.float32), vao, 2, programGUI_id, texture)
    viewer.add_object(o)


    o = Text('Golf', np.array([-0.5, -0.2], np.float32), np.array([0.5, 0.3], np.float32), vao, 2, programGUI_id, texture)
    viewer.add_object(o)


    viewer.run()


if __name__ == '__main__':
    main()