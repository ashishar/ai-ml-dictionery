import re

def fix_literal_unicode_escapes():
    filepath = 'src/data.js'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Literal strings to LaTeX
    literal_map = {
        'u03c3': '\\\\sigma',
        'u03bc': '\\\\mu',
        'u03c0': '\\\\pi',
        'u03b3': '\\\\gamma',
        'u03b1': '\\\\alpha',
        'u03b2': '\\\\beta',
        'u0394': '\\\\Delta',
        'u03a3': '\\\\Sigma',
        'u03bb': '\\\\lambda',
        'u039b': '\\\\Lambda',
        'u03b5': '\\\\epsilon',
        'u03b7': '\\\\eta',
        'u03b8': '\\\\theta',
        'u03c4': '\\\\tau',
        'u03c6': '\\\\phi',
        'u03c8': '\\\\psi',
        'u03c9': '\\\\omega'
    }

    def process_ev(match):
        text = match.group(1)
        
        # 1. Replace literal \u03c3 etc.
        # We handle both \u03c3 and u03c3
        for code, latex in literal_map.items():
            text = text.replace('\\' + code, latex)
            text = text.replace(code, latex)
            
        # 2. Cleanup existing $
        text = text.replace('$', '')
        
        # 3. Wrap math blocks
        # Target anything starting with \
        text = re.sub(r'(\\[a-zA-Z]+(?:\([^\)]*\))?(_[a-zA-Z0-9_{}:-]+)?)', r'$\1$', text)
        
        # Target subscripts
        text = re.sub(r'\b([a-zA-Z][a-zA-Z0-9_{}:-]*_[a-zA-Z0-9_{}:-]*)\b', r'$\1$', text)
        
        # Target single letters
        text = re.sub(r'\b([a-zA-HJ-Z])\b(?=\s+(?:is|denotes|represents))', r'$\1$', text)
        text = re.sub(r'\bi\b(?=\s+is)', r'$i$', text)
        
        # 4. Final cleanup
        text = text.replace('$$', '$')
        text = re.sub(r'(\$[^\$]+\$)([a-zA-Z])', r'\1 \2', text)
        text = re.sub(r'([a-zA-Z])(\$[^\$]+\$)', r'\1 \2', text)
        
        return f'"equationVars": "{text}"'

    new_content = re.sub(r'"equationVars": "(.*?)"', process_ev, content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

fix_literal_unicode_escapes()
print("Surgical fix for literal Unicode escape strings applied.")
