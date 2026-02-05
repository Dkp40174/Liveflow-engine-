[app]
# (str) Title of your application
title = Liveflow Lite

# (str) Package name
package.name = liveflowlite

# (str) Package domain (needed for android/ios packaging)
package.domain = org.liveflow

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning (method 1)
version = 0.1

# (list) Application requirements
# Kivy 2.2.1 sabse stable hai GitHub Actions ke liye
requirements = python3,kivy==2.2.1,pillow

# --- PERMISSIONS (MOST IMPORTANT) ---
# Ye permissions background stream ke liye zaroori hain
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,FOREGROUND_SERVICE,WAKE_LOCK

# --- SCREEN & API SETTINGS ---
orientation = portrait
fullscreen = 1
android.api = 33
android.minapi = 21
android.archs = arm64-v8a
p4a.branch = master

# (int) Android entry point, default is ok for Kivy-based app
android.entrypoint = org.kivy.android.PythonActivity

# (list) List of Java .jar files to add to the libs so that pyjnius can access
# android.add_jars = foo.jar,bar.jar,path/to/more/*.jar

# (list) List of Java files to add to the android project (can be java or a
# directory containing the files)
android.add_src = 

# (bool) Indicate whether the screen should stay on
# Don't sleep the screen while streaming
android.wakelock = True

# iOS settings (Hum use nahi kar rahe par rakhna padta hai)
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master
ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.10.0
ios.codesign.allowed = false

