[app]
title = Liveflow Lite
package.name = liveflowlite
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy==2.2.1

# Permissions
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,FOREGROUND_SERVICE,WAKE_LOCK

# Screen
orientation = portrait
fullscreen = 1
android.api = 33
android.minapi = 21
android.archs = arm64-v8a

# Setup
p4a.branch = stable
android.entrypoint = org.kivy.android.PythonActivity
android.wakelock = True
