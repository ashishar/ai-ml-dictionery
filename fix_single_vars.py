import json
import re

def fix_single_vars():
    filepath = 'src/data.js'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    def replace_single_vars(match):
        text = match.group(1)
        
        # Match single letters (a-z, A-Z except A, I, The) followed by "is"
        # We also match x_i, y_i, etc.
        
        # 1. Match x_i, w_i, etc.
        text = re.sub(r'\b([a-zA-Z][a-zA-Z0-9]*_[a-zA-Z0-9]+)\b(?!\$)', r'$\1$', text)
        
        # 2. Match single letters followed by "is", "denotes", etc.
        # Avoid common words
        text = re.sub(r'\b([a-z]|[A-HJ-Z])\b(?=\s+(?:is|denotes|represents|refers|stands for))', r'$\1$', text)

        # 3. Clean up double $$
        text = text.replace('$$', '$')
        
        # 4. Spacing
        text = re.sub(r'(\$[^\$]+\$)([a-zA-Z0-9])', r'\1 \2', text)
        text = re.sub(r'([a-zA-Z0-9])(\$[^\$]+\$)', r'\1 \2', text)
        
        return f'"equationVars": "{text}"'

    new_content = re.sub(r'"equationVars": "(.*?)"', replace_single_vars, content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

fix_single_vars()
print("Surgical single-letter variable replacement applied to equationVars.")
