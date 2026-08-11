<div align="center">
    <pre>
    __      __                   __                   __                        __                
    |  | ___/  |_  ____ ___  ____/  |_  ____ ___  ____/  |_____________    _____/  |_  ___________ 
    |  |/ /\   __\/ __ \\  \/  /\   __\/ __ \\  \/  /\   __\_  __ \__  \ _/ ___\   __\/  _ \_  __ \
    |    <  |  | \  ___/ >    <  |  | \  ___/ >    <  |  |  |  | \// __ \\  \___|  | (  <_> )  | \/
    |__|_ \ |__|  \___  >__/\_ \ |__|  \___  >__/\_ \ |__|  |__|  (____  /\___  >__|  \____/|__|   
        \/           \/      \/           \/      \/                  \/     \/                   
    </pre>
</div>
<p align="center">
    Native OCR plugin for ktools.
</p>
<p align="center">
    <img src="https://img.shields.io/badge/python-3.12+-blue?style=flat-square" alt="Python">
    <img src="https://img.shields.io/badge/platform-macOS-lightgrey?style=flat-square" alt="Platform">
</p>

⠀

## What is ktextextractor?

`ktextextractor` is an OCR (Optical Character Recognition) plugin for `ktools`. It lets you instantly grab unselectable text from images, videos, or protected documents anywhere on your screen.

### Core Features
* **Vision Framework**: Leverages Apple's native machine learning framework (`VNRecognizeTextRequest`) to extract text locally and instantly. No cloud APIs, no privacy leaks.
* **Headless Extraction**: Select an area on your screen and the text is copied automatically. No UI bloat or popups.
* **Global Hotkeys**: Always ready in the background via a system-wide macOS shortcut.

⠀

## How to Use (For Users)

1. Download the `ktextextractor` `.zip` archive from the Releases page.
2. Open the **ktools Plugin Manager** from your menu bar and click **import plugins** to install it.
3. *Note: `ktools` will automatically install the necessary `pyobjc-framework-vision` and `pyobjc-framework-quartz` dependencies in the background.*
4. Press the global hotkey: `⌥⌘X` (Option + Command + X).
5. Your cursor will turn into the native macOS selection crosshair. Drag over the text you want to extract.
6. The OCR engine will process the image in the background and copy the raw text to your clipboard.

⠀

by kriaiss.
