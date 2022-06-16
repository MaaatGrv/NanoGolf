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

    # Initiasiation des programmes graphiques
    program3d_id = glutils.create_program_from_file('Shaders/shader.vert', 'Shaders/shader.frag')
    programGUI_id = glutils.create_program_from_file('Shaders/gui.vert', 'Shaders/gui.frag')
    program2dbar_id = glutils.create_program_from_file('Shaders/bar.vert', 'Shaders/bar.frag')
    program2barkac_id = glutils.create_program_from_file('Shaders/barkac.vert', 'Shaders/barkac.frag')

    #Récupère Tr de Steg mais ne l'affiche pas
    m = Mesh.load_obj('OBJ/stegosaurus.obj')
    m.normalize()
    m.apply_matrix(pyrr.matrix44.create_from_scale([2, 2, 2, 1]))
    tr = Transformation3D()
    tr.translation.y = +0.4
    tr.translation.z = -5
    tr.rotation_center.z = 0.2

    Lim_trou_list = []
    GamePack=[]

    # Ajout de la balle
    m = Mesh.load_obj('OBJ/ball2.obj')
    m.normalize()
    m.apply_matrix(pyrr.matrix44.create_from_scale([0.2, 0.2, 0.2, 1]))
    texture = glutils.load_texture('IMG/ball_red.png')
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, tr)
    viewer.add_object(o)
    GamePack.append(o)

    # Barre rouge de puissance (s'affiche lorsque on appuie sur P)
    m = Mesh()
    Tx=1.5
    p0, p1, p2, p3 = [-2.-Tx, 4.4, 1], [-2.-Tx, 4.1, 1], [-6.-Tx, 4.1, 1], [-6.-Tx, 4.4, 1]
    n, c = [0, 1, 0], [1, 1, 1]
    t0, t1, t2, t3 = [0, 0], [1, 0], [1, 1], [0, 1]
    m.vertices = np.array([[p0 + n + c + t0], [p1 + n + c + t1], [p2 + n + c + t2], [p3 + n + c + t3]], np.float32)
    m.faces = np.array([[0, 1, 2], [0, 2, 3]], np.uint32)
    texture = glutils.load_texture('IMG/white.jpg')
    tr_bar = Transformation3D()
    tr_bar.translation.z = -5
    tr_bar.rotation_center.z = 0.2
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program2dbar_id, texture, tr_bar)
    viewer.add_object(o)
    GamePack.append(o)

    # Arrière plan de la barre rouge
    Tb=0.6
    T2=1.0
    m = Mesh()
    p0, p1, p2, p3 = [Tb, 5.1-T2, 1.1], [Tb, 4.7-T2, 1.1], [-5.3+Tb, 4.7-T2, 1.1], [-5.3+Tb, 5.1-T2, 1.1] # possibilité de mettre y=0
    n, c = [0, 1, 0], [1, 1, 1]
    t0, t1, t2, t3 = [0, 0], [1, 0], [1, 1], [0, 1]
    m.vertices = np.array([[p0 + n + c + t0], [p1 + n + c + t1], [p2 + n + c + t2], [p3 + n + c + t3]], np.float32)
    m.faces = np.array([[0, 1, 2], [0, 2, 3]], np.uint32)
    texture = glutils.load_texture('IMG/white.jpg')
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program2barkac_id, texture, tr)
    viewer.add_object(o)
    GamePack.append(o)

    # Petit triangle permettant de faire fonctionner l'illusion d'optique
    m = Mesh()
    T = 0.1 
    p0, p1, p2, p3 = [-4, 5.05-T2-T, 0.9], [-4, 4.75-T2-T, 0.9], [-3.1, 4.75-T2-T, 0.9], [-3.1, 5.05-T2-T, 0.9]
    n, c = [0, 1, 0], [1, 1, 1]
    t0, t1, t2, t3 = [0, 0], [1, 0], [1, 1], [0, 1]
    m.vertices = np.array([[p0 + n + c + t0], [p1 + n + c + t1], [p2 + n + c + t2], [p3 + n + c + t3]], np.float32)
    m.faces = np.array([[0, 1, 2], [0, 2, 3]], np.uint32)
    texture = glutils.load_texture('IMG/white.jpg')
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program2barkac_id, texture, tr)
    viewer.add_object(o)
    GamePack.append(o)

    # Bouton rejouer
    m=Mesh()
    p0, p1, p2, p3 = [3.1, 5.1-T2, 0.9], [3.1, 4.7-T2, 0.9], [2.2, 4.7-T2, 0.9], [2.2, 5.1-T2, 0.9]
    n, c = [0, 1, 0], [1, 1, 1]
    t0, t1, t2, t3 = [0, 0], [1, 0], [1, 1], [0, 1]
    m.vertices = np.array([[p0 + n + c + t0], [p1 + n + c + t1], [p2 + n + c + t2], [p3 + n + c + t3]], np.float32)
    m.faces = np.array([[0, 1, 2], [0, 2, 3]], np.uint32)
    texture = glutils.load_texture('IMG/white.jpg')
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program2barkac_id, texture, tr)
    viewer.add_object(o)
    GamePack.append(o)

    # Bouton Quitter
    m=Mesh()
    p0, p1, p2, p3 = [3.1, 4.6-T2, 0.9], [3.1, 4.2-T2, 0.9], [2.2, 4.2-T2, 0.9], [2.2, 4.6-T2, 0.9]
    n, c = [0, 1, 0], [1, 1, 1]
    t0, t1, t2, t3 = [0, 0], [1, 0], [1, 1], [0, 1]
    m.vertices = np.array([[p0 + n + c + t0], [p1 + n + c + t1], [p2 + n + c + t2], [p3 + n + c + t3]], np.float32)
    m.faces = np.array([[0, 1, 2], [0, 2, 3]], np.uint32)
    texture = glutils.load_texture('IMG/white.jpg')
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program2barkac_id, texture, tr)
    viewer.add_object(o)
    GamePack.append(o)

    # Quit Button text
    vao = Text.initalize_geometry()
    texture = glutils.load_texture('IMG/fontB.jpg')
    o = Text('QUITTER', np.array([-0.97, 0.7], np.float32), np.array([-0.7, 0.83], np.float32), vao, 2, programGUI_id, texture)
    viewer.add_object(o)
    GamePack.append(o)

    # New Game text
    vao = Text.initalize_geometry()
    texture = glutils.load_texture('IMG/fontB.jpg')
    o = Text('REJOUER', np.array([-0.98, 0.85], np.float32), np.array([-0.7, 0.98], np.float32), vao, 2, programGUI_id, texture)
    viewer.add_object(o)
    GamePack.append(o)

    # Ajout d'une cible

    Pc=5 #Profondeur cible

    m=Mesh()
    p0, p1, p2, p3 = [-0.15, 0.5, Pc], [-0.15, 0.45, Pc], [0.15, 0.45, Pc], [0.15, 0.5, Pc]
    n, c = [0, 1, 0], [1, 1, 1]
    t0, t1, t2, t3 = [0, 0], [1, 0], [1, 1], [0, 1]
    m.vertices = np.array([[p0 + n + c + t0], [p1 + n + c + t1], [p2 + n + c + t2], [p3 + n + c + t3]], np.float32)
    m.faces = np.array([[0, 1, 2], [0, 2, 3]], np.uint32)
    texture = glutils.load_texture('IMG/white.jpg')
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program2barkac_id, texture, tr)
    viewer.add_object(o)
    GamePack.append(o)

    m=Mesh()
    p0, p1, p2, p3 = [-0.025, 0.625, Pc], [-0.025, 0.325, Pc], [0.025, 0.325, Pc], [0.025, 0.625, Pc]
    n, c = [0, 1, 0], [1, 1, 1]
    t0, t1, t2, t3 = [0, 0], [1, 0], [1, 1], [0, 1]
    m.vertices = np.array([[p0 + n + c + t0], [p1 + n + c + t1], [p2 + n + c + t2], [p3 + n + c + t3]], np.float32)
    m.faces = np.array([[0, 1, 2], [0, 2, 3]], np.uint32)
    texture = glutils.load_texture('IMG/white.jpg')
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program2barkac_id, texture, tr)
    viewer.add_object(o)
    GamePack.append(o)

    m = Mesh()
    p0, p1, p2, p3 = [-25, 0, -25], [25, 0, -25], [25, 0, 25], [-25, 0, 25]
    n, c = [0, 1, 0], [1, 1, 1]
    t0, t1, t2, t3 = [0, 0], [1, 0], [1, 1], [0, 1]
    m.vertices = np.array([[p0 + n + c + t0], [p1 + n + c + t1], [p2 + n + c + t2], [p3 + n + c + t3]], np.float32)
    m.faces = np.array([[0, 1, 2], [0, 2, 3]], np.uint32)
    texture = glutils.load_texture('IMG/grass.jpg')
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, Transformation3D())
    viewer.add_object(o)

    m = Mesh.load_obj('OBJ/wall.obj')
    m.normalize()
    m.apply_matrix(pyrr.matrix44.create_from_scale([2, 2, 2, 1])) #changer la taille de la sphere

    collision_box=[]
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
        texture = glutils.load_texture('IMG/bois.png')
        o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, tr)
        viewer.add_object(o)
    
    m = Mesh.load_obj('OBJ/hole_square.obj')
    m.normalize()
    m.apply_matrix(pyrr.matrix44.create_from_scale([2, 2, 2, 1])) #changer la taille de la sphere
    tr = Transformation3D()
    tr.translation.x = 12
    tr.translation.y = 0.2
    tr.translation.z = -5
    tr.rotation_center.z = -2
    texture = glutils.load_texture('IMG/bois.png')
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, tr)
    viewer.add_object(o)
    
    m = Mesh.load_obj('OBJ/flag.obj')
    m.normalize()
    m.apply_matrix(pyrr.matrix44.create_from_scale([2, 2, 2, 1])) #changer la taille de la sphere
    tr = Transformation3D()
    tr.translation.x = 12
    tr.translation.y = 2
    tr.translation.z = -4.3
    tr.rotation_center.z = -2
    texture = glutils.load_texture('IMG/flag_blue.png')
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, tr)
    viewer.add_object(o)

    # Win Text
    vao = Text.initalize_geometry()
    texture = glutils.load_texture('IMG/fontB.jpg')
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

    Lim_Trou=[AABB,CCDD]
    Lim_trou_list.append(Lim_Trou)

    ######################
    ###  THIS IS LV 2  ###
    ######################

    collision_box=[]

    for elmt in GamePack:
        viewer.add_object_LV2(elmt)
    
    m = Mesh()
    p0, p1, p2, p3 = [-50, 0, -50], [50, 0, -50], [50, 0, 50], [-50, 0, 50]
    n, c = [0, 1, 0], [1, 1, 1]
    t0, t1, t2, t3 = [0, 0], [1, 0], [1, 1], [0, 1]
    m.vertices = np.array([[p0 + n + c + t0], [p1 + n + c + t1], [p2 + n + c + t2], [p3 + n + c + t3]], np.float32)
    m.faces = np.array([[0, 1, 2], [0, 2, 3]], np.uint32)
    texture = glutils.load_texture('IMG/moon.jpg')
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, Transformation3D())
    viewer.add_object_LV2(o)

    m = Mesh.load_obj('OBJ/wall.obj')
    m.normalize()
    m.apply_matrix(pyrr.matrix44.create_from_scale([2, 2, 2, 1])) 
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
        texture = glutils.load_texture('IMG/bois.png')
        o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, tr)
        viewer.add_object_LV2(o)
    for i in range(2):
        tr = Transformation3D()
        tr.rotation_euler=(0,0,np.pi/2) #rotation de pi/2
        tr.translation.y = 0.2
        tr.translation.z = -1.2+4*i
        tr.rotation_center.z = 0.2
        tr.translation.x = 11.8
        texture = glutils.load_texture('IMG/bois.png')
        o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, tr)
        viewer.add_object_LV2(o)
    for i in range(6):
        tr = Transformation3D()
        tr.rotation_euler=(0,0,np.pi/2) #rotation de pi/2
        tr.translation.y = 0.2
        tr.translation.z = 9+4*i
        tr.rotation_center.z = 0.2
        tr.translation.x = 11.8
        texture = glutils.load_texture('IMG/bois.png')
        o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, tr)
        viewer.add_object_LV2(o)
    
    m = Mesh.load_obj('OBJ/roundcorner.obj')
    m.normalize()
    m.apply_matrix(pyrr.matrix44.create_from_scale([2, 2, 2, 1])) 
    tr = Transformation3D()
    tr.translation.x = 12
    tr.translation.y = 0.2
    tr.translation.z = -5
    tr.rotation_center.z = -2
    texture = glutils.load_texture('IMG/bois.png')
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, tr)
    viewer.add_object_LV2(o)
    
    m = Mesh.load_obj('OBJ/splitT.obj')
    m.normalize()
    m.apply_matrix(pyrr.matrix44.create_from_scale([2, 2, 2, 1])) 
    tr = Transformation3D()
    tr.rotation_euler=(0,0,-np.pi/2) #rotation de pi/2
    tr.translation.y = 0.2
    tr.translation.z = 6.78
    tr.rotation_center.z = 0.2
    tr.translation.x = 12.2
    texture = glutils.load_texture('IMG/bois.png')
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, tr)
    viewer.add_object_LV2(o)

    m = Mesh.load_obj('OBJ/windwill.obj')
    m.normalize()
    m.apply_matrix(pyrr.matrix44.create_from_scale([3.1, 3.1, 3.1, 1])) 
    tr = Transformation3D()
    tr.rotation_euler=(0,0,-np.pi/2) #rotation de pi/2
    tr.translation.y = 3
    tr.translation.z = 16.9
    tr.rotation_center.z = 0.2
    tr.translation.x = 12.2
    texture = glutils.load_texture('IMG/bois.png')
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, tr)
    viewer.add_object_LV2(o)

    m = Mesh.load_obj('OBJ/tunnel_double.obj')
    m.normalize()
    m.apply_matrix(pyrr.matrix44.create_from_scale([2, 2, 2, 1])) 
    tr = Transformation3D()
    tr.rotation_euler=(0,0,-np.pi/2) #rotation de pi/2
    tr.translation.y = 0.5
    tr.translation.z = 29
    tr.rotation_center.z = 0.2
    tr.translation.x = 12.2
    texture = glutils.load_texture('IMG/bois.png')
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, tr)
    viewer.add_object_LV2(o)
    
    m = Mesh.load_obj('OBJ/hole_open.obj')
    m.normalize()
    m.apply_matrix(pyrr.matrix44.create_from_scale([2, 2, 2, 1])) 
    tr = Transformation3D()
    tr.rotation_euler=(0,0,-np.pi/2) #rotation de pi/2
    tr.translation.y = 0.1
    tr.translation.z = 29
    tr.rotation_center.z = 0.2
    tr.translation.x = -15
    texture = glutils.load_texture('IMG/bois.png')
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, tr)
    viewer.add_object_LV2(o)
    
    m = Mesh.load_obj('OBJ/flag.obj')
    m.normalize()
    m.apply_matrix(pyrr.matrix44.create_from_scale([2, 2, 2, 1])) #changer la taille de la sphere
    tr = Transformation3D()
    tr.translation.x = -15.3
    tr.translation.y = 2
    tr.translation.z = 30
    tr.rotation_center.z = -2
    texture = glutils.load_texture('IMG/flag_blue.png')
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, tr)
    viewer.add_object_LV2(o)

    viewer.run(Lim_trou_list)

if __name__ == '__main__':
    main()