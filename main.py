"""
8/12/2020
Debug:
[x] Volume Slider Connection
[x] Userpath
[x] Volume slider start from 0

Features:
[] Music length
[] Control With Pc Keyboard Bindings
[] Play/Pause Binding


"""
import pygame
import getpass
from pygame import mixer
from tkinter import *
from tkinter import filedialog
import os
import time

def playpausesong():
    currentsong=playlist.get(ACTIVE)
    mixer.music.load(currentsong)
    root.title('Playing ' + currentsong)
    if songstatus == "Playing":
        mixer.music.pause()
        songstatus.set("Paused")
    else:
        mixer.music.play()


def pausesong():
    songstatus.set("Paused")
    mixer.music.pause()
    root.title('Paused')

def stopsong():
    songstatus.set("Stopped")
    mixer.music.stop()
    root.title('Stopped')

def resumesong():
    songstatus.set("Resuming")
    mixer.music.unpause()  
    root.title('Resumed')

def setvolume(self):
    volume = VolumeSlider.get()
    volumed = volume / 100 +0.00
    mixer.music.set_volume(volumed)
    
root=Tk()
root.title('Slimer Music Player')
root.configure(background='grey22')
root.geometry('800x400')
root.resizable(height = False, width = False)
mixer.init()
songstatus=StringVar()
songstatus.set("choosing")

#playlist---------------
playlist=Listbox(root,selectmode=SINGLE,bg="black",fg="grey88",font=('arial',15),width=60)
playlist.grid(columnspan=5)
playlist.place(x=0, y=50)
path = filedialog.askdirectory()
os.chdir(path)
songs=os.listdir()

for s in songs:
    playlist.insert(END,s)

label_widget = Label(root, text="Selected Path: " + path)
label_widget.config(font=('arial',12),bg="grey10",fg="white",padx=7,pady=7)
label_widget.place(bordermode=OUTSIDE, x=0, y=0)

playbtn=Button(root,text="play",command=playpausesong)
playbtn.config(font=('arial',20),bg="grey10",fg="white",padx=7,pady=7)
playbtn.place(bordermode=OUTSIDE, height=50, width=150, x=0, y=350)

pausebtn=Button(root,text="Pause",command=playpausesong)
pausebtn.config(font=('arial',20),bg="grey10",fg="white",padx=7,pady=7)
pausebtn.place(bordermode=OUTSIDE, height=50, width=150, x=150, y=350)

stopbtn=Button(root,text="Stop",command=stopsong)
stopbtn.config(font=('arial',20),bg="grey10",fg="white",padx=7,pady=7)
stopbtn.place(bordermode=OUTSIDE, height=50, width=150, x=300, y=350)

Resumebtn=Button(root,text="Resume",command=resumesong)
Resumebtn.config(font=('arial',20),bg="grey10",fg="white",padx=7,pady=7)
Resumebtn.place(bordermode=OUTSIDE, height=50, width=150, x=450, y=350)

v = DoubleVar() 
VolumeSlider = Scale(root, bg="grey10",fg="white", variable=v, from_ = 0,to = 100, orient = HORIZONTAL, command=setvolume) 
VolumeSlider.place(bordermode=OUTSIDE, height=50, width=200, x=600, y=350)
VolumeSlider.set(100)

mainloop()