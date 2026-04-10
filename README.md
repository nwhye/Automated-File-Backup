# Automated-File-Backup

#### Video Demo:  
https://youtu.be/twehcq9rW2g


#### Description: 
A command-line Python application that automates periodic folder backups. The user configures a source directory, a destination directory, schedule type and time interval at startup. The program then runs continuously, copying the source folder to the destination at the specified interval. 

The motivation for this project was to create a simple, dependency-light backup tool that anyone can run without third-party cloud services or complex configuration files. Everything is controlled through the terminal at startup, and all backup history is stored locally.

#### Features:
- Backs up any folder to a chosen destination
- Supports two schedule types (every N seconds, or once daily at a set time)
- Organizes backups by date
- Logs every backup attempt to a backup_log.json file
- Validates user input at startup
- Runs an immediate backup on startup before the schedule kicks in
- Exits on Ctrl+C

#### Files: 
- project.py

  The main application file.
  
- test_project.py

  Contains pytest tests for all four functions. The tests use tmp_path to avoid touching real files on disk and monkeypatch to redirect DB_FILE and simulate user input without actual terminal interaction.
  
- backup_log.json

  Automatically created on the first backup. Stores a JSON array of log entries, one per backup attempt.


#### Functions:
- write_config() - Handles all startup user input. Prompts for the source directory, destination directory, schedule type and interval or time. Validates every input before proceeding. After that registers the backup job with the scheduler and returns the source and destination paths to main().
  
- write_json(source, dest, status) — The logging function. Every time a backup completes or fails, this function appends a new entry to backup_log.json. Each entry stores a timestamp, the source path, the destination path and a status of either Success or Failed. If the log file does not yet exist, it creates it automatically.
  
- copy_folder_to_directory(source, dest) — Performs the actual file copy using Python's built-in shutil.copytree. It organizes backups by date, creating a subdirectory named after today's date inside the destination folder. If a backup for today already exists, it removes it first and replaces it with a fresh copy.
  
- perform_backup(source_dir, destination_dir) — prints a timestamped status message before and after the copy. This is the function that the scheduler calls on each interval.


#### Design Choices:
- JSON. Each entry is a proper data structure, easily readable by other scripts, sortable by field and extendable with new fields in the future without breaking old entries.
- Validating inputs at startup. The program exits immediately with a clear error message rather than failing hours later when the first scheduled backup runs and finds a missing folder.
- Running one immediate backup on startup.  If a user sets a daily schedule and starts the script in the morning, they could wait until the next day for the first backup. Running one backup immediately guarantees the source is protected from the moment the script starts.
- shutil.copytree. Writing a manual recursive copy loop would introduce more surface area for bugs with no practical benefit, so I chose python's built-in shutil library.
