from tkinter import filedialog
import os
import tkinter as tk
from tkinter import *
import pygame
import threading

# initialize pygame
pygame.mixer.init()


# Root Window
root = Tk()
root.title("Music Player")
root.geometry('500x500')
root.resizable(False,False)
root.config(bg='grey25')



songs = []
current_song = ""
paused = False
playing = False

def select_music(event):
    global current_song
    if not paused:
        current_song = songs[songlist.curselection()[0]]
        play_music()
    else:
        songlist.selection_clear(0,END)
        songlist.selection_set()
        current_song = songs[songlist.curselection()[0]]
        play_music()

def load_music():
    global current_song
    root.directory = filedialog.askdirectory()

    for song in os.listdir(root.directory):
        name, ext = os.path.splitext(song)
        if ext == '.mp3':
            songs.append(song)
    for song in songs:
        songlist.insert("end", song)
    
    songlist.selection_set(0)
    current_song = songs[songlist.curselection()[0]]

# functions to control music
def play_music():
    global paused, current_song, playing
    pygame.mixer.music.load(os.path.join(root.directory, current_song))
    pygame.mixer.music.play()     
    play_btn.config(image=pause_image, command=pause_music)

   

def pause_music():
    global paused, current_song, playing
    pygame.mixer.music.pause()
    play_btn.config(image=play_image, command=play_music)
    paused = True
    

def next_music():
    global current_song, songs
    try:
        
        songlist.selection_clear(0, END)
        songlist.selection_set(songs.index(current_song)+1)
        current_song = songs[songlist.curselection()[0]]
        play_music()
        play_btn.config(image=pause_image, command=pause_music)
    
    except:
        pass

def prev_music():
    global current_song, songs
    try:
        
        songlist.selection_clear(0,END)
        songlist.selection_set(songs.index(current_song)-1)
        current_song = songs[songlist.curselection()[0]]
        play_music()
        play_btn.config(image=pause_image, command=pause_music)

    except:
        pass


    
# creating menubar
menubar = Menu(root,activebackground='blue')
root.config(menu=menubar)

organise_menu = Menu(menubar, tearoff=False, activeforeground='white', activebackground='blue')
organise_menu.add_command(label='Select Folder', command=load_music)
menubar.add_cascade(label='Import Music', menu=organise_menu,activebackground='blue')


# load icons
play_image = PhotoImage(file='play.png')
pause_image = PhotoImage(file='pause.png')
prev_image = PhotoImage(file='prev.png')
next_image = PhotoImage(file='next.png')


# main frame
main = tk.Frame(root)
main.pack()
songlist = tk.Listbox(root, bg='grey9', fg='white', width=100, height=24, selectmode=SINGLE, relief='ridge')
songlist.pack(padx=5, pady=5)
songlist.bind("<<ListboxSelect>>", select_music) 

# control frame
control_frame = tk.Frame(root,bg='grey25')
control_frame.pack()

# add control buttons
play_btn = tk.Button(control_frame, image=play_image, borderwidth=0, command=play_music,bg='grey25')
prev_btn = tk.Button(control_frame, image=prev_image, borderwidth=0, command=prev_music,bg='grey25')
next_btn = tk.Button(control_frame, image=next_image, borderwidth=0, command=next_music, bg='grey25')
prev_btn.grid(row=0, column=0, padx=5, pady=25)
play_btn.grid(row=0, column=1, padx=5, pady=25)
next_btn.grid(row=0, column=2, padx=5, pady=25)

# run mainloop
root.mainloop()