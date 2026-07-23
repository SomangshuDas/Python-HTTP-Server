# Python HTTP Server

A tiny Windows utility that turns any folder (or single file) into an instant, shareable HTTP link on your local network — with the URL auto-copied to your clipboard and a scannable QR code printed right in the console.

No setup, no config files. Point it at a folder, get a link, share it with any device on the same Wi-Fi/LAN.

## Features

- **Instant local file sharing** — serve any directory or single file over HTTP in seconds.
- **Auto-clipboard copy** — the shareable URL is copied for you the moment the server starts.
- **In-console QR code** — scan it with a phone to open the link immediately, no typing required.
- **Shell integration (installer build)** — right-click any file, folder, or drive and choose "Open with Python HTTP Server."
- **Folder shortcuts** — type `desktop`, `downloads`, `documents`, `pictures`, `music`, or `videos` instead of a full path.
- **Threaded server** — built on `ThreadingHTTPServer`, so multiple devices can download at once without blocking each other.

## How it works

1. Run the program.
2. Enter a folder or file path (or use a shortcut like `desktop`).
3. Enter a port, or press Enter to use the default `8080`.
4. The server starts, prints the URL, copies it to your clipboard, and shows a QR code.
5. Open the link from any device on the same network, or scan the QR code.
6. Press `Ctrl+C` to stop the server.

## Download (recommended for most users)

If you just want to use the app, grab the prebuilt installer from the **[Releases](../../releases)** page — no Python required. Run the setup file, and the app will be installed with Start Menu shortcuts and optional right-click context menu integration.

## Running from source

Requires Python 3.9+.

```bash
git clone https://github.com/SomangshuDas/Python-HTTP-Server.git
cd Python-HTTP-Server
pip install -r requirements.txt
python src/python_http_server.py
```

## Building it yourself

### 1. Build the executable

The build script uses [PyInstaller](https://pyinstaller.org/) and expects to be run from inside `build_tools/`:

```bash
pip install -r requirements.txt
pip install pyinstaller
cd build_tools
build.bat
```

This produces `dist/Python_HTTP_Server.exe`.

### 2. Stamp it with version info (optional)

PyInstaller doesn't embed `version_info.txt` automatically — it has to be injected afterward with [Resource Hacker](http://www.angusj.com/resourcehacker/):

1. Open `dist/Python_HTTP_Server.exe` in Resource Hacker.
2. **Action → Add a new resource...** (or `Ctrl+T`), choose the **VERSION_INFO** script template.
3. Paste in the contents of `build_tools/version_info.txt`.
4. **Action → Compile Script** (or `F5`).
5. **File → Save** (or `Ctrl+S`) — this writes a new exe with the version resource baked in, under the same filename.
6. Rename the untouched original as a backup, e.g. `Python_HTTP_Server_original.exe`, if you want to keep it around.

### 3. Build the Windows installer (optional)

The installer is built with [Inno Setup](https://jrsoftware.org/isinfo.php):

1. Install Inno Setup.
2. Open `installer/python_http_server.iss` in the Inno Setup Compiler (or right-click → Compile).
3. It picks up `dist/Python_HTTP_Server.exe` and `assets/python_http_server.ico` automatically and outputs `dist/Python_HTTP_Server_Setup.exe`.

See `dist/PLACE_EXE_FILES_HERE.md` for notes on where local builds land and how to publish them.

## Project structure

```
Python-HTTP-Server/
├── src/
│   └── python_http_server.py     # Main application source
├── assets/
│   └── python_http_server.ico    # App / installer icon
├── build_tools/
│   ├── build.bat                 # PyInstaller build script
│   └── version_info.txt          # Windows EXE version resource info
├── installer/
│   └── python_http_server.iss    # Inno Setup installer script
├── dist/                         # Local build output (git-ignored)
├── requirements.txt
├── LICENSE
└── README.md
```

## Requirements

- Windows (the console icon fix, clipboard, and installer are Windows-specific; the server itself is cross-platform)
- Python 3.9+
- Dependencies listed in `requirements.txt`:
  - [`qrcode`](https://pypi.org/project/qrcode/)
  - [`pyperclip`](https://pypi.org/project/pyperclip/)

## Notes

- The server binds to `0.0.0.0`, meaning it's reachable by any device on the same local network as your machine — don't run it on a network you don't trust, and stop it (`Ctrl+C`) when you're done sharing.
- Firewall prompts may appear the first time you run it; allow access on private/home networks.

## License

Released under the [MIT License](LICENSE) © 2026 Somangshu Das.
