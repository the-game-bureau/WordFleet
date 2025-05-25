#!/usr/bin/env python3
"""
Dictionary downloader for GCIDE (GNU Collaborative International Dictionary of English)
Downloads the dictionary XML file from ibiblio.org to ../dictionary/dictionary.xml

CLAUDE.AI PROMPT TO RECREATE THIS FILE:
---------------------------------------
Create a Python script that downloads the GCIDE (GNU Collaborative International Dictionary of English) 
from https://www.ibiblio.org/webster/gcide_xml-0.53.zip and processes it into a clean XML dictionary file.

Requirements:
1. Download the ZIP file with a progress indicator
2. Extract and find the XML files (gcide_a.xml through gcide_z.xml)
3. Parse each XML file to extract dictionary entries with <hw> (headword) and <def> (definition) tags
4. Clean up HTML entities and remove markup from definitions
5. Filter entries to only include valid words (letters, hyphens, apostrophes only)
6. Combine all entries into a single dictionary.xml file with <entry><word></word><definition></definition></entry> structure
7. Remove duplicates and sort alphabetically
8. Create backups of existing files before overwriting
9. Include proper error handling and user prompts
10. Store the final file in ../dictionary/dictionary.xml relative to the script location

The script should handle XML entity replacements, progress reporting, and cleanup of temporary files.
---------------------------------------
"""

import os
import sys
import urllib.request
import urllib.error
import shutil
from pathlib import Path

# GCIDE XML download URL - from ibiblio.org (current working location)
GCIDE_URL = "https://www.ibiblio.org/webster/gcide_xml-0.53.zip"

def create_directory_structure():
    """
    Create the dictionary directory if it doesn't exist.
    
    Returns:
        Path: Path object pointing to the dictionary directory (../dictionary relative to script)
    """
    script_dir = Path(__file__).parent  # Get directory containing this script
    dict_dir = script_dir.parent / "dictionary"  # Go up one level, then into dictionary folder
    dict_dir.mkdir(exist_ok=True)  # Create directory if it doesn't exist
    return dict_dir

def create_backup(original_file, backup_file):
    """
    Create a backup copy of the original dictionary file.
    
    Args:
        original_file (Path): Path to the existing dictionary.xml file
        backup_file (Path): Path where backup should be created (dictionary_bu.xml)
    
    Returns:
        bool: True if backup successful, False otherwise
    """
    try:
        print(f"Creating backup: {backup_file}")
        # shutil.copy2 preserves timestamps and metadata
        shutil.copy2(original_file, backup_file)
        print(f"Backup created successfully!")
        return True
    except Exception as e:
        print(f"Failed to create backup: {e}")
        return False

def download_with_progress(url, filename):
    """
    Download file with progress indicator.
    
    Args:
        url (str): URL to download from
        filename (Path): Local filename to save to
    
    Returns:
        bool: True if download successful, False otherwise
    """
    def progress_hook(block_num, block_size, total_size):
        """Callback function to show download progress"""
        if total_size > 0:
            # Calculate percentage completed
            percent = min(100, (block_num * block_size * 100) // total_size)
            sys.stdout.write(f"\rDownloading: {percent}% ")
            sys.stdout.flush()
    
    try:
        print(f"Downloading GCIDE from {url}")
        # urllib.request.urlretrieve downloads file and calls progress_hook for updates
        urllib.request.urlretrieve(url, filename, progress_hook)
        print("\nDownload completed!")
        return True
    except urllib.error.URLError as e:
        print(f"\nDownload failed: {e}")
        return False

def extract_zip_file(zip_file, extract_dir):
    """
    Extract ZIP file and find the XML directory.
    
    Args:
        zip_file (Path): Path to the downloaded ZIP file
        extract_dir (Path): Directory to extract contents to
    
    Returns:
        Path or None: Path to directory containing XML files, or None if not found
    """
    try:
        import zipfile
        print("Extracting XML from ZIP archive...")
        
        # Extract all contents of ZIP file
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        
        # Search through extracted files to find XML directory
        # GCIDE files are named gcide_a.xml, gcide_b.xml, etc.
        xml_dir = None
        for root, dirs, files in os.walk(extract_dir):
            # Look for a directory containing gcide_a.xml (first letter file)
            if 'gcide_a.xml' in files:
                xml_dir = root
                break
        
        if xml_dir:
            print(f"Found XML files in: {xml_dir}")
            return Path(xml_dir)
        else:
            print("Error: Could not find GCIDE XML files in the extracted archive")
            return None
        
    except Exception as e:
        print(f"Extraction failed: {e}")
        return None

def combine_xml_files(source_dir, output_file):
    """
    Combine all GCIDE XML files into a single dictionary.xml file.
    
    This function processes the individual letter XML files (gcide_a.xml through gcide_z.xml),
    extracts dictionary entries, cleans up the text, and combines them into one organized file.
    
    Args:
        source_dir (Path): Directory containing the GCIDE XML files
        output_file (Path): Path where the combined dictionary.xml should be written
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        import re
        print("Parsing and combining XML files...")
        
        # Find letter files only (skip authorities and abbreviations)
        # Pattern matches gcide_a.xml, gcide_b.xml, etc.
        xml_files = list(source_dir.glob("gcide_[a-z].xml"))
        xml_files.sort()  # Process in alphabetical order (a, b, c, ...)
        
        entry_count = 0
        all_entries = []
        
        # Common HTML/XML entity replacements - converts encoded characters to Unicode
        entity_replacements = {
            '&mdash;': '—',     # Em dash
            '&nbsp;': ' ',      # Non-breaking space
            '&amp;': '&',       # Ampersand
            '&lt;': '<',        # Less than
            '&gt;': '>',        # Greater than
            '&quot;': '"',      # Quote
            '&apos;': "'",      # Apostrophe
            '&deg;': '°',       # Degree symbol
            '&pound;': '£',     # Pound sterling
            '&sect;': '§',      # Section symbol
            '&para;': '¶',      # Paragraph symbol
            '&middot;': '·',    # Middle dot
            '&times;': '×',     # Multiplication
            '&divide;': '÷',    # Division
            '&prime;': '′',     # Prime (minutes/feet)
            '&Prime;': '″',     # Double prime (seconds/inches)
            '&radic;': '√',     # Square root
            '&int;': '∫',       # Integral
            # Greek letters
            '&Alpha;': 'Α', '&Beta;': 'Β', '&Gamma;': 'Γ', '&Delta;': 'Δ',
            '&alpha;': 'α', '&beta;': 'β', '&gamma;': 'γ', '&delta;': 'δ',
            # Latin characters with diacritics
            '&AElig;': 'Æ', '&aelig;': 'æ', '&OElig;': 'Œ', '&oelig;': 'œ',
            '&agrave;': 'à', '&aacute;': 'á', '&acirc;': 'â', '&atilde;': 'ã',
            '&auml;': 'ä', '&aring;': 'å', '&ccedil;': 'ç', '&egrave;': 'è',
            '&eacute;': 'é', '&ecirc;': 'ê', '&euml;': 'ë', '&igrave;': 'ì',
            '&iacute;': 'í', '&icirc;': 'î', '&iuml;': 'ï', '&ntilde;': 'ñ',
            '&ograve;': 'ò', '&oacute;': 'ó', '&ocirc;': 'ô', '&ouml;': 'ö',
            '&ugrave;': 'ù', '&uacute;': 'ú', '&ucirc;': 'û', '&uuml;': 'ü',
            # Remove formatting markers
            '*': '',  # Remove asterisks used for pronunciation marks
        }
        
        # Process each XML file (gcide_a.xml, gcide_b.xml, etc.)
        for xml_file in xml_files:
            print(f"Processing {xml_file.name}...")
            
            try:
                # Read the entire XML file as text
                with open(xml_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Replace HTML/XML entities with Unicode characters
                for entity, replacement in entity_replacements.items():
                    content = content.replace(entity, replacement)
                
                # Extract dictionary entries using regex
                # GCIDE structure: <p>...</p> tags contain dictionary entries
                # Each entry has <hw>headword</hw> and <def>definition</def> tags
                pattern = r'<p[^>]*>(.*?)</p>'  # Find all paragraph tags
                p_matches = re.findall(pattern, content, re.DOTALL)  # DOTALL allows . to match newlines
                
                for p_content in p_matches:
                    # Extract headword (the word being defined)
                    hw_match = re.search(r'<hw[^>]*>(.*?)</hw>', p_content, re.DOTALL)
                    # Extract definition (the meaning)
                    def_match = re.search(r'<def[^>]*>(.*?)</def>', p_content, re.DOTALL)
                    
                    # Only process entries that have both headword and definition
                    if hw_match and def_match:
                        # Clean up the headword - remove any remaining HTML/XML tags
                        headword = re.sub(r'<[^>]+>', '', hw_match.group(1)).strip()
                        # Clean up the definition - remove HTML/XML tags but keep the text
                        definition = re.sub(r'<[^>]+>', ' ', def_match.group(1)).strip()
                        # Clean up extra whitespace (multiple spaces become single space)
                        definition = re.sub(r'\s+', ' ', definition)
                        
                        # Filter headword to only contain valid characters
                        # Keep: letters (including international), hyphens, apostrophes
                        # Remove: numbers, symbols, punctuation marks
                        clean_headword = re.sub(r'[^a-zA-ZÀ-ÿĀ-žΑ-ωА-я\'-]', '', headword)
                        
                        # Quality filters - only keep entries that:
                        # 1. Have actual letters (not empty after cleaning)
                        # 2. Are longer than 1 character (no single letters)
                        # 3. Start and end with alphabetic characters (not punctuation)
                        # 4. Have a meaningful definition (longer than 10 characters)
                        if (clean_headword and 
                            len(clean_headword) > 1 and 
                            clean_headword[0].isalpha() and 
                            clean_headword[-1].isalpha() and 
                            definition and 
                            len(definition) > 10):
                            
                            entry_count += 1
                            all_entries.append({
                                'word': clean_headword,
                                'definition': definition
                            })
                            
                            # Progress indicator - print every 5000 entries
                            if entry_count % 5000 == 0:
                                print(f"  Processed {entry_count} entries...")
                                
            except Exception as e:
                # If one file fails, continue with the others
                print(f"  Warning: Could not process {xml_file.name}: {e}")
                continue
        
        # Write the final combined XML file
        print(f"Writing combined dictionary with {entry_count} entries...")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            # Write XML header
            f.write('<?xml version="1.0" encoding="utf-8"?>\n')
            f.write('<dictionary>\n')
            
            # Remove duplicates based on word (case-insensitive)
            # Keep the first occurrence of each word
            seen_words = set()
            unique_entries = []
            for entry in all_entries:
                word_lower = entry['word'].lower()
                if word_lower not in seen_words:
                    seen_words.add(word_lower)
                    unique_entries.append(entry)
            
            # Sort entries alphabetically by word (case-insensitive)
            unique_entries.sort(key=lambda x: x['word'].lower())
            
            # Write each dictionary entry
            for entry in unique_entries:
                # Escape XML characters in word and definition to prevent XML parsing errors
                word = entry['word'].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                definition = entry['definition'].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                
                # Write entry in clean XML format
                f.write(f'  <entry>\n')
                f.write(f'    <word>{word}</word>\n')
                f.write(f'    <definition>{definition}</definition>\n')
                f.write(f'  </entry>\n')
            
            # Close XML root tag
            f.write('</dictionary>\n')
        
        unique_count = len(unique_entries)
        print(f"Successfully created {output_file} with {unique_count} unique dictionary entries!")
        return True
        
    except Exception as e:
        print(f"Error combining XML files: {e}")
        return False

def main():
    """
    Main download and processing function.
    
    This orchestrates the entire process:
    1. Create directory structure
    2. Check for existing files and create backups
    3. Download the GCIDE ZIP file
    4. Extract and find XML files
    5. Process and combine into single dictionary.xml
    6. Clean up temporary files
    """
    print("GCIDE Dictionary Downloader")
    print("=" * 30)
    
    # Set up file paths
    dict_dir = create_directory_structure()  # ../dictionary/ relative to script
    temp_file = dict_dir / "gcide.zip"       # Temporary ZIP download
    temp_extract_dir = dict_dir / "temp_extract"  # Temporary extraction directory
    final_file = dict_dir / "dictionary.xml"      # Final output file
    backup_file = dict_dir / "dictionary_bu.xml"  # Backup of existing file
    
    # Handle existing dictionary file
    if final_file.exists():
        print(f"Existing dictionary found at {final_file}")
        
        # Create backup first - this is critical to prevent data loss
        if create_backup(final_file, backup_file):
            print("Backup created successfully!")
        else:
            print("Failed to create backup. Aborting to prevent data loss.")
            return
        
        # Automatically proceed after backup is created
        print("Proceeding with download...")
    else:
        print(f"Dictionary not found. Creating new dictionary at {final_file}")
    
    # Download the GCIDE ZIP file from ibiblio.org
    if download_with_progress(GCIDE_URL, temp_file):
        print("Download completed!")
    else:
        print("Download failed. Please check your internet connection.")
        return
    
    # Extract ZIP file and locate XML files
    temp_extract_dir.mkdir(exist_ok=True)  # Create extraction directory
    xml_source_dir = extract_zip_file(temp_file, temp_extract_dir)
    
    if xml_source_dir:
        # Process XML files and create combined dictionary
        if combine_xml_files(xml_source_dir, final_file):
            # Clean up temporary files to save disk space
            shutil.rmtree(temp_extract_dir)  # Remove entire extraction directory
            temp_file.unlink()               # Remove ZIP file
            
            # Show success information
            print(f"\nDictionary successfully created at: {final_file}")
            print(f"File size: {final_file.stat().st_size / (1024*1024):.1f} MB")
            if backup_file.exists():
                print(f"Backup available at: {backup_file}")
        else:
            print("Failed to combine XML files.")
            if backup_file.exists():
                print(f"Original dictionary backup is safe at: {backup_file}")
    else:
        print("Failed to extract dictionary files.")
        if backup_file.exists():
            print(f"Original dictionary backup is safe at: {backup_file}")

if __name__ == "__main__":
    """
    Script entry point - only runs main() when script is executed directly,
    not when imported as a module.
    """
    main()