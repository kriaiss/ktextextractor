import subprocess
import os
import tempfile
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
        self.tmp_path = None

    def run(self):
        try:
            subprocess.run(["screencapture", "-i", self.tmp_path], check=True)
            if os.path.exists(self.tmp_path) and os.path.getsize(self.tmp_path) > 0:
                self.finished_signal.emit(self.tmp_path)
            else:
                self.error_signal.emit(self.tmp_path)
        except subprocess.CalledProcessError:
            self.error_signal.emit(self.tmp_path)


class Plugin:
    def __init__(self, ktools):
        self.ktools = ktools
        self.name = "ktextextractor"
        self.worker = None
        
        def handler(event):
            mask = (1 << 20) | (1 << 19)
            if event.keyCode() == 7 and (event.modifierFlags() & mask) == mask:
                QTimer.singleShot(0, self.extract_text)
                return None
            return event

        self.global_monitor = NSEvent.addGlobalMonitorForEventsMatchingMask_handler_(NSKeyDownMask, handler)
        self.local_monitor = NSEvent.addLocalMonitorForEventsMatchingMask_handler_(NSKeyDownMask, handler)
        
        self.action = QAction("open ktextextractor (⌥⌘X)", self.ktools.menu)
        self.action.triggered.connect(self.extract_text)

    def extract_text(self):
        if self.worker and self.worker.isRunning():
            return

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            tmp_path = tmp.name

        if not self.worker:
            self.worker = CaptureWorker()
            self.worker.finished_signal.connect(self._on_capture_success)
            self.worker.error_signal.connect(self._on_capture_failed)

        self.worker.tmp_path = tmp_path
        self.worker.start()

    def _on_capture_success(self, tmp_path):
        try:
            text = self._recognize_text(tmp_path)
            if text:
                QApplication.clipboard().setText(text)
                print(f"ktextextractor: copied to clipboard")
                QTimer.singleShot(200, lambda: self.ktools.notify("text copied to clipboard"))
            else:
                print(f"ktextextractor: no text found.")
                QTimer.singleShot(200, lambda: self.ktools.notify("no text found"))
        finally:
            self._clean_file(tmp_path)

    def _on_capture_failed(self, tmp_path):
        print(f"ktextextractor: capture cancelled or empty.")
        self._clean_file(tmp_path)

    def _clean_file(self, tmp_path):
        if os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except:
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
    
    def _vision_completion(self, request, error):
        if error:
            print(f"ktextextractor: vision error: {error}")
            return
        observations = request.results()
        if observations:
            for observation in observations:
                top_candidate = observation.topCandidates_(1)[0]
                self._ocr_results.append(top_candidate.string())

    def unload(self):
        try:
            if hasattr(self, 'global_monitor'):
                NSEvent.removeMonitor_(self.global_monitor)
                self.global_monitor = None
            if hasattr(self, 'local_monitor'):
                NSEvent.removeMonitor_(self.local_monitor)
                self.local_monitor = None
        except: pass

        if self.worker:
            try:
                self.worker.finished_signal.disconnect()
                self.worker.error_signal.disconnect()
            except: pass
            if self.worker.isRunning():
                self.worker.terminate()
                self.worker.wait()
            self.worker = None

        try:
            self.action.triggered.disconnect()
        except: pass

        import gc
        gc.collect()
        print("ktextextractor: reloaded")

    def _hotkey_handler(self, event):
        mask = (1 << 20) | (1 << 19)
        if event.keyCode() == 7 and (event.modifierFlags() & mask) == mask:
            QTimer.singleShot(0, self.extract_text)
            return None
        return event

    def update_theme(self):
        pass

    def get_actions(self):
        return [self.action]