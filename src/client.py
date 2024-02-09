import os
import dotenv
import requests
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

dotenv.load_dotenv()

token = os.getenv("TOKEN")

update_delay = 2000
host = "localhost"
port = 62952
image_size = 256
volume_delta = 10

bg_color = "#222222"
fg_color = "#aaaaaa"

class App():
    def __init__(self) -> None:
        self.root = Tk()
        self.root.geometry("800x480")
        self.root.title("player")
        self.root.config(background=bg_color)

        self.image_url = ""

        self.img = ImageTk.PhotoImage(image=Image.new("RGB", (image_size, image_size)))

        self.album_art = Label(self.root, image=self.img)
        self.title = Label(self.root, text="", bg=bg_color, fg=fg_color, font=(None, 20))
        self.artist = Label(self.root, text="", bg=bg_color, fg=fg_color, font=(None, 10))

        self.progress_bar = ttk.Progressbar(self.root, length=420, maximum=1)

        self.previous_button = Button(self.root, text="Previous", command=self.previous)
        self.pause_button = Button(self.root, text="Pause/Play", command=self.pause_play)
        self.next_button = Button(self.root, text="Next", command=self.next)

        self.volume_bar = ttk.Progressbar(self.root, length=300, maximum=1)

        self.volume_up_button = Button(self.root, text="Volume +", command=lambda : self.adjust_volume(volume_delta))
        self.volume_down_button = Button(self.root, text="Volume -", command=lambda : self.adjust_volume(-volume_delta))

        self.album_art.place(x=0, y=0)
        self.title.place(x=300, y=75)
        self.artist.place(x=300, y=125)
        self.progress_bar.place(x=300, y=175)

        self.pause_button.place(x=440, y=200, width=140)
        self.previous_button.place(x=440-140, y=200, width=140)
        self.next_button.place(x=440+140, y=200, width=140)

        self.volume_bar.place(x=250, y=350)
        self.volume_up_button.place(x=400, y=400, width=100)
        self.volume_down_button.place(x=300, y=400, width=100)

        self.update()

        self.root.mainloop()

    def adjust_volume(self, delta : int):
        try:
            res = requests.post(f"http://{host}:{port}/volume", data={"delta" : delta} , headers={"auth": token})
        except requests.exceptions.ConnectionError:
            print("Connection error")
            return
        
        try:
            res = requests.get(f"http://{host}:{port}/info", headers={"auth": token})
        except requests.exceptions.ConnectionError:
            print("Connection error")
            return

        try:
            info = res.json()
        except requests.exceptions.JSONDecodeError:
            print("Could not decode json")
            return
        
        self.volume_bar.config(value=info['volume']/100)

    def pause_play(self):
        try:
            res = requests.get(f"http://{host}:{port}/pause-play", headers={"auth": token})
        except requests.exceptions.ConnectionError:
            print("Connection error")
            return

    def previous(self):
        try:
            res = requests.get(f"http://{host}:{port}/previous", headers={"auth": token})
        except requests.exceptions.ConnectionError:
            print("Connection error")
            return

    def next(self):
        try:
            res = requests.get(f"http://{host}:{port}/next", headers={"auth": token})
        except requests.exceptions.ConnectionError:
            print("Connection error")
            return

    def update(self):
        self.root.after(update_delay, self.update)

        try:
            res = requests.get(f"http://{host}:{port}/info", headers={"auth": token})
        except requests.exceptions.ConnectionError:
            print("Connection error")
            return

        try:
            info = res.json()
        except requests.exceptions.JSONDecodeError:
            print("Could not decode json")
            return

        self.title.config(text=info['title'])
        self.artist.config(text=info['artist'])

        self.progress_bar.config(value=info['position'] / info['duration'])
        self.volume_bar.config(value=info['volume']/100)

        if self.image_url != info['art']:
            self.img = ImageTk.PhotoImage(Image.open(requests.get(info['art'], stream=True).raw).resize((image_size, image_size), Image.Resampling.BILINEAR))
            self.album_art.config(image=self.img)
            self.image_url = info['art']


def main():
    app = App()

if __name__ == "__main__":
    main()