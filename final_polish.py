import json
import re

def final_polish_math():
    filepath = 'src/data.js'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    json_str = content.replace('export const dictionaryData = ', '').rstrip(';\n')
    data = json.loads(json_str)

    # Unicode to LaTeX wrapped in $
    greek_map = {
        '\u03c0': r'$\pi$', '\u03b3': r'$\gamma$', '\u03b1': r'$\alpha$', '\u03b5': r'$\epsilon$',
        '\u03bc': r'$\mu$', '\u03c3': r'$\sigma$', '\u03b2': r'$\beta$', '\u0394': r'$\Delta$',
        '\u03a3': r'$\Sigma$', '\u039b': r'$\Lambda$', '\u03b7': r'$\eta$', '\u03b8': r'$\theta$',
        '\u03bb': r'$\lambda$', '\u03c1': r'$\rho$', '\u03c4': r'$\tau$', '\u03c6': r'$\phi$',
        '\u03c8': r'$\psi$', '\u03c9': r'$\omega$', '\u03f5': r'$\epsilon$'
    }

    # Complex blocks that often appear as plain text in the remaining terms
    complex_fixes = [
        (r'\bw\b(?=\s+is)', r'$w$'),
        (r'\bb\b(?=\s+is)', r'$b$'),
        (r'\bx\b(?=\s+is)', r'$x$'),
        (r'\by\b(?=\s+is)', r'$y$'),
        (r'\bn\b(?=\s+is)', r'$n$'),
        (r'\bk\b(?=\s+is)', r'$k$'),
        (r'\bi\b(?=\s+is)', r'$i$'),
        (r'\bj\b(?=\s+is)', r'$j$'),
        (r'\bE\b(?=\s+is)', r'$E$'),
        (r'\bL\b(?=\s+is)', r'$L$'),
        (r'\bX\b(?=\s+is)', r'$X$'),
        (r'\bY\b(?=\s+is)', r'$Y$'),
        (r'\bP\b(?=\s+is)', r'$P$'),
        (r'\bW\b(?=\s+is)', r'$W$')
    ]

    for term in data:
        sd = term.get("structuredDefinition", {})
        if "equationVars" in sd:
            text = sd["equationVars"]
            
            # 1. Replace Unicode Greek with wrapped LaTeX
            for char, latex in greek_map.items():
                text = text.replace(char, latex)

            # 2. Apply complex fixes for single variables followed by "is"
            for pattern, replacement in complex_fixes:
                text = re.sub(pattern, replacement, text)

            # 3. Handle subscripts like x_i if not already wrapped
            # Match word starting with letter, followed by _, followed by letter/number
            # But only if not already inside $
            text = re.sub(r'\b([a-zA-Z][a-zA-Z0-9]*_[a-zA-Z0-9]+)\b(?!\$)', r'$\1$', text)

            # 4. Clean up any double dollar signs $$ caused by overlapping replacements
            text = text.replace('$$', '$')
            
            # 5. Fix spacing
            text = re.sub(r'(\$[^\$]+\$)([a-zA-Z0-9])', r'\1 \2', text)
            text = re.sub(r'([a-zA-Z0-9])(\$[^\$]+\$)', r'\1 \2', text)
            
            # Final space cleanup
            text = text.replace('  ', ' ')
            text = text.strip()

            sd["equationVars"] = text

    # Save
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('export const dictionaryData = ' + json.dumps(data, indent=2) + ';')

final_polish_math()
print("Final polished math formatting applied.")
