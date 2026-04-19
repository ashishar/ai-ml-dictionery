import json
import re

def find_math_issues():
    filepath = 'src/data.js'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    json_str = content.replace('export const dictionaryData = ', '').rstrip(';\n')
    data = json.loads(json_str)

    greek_unicode = r'[\u0370-\u03ff\u1f00-\u1fff]'
    
    issues = []
    for term in data:
        ev = term.get("structuredDefinition", {}).get("equationVars", "")
        if re.search(greek_unicode, ev) or re.search(r'_[a-zA-Z0-9]', ev) or re.search(r'\^[a-zA-Z0-9]', ev):
            # Only report if not wrapped in $
            if not re.search(r'\$.*?\$', ev):
                issues.append((term["title"], ev))
    
    for title, ev in issues:
        print(f"ISSUE in {title}: {ev}")

find_math_issues()
