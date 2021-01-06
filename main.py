#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
PyTone 1.2
Finally pytone 1.2 is out and I have fix some bugs included:
	Number collapse when song length is one numbered (4:8-->04:08)
	Slider woking now but user still cannot set the length because some bug
	All numeric system working
	Redesigned the main window
	Some minor bug fix

"""

#lib import
import pygame #Music player core
import sys #sometimes it can use to fix some weird bug
from pygame import mixer #Music player core with playlist binding
from tkinter import * #the most important module in the world
from tkinter import filedialog #for handling file dialog
from tkinter import messagebox #for handling messagebox
from tkinter.messagebox import askokcancel #for prompt ok-cancel message box
import os #for handling path stuff
import time #for the timer
import threading #multithreading
from custom_ttkthemes import ThemedTk #for the music progress slider
import tkinter.ttk as ttk #the second important module in the world
import re #for handling string stuff
import mutagen #for getting mp3 data
from mutagen.id3 import ID3 #Helps other 3 mutagen module get the song's ID3 metadata
from mutagen.mp3 import MP3 #mp3 extension details
from mutagen.flac import FLAC #flac extension details
from mutagen.wave import WAVE #ogg extension details
#import datetime #actually its use to get song length
#from datetime import time #I mentioned above

class MusicPlayer(ThemedTk):

	def __init__(self, *args, **kwargs):

		#initialization
		super(MusicPlayer, self).__init__(theme='equilux')
		pygame.init()
		mixer.init()
		SONG_END = pygame.USEREVENT + 1
		pygame.mixer.music.set_endevent(SONG_END)
		self.automusicslider = threading.Thread(target=self.musicsliderplace)
		

		#window layout initialization
		self.resizable(False, False)
		self.title('Pytone v1.2') #1.2 release
		self.configure(background='grey22')
		self.geometry('1000x600')
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
		self.explorer_icon=PhotoImage(file='assets/explorer.png')
		self.explorer_icon_active=PhotoImage(file='assets/explorer_active.png')
		self.music_icon=PhotoImage(file='assets/music.png')
		self.music_icon_active=PhotoImage(file='assets/music_active.png')
		self.mute_icon=PhotoImage(file='assets/mute.png')
		self.mute_icon_active=PhotoImage(file='assets/mute_active.png')
		self.disc_icon=PhotoImage(file='assets/disc.png')
		self.disc_icon_active=PhotoImage(file='assets/disc_active.png')
		#variable initialization
		self.songstatus=StringVar()
		self.v = DoubleVar()
		self.currentsong = None
		self.pauseonly = False
		self.songlength=1

		#post initialization
		self._widget()
		self._config()
		self._layout()



	def _widget(self):
		#widget setup
		self.play_pause_button = Button(self, image=self.play_icon, command=self.play_pause, takefocus=False, relief=FLAT, bg='grey22', activebackground='grey22')
		self.VolumeSlider = ttk.Scale(self, variable=self.v, from_ = 0,to = 100, orient = HORIZONTAL, command=self.setvolume) 
		self.music_player_scale = ttk.Scale(self, orient=HORIZONTAL,command=self.musicsliderset)
		self.volume_button = Button(self, image=self.volume_max_icon, relief=FLAT, bg='grey22', activebackground='grey22', command=self.togglemute)
		self.progress_label_1 = Label(self, text='00:00', bg='grey22', fg='white')
		self.progress_label_2 = Label(self, text='00:00', bg='grey22', fg='white')
		self.repeat_button = Button(self, image=self.repeat_icon, bg='grey22', relief=FLAT, activebackground='grey22',command=self.loopsong)
		self.shuffle_button = Button(self, image=self.shuffle_icon, bg='grey22', relief=FLAT, activebackground='grey22')
		self.last_song_button = Button(self, image=self.skip_back_icon, bg='grey22', relief=FLAT, activebackground='grey22',command=self.previous_song)
		self.next_song_button = Button(self, image=self.skip_forward_icon, bg='grey22', relief=FLAT, activebackground='grey22', command=self.next_song)
		self.playlist=Listbox(self, relief=FLAT,selectmode=SINGLE,bg="grey20",fg="grey88",font=('Arial',13),width=82,height=15,selectbackground="grey40", activestyle='none')
		self.browse_button= Button(self, bg='grey30',fg='grey92',activebackground='grey70',image=self.browse_file_icon, command=self.selectpath, relief=FLAT)
		self.pathname=Label(self, bg='grey22',fg='white', font=('arial',10))	
		self.pathtoggle=Button(self, image=self.explorer_icon, bg='grey22', relief=FLAT, width=500, height=50, command=self.toggleplaylist)
		self.nowmusictoggle=Button(self, image=self.music_icon, bg='grey30', relief=FLAT, width=500, height=50, command=self.toggleplaylist)
		self.currentvolume=Label(self,bg='grey22',fg='grey88', relief=FLAT, text='100')
		self.songname=Label(self,bg='grey22',fg='grey88', relief=FLAT, text='Name: - ',font=('Arial',13))
		self.artistname=Label(self,bg='grey22',fg='grey88', relief=FLAT, text='Artist: - ',font=('Arial',13))
		self.albumname=Label(self,bg='grey22',fg='grey88', relief=FLAT, text='Album: - ',font=('Arial',13))
		self.discicon=Button(image=self.disc_icon, bg='grey22', relief=FLAT)
		#widget binding
		self.playlist.bind('<Button-1>', self.playlistclick)	
		self.playlist.bind('<Double-Button-1>', self.playlistdoubleclick)
		#24/7 threading
		self.automusicslider.start()

	def _layout(self):
		#widget placement
		self.songname.place(relx=0.5, rely=0.35)
		self.artistname.place(relx=0.5, rely=0.45)
		self.albumname.place(relx=0.5, rely=0.55)
		self.play_pause_button.place(relx=0.5, rely=0.85, anchor=CENTER)
		self.repeat_button.place(relx=0.4, rely=0.85, anchor=CENTER)
		#self.shuffle_button.place(relx=0.6, rely=0.85, anchor=CENTER)
		self.music_player_scale.place(relx=0.5, rely=0.95, width=500, anchor=CENTER)
		self.progress_label_1.place(relx=0.20, rely=0.93)
		self.progress_label_2.place(relx=0.75, rely=0.93)
		self.last_song_button.place(relx=0.45, rely=0.85, anchor=CENTER)
		self.next_song_button.place(relx=0.55, rely=0.85, anchor=CENTER)
		self.volume_button.place(relx=0.81, rely=0.845)
		self.VolumeSlider.place(relx=0.85, rely=0.85)
		self.pathtoggle.place(relx=0.0, rely=0.0)
		self.nowmusictoggle.place(relx=0.5, rely=0.0)
		self.currentvolume.place(relx=0.95, rely=0.85)
		self.discicon.place(relx=0.15, rely=0.25)


	def playlistclick(self, event):
		self.loadsong()


	def playlistdoubleclick(self, event):
		self.loadsong()
		self.play_music()

	def check_event(self):
		pass
			


	def _config(self):
		#variable setup
		self.VolumeSlider.set(100)
		self.songstatus.set("choosing")

		#key binding
		self.bind('<Button-1>', self._flat_button)
		self.bind('<Enter>', self._button_hover)
		self.bind('<Leave>', self._button_leave)
		self.bind('<space>', self.play_pause)

	def toggleplaylist(self):
		#toggle playlist and its accessories here
		if self.playlist.winfo_ismapped() == True:
			self.playlist.place_forget()
			self.pathname.place_forget()
			self.browse_button.place_forget()
			self.pathtoggle.config(bg='grey22')
			self.nowmusictoggle.config(bg='grey30')
		else:
			self.playlist.place(relx=0.01, rely=0.15)
			self.playlist.tkraise()
			self.pathname.place(relx=0.01, rely=0.10) 
			self.browse_button.place(relx=0.96, rely=0.086)
			self.pathtoggle.config(bg='grey30')
			self.nowmusictoggle.config(bg='grey22')

	def setmusiclength(self):
		#important function on a player (also hard to do)
		if self.currentsong.endswith('.mp3') == True:
			self.song=MP3(self.currentsong)
			self.songinfo=ID3(self.currentsong)
			self.songlength=self.song.info.length
			self.songround=round(self.songlength)
			self.songmins, self.songsecs= divmod(self.songround, 60)
			self.songmins=str(self.songmins).zfill(2)
			self.songsecs=str(self.songsecs).zfill(2)
			self.progress_label_2.config(text=str(self.songmins)+':'+str(self.songsecs))
			self.songname.config(text='Song: ' + self.songinfo['TIT2'].text[0])
			self.artistname.config(text='Artist: ' + self.songinfo['TPE1'].text[0])
			self.albumname.config(text='Album: ' + self.songinfo['TALB'].text[0])
			

		if self.currentsong.endswith('.flac') == True:
			#self.song=FLAC(self.currentsong)
			#self.songinfo=ID3(self.currentsong)
			#self.songpict = self.songinfo.get("APIC:").data
			#self.songlength=self.song.info.length
			#self.songround=round(self.songlength)
			#self.songmins, self.songsecs= divmod(self.songround, 60)
			#self.songsecs=str(self.songsecs).zfill(2)
			#self.progress_label_2.config(text=str(self.songmins)+':'+str(self.songsecs))
			#self.music_player_scale.config(from_ = 0,to = self.songlength)
			#self.songname.config(text='Song: ' + self.songinfo['TIT2'].text[0])
			#self.artistname.config(text='Artist: ' + self.songinfo['TPE1'].text[0])
			#self.albumname.config(text='Album: ' + self.songinfo['TALB'].text[0])
			pass

		if self.currentsong.endswith('.ogg') == True:
			self.song=WAVE(self.currentsong)
			self.songlength=self.song.info.length
			self.songround=round(self.songlength)
			self.songmins, self.songsecs= divmod(self.songround, 60)
			self.songsecs=str(self.songsecs).zfill(2)
			self.progress_label_2.config(text=str(self.songmins)+':'+str(self.songsecs))

	def musicsliderset(self, *args):
		#Also important as user need to choose where to play
		#self.userlength = self.music_player_scale.get()
		#print(self.userlength)
		#mixer.music.set_pos(self.userlength)
		pass
	
	def musicsliderplace(self):
		for i in range(999999999):
			self.currenttime = mixer.music.get_pos()
			self.currenttime, self.currenttimemil=divmod(self.currenttime, 1000)
			self.currentmin, self.currentsec = divmod(self.currenttime, 60)
			self.currentmin=str(self.currentmin).zfill(2)
			self.currentsec=str(self.currentsec).zfill(2)
			self.progress_label_1.config(text=str(self.currentmin)+':'+str(self.currentsec))
			if self.progress_label_1['text']=='-1:59':
				self.progress_label_1.config(text='00:00')
			self.currentsongpos=int(self.currenttime)/int(self.songlength)
			self.music_player_scale.set(self.currentsongpos)

			time.sleep(1)	
	
	def _button_hover(self, event):
		try:	
			if type(event.widget) == Button:
				exec('event.widget.config(image=self.'+re.search(r'assets/(.*?)\.png', root.call(event.widget.cget('image'), 'cget', '-file')).group(1).replace('-', '_')+'_icon_active)')
		except AttributeError:
			pass
		
	#button hover out animation
	def _button_leave(self, event):
		if type(event.widget) == Button:
			exec('event.widget.config(image=self.'+re.search(r'assets/(.*?)\.png', root.call(event.widget.cget('image'), 'cget', '-file')).group(1).replace('-', '_').replace('_active', '')+'_icon)')

	#relief locking
	def _flat_button(self, event):
		if type(event.widget) == Button:
			event.widget.config(relief=FLAT)

	#music play and pause area
	def loadsong(self):
		self.currentsong=self.playlist.get(ACTIVE)
		#loading bay

		try:
			mixer.music.load(self.currentsong)
			self.play_pause_button.config(image=self.pause_icon_active)
			self.setmusiclength()
		except pygame.error:
			mixer.music.unload()
			messagebox.showerror(title="ERROR", message="Invalid Music Format!")
		
	def play_music(self, *args):
		mixer.music.play()
		self.title('Pytone v1.1 - Playing '+self.currentsong)
		self.check_event()
		

	def loopsong(self):
		if self.repeat_button.cget('bg') == 'grey40':
			pygame.mixer.music.play()
			self.repeat_button.config(bg='grey22')
		else:
			pygame.mixer.music.play(-1)
			self.repeat_button.config(bg='grey40')

	def play_pause(self):
		if self.play_pause_button['image'] == str(self.pause_icon_active):
			mixer.music.pause()
			self.play_pause_button.config(image=self.play_icon_active)
		else:
			mixer.music.unpause()
			self.play_pause_button.config(image=self.pause_icon_active)

	def next_song(self):
		selection_indices = self.playlist.curselection()

		# default next selection is the beginning
		next_selection = 0

		# make sure at least one item is selected
		if len(selection_indices) > 0:
			# Get the last selection, remember they are strings for some reason
			# so convert to int
			last_selection = int(selection_indices[-1])

			# clear current selections
			self.playlist.selection_clear(selection_indices)

			# Make sure we're not at the last item
			if last_selection < self.playlist.size() - 1:
				next_selection = last_selection + 1

		self.playlist.activate(next_selection)
		self.playlist.selection_set(next_selection)
		self.play_pause_button.config(image=self.pause_icon_active)
		self.loadsong()
		self.play_music()

	def previous_song(self):
		selection_indicesb = self.playlist.curselection()

		# default next selection is the beginning
		next_selectionb = 0

		# make sure at least one item is selected
		if len(selection_indicesb) > 0:
			# Get the last selection, remember they are strings for some reason
			# so convert to int
			last_selectionb = int(selection_indicesb[-1])

			# clear current selections
			self.playlist.selection_clear(selection_indicesb)

			# Make sure we're not at the last item
			if last_selectionb < self.playlist.size() - 1:
				next_selectionb = last_selectionb - 1

		self.playlist.activate(next_selectionb)
		self.playlist.selection_set(next_selectionb)
		self.play_pause_button.config(image=self.pause_icon_active)
		self.loadsong()
		self.play_music()


	#volume control
	def setvolume(self, event):
		self.volume = self.VolumeSlider.get()
		self.volumed = self.volume/100+0.00
		mixer.music.set_volume(self.volumed) #also write your code here 
		self.currentvolume.config(text=int(self.volume))
		if self.volume <= 100:
			self.volume_button.config(image=self.volume_max_icon)

		if self.volume <= 70:
			self.volume_button.config(image=self.volume_medium_icon)

		if self.volume <= 40:
			self.volume_button.config(image=self.volume_min_icon)	

		if self.volume == 0:
			self.volume_button.config(image=self.mute_icon)	

	def togglemute(self):
		if self.VolumeSlider.get() != 0:
			#mute
			self.VolumeSlider.set(0)
		else:
			#unmute
			self.VolumeSlider.set(100)


	def selectpath(self):
		path = filedialog.askdirectory()
		self.playlist.delete(0,'end')
		try:
			os.chdir(path)
			songs=os.listdir()
			filteredsongs=filter(lambda x: x.endswith(('.mp3')), songs)
			self.pathname.config(text = 'Selected path: ' + path) 
			for s in filteredsongs:
				self.playlist.insert(END,s)
		except OSError:
			self.pathname.config(text = 'Please choose a path...')

	def ask_quit(self):
		if mixer.music.get_busy() == False:
			root.destroy()
			os.system('taskkill /f /im python.exe')
			
		elif askokcancel("Exit", "Stop Music?"):
			mixer.music.stop()
			root.destroy()
			os.system('taskkill /f /im python.exe')
	
	

if __name__ == '__main__':

	root = MusicPlayer()
	root.mainloop()

