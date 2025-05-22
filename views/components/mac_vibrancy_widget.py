# from PySide6.QtWidgets import QMacCocoaViewContainer, QWidget
# from utils.platform_utils import HAS_NSVIEW
# from PySide6.QtGui import NSVisualEffectView, NSVisualEffectMaterial, NSVisualEffectBlendingMode, NSAppearance

# class MacVibrancyWidget(QMacCocoaViewContainer if HAS_NSVIEW else QWidget):
#     """MacOS specific vibrancy effect widget"""
    
#     def __init__(self, parent=None):
#         super().__init__(0, parent)
        
#         if HAS_NSVIEW:
#             # Create NSVisualEffectView
#             self.effect_view = NSVisualEffectView.alloc().initWithFrame_((0, 0), (100, 100))
#             self.effect_view.setMaterial_(NSVisualEffectMaterial.underWindowBackground)
#             self.effect_view.setBlendingMode_(NSVisualEffectBlendingMode.behindWindow)
#             self.effect_view.setState_(1)  # Active state
#             self.effect_view.setAutoresizingMask_(18)  # width + height
            
#             # Set the NSView
#             self.setCocoaView(self.effect_view)
#         else:
#             # Fallback for non-macOS systems
#             self.setObjectName("macVibrancyWidget")
    
#     def set_dark_mode(self, is_dark):
#         """Toggle dark/light mode for macOS"""
#         if HAS_NSVIEW:
#             appearance = NSAppearance.appearanceNamed_("NSAppearanceNameDarkAqua" if is_dark 
#                                                      else "NSAppearanceNameAqua")
#             self.effect_view.setAppearance_(appearance)

from PySide6.QtWidgets import QWidget

class MacVibrancyWidget(QWidget):
    """MacOS specific vibrancy effect widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("macVibrancyWidget")
    