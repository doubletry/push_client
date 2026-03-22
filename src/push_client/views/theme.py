"""
浅冷色系主题
============

提供全局统一的颜色常量和 QSS 样式表，供所有 QWidgets 组件引用。
以纯白为基底，搭配淡蓝灰色表面和冷钢蓝强调色，
营造干净、清透的轻工业视觉风格。

使用方式::

    from push_client.views.theme import Theme
    app.setStyleSheet(Theme.global_stylesheet())
"""

from __future__ import annotations


class Theme:
    """浅冷色系主题色板与全局样式表。

    所有颜色均为 ``#RRGGBB`` 格式的字符串常量，
    可直接在 QSS 或 QPalette 中使用。
    """

    # ── 基础色（白色基底）──
    BASE   = "#ffffff"  # 主背景：纯白
    MANTLE = "#f5f7fa"  # 次级背景：冰蓝白
    CRUST  = "#edf0f5"  # 最深背景：浅灰蓝

    # ── 表面色（输入框、边框、分隔线）──
    SURFACE0 = "#e8ecf1"
    SURFACE1 = "#d5dbe4"
    SURFACE2 = "#c2cada"

    # ── 覆盖色（禁用文本、占位符）──
    OVERLAY0 = "#9ca8b8"
    OVERLAY1 = "#8a97a8"
    OVERLAY2 = "#788698"

    # ── 副文本色 ──
    SUBTEXT0 = "#677585"
    SUBTEXT1 = "#566474"

    # ── 主文本色 ──
    TEXT = "#2c3e50"

    # ── 强调色（冷色系）──
    STEEL    = "#5082b5"   # 钢蓝主色
    SLATE    = "#6a8caa"   # 石板蓝
    CYAN     = "#4a9bb0"   # 冷青
    TEAL     = "#3d9484"   # 冷水绿
    GREEN    = "#48a068"   # 指示灯绿
    RED      = "#d05050"   # 警告红
    AMBER    = "#c08a30"   # 琥珀黄
    ORANGE   = "#b07040"   # 暗橙
    BLUE     = "#4a7ec0"   # 钢蓝强
    ICE      = "#6aafc8"   # 冰蓝

    # ── 语义色 ──
    ACCENT  = STEEL
    SUCCESS = GREEN
    ERROR   = RED
    WARNING = AMBER
    YELLOW  = AMBER

    # ── 字体 ──
    FONT_FAMILY = "Microsoft YaHei UI"
    FONT_SIZE_SMALL  = 8    # pt
    FONT_SIZE_NORMAL = 9    # pt
    FONT_SIZE_LARGE  = 11   # pt

    # ── 圆角半径 ──
    RADIUS_SMALL  = 3
    RADIUS_NORMAL = 5
    RADIUS_LARGE  = 8

    @classmethod
    def global_stylesheet(cls) -> str:
        """生成应用级全局 QSS 样式表。

        浅冷色系：白色底色、淡蓝灰表面、钢蓝强调，
        清爽明亮的专业视觉风格。

        Returns:
            完整的 QSS 字符串，可通过 ``QApplication.setStyleSheet()`` 应用。
        """
        return f"""
        /* ── 全局基础 ── */
        QWidget {{
            background-color: {cls.BASE};
            color: {cls.TEXT};
        }}

        /* ── 按钮 ── */
        QPushButton {{
            background-color: {cls.MANTLE};
            color: {cls.TEXT};
            border: 1px solid {cls.SURFACE1};
            border-radius: {cls.RADIUS_NORMAL}px;
            padding: 5px 14px;
        }}
        QPushButton:hover {{
            background-color: {cls.SURFACE0};
            border-color: {cls.STEEL};
        }}
        QPushButton:pressed {{
            background-color: {cls.SURFACE1};
        }}
        QPushButton:disabled {{
            background-color: {cls.MANTLE};
            color: {cls.OVERLAY0};
            border-color: {cls.SURFACE0};
        }}

        /* ── 输入框 ── */
        QLineEdit {{
            background-color: {cls.BASE};
            color: {cls.TEXT};
            border: 1px solid {cls.SURFACE1};
            border-radius: {cls.RADIUS_NORMAL}px;
            padding: 4px 8px;
            selection-background-color: {cls.STEEL};
            selection-color: {cls.BASE};
        }}
        QLineEdit:focus {{
            border-color: {cls.STEEL};
        }}
        QLineEdit:read-only {{
            background-color: {cls.CRUST};
            color: {cls.SUBTEXT0};
        }}

        /* ── 下拉框 ── */
        QComboBox {{
            background-color: {cls.BASE};
            color: {cls.TEXT};
            border: 1px solid {cls.SURFACE1};
            border-radius: {cls.RADIUS_NORMAL}px;
            padding: 4px 8px;
        }}
        QComboBox:hover {{
            border-color: {cls.STEEL};
        }}
        QComboBox::drop-down {{
            border: none;
            width: 20px;
        }}
        QComboBox QAbstractItemView {{
            background-color: {cls.BASE};
            color: {cls.TEXT};
            border: 1px solid {cls.SURFACE1};
            border-radius: {cls.RADIUS_SMALL}px;
            selection-background-color: {cls.SURFACE0};
            selection-color: {cls.TEXT};
        }}

        /* ── 复选框 ── */
        QCheckBox {{
            color: {cls.TEXT};
            spacing: 6px;
        }}
        QCheckBox::indicator {{
            width: 16px;
            height: 16px;
            border: 1px solid {cls.SURFACE2};
            border-radius: {cls.RADIUS_SMALL}px;
            background-color: {cls.BASE};
        }}
        QCheckBox::indicator:checked {{
            background-color: {cls.STEEL};
            border-color: {cls.STEEL};
        }}

        /* ── QFrame 卡片 ── */
        QFrame[frameShape="6"] {{
            background-color: {cls.MANTLE};
            border: 1px solid {cls.SURFACE0};
            border-radius: {cls.RADIUS_LARGE}px;
        }}

        /* ── 滚动区域 ── */
        QScrollArea {{
            border: none;
            background-color: transparent;
        }}
        QScrollBar:vertical {{
            background-color: {cls.MANTLE};
            width: 8px;
            border-radius: 4px;
        }}
        QScrollBar::handle:vertical {{
            background-color: {cls.SURFACE1};
            border-radius: 4px;
            min-height: 30px;
        }}
        QScrollBar::handle:vertical:hover {{
            background-color: {cls.SURFACE2};
        }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}

        /* ── 工具提示 ── */
        QToolTip {{
            background-color: {cls.MANTLE};
            color: {cls.TEXT};
            border: 1px solid {cls.SURFACE1};
            border-radius: {cls.RADIUS_SMALL}px;
            padding: 4px;
        }}

        /* ── 对话框 ── */
        QDialog {{
            background-color: {cls.BASE};
        }}
        QMessageBox {{
            background-color: {cls.BASE};
        }}
        """
