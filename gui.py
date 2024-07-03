import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox, BOTH, YES, WORD
import threading
import subprocess
import time
import datetime
import os

running = True

def get_log_filename():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"log_{timestamp}.txt"

log_filename = get_log_filename()

def run_wechat_bot(log_filename):
    with open(log_filename, 'a', encoding='utf-8') as log_file:
        log_file.write("WeChat Bot Started\n")
        result = subprocess.run(['python', 'main.py'], stdout=log_file, stderr=log_file)
        log_file.write(f"WeChat Bot Finished with exit code {result.returncode}\n")

def run_email_sender(log_filename):
    with open(log_filename, 'a', encoding='utf-8') as log_file:
        while running:
            time.sleep(60)
            log_file.write(f"Checking emails at {datetime.datetime.now().isoformat()}\n")
            result = subprocess.run(['python', 'send_email.py'], stdout=log_file, stderr=log_file)
            log_file.write(f"Email Sender Finished with exit code {result.returncode}\n")

def start_threads():
    global running
    running = True
    wechat_thread = threading.Thread(target=run_wechat_bot, args=(log_filename,))
    email_thread = threading.Thread(target=run_email_sender, args=(log_filename,))
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
        content = "文件未找到。"

    text_widget.configure(state='normal')
    text_widget.delete(1.0, END)
    text_widget.insert(END, content)
    text_widget.see(END)
    text_widget.configure(state='disabled')
    text_widget.after(1000, periodic_task, text_widget, filepath)

def save_config(email, password):
    config_filename = 'config.properties'
    with open(config_filename, 'w', encoding='utf-8') as config_file:
        config_file.write(f"email={email}\n")
        config_file.write(f"password={password}\n")
    messagebox.showinfo("信息", "配置已保存")

def read_config():
    config = {}

    if os.path.exists('config.properties'):
        with open('config.properties', 'r', encoding='utf-8') as file:

            for line in file:
                key, value = line.strip().split('=')
                config[key] = value
    return config

def create_gui():
    root = ttk.Window(themename="darkly")
    root.title("MyApp GUI")
    root.geometry('600x600')

    frame = ttk.Frame(root, padding=20)
    frame.pack(fill=BOTH, expand=YES)

    email_label = ttk.Label(frame, text="邮箱:")
    email_label.pack(pady=5)
    email_entry = ttk.Entry(frame, width=50)
    email_entry.pack(pady=5)

    password_label = ttk.Label(frame, text="授权码:")
    password_label.pack(pady=5)
    password_entry = ttk.Entry(frame, width=50, show='*')
    password_entry.pack(pady=5)

    config = read_config()
    email_entry.insert(0, config.get('email', ''))
    password_entry.insert(0, config.get('password', ''))

    def save_config_button_action():
        email = email_entry.get()
        password = password_entry.get()
        save_config(email, password)

    config_button = ttk.Button(frame, text="保存配置", bootstyle=PRIMARY, command=save_config_button_action)
    config_button.pack(pady=20)

    start_button = ttk.Button(frame, text="启动", bootstyle=SUCCESS, command=start_threads)
    start_button.pack(pady=20)

    stop_button = ttk.Button(frame, text="停止", bootstyle=DANGER, command=stop_threads)
    stop_button.pack(pady=20)

    text_box = ttk.Text(frame, wrap=WORD, width=70, height=15, state='disabled')
    text_box.pack(pady=10)

    text_box.after(1000, periodic_task, text_box, log_filename)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
