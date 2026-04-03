import sys
import datetime
import os
import schedule

DB_FILE = "backup_log.txt"


def write_txt():
    ...


def copy_folder_to_directory(source, dest):
    today = datetime.date.today()
    dest_dir = os.path.join(dest, str(today))


def perform_backup(source_dir, destination_dir):
    print("Performing backup...")
    copy_folder_to_directory(source_dir, destination_dir)
    print("Backup routine finished")


def main():
    source_dir = input("Enter directory path for backup: ").strip()
    destination_dir = input("Enter destination directory path for backup: ").strip()
    schedule_pick = input("Choose schedule type for backup. Every (seconds/day): ").strip().lower()
    if schedule_pick == 'seconds':
        time_pick = input("Enter interval in seconds: ").strip()
        try:
            interval = int(time_pick)
        except ValueError:
            sys.exit("Invalid input: seconds must be a whole number.")
        schedule.every(interval).seconds.do(perform_backup, source_dir, destination_dir)

    elif schedule_pick == 'day':
        time_pick = input("Enter time for daily backup (HH:MM): ").strip()
        schedule.every(time_pick).day.do(perform_backup, source_dir, destination_dir)
    else:
        sys.exit("Invalid schedule type. Choose 'seconds' or 'day'.")


if __name__ == "__main__":
    main()