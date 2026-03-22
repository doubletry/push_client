"""
冷色工业风深色主题
==================

提供全局统一的颜色常量和 QSS 样式表，供所有 QWidgets 组件引用。
灵感来源于工业控制面板的冷色调设计，以深蓝灰为基底，
搭配钢蓝色强调，营造沉稳、专业的轻工业视觉风格。

使用方式::

    from push_client.views.theme import Theme
    app.setStyleSheet(Theme.global_stylesheet())
"""

from __future__ import annotations


class Theme:
    """冷色工业风主题色板与全局样式表。

    所有颜色均为 ``#RRGGBB`` 格式的字符串常量，
    可直接在 QSS 或 QPalette 中使用。
    """

    # ── 基础色（深蓝灰色调）──
    BASE   = "#1a1d23"  # 主背景：深炭灰
    MANTLE = "#15181e"  # 次级背景：更深
    CRUST  = "#10131a"  # 最深背景

    # ── 表面色（输入框、边框、分隔线）──
    SURFACE0 = "#252a33"
    SURFACE1 = "#333a47"
    SURFACE2 = "#434d5e"

    # ── 覆盖色（禁用文本、占位符）──
    OVERLAY0 = "#5a6577"
    OVERLAY1 = "#6e7b8f"
    OVERLAY2 = "#8392a7"

    # ── 副文本色 ──
    SUBTEXT0 = "#97a5b8"
    SUBTEXT1 = "#afbccd"

    # ── 主文本色 ──
    TEXT = "#c8d2e0"

    # ── 强调色（冷色工业色板）──
    STEEL    = "#6b8aad"   # 钢蓝
    SLATE    = "#7b8fa8"   # 石板蓝
    CYAN     = "#5ba4b5"   # 工业青
    TEAL     = "#4d9e8e"   # 冷水绿
    GREEN    = "#5fa87a"   # 指示灯绿
    RED      = "#c45c5c"   # 警告红
    AMBER    = "#c49a4a"   # 琥珀黄（工业警告）
    ORANGE   = "#b87a48"   # 暗橙
    BLUE     = "#5b8ec9"   # 钢蓝强
    ICE      = "#82b3cc"   # 冰蓝

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

        冷色工业风：低饱和度冷色调，直线棱角感，
        按钮/输入框使用较小圆角，整体沉稳克制。

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
            background-color: {cls.SURFACE1};
            color: {cls.TEXT};
            border: 1px solid {cls.SURFACE2};
            border-radius: {cls.RADIUS_NORMAL}px;
            padding: 5px 14px;
        }}
        QPushButton:hover {{
            background-color: {cls.SURFACE2};
            border-color: {cls.STEEL};
        }}
        QPushButton:pressed {{
            background-color: {cls.SURFACE0};
        }}
        QPushButton:disabled {{
            background-color: {cls.SURFACE0};
            color: {cls.OVERLAY0};
            border-color: {cls.SURFACE0};
        }}

        /* ── 输入框 ── */
        QLineEdit {{
            background-color: {cls.SURFACE0};
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
            background-color: {cls.SURFACE0};
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
            background-color: {cls.SURFACE0};
            color: {cls.TEXT};
            border: 1px solid {cls.SURFACE1};
            border-radius: {cls.RADIUS_SMALL}px;
            selection-background-color: {cls.SURFACE1};
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
            background-color: {cls.SURFACE0};
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
            background-color: {cls.SURFACE0};
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
