# -*- coding: utf-8 -*-
"""
弹窗爱心 → 逐个消失 → 满屏弹窗雨
运行：python pop_love.py
依赖：仅 Python 内置 tkinter
"""

import tkinter as tk
import random
import math

# ====== 可自定义 ======
WORDS = [
    "我想你了", "天冷了，多穿衣服", "保持微笑呀", "别熬夜",
    "记得吃水果", "每天都要元气满满", "愿所有烦恼都消失", "好好爱自己",
    "待下一次见面", "梦想成真", "多喝水哦~", "心情棒棒",
    "你今天真好看", "我在呢", "要开心呀", "喜欢你",
]

BG_COLORS = [
    "#FFF9C4", "#FFE0B2", "#FFCCBC", "#F8BBD0",
    "#E1BEE7", "#D1C4E9", "#BBDEFB", "#B3E5FC",
    "#B2DFDB", "#C8E6C9", "#FFFFFF", "#FFECB3",
]

HEART_DOTS = 110       # 爱心上摆多少个弹窗
HEART_BUILD_GAP = 30   # 摆爱心时每个弹窗的间隔(ms)
HEART_BEFORE_VANISH = 600   # 爱心摆好后停留多久再开始消失(ms)
VANISH_GAP = 25        # 逐个消失的间隔(ms)
RAIN_INTERVAL = 120    # 进入弹窗雨后每隔多久弹一个（越小越快铺满）
MAX_RAIN = 200         # 弹窗雨最多同时存在（铺满屏）
RAIN_HOLD_SEC = 5      # 铺满后停留几秒再弹出结束按钮
FONT = ("微软雅黑", 11)


class Popup:
    """一个真实小弹窗"""
    def __init__(self, root, x, y, word=None, bg=None):
        self.root = root
        self.top = tk.Toplevel(root)
        self.top.overrideredirect(False)
        self.top.attributes("-topmost", True)

        self.w = random.randint(110, 160)
        self.h = random.randint(55, 80)
        self.x = x - self.w / 2
        self.y = y - self.h / 2
        self.top.geometry(f"{int(self.w)}x{int(self.h)}+{int(self.x)}+{int(self.y)}")

        bg = bg or random.choice(BG_COLORS)
        self.top.configure(bg=bg)
        word = word or random.choice(WORDS)
        tk.Label(self.top, text=word, font=FONT, bg=bg, fg="#333",
                 padx=8, pady=12).pack(expand=True, fill=tk.BOTH)
        self.top.title(random.choice(["💌", "小提醒", "有句话想对你说"]))

        # 花瓣凋落参数（触发时才启用）
        self.falling = False
        self.vy = 0
        self.phase = 0
        self.sway_amp = 0
        self.sway_freq = 0

    def start_falling(self):
        """进入花瓣凋落状态"""
        self.falling = True
        self.vy = random.uniform(2.0, 5.0)
        self.phase = random.uniform(0, 2 * math.pi)
        self.sway_amp = random.uniform(0.5, 2.5)
        self.sway_freq = random.uniform(0.08, 0.2)

    def step_fall(self, sh):
        """每帧更新凋落位置和大小；返回 False 表示该弹窗已消失"""
        if not self.falling:
            return True
        self.y += self.vy
        self.phase += self.sway_freq
        self.x += math.sin(self.phase) * self.sway_amp
        # 逐渐缩小（像花瓣变小）
        self.w *= 0.97
        self.h *= 0.97
        try:
            self.top.geometry(
                f"{max(int(self.w), 8)}x{max(int(self.h), 8)}"
                f"+{int(self.x)}+{int(self.y)}"
            )
        except Exception:
            return False
        # 飘出屏幕底部或缩得太小就消失
        if self.y > sh + 50 or self.w < 12:
            self.destroy()
            return False
        return True

    def destroy(self):
        try:
            self.top.destroy()
        except Exception:
            pass


def heart_points(n, sw, sh):
    """生成爱心参数方程上的 n 个点，返回 (x,y) 列表，坐标已映射到屏幕"""
    pts = []
    cx, cy = sw / 2, sh / 2          # 屏幕中心
    scale = min(sw, sh) / 45         # 缩放系数
    for i in range(n):
        t = 2 * math.pi * i / n
        # 经典爱心参数方程
        x = 16 * math.sin(t) ** 3
        y = 13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t)
        # y 轴翻转（屏幕 y 向下为正），并居中
        px = cx + x * scale
        py = cy - y * scale
        pts.append((px, py))
    return pts


def main():
    root = tk.Tk()
    root.withdraw()
    sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()

    heart_pops = []   # 摆成爱心的弹窗
    rain_pops = []    # 弹窗雨的弹窗

    state = {"phase": "build"}   # build -> hold -> vanish -> rain

    # ---- 阶段1：逐个摆成爱心 ----
    pts = heart_points(HEART_DOTS, sw, sh)
    build_idx = [0]

    def step_build():
        if build_idx[0] >= len(pts):
            state["phase"] = "hold"
            root.after(HEART_BEFORE_VANISH, step_vanish)
            return
        x, y = pts[build_idx[0]]
        heart_pops.append(Popup(root, x, y))
        build_idx[0] += 1
        root.after(HEART_BUILD_GAP, step_build)

    # ---- 阶段2：逐个消失 ----
    vanish_idx = [0]

    def step_vanish():
        if vanish_idx[0] >= len(heart_pops):
            state["phase"] = "rain"
            # 最后一个弹窗消失的同一瞬间，立刻进入弹窗雨
            start_rain()
            return
        # 从外向内消失：把列表打乱顺序，看起来更自然
        if vanish_idx[0] == 0:
            random.shuffle(heart_pops)
        heart_pops[vanish_idx[0]].destroy()
        vanish_idx[0] += 1
        root.after(VANISH_GAP, step_vanish)

    # ---- 阶段3：满屏随机弹窗雨 ----
    rain_going = {"on": True}

    def step_rain():
        if not rain_going["on"]:
            return
        rain_pops[:] = [p for p in rain_pops if p.top.winfo_exists()]
        if len(rain_pops) < MAX_RAIN:
            x = random.randint(0, sw - 150)
            y = random.randint(0, sh - 80)
            rain_pops.append(Popup(root, x + 75, y + 40))
        root.after(RAIN_INTERVAL, step_rain)

    def start_rain():
        # 先一口气弹一批，瞬间铺满大半屏，再持续补
        for _ in range(40):
            x = random.randint(0, sw - 150)
            y = random.randint(0, sh - 80)
            rain_pops.append(Popup(root, x + 75, y + 40))
        root.after(RAIN_INTERVAL, step_rain)
        # 铺满后停留指定秒数，再弹出结束按钮
        root.after(RAIN_HOLD_SEC * 1000, show_finish_button)

    # ---- 阶段4：居中弹出"点我结束"按钮 ----
    def show_finish_button():
        rain_going["on"] = False   # 停止新增弹窗
        rain_pops[:] = [p for p in rain_pops if p.top.winfo_exists()]

        btn_win = tk.Toplevel(root)
        btn_win.overrideredirect(True)
        btn_win.attributes("-topmost", True)
        w, h = 220, 120
        btn_win.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")
        btn_win.configure(bg="#FF4081")

        tk.Label(btn_win, text="💗", font=("Arial", 28),
                 bg="#FF4081", fg="white").pack(pady=(12, 0))

        def on_click():
            btn_win.destroy()
            scatter_petals()

        tk.Button(btn_win, text="点我结束 ❤", font=("微软雅黑", 14, "bold"),
                  bg="white", fg="#FF4081", activebackground="#FFE0EC",
                  relief=tk.FLAT, width=12, command=on_click).pack(pady=10)

    # ---- 阶段5：所有弹窗碎成花瓣凋落 ----
    def scatter_petals():
        for p in rain_pops:
            if p.top.winfo_exists():
                p.start_falling()

        def fall_tick():
            alive = []
            for p in rain_pops:
                if p.top.winfo_exists() and p.step_fall(sh):
                    alive.append(p)
            rain_pops[:] = alive
            if rain_pops:
                root.after(30, fall_tick)
            else:
                # 全部凋落完，结束程序
                root.destroy()

        fall_tick()

    # 退出按钮（小，放右上角）
    quit_btn = tk.Toplevel(root)
    quit_btn.overrideredirect(True)
    quit_btn.attributes("-topmost", True)
    quit_btn.geometry(f"80x25+{sw-90}+10")
    tk.Button(quit_btn, text="退出 (ESC)", command=root.destroy,
              font=("微软雅黑", 9), bg="#333", fg="white").pack(expand=True, fill=tk.BOTH)
    root.bind("<Escape>", lambda e: root.destroy())

    # 开跑
    root.after(200, step_build)
    root.mainloop()


if __name__ == "__main__":
    main()
