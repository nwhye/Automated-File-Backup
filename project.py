import sys
import datetime
import os
import schedule
import shutil
import time
import re
import json


DB_FILE = "backup_log.json"


def write_config():

    """Log user configuration for backup."""

    source_dir = input("Enter directory path for backup: ").strip()
    if not os.path.isdir(source_dir):
        sys.exit(f"Source directory not found: {source_dir}")

    destination_dir = input("Enter destination directory path for backup: ").strip()
    if not os.path.isdir(destination_dir):
        sys.exit(f"Destination directory not found: {destination_dir}")

    schedule_pick = input("Choose schedule type for backup. Every (seconds/day): ").strip().lower()
    if schedule_pick == 'seconds':
        time_pick = input("Enter interval in seconds: ").strip()
        try:
            interval = int(time_pick)
        except ValueError:
            sys.exit("Invalid input: seconds must be a whole number.")
        schedule.every(interval).seconds.do(perform_backup, source_dir, destination_dir)
        print(f"Scheduler set: backup every {interval} second(s). Press Ctrl+C to stop.\n")

    elif schedule_pick == 'day':
        time_pick = input("Enter time for daily backup (HH:MM): ").strip()
        if not re.match(r"^\d{2}:\d{2}$", time_pick):
            sys.exit("Invalid time format. Use HH:MM (e.g. 09:00).")
        schedule.every().day.at(time_pick).do(perform_backup, source_dir, destination_dir)
        print(f"Scheduler set: daily backup at {time_pick}. Press Ctrl+C to stop.\n")

    else:
        sys.exit("Invalid schedule type. Choose 'seconds' or 'day'.")

    return source_dir, destination_dir


def write_json(source, dest, status):

    """Log a backup entry to the JSON file."""

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    entry = {
        "timestamp": timestamp,
        "source": source,
        "destination": dest,
        "status": status
    }
    if os.path.isfile(DB_FILE):
        with open(DB_FILE, "r") as db:
            data = json.load(db)
    else:
        data = []

    data.append(entry)

    with open(DB_FILE, "w") as db:
        json.dump(data, db, indent=4)


def copy_folder_to_directory(source, dest):

    """Copy source folder into dest/YYYY-MM-DD/."""

    today = datetime.date.today()
    dest_dir = os.path.join(dest, str(today))

    try:
        if os.path.exists(dest_dir):
            shutil.rmtree(dest_dir)

        shutil.copytree(source, dest_dir)

        write_json(source, dest_dir, "Success")
        print(f"Copied '{source}' to '{dest_dir}'")

    except Exception as error:
        write_json(source, dest, "Failed")
        print(f"Backup failed: {error}")


def perform_backup(source_dir, destination_dir):

    """Run a single backup cycle."""

    print(f"\n[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Performing backup...")
    copy_folder_to_directory(source_dir, destination_dir)
    print("Backup routine finished")


def main():
    source_dir, destination_dir = write_config()
    perform_backup(source_dir, destination_dir)

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nBackup scheduler stopped.")


if __name__ == "__main__":
    main()