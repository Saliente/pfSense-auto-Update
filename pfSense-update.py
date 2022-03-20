import subprocess
import paramiko
import csv
import time

# SSH user and password
username = 'root'
password = 'pfsense'

# Enable paramiko to connect on everything
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Open costumer list with Name, VPN and IP of Firewall
with open('costumer.csv', 'r') as costumer:
    costumer = csv.reader(costumer)

    # Jump first line of CSV
    next(costumer)

    # Start process
    for line in costumer:
        # If no IP, jump it
        if line[3] == '----':
            continue
        else:
            # Connect to VPN
            subprocess.Popen(['openvpn', '--config', "VPN/{0}".format(line[2]), '--auth-user-pass', 'auth.pass'])
            time.sleep(30)
            print("="*50, "\n", "Connected at", line[1], "\n", "="*50)

            # Connect via SSH on FW
            ssh.connect(hostname=line[3], username=username, password=password)
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('pfSense-upgrade -y')
            ssh_stdin.close()
            stdout = ssh_stdout.read().decode()
            print(stdout)

            # Desconnect to SSH and VPN
            ssh.close()
            subprocess.Popen(['killall', 'openvpn'])

            # Check if is an error
            stderr = ssh_stderr.read().decode()
            if stderr:
                print("=" * 50, "\n", stderr, "\n", "=" * 50)
                break
            else:
                print("="*20, "SUCCESS GO TO NEXT", "="*20)


print("="*15, "If no error, is every finished", "="*15)
