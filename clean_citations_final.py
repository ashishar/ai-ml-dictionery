import json
import re

def clean_image_citations_final():
    filepath = 'src/data.js'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    json_str = content.replace('export const dictionaryData = ', '').rstrip(';\n')
    data = json.loads(json_str)

    for term in data:
        citation = term.get("imageCitation", "")
        if not citation:
            continue
            
        # Split into title and URL
        if ' - http' in citation:
            parts = citation.split(' - http', 1)
            title = parts[0]
            url = 'http' + parts[1]
        elif citation.startswith('http'):
            title = ''
            url = citation
        else:
            title = citation
            url = ''

        # Clean title
        # Remove hex/numeric strings (8+ chars)
        title = re.sub(r'\b[A-Fa-f0-9]*[0-9][A-Fa-f0-9]*[A-Fa-f][A-Fa-f0-9]*\b', '', title)
        title = re.sub(r'\b\d{8,}\b', '', title)
        
        # Clean up punctuation and spacing
        title = re.sub(r'\s+', ' ', title).strip(' -–—,')
        
        # Fallback to term title if empty
        if not title:
            title = f"{term['title']} Diagram"
            
        if url:
            term["imageCitation"] = f"{title} - {url}"
        else:
            term["imageCitation"] = title

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('export const dictionaryData = ' + json.dumps(data, indent=2) + ';')

clean_image_citations_final()
print("Final cleaning of imageCitation fields completed with fallbacks.")
