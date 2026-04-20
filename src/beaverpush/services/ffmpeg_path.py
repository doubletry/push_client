"""
FFmpeg 可执行文件路径解析
=========================

自动查找 ``ffmpeg`` / ``ffplay`` / ``ffprobe`` 的完整路径。

查找顺序：
    1. 程序自带的 ``ffmpeg/`` 子目录（安装包内嵌）
    2. 系统 ``PATH`` 环境变量

使用方式::

    from beaverpush.services.ffmpeg_path import get_ffmpeg, get_ffplay, get_ffprobe

    cmd = [get_ffmpeg(), "-y", "-i", ...]
"""

from __future__ import annotations

import os
import sys
import shutil


def _app_dir() -> str:
    """获取应用程序所在目录。

    打包后 (Nuitka standalone) ``sys.argv[0]`` 指向 exe 所在目录；
    开发模式下同样使用 ``sys.argv[0]`` 所在目录。
    """
    return os.path.dirname(os.path.abspath(sys.argv[0]))


def _candidate_roots() -> list[str]:
    """枚举可能放置内嵌 ``ffmpeg/`` 的根目录，按优先级排序。

    依次尝试：

    1. ``sys.argv[0]`` 所在目录 —— 打包后即 exe 同级目录。
    2. ``sys.argv[0]`` 向上若干层 —— 兼容开发模式从 ``src/beaverpush/main.py``
       启动时，项目根 ``<repo>/ffmpeg/`` 才是真正放二进制的地方。
    3. 当前工作目录 —— 用户在仓库根目录手动启动时也能命中。
    4. 本模块文件向上若干层 —— 兜底覆盖 ``uv run`` / ``python -m`` 等
       ``sys.argv[0]`` 不指向项目目录的启动方式。

    去重后保持插入顺序，避免重复 stat。
    """
    roots: list[str] = []

    def _add(p: str) -> None:
        try:
            real = os.path.abspath(p)
        except Exception:
            return
        if real and real not in roots:
            roots.append(real)

    argv0_dir = _app_dir()
    _add(argv0_dir)
    for up in (1, 2, 3):
        _add(os.path.join(argv0_dir, *([".."] * up)))

    _add(os.getcwd())

    here = os.path.dirname(os.path.abspath(__file__))
    for up in (2, 3, 4):
        # services/ → beaverpush/ → src/ → <repo>
        _add(os.path.join(here, *([".."] * up)))

    return roots


def _find_executable(name: str) -> str:
    """查找可执行文件的完整路径。

    Args:
        name: 可执行文件名（不含 ``.exe`` 后缀）。

    Returns:
        完整路径字符串。如果在内嵌目录和 PATH 中都找不到，
        则返回原始 ``name``，让后续 ``subprocess`` 抛出
        ``FileNotFoundError``。

    内嵌优先级最高，避免用户 ``PATH`` 上的旧 ffmpeg（与新 NVIDIA 驱动
    NVENC SDK 不兼容、preset 列表过时等）让硬件加速整体不可用。
    """
    exe_name = f"{name}.exe" if os.name == "nt" else name

    for root in _candidate_roots():
        # 1) <root>/ffmpeg/<exe>  ——常规内嵌目录
        bundled = os.path.join(root, "ffmpeg", exe_name)
        if os.path.isfile(bundled):
            return bundled
        # 2) <root>/<exe>         ——有些用户直接放同级目录
        same = os.path.join(root, exe_name)
        if os.path.isfile(same):
            return same

    # 3) 系统 PATH —— 仅在没有任何内嵌副本时才使用
    found = shutil.which(name)
    if found:
        return found

    # 4) 回退：返回原始名字，让 subprocess 报错
    return name


def get_ffmpeg() -> str:
    """获取 ``ffmpeg`` 可执行文件路径。"""
    return _find_executable("ffmpeg")


def get_ffplay() -> str:
    """获取 ``ffplay`` 可执行文件路径。"""
    return _find_executable("ffplay")


def get_ffprobe() -> str:
    """获取 ``ffprobe`` 可执行文件路径。"""
    return _find_executable("ffprobe")
