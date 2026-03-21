[app]
title = القرآن الكريم
package.name = quranqatami
package.domain = org.quran
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf
version = 1.0

requirements = python3,kivy==2.2.1,requests,android

# Include the fonts folder inside the APK
source.include_patterns = fonts/*.ttf

orientation = portrait
fullscreen = 0

android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE
android.accept_sdk_license = True
android.api = 33
android.minapi = 21
android.ndk = 25b
android.build_tools_version = 33.0.2
android.archs = arm64-v8a

[buildozer]
log_level = 2
