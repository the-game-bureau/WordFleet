#!/usr/bin/env python3
"""
ENABLE Word List Downloader with Definitions
===========================================
Downloads ENABLE word list, extracts 2-5 letter words, and adds definitions.
Incremental updates - only adds new words/definitions.
"""

import os
import requests
import time
from pathlib import Path
from typing import Optional, List
from datetime import datetime
import xml.etree.ElementTree as ET
from xml.dom import minidom

print("🚀 Starting ENABLE Dictionary Builder...")
print("=" * 60)

# Global configuration
DICT_DIR = Path("dictionary")
LOG_DIR = Path("log")
WORDS_FILE = DICT_DIR / "words.lst"
XML_FILE = DICT_DIR / "words.xml"
LOG_FILE = LOG_DIR / "log.txt"
ENABLE_URL = "https://norvig.com/ngrams/enable1.txt"

# Create directories
DICT_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)
print(f"📁 Created directories: {DICT_DIR}, {LOG_DIR}")

# Log messages for later
log_messages = []

def log_message(msg):
    """Log message to both console and log buffer"""
    print(msg)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_messages.append(f"[{timestamp}] {msg}")

def write_log():
    """Write log messages to file"""
    try:
        with open(LOG_FILE, 'w', encoding='utf-8') as f:
            f.write("ENABLE Dictionary Builder Log\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 50 + "\n\n")
            for msg in log_messages:
                clean_msg = ''.join(c for c in msg if ord(c) < 128 or c.isalnum() or c in ' .,!?:-/\\()[]{}=')
                f.write(clean_msg + "\n")
        log_message(f"📝 Log saved to: {LOG_FILE}")
    except Exception as e:
        print(f"❌ Error writing log: {e}")

def download_words():
    """Download ENABLE word list if it doesn't exist"""
    log_message("\n🔄 Phase 1: Download ENABLE word list")
    
    if WORDS_FILE.exists():
        log_message(f"✅ Word list already exists: {WORDS_FILE}")
        with open(WORDS_FILE, 'r') as f:
            existing_words = [line.strip() for line in f if line.strip()]
        log_message(f"📊 Found {len(existing_words)} existing words")
        return True
    
    log_message("📥 Downloading ENABLE word list...")
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(ENABLE_URL, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Process and save words
        words = [line.strip().upper() for line in response.text.strip().split('\n') if line.strip()]
        words = sorted(set(words))  # Remove duplicates and sort
        
        with open(WORDS_FILE, 'w') as f:
            for word in words:
                f.write(word + '\n')
        
        log_message(f"✅ Downloaded {len(words)} words to {WORDS_FILE}")
        log_message(f"📊 File size: {WORDS_FILE.stat().st_size / 1024:.1f} KB")
        return True
        
    except Exception as e:
        log_message(f"❌ Download failed: {e}")
        return False

def extract_short_words():
    """Extract 2-5 letter words and create/update XML"""
    log_message("\n🔄 Phase 2: Extract short words to XML")
    
    if not WORDS_FILE.exists():
        log_message(f"❌ Word list not found: {WORDS_FILE}")
        return False
    
    # Read all words
    with open(WORDS_FILE, 'r') as f:
        all_words = [line.strip().upper() for line in f if line.strip()]
    
    log_message(f"📖 Read {len(all_words)} words from {WORDS_FILE}")
    
    # Filter for short words (2-5 letters)
    new_short_words = {}
    for word in all_words:
        word_len = len(word)
        if 2 <= word_len <= 5:
            if word_len not in new_short_words:
                new_short_words[word_len] = []
            new_short_words[word_len].append(word)
    
    # Check existing XML
    existing_words = {}
    root = None
    
    if XML_FILE.exists():
        log_message(f"📂 Loading existing XML: {XML_FILE}")
        try:
            tree = ET.parse(XML_FILE)
            root = tree.getroot()
            
            for length_group in root.findall('length_group'):
                length = int(length_group.get('letters'))
                existing_words[length] = set()
                for word_elem in length_group.findall('word'):
                    existing_words[length].add(word_elem.text.strip().upper())
            
            existing_count = sum(len(words) for words in existing_words.values())
            log_message(f"📊 Found {existing_count} existing words in XML")
            
        except Exception as e:
            log_message(f"⚠️ Error reading XML: {e} - creating new file")
            existing_words = {}
            root = None
    else:
        log_message("📄 No existing XML - creating new file")
    
    # Calculate new words to add
    words_to_add = {}
    total_new = 0
    
    for length, words in new_short_words.items():
        existing_set = existing_words.get(length, set())
        new_words = [w for w in words if w not in existing_set]
        if new_words:
            words_to_add[length] = sorted(new_words)
            total_new += len(new_words)
    
    if total_new == 0:
        log_message("✅ No new words to add - XML is up to date")
        return True
    
    log_message(f"➕ Adding {total_new} new words:")
    for length, words in words_to_add.items():
        log_message(f"   • {length} letters: {len(words)} words")
    
    # Create or update XML
    if root is None:
        root = ET.Element("wordlist")
        root.set("source", "ENABLE")
        
        metadata = ET.SubElement(root, "metadata")
        ET.SubElement(metadata, "description").text = "Short words (2-5 letters) from ENABLE"
        ET.SubElement(metadata, "license").text = "Public Domain"
        ET.SubElement(metadata, "url").text = ENABLE_URL
    
    root.set("last_updated", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    # Add new words
    for length in sorted(words_to_add.keys()):
        new_words = words_to_add[length]
        
        # Find or create length group
        length_group = None
        for group in root.findall('length_group'):
            if group.get('letters') == str(length):
                length_group = group
                break
        
        if length_group is None:
            length_group = ET.SubElement(root, "length_group")
            length_group.set("letters", str(length))
        
        # Add new words
        for word in new_words:
            word_elem = ET.SubElement(length_group, "word")
            word_elem.text = word
        
        # Update count
        all_words_in_group = length_group.findall('word')
        length_group.set("count", str(len(all_words_in_group)))
    
    # Update total count
    total_words = sum(len(group.findall('word')) for group in root.findall('length_group'))
    root.set("total_words", str(total_words))
    
    # Save XML
    rough_string = ET.tostring(root, encoding='unicode')
    reparsed = minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent="  ")
    pretty_lines = [line for line in pretty_xml.split('\n') if line.strip()]
    formatted_xml = '\n'.join(pretty_lines)
    
    with open(XML_FILE, 'w') as f:
        f.write(formatted_xml)
    
    log_message(f"💾 Updated XML: {XML_FILE}")
    log_message(f"📊 Total words: {total_words}")
    log_message(f"📊 File size: {XML_FILE.stat().st_size / 1024:.1f} KB")
    
    return True

def test_definition_api():
    """Test definition API with sample words"""
    log_message("\n🧪 Testing definition API...")
    
    test_words = ["CAT", "DOG", "RUN", "BIG", "SUN"]
    successful = 0
    
    for word in test_words:
        try:
            url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word.lower()}"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data and len(data) > 0 and 'meanings' in data[0]:
                    definition = data[0]['meanings'][0]['definitions'][0]['definition']
                    log_message(f"   ✅ {word}: {definition[:40]}...")
                    successful += 1
                else:
                    log_message(f"   ❌ {word}: No definition found")
            else:
                log_message(f"   ❌ {word}: API error {response.status_code}")
            time.sleep(0.2)
        except:
            log_message(f"   ❌ {word}: Request failed")
    
    success_rate = (successful / len(test_words)) * 100
    log_message(f"📊 API test: {successful}/{len(test_words)} successful ({success_rate:.1f}%)")
    
    return success_rate >= 60

def lookup_definition(word):
    """Look up single word definition"""
    try:
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word.lower()}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0 and 'meanings' in data[0]:
                meaning = data[0]['meanings'][0]
                definition = meaning['definitions'][0]['definition']
                part_of_speech = meaning.get('partOfSpeech', '')
                
                if part_of_speech:
                    return f"({part_of_speech}) {definition}"
                else:
                    return definition
        return None
    except:
        return None

def add_definitions():
    """Add definitions to words that don't have them - 1000 at a time"""
    log_message("\n🔄 Phase 3: Add definitions (1000 at a time)")
    
    if not XML_FILE.exists():
        log_message(f"❌ XML file not found: {XML_FILE}")
        return False
    
    # Parse XML
    tree = ET.parse(XML_FILE)
    root = tree.getroot()
    
    # Count definition status
    total_words = 0
    has_definitions = 0
    needs_definitions = []
    
    for length_group in root.findall('length_group'):
        for word_elem in length_group.findall('word'):
            total_words += 1
            word = word_elem.text.strip()
            existing_def = word_elem.get('definition')
            
            if existing_def and existing_def != '[Definition not found]':
                has_definitions += 1
            else:
                needs_definitions.append((word_elem, word))
    
    log_message(f"📊 Definition status:")
    log_message(f"   • Total words: {total_words}")
    log_message(f"   • Have definitions: {has_definitions}")
    log_message(f"   • Need definitions: {len(needs_definitions)}")
    
    if len(needs_definitions) == 0:
        log_message("✅ All words already have definitions!")
        return True
    
    # Test API first
    if not test_definition_api():
        log_message("⚠️ API test failed - skipping definitions")
        log_message("💡 Try again later when API is working")
        return True
    
    # Process 1000 words that need definitions
    words_to_process = needs_definitions[:1000]
    log_message(f"🔍 Looking up definitions for {len(words_to_process)} words...")
    log_message(f"⏱️ This will take about {len(words_to_process) * 0.1 / 60:.1f} minutes with rate limiting...")
    
    found = 0
    failed = 0
    
    for i, (word_elem, word) in enumerate(words_to_process):
        definition = lookup_definition(word)
        
        if definition:
            word_elem.set('definition', definition)
            found += 1
        else:
            word_elem.set('definition', '[Definition not found]')
            failed += 1
        
        # Progress indicator every 100 words
        if (i + 1) % 100 == 0:
            progress = ((i + 1) / len(words_to_process)) * 100
            log_message(f"   Progress: {progress:.0f}% ({found} found, {failed} failed)")
        
        time.sleep(0.1)  # Rate limiting - 10 requests per second
    
    # Update metadata
    metadata = root.find('metadata')
    if metadata is not None:
        # Update or create timestamp
        timestamp_elem = metadata.find('definitions_last_updated')
        if timestamp_elem is not None:
            timestamp_elem.text = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            ET.SubElement(metadata, 'definitions_last_updated').text = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Update or create source
        source_elem = metadata.find('definition_source')
        if source_elem is None:
            ET.SubElement(metadata, 'definition_source').text = "Free Dictionary API"
    
    # Save updated XML
    try:
        rough_string = ET.tostring(root, encoding='unicode')
        reparsed = minidom.parseString(rough_string)
        pretty_xml = reparsed.toprettyxml(indent="  ")
        pretty_lines = [line for line in pretty_xml.split('\n') if line.strip()]
        formatted_xml = '\n'.join(pretty_lines)
        
        with open(XML_FILE, 'w', encoding='utf-8') as f:
            f.write(formatted_xml)
        
        log_message(f"💾 Saved updated XML to: {XML_FILE}")
        
    except Exception as e:
        log_message(f"❌ Error saving XML: {e}")
        return False
    
    # Calculate totals
    total_found = has_definitions + found
    total_failed = total_words - total_found
    remaining = len(needs_definitions) - len(words_to_process)
    
    log_message(f"\n✅ Batch complete!")
    log_message(f"📊 This batch:")
    log_message(f"   • Processed: {len(words_to_process)} words")
    log_message(f"   • Found: {found} definitions")
    log_message(f"   • Failed: {failed} definitions")
    log_message(f"   • Success rate: {(found/len(words_to_process))*100:.1f}%")
    log_message(f"📊 Overall status:")
    log_message(f"   • Total with definitions: {total_found}/{total_words}")
    log_message(f"   • Still need definitions: {remaining}")
    log_message(f"   • Overall success rate: {(total_found/total_words)*100:.1f}%")
    
    if remaining > 0:
        batches_remaining = (remaining + 999) // 1000  # Round up
        log_message(f"💡 Run the script {batches_remaining} more time(s) to process {remaining} more words")
    else:
        log_message(f"🎉 All words now have definitions!")
    
    return True

def main():
    """Main workflow"""
    try:
        # Phase 1: Download words (if needed)
        if not download_words():
            log_message("❌ Download failed")
            write_log()
            return False
        
        # Phase 2: Extract short words to XML
        if not extract_short_words():
            log_message("❌ XML creation failed")
            write_log()
            return False
        
        # Phase 3: Ask about definitions
        print(f"\n" + "=" * 60)
        print("🤔 Add definitions to words?")
        print("   This takes several minutes (~12k words)")
        print("   Uses free API with rate limiting")
        
        choice = input("Add definitions? (y/N): ").lower().strip()
        
        if choice in ['y', 'yes']:
            add_definitions()
        else:
            log_message("⏭️ Skipping definitions")
        
        # Success summary
        log_message(f"\n🎉 Dictionary processing complete!")
        log_message(f"📂 Files created:")
        log_message(f"   • {WORDS_FILE} (full word list)")
        log_message(f"   • {XML_FILE} (short words + definitions)")
        log_message(f"   • {LOG_FILE} (process log)")
        
        write_log()
        
        print(f"\n✨ SUCCESS!")
        print(f"📂 Check your files:")
        print(f"   • dictionary/words.lst")
        print(f"   • dictionary/words.xml") 
        print(f"   • log/log.txt")
        print(f"\n💡 Perfect for word games!")
        
        return True
        
    except Exception as e:
        log_message(f"💥 Critical error: {e}")
        import traceback
        traceback.print_exc()
        write_log()
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        exit(1)