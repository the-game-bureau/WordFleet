import xml.etree.ElementTree as ET
import shutil
import os

def process_dictionary():
   source_file = "dictionary/dictionary.xml"
   target_file = "dictionary/word_decks.xml"
   
   if not os.path.exists(source_file):
       print("Error: dictionary.xml not found!")
       return
   
   shutil.copy2(source_file, target_file)
   print("Copied dictionary.xml to word_decks.xml")
   
   try:
       tree = ET.parse(target_file)
       root = tree.getroot()
       
       entries_to_remove = []
       
       for entry in root.findall('entry'):
           word_element = entry.find('word')
           if word_element is not None:
               word = word_element.text.strip()
               
               is_valid_length = 2 <= len(word) <= 5
               is_only_letters = word.isalpha()
               
               if not (is_valid_length and is_only_letters):
                   entries_to_remove.append(entry)
               else:
                   deck_element = ET.SubElement(entry, 'deck:All')
                   deck_element.text = 'All'
       
       for entry in entries_to_remove:
           root.remove(entry)
       
       tree.write(target_file, encoding='utf-8', xml_declaration=True)
       
       print("Processing complete!")
       print(f"Removed {len(entries_to_remove)} entries")
       print("Added deck:All to remaining entries")
       
   except Exception as e:
       print(f"Error: {e}")

if __name__ == "__main__":
   process_dictionary()