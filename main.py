from subprocess import Popen, call
from win32gui import FindWindow, SetWindowPos, SetForegroundWindow
from win32con import HWND_TOP, SWP_NOSIZE

from pywinauto import Desktop, Application

from pyautogui import write, press
from pyperclip import paste

from constants import PATH_TO_SDA, PATH_TO_STEAM, LOGINS, PASSWORDS, POSITIONS

from time import sleep


def window_exists(window_title):
    return FindWindow(None, window_title) != 0


def wait_for_window(window_title):
    while not window_exists(window_title):
        pass


def activate_window(window_title):
    hwnd = FindWindow(None, window_title)
    SetForegroundWindow(hwnd)


def launch_sda():
    Popen(PATH_TO_SDA, shell=True)
    wait_for_window('Steam Desktop Authenticator')


def configure_sda():
    if not window_exists('Steam Desktop Authenticator'):
        launch_sda()
    hwnd = FindWindow(None, 'Steam Desktop Authenticator')
    SetWindowPos(hwnd, HWND_TOP, 100, 100, 0, 0, SWP_NOSIZE)


def generate_bat_file(position: tuple):
    # generate batch to launch an account with given credentials
    x, y = position

    batch_commands = f"""@echo off
start "" "{PATH_TO_STEAM}" -dev -nofriendsui -no-dwrite -nointro -nobigpicture -nofasthtml -nocrashmonitor -noshaders  -no-shared-textures -disablehighdpi -cef-single-process -cef-in-process-gpu -single_core -cef-disable-d3d11 -cef-disable-sandbox -disable-winh264 -no-cef-sandbox -vrdisable -cef-disable-breakpad -language english -no-browser -applaunch 730 -low -nohltv -nosound -novid -window -w 320 -h 240 -x {x} -y {y}
"""
    with open(f"launch_cs.bat", "w") as file:
        file.write(batch_commands)


def paste_credentials(login: str, password: str):
    sleep(1)
    write(login)
    press('tab')
    write(password)
    press('Enter')


def paste_steam_guard():
    write(paste())


def copy_steam_guard_for_account(login: str):
    window_title = "Steam Desktop Authenticator"

    # Connect to the window using the window title
    app = Application(backend="uia").connect(title=window_title)
    window_handle = app.window(title=window_title).handle

    # Activate the window using its handle
    desktop = Desktop()
    window = desktop.window(handle=window_handle)
    window.set_focus()

    # Find the login item and click it
    window['list'].select(login.lower())

    # Click the "Copy" button
    window['Copy'].click()


def run_csgo_instance(login: str, password: str, position: tuple):
    # generate batch file and launch an account with given credentials
    generate_bat_file(position)
    call(f"launch_cs.bat")
    wait_for_window("Sign in to Steam")
    activate_window("Sign in to Steam")
    paste_credentials(login, password)
    activate_window("Steam Desktop Authenticator")
    copy_steam_guard_for_account(login)
    activate_window("Sign in to Steam")
    sleep(5)
    paste_steam_guard()


def run_all_csgo_windows():
    for login, password, position in zip(LOGINS, PASSWORDS, POSITIONS):
        """
        iterate through logins and passwords, thereby generating batch files and launching instances of cs:go
        """
        run_csgo_instance(login, password, position)


def main():
    configure_sda()
    run_all_csgo_windows()


if __name__ == '__main__':
    main()
