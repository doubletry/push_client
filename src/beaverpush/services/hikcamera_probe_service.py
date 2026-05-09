from __future__ import annotations

import threading

from PySide6.QtCore import QThread, Signal

from .hikcamera_capture import (
    probe_hikcamera_size,
)
from .log_service import logger


class HikCameraProbeWorker(QThread):
    """在后台线程中探测海康相机尺寸，避免阻塞 UI 线程。"""

    probe_succeeded = Signal(int, int)
    probe_failed = Signal(str)

    def __init__(
        self,
        serial_number: str,
        timeout_ms: int = 3000,
        *,
        use_sdk_decode: bool = True,
        parent=None,
    ):
        super().__init__(parent)
        self._serial_number = serial_number
        self._timeout_ms = timeout_ms
        self._use_sdk_decode = bool(use_sdk_decode)
        self._stop_requested = threading.Event()

    def stop(self) -> None:
        self._stop_requested.set()

    def run(self) -> None:
        try:
            width, height = probe_hikcamera_size(
                self._serial_number,
                timeout_ms=self._timeout_ms,
                use_sdk_decode=self._use_sdk_decode,
            )
        except Exception as exc:  # noqa: BLE001
            logger.warning("海康相机后台探测失败 sn={} err={}", self._serial_number, exc)
            if not self._stop_requested.is_set():
                self.probe_failed.emit(str(exc))
        else:
            if not self._stop_requested.is_set():
                self.probe_succeeded.emit(width, height)
