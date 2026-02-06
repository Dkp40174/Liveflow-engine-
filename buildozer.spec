[app]
title = Liveflow Engine
package.name = liveflowengine
package.domain = org.akumasmp
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy==2.2.1,ffmpeg
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,FOREGROUND_SERVICE,WAKE_LOCK,ACCESS_NETWORK_STATE
orientation = portrait
fullscreen = 0
android.api = 33
android.minapi = 21
android.archs = arm64-v8a
p4a.branch = release-2022.12.20
android.entrypoint = org.kivy.android.PythonActivity
