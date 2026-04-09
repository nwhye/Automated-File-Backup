# Automated-File-Backup

#### Video Demo:  
https://youtu.be/twehcq9rW2g


#### Description: 
A command-line Python application that automates periodic folder backups. The user configures a source directory, a destination directory, schedule type and time interval at startup. The program then runs continuously, copying the source folder to the destination at the specified interval. 

The motivation for this project was to create a simple, dependency-light backup tool that anyone can run without third-party cloud services or complex configuration files. Everything is controlled through the terminal at startup, and all backup history is stored locally.

#### Files: 
- project.py

  The main application file.
  
- test_project.py

  Contains pytest tests for all four functions.
  
- backup_log.json

  Automatically created on the first backup. Stores a JSON array of log entries, one per backup attempt.
