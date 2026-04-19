import re

def clean_citations_surgical():
    filepath = 'src/data.js'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    def clean_match(match):
        citation = match.group(1)
        
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
        
        # We don't have easy access to term title here without more complex regex, 
        # so we'll just return the URL if title is empty, or a generic placeholder.
        if not title and url:
            return f'"imageCitation": "{url}"'
        
        if url:
            return f'"imageCitation": "{title} - {url}"'
        else:
            return f'"imageCitation": "{title}"'

    new_content = re.sub(r'"imageCitation": "(.*?)"', clean_match, content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

clean_citations_surgical()
print("Surgical cleaning of imageCitation fields completed.")
