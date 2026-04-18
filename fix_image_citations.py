import json

filepath = 'C:/Users/ashis/.gemini/antigravity/scratch/ai-dictionary-app/src/data.js'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

json_str = content.replace('export const dictionaryData = ', '').rstrip(';\n')
terms = json.loads(json_str)

for term in terms:
    cit = term.get('imageCitation', '').lower()
    
    # Check for Bing, DuckDuckGo, or our previous generic string
    if 'original research paper' in cit or 'bing.com' in cit or 'duckduckgo' in cit or 'th?id=' in cit:
        # Fallback systematically to exact resource links
        if term.get('resources') and term['resources'].get('papers') and len(term['resources']['papers']) > 0:
            term['imageCitation'] = term['resources']['papers'][0]['url']
        elif term.get('resources') and term['resources'].get('tutorials') and len(term['resources']['tutorials']) > 0:
            term['imageCitation'] = term['resources']['tutorials'][0]['url']
        else:
            term['imageCitation'] = f"https://en.wikipedia.org/wiki/{term['title'].replace(' ', '_')}"

with open(filepath, 'w', encoding='utf-8') as f:
    f.write('export const dictionaryData = ')
    f.write(json.dumps(terms, indent=2))
    f.write(';\n')

print("Image citations correctly mapped to explicit resource URLs.")
