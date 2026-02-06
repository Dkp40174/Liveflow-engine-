
import os
import threading
import subprocess
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.storage.jsonstore import JsonStore

# 1. Basic UI Settings
Window.clearcolor = (0.1, 0.1, 0.1, 1)

class LiveflowLite(App):
    stream_process = None

    def build(self):
        # NOTE: Maine yaha se Permission maangne wala code hata diya hai.
        
        # 2. UI Layout
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        # Title
        layout.add_widget(Label(text="LIVEFLOW ENGINE (NO PERM)", font_size='22sp', bold=True, color=(1, 1, 0, 1), size_hint_y=0.1))

        # Input 1: Video File Path
        layout.add_widget(Label(text="Video Path (e.g. /sdcard/live.mp4)", size_hint_y=None, height=30))
        self.path_input = TextInput(text="/sdcard/live.mp4", multiline=False, size_hint_y=None, height=50, background_color=(0.2, 0.2, 0.2, 1), foreground_color=(1, 1, 1, 1))
        layout.add_widget(self.path_input)

        # Input 2: Stream Key
        layout.add_widget(Label(text="YouTube Stream Key", size_hint_y=None, height=30))
        self.key_input = TextInput(hint_text="Paste Key Here", multiline=False, size_hint_y=None, height=50, background_color=(0.2, 0.2, 0.2, 1), foreground_color=(1, 1, 1, 1))
        layout.add_widget(self.key_input)

        # Load saved settings
        self.store = JsonStore('user_data.json')
        if self.store.exists('config'):
            data = self.store.get('config')
            self.path_input.text = data.get('path', '/sdcard/live.mp4')
            self.key_input.text = data.get('key', '')

        # Status Log
        self.status_label = Label(text="Testing Mode...", color=(0, 1, 0, 1), size_hint_y=0.1)
        layout.add_widget(self.status_label)

        # Buttons
        btn_start = Button(text="START STREAM", background_color=(0, 0.8, 0, 1), bold=True, size_hint_y=None, height=80)
        btn_start.bind(on_press=self.start_thread)
        layout.add_widget(btn_start)

        btn_stop = Button(text="STOP", background_color=(0.8, 0, 0, 1), bold=True, size_hint_y=None, height=80)
        btn_stop.bind(on_press=self.stop_stream)
        layout.add_widget(btn_stop)

        return layout

    def start_thread(self, instance):
        threading.Thread(target=self.start_stream, daemon=True).start()

    def start_stream(self):
        path = self.path_input.text.strip()
        key = self.key_input.text.strip()

        if not key:
            self.status_label.text = "Error: Key missing!"
            return
        
        # Save Data
        self.store.put('config', path=path, key=key)

        rtmp_url = f"rtmp://a.rtmp.youtube.com/live2/{key}"
        command = f'ffmpeg -re -stream_loop -1 -i "{path}" -c:v copy -c:a aac -b:a 128k -f flv "{rtmp_url}"'

        try:
            self.status_label.text = "Attempting Stream..."
            # Note: Bina permission ke ye shayad fail ho jaye, par abhi hum build check kar rahe hain
            self.stream_process = subprocess.Popen(command, shell=True)
            self.status_label.text = "Streaming Signal Sent!"
        except Exception as e:
            self.status_label.text = f"Error: {str(e)}"

    def stop_stream(self, instance):
        if self.stream_process:
            self.stream_process.kill()
            self.stream_process = None
            self.status_label.text = "Stopped."

if __name__ == '__main__':
    LiveflowLite().run()
    
