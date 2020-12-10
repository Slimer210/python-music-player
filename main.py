#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
10/12/2020
Debug:
[] Music Playing Logic

es:
[x] Core modification (CRITICAL) (p.s demolished by an anynymous people lol)	
[] Now Playing GUI 

"""

#lib import
import pygame #for music playing
import getpass #why you want to put this lol
from pygame import mixer #for music playing also
from tkinter import * #the most important module in the world
from tkinter import filedialog #for handling file dialog
from tkinter import messagebox #messagebox
import os #for handling path stuff
import time #for the timer
from custom_ttkthemes import ThemedTk #for the music progress slider
import tkinter.ttk as ttk #the second important module in the world
import re #for handling string stuff
import mutagen #for getting mp3 metadata
from mutagen.mp3 import MP3 #mp3 extension
from tkinter.messagebox import askokcancel #for prompt message box

class MusicPlayer(ThemedTk):

	def __init__(self, *args, **kwargs):

		#initialization
		super(MusicPlayer, self).__init__(theme='equilux')
		pygame.init()
		mixer.init()

		#window layout initialization
		self.resizable(False, False)
		self.title('Pytone')
		self.configure(background='grey22')
		self.geometry('800x450')
		self.iconbitmap('icon.ico')
		self.protocol("WM_DELETE_WINDOW", self.ask_quit)

		self.style = ttk.Style()
		self.style.configure('TButton', background='grey22')
		self.style.configure('TScale', background='grey22')

		#icon initialization
		self.play_icon = PhotoImage(file='assets/play.png')
		self.pause_icon = PhotoImage(file='assets/pause.png')
		self.volume_min_icon = PhotoImage(file='assets/volume-min.png')
		self.volume_medium_icon = PhotoImage(file='assets/volume-medium.png')
		self.volume_max_icon = PhotoImage(file='assets/volume-max.png')
		self.volume_mute_icon = PhotoImage(file='assets/volume-mute.png')
		self.repeat_icon = PhotoImage(file='assets/repeat.png')
		self.shuffle_icon = PhotoImage(file='assets/shuffle.png')
		self.skip_back_icon = PhotoImage(file='assets/skip-back.png')
		self.skip_forward_icon = PhotoImage(file='assets/skip-forward.png')
		self.play_icon_active = PhotoImage(file='assets/play_active.png')
		self.pause_icon_active = PhotoImage(file='assets/pause_active.png')
		self.volume_min_icon_active = PhotoImage(file='assets/volume-min_active.png')
		self.volume_medium_icon_active = PhotoImage(file='assets/volume-medium_active.png')
		self.volume_max_icon_active = PhotoImage(file='assets/volume-max_active.png')
		self.volume_mute_icon_active = PhotoImage(file='assets/volume-mute_active.png')
		self.repeat_icon_active = PhotoImage(file='assets/repeat_active.png')
		self.shuffle_icon_active = PhotoImage(file='assets/shuffle_active.png')
		self.skip_back_icon_active = PhotoImage(file='assets/skip-back_active.png')
		self.skip_forward_icon_active = PhotoImage(file='assets/skip-forward_active.png')
		self.browse_file_icon = PhotoImage(file='assets/browse-file.png')
		self.browse_file_icon_active = PhotoImage(file='assets/browse-file_active.png')

		#variable initialization
		self.songstatus=StringVar()
		self.v = DoubleVar()
		self.currentsong = None
		self.pauseonly = False
		self.volumeslider_shown = False

		#post initialization
		self._widget()
		self._config()
		self._layout()

	def _widget(self):
		#widget setup
		self.play_pause_button = Button(self, image=self.play_icon, command=self.play_pause, takefocus=False, relief=FLAT, bg='grey22', activebackground='grey22')
		self.VolumeSlider = ttk.Scale(self, variable=self.v, from_ = 0,to = 100, orient = HORIZONTAL, command=self.setvolume,) 
		self.music_player_scale = ttk.Scale(self, orient=HORIZONTAL,)
		self.volume_button = Button(self, image=self.volume_max_icon, relief=FLAT, bg='grey22', activebackground='grey22',command=self.togglevolume)
		self.progress_label_1 = Label(self, text='00:00', bg='grey22', fg='white')
		self.progress_label_2 = Label(self, text='00:00', bg='grey22', fg='white')
		self.repeat_button = Button(self, image=self.repeat_icon, bg='grey22', relief=FLAT, activebackground='grey22')
		self.shuffle_button = Button(self, image=self.shuffle_icon, bg='grey22', relief=FLAT, activebackground='grey22')
		self.last_song_button = Button(self, image=self.skip_back_icon, bg='grey22', relief=FLAT, activebackground='grey22')
		self.next_song_button = Button(self, image=self.skip_forward_icon, bg='grey22', relief=FLAT, activebackground='grey22')
		self.playlist=Listbox(self, selectmode=SINGLE,bg="grey20",fg="grey88",font=('Arial',13),width=65,height=11)
		self.browse_button= Button(self, bg='grey22',fg='grey92',activebackground='grey22',image=self.browse_file_icon, command=self._musicpath, relief=FLAT)
		self.pathname=Label(self, bg='grey22',fg='white', font=('arial',10))		

	def _config(self):
		#variable setup
		self.VolumeSlider.set(100)
		self.songstatus.set("choosing")

		#key binding
		self.bind('<Button-1>', self._flat_button)
		self.bind('<Enter>', self._button_hover)
		self.bind('<Leave>', self._button_leave)
		self.bind('<space>', self.play_pause)

	def togglevolume(self):
		#toggle volume slider
		if self.volumeslider_shown == False:
			self.VolumeSlider.place(relx=0.87, rely=0.85)
			self.volumeslider_shown = True
		else:
			self.VolumeSlider.pack_forget()
			self.volumeslider_shown = False

		

	def _layout(self):
		#widget placement
		self.play_pause_button.place(relx=0.5, rely=0.85, anchor=CENTER)
		self.repeat_button.place(relx=0.4, rely=0.85, anchor=CENTER)
		self.shuffle_button.place(relx=0.6, rely=0.85, anchor=CENTER)
		self.music_player_scale.place(relx=0.5, rely=0.95, width=500, anchor=CENTER)
		self.progress_label_1.place(relx=0.12, rely=0.915)
		self.progress_label_2.place(relx=0.83, rely=0.915)
		self.last_song_button.place(relx=0.45, rely=0.85, anchor=CENTER)
		self.next_song_button.place(relx=0.55, rely=0.85, anchor=CENTER)
		self.volume_button.place(relx=0.92, rely=0.91)
		self.playlist.place(relx=0.01, rely=0.10)
		self.browse_button.place(relx=0.94, rely=0.01)
		self.pathname.place(relx=0.01, rely=0.04) 

	def _button_hover(self, event):
		if type(event.widget) == Button:
			exec('event.widget.config(image=self.'+re.search(r'assets/(.*?)\.png', root.call(event.widget.cget('image'), 'cget', '-file')).group(1).replace('-', '_')+'_icon_active)')

	#button hover out animation
	def _button_leave(self, event):
		if type(event.widget) == Button:
			exec('event.widget.config(image=self.'+re.search(r'assets/(.*?)\.png', root.call(event.widget.cget('image'), 'cget', '-file')).group(1).replace('-', '_').replace('_active', '')+'_icon)')

	#relief locking
	def _flat_button(self, event):
		if type(event.widget) == Button:
			event.widget.config(relief=FLAT)

	#music play and pause area
	def play_pause(self, *args):

		#loading bay
		self.currentsong=self.playlist.get(ACTIVE)
		try:
			mixer.music.load(self.currentsong)
		except pygame.error:
			print("Bruh wrong format")
			mixer.music.unload()
			messagebox.showerror(title="ERROR", message="Invalid Music Format!")
		

		#play-pause logic
		if self.play_pause_button['image'] == str(self.play_icon_active):
			self.play_pause_button.config(image=self.pause_icon_active)
			mixer.music.play()
			#play here
		else:
			self.play_pause_button.config(image=self.play_icon_active)
			mixer.music.pause()
			#pause here

	#volume control
	def setvolume(self, event):
		self.volume = self.VolumeSlider.get()
		self.volumed = self.volume/100+0.00
		mixer.music.set_volume(self.volumed) #also write your code here 


	def _musicpath(self):
		#playlist Setup with initialization

		path = filedialog.askdirectory()
		self.playlist.delete(0,'end')
		try:
			os.chdir(path)
			songs=os.listdir()
			self.pathname.config(text = 'Selected path: ' + path) 
			for s in songs:
				self.playlist.insert(END,s)
		except OSError:
			self.pathname.config(text = 'Please choose a path...')


	def ask_quit(self):
		if mixer.music.get_busy() == False:
			root.destroy()
		elif askokcancel("Exit", "Stop Music?"):
			mixer.music.stop()
			root.destroy()

if __name__ == '__main__':

	root = MusicPlayer()
	root.mainloop()
