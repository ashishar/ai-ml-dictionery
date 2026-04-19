import re

def fix_smashed_math_v3():
    filepath = 'src/data.js'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    def clean_math_errors(match):
        text = match.group(1)
        
        # 1. Strip ALL existing $
        text = text.replace('$', '')
        
        # 2. Fix functions like f(x), g(f(x)), g()
        # Pattern: Letters followed by ( and anything until balanced )
        # Simplified: Letters followed by ( ... )
        text = re.sub(r'\b[a-zA-Z][a-zA-Z0-9_]*\([^\)]*\)', lambda m: "$" + m.group(0) + "$", text)
        
        # 3. Fix subscripts: x_i, h_{t-1}
        text = re.sub(r'\b[a-zA-Z][a-zA-Z0-9_]*_[a-zA-Z0-9_{}:-]+\b', lambda m: "$" + m.group(0) + "$", text)

        # 4. Fix single variables followed by "is", "represents", etc.
        text = re.sub(r'\b([a-zA-HJ-Z])\b(?=\s+(?:is|denotes|represents|refers|stands for))', lambda m: "$" + m.group(1) + "$", text)
        text = re.sub(r'\bi\b(?=\s+is)', lambda m: "$i$", text)

        # 5. Fix common Greek names
        greek_names = ['alpha', 'beta', 'gamma', 'delta', 'epsilon', 'mu', 'sigma', 'tau', 'phi', 'omega', 'pi']
        for name in greek_names:
            text = re.sub(r'\b' + name + r'\b(?=\s+(?:is|denotes|represents))', lambda m, n=name: "$\\" + n + "$", text)

        # 6. Cleanup spacing around $
        text = re.sub(r'\$\s+', '$', text)
        text = re.sub(r'\s+\$', '$', text)
        
        # Ensure space after $ if followed by a word (and not a period)
        text = re.sub(r'(\$[^\$]+\$)([a-zA-Z])', r'\1 \2', text)
        # Ensure space before $ if preceded by a word
        text = re.sub(r'([a-zA-Z])(\$[^\$]+\$)', r'\1 \2', text)
        
        # 7. Final double check for double $$
        text = text.replace('$$', '$')
        text = text.replace('  ', ' ')
        
        return '"equationVars": "' + text + '"'

    new_content = re.sub(r'"equationVars": "(.*?)"', clean_math_errors, content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

fix_smashed_math_v3()
print("V3 Surgical fix for smashed math applied with lambda.")
