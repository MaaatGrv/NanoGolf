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

        # initialisation des variables (ça fait beaucoup)
        self.objs = []
        self.new_scene=[]
        self.removed = []
        self.to_add=[] # Contient le texte de félicitation qui s'affiche àprès avoir mis la balle dans le trou
        self.lv_2_component = [] # Contient les composants de la scène de niveau 2
        self.touch = {}
        self.power=0.0  # Puissance du coup
        self.length=0.0 # Longueur de la barre de puissance
        self.shot=0 # Gestion de la puissance
        self.downlength=0.0 # Longueur de rétraction la barre de puissance
        self.origin= np.array([ 6 ,  0.4, -5. ]) # Coordonnées  de la balle au spawn
        self.t0=0 # timer
        self.t1=0 # timer
        self.replay = False # Indique que la partie reccommence
        self.WinTextAdded = False # Variable pour savoir si le texte de fin de partie est affiché
        self.start=0 # timer
        self.end=0 # timer
        self.coups=0 # nombre de coups
        self.shooting=False # Joueur est en train de tirer ou non
        self.next_lv=False
        self.lv_nb=1

    def run(self,LimTrouList):
        self.init_context()
        # boucle d'affichage
        while not glfw.window_should_close(self.window):
            # nettoyage de la fenêtre : fond et profondeur
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

            self.update_key()
            self.verif_collision()
            self.trajectory()
            self.toucher_drapeau(LimTrouList)

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
                        self.next_level()
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

        # Gestion du contrôle de la puissance

        # Il y a un délai de 1s entre le moment où le joueur relache la touche et le moment où la balle part
        # La barre de puissance rentre ensuite en place
        if key == glfw.KEY_P and action == glfw.RELEASE:
            print("Puissance finale", self.power)
            time.sleep(1) 
            self.objs[1].transformation.translation -= \
                pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[1].transformation.rotation_euler), pyrr.Vector3([self.downlength, 0, 0,]))
            
            # Réinitialisation des variables de puissance
            self.downlength = 0.0
            self.shot=0
            self.shooting=True

            # Un coup est comptabilisé et affiché
            self.coups+=1
            self.display_coups()

        # Certaines variables sont réinitialisées à l'appuie de P pour un nouveau coup
        if key == glfw.KEY_P and action == glfw.PRESS:
            self.power = 0.0
            self.length = 0.0
            self.shooting=False
        
        if key == glfw.KEY_Q and action == glfw.PRESS:
            self.next_level()

    # Gestions de objets présents dans la scène

    def add_object(self, obj):
        self.objs.append(obj)
        if not self.WinTextAdded :
            if not self.replay :
                self.new_scene.append(obj)
    
    def add_object_LV2(self,obj):
        self.lv_2_component.append(obj)
    
    def add_future_object(self, obj):
        self.to_add.append(obj)

    def set_camera(self, cam):
        self.cam = cam
    
    def delete_object(self, obj):
        self.removed.append(obj)
        self.objs.remove(obj)

    # Gestion des mouvements de la caméra
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

    # Permet de détecter si la balle est dans le trou (en réalité zone délimitée autour du drapeau)
    def toucher_drapeau(self, LimTrouList):
        if self.lv_nb == 1:
            L1=LimTrouList[self.lv_nb-1][0]
            L2=LimTrouList[self.lv_nb-1][1]
            xmin,xmax,zmin,zmax = [],[],[],[]
            xmin.append(L1[0][0])
            xmax.append(L2[1][0])
            zmax.append(L1[1][2])
            zmin.append(L2[0][2])
            if len(self.objs) > 0:
                if self.objs[0].transformation.translation[0]>xmin[0] and self.objs[0].transformation.translation[0]<xmax[0] and self.objs[0].transformation.translation[2]>zmin[0] and self.objs[0].transformation.translation[2]<zmax[0] and self.WinTextAdded==False :
                    self.add_object(self.to_add[0])
                    # Ajout du texte de fin de partie
                    self.WinTextAdded=True
                    self.power=0.0
                    # La balle tombe dans le trou...
                    self.objs[0].transformation.translation[1]=0.0
                    self.objs[1].transformation.translation[1]=0.0
                    self.update_cam()
    
    # Cette fonction permet à la camera de suivre la balle alors de son appel
    def update_cam(self):
        #Adaptation de la caméra
        self.cam.transformation.rotation_euler = self.objs[0].transformation.rotation_euler.copy() 
        self.cam.transformation.rotation_euler[pyrr.euler.index().yaw] += np.pi
        self.cam.transformation.rotation_center = self.objs[0].transformation.translation + self.objs[0].transformation.rotation_center
        self.cam.transformation.translation = self.objs[0].transformation.translation + pyrr.Vector3([0, 1, 5])

    # Gestion des touches du clavier
    def update_key(self):
        if glfw.KEY_LEFT in self.touch and self.touch[glfw.KEY_LEFT] > 0:
            self.mvmt_rotation(-0.05)
        if glfw.KEY_RIGHT in self.touch and self.touch[glfw.KEY_RIGHT] > 0:
            self.mvmt_rotation(0.05)

        # Pendant que la touche P est ajoutée, la puissance augmente jusqu'à atteindre 100, sa valeur maximale
        if glfw.KEY_P in self.touch and self.touch[glfw.KEY_P] > 0:
            self.calculate_bar_length()
            if self.power  < 100:
                self.power+=1.2
            else:
                self.power = 100
            if self.length < 5:
                # Translation de la barre de puissance pour indiquer la charge de puissance
                self.objs[1].transformation.translation += \
                pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[1].transformation.rotation_euler), pyrr.Vector3([0.048, 0, 0,]))
                self.downlength+=0.048 # Stockage pour pouvoir redescendre a barre une fois le tir lancé.
    
    # Calcul la longueur que la barre doit avoir selon la puissance obtenue
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

    # Gestions des 2 boutons Rejouer et Quitter
    def mouse_button_callback(self, window, button, action, mods):
        if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
            # Détection des boutons :

            # Positions points Bouton 1
            A1,B1,C1=[11,11],[120,11],[120,58]
            # Positions points Bouton 2
            A2,B2,C2=[11,75],[120,75],[120,120]

            if self.verif_mouse_pos(A1,B1,C1) == True:
                print("Bouton Rejouer")
                self.replay_game()

            if self.verif_mouse_pos(A2,B2,C2) == True:
                print('Bouton Quitter')
                glfw.set_window_should_close(window, glfw.TRUE)

    # Gestion des collisions
    def verif_collision(self):
        if self.lv_nb == 1:
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
    
    # Gestion du mouvement de la balle
    # Nous avons essayé de donner à la balle un mouvement assez réaliste
    # Nous avons donc régler les paramètres de l'équation de mouvement de la balle pour avoir le meilleur résultat
    def trajectory(self):
        if not self.WinTextAdded:
            if self.shooting:
                self.shot+=0.5
                if self.shot < self.power:
                    self.t1=time.time()
                    # Variables
                    v0= self.power * 0.8 # Vitesse initiale dépend de la puissance
                    f=30.0 # force de frottement
                    m=0.05 # masse de la balle de golf en kg
                    Tau=m/f
                    tr = Tau*v0*(math.exp((-self.t0)/Tau)-math.exp((-self.t1)/Tau))
                    self.mvmt_translation(tr)
                self.tO=time.time()

    # Permet la translation de la balle avec les éléments graphiques et la caméra qui suivent
    def mvmt_translation(self,tr):
        self.objs[0].transformation.translation += \
            pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[0].transformation.rotation_euler), pyrr.Vector3([0, 0, tr]))
        self.objs[1].transformation.translation += \
            pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[1].transformation.rotation_euler), pyrr.Vector3([0, 0, tr]))
        self.update_cam()
    
    # Permet la rotation de la balle avec les éléments graphiques et la caméra qui suivent
    def mvmt_rotation(self,angle):
        self.objs[0].transformation.rotation_euler[pyrr.euler.index().yaw] += angle
        self.objs[1].transformation.rotation_euler[pyrr.euler.index().yaw] += angle
        self.update_cam()
    
    # Gestion de l'affichage des coups, le score doit être actualisé après chaque coups.
    def display_coups(self):
        n=0

        # Création de l'objet text
        programGUI_id = glutils.create_program_from_file('Shaders/gui.vert', 'Shaders/gui.frag')
        vao = Text.initalize_geometry()
        texture = glutils.load_texture('IMG/fontB.jpg')
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
    
    # Permet de replacer la balle dans les conditions d'origine avec la camera et les éléments graphiques
    def replay_game(self):
        if self.coups > 0:
            self.replay=True
            self.coups=0 # Remise à 0 du nombre de coups (logique on retente sa chance)
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

    # Fonction permettant changer de niveau en supprimant et ajoutant des éléments à la scène

    def next_level(self):
        self.lv_nb+=1
        for i in range(len(self.objs)):
            self.delete_object(self.objs[0])

        for elmt in eval('self.lv_'+str(self.lv_nb)+'_component'):
            self.add_object(elmt)