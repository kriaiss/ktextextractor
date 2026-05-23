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
    OCR plugin for ktools.
</p>
<p align="center">
    <img src="https://img.shields.io/badge/python-3.12+-blue?style=flat-square" alt="Python">
    <img src="https://img.shields.io/badge/platform-macOS-lightgrey?style=flat-square" alt="Platform">
</p>

⠀

# what is this?

ktextextractor is the flagship OCR plugin for ktools. it leverages Apple’s native Vision framework to pull text out of anything on ur screen. no cloud APIs, no privacy leaks—just pure local machine learning goodness.

### features

* native vision framework: utilizes VNRecognizeTextRequest under the hood. it's fast, accurate, and runs entirely on the Apple Neural Engine.
* multi-language support: detects English, Russian, Chinese, Spanish, German, French, Italian, Japanese, and Korean out of the box.
* headless extraction: select, grab, copy. no UI clutter.
* async lifecycle: OCR runs in a background thread so ur main app won't hang during heavy analysis.

⠀

# how to use

### 1. summoning the tool

just hit

```
⌥⌘X (option + command + x)
```

global event monitors capture this shortcut anywhere in the OS.

### 2. interaction

* ur cursor turns into the selection crosshair.
* define the region.
* ktextextractor immediately performs OCR on that crop and spits the result into ur clipboard.
* u'll see a native ktools notification once the text is ready for cmd+v.

⠀

### final thoughts

this is the absolute final plugin in this set. i am completely drained and at my limit, so i’m taking a hard break. for the next week, i’m officially off the clock - i plan to do absolutely nothing productive and stay as far away from keyboards as humanly possible. my wrists have officially declared a state of emergency.

also, along with all the plugin dependencies, i’ve accidentally picked up a serious caffeine dependency. absolutely love my life.

and one more thing: notice how the naming convention got progressively worse and more unhinged with each plugin? the later i wrote it, the longer and more cursed the name became. i’m clearly losing it. live with it, lol.

want more final thoughts? i not.

by kriaiss.

this is 67 line lol
676767676767676767