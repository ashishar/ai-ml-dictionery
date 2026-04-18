import json
import re
from urllib.parse import urlparse, unquote

filepath = 'C:/Users/ashis/.gemini/antigravity/scratch/ai-dictionary-app/src/data.js'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

json_str = content.replace('export const dictionaryData = ', '').rstrip(';\n')
terms = json.loads(json_str)

for term in terms:
    cit = term.get('imageCitation', '')
    if 'Bing (' in cit:
        match = re.search(r'Bing \((https?://[^)]+)\)', cit)
        if match:
            url = match.group(1)
            parsed = urlparse(url)
            domain = parsed.netloc.replace('www.', '')
            
            # Create a pretty title from the URL path or query
            if 'title=' in url:
                title_part = url.split('title=')[-1].split('&')[0]
                pretty_title = unquote(title_part).replace('_', ' ')
            else:
                path_parts = [p for p in parsed.path.split('/') if p]
                if path_parts:
                    last_part = path_parts[-1]
                    if '.' in last_part and len(last_part) > 4:
                        last_part = last_part.split('.')[0]
                    pretty_title = unquote(last_part).replace('-', ' ').replace('_', ' ').title()
                else:
                    pretty_title = f"{term['title']} Resource"
            
            if len(pretty_title) < 4 or re.search(r'^\d+$', pretty_title):
                pretty_title = f"{domain} Article"
                
            term['imageCitation'] = f"{pretty_title.strip()} - {url}"

with open(filepath, 'w', encoding='utf-8') as f:
    f.write('export const dictionaryData = ')
    f.write(json.dumps(terms, indent=2))
    f.write(';\n')

print("Cleaned Bing citations successfully.")
