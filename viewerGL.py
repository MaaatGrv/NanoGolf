#!/usr/bin/env python3

import multiprocessing
from operator import length_hint
from tkinter import Menu
from turtle import update
import OpenGL.GL as GL
import glfw
import pyrr
import numpy as np
from cpe3d import Object3D, Text
import time
from multiprocessing import Process, Queue, Pipe
import math
import glutils

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
        self.window = glfw.create_window(800, 800, 'NanoGolf', None, None)
        # paramétrage de la fonction de gestion des évènements
        glfw.set_key_callback(self.window, self.key_callback)
        glfw.set_mouse_button_callback(self.window, self.mouse_button_callback)
        # activation du context OpenGL pour la fenêtre
        glfw.make_context_current(self.window)
        glfw.swap_interval(1)
        # activation de la gestion de la profondeur
        GL.glEnable(GL.GL_DEPTH_TEST)
        # choix de la couleur de fond
        GL.glClearColor(0.5, 0.6, 0.9, 1.0)
        print(f"NanoGolf: {GL.glGetString(GL.GL_VERSION).decode('ascii')}")

        self.objs = []
        self.new_scene=[]
        self.touch = {}
        self.power=0.0
        self.length=0.0
        self.downlength=0.0
        self.menu = 0
        self.verif=False
        self.rebond=False
        self.origin= np.array([ 6 ,  0.4, -5. ])
        self.shot=0
        self.t0=0
        self.t1=0
        self.translation=[]
        self.rotation=[]
        self.replay = False
        self.removed = []
        self.to_add=[]
        self.WinTextAdded = False
        self.start=0
        self.end=0
        self.coups=0
        self.shooting=False
        self.gravity=False

    def run(self,L1,L2):
        self.init_context()
        # boucle d'affichage
        while not glfw.window_should_close(self.window):
            # nettoyage de la fenêtre : fond et profondeur
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

            self.update_key()
            self.verif_collision()
            self.trajectory()
            self.toucher_drapeau(L1,L2)
            self.gravity_fall()

            # Gestion du timer pour le Win Text
            if self.WinTextAdded == True :
                if self.start ==0:
                    self.start = time.time()
                self.end = time.time()
                if self.start != 0 :
                    if self.end-self.start > 3 :
                        self.delete_object(self.objs[-1])
                        self.WinTextAdded = False
                        self.start=0
                        self.replay_game()

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

        if key == glfw.KEY_P and action == glfw.RELEASE:
            print("Puissance finale", self.power)
            time.sleep(1)
            self.objs[1].transformation.translation -= \
                pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[1].transformation.rotation_euler), pyrr.Vector3([self.downlength, 0, 0,]))
            self.downlength = 0.0
            self.shot=0
            self.shooting=True
            self.coups+=1
            self.display_coups()

        if key == glfw.KEY_P and action == glfw.PRESS:
            self.power = 0.0
            self.length = 0.0
            self.shooting=False

        if key == glfw.KEY_Q and action == glfw.PRESS:
            self.coups+=1

        if key == glfw.KEY_W and action == glfw.PRESS:
            pass

    def collision(self,L):
        Xmin=[]
        Xmax=[]
        Zmin=[]
        Zmax=[]
        for i in range(0,len(L)-1):
            Xmin.append(L[i][2])
            Xmax.append(L[i+1][2])
            Zmin.append(L[i][3])
            Zmax.append(L[i+1][3])
        return Xmin,Xmax,Zmin,Zmax
    
    def send_length(self, length):
        pass

    def add_object(self, obj):
        self.objs.append(obj)
        if not self.WinTextAdded :
            if not self.replay :
                self.new_scene.append(obj)
    
    def add_future_object(self, obj):
        self.to_add.append(obj)

    def set_camera(self, cam):
        self.cam = cam
    
    def delete_object(self, obj):
        self.removed.append(obj)
        self.objs.remove(obj)

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


    def toucher_drapeau(self, L1, L2):
        xmin,xmax,zmin,zmax = [],[],[],[]
        xmin.append(L1[0][0])
        xmax.append(L2[1][0])
        zmax.append(L1[1][2])
        zmin.append(L2[0][2])
        if len(self.objs) > 0:
            if self.objs[0].transformation.translation[0]>xmin[0] and self.objs[0].transformation.translation[0]<xmax[0] and self.objs[0].transformation.translation[2]>zmin[0] and self.objs[0].transformation.translation[2]<zmax[0] and self.WinTextAdded==False :
                self.add_object(self.to_add[0])
                self.WinTextAdded=True
                self.power=0.0
                self.objs[0].transformation.translation[1]=0.0
                self.objs[1].transformation.translation[1]=0.0
                self.update_cam()
    
    def update_cam(self):
        #Adaptation de la caméra
        self.cam.transformation.rotation_euler = self.objs[0].transformation.rotation_euler.copy() 
        self.cam.transformation.rotation_euler[pyrr.euler.index().yaw] += np.pi
        self.cam.transformation.rotation_center = self.objs[0].transformation.translation + self.objs[0].transformation.rotation_center
        self.cam.transformation.translation = self.objs[0].transformation.translation + pyrr.Vector3([0, 1, 5])

    def update_key(self):
        if glfw.KEY_UP in self.touch and self.touch[glfw.KEY_UP] > 0:
            self.mvmt_translation(0.02)
        if glfw.KEY_DOWN in self.touch and self.touch[glfw.KEY_DOWN] > 0:
            self.mvmt_translation(-0.02)

        if glfw.KEY_LEFT in self.touch and self.touch[glfw.KEY_LEFT] > 0:
            self.mvmt_rotation(-0.05)
        if glfw.KEY_RIGHT in self.touch and self.touch[glfw.KEY_RIGHT] > 0:
            self.mvmt_rotation(0.05)
            
        if glfw.KEY_I in self.touch and self.touch[glfw.KEY_I] > 0:
            self.cam.transformation.rotation_euler[pyrr.euler.index().roll] -= 0.1
        if glfw.KEY_K in self.touch and self.touch[glfw.KEY_K] > 0:
            self.cam.transformation.rotation_euler[pyrr.euler.index().roll] += 0.1
        if glfw.KEY_J in self.touch and self.touch[glfw.KEY_J] > 0:
            self.cam.transformation.rotation_euler[pyrr.euler.index().yaw] -= 0.1
        if glfw.KEY_L in self.touch and self.touch[glfw.KEY_L] > 0:
            self.cam.transformation.rotation_euler[pyrr.euler.index().yaw] += 0.1

        if glfw.KEY_SPACE in self.touch and self.touch[glfw.KEY_SPACE] > 0:
            self.cam.transformation.rotation_euler = self.objs[0].transformation.rotation_euler.copy() 
            self.cam.transformation.rotation_euler[pyrr.euler.index().yaw] += np.pi
            self.cam.transformation.rotation_center = self.objs[0].transformation.translation + self.objs[0].transformation.rotation_center
            self.cam.transformation.translation = self.objs[0].transformation.translation + pyrr.Vector3([0, 1, 5])

        if glfw.KEY_P in self.touch and self.touch[glfw.KEY_P] > 0:
            self.calculate_bar_length()
            if self.power  < 100:
                self.power+=1.2
            else:
                self.power = 100
            if self.length < 5:
                self.objs[1].transformation.translation += \
                pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[1].transformation.rotation_euler), pyrr.Vector3([0.048, 0, 0,]))
                self.downlength+=0.048

    def calculate_bar_length(self):
        lmax = 5
        powermax=100
        if self.power  < powermax:
            self.length = (self.power*lmax)/powermax
        else :
            self.length = lmax
    
    # Initialise la position de la balle
    def init_context(self):
        self.objs[0].transformation.rotation_euler[pyrr.euler.index().yaw] -= np.pi/2
        self.objs[1].transformation.rotation_euler[pyrr.euler.index().yaw] -= np.pi/2
        self.update_cam()   

    # Vérifie que le curseur de la souris est situé sur le bouton
    def verif_mouse_pos(self,A,B,C):
        xpos,ypos=glfw.get_cursor_pos(self.window)
        if A[0] < xpos and B[0] > xpos and A[1] < ypos and C[1] > ypos:
            return True
        else:
            return False

    def mouse_button_callback(self, window, button, action, mods):
        if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
            # Détection des boutons :

            #Bouton 1
            A1,B1,C1=[11,11],[120,11],[120,58]
            #Bouton 2
            A2,B2,C2=[11,75],[120,75],[120,120]

            xpos,ypos=glfw.get_cursor_pos(self.window)

            if self.verif_mouse_pos(A1,B1,C1) == True:
                print("Bouton Rejouer")
                self.replay_game()

            if self.verif_mouse_pos(A2,B2,C2) == True:
                print('Bouton Quitter')
                glfw.set_window_should_close(window, glfw.TRUE)

    # Gestion des collisions
    def verif_collision(self):
        if not self.replay:
            if len(self.objs) > 0:
                if self.objs[0].transformation.translation[2] <=-6.59623226 or self.objs[0].transformation.translation[2] >=-3.87759959:
                    H=np.array([self.objs[0].transformation.translation[0],self.origin[1],self.origin[2]]) #projeter de l'origine 
                    dist1 = np.linalg.norm(self.objs[0].transformation.translation-self.origin)
                    dist2= np.linalg.norm(H-self.origin)
                    angle=np.arccos(dist2/dist1)
                    self.mvmt_rotation(-angle)

                if self.objs[0].transformation.translation[0] <= -1.25192378:
                    self.mvmt_rotation(0.5)
                if self.objs[0].transformation.translation[0] >= 13.22652818:
                    self.mvmt_translation(-0.5)
    
    def go_to_origin(self):
        for i in range(len(self.objs)):
            self.delete_object(self.objs[0])
        for i in range(len(self.new_scene)):
            self.add_object(self.new_scene[i])
            print('add')

    # Gestion du mouvement de la balle
    def trajectory(self):
        if not self.WinTextAdded:
            if self.shooting:
                self.shot+=0.5
                if self.shot < self.power:
                    self.t1=time.time()
                    # Variables
                    v0= self.power * 0.8
                    f=30.0
                    m=0.05
                    Tau=m/f
                    tr = Tau*v0*(math.exp((-self.t0)/Tau)-math.exp((-self.t1)/Tau))
                    self.mvmt_translation(tr)
                self.tO=time.time()

    def mvmt_translation(self,tr):
        self.objs[0].transformation.translation += \
            pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[0].transformation.rotation_euler), pyrr.Vector3([0, 0, tr]))
        self.objs[1].transformation.translation += \
            pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[1].transformation.rotation_euler), pyrr.Vector3([0, 0, tr]))
        self.update_cam()
        self.translation.append(tr)
    
    def mvmt_rotation(self,angle):
        self.objs[0].transformation.rotation_euler[pyrr.euler.index().yaw] += angle
        self.objs[1].transformation.rotation_euler[pyrr.euler.index().yaw] += angle
        self.update_cam()
        self.rotation.append(angle)
    
    def display_coups(self):
        n=0
        programGUI_id = glutils.create_program_from_file('gui.vert', 'gui.frag')
        vao = Text.initalize_geometry()
        texture = glutils.load_texture('fontB.jpg')
        o = Text('Coups:' + str(self.coups), np.array([-0.3, -0.98], np.float32), np.array([0.3, -0.7], np.float32), vao, 2, programGUI_id, texture)

        if self.coups == 0 and self.replay == True:
            self.delete_object(self.objs[-1])

        if self.coups > 0:
            if self.WinTextAdded == False :
                if self.coups > 1:
                    self.delete_object(self.objs[-1])
                self.add_object(o)
            else :
                while self.WinTextAdded == True :
                    n+=1
                if self.coups > 1:
                    self.delete_object(self.objs[-1])
                self.add_object(o)
    
    def replay_game(self):
        if self.coups > 0:
            self.replay=True
            self.coups=0
            self.display_coups()
            
            self.objs[0].transformation.translation[0]=0.0
            self.objs[0].transformation.translation[1]=0.4
            self.objs[0].transformation.translation[2]=-5.0
            self.objs[0].transformation.rotation_euler[2]= -1.57079633
            
            self.objs[1].transformation.translation[0]=0.0
            self.objs[1].transformation.translation[1]=0.0
            self.objs[1].transformation.translation[2]=-5.0
            self.objs[1].transformation.rotation_euler[2]= -1.57079633

            self.update_cam()
            self.replay=False
    
    #Fonction permettant de gérer les déplacement de la balle dans les pentes
    def gravity_fall(self):
        # if self.gravity:
        #     self.objs[0].transformation.translation[1]=0.0
        #     self.objs[1].transformation.translation[1]=0.0
        # else:
        #     self.objs[0].transformation.translation[1]=0.4
        #     self.objs[1].transformation.translation[1]=0.4
        pass
