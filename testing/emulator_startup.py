import screen_capture_tools
import AutoRecruit


# emulator startup testing
emulator_path = r"C:\Program Files\Google\Play Games\Bootstrapper.exe"
emulator_title = "Google Play Games beta"
emu = screen_capture_tools.SourceWindow(emulator_title)
AutoRecruit.start_AutoRecruit(emulator_path, emulator_title)
