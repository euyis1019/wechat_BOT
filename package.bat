taskkill /f /im wechat-bot.exe
taskkill /f /im wechat-bot-core.exe
taskkill /f /im send-mail.exe

pyinstaller -c -F -y -n wechat-bot gui.py
pyinstaller -c -F -y -n send-mail send_email.py
pyinstaller -c -F -y -n wechat-bot-core main.py
