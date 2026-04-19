import re

def fix_unicode_to_latex():
    filepath = 'src/data.js'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Map of Unicode Greek characters to LaTeX names
    greek_map = {
        '\u03c3': r'\\sigma',
        '\u03bc': r'\\mu',
        '\u03c0': r'\\pi',
        '\u03b3': r'\\gamma',
        '\u03b1': r'\\alpha',
        '\u03b2': r'\\beta',
        '\u0394': r'\\Delta',
        '\u03a3': r'\\Sigma',
        '\u03bb': r'\\lambda',
        '\u03b7': r'\\eta',
        '\u03b8': r'\\theta',
        '\u03b5': r'\\epsilon',
        '\u03c4': r'\\tau',
        '\u03c6': r'\\phi',
        '\u03c8': r'\\psi',
        '\u03c9': r'\\omega',
        '\u03a6': r'\\Phi',
        '\u039b': r'\\Lambda'
    }

    def clean_ev(match):
        text = match.group(1)
        
        # 1. Replace Unicode characters with LaTeX names
        for char, latex in greek_map.items():
            text = text.replace(char, latex)
            
        # 2. Strip existing $ to re-wrap correctly
        text = text.replace('$', '')
        
        # 3. Wrap any word starting with \ or containing _ or ^ or { in $
        # We target blocks of math
        # Pattern: Starts with \ or a letter, contains math chars, ends with space or boundary
        # Specifically handle \sigma(z)_i
        text = re.sub(r'(\\[a-zA-Z]+(?:\([a-zA-Z0-9_,]*\))?(_[a-zA-Z0-9_{}:-]+)?)', r'$\1$', text)
        
        # 4. Wrap subscripts like z_i, w_t
        text = re.sub(r'\b([a-zA-Z][a-zA-Z0-9_{}:-]*_[a-zA-Z0-9_{}:-]*)\b', r'$\1$', text)
        
        # 5. Fix remaining single letter variables
        text = re.sub(r'\b([a-zA-HJ-Z])\b(?=\s+(?:is|denotes|represents|refers|stands for))', r'$\1$', text)
        text = re.sub(r'\bi\b(?=\s+is)', r'$i$', text)
        
        # 6. Cleanup spacing and double $$
        text = text.replace('$$', '$')
        text = re.sub(r'(\$[^\$]+\$)([a-zA-Z])', r'\1 \2', text)
        text = re.sub(r'([a-zA-Z])(\$[^\$]+\$)', r'\1 \2', text)
        text = text.replace('  ', ' ')
        
        return f'"equationVars": "{text}"'

    new_content = re.sub(r'"equationVars": "(.*?)"', clean_ev, content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

fix_unicode_to_latex()
print("Surgical Unicode-to-LaTeX replacement applied.")
