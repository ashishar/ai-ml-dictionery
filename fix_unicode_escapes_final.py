import re

def fix_unicode_escapes_final():
    filepath = 'src/data.js'
    # We read as text, and Python will interpret \u03c3 as the character σ
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Character map
    char_to_latex = {
        '\u03c3': '\\sigma',
        '\u03bc': '\\mu',
        '\u03c0': '\\pi',
        '\u03b3': '\\gamma',
        '\u03b1': '\\alpha',
        '\u03b2': '\\beta',
        '\u0394': '\\Delta',
        '\u03a3': '\\Sigma',
        '\u03bb': '\\lambda',
        '\u039b': '\\Lambda'
    }

    def process_ev(match):
        text = match.group(1)
        
        # 1. Replace characters
        for char, latex in char_to_latex.items():
            text = text.replace(char, latex)
            
        # 2. Re-wrap math
        text = text.replace('$', '')
        
        # Wrap anything starting with \ or containing _ or ^
        # and ensure subscripts are inside
        # Specifically target \sigma(z)_i
        text = re.sub(r'(\\[a-zA-Z]+(?:\([^\)]*\))?(_[a-zA-Z0-9_{}:-]+)?)', r'$\1$', text)
        
        # Wrap plain subscripts
        text = re.sub(r'\b([a-zA-Z][a-zA-Z0-9_{}:-]*_[a-zA-Z0-9_{}:-]*)\b', r'$\1$', text)
        
        # Wrap single letters followed by is/denotes
        text = re.sub(r'\b([a-zA-HJ-Z])\b(?=\s+(?:is|denotes|represents))', r'$\1$', text)
        text = re.sub(r'\bi\b(?=\s+is)', r'$i$', text)
        
        # Clean up
        text = text.replace('$$', '$')
        text = re.sub(r'(\$[^\$]+\$)([a-zA-Z])', r'\1 \2', text)
        text = re.sub(r'([a-zA-Z])(\$[^\$]+\$)', r'\1 \2', text)
        
        return f'"equationVars": "{text}"'

    new_content = re.sub(r'"equationVars": "(.*?)"', process_ev, content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

fix_unicode_escapes_final()
print("Final Unicode-to-LaTeX fix applied.")
