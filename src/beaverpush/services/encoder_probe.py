"""
硬件编码器探测
==============

在应用启动时调用 :func:`detect_available_encoders` 探测当前机器实际可用的
视频编码器，UI 只会展示这些编码器供用户选择，避免出现"选了 nvenc 但是机器
没有 N 卡"等运行时报错。

探测流程：
    1. 调用 ``ffmpeg -hide_banner -encoders`` 列出 FFmpeg 注册的全部编码器；
       如果某个候选编码器没有出现在输出中，直接判定不可用。
    2. 对剩下的硬件编码器（``*_nvenc`` / ``*_qsv``），用一帧极小的
       ``testsrc`` 实际跑一次编码到 ``-f null``，若返回码为 0 则视为可用。
       这一步可以排除"FFmpeg 编进了 nvenc 但驱动 / 硬件不支持"的场景。
"""

from __future__ import annotations

import subprocess

from .ffmpeg_path import get_ffmpeg
from .log_service import logger

CREATE_NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)

# 可能展示给用户的全部编码器（顺序即 UI 顺序）。
# 软件编码器认为始终可用；硬件编码器需要实际探测。
SOFTWARE_ENCODERS: tuple[str, ...] = ("libx264", "libx265")
HARDWARE_ENCODERS: tuple[str, ...] = (
    "h264_nvenc", "hevc_nvenc",
    "h264_qsv", "hevc_qsv",
)


def _ffmpeg_lists_encoder(name: str, timeout: float = 5.0) -> bool:
    """快速判断 FFmpeg 是否注册了某个编码器。"""
    try:
        result = subprocess.run(
            [get_ffmpeg(), "-hide_banner", "-encoders"],
            capture_output=True,
            text=True,
            timeout=timeout,
            creationflags=CREATE_NO_WINDOW,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        return False
    return f" {name} " in result.stdout


def _probe_encoder(name: str, timeout: float = 8.0) -> bool:
    """尝试用 1 帧 ``testsrc`` 实际跑一次该编码器，返回是否成功。"""
    try:
        result = subprocess.run(
            [
                get_ffmpeg(), "-hide_banner", "-y",
                "-f", "lavfi",
                "-i", "testsrc=duration=1:size=320x240:rate=1",
                "-frames:v", "1",
                "-c:v", name,
                "-f", "null", "-",
            ],
            capture_output=True,
            text=True,
            timeout=timeout,
            creationflags=CREATE_NO_WINDOW,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        return False
    return result.returncode == 0


def detect_available_encoders() -> list[str]:
    """探测当前机器实际可用的编码器列表。

    返回示例：``["libx264", "libx265", "h264_qsv", "hevc_qsv"]``

    规则：
        * 软件编码器只检查 ``ffmpeg -encoders`` 列表，缺失则跳过。
        * 硬件编码器除列表检查外，还会实际跑一次极短编码确认硬件可用。
        * 任何探测异常都视为该编码器不可用，不抛出。
    """
    available: list[str] = []
    for name in SOFTWARE_ENCODERS:
        if _ffmpeg_lists_encoder(name):
            available.append(name)
        else:
            logger.info("FFmpeg 未注册编码器 {}，跳过", name)

    for name in HARDWARE_ENCODERS:
        if not _ffmpeg_lists_encoder(name):
            logger.info("FFmpeg 未注册硬件编码器 {}，跳过", name)
            continue
        if not _probe_encoder(name):
            logger.info("硬件编码器 {} 探测失败，硬件/驱动可能不支持", name)
            continue
        available.append(name)
        logger.info("硬件编码器 {} 可用", name)

    return available
