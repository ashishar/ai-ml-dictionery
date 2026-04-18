import json
import time
import os
import requests
from duckduckgo_search import DDGS
from duckduckgo_search.exceptions import RatelimitException

filepath = 'C:/Users/ashis/.gemini/antigravity/scratch/ai-dictionary-app/src/data.js'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

json_str = content.replace('export const dictionaryData = ', '').rstrip(';\n')
terms = json.loads(json_str)

img_dir = 'C:/Users/ashis/.gemini/antigravity/scratch/ai-dictionary-app/public/images'
os.makedirs(img_dir, exist_ok=True)
ddgs = DDGS()

print(f"Starting to fetch unique technical diagrams for {len(terms)} terms...")

for idx, term in enumerate(terms):
    paper_title = term['resources']['papers'][0]['title'].split('(')[0].strip()
    
    query = f"{term['title']} {paper_title} architecture technical diagram graph"
    print(f"[{idx+1}/{len(terms)}] Searching: {term['title']}")
    
    success = False
    retries = 3
    
    for attempt in range(retries):
        if success:
            break
        try:
            results = list(ddgs.images(query, max_results=5))
            if not results:
                results = list(ddgs.images(f"{term['title']} machine learning architecture diagram", max_results=5))
                
            for res in results:
                img_url = res['image']
                try:
                    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
                    response = requests.get(img_url, headers=headers, timeout=5)
                    
                    if response.status_code == 200 and len(response.content) > 5000:
                        filename = f"{term['title'].replace(' ', '_').replace('(', '').replace(')', '').replace('/', '').lower()}.jpg"
                        save_path = os.path.join(img_dir, filename)
                        
                        with open(save_path, 'wb') as img_f:
                            img_f.write(response.content)
                        
                        term['image'] = f"/images/{filename}"
                        
                        source = res.get('source', '')
                        url = res.get('url', '')
                        term['imageCitation'] = f"Sourced from: {source} ({url})"
                        
                        success = True
                        print(f"  -> Downloaded: {filename}")
                        break
                except Exception:
                    continue
        except RatelimitException:
            print("  -> Rate limited! Sleeping for 10 seconds...")
            time.sleep(10)
        except Exception as e:
            print(f"  -> Search error: {e}")
            
    if not success:
        print(f"  -> Could not find/download image for {term['title']}")
        
    time.sleep(2.5)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write('export const dictionaryData = ')
    f.write(json.dumps(terms, indent=2))
    f.write(';\n')

print("Finished updating all terms with unique technical diagrams.")
