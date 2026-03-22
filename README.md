# القرآن الكريم - Quran App

A beautiful mobile application to listen to the Quran with the recitation of Sheikh Nasser Al-Qatami.

## 📱 Features

- **All 114 Surahs**: Complete Quran with all chapters
- **High Quality Audio**: Recitation by Sheikh Nasser Al-Qatami
- **Download Management**: Download surahs for offline listening
- **Beautiful UI**: Modern dark theme with intuitive interface
- **Easy Navigation**: Simple controls to switch between surahs
- **Arabic Support**: Full RTL support with Arabic font
- **Lightweight**: Minimal resource usage

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Kivy framework
- Android SDK (for APK building)

### Installation

```bash
# Clone the repository
git clone https://github.com/Soukaina-mehdi/Quran-app.git
cd Quran-app

# Install dependencies
pip install -r requirements.txt
```

### Running on Desktop
```bash
python main.py
```

## 📦 Building APK

### Using Buildozer

```bash
# Install Buildozer
pip install buildozer

# Build the APK
buildozer android debug

# Build release APK
buildozer android release
```

The generated APK will be in `bin/` directory.

## 📂 Project Structure

```
Quran-app/
├── main.py                 # Main application file
├── buildozer.spec         # Buildozer configuration for APK building
├── Amiri-Regular.ttf      # Arabic font file
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore file
└── downloads/            # Downloaded audio files (created at runtime)
```

## 🎨 Features Explained

### Surah List Screen
- Displays all 114 surahs
- Shows number of verses
- Download or play buttons
- Delete downloaded files

### Player Screen
- Full playback controls
- Progress bar
- Current/total time display
- Next/Previous navigation
- Return to list button

## 🔊 Audio Source

Audio files are downloaded from: `https://server8.mp3quran.net/qtm/`

## 🛠️ Technical Details

### Built With
- **Kivy**: Cross-platform Python GUI framework
- **Python 3**: Programming language
- **Requests**: HTTP library for downloading audio

### Permissions (Android)
- `INTERNET`: For downloading audio files
- `WRITE_EXTERNAL_STORAGE`: For saving downloaded files
- `READ_EXTERNAL_STORAGE`: For accessing saved files

## 📝 License

This project is open source and available for personal and educational use.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## 📧 Contact

For questions or suggestions, please open an issue on GitHub.

---

**Made with ❤️ for the Ummah**