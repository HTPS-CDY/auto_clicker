"""
鼠标连点器 (Python)
热键: Shift+C 开始/停止连点, Shift+Q 退出
依赖: pip install keyboard mouse
Windows 上可能需要管理员权限才能正常捕获全局热键。
"""

import keyboard
import mouse
import threading
import time
import sys

# ========= 配置 =========
CLICK_INTERVAL = 0.05  # 点击间隔（秒），0.05 = 20次/秒，可自行修改
# ========================

clicking = False
exit_flag = False
click_thread = None

def click_loop():
    """连点循环，在子线程中运行"""
    while not exit_flag:
        if clicking:
            mouse.click('left')
            time.sleep(CLICK_INTERVAL)
        else:
            time.sleep(0.01)  # 未点击时短暂休眠，避免忙等待

def toggle_clicking():
    """切换连点状态"""
    global clicking
    clicking = not clicking
    status = "开始" if clicking else "停止"
    print(f"连点已{status}")
    try:
        # 发出提示音（800Hz 和 400Hz）
        import winsound
        winsound.Beep(800 if clicking else 400, 100)
    except Exception:
        pass

def quit_program():
    """安全退出"""
    global exit_flag
    print("正在退出...")
    exit_flag = True
    # 移除所有热键，避免退出时残留钩子
    keyboard.unhook_all()
    sys.exit(0)

def main():
    global click_thread

    # 启动连点线程
    click_thread = threading.Thread(target=click_loop, daemon=True)
    click_thread.start()

    # 注册热键
    keyboard.add_hotkey('shift+c', toggle_clicking)
    keyboard.add_hotkey('shift+q', quit_program)

    print("鼠标连点器已启动")
    print("按下 Shift+C 开始/停止连点 | 按下 Shift+Q 退出")
    print("点击间隔: {}秒 ({} 次/秒)".format(CLICK_INTERVAL, 1/CLICK_INTERVAL))

    # 进入等待（阻塞主线程，直到键盘钩子终止）
    try:
        keyboard.wait()
    except KeyboardInterrupt:
        quit_program()

if __name__ == "__main__":
    main()