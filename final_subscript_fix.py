import re

def final_subscript_fix():
    filepath = 'src/data.js'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    def fix_ev(match):
        text = match.group(1)
        
        # 1. Clean up messy nesting like $...$ inside $...$
        # If we have something like $P($...$)$, remove the internal ones
        text = re.sub(r'(\$[^\$]*)\$([^\$]+)\$([^\$]*\$)', r'\1\2\3', text)
        
        # 2. Fix subscripts that were partially wrapped
        # e.g., $w_{1:t-1$}$ -> $w_{1:t-1}$
        text = text.replace('$}', '}')
        text = text.replace('${', '{')
        
        # 3. Handle specific patterns
        text = text.replace('\mid', '\\mid')
        
        # 4. Final spacing cleanup
        text = text.replace('$$', '$')
        text = text.replace('  ', ' ')
        
        return f'"equationVars": "{text}"'

    new_content = re.sub(r'"equationVars": "(.*?)"', fix_ev, content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

final_subscript_fix()
print("Final subscript formatting polish applied.")
