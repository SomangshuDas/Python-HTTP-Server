# Where the compiled binaries go

This folder is where your **locally built** files land — it is git-ignored,
so nothing here gets committed or pushed to GitHub:

- `Python_HTTP_Server.exe` — the raw PyInstaller output, produced by running
  `build_tools/build.bat`.
- `Python_HTTP_Server_Setup.exe` — the installer produced by compiling
  `installer/python_http_server.iss` with Inno Setup (it reads the exe above
  from this same folder).

## Publishing the binaries

Since GitHub repos shouldn't contain compiled executables, publish them as
release assets instead:

1. Push the source code to GitHub first.
2. Go to your repo -> **Releases** -> **Draft a new release**.
3. Tag it (e.g. `v1.0.0`), title it, add release notes.
4. Drag and drop both `Python_HTTP_Server.exe` and
   `Python_HTTP_Server_Setup.exe` into the "Attach binaries" area.
5. Publish. The README's download link points users at this Releases page.

This keeps the repo lightweight (source only) while still giving users a
one-click download.
