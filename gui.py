import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
import threading
import subprocess
import time
import sys

# 定义重定向类
class StdoutRedirector:
    def __init__(self, text_widget,stdoutOri):
        self.text_widget = text_widget
        self.original_stdout = stdoutOri

    def write(self, text):
        self.text_widget.insert(ttk.END, text)
        self.text_widget.see(ttk.END)

    def flush(self):
        pass

# 定义两个线程的目标函数
def run_wechat_bot():
    subprocess.run(['python', 'main.py'])

def run_email_sender():
    while True:
        time.sleep(60)  # 每隔一小时检查一次 emails.txt
        subprocess.run(['python', 'send_email.py'])

# 启动线程的函数
def start_threads():
    wechat_thread = threading.Thread(target=run_wechat_bot)
    email_thread = threading.Thread(target=run_email_sender)
    wechat_thread.start()
    email_thread.start()
    messagebox.showinfo("信息", "微信机器人和邮件发送器已启动")

# 创建并启动GUI
def create_gui():
    root = ttk.Window(themename="darkly")
    root.title("MyApp GUI")
    root.geometry('600x400')  # 设置窗口大小为600x400

    frame = ttk.Frame(root, padding=20)
    frame.pack(fill=BOTH, expand=YES)

    start_button = ttk.Button(frame, text="启动", bootstyle=SUCCESS, command=start_threads)
    start_button.pack(pady=20)

    # 创建文本框
    text_box = ttk.Text(frame, wrap=ttk.WORD, width=70, height=15)
    text_box.pack(pady=10)

    # 重定向标准输出到文本框
    sys.stdout = StdoutRedirector(text_box,sys.stdout)

    root.mainloop()

    # 恢复原始标准输出
    sys.stdout = sys.__stdout__

if __name__ == "__main__":
    create_gui()
