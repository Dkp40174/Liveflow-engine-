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
from kivy.utils import platform

Window.clearcolor = (0.1, 0.1, 0.1, 1)

class LiveflowLite(App):
    stream_process = None
    def build(self):
        if platform == 'android':
            try:
                from android.permissions import request_permissions, Permission
                request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE, Permission.INTERNET, Permission.FOREGROUND_SERVICE])
            except: pass
        layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        layout.add_widget(Label(text="LIVEFLOW LITE", font_size='24sp', bold=True, size_hint_y=0.15, color=(0, 1, 1, 1)))
        self.key_input = TextInput(hint_text="Paste Stream Key Here", multiline=False, size_hint_y=None, height=120, background_color=(0.2, 0.2, 0.2, 1), foreground_color=(1, 1, 1, 1))
        self.store = JsonStore('livedata.json')
        if self.store.exists('user_settings'):
            self.key_input.text = self.store.get('user_settings')['stream_key']
        layout.add_widget(self.key_input)
        self.status_label = Label(text="Ready to Stream", color=(0.5, 0.5, 0.5, 1), size_hint_y=0.15)
        layout.add_widget(self.status_label)
        btn_start = Button(text="START STREAM", background_color=(0, 0.8, 0, 1), size_hint_y=None, height=150, bold=True)
        btn_start.bind(on_press=self.start_thread)
        layout.add_widget(btn_start)
        btn_stop = Button(text="STOP", background_color=(0.8, 0, 0, 1), size_hint_y=None, height=150, bold=True)
        btn_stop.bind(on_press=self.stop_stream)
        layout.add_widget(btn_stop)
        return layout
    def start_thread(self, instance):
        threading.Thread(target=self.start_stream, daemon=True).start()
    def start_stream(self):
        key = self.key_input.text.strip()
        if not key: return
        self.store.put('user_settings', stream_key=key)
        video_path = "/sdcard/live.mp4"
        rtmp_url = f"rtmp://a.rtmp.youtube.com/live2/{key}"
        command = f'ffmpeg -re -stream_loop -1 -i "{video_path}" -vf scale=1280:720 -b:v 3000k -c:v libx264 -preset ultrafast -f flv "{rtmp_url}"'
        try:
            self.status_label.text = "🔴 LIVE..."
            self.stream_process = subprocess.Popen(command, shell=True)
        except: pass
    def stop_stream(self, instance):
        if self.stream_process:
            self.stream_process.kill()
            self.stream_process = None
            self.status_label.text = "Stopped"

if __name__ == '__main__':
    LiveflowLite().run()
    
