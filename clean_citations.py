import json
import re

def clean_image_citations():
    filepath = 'src/data.js'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # We process the text directly to avoid JSON escape issues
    def clean_citation(match):
        citation_text = match.group(1)
        
        # 1. Remove leading hex-like strings (e.g., A538B05E...) followed by hyphen or space
        # Pattern: 8+ characters of hex/numbers followed by optional space/hyphen
        citation_text = re.sub(r'^[A-Fa-f0-9]{8,}\s*[-–—]?\s*', '', citation_text)
        
        # 2. Remove leading long numbers (e.g., 23060859)
        citation_text = re.sub(r'^\d{6,}\s*', '', citation_text)
        
        # 3. Remove trailing hashes or indexes if they look like "Title 82C771Fb25D7"
        citation_text = re.sub(r'\s+[A-Fa-f0-9]{8,}$', '', citation_text)
        
        # 4. Clean up any resulting double spaces or leading/trailing hyphens
        citation_text = citation_text.strip(' -–—')
        
        return f'"imageCitation": "{citation_text}"'

    # Match "imageCitation": "..."
    new_content = re.sub(r'"imageCitation": "(.*?)"', clean_citation, content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

clean_image_citations()
print("Surgical cleaning of imageCitation fields completed.")
