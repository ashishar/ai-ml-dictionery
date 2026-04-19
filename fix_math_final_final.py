import re

def fix_math_final_final():
    filepath = 'src/data.js'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    def clean_ev(match):
        text = match.group(1)
        
        # 1. Strip ALL existing $ from equationVars to start clean
        text = text.replace('$', '')
        
        # 2. Wrap subscripts like w_t, h_t, w_{1:t-1}
        # Match word characters or braces or colons around _
        text = re.sub(r'\b([a-zA-Z][a-zA-Z0-9_{}:-]*_[a-zA-Z0-9_{}:-]*)\b', r'$\1$', text)
        
        # 3. Wrap P(...) blocks
        text = re.sub(r'\bP\([a-zA-Z0-9_|:_{}\s-]+\)', r'$\0$', text)
        
        # 4. Wrap single letter variables followed by is/denotes
        text = re.sub(r'\b([a-z]|[A-HJ-Z])\b(?=\s+(?:is|denotes|represents|refers|stands for))', r'$\1$', text)
        
        # 5. Fix | to \mid inside $
        text = re.sub(r'\$([^\$]+\|[^\$]+)\$', lambda m: "$" + m.group(1).replace('|', r' \mid ') + "$", text)
        
        # 6. Clean up double $$
        text = text.replace('$$', '$')
        text = text.replace('  ', ' ')
        
        return f'"equationVars": "{text}"'

    new_content = re.sub(r'"equationVars": "(.*?)"', clean_ev, content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

fix_math_final_final()
print("Final surgical fix for math subscripts and probability notation applied.")
