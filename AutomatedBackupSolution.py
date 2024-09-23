import os
import paramiko
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(filename='backup_report.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def sftp_backup(local_directory, remote_directory, hostname, username, password):
    try:
        # Connect to the remote server
        transport = paramiko.Transport((hostname, 22))
        transport.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        
        # Ensure remote directory exists
        try:
            sftp.listdir(remote_directory)
        except IOError:
            sftp.mkdir(remote_directory)

        # Backup files
        for root, dirs, files in os.walk(local_directory):
            for file in files:
                local_path = os.path.join(root, file)
                # Create a corresponding remote path
                remote_path = os.path.join(remote_directory, os.path.relpath(local_path, local_directory))
                remote_dir = os.path.dirname(remote_path)
                
                # Ensure the remote directory exists
                try:
                    sftp.listdir(remote_dir)
                except IOError:
                    sftp.mkdir(remote_dir)

                # Upload the file
                sftp.put(local_path, remote_path)
                logging.info(f"Successfully backed up {local_path} to {remote_path}")
        
        sftp.close()
        transport.close()
        logging.info("Backup completed successfully.")
    
    except Exception as e:
        logging.error(f"Backup failed: {e}")

if __name__ == "__main__":
    # User-defined variables
    local_directory = '/path/to/local/directory'  # Specify your local directory
    remote_directory = '/path/to/remote/directory'  # Specify your remote directory
    hostname = 'your.remote.server.com'  # Remote server hostname
    username = 'your_username'  # Remote server username
    password = 'your_password'  # Remote server password
    
    # Run the backup
    sftp_backup(local_directory, remote_directory, hostname, username, password)

