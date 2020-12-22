
"""Script to upload files in a folder via ftp."""

import argparse
import ftplib
import os


def get_upload_list(base_path):
    files = []

    for name in os.listdir(base_path):
        files.append((name, os.path.join(base_path, name)))

    return files


def main():
    """Run the main function."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-fs', '--ftp_server', help='The ftp server address')
    parser.add_argument('-fu', '--ftp_user', help='The ftp username')
    parser.add_argument('-fp', '--ftp_pass', help='The ftp password')
    parser.add_argument('-fd', '--ftp_dir', help='The ftp remote directory')
    parser.add_argument('-ud', '--upload_dir', help='The upload directory')
    args = parser.parse_args()

    print('FTP SERVER', args.ftp_server)
    print('FTP USERNAME', args.ftp_user)
    print('FTP DIR', args.ftp_dir)
    print('UPLOAD DIR', args.upload_dir)

    # Get base files
    file_list = get_upload_list(args.upload_dir)

    with ftplib.FTP(args.ftp_server, args.ftp_user, args.ftp_pass) as session:
        print('Server Path', session.pwd())
        session.cwd(args.ftp_dir)
        print('New Server Path', session.pwd())

        for file_name, file_path in file_list:
            print(F'Upload "{file_name}" from "{file_path}"')
            with open(file_path, 'rb') as file_ptr:
                print(F'Upload File as "{file_name}"')
                session.storbinary(F'STOR {file_name}', file_ptr)
        print('### TRANSFER COMPLETE ###')


if __name__ == '__main__':
    main()
