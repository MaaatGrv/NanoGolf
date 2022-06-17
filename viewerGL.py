from tkinter import Y
import OpenGL.GL as GL
import glfw
import pyrr
import numpy as np
from cpe3d import Object3D
from random import randint

class ViewerGL:
    def __init__(self):
        # initialisation de la librairie GLFW
        glfw.init()
        # paramétrage du context OpenGL
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL.GL_TRUE)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        # création et paramétrage de la fenêtre
        glfw.window_hint(glfw.RESIZABLE, False)
        self.window = glfw.create_window(800, 800, 'OpenGL', None, None)
        # paramétrage de la fonction de gestion des évènements
        glfw.set_key_callback(self.window, self.key_callback)
        # activation du context OpenGL pour la fenêtre
        glfw.make_context_current(self.window)
        glfw.swap_interval(1)
        # activation de la gestion de la profondeur
        GL.glEnable(GL.GL_DEPTH_TEST)
        # choix de la couleur de fond
        GL.glClearColor(0.5, 0.6, 0.9, 1.0)
        print(f"OpenGL: {GL.glGetString(GL.GL_VERSION).decode('ascii')}")

        self.objs = []
        self.touch = {}
        self.verif=False
        self.rebond=False
        self.origin= np.array([ 6 ,  0.4, -5. ])

    def run(self):
        # boucle d'affichage
        while not glfw.window_should_close(self.window):
            # nettoyage de la fenêtre : fond et profondeur
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

            self.update_key()
            # self.verif_collision()

            self.trajectory(5)

            for obj in self.objs:
                GL.glUseProgram(obj.program)
                if isinstance(obj, Object3D):
                    self.update_camera(obj.program)
                obj.draw()

            # changement de buffer d'affichage pour éviter un effet de scintillement
            glfw.swap_buffers(self.window)
            # gestion des évènements
            glfw.poll_events()
        
    def key_callback(self, win, key, scancode, action, mods):
        # sortie du programme si appui sur la touche 'échappement'
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(win, glfw.TRUE)
        self.touch[key] = action
    

    #retourner au debut
    def ball_spawn(self):
        self.objs[0].transformation.translation[0]=0.0
        self.objs[0].transformation.translation[1]=0.4
        self.objs[0].transformation.translation[2]=-5.0
        self.objs[0].transformation.rotation_euler[2]= -1.57079633
        
        self.objs[1].transformation.translation[0]=0.0
        self.objs[1].transformation.translation[1]=0.0
        self.objs[1].transformation.translation[2]=-5.0
        self.objs[1].transformation.rotation_euler[2]= -1.57079633

    #teleporte la balle sur la plateforme ou se situe le drapeau
    def goal_flag(self):
        self.objs[0].transformation.translation[0]=-14.29777672 
        self.objs[0].transformation.translation[1]=0.4
        self.objs[0].transformation.translation[2]= 28.27962753
        self.objs[0].transformation.rotation_euler[2]= -1.57079633
        
        
        
    #transporte la balle soit au debut soit au niveau du trou de golf
    def teleportation(self):
        x=randint(1,50)
        y=randint(1,50)
        z=x/y
        if z<=1:
            self.ball_spawn()
        else:
            self.goal_flag()

    def add_object(self, obj):
        self.objs.append(obj)

    def delete_object(self, obj):
       self.objs.remove(obj)
    
    def set_camera(self, cam):
        self.cam = cam

    def update_camera(self, prog):
        GL.glUseProgram(prog)
        # Récupère l'identifiant de la variable pour le programme courant
        loc = GL.glGetUniformLocation(prog, "translation_view")
        # Vérifie que la variable existe
        if (loc == -1) :
            print("Pas de variable uniforme : translation_view")
        # Modifie la variable pour le programme courant
        translation = -self.cam.transformation.translation
        GL.glUniform4f(loc, translation.x, translation.y, translation.z, 0)

        # Récupère l'identifiant de la variable pour le programme courant
        loc = GL.glGetUniformLocation(prog, "rotation_center_view")
        # Vérifie que la variable existe
        if (loc == -1) :
            print("Pas de variable uniforme : rotation_center_view")
        # Modifie la variable pour le programme courant
        rotation_center = self.cam.transformation.rotation_center
        GL.glUniform4f(loc, rotation_center.x, rotation_center.y, rotation_center.z, 0)

        rot = pyrr.matrix44.create_from_eulers(-self.cam.transformation.rotation_euler)
        loc = GL.glGetUniformLocation(prog, "rotation_view")
        if (loc == -1) :
            print("Pas de variable uniforme : rotation_view")
        GL.glUniformMatrix4fv(loc, 1, GL.GL_FALSE, rot)
    
        loc = GL.glGetUniformLocation(prog, "projection")
        if (loc == -1) :
            print("Pas de variable uniforme : projection")
        GL.glUniformMatrix4fv(loc, 1, GL.GL_FALSE, self.cam.projection)

    def update_key(self):
        if glfw.KEY_UP in self.touch and self.touch[glfw.KEY_UP] > 0:

            self.objs[0].transformation.translation += \
               pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[0].transformation.rotation_euler), pyrr.Vector3([0, 0, 0.2]))   
            print(self.objs[0].transformation.translation)   
        if glfw.KEY_DOWN in self.touch and self.touch[glfw.KEY_DOWN] > 0:
            self.objs[0].transformation.translation -= \
                pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[0].transformation.rotation_euler), pyrr.Vector3([0, 0, 0.02]))
        if glfw.KEY_LEFT in self.touch and self.touch[glfw.KEY_LEFT] > 0:
            self.objs[0].transformation.rotation_euler[pyrr.euler.index().yaw] -= 0.1

        if glfw.KEY_RIGHT in self.touch and self.touch[glfw.KEY_RIGHT] > 0:
            self.objs[0].transformation.rotation_euler[pyrr.euler.index().yaw] += 0.1

        if glfw.KEY_I in self.touch and self.touch[glfw.KEY_I] > 0:
            self.cam.transformation.rotation_euler[pyrr.euler.index().roll] -= 0.1
        if glfw.KEY_K in self.touch and self.touch[glfw.KEY_K] > 0:
            self.cam.transformation.rotation_euler[pyrr.euler.index().roll] += 0.1
        if glfw.KEY_J in self.touch and self.touch[glfw.KEY_J] > 0:
            self.cam.transformation.rotation_euler[pyrr.euler.index().yaw] -= 0.1
        if glfw.KEY_L in self.touch and self.touch[glfw.KEY_L] > 0:
            self.cam.transformation.rotation_euler[pyrr.euler.index().yaw] += 0.1


        self.cam.transformation.rotation_euler = self.objs[0].transformation.rotation_euler.copy() 
        self.cam.transformation.rotation_euler[pyrr.euler.index().yaw] += np.pi
        self.cam.transformation.rotation_center = self.objs[0].transformation.translation + self.objs[0].transformation.rotation_center
        self.cam.transformation.translation = self.objs[0].transformation.translation + pyrr.Vector3([0, 1, 5])

    def verif_collision(self):
        x=self.objs[0].transformation.translation[0]
        y=self.objs[0].transformation.translation[1]
        z=self.objs[0].transformation.translation[2]
        #premiére zone de collision 
        if z<= -3.87759959 : #Faire des exceptions dans le rectangle de collision 
            pass
        #deuxième zone de collision
        # if x <= -1.25192378:
        #     self.objs[0].transformation.rotation_euler[pyrr.euler.index().yaw] +=0.5
        # if x>= 13.22652818:
        #     self.objs[0].transformation.rotation_euler[pyrr.euler.index().yaw] -=0.5

        #SplitT
        elif (x>= 13.41981779 and x<= 10.73907768 and z== 8.28156984):
            self.objs[0].transformation.rotation_euler[pyrr.euler.index().yaw] -=0.5
        elif (x>= 13.41981779 and x<= 10.73907768 and z== 9.40632919):
            self.objs[0].transformation.rotation_euler[pyrr.euler.index().yaw] -=0.5




    def zone_collision_1(self):
        x=self.objs[0].transformation.translation[0]
        y=self.objs[0].transformation.translation[1]
        z=self.objs[0].transformation.translation[2]
        H=np.array([x,self.origin[1],self.origin[2]]) #projeter de l'origine 
        dist1 = np.linalg.norm(self.objs[0].transformation.translation-self.origin)
        dist2= np.linalg.norm(H-self.origin)
        angle=np.arccos(dist2/dist1)
        print("angle",angle)
        self.objs[0].transformation.rotation_euler[pyrr.euler.index().yaw] -= angle

    
    def zone_collision_2(self):
        pass
    
    def zone_collision_3(self):
        pass
    
    def zone_collision_4(self):
        pass
    
    def zone_collision_5(self):
        pass
    
    def zone_collision_6(self):
        pass
    
    def zone_collision_7(self): 
        pass
    
    def trajectory(self,a):
        b=0
        if self.verif:
            while a-b>0:
                self.objs[0].transformation.translation += \
                    pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[0].transformation.rotation_euler), pyrr.Vector3([0, 0, 0.02]))
                b+=1


            
