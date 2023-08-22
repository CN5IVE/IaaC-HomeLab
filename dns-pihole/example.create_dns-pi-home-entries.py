import paramiko

def read_remote_file(ssh_client, remote_path):
    with ssh_client.open_sftp() as sftp:
        with sftp.open(remote_path, 'r') as remote_file:
            return remote_file.read()

def append_to_remote_file(ssh_client, remote_path, content):
    with ssh_client.open_sftp() as sftp:
        with sftp.open(remote_path, 'a') as remote_file:
            remote_file.write(content)

def main():
    host = '192.168.10.3'
    port = 22
    username = 'root'
    password = 'xxxxxx' # password to pi-hole server
    
    remote_path = '/etc/pihole/custom.list'
    local_file_path = 'path-to-files/dns-pihole/dns_entries.txt'
    
    with paramiko.SSHClient() as ssh_client:
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(host, port, username, password)
        
        with open(local_file_path, 'r') as local_file:
            local_entries = local_file.read().splitlines()
            
        remote_content = read_remote_file(ssh_client, remote_path).decode('utf-8')
        remote_entries = remote_content.splitlines()
        
        new_entries = set(local_entries) - set(remote_entries)
        
        if new_entries:
            append_to_remote_file(ssh_client, remote_path, '\n'.join(new_entries).encode('utf-8'))
            print(f"Appended new contents to {remote_path}.")
            
            # Reboot the remote server
            stdin, stdout, stderr = ssh_client.exec_command("sudo reboot")
            reboot_output = stdout.read().decode('utf-8')
            print("Reboot command executed:", reboot_output)
        else:
            print("No new contents to append.")

if __name__ == "__main__":
    main()
