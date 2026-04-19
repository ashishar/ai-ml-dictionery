import json
import re

def fix_smashed_math_v2():
    filepath = 'src/data.js'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    def clean_math_errors(match):
        text = match.group(1)
        
        # 1. Strip ALL existing $
        text = text.replace('$', '')
        
        # 2. Fix functions with parentheses: f(x), g(f(x)), g()
        # We look for letters followed by parentheses
        text = re.sub(r'\b[a-zA-Z][a-zA-Z0-9_]*\([a-zA-Z0-9_(),\s]*\)', r'$\0$', text)
        
        # 3. Fix subscripts: x_i, h_{t-1}
        text = re.sub(r'\b[a-zA-Z][a-zA-Z0-9_]*_[a-zA-Z0-9_{}:-]+\b', r'$\0$', text)

        # 4. Fix single variables followed by "is", "represents", etc.
        # But skip common English words like "a", "i" at start of sentence
        text = re.sub(r'\b([a-zA-HJ-Z])\b(?=\s+(?:is|denotes|represents|refers|stands for))', r'$\1$', text)
        # Special case for 'i' if followed by 'is' (unlikely to be the word 'I')
        text = re.sub(r'\bi\b(?=\s+is)', r'$i$', text)

        # 5. Fix common Greek names
        greek_names = ['alpha', 'beta', 'gamma', 'delta', 'epsilon', 'mu', 'sigma', 'tau', 'phi', 'omega', 'pi']
        for name in greek_names:
            text = re.sub(r'\b' + name + r'\b(?=\s+(?:is|denotes|represents))', r'$\\' + name + r'$', text)

        # 6. Cleanup spacing around $
        # Remove spaces immediately inside $
        text = re.sub(r'\$\s+', '$', text)
        text = re.sub(r'\s+\$', '$', text)
        
        # Ensure space after $ if followed by a word
        text = re.sub(r'(\$[^\$]+\$)([a-zA-Z])', r'\1 \2', text)
        # Ensure space before $ if preceded by a word
        text = re.sub(r'([a-zA-Z])(\$[^\$]+\$)', r'\1 \2', text)
        
        # 7. Final double check for double $$
        text = text.replace('$$', '$')
        text = text.replace('  ', ' ')
        
        return f'"equationVars": "{text}"'

    new_content = re.sub(r'"equationVars": "(.*?)"', clean_math_errors, content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

fix_smashed_math_v2()
print("V2 Surgical fix for smashed math applied.")
