import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox, BOTH, YES, WORD
import threading
import subprocess
import time
import datetime
import os
import sys

running = True
config = None
content = None


def get_log_filename():
    # 确保 console 文件夹存在
    log_dir = os.path.join(os.path.dirname(__file__), 'console')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join(log_dir, f"log_{timestamp}.txt")


log_filename = get_log_filename()


def run_wechat_bot(log_filename):
    with open(log_filename, 'a', encoding='utf-8') as log_file:
        log_file.write("WeChat Bot Started\n")
        result = subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), 'main.py')], stdout=log_file,
                                stderr=log_file)
        log_file.write(f"WeChat Bot Finished with exit code {result.returncode}\n")


def run_email_sender(log_filename, sleep_time, config, content):
    with open(log_filename, 'a', encoding='utf-8') as log_file:
        while running:
            time.sleep(sleep_time)
            log_file.write(f"Checking emails at {datetime.datetime.now().isoformat()}\n")
            result = subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), 'send_email.py')],
                                    stdout=log_file, stderr=log_file)
            log_file.write(f"Email Sender Finished with exit code {result.returncode}\n")


def start_threads(sleep_time, config, content):
    global running
    running = True
    wechat_thread = threading.Thread(target=run_wechat_bot, args=(log_filename,))
    email_thread = threading.Thread(target=run_email_sender, args=(log_filename, sleep_time, config, content))
    wechat_thread.start()
    email_thread.start()
    messagebox.showinfo("信息", "微信机器人和邮件发送器已启动")


def stop_threads():
    global running
    running = False
    messagebox.showinfo("信息", "微信机器人和邮件发送器已停止")


def periodic_task(text_widget, filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
    except FileNotFoundError:
        content = "已成功初始化请确认邮箱，授权码，时间间隔的配置信息是否正确。\n 请点击启动"

    text_widget.configure(state='normal')
    text_widget.delete(1.0, END)
    text_widget.insert(END, content)
    text_widget.see(END)
    text_widget.configure(state='disabled')
    text_widget.after(1000, periodic_task, text_widget, filepath)


def save_config(email, password, sleep_time):
    config_filename = os.path.join(os.path.dirname(__file__), 'config.properties')
    with open(config_filename, 'w', encoding='utf-8') as config_file:
        config_file.write(f"email={email}\n")
        config_file.write(f"password={password}\n")
        config_file.write(f"sleep={sleep_time}\n")
    messagebox.showinfo("信息", "配置已保存")


def read_config():
    config = {}
    config_filename = os.path.join(os.path.dirname(__file__), 'config.properties')
    if os.path.exists(config_filename):
        with open(config_filename, 'r', encoding='utf-8') as file:
            for line in file:
                key, value = line.strip().split('=')
                config[key] = value
    return config


def read_email_content():
    default_content = '''您好，我们是领先的大学生求职服务领导品牌 求职蛙，我们专注于国内外名校的同学求职服务。为同学提供“求职辅导+机会推荐匹配"的一站式求职解决方案。
    如果您需要实习生，我们有非常多的实习生社群和应届生资源，可以提供高质量并且背景对口的候选人，以及想要和您进行深入的合作包括但不仅限于（求职辅导/简历修改/讲座宣讲/实习和全职内推）我们会给予您高于市场价的求职费用
    我的VX号是 careerfrog01    \n您也可以直接通过此邮件回复'''

    if os.path.exists('email_content.txt'):
        with open('email_content.txt', 'r', encoding='utf-8') as file:
            return file.read()
    else:
        print('邮件内容文件不存在，使用默认邮件内容')
        return default_content


def create_gui():
    global config, content
    config = read_config()
    content = read_email_content()

    root = ttk.Window(themename="darkly")
    root.title("邮件助手")
    root.geometry('600x600')

    frame = ttk.Frame(root, padding=20)
    frame.pack(fill=BOTH, expand=YES)

    email_label = ttk.Label(frame, text="邮箱:")
    email_label.pack(pady=5)
    email_entry = ttk.Entry(frame, width=50)
    email_entry.pack(pady=5)

    password_label = ttk.Label(frame, text="授权码:")
    password_label.pack(pady=5)
    password_entry = ttk.Entry(frame, width=50)
    password_entry.pack(pady=5)

    sleep_label = ttk.Label(frame, text="检查间隔（秒）:")
    sleep_label.pack(pady=5)
    sleep_entry = ttk.Entry(frame, width=50)
    sleep_entry.pack(pady=5)

    email_entry.insert(0, config.get('email', ''))
    password_entry.insert(0, config.get('password', ''))
    sleep_entry.insert(0, config.get('sleep', '60'))

    def save_config_button_action():
        email = email_entry.get()
        password = password_entry.get()
        sleep_time = sleep_entry.get()
        save_config(email, password, sleep_time)

    config_button = ttk.Button(frame, text="保存配置", bootstyle=PRIMARY, command=save_config_button_action)
    config_button.pack(pady=20)

    def start_button_action():
        sleep_time = int(sleep_entry.get())
        start_threads(sleep_time, config, content)

    start_button = ttk.Button(frame, text="启动", bootstyle=SUCCESS, command=start_button_action)
    start_button.pack(pady=20)

    stop_button = ttk.Button(frame, text="停止", bootstyle=DANGER, command=stop_threads)
    stop_button.pack(pady=20)

    text_box = ttk.Text(frame, wrap=WORD, width=70, height=15, state='disabled')
    text_box.pack(pady=10)

    text_box.after(1000, periodic_task, text_box, log_filename)

    root.mainloop()


if __name__ == "__main__":
    create_gui()
