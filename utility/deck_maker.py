#!/usr/bin/env python3
"""
Dictionary Deck Maker - Creates word decks from dictionary XML
Processes dictionary.xml to create word_decks.xml with filtered and capitalized words

CLAUDE.AI RECREATION PROMPT:
===========================
Create a Python script that processes a dictionary XML file with the following specifications:

CORE FUNCTIONALITY:
- Read dictionary/dictionary.xml relative to script location
- Copy to dictionary/word_decks.xml as backup and working file
- Parse XML entries with <entry><word></word><definition></definition></entry> structure
- Filter words: length 2-5 characters, standard 26 letters only (a-z, A-Z)
- Convert all words to UPPERCASE (word -> WORD format)
- Add <deck_All>All</deck_All> element to each remaining entry
- Remove entries that don't meet criteria
- Save processed XML with proper encoding and declaration

REQUIREMENTS:
- Use relative paths (../dictionary/ folder from utility/ subdirectory)
- Use xml.etree.ElementTree for XML processing
- Proper error handling with informative messages
- Progress reporting: show removed count and processing status
- Preserve XML structure and formatting
- Cross-platform compatibility with pathlib
- Log all output to log/log.txt

STRUCTURE:
- process_dictionary(): Main processing function
- Input validation and file existence checks
- XML parsing, filtering, and modification
- Statistics reporting (entries removed, entries processed)
- Clean error handling and user feedback

The script should be self-contained and work in any environment.
===========================
"""

import xml.etree.ElementTree as ET
import shutil
from pathlib import Path
from datetime import datetime
import re

def log_message(message, log_file):
    """Write message to both console and log file."""
    print(message)
    log_file.write(message + '\n')
    log_file.flush()  # Ensure immediate write

def is_word_related_to_topic(word, definition, topic):
    """Use AI magic (keyword matching) to determine if word relates to topic."""
    topic_lower = topic.lower()
    word_lower = word.lower()
    definition_lower = definition.lower() if definition else ""
    
    # Direct word match
    if topic_lower in word_lower or word_lower in topic_lower:
        return True
    
    # Definition contains topic
    if topic_lower in definition_lower:
        return True
    
    # Topic-specific keyword matching (expandable AI magic)
    topic_keywords = {
        'animals': ['animal', 'beast', 'creature', 'pet', 'wild', 'zoo', 'farm', 'dog', 'cat', 'bird', 'fish', 'mammal', 'reptile'],
        'food': ['eat', 'food', 'meal', 'cook', 'recipe', 'taste', 'flavor', 'dish', 'fruit', 'meat', 'bread', 'drink', 'sweet', 'sour', 'salt', 'spice', 'hot', 'cold', 'fresh', 'ripe', 'raw', 'bake', 'fry', 'boil', 'mix', 'chop', 'cut', 'slice', 'serve', 'plate', 'bowl', 'cup', 'fork', 'knife', 'spoon', 'chef', 'kitchen', 'oven', 'fire', 'heat', 'oil', 'soup', 'cake', 'pie', 'egg', 'milk', 'fish', 'beef', 'pork', 'rice', 'bean', 'corn', 'apple', 'berry'],
        'colors': ['color', 'colour', 'red', 'blue', 'green', 'yellow', 'black', 'white', 'pink', 'purple', 'orange', 'brown'],
        'nature': ['tree', 'plant', 'flower', 'forest', 'mountain', 'river', 'ocean', 'sky', 'earth', 'nature', 'outdoor', 'wild', 'wood', 'leaf', 'grass', 'rock', 'stone', 'water', 'lake', 'sea', 'beach', 'hill', 'field', 'park', 'cave', 'bird', 'wind', 'rain', 'snow', 'sun'],
        'sports': ['sport', 'game', 'play', 'team', 'ball', 'run', 'jump', 'race', 'win', 'compete', 'athletic'],
        'science': ['science', 'lab', 'test', 'study', 'research', 'experiment', 'theory', 'biology', 'chemistry', 'physics'],
        'music': ['music', 'song', 'sound', 'note', 'rhythm', 'melody', 'instrument', 'piano', 'guitar', 'drum', 'sing'],
        'travel': ['travel', 'trip', 'journey', 'road', 'path', 'city', 'country', 'map', 'explore', 'visit', 'tour', 'plane', 'train', 'car', 'bus', 'ship', 'boat', 'hotel', 'place', 'go', 'move', 'away', 'far', 'near', 'here', 'there'],
        'space': ['space', 'star', 'moon', 'sun', 'planet', 'galaxy', 'orbit', 'rocket', 'sky', 'cosmic', 'solar', 'lunar', 'mars', 'earth', 'venus', 'outer', 'void', 'dark', 'light', 'bright', 'far', 'vast', 'big', 'huge', 'high', 'up', 'fly', 'float'],
        'technology': ['tech', 'computer', 'machine', 'device', 'tool', 'gadget', 'robot', 'digital', 'cyber', 'electronic', 'electric', 'power', 'energy', 'motor', 'engine', 'gear', 'wire', 'cable', 'circuit', 'chip', 'code', 'data', 'info', 'web', 'net', 'online', 'smart', 'auto', 'fast', 'new', 'modern', 'high', 'tech'],
    }
    
    # Check if topic has predefined keywords
    keywords = topic_keywords.get(topic_lower, [topic_lower])
    
    # Check if any keyword appears in word or definition
    for keyword in keywords:
        if keyword in word_lower or keyword in definition_lower:
            return True
    
    return False

def process_dictionary():
    """Process dictionary XML to create filtered word decks."""
    # Use relative paths from utility/ folder
    script_dir = Path(__file__).parent
    dict_dir = script_dir.parent / "dictionary"  # Go up one level to reach dictionary/
    log_dir = script_dir.parent / "log"  # Go up one level to reach log/
    source_file = dict_dir / "dictionary.xml"
    target_file = dict_dir / "word_decks.xml"
    log_file_path = log_dir / "log.txt"
    
    # Create log directory if it doesn't exist
    log_dir.mkdir(exist_ok=True)
    
    # Open log file for writing
    with open(log_file_path, 'w', encoding='utf-8') as log_file:
        # Write header with timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message(f"Dictionary Deck Maker - Started at {timestamp}", log_file)
        log_message("==================================================", log_file)
        
        # Validate source file exists
        if not source_file.exists():
            log_message(f"✗ Error: {source_file} not found!", log_file)
            log_message("Please run dictionary_download.py first to create the dictionary.", log_file)
            return False
        
        # Check if word_decks.xml already exists
        if target_file.exists():
            log_message(f"✓ {target_file.name} already exists - skipping initial processing", log_file)
            log_message("Your existing deck tags are preserved!", log_file)
            return True
        
        try:
            # Create backup copy ONLY if word_decks.xml doesn't exist
            log_message(f"Creating initial {target_file.name} from {source_file.name}...", log_file)
            shutil.copy2(source_file, target_file)
            log_message("✓ Initial file created successfully", log_file)
            
            # Parse XML
            log_message("Parsing XML...", log_file)
            tree = ET.parse(target_file)
            root = tree.getroot()
            
            total_entries = len(root.findall('entry'))
            log_message(f"Found {total_entries} total entries", log_file)
            
            entries_to_remove = []
            entries_processed = 0
            
            # Process each entry
            log_message("Processing entries...", log_file)
            for entry in root.findall('entry'):
                word_element = entry.find('word')
                if word_element is not None and word_element.text:
                    word = word_element.text.strip()
                    
                    # Apply filters
                    is_valid_length = 2 <= len(word) <= 5
                    is_standard_letters = word.isalpha() and all(c.isascii() for c in word)
                    
                    if not (is_valid_length and is_standard_letters):
                        entries_to_remove.append(entry)
                    else:
                        # Convert to uppercase
                        word_element.text = word.upper()
                        
                        # Add deck element with correct format
                        deck_element = ET.SubElement(entry, 'deck_All')
                        deck_element.text = 'All'
                        entries_processed += 1
                else:
                    # Remove entries without valid word elements
                    entries_to_remove.append(entry)
            
            # Remove filtered entries
            log_message("Removing filtered entries...", log_file)
            for entry in entries_to_remove:
                root.remove(entry)
            
            # Save processed XML
            log_message("Saving processed dictionary...", log_file)
            tree.write(target_file, encoding='utf-8', xml_declaration=True)
            
            # Report results
            log_message("", log_file)  # Empty line
            log_message("✓ Processing complete!", log_file)
            log_message(f"Total entries processed: {total_entries}", log_file)
            log_message(f"Entries kept: {entries_processed}", log_file)
            log_message(f"Entries removed: {len(entries_to_remove)}", log_file)
            log_message(f"Words converted to UPPERCASE and deck tags added", log_file)
            log_message(f"Output saved to: {target_file}", log_file)
            log_message(f"Log saved to: {log_file_path}", log_file)
            
            return True
            
        except ET.ParseError as e:
            log_message(f"✗ XML parsing error: {e}", log_file)
            log_message("The dictionary file may be corrupted or invalid.", log_file)
            return False
        except Exception as e:
            log_message(f"✗ Error: {e}", log_file)
            return False
        
        finally:
            # Write footer
            end_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_message("==================================================", log_file)
            log_message(f"Dictionary Deck Maker - Completed at {end_timestamp}", log_file)

def get_existing_deck_topics(target_file):
    """Get list of all deck topics that already exist in the XML."""
    existing_topics = set()
    
    try:
        tree = ET.parse(target_file)
        root = tree.getroot()
        
        # Find all deck tags in format deck_TopicName
        for entry in root.findall('entry'):
            for element in entry:
                if element.tag.startswith('deck_'):
                    topic = element.tag[5:]  # Remove 'deck_' prefix
                    if topic != 'All':  # Skip the default 'All' topic
                        existing_topics.add(topic.lower())
        
    except Exception as e:
        print(f"Warning: Could not read existing topics: {e}")
    
    return existing_topics

def show_available_topics_for_make(target_file):
    """Display available predefined topics that haven't been created yet."""
    all_topics = {
        'animals': ['animal', 'beast', 'creature', 'pet', 'wild', 'zoo', 'farm', 'dog', 'cat', 'bird', 'fish', 'mammal', 'reptile'],
        'food': ['eat', 'food', 'meal', 'cook', 'recipe', 'taste', 'flavor', 'dish', 'fruit', 'meat', 'bread', 'drink', 'sweet', 'sour', 'salt', 'spice', 'hot', 'cold', 'fresh', 'ripe', 'raw', 'bake', 'fry', 'boil', 'mix', 'chop', 'cut', 'slice', 'serve', 'plate', 'bowl', 'cup', 'fork', 'knife', 'spoon', 'chef', 'kitchen', 'oven', 'fire', 'heat', 'oil', 'soup', 'cake', 'pie', 'egg', 'milk', 'fish', 'beef', 'pork', 'rice', 'bean', 'corn', 'apple', 'berry'],
        'colors': ['color', 'colour', 'red', 'blue', 'green', 'yellow', 'black', 'white', 'pink', 'purple', 'orange', 'brown'],
        'nature': ['tree', 'plant', 'flower', 'forest', 'mountain', 'river', 'ocean', 'sky', 'earth', 'nature', 'outdoor', 'wild', 'wood', 'leaf', 'grass', 'rock', 'stone', 'water', 'lake', 'sea', 'beach', 'hill', 'field', 'park', 'cave', 'bird', 'wind', 'rain', 'snow', 'sun'],
        'sports': ['sport', 'game', 'play', 'team', 'ball', 'run', 'jump', 'race', 'win', 'compete', 'athletic'],
        'science': ['science', 'lab', 'test', 'study', 'research', 'experiment', 'theory', 'biology', 'chemistry', 'physics'],
        'music': ['music', 'song', 'sound', 'note', 'rhythm', 'melody', 'instrument', 'piano', 'guitar', 'drum', 'sing'],
        'travel': ['travel', 'trip', 'journey', 'road', 'path', 'city', 'country', 'map', 'explore', 'visit', 'tour', 'plane', 'train', 'car', 'bus', 'ship', 'boat', 'hotel', 'place', 'go', 'move', 'away', 'far', 'near', 'here', 'there'],
        'space': ['space', 'star', 'moon', 'sun', 'planet', 'galaxy', 'orbit', 'rocket', 'sky', 'cosmic', 'solar', 'lunar', 'mars', 'earth', 'venus', 'outer', 'void', 'dark', 'light', 'bright', 'far', 'vast', 'big', 'huge', 'high', 'up', 'fly', 'float'],
        'technology': ['tech', 'computer', 'machine', 'device', 'tool', 'gadget', 'robot', 'digital', 'cyber', 'electronic', 'electric', 'power', 'energy', 'motor', 'engine', 'gear', 'wire', 'cable', 'circuit', 'chip', 'code', 'data', 'info', 'web', 'net', 'online', 'smart', 'auto', 'fast', 'new', 'modern', 'high', 'tech'],
    }
    
    existing_topics = get_existing_deck_topics(target_file)
    available_topics = []
    
    print("\nAvailable topics with AI magic (not yet created):")
    counter = 1
    for topic in all_topics.keys():
        if topic.lower() not in existing_topics:
            print(f"{counter:2d}. {topic.title()}")
            available_topics.append(topic)
            counter += 1
    
    if not available_topics:
        print("   (All predefined topics have been created)")
    
    if existing_topics:
        print(f"\nAlready created topics: {', '.join(sorted(existing_topics))}")
    
    return available_topics

def show_available_topics_for_verify():
    """Display all predefined topics for verification."""
    topic_keywords = {
        'animals': ['animal', 'beast', 'creature', 'pet', 'wild', 'zoo', 'farm', 'dog', 'cat', 'bird', 'fish', 'mammal', 'reptile'],
        'food': ['eat', 'food', 'meal', 'cook', 'recipe', 'taste', 'flavor', 'dish', 'fruit', 'meat', 'bread', 'drink', 'sweet', 'sour', 'salt', 'spice', 'hot', 'cold', 'fresh', 'ripe', 'raw', 'bake', 'fry', 'boil', 'mix', 'chop', 'cut', 'slice', 'serve', 'plate', 'bowl', 'cup', 'fork', 'knife', 'spoon', 'chef', 'kitchen', 'oven', 'fire', 'heat', 'oil', 'soup', 'cake', 'pie', 'egg', 'milk', 'fish', 'beef', 'pork', 'rice', 'bean', 'corn', 'apple', 'berry'],
        'colors': ['color', 'colour', 'red', 'blue', 'green', 'yellow', 'black', 'white', 'pink', 'purple', 'orange', 'brown'],
        'nature': ['tree', 'plant', 'flower', 'forest', 'mountain', 'river', 'ocean', 'sky', 'earth', 'nature', 'outdoor', 'wild', 'wood', 'leaf', 'grass', 'rock', 'stone', 'water', 'lake', 'sea', 'beach', 'hill', 'field', 'park', 'cave', 'bird', 'wind', 'rain', 'snow', 'sun'],
        'sports': ['sport', 'game', 'play', 'team', 'ball', 'run', 'jump', 'race', 'win', 'compete', 'athletic'],
        'science': ['science', 'lab', 'test', 'study', 'research', 'experiment', 'theory', 'biology', 'chemistry', 'physics'],
        'music': ['music', 'song', 'sound', 'note', 'rhythm', 'melody', 'instrument', 'piano', 'guitar', 'drum', 'sing'],
        'travel': ['travel', 'trip', 'journey', 'road', 'path', 'city', 'country', 'map', 'explore', 'visit', 'tour', 'plane', 'train', 'car', 'bus', 'ship', 'boat', 'hotel', 'place', 'go', 'move', 'away', 'far', 'near', 'here', 'there'],
        'space': ['space', 'star', 'moon', 'sun', 'planet', 'galaxy', 'orbit', 'rocket', 'sky', 'cosmic', 'solar', 'lunar', 'mars', 'earth', 'venus', 'outer', 'void', 'dark', 'light', 'bright', 'far', 'vast', 'big', 'huge', 'high', 'up', 'fly', 'float'],
        'technology': ['tech', 'computer', 'machine', 'device', 'tool', 'gadget', 'robot', 'digital', 'cyber', 'electronic', 'electric', 'power', 'energy', 'motor', 'engine', 'gear', 'wire', 'cable', 'circuit', 'chip', 'code', 'data', 'info', 'web', 'net', 'online', 'smart', 'auto', 'fast', 'new', 'modern', 'high', 'tech'],
    }
    
    print("\nAvailable topics with AI magic:")
    topics = list(topic_keywords.keys())
    for i, topic in enumerate(topics, 1):
        print(f"{i:2d}. {topic.title()}")
    
    return topics

def make_deck():
    """Create a new themed deck by adding deck tags to related words."""
    script_dir = Path(__file__).parent
    dict_dir = script_dir.parent / "dictionary"
    target_file = dict_dir / "word_decks.xml"
    
    if not target_file.exists():
        print("✗ Error: word_decks.xml not found! Please run the initial processing first.")
        return
    
    # Show available topics that haven't been created yet
    available_topics = show_available_topics_for_make(target_file)
    print("\nYou can:")
    print("- Enter a number to select an available predefined topic")
    print("- Type any custom topic name")
    print("- Press Enter to cancel")
    
    user_input = input("\nEnter topic choice: ").strip()
    
    if not user_input:
        print("✗ Cancelled.")
        return
    
    # Check if user entered a number
    if user_input.isdigit():
        topic_index = int(user_input) - 1
        if 0 <= topic_index < len(available_topics):
            topic = available_topics[topic_index]
            print(f"Selected predefined topic: {topic.title()}")
        else:
            print("✗ Invalid topic number.")
            return
    else:
        # User entered a custom topic
        topic = user_input
        print(f"Using custom topic: {topic.title()}")
    
    try:
        print("Parsing XML file...")
        tree = ET.parse(target_file)
        root = tree.getroot()
        
        added_count = 0
        deck_tag = f"deck_{topic}"
        
        print(f"Processing entries for topic '{topic}' with tag '{deck_tag}'...")
        
        for entry in root.findall('entry'):
            word_element = entry.find('word')
            definition_element = entry.find('definition')
            
            if word_element is not None and word_element.text:
                word = word_element.text.strip()
                definition = definition_element.text if definition_element is not None else ""
                
                if is_word_related_to_topic(word, definition, topic):
                    # Check if deck tag already exists for this topic
                    existing_deck = entry.find(deck_tag)
                    if existing_deck is None:
                        # Add new deck element
                        deck_element = ET.SubElement(entry, deck_tag)
                        deck_element.text = 'All'
                        added_count += 1
        
        # Save updated XML
        print("Saving updated XML...")
        tree.write(target_file, encoding='utf-8', xml_declaration=True)
        print(f"✓ Added '{topic}' deck tag to {added_count} words.")
        
    except ET.ParseError as e:
        print(f"✗ XML parsing error: {e}")
        print("There's a corrupted entry or invalid character in the XML file.")
        print("Use option (X) to diagnose which entry is causing the issue.")
    except Exception as e:
        print(f"✗ Error creating deck: {e}")

def verify_deck():
    """Verify and clean up a deck by reviewing each entry."""
    script_dir = Path(__file__).parent
    dict_dir = script_dir.parent / "dictionary"
    target_file = dict_dir / "word_decks.xml"
    
    if not target_file.exists():
        print("✗ Error: word_decks.xml not found! Please run the initial processing first.")
        return
    
    # Show all available topics for verification
    available_topics = show_available_topics_for_verify()
    print("\nYou can:")
    print("- Enter a number to select a predefined topic")
    print("- Type any custom topic name")
    print("- Press Enter to cancel")
    
    user_input = input("\nEnter topic to verify: ").strip()
    
    if not user_input:
        print("✗ Cancelled.")
        return
    
    # Check if user entered a number
    if user_input.isdigit():
        topic_index = int(user_input) - 1
        if 0 <= topic_index < len(available_topics):
            topic = available_topics[topic_index]
            print(f"Verifying predefined topic: {topic.title()}")
        else:
            print("✗ Invalid topic number.")
            return
    else:
        # User entered a custom topic
        topic = user_input
        print(f"Verifying custom topic: {topic.title()}")
    
    try:
        print("Parsing XML file...")
        tree = ET.parse(target_file)
        root = tree.getroot()
        
        deck_tag = f"deck_{topic}"
        entries_with_deck = []
        
        # Find all entries with this deck tag
        for entry in root.findall('entry'):
            deck_element = entry.find(deck_tag)
            if deck_element is not None:
                entries_with_deck.append(entry)
        
        if not entries_with_deck:
            print(f"✗ No entries found with deck '{topic}'.")
            return
        
        print(f"\nFound {len(entries_with_deck)} entries with deck '{topic}'.")
        print("For each entry, press Y to keep, N to remove the deck tag, or Q to quit verification.")
        print("--------------------------------------------------")
        
        removed_count = 0
        
        for i, entry in enumerate(entries_with_deck, 1):
            word_element = entry.find('word')
            definition_element = entry.find('definition')
            
            word = word_element.text if word_element is not None else "Unknown"
            definition = definition_element.text if definition_element is not None else "No definition"
            
            print(f"\nEntry {i}/{len(entries_with_deck)}:")
            print(f"Word: {word}")
            print(f"Definition: {definition}")
            
            while True:
                choice = input("Keep this word in the deck? (Y/N/Q): ").strip().upper()
                if choice in ['Y', 'N', 'Q']:
                    break
                print("Please enter Y, N, or Q.")
            
            if choice == 'Q':
                print("Verification stopped.")
                break
            elif choice == 'N':
                # Remove the deck tag
                deck_element = entry.find(deck_tag)
                if deck_element is not None:
                    entry.remove(deck_element)
                    removed_count += 1
                    print(f"✓ Removed '{topic}' deck tag from '{word}'")
        
        # Save updated XML
        tree.write(target_file, encoding='utf-8', xml_declaration=True)
        print(f"\n✓ Verification complete. Removed deck tag from {removed_count} words.")
        
    except ET.ParseError as e:
        print(f"✗ XML parsing error: {e}")
        print("There's a corrupted entry or invalid character in the XML file.")
        print("Use option (X) to diagnose which entry is causing the issue.")
    except Exception as e:
        print(f"✗ Error verifying deck: {e}")

def diagnose_xml_error():
    """Diagnose which entry is causing XML parsing issues."""
    script_dir = Path(__file__).parent
    dict_dir = script_dir.parent / "dictionary"
    target_file = dict_dir / "word_decks.xml"
    
    if not target_file.exists():
        print("✗ word_decks.xml not found!")
        return
    
    print("Diagnosing XML parsing issue...")
    
    try:
        with open(target_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        print(f"Total lines in file: {len(lines)}")
        
        # Try to find the problematic area around line 60
        start_line = max(0, 55)  # Start a few lines before line 60
        end_line = min(len(lines), 65)  # End a few lines after
        
        print(f"\nContent around line 60 (lines {start_line+1}-{end_line}):")
        print("=" * 60)
        
        for i in range(start_line, end_line):
            line_num = i + 1
            line_content = lines[i].rstrip()
            print(f"{line_num:3d}: {line_content}")
        
        print("=" * 60)
        
        # Try to parse line by line to find the exact issue
        print("\nTrying to identify the problematic entry...")
        
        current_entry = []
        entry_start_line = 0
        
        for i, line in enumerate(lines):
            line_num = i + 1
            
            if '<entry>' in line:
                current_entry = [line]
                entry_start_line = line_num
            elif '</entry>' in line:
                current_entry.append(line)
                
                # Try to parse this entry
                entry_xml = ''.join(current_entry)
                try:
                    # Wrap in a root element for testing
                    test_xml = f"<root>{entry_xml}</root>"
                    ET.fromstring(test_xml)
                except ET.ParseError as e:
                    print(f"\n✗ PROBLEMATIC ENTRY found at lines {entry_start_line}-{line_num}:")
                    print(f"XML Error: {e}")
                    print("Entry content:")
                    print("-" * 40)
                    for entry_line in current_entry:
                        print(entry_line.rstrip())
                    print("-" * 40)
                    return
                
                current_entry = []
            elif current_entry:
                current_entry.append(line)
        
        print("Could not identify the specific problematic entry through line-by-line parsing.")
        
    except Exception as e:
        print(f"Error during diagnosis: {e}")

def show_menu():
    """Display and handle the main menu."""
    while True:
        print("\n========================================")
        print("Dictionary Deck Manager")
        print("========================================")
        print("(M) Make a Deck")
        print("(V) Verify a Deck") 
        print("(R) Regenerate word_decks.xml")
        print("(X) Diagnose XML Error")
        print("(D) Done")
        print("----------------------------------------")
        
        choice = input("Select an option: ").strip().upper()
        
        if choice == 'M':
            make_deck()
        elif choice == 'V':
            verify_deck()
        elif choice == 'R':
            regenerate_word_decks()
        elif choice == 'X':
            diagnose_xml_error()
        elif choice == 'D':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter M, V, R, X, or D.")

def regenerate_word_decks():
    """Delete and regenerate word_decks.xml file."""
    script_dir = Path(__file__).parent
    dict_dir = script_dir.parent / "dictionary"
    target_file = dict_dir / "word_decks.xml"
    
    if target_file.exists():
        print("This will delete your existing word_decks.xml and regenerate it.")
        print("WARNING: This will remove all custom deck tags you've created!")
        confirm = input("Are you sure? (yes/no): ").strip().lower()
        
        if confirm == 'yes':
            target_file.unlink()  # Delete the file
            print("✓ Deleted existing word_decks.xml")
            print("Regenerating...")
            success = process_dictionary()
            if success:
                print("✓ Successfully regenerated word_decks.xml with correct format!")
            else:
                print("✗ Failed to regenerate file.")
        else:
            print("✗ Cancelled.")
    else:
        print("word_decks.xml doesn't exist. Running initial processing...")
        success = process_dictionary()
        if success:
            print("✓ Successfully created word_decks.xml!")
        else:
            print("✗ Failed to create file.")

def main():
    """Main entry point."""
    # Check if word_decks.xml already exists
    script_dir = Path(__file__).parent
    dict_dir = script_dir.parent / "dictionary"
    target_file = dict_dir / "word_decks.xml"
    
    if target_file.exists():
        print("✓ word_decks.xml found - proceeding to menu (your existing decks are safe)")
        show_menu()
    else:
        print("Starting initial dictionary processing...")
        success = process_dictionary()
        
        if success:
            # Show the menu after successful processing
            show_menu()
        else:
            print("Dictionary processing failed. Please check the log file for details.")

if __name__ == "__main__":
    main()