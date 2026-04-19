import json
import re

def clean_image_citations_robust():
    filepath = 'src/data.js'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    def clean_citation(match):
        full_text = match.group(1)
        
        # Split into title and URL
        if ' - http' in full_text:
            parts = full_text.split(' - http', 1)
            title = parts[0]
            url = 'http' + parts[1]
        else:
            title = full_text
            url = ''

        # Clean title
        # 1. Remove long hex/numeric strings (8+ chars) that are separated by space or boundary
        # We use a pattern that looks for strings containing both numbers and letters, or very long numbers
        title = re.sub(r'\b[A-Fa-f0-9]*[0-9][A-Fa-f0-9]*[A-Fa-f][A-Fa-f0-9]*\b', '', title) # Hex with at least one digit and one letter
        title = re.sub(r'\b\d{8,}\b', '', title) # Long numeric strings
        
        # 2. Clean up specific artifacts like "A Revolution In Computer Vision 82C771Fb25D7"
        # The above hex regex should catch 82C771Fb25D7
        
        # 3. Final cleanup of spacing and punctuation
        title = re.sub(r'\s+', ' ', title).strip(' -–—,')
        
        if url:
            return f'"imageCitation": "{title} - {url}"' if title else f'"imageCitation": "{url}"'
        else:
            return f'"imageCitation": "{title}"'

    new_content = re.sub(r'"imageCitation": "(.*?)"', clean_citation, content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

clean_image_citations_robust()
print("Robust cleaning of imageCitation fields completed.")
