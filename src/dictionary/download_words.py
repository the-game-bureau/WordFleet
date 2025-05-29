#!/usr/bin/env python3
"""
Simple ENABLE Dictionary Downloader

This script automates downloading and maintaining the ENABLE word list.

Behavior:
  1. Downloads the latest ENABLE word list from the specified URL.
  2. Saves/updates a local file at <script_dir>/dictionary/words.txt:
     - Creates the dictionary folder if it doesn't exist.
     - Reads existing words (if any).
     - Compares count of downloaded words to existing file.
     - If counts differ, appends only the new words to words.txt, then alphabetizes the full list.
  3. Logs progress and milestones:
     - Milestones: 1%, 50%, 100% download completion
     - Log output is written to <script_dir>/log/log.txt in pipe-delimited format:
         LEVEL|YYYY-MM-DDTHH:MM:SS|message
  4. Console output displays every download progress percentage and key status messages.

Usage:
  python enable_downloader.py

Requirements:
  - Python 3.x
  - Internet connection to fetch the ENABLE list

File Locations (relative to this script):
  - dictionary/words.txt    # Maintained word list
  - log/log.txt             # Appended log entries
"""

import sys
import urllib.request
from pathlib import Path
import logging
from datetime import datetime

# IMPROVEMENT: Add backup functionality
import shutil

# IMPROVEMENT: Add retry logic for network failures
import time
import urllib.error

# Base directory: folder containing this script
# ANNOTATION: Good practice - using __file__ ensures paths are relative to script location
base_dir = Path(__file__).resolve().parent

# Create and reference dictionary and log folders next to script
dict_dir = base_dir / "dictionary"
dict_dir.mkdir(exist_ok=True)
log_dir = base_dir / "log"
log_dir.mkdir(exist_ok=True)

words_path = dict_dir / "words.txt"
# IMPROVEMENT: Add backup path
backup_path = dict_dir / "words_bu.txt"
log_path = log_dir / "log.txt"

# ANNOTATION: The logging setup is good but could be cleaner
# Set up logging: append to log/log.txt and also output to console
logging.basicConfig(
    filename=str(log_path),
    filemode='a',
    level=logging.INFO,
    # ANNOTATION: Pipe-delimited format is good for parsing, but consider JSON for structured logs
    format='%(levelname)s|%(asctime)s|%(message)s',
    datefmt='%Y-%m-%dT%H:%M:%S'
)
logger = logging.getLogger()
console = logging.StreamHandler(sys.stdout)
console.setLevel(logging.INFO)
console_fmt = logging.Formatter('%(levelname)s|%(asctime)s|%(message)s', datefmt='%Y-%m-%dT%H:%M:%S')
console.setFormatter(console_fmt)
logger.addHandler(console)

# URL for ENABLE word list (raw text)
ENABLE_URL = "https://raw.githubusercontent.com/dolph/dictionary/master/enable1.txt"

# IMPROVEMENT: Add constants for configuration
DOWNLOAD_TIMEOUT = 30  # seconds
RETRY_ATTEMPTS = 3
RETRY_DELAY = 5  # seconds
CHUNK_SIZE = 8192


def create_backup():
    """
    IMPROVEMENT: Create backup of existing word list before modifications.
    Returns True if successful or no backup needed, False if failed.
    """
    if not words_path.exists():
        return True
    
    try:
        shutil.copy2(words_path, backup_path)
        logger.info(f"INFO|Backup created: {backup_path}")
        return True
    except Exception as e:
        logger.error(f"ERROR|Failed to create backup: {e}")
        return False


def download_with_progress(url, retry_attempts=RETRY_ATTEMPTS):
    """
    Downloads content from `url`.
    - Prints every percentage to the console.
    - Logs only 1%, 50%, and 100% milestones.
    
    IMPROVEMENT: Added retry logic and timeout handling
    """
    for attempt in range(retry_attempts):
        try:
            logger.info(f"START|Downloading from {url} (attempt {attempt + 1}/{retry_attempts})")
            
            # IMPROVEMENT: Add timeout to prevent hanging
            response = urllib.request.urlopen(url, timeout=DOWNLOAD_TIMEOUT)
            total = int(response.headers.get('Content-Length', 0))
            downloaded = 0
            # ANNOTATION: Good use of constant for block size
            block_size = CHUNK_SIZE
            data = b''
            milestones = {1, 50, 100}
            hit = set()
            
            # IMPROVEMENT: Add time tracking for download speed
            start_time = time.time()
            last_update = start_time

            while True:
                chunk = response.read(block_size)
                if not chunk:
                    break
                downloaded += len(chunk)
                data += chunk
                
                # IMPROVEMENT: Throttle console updates to reduce overhead
                current_time = time.time()
                if total and (current_time - last_update >= 0.1):  # Update max 10 times per second
                    pct = (downloaded * 100) // total
                    speed = downloaded / (current_time - start_time) / 1024  # KB/s
                    # ANNOTATION: Using carriage return for clean progress display
                    print(f"\rDownloading: {pct}% ({downloaded:,}/{total:,} bytes) - {speed:.1f} KB/s", end='')
                    last_update = current_time
                    
                    # Log only milestone percentages
                    if pct in milestones and pct not in hit:
                        logger.info(f"PROGRESS|{pct}%|{downloaded}/{total} bytes")
                        hit.add(pct)
            
            print()  # New line after progress
            
            # Ensure final 100% milestone is logged
            if 100 not in hit and total:
                logger.info(f"PROGRESS|100%|{downloaded}/{total} bytes")
            
            # IMPROVEMENT: Log download statistics
            elapsed = time.time() - start_time
            logger.info(f"COMPLETE|Download successful|{len(data)} bytes in {elapsed:.1f}s")
            
            return data.decode('utf-8')
            
        except urllib.error.URLError as e:
            logger.error(f"ERROR|Download attempt {attempt + 1} failed: {e}")
            if attempt < retry_attempts - 1:
                logger.info(f"INFO|Retrying in {RETRY_DELAY} seconds...")
                time.sleep(RETRY_DELAY)
            else:
                logger.error("ERROR|All download attempts failed")
                return None
        except Exception as e:
            logger.error(f"ERROR|Unexpected download error: {e}")
            return None


def validate_words(words):
    """
    IMPROVEMENT: Validate downloaded words for data integrity.
    Returns cleaned word list and logs any issues.
    """
    valid_words = []
    invalid_count = 0
    
    for word in words:
        # ANNOTATION: Basic validation - only letters and common word characters
        if word and word.replace("'", "").replace("-", "").isalpha():
            valid_words.append(word.lower())
        else:
            invalid_count += 1
    
    if invalid_count > 0:
        logger.warning(f"WARN|Filtered out {invalid_count} invalid entries")
    
    return valid_words


def restore_backup():
    """
    IMPROVEMENT: Restore the backup file to words.txt
    Returns True if successful, False otherwise.
    """
    if not backup_path.exists():
        logger.error("ERROR|No backup file found to restore")
        return False
    
    try:
        shutil.copy2(backup_path, words_path)
        logger.info(f"INFO|Backup restored from {backup_path}")
        return True
    except Exception as e:
        logger.error(f"ERROR|Failed to restore backup: {e}")
        return False


def update_word_list(existing_words, new_words):
    """
    IMPROVEMENT: Separate function for updating word list with better error handling.
    Returns final word count or -1 on error.
    """
    try:
        # ANNOTATION: Using set operations for efficiency with large word lists
        existing_set = set(existing_words)
        new_set = set(new_words)
        
        # Find truly new words
        additions = new_set - existing_set
        deletions = existing_set - new_set  # IMPROVEMENT: Track removed words
        
        if deletions:
            logger.warning(f"WARN|{len(deletions)} words removed from source: {list(deletions)[:10]}...")
        
        if not additions and not deletions:
            logger.info("INFO|No changes detected in word list")
            return len(existing_words)
        
        # IMPROVEMENT: Check if new word count is suspiciously smaller
        if len(new_set) < len(existing_set) * 0.9:  # More than 10% reduction
            logger.warning(f"WARN|New word list is significantly smaller ({len(new_set)} vs {len(existing_set)})")
            response = input(f"New list has {len(existing_set) - len(new_set)} fewer words. Continue? (y/n): ")
            if response.lower() != 'y':
                logger.info("INFO|User cancelled update due to size reduction")
                return -2  # Special code for user cancellation
        
        # IMPROVEMENT: Write directly to sorted file instead of append-then-sort
        all_words = sorted(new_set)
        
        # Write to temporary file first for safety
        temp_path = words_path.with_suffix('.tmp')
        with open(temp_path, 'w', encoding='utf-8') as f:
            for word in all_words:
                f.write(word + '\n')
        
        # Atomic rename
        temp_path.replace(words_path)
        
        logger.info(f"INFO|Updated dictionary: {len(additions)} added, {len(deletions)} removed")
        logger.info(f"INFO|Final word count: {len(all_words)}")
        
        return len(all_words)
        
    except Exception as e:
        logger.error(f"ERROR|Failed to update word list: {e}")
        return -1


def main():
    """
    IMPROVEMENT: Better error handling and structured workflow
    """
    # Report file locations being used
    logger.info(f"INFO|Dictionary path: {words_path}")
    logger.info(f"INFO|Log path: {log_path}")
    
    # Track original word count for comparison
    original_word_count = 0
    
    # IMPROVEMENT: Create backup before any modifications
    if words_path.exists():
        try:
            with open(words_path, 'r', encoding='utf-8') as f:
                original_word_count = sum(1 for line in f if line.strip())
            logger.info(f"INFO|Original dictionary has {original_word_count} words")
        except Exception as e:
            logger.error(f"ERROR|Failed to count existing words: {e}")
        
        if not create_backup():
            response = input("Failed to create backup. Continue anyway? (y/n): ")
            if response.lower() != 'y':
                logger.info("INFO|User aborted due to backup failure")
                return 1

    # Load existing words and count
    existing = []
    if words_path.exists():
        try:
            with open(words_path, 'r', encoding='utf-8') as f:
                # ANNOTATION: List comprehension efficiently filters empty lines
                existing = [w.strip().lower() for w in f if w.strip()]
            logger.info(f"INFO|Loaded {len(existing)} existing words")
        except Exception as e:
            logger.error(f"ERROR|Failed to read existing dictionary: {e}")
            return 1
    else:
        logger.info("INFO|No existing dictionary found, creating new one")

    # Fetch ENABLE list
    content = download_with_progress(ENABLE_URL)
    if not content:
        logger.error("ERROR|Download failed; attempting to restore backup")
        if backup_path.exists() and restore_backup():
            logger.info("INFO|Successfully restored from backup after download failure")
            return 1
        else:
            logger.error("ERROR|Failed to restore backup")
            return 1
    
    # Parse and validate downloaded words
    downloaded_words = [w.strip() for w in content.splitlines() if w.strip()]
    downloaded_words = validate_words(downloaded_words)
    logger.info(f"INFO|Downloaded {len(downloaded_words)} valid words")

    # IMPROVEMENT: More detailed comparison
    if len(downloaded_words) == len(existing):
        # Still check for content differences even if counts match
        if set(downloaded_words) == set(existing):
            logger.info("INFO|Dictionary is up to date (identical content)")
            return 0
        else:
            logger.info("INFO|Same count but different words detected")

    # Update word list
    result = update_word_list(existing, downloaded_words)
    
    # Handle update results
    if result == -1:
        logger.error("ERROR|Failed to update dictionary, restoring backup")
        if backup_path.exists() and restore_backup():
            logger.info("INFO|Successfully restored from backup after update failure")
        return 1
    elif result == -2:
        logger.info("INFO|Update cancelled by user, restoring backup")
        if backup_path.exists() and restore_backup():
            logger.info("INFO|Successfully restored from backup after user cancellation")
        return 0
    
    # IMPROVEMENT: Final safety check - ensure new file isn't smaller than backup
    if words_path.exists() and backup_path.exists():
        try:
            new_count = sum(1 for line in open(words_path, 'r', encoding='utf-8') if line.strip())
            if new_count < original_word_count:
                logger.warning(f"WARN|New dictionary ({new_count} words) is smaller than original ({original_word_count} words)")
                response = input(f"New dictionary has {original_word_count - new_count} fewer words than original. Keep changes? (y/n): ")
                if response.lower() != 'y':
                    logger.info("INFO|Restoring backup due to size reduction")
                    if restore_backup():
                        logger.info("INFO|Successfully restored original dictionary")
                        return 0
                    else:
                        logger.error("ERROR|Failed to restore backup")
                        return 1
        except Exception as e:
            logger.error(f"ERROR|Failed to verify final file size: {e}")
    
    # IMPROVEMENT: Summary statistics
    logger.info(f"INFO|Script completed successfully")
    print(f"\nDictionary updated: {result:,} total words")
    print(f"Location: {words_path}")
    if backup_path.exists():
        print(f"Backup: {backup_path}")
    
    return 0


if __name__ == '__main__':
    # IMPROVEMENT: Exit with proper code
    sys.exit(main())