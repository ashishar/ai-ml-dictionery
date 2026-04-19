import re

def fix_broken_unicode_math():
    filepath = 'src/data.js'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Map of broken unicode escapes (missing backslash or raw) to LaTeX
    unicode_map = {
        'u03c3': r'\\sigma',
        'u03bc': r'\\mu',
        'u03c0': r'\\pi',
        'u03b3': r'\\gamma',
        'u03b1': r'\\alpha',
        'u03b2': r'\\beta',
        'u0394': r'\\Delta',
        'u03a3': r'\\Sigma',
        'u03bb': r'\\lambda',
        'u03b7': r'\\eta',
        'u03b8': r'\\theta',
        'u03b5': r'\\epsilon',
        'u03c4': r'\\tau',
        'u03c6': r'\\phi',
        'u03c8': r'\\psi',
        'u03c9': r'\\omega'
    }

    # 1. Replace broken unicode strings with LaTeX equivalents
    for code, latex in unicode_map.items():
        # Match "u03c3" or "\u03c3" or " u03c3"
        content = re.sub(r'\\?u[0-9a-fA-F]{4}', lambda m, l=latex: l if m.group(0).endswith(code) else m.group(0), content)

    # 2. Specifically target the "u03c3(z)_i" pattern
    # It might have been turned into "\sigma(z)_i" by step 1
    # Now wrap any word starting with \ in $
    def wrap_math(match):
        text = match.group(0)
        # If it's already wrapped, don't wrap again
        # Actually, let's just use the previous logic but cleaner
        return f"${text}$"

    # Match anything like \sigma(z)_i or \mu_k
    content = re.sub(r'\\[a-zA-Z]+\(?[a-zA-Z0-9_,]*\)?(_[a-zA-Z0-9_{}:-]+)?', wrap_math, content)

    # 3. Clean up double $$
    content = content.replace('$$', '$')
    
    # 4. Final spacing fix
    content = re.sub(r'(\$[^\$]+\$)([a-zA-Z])', r'\1 \2', content)
    content = re.sub(r'([a-zA-Z])(\$[^\$]+\$)', r'\1 \2', content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_broken_unicode_math()
print("Surgical fix for broken Unicode math symbols applied.")
