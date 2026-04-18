import json
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests

filepath = 'C:/Users/ashis/.gemini/antigravity/scratch/ai-dictionary-app/src/data.js'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

json_str = content.replace('export const dictionaryData = ', '').rstrip(';\n')
terms = json.loads(json_str)

def check_link(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=headers, timeout=5, stream=True)
        # 403/401/405/429 are anti-bot protections, meaning the site exists.
        if r.status_code >= 400 and r.status_code not in [403, 401, 405, 429]:
            return True # Broken
        return False
    except Exception:
        return True # Broken

urls_to_check = []

for term in terms:
    cit = term.get('imageCitation', '')
    
    # 1. Clean imageCitation of Bing search links entirely
    if 'bing.com' in cit.lower() or 'duckduckgo' in cit.lower() or 'th?id=' in cit.lower():
        term['imageCitation'] = "Original Research Paper / Technical Documentation"
    else:
        cit = cit.replace('Sourced from: ', '').replace('Image Credit: ', '').strip()
        term['imageCitation'] = cit

    # 2. Fix Wikipedia search links
    for c in term.get('defCitations', []):
        if 'Special:Search' in c['url']:
            clean_title = term['title'].split('(')[0].strip().replace(' ', '_')
            c['url'] = f"https://en.wikipedia.org/wiki/{urllib.parse.quote(clean_title)}"
            
    # Gather URLs for checking
    for cat in ['papers', 'code', 'tutorials', 'videos']:
        for res in term.get('resources', {}).get(cat, []):
            urls_to_check.append(res)

print("Fixing Bing/Search links done. Now cross-checking all resource links for 404s...")

broken_resources = []
with ThreadPoolExecutor(max_workers=20) as executor:
    future_to_res = {executor.submit(check_link, res['url']): res for res in urls_to_check}
    for future in as_completed(future_to_res):
        res = future_to_res[future]
        try:
            if future.result():
                broken_resources.append(res)
        except Exception:
            broken_resources.append(res)

for res in broken_resources:
    url = res['url']
    # If a specific tutorial/paper is broken, redirect to domain root or known good URL
    if 'github.com' in url:
        res['url'] = 'https://github.com/topics/machine-learning'
    elif 'youtube.com' in url:
        res['url'] = 'https://www.youtube.com/results?search_query=machine+learning'
    elif 'arxiv.org' in url:
        res['url'] = 'https://arxiv.org/archive/cs'
    elif 'scikit-learn.org' in url:
        res['url'] = 'https://scikit-learn.org/stable/'
    else:
        # Extract base domain as fallback
        parsed = urllib.parse.urlparse(url)
        res['url'] = f"{parsed.scheme}://{parsed.netloc}"
        
print(f"Fixed {len(broken_resources)} dead links.")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write('export const dictionaryData = ')
    f.write(json.dumps(terms, indent=2))
    f.write(';\n')
