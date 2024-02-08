import subprocess

players = ["spotify"]

class ServiceInterface():
    def __init__(self) -> None:
        self.current_volume = self.get_volume()

    def previous(self) -> None:
        subprocess.call(("playerctl", f"--player={','.join(players)}", "previous"))

    def pause_play(self) -> None:
        subprocess.call(("playerctl", f"--player={','.join(players)}", "play-pause"))

    def next(self) -> None:
        subprocess.call(("playerctl", f"--player={','.join(players)}", "next"))

    def get_volume(self) -> int:
        return int(float(subprocess.run(
                ["playerctl", f"--player={','.join(players)}", "metadata", "--format", "{{ volume * 100 }}"],
                stdout=subprocess.PIPE
            ).stdout.decode("utf8").strip()))

    def change_volume(self, delta : int) -> None:
        self.current_volume += delta
        self.current_volume = max(0, min(100, self.current_volume))
        subprocess.call(("playerctl", f"--player={','.join(players)}", "volume", f"{self.current_volume / 100}"))

    def get_info(self) -> dict:
        return {
            "title" : subprocess.run(
                    ["playerctl", f"--player={','.join(players)}", "metadata", "--format", "{{ title }}"],
                    stdout=subprocess.PIPE
                ).stdout.decode("utf8").strip(),
            "art" : subprocess.run(
                    ["playerctl", f"--player={','.join(players)}", "metadata", "--format", "{{ mpris:artUrl }}"],
                    stdout=subprocess.PIPE
                ).stdout.decode("utf8").strip(),
            "album" : subprocess.run(
                    ["playerctl", f"--player={','.join(players)}", "metadata", "--format", "{{ album }}"],
                    stdout=subprocess.PIPE
                ).stdout.decode("utf8").strip(),
            "artist" : subprocess.run(
                    ["playerctl", f"--player={','.join(players)}", "metadata", "--format", "{{ artist }}"],
                    stdout=subprocess.PIPE
                ).stdout.decode("utf8").strip(),
            "duration" : int(subprocess.run(
                    ["playerctl", f"--player={','.join(players)}", "metadata", "--format", "{{ mpris:length }}"],
                    stdout=subprocess.PIPE
                ).stdout.decode("utf8").strip()),
            "position" : int(subprocess.run(
                    ["playerctl", f"--player={','.join(players)}", "metadata", "--format", "{{ position }}"],
                    stdout=subprocess.PIPE
                ).stdout.decode("utf8").strip()),
            "volume" : int(float(subprocess.run(
                    ["playerctl", f"--player={','.join(players)}", "metadata", "--format", "{{ volume * 100 }}"],
                    stdout=subprocess.PIPE
                ).stdout.decode("utf8").strip())),
        }
