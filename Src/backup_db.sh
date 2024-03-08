#!/bin/bash

# Define backup directory (modify as needed)
BACKUP_DIR=~/backups

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# Get today's date in YYYY-MM-DD format
TODAY=$(date +%Y-%m-%d)

# Define backup filename with date
BACKUP_FILE="$BACKUP_DIR/mhs_geographic_backup_$TODAY.sql"

# Define log directory
LOG_DIR=~/logs

# Create log directory if it doesn't exist
mkdir -p "$LOG_DIR"

# Define log filename with date
LOG_FILE="$LOG_DIR/mhs_geographic_backup_$TODAY.log"

# Perform the backup and log to file
{
  pg_dump -U postgres mhs_geographic > "$BACKUP_FILE" &&
  echo "$(date +'%Y-%m-%d %H:%M:%S') Database backup to $BACKUP_FILE completed."
} >> "$LOG_FILE" 2>&1
