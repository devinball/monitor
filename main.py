from typing import Type
from rich.console import RenderableType
from rich.text import TextType
from textual._path import CSSPathType
from textual.driver import Driver
from textual.widgets._button import ButtonVariant
from interface import ServiceInterface
from textual import on
from textual.app import App, CSSPathType, ComposeResult
from textual.widgets import Header, Footer, Button, Static, Label, ProgressBar

class PlayInfoDisplay(Static):
    def __init__(self, service_interface : ServiceInterface, renderable: RenderableType = "", *, expand: bool = False, shrink: bool = False, markup: bool = True, name: str | None = None, id: str | None = None, classes: str | None = None, disabled: bool = False) -> None:
        super().__init__(renderable, expand=expand, shrink=shrink, markup=markup, name=name, id=id, classes=classes, disabled=disabled)
        self.service_interface = service_interface

    def on_mount(self) -> None:
        self.set_interval(service_interface.update_time, self.update_display)

    def update_display(self) -> None:
        info : dict = self.service_interface.get_info()

        song_name : str = info['song_name']
        artist_names : str = " | ".join(info["artist_names"])

        progress : float = (info['song_progress'] / info['song_duration']) * 100

        self.song_name_label.update(song_name)
        self.artist_name_label.update(artist_names)
        self.update_frequency_label.update(f"Update Frequency: {self.service_interface.update_time}")

        self.bar.total = 100
        self.bar.progress = progress

    def compose(self) -> ComposeResult:
        self.song_name_label = Label()
        self.artist_name_label = Label()

        self.update_frequency_label = Label()

        self.bar = ProgressBar(show_eta=False, show_percentage=False)
        self.bar.total = 100
        self.bar.progress = 0

        yield self.bar
        yield self.song_name_label
        yield self.artist_name_label
        yield self.update_frequency_label

class ActionButton(Button):
    def __init__(self, label: TextType | None = None, variant: ButtonVariant = "default", *, name: str | None = None, id: str | None = None, classes: str | None = None, disabled: bool = False):
        super().__init__(label, variant, name=name, id=id, classes=classes, disabled=disabled)

class ActionButtons(Static):
    def __init__(self, service_interface : ServiceInterface, renderable: RenderableType = "", *, expand: bool = False, shrink: bool = False, markup: bool = True, name: str | None = None, id: str | None = None, classes: str | None = None, disabled: bool = False) -> None:
        super().__init__(renderable, expand=expand, shrink=shrink, markup=markup, name=name, id=id, classes=classes, disabled=disabled)
        self.service_interface = service_interface

    def compose(self) -> ComposeResult:
        yield ActionButton("Previous", id="previous", variant="success")
        yield ActionButton("Pause/Play", id="pause-play", variant="success")
        yield ActionButton("Next", id="next", variant="success")

    @on(Button.Pressed, "#previous")
    def previous(self) -> None:
        self.service_interface.previous()

    @on(Button.Pressed, "#pause-play")
    def pause_play(self) -> None:
        self.service_interface.pause_play()

    @on(Button.Pressed, "#next")
    def next(self) -> None:
        self.service_interface.next()

class VolumeButton(Button):
    def __init__(self, label: TextType | None = None, variant: ButtonVariant = "default", *, name: str | None = None, id: str | None = None, classes: str | None = None, disabled: bool = False):
        super().__init__(label, variant, name=name, id=id, classes=classes, disabled=disabled)

class VolumeDisplay(Static):
    def __init__(self, service_interface : ServiceInterface, renderable: RenderableType = "", *, expand: bool = False, shrink: bool = False, markup: bool = True, name: str | None = None, id: str | None = None, classes: str | None = None, disabled: bool = False) -> None:
        super().__init__(renderable, expand=expand, shrink=shrink, markup=markup, name=name, id=id, classes=classes, disabled=disabled)
        self.service_interface = service_interface

    def compose(self) -> ComposeResult:
        self.bar = ProgressBar(show_percentage=False, show_eta=False)
        self.bar.total = 100
        self.bar.progress = self.service_interface.current_volume
        yield self.bar
        yield VolumeButton("Increase", id="increase", variant="success")
        yield VolumeButton("Decrease", id="decrease", variant="success")

    @on(Button.Pressed, "#increase")
    def increase_volume(self) -> None:
        self.service_interface.change_volume(10)
        self.bar.progress = self.service_interface.current_volume

    @on(Button.Pressed, "#decrease")
    def decrease_volume(self) -> None:
        self.service_interface.change_volume(-10)
        self.bar.progress = self.service_interface.current_volume

class DisplayApp(App):
    TITLE = "Music Monitor"
    CSS_PATH = "monitor.css"

    def __init__(self, service_interface : ServiceInterface, driver_class: type[Driver] | None = None, css_path: CSSPathType | None = None, watch_css: bool = False):
        super().__init__(driver_class, css_path, watch_css)
        self.service_interface = service_interface
        
    def compose(self) -> ComposeResult:
        yield ActionButtons(service_interface)
        yield PlayInfoDisplay(service_interface)
        yield VolumeDisplay(service_interface)
        #yield Header()
        #yield Footer()

    def quit(self):
        self.exit()

if __name__ == "__main__":
    service_interface = ServiceInterface()
    app = DisplayApp(service_interface)
    app.run()
