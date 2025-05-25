#!/usr/bin/env python3
"""
Enhanced Dictionary Downloader for GCIDE (GNU Collaborative International Dictionary of English)
Downloads and processes the dictionary XML from ibiblio.org to ../dictionary/dictionary.xml

CLAUDE.AI RECREATION PROMPT:
===========================
Create a Python script that downloads the GCIDE dictionary from https://www.ibiblio.org/webster/gcide_xml-0.53.zip
and processes it into a clean XML dictionary file with the following specifications:

CORE FUNCTIONALITY:
- Download ZIP with progress indicator using urllib
- Extract and parse gcide_a.xml through gcide_z.xml files
- Extract <hw> (headword) and <def> (definition) from <p> tags using regex
- Clean HTML entities (&mdash;, &nbsp;, &amp;, Greek letters, accented chars, etc.)
- Filter headwords: letters/hyphens/apostrophes only, length > 1, meaningful definitions > 10 chars
- Remove duplicates (case-insensitive) and sort alphabetically
- Output format: <dictionary><entry><word></word><definition></definition></entry></dictionary>
- Single-line entries for compact format

REQUIREMENTS:
- Store in dictionary/dictionary.xml relative to script location (GitHub Actions compatible)
- Log all output to log/log.txt relative to script location
- Create automatic backup (dictionary_bu.xml) of existing files
- Handle errors gracefully, continue processing if individual files fail
- Clean up temporary files after processing
- Show progress every 5000 entries, log download progress at 10% intervals (once each)
- Use pathlib.Path for cross-platform file handling
- Proper XML escaping for output (&, <, > characters)

STRUCTURE:
- create_directory_structure(): Setup dictionary/ folder relative to script
- setup_logging(): Create log/ folder and log file relative to script
- download_with_progress(): Download with percentage indicator
- extract_zip_file(): Extract and find XML directory
- combine_xml_files(): Main processing logic with entity replacement and filtering
- Comprehensive error handling and user feedback throughout

The script should work in any environment including CI/CD systems like GitHub Actions.
===========================
"""

import os
import sys
import urllib.request
import urllib.error
import shutil
import re
import zipfile
from pathlib import Path
from datetime import datetime

# GCIDE download URL
GCIDE_URL = "https://www.ibiblio.org/webster/gcide_xml-0.53.zip"

# Global log file handle
log_file = None

def log_print(message, end='\n'):
    """Print to both console and log file."""
    print(message, end=end)
    if log_file:
        log_file.write(message + end)
        log_file.flush()

def setup_logging():
    """Initialize logging to log/log.txt."""
    global log_file
    
    # Create log directory
    log_dir = Path("log")
    log_dir.mkdir(exist_ok=True)
    
    # Open log file
    log_file_path = log_dir / "log.txt"
    log_file = open(log_file_path, 'w', encoding='utf-8')
    
    # Write header with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_print(f"GCIDE Dictionary Download Log - {timestamp}")
    log_print("=" * 50)
    
    return log_file_path

def close_logging():
    """Close log file."""
    global log_file
    if log_file:
        log_file.close()

# HTML/XML entity replacements for clean text output
ENTITY_REPLACEMENTS = {
    '&mdash;': '—', '&nbsp;': ' ', '&amp;': '&', '&lt;': '<', '&gt;': '>',
    '&quot;': '"', '&apos;': "'", '&deg;': '°', '&pound;': '£', '&sect;': '§',
    '&para;': '¶', '&middot;': '·', '&times;': '×', '&divide;': '÷',
    '&prime;': '′', '&Prime;': '″', '&radic;': '√', '&int;': '∫',
    # Greek letters
    '&Alpha;': 'Α', '&Beta;': 'Β', '&Gamma;': 'Γ', '&Delta;': 'Δ',
    '&alpha;': 'α', '&beta;': 'β', '&gamma;': 'γ', '&delta;': 'δ',
    # Accented characters
    '&AElig;': 'Æ', '&aelig;': 'æ', '&OElig;': 'Œ', '&oelig;': 'œ',
    '&agrave;': 'à', '&aacute;': 'á', '&acirc;': 'â', '&atilde;': 'ã',
    '&auml;': 'ä', '&aring;': 'å', '&ccedil;': 'ç', '&egrave;': 'è',
    '&eacute;': 'é', '&ecirc;': 'ê', '&euml;': 'ë', '&igrave;': 'ì',
    '&iacute;': 'í', '&icirc;': 'î', '&iuml;': 'ï', '&ntilde;': 'ñ',
    '&ograve;': 'ò', '&oacute;': 'ó', '&ocirc;': 'ô', '&ouml;': 'ö',
    '&ugrave;': 'ù', '&uacute;': 'ú', '&ucirc;': 'û', '&uuml;': 'ü',
    '*': '',  # Remove pronunciation markers
}

def create_directory_structure():
    """Create ../dictionary directory relative to script location."""
    script_dir = Path(__file__).parent
    dict_dir = script_dir.parent / "dictionary"
    dict_dir.mkdir(exist_ok=True)
    return dict_dir

def create_backup(original_file, backup_file):
    """Create backup of existing dictionary file."""
    try:
        log_print(f"Creating backup: {backup_file.name}")
        shutil.copy2(original_file, backup_file)
        log_print("✓ Backup created successfully")
        return True
    except Exception as e:
        log_print(f"✗ Backup failed: {e}")
        return False

def download_with_progress(url, filename):
    """Download file with progress indicator."""
    logged_percents = set()  # Track which percentages we've already logged
    
    def progress_hook(block_num, block_size, total_size):
        if total_size > 0:
            percent = min(100, (block_num * block_size * 100) // total_size)
            message = f"\rDownloading: {percent}% "
            sys.stdout.write(message)
            sys.stdout.flush()
            # Log progress only once per 10% milestone
            if percent % 10 == 0 and percent > 0 and percent not in logged_percents:
                logged_percents.add(percent)
                if log_file:
                    log_file.write(f"Download progress: {percent}%\n")
                    log_file.flush()
    
    try:
        log_print(f"Downloading GCIDE from {url}")
        urllib.request.urlretrieve(url, filename, progress_hook)
        log_print("\n✓ Download completed")
        return True
    except urllib.error.URLError as e:
        log_print(f"\n✗ Download failed: {e}")
        return False

def extract_zip_file(zip_file, extract_dir):
    """Extract ZIP and locate XML directory."""
    try:
        log_print("Extracting ZIP archive...")
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        
        # Find directory containing gcide_a.xml
        for root, dirs, files in os.walk(extract_dir):
            if 'gcide_a.xml' in files:
                log_print(f"✓ Found XML files in: {Path(root).name}")
                return Path(root)
        
        log_print("✗ GCIDE XML files not found in archive")
        return None
        
    except Exception as e:
        log_print(f"✗ Extraction failed: {e}")
        return None

def clean_text(text):
    """Clean HTML entities and extra whitespace from text."""
    for entity, replacement in ENTITY_REPLACEMENTS.items():
        text = text.replace(entity, replacement)
    return re.sub(r'\s+', ' ', text).strip()

def is_valid_headword(word):
    """Check if headword meets quality criteria."""
    # Remove non-letter characters except hyphens and apostrophes
    clean_word = re.sub(r'[^a-zA-ZÀ-ÿĀ-žΑ-ωА-я\'-]', '', word)
    
    return (clean_word and 
            len(clean_word) > 1 and 
            clean_word[0].isalpha() and 
            clean_word[-1].isalpha())

def extract_entries_from_file(xml_file):
    """Extract dictionary entries from a single XML file."""
    entries = []
    
    try:
        with open(xml_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Clean HTML entities
        content = clean_text(content)
        
        # Extract entries from <p> tags containing <hw> and <def>
        p_pattern = r'<p[^>]*>(.*?)</p>'
        p_matches = re.findall(p_pattern, content, re.DOTALL)
        
        for p_content in p_matches:
            hw_match = re.search(r'<hw[^>]*>(.*?)</hw>', p_content, re.DOTALL)
            def_match = re.search(r'<def[^>]*>(.*?)</def>', p_content, re.DOTALL)
            
            if hw_match and def_match:
                # Clean headword and definition
                headword = re.sub(r'<[^>]+>', '', hw_match.group(1)).strip()
                definition = re.sub(r'<[^>]+>', ' ', def_match.group(1)).strip()
                definition = re.sub(r'\s+', ' ', definition)
                
                # Apply quality filters
                if is_valid_headword(headword) and len(definition) > 10:
                    clean_headword = re.sub(r'[^a-zA-ZÀ-ÿĀ-žΑ-ωА-я\'-]', '', headword)
                    entries.append({
                        'word': clean_headword,
                        'definition': definition
                    })
        
        return entries
        
    except Exception as e:
        log_print(f"  ⚠ Warning: Could not process {xml_file.name}: {e}")
        return []

def combine_xml_files(source_dir, output_file):
    """Process all GCIDE XML files and combine into single dictionary."""
    try:
        log_print("Processing XML files...")
        
        # Find and sort letter files (gcide_a.xml through gcide_z.xml)
        xml_files = sorted(source_dir.glob("gcide_[a-z].xml"))
        if not xml_files:
            log_print("✗ No GCIDE letter files found")
            return False
        
        log_print(f"Found {len(xml_files)} XML files to process")
        all_entries = []
        
        # Process each XML file
        for i, xml_file in enumerate(xml_files, 1):
            log_print(f"  Processing {xml_file.name} ({i}/{len(xml_files)})...")
            entries = extract_entries_from_file(xml_file)
            all_entries.extend(entries)
            log_print(f"    Added {len(entries)} entries (total: {len(all_entries)})")
            
            # Progress indicator every 5000 entries
            if len(all_entries) % 5000 < len(entries):
                log_print(f"    Progress: {len(all_entries)} entries processed...")
        
        # Remove duplicates and sort
        log_print("Removing duplicates and sorting...")
        seen_words = set()
        unique_entries = []
        
        for entry in all_entries:
            word_lower = entry['word'].lower()
            if word_lower not in seen_words:
                seen_words.add(word_lower)
                unique_entries.append(entry)
        
        duplicates_removed = len(all_entries) - len(unique_entries)
        log_print(f"Removed {duplicates_removed} duplicate entries")
        
        unique_entries.sort(key=lambda x: x['word'].lower())
        log_print("Entries sorted alphabetically")
        
        # Write combined XML file
        log_print(f"Writing dictionary with {len(unique_entries)} entries...")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('<?xml version="1.0" encoding="utf-8"?>\n<dictionary>\n')
            
            for entry in unique_entries:
                # Escape XML characters
                word = entry['word'].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                definition = entry['definition'].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                
                f.write(f'  <entry><word>{word}</word><definition>{definition}</definition></entry>\n')
            
            f.write('</dictionary>\n')
        
        log_print(f"✓ Dictionary created with {len(unique_entries)} unique entries")
        return True
        
    except Exception as e:
        log_print(f"✗ Error combining XML files: {e}")
        return False

def main():
    """Main orchestration function."""
    # Setup logging first
    log_file_path = setup_logging()
    
    try:
        log_print("GCIDE Dictionary Downloader")
        log_print("=" * 30)
        
        # Setup paths
        dict_dir = create_directory_structure()
        temp_file = dict_dir / "gcide.zip"
        temp_extract_dir = dict_dir / "temp_extract"
        final_file = dict_dir / "dictionary.xml"
        backup_file = dict_dir / "dictionary_bu.xml"
        
        log_print(f"Dictionary directory: {dict_dir}")
        log_print(f"Output file: {final_file}")
        log_print(f"Log file: {log_file_path}")
        
        # Handle existing files
        if final_file.exists():
            log_print(f"Existing dictionary found: {final_file.name}")
            if not create_backup(final_file, backup_file):
                log_print("Aborting to prevent data loss")
                return
        
        # Download and process
        if not download_with_progress(GCIDE_URL, temp_file):
            log_print("Download failed, aborting")
            return
        
        temp_extract_dir.mkdir(exist_ok=True)
        xml_source_dir = extract_zip_file(temp_file, temp_extract_dir)
        
        if xml_source_dir and combine_xml_files(xml_source_dir, final_file):
            # Cleanup
            log_print("Cleaning up temporary files...")
            shutil.rmtree(temp_extract_dir)
            temp_file.unlink()
            log_print("✓ Temporary files removed")
            
            # Success summary
            size_mb = final_file.stat().st_size / (1024 * 1024)
            log_print(f"\n✓ SUCCESS!")
            log_print(f"Dictionary: {final_file} ({size_mb:.1f} MB)")
            if backup_file.exists():
                log_print(f"Backup: {backup_file.name}")
            log_print(f"Complete log saved to: {log_file_path}")
        else:
            log_print(f"\n✗ FAILED!")
            if backup_file.exists():
                log_print(f"Original backup safe at: {backup_file.name}")
    
    finally:
        # Always close log file
        close_logging()

if __name__ == "__main__":
    main()