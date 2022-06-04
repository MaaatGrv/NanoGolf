from curses.textpad import rectangle
from viewerGL import ViewerGL
import glutils
from mesh import Mesh
from cpe3d import Object3D, Camera, Transformation3D, Text
import numpy as np
import OpenGL.GL as GL
import pyrr

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

    m = Mesh.load_obj('stegosaurus.obj')
    m.normalize()
    m.apply_matrix(pyrr.matrix44.create_from_scale([2, 2, 2, 1]))
    tr = Transformation3D()
    tr.translation.y = -np.amin(m.vertices, axis=0)[1]
    tr.translation.z = -5
    tr.rotation_center.z = 0.2
    texture = glutils.load_texture('stegosaurus.jpg')
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, tr)
    viewer.add_object(o)


    # This is the front of the bar
    m = Mesh()
    p0, p1, p2, p3 = [-2.7, 0, 1], [-2.7, -4, 1], [-2.4, -4, 1], [-2.4, 0, 1]
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
    m = Mesh()
    p0, p1, p2, p3 = [-2.79, 3.1, 1.1], [-2.79, -2.2, 1.1], [-2.4, -2.2, 1.1], [-2.4, 3.1, 1.1] # possibilité de mettre y=0
    n, c = [0, 1, 0], [1, 1, 1]
    t0, t1, t2, t3 = [0, 0], [1, 0], [1, 1], [0, 1]
    m.vertices = np.array([[p0 + n + c + t0], [p1 + n + c + t1], [p2 + n + c + t2], [p3 + n + c + t3]], np.float32)
    m.faces = np.array([[0, 1, 2], [0, 2, 3]], np.uint32)
    texture = glutils.load_texture('white.jpg')
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program2barkac_id, texture, tr)
    viewer.add_object(o)

    # Add a little white triangle in front
    m = Mesh()
    T = tr.translation.y 
    p0, p1, p2, p3 = [-2.69, 0.07-T, 0.9], [-2.69, 0-T, 0.9], [-2.315, 0-T, 0.9], [-2.315, 0.07-T, 0.9]
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

    # vao = Text.initalize_geometry()
    # texture = glutils.load_texture('fontB.jpg')
    # o = Text('Bonjour les', np.array([-0.8, 0.3], np.float32), np.array([0.8, 0.8], np.float32), vao, 2, programGUI_id, texture)
    # viewer.add_object(o)
    # o = Text('3ETI', np.array([-0.5, -0.2], np.float32), np.array([0.5, 0.3], np.float32), vao, 2, programGUI_id, texture)
    # viewer.add_object(o)

    viewer.run()


if __name__ == '__main__':
    main()