# -*- coding: utf-8 -*-
# Module graphique

"""
Module graphique pour NSI
Auteurs : M. Boehm & P. Remy (améliorations : L. Rebmeister),
          Lycée Les Pierres Vives, Carrières-sur-Seine
Version 4.1 du 14/10/18


SOMMAIRE :
PARTIE 1 : CONSTANTES ET CLASSES
PARTIE 2 : COULEURS
PARTIE 3 : FENETRE GRAPHIQUE
PARTIE 4 : AFFICHAGE DE TEXTES
PARTIE 5 : TRACE DE FORMES
PARTIE 6 : GESTION D'IMAGES
PARTIE 7 : GESTION DES SONS ET MUSIQUES
PARTIE 8 : GESTION DE LA SOURIS
PARTIE 9 : GESTION DU CLAVIER
PARTIE 10 : GESTION DU TEMPS
"""

import math
import cmath
import pygame
from pygame.locals import *

pygame.init()


#--------------------------------------------------
# PARTIE 1 : CONSTANTES ET CLASSES
#--------------------------------------------------

# PARTIE 1.1 : CONSTANTES GLOBALES

PYGAME_SDL_WEIGHT=0            # largeur de la fenêtre graphique
PYGAME_SDL_HEIGHT=0            # hauteur de la fenêtre graphique
PYGAME_SDL_BGCOLOR = 0         # couleur de fond de la fenêtre graphique
PYGAME_SDL_FONT="verdana"      # police par défaut
PYGAME_SDL_AFFICHAGE=1         # constante par défaut pour l'affichage



# PARTIE 1.2 : CLASSES PREDEFINIES

class Point :
    """
    Cette classe définit un point prenant deux champs x et y.
    P.x est l'abscisse du point P.
    P.y est l'ordonnée du point P.
    On écrira P=Point(10,50) pour définir le point P de coordonnées (10,50).
    """
    def __init__(self, x, y) :
        self.x = x
        self.y = y

    # Ajout Loïc
    def __eq__(self, other) :
        """
        Rend le P1 == P2 fonctionnel
        """
        if isinstance(other, Point) :
            return self.x == other.x and self.y == other.y
        return False

    # Ajout Loïc
    def __ne__(self, other) :
        """
        Rend le P1 != P2 fonctionnel
        """
        return not self.__eq__(other)

    # Ajout Loïc
    def __str__(self) :
        """
        Permet d'écrire des points dans la console
        """
        return "("+str(self.x)+", "+str(self.y)+")"



#--------------------------------------------------
# PARTIE 2 : COULEURS
#--------------------------------------------------

# PARTIE 2.1 : COULEURS PREDEFINIES

black=pygame.Color(0,0,0)
blue=pygame.Color(0,0,255)
brown=pygame.Color(88,41,0)
cyan=pygame.Color(0,255,255)
gold=pygame.Color(255,215,0)
gray=pygame.Color(128,128,128)
green=pygame.Color(0,255,0)
magenta=pygame.Color(255,0,255)
orange=pygame.Color(255,127,0)
pink=pygame.Color(253,108,158)
purple=pygame.Color(127,0,255)
red=pygame.Color(255,0,0)
salmon=pygame.Color(248,142,85)
silver=pygame.Color(206,206,206)
turquoise=pygame.Color(37,253,233)
white=pygame.Color(255,255,255)
yellow=pygame.Color(255,255,0)


# PARTIE 2.2 CREATION DE COULEURS RGB

def couleur_RGB(r,g,b) :
    """
    Renvoie une couleur RGB.
    r (compris entre 0 et 255) est la quantité de rouge
    g (compris entre 0 et 255) est la quantité de vert
    b (compris entre 0 et 255) est la quantité de bleu
    """
    return pygame.Color(r,g,b)




#--------------------------------------------------
# PARTIE 3 : FENETRE GRAPHIQUE
#--------------------------------------------------

# Initialisation de la fenêtre graphique
def init_graphic(W,H,name="Fenêtre ISN",bg_color=black,fullscreen=0) :
    """
    Initialise la fenêtre graphique.
    W est la largeur et H est la hauteur
    name est le nom de la fenêtre (par défaut Fenêtre ISN).
    bg_color est la couleur de l'arrière-plan (par défaut noir).
    fullscreen affiche la fenêtre de taille W*H si la valeur est 0 (par défaut)
    et en plein écran pour une autre valeur.
    L'origine (0,0) de la fenêtre graphique est situé en haut à gauche.
    """
    global PYGAME_SDL_WINDOW,PYGAME_SDL_WEIGHT,PYGAME_SDL_HEIGHT,PYGAME_SDL_BGCOLOR
    PYGAME_SDL_WEIGHT = W; PYGAME_SDL_HEIGHT = H
    PYGAME_SDL_BGCOLOR = bg_color
    if fullscreen == 0:
        PYGAME_SDL_WINDOW = pygame.display.set_mode((int(W),int(H)))
    else:
        PYGAME_SDL_WINDOW = pygame.display.set_mode((int(W),int(H)),FULLSCREEN)
    pygame.display.set_caption(name)
    pygame.draw.rect(PYGAME_SDL_WINDOW,bg_color,(0,0,int(W),int(H)),0)
    pygame.display.flip()


def init_graphic_fullscreen(bg_color=black) :
    """
    Initialise la fenêtre graphique en plein écran.
    bg_color est la couleur de l'arrière-plan (par défaut noir).
    L'origine (0,0) de la fenêtre graphique est situé en haut à gauche.
    Renvoie un tuple (W,H) correspond à la largeur et hauteur de l'écran.
    """
    global PYGAME_SDL_WINDOW,PYGAME_SDL_WEIGHT,PYGAME_SDL_HEIGHT
    InfoWindow = pygame.display.Info()
    W = InfoWindow.current_w; H = InfoWindow.current_h
    PYGAME_SDL_WEIGHT = W; PYGAME_SDL_HEIGHT = H
    PYGAME_SDL_WINDOW = pygame.display.set_mode((int(W),int(H)),FULLSCREEN)
    pygame.draw.rect(PYGAME_SDL_WINDOW,bg_color,(0,0,int(W),int(H)),0)
    pygame.display.flip()
    return W,H



# Fermeture de la fenêtre graphique
def wait_escape(text="Appuyer sur Echap pour terminer",size=20,color=gray,text_bold=False,text_italic=False,place="") :
    """
    Attend que l'on presse la touche Echap et ferme la fenêtre graphique.
    Instruction bloquante.
    Les arguments text (chaîne de caractères), size (entier), color (couleur),
    text_bold (gras) et text_italic (italique) et place (Point donnant la position
    en haut à gauche à partir duquel le texte est affiché) sont optionnels.
    """
    if text != "" :
        if place == "" :
            a = PYGAME_SDL_WEIGHT/2-largeur_texte(text,int(size),text_bold,text_italic)/2
            b = PYGAME_SDL_HEIGHT-hauteur_texte(text,int(size),text_bold,text_italic)
            place = Point(a,b)
        aff_pol(text,int(size),place,color,text_bold,text_italic)
    pygame.display.flip()
    continuer=1
    while continuer:
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                continuer = 0
            if event.type == KEYDOWN and event.key == K_ESCAPE :
                continuer = 0
    pygame.quit()


# Réinitialisation de la fenêtre graphique
def clear_graphics():
    """
    Efface tout le contenu de la fenêtre graphique
    """
    W = PYGAME_SDL_WEIGHT; H = PYGAME_SDL_HEIGHT
    pygame.draw.rect(PYGAME_SDL_WINDOW,PYGAME_SDL_BGCOLOR,(0,0,int(W),int(H)),0)
    pygame.display.flip()


# Taille de la fenêtre graphique
def size_graphics():
    """
    Renvoie le tuple (largeur,hauteur) des dimensions de la fenêtre graphique
    """
    return PYGAME_SDL_WEIGHT,PYGAME_SDL_HEIGHT


# Désactivation de l'affichage automatique
def affiche_auto_off() :
    """
    Désactive l'affichage automatique.
    """
    global PYGAME_SDL_AFFICHAGE
    PYGAME_SDL_AFFICHAGE = 0


# Activation de l'affichage automatique
def affiche_auto_on() :
    """
    Active l'affichage automatique.
    """
    global PYGAME_SDL_AFFICHAGE
    PYGAME_SDL_AFFICHAGE = 1


# Affichage des formes construites
def affiche_all() :
    """
    Affiche les tracés de formes
    """
    pygame.display.flip()




#--------------------------------------------------
# PARTIE 4 : AFFICHAGE DE TEXTES
#--------------------------------------------------

def largeur_texte(T,t,text_bold=False,text_italic=False) :
    """
    Calcule la largeur d'un texte T écrit en taille t.
    Les arguments text_bold (gras) et text_italic (italique) sont optionnels.
    """
    font = pygame.font.SysFont(PYGAME_SDL_FONT,t,bold=text_bold,italic=text_italic)
    text = font.render(T,1,black)
    text_coordinates = text.get_rect()
    return tuple(text_coordinates)[2]


def hauteur_texte(T,t,text_bold=False,text_italic=False) :
    """
    Calcule la hauteur d'un texte T écrit en taille t.
    Les arguments text_bold (gras) et text_italic (italique) sont optionnels.
    """
    font = pygame.font.SysFont(PYGAME_SDL_FONT,t,bold=text_bold,italic=text_italic)
    text = font.render(T,1,black)
    text_coordinates = text.get_rect()
    return tuple(text_coordinates)[3]



def aff_pol(T,t,P,C,text_bold=False,text_italic=False) :
    """
    Affiche une chaîne de caractère T en police Verdana à la taille t.
    P est le point en haut à gauche
    C est la couleur d'affichage.
    Les arguments text_bold (gras) et text_italic (italique) sont optionnels.
    """
    P.x = int(P.x); P.y = int(P.y)
    font = pygame.font.SysFont(PYGAME_SDL_FONT,t,bold=text_bold,italic=text_italic)
    text = font.render(T,1,C)
    PYGAME_SDL_WINDOW.blit(text,(P.x,P.y))



def list_fonts() :
    """
    Renvoie la liste des polices disponibles.
    """
    return pygame.font.get_fonts()



def test_font(S) :
    """
    S est une chaîne de caractères.
    Renvoie 1 si S est une police disponible et 0 sinon.
    """
    if S in pygame.font.get_fonts():
        return 1
    return 0



def change_font(S) :
    """
    S est une chaîne de caractères.
    Change la police initiale en la police S si elle est disponible.
    """
    global PYGAME_SDL_FONT

    if S in pygame.font.get_fonts():
        PYGAME_SDL_FONT = S



#--------------------------------------------------
# PARTIE 5 : TRACE DE FORMES
#--------------------------------------------------

def draw_pixel(P,C) :
    """
    Affiche un pixel de couleur C au point P.
    """
    P.x = int(P.x); P.y = int(P.y)
    pygame.draw.line(PYGAME_SDL_WINDOW,C,(P.x,P.y),(P.x,P.y),1)


def draw_line(P,Q,C) :
    """
    Trace un segment de couleur C entre les points P et Q.
    """
    P.x = int(P.x); P.y = int(P.y)
    Q.x = int(Q.x); Q.y = int(Q.y)
    pygame.draw.line(PYGAME_SDL_WINDOW,C,(P.x,P.y),(Q.x,Q.y),1)


def draw_triangle(P,Q,R,C) :
    """
    Trace un triangle de couleur C et de sommets P, Q et R.
    """
    P.x = int(P.x); P.y = int(P.y)
    Q.x = int(Q.x); Q.y = int(Q.y)
    R.x = int(R.x); R.y = int(R.y)
    pygame.draw.polygon(PYGAME_SDL_WINDOW,C,([P.x,P.y],[Q.x,Q.y],[R.x,R.y]),1)


def draw_fill_triangle(P,Q,R,C) :
    """
    Trace un triangle de couleur C et de sommets P, Q et R.
    """
    P.x = int(P.x); P.y = int(P.y)
    Q.x = int(Q.x); Q.y = int(Q.y)
    R.x = int(R.x); R.y = int(R.y)
    pygame.draw.polygon(PYGAME_SDL_WINDOW,C,([P.x,P.y],[Q.x,Q.y],[R.x,R.y]),0)


def draw_rectangle(P,l,h,C) :
    """
    Trace un rectangle de couleur C, de centre P, de largeur l et de hauteur h.
    """
    pygame.draw.rect(PYGAME_SDL_WINDOW,C,(int(P.x-l/2),int(P.y-h/2),int(l),int(h)),1)


def draw_fill_rectangle(P,l,h,C) :
    """
    Trace un rectangle plein de couleur C, de centre P, de largeur l et
    de hauteur h.
    """
    pygame.draw.rect(PYGAME_SDL_WINDOW,C,(int(P.x-l/2),int(P.y-h/2),int(l),int(h)),0)


def draw_circle(P,r,C) :
    """
    Trace un cercle de couleur C, de centre P et de rayon r.
    """
    P.x = int(P.x); P.y = int(P.y)
    r=int(r)
    pygame.draw.circle(PYGAME_SDL_WINDOW,C,(P.x,P.y),r,1)


def draw_fill_circle(P,r,C) :
    """
    Trace un cercle plein de couleur C, de centre P et de rayon r.
    """
    P.x = int(P.x); P.y = int(P.y)
    r=int(r)
    pygame.draw.circle(PYGAME_SDL_WINDOW,C,(P.x,P.y),r,0)


def draw_ellipse(P,l,h,C) :
    """
    Trace une ellipse de couleur C inscrite dans un rectangle de centre P,
    de largeur l et de hauteur h.
    """
    pygame.draw.ellipse(PYGAME_SDL_WINDOW,C,(int(P.x-l/2),int(P.y-h/2),int(l),int(h)),1)


def draw_fill_ellipse(P,l,h,C) :
    """
    Trace une ellipse pleine de couleur C inscrite dans un rectangle de
    centre P, de largeur l et de hauteur h.
    """
    pygame.draw.ellipse(PYGAME_SDL_WINDOW,C,(int(P.x-l/2),int(P.y-h/2),int(l),int(h)),0)


def draw_arc(P,l,h,start,end,C) :
    """
    Trace une portion d'ellipse de couleur C inscrite dans un rectangle
    de centre P, de largeur l et de hauteur h.
    Les angles start et end sont donnés en radians et sont dans [0;2*pi[.
    """
    pygame.draw.arc(PYGAME_SDL_WINDOW,C,(int(P.x-l/2),int(P.y-h/2),int(l),int(h)),start,end,1)


def draw_sector(P,r,start,end,C) :
    """
    Trace un secteur angulaire d'origine P, de rayon r, d'angle end-start et
    de couleur C.
    Les angles start et end sont donnés en radians et sont dans [0;2*pi[.
    """
    draw_arc(P,2*r,2*r,start,end,C)
    draw_line(P,Point(P.x+r*math.cos(start),P.y-r*math.sin(start)),C)
    draw_line(P,Point(P.x+r*math.cos(end),P.y-r*math.sin(end)),C)


def draw_fill_sector(P,r,start,end,C) :
    """
    Trace un secteur angulaire plein d'origine P, de rayon r,
    d'angle end-start et de couleur C.
    Les angles start et end sont donnés en radians et sont dans [0;2*pi[.
    """
    for x in range(-r,r+1):
        for y in range(-r,r+1):
            z = complex(x,y)
            arg = cmath.phase(z)
            if arg < 0:
                arg += 2*math.pi
            if(abs(z) <= r and start <= arg <= end):
                draw_pixel(Point(P.x+x,P.y-y),C)



#--------------------------------------------------
# PARTIE 6 : GESTION D'IMAGES
#--------------------------------------------------

def load_image(F,P) :
    """
    Affiche une image.
    F est une chaîne de caractère donnant le nom du fichier image.
    P est le point en haut à gauche de l'image.
    Renvoie l'image sous forme de surface pygame.
    """
    P.x = int(P.x); P.y = int(P.y)
    fond = pygame.image.load(F).convert()
    PYGAME_SDL_WINDOW.blit(fond,(P.x,P.y))
    return fond


def load_image_transp(F,P) :
    """
    Affiche une image à transparence.
    F est une chaîne de caractère donnant le nom du fichier image.
    P est le point en haut à gauche de l'image.
    Renvoie l'image sous forme de surface pygame.
    """
    P.x = int(P.x); P.y = int(P.y)
    fond = pygame.image.load(F).convert_alpha()
    PYGAME_SDL_WINDOW.blit(fond,(P.x,P.y))
    return fond


def transfer_image(F) :
    """
    Renvoie la surface pygame correspondant à l'image F (fichier).
    Attention, l'image n'est pas affichée à l'écran ; cette fonction est
    utile pour obtenir les dimensions de l'image, la redimensionner ou la
    sauvegarder
    """
    return pygame.image.load(F)


def save_image(I,F) :
    """
    I est une surface pygame.
    F est une chaîne de caractères.
    Permet de sauvegarder la surface I dans un fichier F.
    """
    pygame.image.save(I,F)


def get_size_image(I) :
    """
    Renvoie les dimensions de la surface pygame I.
    """
    return pygame.Surface.get_size(I)


def resize_image(I,W,H) :
    """
    I est une surface pygame.
    W et H sont des entiers supérieurs à 1.
    Permet de redimensionner I avec la largeur W et la hauteur H.
    Renvoie la nouvelle surface pygame.
    """
    return pygame.transform.scale(I,(W,H))



#--------------------------------------------------
# PARTIE 7 : GESTION DES SONS ET MUSIQUES
#--------------------------------------------------


# PARTIE 7.1 : SONS

def play_sound(F) :
    """
    F est une chaîne de caractères contenant le nom du fichier son.
    Joue le son F.
    """
    pygame.mixer.Sound(F).play()


def stop_sound(F) :
    """
    F est une chaîne de caractères contenant le nom du fichier son.
    Arrête le son F.
    """
    pygame.mixer.Sound(F).stop()


def set_volume_sound(F,v) :
    """
    F est une chaîne de caractères contenant le nom du fichier son.
    v est un flottant entre 0.0 et 1.0.
    Permet de régler le volume du son F.
    """
    pygame.mixer.Sound(name).set_volume(v)


def get_volume_sound(F) :
    """
    F est une chaîne de caractères.
    Renvoie le volume du son F.
    """
    return pygame.mixer.Sound(F).get_volume()


# PARTIE 7.2 : MUSIQUES

def load_music(F) :
    """
    F est une chaîne de caractères contenant le nom du fichier audio.
    Charge la musique F mais ne la joue pas.
    Si une musique était déjà chargée, cela la stoppe si elle etait jouée.
    Utiliser de préférence des .wav
    """
    pygame.mixer.music.load(F)


def play_music(loop=0) :
    """
    Lance la musique. Si la musique était déjà jouée, elle reprend au début
    L'argument optionnel loop prend les valeurs 0 ou 1.
    Si loop vaut 1, alors la musique est jouée en boucle.
    """
    if loop == 1:
        pygame.mixer.music.play(loops=-1)
    else:
        pygame.mixer.music.play()


def restart_music() :
    """
    Relance la musique à partir du début.
    """
    pygame.mixer.music.rewind()


def stop_music() :
    """
    Arrête la musique.
    """
    pygame.mixer.music.stop()


def pause_music() :
    """
    Met la musique en pause.
    """
    pygame.mixer.music.pause()


def unpause_music() :
    """
    Reprend la musique
    """
    pygame.mixer.music.unpause()


def set_volume_music(v) :
    """
    v est un flottant entre 0.0 et 1.0.
    Permet de régler le volume de la musique.
    """
    pygame.mixer.music.set_volume(v)


def get_volume_music() :
    """
    Renvoie le volume de la musique.
    """
    return pygame.mixer.music.get_volume()


def get_busy_music() :
    """
    Renvoie 1 si une musique est jouée et 0 sinon.
    """
    return pygame.mixer.music.get_busy()




#--------------------------------------------------
# PARTIE 8 : GESTION DE LA SOURIS
#--------------------------------------------------

def wait_clic() :
    """
    Attend que l'on clique gauche avec la souris.
    Renvoie les coordonnées du point cliqué.
    Instruction bloquante.
    """
    # Ajout Loïc
    if PYGAME_SDL_AFFICHAGE == 1 :
        affiche_all()

    pygame.event.clear()

    while 1 :
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                return pygame.quit()
            if event.type == MOUSEBUTTONDOWN and event.button == 1 :
                return Point(event.pos[0],event.pos[1])


def wait_clic_LR() :
    """
    Attend que l'on clique avec la souris.
    Renvoie une liste contenant une chaîne de caractère indiquant le bouton
    cliqué (G pour gauche et D pour droit) et les coordonnées du point cliqué.
    Instruction bloquante.
    """
    #Ajout Loïc
    if PYGAME_SDL_AFFICHAGE == 1 :
        affiche_all()

    pygame.event.clear()

    while 1 :
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                return pygame.quit()
            if event.type == MOUSEBUTTONDOWN :
                if event.button == 1 :
                    return ["G",Point(event.pos[0],event.pos[1])]
                if event.button == 3 :
                    return ["D",Point(event.pos[0],event.pos[1])]


def device_mouse_off() :
    """
    Supprime le curseur de la souris dans la fenêtre graphique
    """
    pygame.mouse.set_visible(0)


def device_mouse_on() :
    """
    Affiche le curseur de la souris dans la fenêtre graphique
    """
    pygame.mouse.set_visible(1)


def get_mouse() :
    """
    Renvoie la position de la souris
    Instruction non bloquante
    """
    mouse = pygame.mouse.get_pos()
    return Point(mouse[0],mouse[1])


def is_mouse_pressed_left() :
    """
    Renvoie True si le bouton gauche de la souris est cliqué
    Instruction non bloquante
    """
    pygame.event.get()
    return pygame.mouse.get_pressed()[0]


def is_mouse_pressed_right() :
    """
    Renvoie True si le bouton droit de la souris est cliqué
    Instruction non bloquante
    """
    pygame.event.get()
    return pygame.mouse.get_pressed()[2]

def is_mouse_focused():
    """
    Renvoie True si la fenêtre graphique est sélectionnée
    """
    return pygame.mouse.get_focused()



#--------------------------------------------------
# PARTIE 9 : GESTION DU CLAVIER
#--------------------------------------------------
def wait_key():
    """
    Attend que l'on tape sur une touche du clavier (y compris
    une combinaison de touches) et renvoie le caractère correspondant.
    Instruction bloquante
    """
    # Ajout Loïc
    if PYGAME_SDL_AFFICHAGE == 1 :
        affiche_all()

    pygame.event.clear()

    caractere = ""
    while caractere == "" :
        for event in pygame.event.get() :
            if event.type == KEYDOWN :
                caractere = event.dict['unicode']
                if caractere != "" :
                    return caractere


def wait_space_letter():
    """
    Attend que l'on presse une touche du clavier.
    Si la touche est une lettre, renvoie la lettre correspondante en majuscule.
    Si la touche est la barre d'espace, renvoie la chaîne de caractère espace.
    Sinon, renvoie une chaîne vide.
    Instruction bloquante.
    """
    key = wait_key()
    if 96 < key < 123 :
        return chr(key-32)
    if key == 32 :
        return " "
    return ""


def wait_arrow():
    """
    Attend que l'on presse une touche du clavier.
    Renvoie "up", "down", "left" ou  "right" suivant que l'on a
    tapé sur la flèche du haut, du bas, de gauche ou de droite.
    Renvoie une chaîne vide sinon.
    Instruction bloquante.
    """
    # Ajout Loïc
    if PYGAME_SDL_AFFICHAGE == 1 :
        affiche_all()

    pygame.event.clear()

    while 1 :
        for event in pygame.event.get() :
            if event.type == KEYDOWN:
                if event.key == K_UP :
                    return "up"
                elif event.key == K_DOWN :
                    return "down"
                elif event.key == K_LEFT :
                    return "left"
                elif event.key == K_RIGHT :
                    return "right"



# Les fonctions ci-dessous sont à combiner en général avec la fonction wait_key()
def get_space_letter(key) :
    """
    key est un nombre code ascii (nombre entier entre 0 et 255).
    Si key est le code d'une lettre minuscule (valeur entre 97 et 122)
    ou majuscule (valeur entre 65 et 90), renvoie la lettre majuscule
    correspondante.
    Si key est le code de l'espace (valeur 32), renvoie la chaîne de
    caractères espace (" ").
    Renvoie une chaîne vide dans les autres cas.

    """
    if 64 < key < 91 :  # ord('A') <= key <= ord('Z')
        return chr(key)
    if 96 < key < 123 :   # if ord('a') <= key <= ord('z') :
        return chr(key-32)
    if key == 32 :
        return " "
    return ""


def is_letter(key) :
    """
    Teste si key est le code ascii d'une lettre minuscule (valeur entre 97
    et 122) ou d'une lettre majuscule (valeur entre 65 et 90)
    Retourne 1 si vrai et 0 sinon
    """
    return ord('A') <= key <= ord('Z') or ord('a') <= key <= ord('z')


def is_space(key) :
    """
    Teste si key est le code ascii de l'espace (valeur 32)
    Retourne 1 si vrai et 0 sinon
    """
    return key == ord(' ')


def is_return(key) :
    """
    Teste si key est le code ascii de la touche return (valeur 13)
    Retourne 1 si vrai et 0 sinon
    """
    return key == 13


#--------------------------------------------------
# PARTIE 10 : GESTION DU TEMPS
#--------------------------------------------------

def attendre(millisecondes) :
    """
    Attend le nombre de millisecondes passé en argument
    """
    # Modification Loïc
    if PYGAME_SDL_AFFICHAGE == 1 :
        affiche_all()

    pygame.time.delay(millisecondes)


def chrono_start() :
    """
    Démarre un chronomètre
    """
    global CHRONO
    CHRONO = pygame.time.get_ticks()


def chrono_val() :
    """
    Affiche le temps écoulé en millisecondes depuis le lancement du chronomètre
    """
    global CHRONO
    return pygame.time.get_ticks()-CHRONO