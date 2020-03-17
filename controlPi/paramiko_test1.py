import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("IP",22,"name", "password")  # 網路連線設定
stdin, stdout, stderr = ssh.exec_command("python /home/pi/Desktop/test.py hahahaha")  # 呼叫執行檔並傳送參數
print(stdout.readlines()[0])  # 回傳產出結果
ssh.close()