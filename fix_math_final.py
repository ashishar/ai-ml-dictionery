import json
import re
import sys

# Ensure output is UTF-8
if sys.stdout.encoding != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def fix_math_final():
    filepath = 'src/data.js'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    json_str = content.replace('export const dictionaryData = ', '').rstrip(';\n')
    data = json.loads(json_str)

    # Unicode to LaTeX
    greek_map = {
        '\u03c0': r'\pi', '\u03b3': r'\gamma', '\u03b1': r'\alpha', '\u03b5': r'\epsilon',
        '\u03bc': r'\mu', '\u03c3': r'\sigma', '\u03b2': r'\beta', '\u0394': r'\Delta',
        '\u03a3': r'\Sigma', '\u039b': r'\Lambda', '\u03b7': r'\eta', '\u03b8': r'\theta',
        '\u03bb': r'\lambda', '\u03c1': r'\rho', '\u03c4': r'\tau', '\u03c6': r'\phi',
        '\u03c8': r'\psi', '\u03c9': r'\omega'
    }

    # Complex patterns
    complex_patterns = [
        (r'L_{MLM}', r'$L_{MLM}$'),
        (r'X_tilde', r'$\tilde{X}$'),
        (r'X_([1-n])', r'$X_\1$'),
        (r'P\(X_i\s?\|\s?Parents\(X_i\)\)', r'$P(X_i \mid Parents(X_i))$'),
        (r'P\(X_1\.\.\.X_n\)', r'$P(X_1...X_n)$'),
        (r'f_r\$f\(x\)', r'$f_{rf}(x)$'), # Handle potential mess
        (r'f_b\(x\)', r'$f_b(x)$'),
        (r'MSE_k', r'$MSE_k$'),
        (r'CV_{\(K\)}', r'$CV_{(K)}$'),
        (r'Gain\(S, A\)', r'$Gain(S, A)$'),
        (r'Entropy\(S\)', r'$Entropy(S)$'),
        (r'I\(x,y\)', r'$I(x,y)$'),
        (r'K\(i,j\)', r'$K(i,j)$'),
        (r'P\(x-i,\s?y-j\)', r'$P(x-i, y-j)$')
    ]

    for term in data:
        sd = term.get("structuredDefinition", {})
        if "equationVars" in sd:
            text = sd["equationVars"]
            
            # 1. Clean existing $ to avoid nested mess
            text = text.replace('$', '')

            # 2. Replace Unicode Greek
            for char, latex in greek_map.items():
                text = text.replace(char, latex)

            # 3. Apply complex patterns
            for pattern, replacement in complex_patterns:
                text = re.sub(pattern, replacement, text)

            # 4. Wrap remaining \ symbols (LaTeX commands)
            # Only if they look like a command: \followed by letters
            text = re.sub(r'(\\[a-zA-Z]+(?:_[a-zA-Z0-9{}]+)?)', r'$\1$', text)

            # 5. Wrap single character variables followed by is/denotes
            # But skip words like "A", "I", "The"
            text = re.sub(r'\b([a-z]|[A-HJ-Z])\b(?=\s+(?:is|denotes|represents|refers|stands for))', r'$\1$', text)

            # 6. Cleanup spacing
            text = re.sub(r'(\$[^\$]+\$)([a-zA-Z0-9])', r'\1 \2', text)
            text = re.sub(r'([a-zA-Z0-9])(\$[^\$]+\$)', r'\1 \2', text)

            # 7. Redundant parenthetical cleanup
            text = re.sub(r'(\$\\[a-z]+\$)\s+\((?:gamma|alpha|pi|mu|sigma|epsilon|lambda|delta)\)', r'\1', text)
            
            # Final touch
            text = text.replace('$$', '$')
            text = text.replace('  ', ' ')
            text = text.strip()

            sd["equationVars"] = text

    # Save
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('export const dictionaryData = ' + json.dumps(data, indent=2) + ';')

fix_math_final()
print("Final surgical math fixes applied successfully.")
