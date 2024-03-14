#!/bin/bash

# Define backup and log directory if it doesn't exist
BACKUP_DIR=~/backups
LOG_DIR=~/logs

# Create the backup and log directory
mkdir -p "$BACKUP_DIR"
mkdir -p "$LOG_DIR"

# NUmbers of backup to keep
NUM_BACKUPS=3

# Define log file with the current date
LOG_FILE="$LOG_DIR/ROTATE_BACKUPS$(date +'%Y-%m-%d').log"

# Function to log messages
log_message() {
  echo "$(date +'%Y-%m-%d %H:%M:%S') $1" >> "$LOG_FILE"
}

# Find all backup files in the directory and count how many
BACKUP_FILES=$(find "$BACKUP_DIR" -name "mhs_geographic_backup_*.sql")
NUM_FILES=$(echo "$BACKUP_FILES" | wc -l)

# Log the number of backup files found
log_message "Number of backup files found: $NUM_FILES"

# Check if there are more than NUM_BACKUPS files
if [ $NUM_FILES -gt $NUM_BACKUPS ]; then
  # Sort files by modification time (oldest first)
  sorted_files=$(echo "$BACKUP_FILES" | sort)

  # Get the files to delete (oldest ones)
  FILES_TO_DELETE=$(echo "$sorted_files" | head -n $(($NUM_FILES - $NUM_BACKUPS)))

  # Delete the oldest backups
  echo "$FILES_TO_DELETE" | xargs rm -f
  echo "Deleted oldest backups:"
  echo "$FILES_TO_DELETE" | while read -r file; do
    log_message "Deleted: $file"
  done
fi

# Optional: Log no cleanup needed
if [ $NUM_FILES -le $NUM_BACKUPS ]; then
  log_message "No backups to delete. Currently keeping $NUM_BACKUPS backups."
fi
