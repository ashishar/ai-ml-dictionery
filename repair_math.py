import json
import re

def repair_math():
    filepath = 'src/data.js'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Clean up the export string to parse as JSON
    json_str = content.replace('export const dictionaryData = ', '').rstrip(';\n')
    data = json.loads(json_str)

    # Specific repairs for malformed sequences
    # Using lambda to avoid backreference/escape issues in re.sub
    repairs = [
        (r'V\^?\$?\\pi\s?\$?\(s\)', r'$V^\pi(s)$'),
        (r'E_?\$?\\pi\s?\$?', r'$E_\pi$'),
        (r'\$?\s?r_{t\+k\+1}\s?\$?', r' $r_{t+k+1}$ '),
        (r'max Q\(s\',a\'\)', r'$\max_{a\'} Q(s\',a\')$'),
        (r'Q\(s,a\)', r'$Q(s,a)$'),
        (r'\$\s?\\pi\s?\$', r'$\pi$'),
        (r'\$\s?\\gamma\s?\$', r'$\gamma$'),
        (r'\bpi\b', r'$\pi$'),
        (r'\balpha\b', r'$\alpha$'),
        (r'\bgamma\b', r'$\gamma$'),
        (r'\bsigma\b', r'$\sigma$'),
        (r'\bmu\b', r'$\mu$'),
        (r'\bepsilon\b', r'$\epsilon$'),
        (r'\bbeta\b', r'$\beta$'),
        (r'd iscount', 'discount'),
        (r'represe n ts', 'represents'),
        (r'followi n g', 'following'),
        (r'st a te', 'state'),
        (r'v a lue', 'value')
    ]

    for term in data:
        sd = term.get("structuredDefinition", {})
        if "equationVars" in sd:
            text = sd["equationVars"]
            
            # Apply all repairs
            for pattern, replacement in repairs:
                text = re.sub(pattern, lambda m, r=replacement: r, text, flags=re.IGNORECASE)

            # Cleanup spacing
            text = re.sub(r'(\$[^\$]+\$)([a-zA-Z])', r'\1 \2', text)
            text = re.sub(r'([a-zA-Z])(\$[^\$]+\$)', r'\1 \2', text)
            
            # Remove redundant parentheticals
            text = text.replace('($\gamma$)', '')
            text = text.replace('($\alpha$)', '')
            text = text.replace('($\pi$)', '')
            text = text.replace('($\epsilon$)', '')
            
            # Clean up double $
            text = text.replace('$$', '$')
            
            # Ensure space after symbol at start of sentence
            text = re.sub(r'\.\s*(\$[^\$]+\$)([a-zA-Z])', r'. \1 \2', text)

            text = text.replace('  ', ' ')
            text = text.strip()
            
            sd["equationVars"] = text

    # Save the updated data
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('export const dictionaryData = ' + json.dumps(data, indent=2) + ';')

repair_math()
print("Successfully repaired malformed math and text sequences with safe replacements.")
