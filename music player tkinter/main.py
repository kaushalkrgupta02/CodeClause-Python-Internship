from tkinter import *
import pygame
import os
from tkinter import filedialog
from PIL import Image, ImageTk
from pygame import mixer

mixer.init()

root = Tk()
root.title("Music Player")
root.geometry("500x350")

pygame.mixer.init()

menubar = Menu(root)
root.config(menu=menubar)

songs = []
curr_song = ""
paused = False


def load_music():
    global curr_song
    root.directory = filedialog.askdirectory()

    for song in os.listdir(root.directory):
        name, ext = os.path.splitext(song)
        if ext == ".mp3" or ext == ".wav":
            songs.append(song)

    for song in songs:
        songlist.insert("end", song)


# Load the music disc icon image
music_disc_icon = Image.open(
    "C:\\#Projects\\CodeClause.py\\music player tkinter\\assest\\music_disc_icon.png"
)

# Create a list of rotated images
rotated_images = []
for i in range(36):
    rotated_image = music_disc_icon.rotate(10 * i)
    rotated_images.append(ImageTk.PhotoImage(rotated_image))


# Create a label to display the rotated images
music_disc_label = Label(root)
music_disc_label.grid(column=1, row=0, padx=30)


rotating = False
last_index = 0


# Update the update_image function
def update_image(index):
    global rotating, last_index
    if rotating:
        music_disc_label.config(image=rotated_images[index])
        root.update()
        index += 1
        if index >= len(rotated_images):
            index = 0
        last_index = index
        print("updt_img vala hai", last_index)
        root.after(100, update_image, index)


# Play music function
def play_music():
    global curr_song, paused, rotating, last_index
    selected_song = songlist.get(ACTIVE)
    pause_resume_btn.config(image=pause_icon, command=pause_resume)  # resume btn on

    if selected_song:
        curr_song = selected_song
        try:
            pygame.mixer.music.load(os.path.join(root.directory, curr_song))
            pygame.mixer.music.play()
            paused = False
            status_label.config(text="Playing")
            rotating = True
            update_image(0)  # Start the animation
            pygame.mixer.music.set_endevent(pygame.USEREVENT)
            root.after(100, check_if_song_finished)

        except pygame.error as e:
            print(f"Error playing song: {e}")


def check_if_song_finished():
    if not pygame.mixer.music.get_busy():
        next_song_index = songlist.curselection()[0] + 1
        if next_song_index < songlist.size():
            songlist.selection_clear(0, END)
            songlist.selection_set(next_song_index)
            play_music()


# Stop the animation when the music stops
def stop_music():
    global rotating, last_index
    pygame.mixer.music.stop()
    pause_resume_btn.config(image=pause_icon, command=pause_resume)  # resume btn on
    status_label.config(text="Stopped")
    music_disc_label.config(image=music_disc_icon)  # Reset the image
    rotating = False
    last_index = 0


def pause_resume():
    global paused, rotating, last_index
    if (
        paused and not pygame.mixer.music.get_busy()
    ):  # Check if music is paused and not playing
        pygame.mixer.music.unpause()
        paused = False
        pause_resume_btn.config(image=pause_icon, command=pause_resume)
        status_label.config(text="Resumed")
        rotating = True
        update_image(last_index)  # Resume rotation from last index
    else:  # If playing, pause music and update status
        pygame.mixer.music.pause()
        paused = True
        pause_resume_btn.config(image=resume_icon, command=resume)
        status_label.config(text="Paused")
        rotating = False


def resume():
    pygame.mixer.music.unpause()
    pause_resume_btn.config(image=pause_icon, command=pause_resume)


org_menu = Menu(menubar, tearoff=False)
org_menu.add_command(label="Select Folder", command=load_music)
menubar.add_cascade(label="Organise", menu=org_menu)

play_icon = PhotoImage(
    file="C:\\#Projects\\CodeClause.py\\music player tkinter\\assest\\play_icon.png"
)
pause_icon = PhotoImage(
    file="C:\\#Projects\\CodeClause.py\\music player tkinter\\assest\\pause_icon.png"
)
stop_icon = PhotoImage(
    file="C:\\#Projects\\CodeClause.py\\music player tkinter\\assest\\stop_icon.png"
)
resume_icon = PhotoImage(
    file="C:\\#Projects\\CodeClause.py\\music player tkinter\\assest\\resume_icon.png"
)


songlist = Listbox(root, bg="black", fg="white", width=50, height=15)
songlist.grid(column=0, row=0, padx=10)


music_disc_icon = PhotoImage(
    file="C:\\#Projects\\CodeClause.py\\music player tkinter\\assest\\music_disc_icon.png"
)
music_disc_label = Label(root, image=music_disc_icon)
music_disc_label.grid(column=1, row=0, padx=30)

my_label_img = PhotoImage(
    file="C:\\#Projects\\CodeClause.py\\music player tkinter\\assest\\text-ezgif.com-resize.gif"
)
my_label = Label(root, image=my_label_img)
my_label.grid(column=1, row=1, padx=12)

controls_frame1 = Frame(root)
controls_frame1.grid(column=0, row=1)

controls_frame2 = Frame(root)
controls_frame2.grid(column=1, row=1)

play_btn = Button(controls_frame1, image=play_icon, borderwidth=0, command=play_music)
stop_btn = Button(controls_frame1, image=stop_icon, borderwidth=0, command=stop_music)
pause_resume_btn = Button(
    controls_frame1, image=pause_icon, borderwidth=0, command=pause_resume
)

play_btn.grid(column=0, row=0, padx=12, pady=30)
stop_btn.grid(column=2, row=0, padx=12, pady=30)
pause_resume_btn.grid(column=4, row=0, padx=12, pady=30)

status_label = Label(controls_frame1, text="")
status_label.grid(column=6, row=0, padx=12, pady=30)


root.mainloop()
