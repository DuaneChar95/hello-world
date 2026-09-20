# PyInstaller spec: one windowed launcher, one console app beside it.
# Build with:  pyinstaller mtga-coach.spec --noconfirm
import os

block_cipher = None
ICON = os.path.join("assets", "mtga-coach.ico")
DATAS = [("data", "data"), ("assets", "assets")]
HIDDEN = ["tkinter", "tkinter.font", "tkinter.filedialog", "tkinter.messagebox"]

gui_a = Analysis(["launcher.py"], pathex=["."], binaries=[], datas=DATAS,
                 hiddenimports=HIDDEN, hookspath=[], runtime_hooks=[],
                 excludes=[], cipher=block_cipher)
cli_a = Analysis(["run_overlay.py"], pathex=["."], binaries=[], datas=DATAS,
                 hiddenimports=HIDDEN, hookspath=[], runtime_hooks=[],
                 excludes=[], cipher=block_cipher)

gui_pyz = PYZ(gui_a.pure, gui_a.zipped_data, cipher=block_cipher)
cli_pyz = PYZ(cli_a.pure, cli_a.zipped_data, cipher=block_cipher)

gui_exe = EXE(gui_pyz, gui_a.scripts, gui_a.binaries, gui_a.zipfiles, gui_a.datas, [],
              name="MTGA Coach", debug=False, bootloader_ignore_signals=False,
              strip=False, upx=True, console=False, icon=ICON)

cli_exe = EXE(cli_pyz, cli_a.scripts, cli_a.binaries, cli_a.zipfiles, cli_a.datas, [],
              name="MTGA Coach (console)", debug=False, bootloader_ignore_signals=False,
              strip=False, upx=True, console=True, icon=ICON)
