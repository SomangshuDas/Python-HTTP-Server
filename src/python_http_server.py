"""
Python HTTP Server
-------------------
A lightweight command-line utility that turns any folder (or single file)
on a Windows machine into a quick, shareable HTTP endpoint on the local
network. It prints the shareable URL, copies it straight to the clipboard,
and renders a scannable QR code in the console so a phone on the same
network can open it in one scan.

Author: Somangshu Das
"""

import os
import sys
import ctypes
import socket
import qrcode
import pyperclip
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

# Bind to all network interfaces so the server is reachable from other
# devices on the same LAN, not just localhost.
host = "0.0.0.0"


def fix_console_icon():
    """
    Replace the default console window icon with the bundled app icon.

    Windows shows a generic console icon for any terminal-based EXE unless
    the taskbar/title-bar icon is explicitly swapped at runtime. This is a
    Windows-only cosmetic fix and is skipped entirely on other platforms.
    """
    if sys.platform != "win32":
        return
    try:
        hwnd = ctypes.windll.kernel32.GetConsoleWindow()
        if not hwnd:
            return
        # Extract icon index 0 (the first embedded icon) from the running
        # executable itself, so this works whether run as a .py or .exe.
        hicon = ctypes.windll.shell32.ExtractIconW(None, sys.executable, 0)
        if hicon:
            # WM_SETICON = 0x0080; wParam 0 = small icon, 1 = big icon.
            ctypes.windll.user32.SendMessageW(hwnd, 0x0080, 0, hicon)
            ctypes.windll.user32.SendMessageW(hwnd, 0x0080, 1, hicon)
    except Exception:
        # Never let a cosmetic failure crash the server.
        pass


# Friendly shortcuts so users can type "desktop" instead of a full path.
# Each key maps to a folder under the current user's home directory.
SHORTCUTS = {
    "desktop": "Desktop",
    "documents": "Documents",
    "downloads": "Downloads",
    "music": "Music",
    "pictures": "Pictures",
    "videos": "Videos",
}


def safe_input(prompt):
    """
    Wrap input() so Ctrl+C during a prompt exits cleanly instead of
    printing a Python traceback.
    """
    try:
        return input(prompt)
    except KeyboardInterrupt:
        raise SystemExit


def get_local_ip():
    """
    Determine the machine's LAN IP address.

    Opens a UDP "connection" to a public address (no packets are actually
    sent for UDP until data is written) purely so the OS tells us which
    local interface/IP it would use to reach the outside world. Falls back
    to loopback if the machine has no network route.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"
    finally:
        s.close()


def resolve_shortcut(raw):
    """
    Expand a shortcut keyword (e.g. "desktop") into a full path under the
    user's home directory. Any path that isn't a recognized shortcut is
    returned unchanged (after trimming quotes/whitespace).
    """
    raw = raw.strip().strip('"')
    normalized = raw.replace("/", "\\")
    parts = normalized.split("\\")
    home = os.path.expanduser("~")
    first = parts[0].lower()
    if first in SHORTCUTS:
        base = os.path.join(home, SHORTCUTS[first])
        rest = parts[1:]
        return os.path.join(base, *rest) if rest else base
    return raw


def resolve_directory(path):
    """
    Given a path that may point to a file or a directory, return the
    directory to serve from and, if applicable, the specific filename to
    link to directly.
    """
    path = os.path.abspath(path)
    if os.path.isfile(path):
        return os.path.dirname(path), os.path.basename(path)
    return path, None


def print_qr(url):
    """Render a scannable ASCII QR code for the given URL in the console."""
    qr = qrcode.QRCode(border=1)
    qr.add_data(url)
    qr.make(fit=True)
    qr.print_ascii(invert=True)


def copy_url(url):
    """Copy the server URL to the system clipboard for quick pasting."""
    pyperclip.copy(url)


def start_banner():
    print("===============================")
    print("  Starting Python HTTP Server  ")
    print("===============================\n")


def stop_banner():
    print("\n===============================")
    print("  Stopping Python HTTP Server  ")
    print("===============================")


def main():
    fix_console_icon()
    start_banner()

    # Allow the target path to be passed as a command-line argument
    # (e.g. via "Open with" / right-click shell integration), otherwise
    # fall back to an interactive prompt.
    if len(sys.argv) > 1:
        path = sys.argv[1]
        port_prompt = "Enter port (default 8080): "
    else:
        path = safe_input("Enter directory or file path: ").strip()
        port_prompt = "\nEnter port (default 8080): "

    if not path:
        print("\nError: No directory specified.")
        return

    path = resolve_shortcut(path)
    if not os.path.exists(path):
        print("\nError: The specified path does not exist.")
        return

    directory, target_file = resolve_directory(path)
    os.chdir(directory)

    port_input = safe_input(port_prompt).strip()
    if port_input == "":
        port = 8080
    elif port_input.isdigit():
        port = int(port_input)
    else:
        print("\nError: Invalid port.")
        return

    ip = get_local_ip()
    url = f"http://{ip}:{port}/{target_file}" if target_file else f"http://{ip}:{port}"

    print("\n===============================")
    print(f"\nDirectory: {directory}\n")
    print(f"IPv4 Address: {url}\n")
    print(f"Port: {port}\n")
    print("===============================\n")

    copy_url(url)

    print("Scan QR code to open:")
    print_qr(url)
    print("\n===============================\n")
    print("Server running... (Press CTRL+C to stop)\n")

    server = ThreadingHTTPServer((host, port), SimpleHTTPRequestHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        stop_banner()
        server.server_close()


if __name__ == "__main__":
    main()
