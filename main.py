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

# Dark Theme Background
Window.clearcolor = (0.1, 0.1, 0.1, 1)

class LiveflowLite(App):
    stream_process = None

    def build(self):
        # 1. PERMISSIONS (Start hote hi maang lega)
        if platform == 'android':
            try:
                from android.permissions import request_permissions, Permission
                request_permissions([
                    Permission.READ_EXTERNAL_STORAGE,
                    Permission.WRITE_EXTERNAL_STORAGE,
                    Permission.INTERNET,
                    Permission.FOREGROUND_SERVICE
                ])
            except: pass

        # 2. UI LAYOUT
        layout = BoxLayout(orientation='vertical', padding=30, spacing=20)

        # Title
        layout.add_widget(Label(text="LIVEFLOW LITE", font_size='24sp', bold=True, size_hint_y=0.15, color=(0, 1, 1, 1)))
        
        # Key Input Box
        self.key_input = TextInput(
            hint_text="Paste YouTube Stream Key Here", 
            multiline=False, 
            size_hint_y=None, 
            height=120,
            background_color=(0.2, 0.2, 0.2, 1),
            foreground_color=(1, 1, 1, 1),
            padding_y=[20, 0]
        )
        
        # 3. LOAD SAVED KEY (Memory se purani key uthao)
        self.store = JsonStore('livedata.json')
        if self.store.exists('user_settings'):
            self.key_input.text = self.store.get('user_settings')['stream_key']
            
        layout.add_widget(self.key_input)

        # Status Label
        self.status_label = Label(text="Ready to Stream", color=(0.5, 0.5, 0.5, 1), size_hint_y=0.15)
        layout.add_widget(self.status_label)

        # Start Button
        btn_start = Button(
            text="START STREAM", 
            background_color=(0, 0.8, 0, 1),
            size_hint_y=None, height=150,
            bold=True
        )
        btn_start.bind(on_press=self.start_thread)
        layout.add_widget(btn_start)

        # Stop Button
        btn_stop = Button(
            text="STOP", 
            background_color=(0.8, 0, 0, 1),
            size_hint_y=None, height=150,
            bold=True
        )
        btn_stop.bind(on_press=self.stop_stream)
        layout.add_widget(btn_stop)

        return layout

    def start_thread(self, instance):
        threading.Thread(target=self.start_stream, daemon=True).start()

    def start_stream(self):
        key = self.key_input.text.strip()
        if not key:
            self.status_label.text = "Error: Key Missing!"
            self.status_label.color = (1, 0, 0, 1)
            return
            
        # 4. SAVE KEY (Nayi key ko memory me daalo)
        self.store.put('user_settings', stream_key=key)

        video_path = "/sdcard/live.mp4"
        if not os.path.exists(video_path):
            self.status_label.text = "Error: /sdcard/live.mp4 not found!"
            self.status_label.color = (1, 0, 0, 1)
            return

        rtmp_url = f"rtmp://a.rtmp.youtube.com/live2/{key}"
        
        # FFmpeg Command (Background Optimized)
        command = f'ffmpeg -re -stream_loop -1 -i "{video_path}" -vf scale=1280:720 -b:v 3000k -c:v libx264 -preset ultrafast -f flv "{rtmp_url}"'

        try:
            self.status_label.text = "🔴 LIVE STREAMING ON..."
            self.status_label.color = (0, 1, 0, 1)
            self.stream_process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE)
        except Exception as e:
            self.status_label.text = f"Error: {str(e)}"

    def stop_stream(self, instance):
        if self.stream_process:
            self.stream_process.kill()
            self.stream_process = None
            self.status_label.text = "Stream Stopped."
            self.status_label.color = (1, 1, 0, 1)

if __name__ == '__main__':
    LiveflowLite().run()
      
