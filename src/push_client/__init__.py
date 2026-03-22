"""push_client 包常量"""

from pathlib import Path

# 应用名称（窗口标题、托盘提示、应用名兼用）
APP_NAME = "BeaverPush - 河狸推流"

# 应用图标路径（窗口图标和托盘图标兼用）
APP_ICON_PATH = str(Path(__file__).resolve().parent.parent.parent / "assets" / "beaver_logo.ico")
