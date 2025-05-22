import platform
from pathlib import Path

def get_root_path() -> Path:
    return Path(__file__).parents[1]

ROOT_PATH = get_root_path()
RESOURCES_PATH = ROOT_PATH / "resources"

# Check if running on macOS to enable NSVisualEffectView
IS_MACOS = platform.system() == 'Darwin'
IS_WINDOWS = platform.system() == 'Windows'
IS_LINUX = platform.system() == 'Linux'

if IS_MACOS:
    try:
        from AppKit import NSVisualEffectView, NSVisualEffectMaterial, NSVisualEffectBlendingMode, NSAppearance
        from PySide6.QtWidgets import QMacCocoaViewContainer
        HAS_NSVIEW = True
    except ImportError:
        HAS_NSVIEW = False
else:
    HAS_NSVIEW = False
    