import subprocess
import os
import tempfile
import gc
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer, QThread, pyqtSignal
from AppKit import NSEvent, NSKeyDownMask
import Vision
import Quartz
from Foundation import NSURL

class CaptureWorker(QThread):
    finished_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.process = None

    def run(self):
        tmp_path = ""
        try:
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                tmp_path = tmp.name

            self.process = subprocess.Popen(["screencapture", "-i", tmp_path])
            self.process.wait()
            
            if self.process.returncode == 0 and os.path.exists(tmp_path) and os.path.getsize(tmp_path) > 0:
                self.finished_signal.emit(tmp_path)
            else:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
                self.error_signal.emit("capture failed or aborted")
        except Exception as e:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
            self.error_signal.emit(str(e))
    
    def stop(self):
        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=1)
            except Exception:
                self.process.kill()
            self.process = None
        self.quit()
        self.wait()

class Plugin:
    def __init__(self, ktools):
        self.ktools = ktools
        self.name = "ktextextractor"
        self.worker = None
        
        self.global_monitor = NSEvent.addGlobalMonitorForEventsMatchingMask_handler_(NSKeyDownMask, self._global_hotkey_handler)
        self.local_monitor = NSEvent.addLocalMonitorForEventsMatchingMask_handler_(NSKeyDownMask, self._local_hotkey_handler)
        
        self.action = QAction("open ktextextractor (⌥⌘X)", self.ktools.manager)
        self.action.triggered.connect(self.extract_text)

    def get_actions(self):
        return [self.action]

    def update_theme(self):
        pass

    def unload(self):
        try:
            if hasattr(self, 'global_monitor') and self.global_monitor:
                NSEvent.removeMonitor_(self.global_monitor)
                self.global_monitor = None
            if hasattr(self, 'local_monitor') and self.local_monitor:
                NSEvent.removeMonitor_(self.local_monitor)
                self.local_monitor = None
        except Exception: 
            pass

        if self.worker:
            try:
                self.worker.finished_signal.disconnect()
                self.worker.error_signal.disconnect()
            except Exception: 
                pass
            self.worker.stop()
            self.worker.deleteLater()
            self.worker = None

        try:
            self.action.triggered.disconnect()
        except Exception: 
            pass

        # py garbage collector is asleep at the wheel, force collect or memory leaks into the void
        gc.collect()

    def _global_hotkey_handler(self, event):
        mask = (1 << 20) | (1 << 19)
        if event.keyCode() == 7 and (event.modifierFlags() & mask) == mask:
            QTimer.singleShot(0, self.extract_text)

    def _local_hotkey_handler(self, event):
        mask = (1 << 20) | (1 << 19)
        if event.keyCode() == 7 and (event.modifierFlags() & mask) == mask:
            QTimer.singleShot(0, self.extract_text)
            return None
        return event

    def extract_text(self):
        if self.worker and self.worker.isRunning():
            return

        if self.worker:
            self.worker.deleteLater()

        self.worker = CaptureWorker()
        self.worker.finished_signal.connect(self._on_capture_success)
        self.worker.error_signal.connect(self._on_capture_failed)
        self.worker.start()

    def _on_capture_success(self, tmp_path):
        try:
            text = self._recognize_text(tmp_path)
            if text:
                QApplication.clipboard().setText(text)
                QTimer.singleShot(200, lambda: self.ktools.notify("text copied to clipboard"))
            else:
                QTimer.singleShot(200, lambda: self.ktools.notify("no text found"))
        finally:
            self._clean_file(tmp_path)

    def _on_capture_failed(self, tmp_path):
        self._clean_file(tmp_path)

    def _clean_file(self, tmp_path):
        if os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except Exception:
                pass

    def _recognize_text(self, image_path):
        url = NSURL.fileURLWithPath_(image_path)
        request_handler = Vision.VNImageRequestHandler.alloc().initWithURL_options_(url, None)
        
        request = Vision.VNRecognizeTextRequest.alloc().init()
        request.setRecognitionLevel_(Vision.VNRequestTextRecognitionLevelAccurate)
        request.setRecognitionLanguages_([
            "en-US",
            "ru-RU",
            "zh-Hans",
            "es-ES",
            "de-DE",
            "fr-FR",
            "it-IT",
            "ja-JP",
            "ko-KR"
        ])
        
        success, error = request_handler.performRequests_error_([request], None)
        if not success:
            return None
            
        observations = request.results()
        if not observations:
            return None
            
        results = []
        for observation in observations:
            candidates = observation.topCandidates_(1)
            if candidates:
                results.append(candidates[0].string())
        
        return "\n".join(results) if results else None
