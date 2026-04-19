import json
import re

def add_math_symbols():
    filepath = 'src/data.js'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Clean up the export string to parse as JSON
    json_str = content.replace('export const dictionaryData = ', '').rstrip(';\n')
    data = json.loads(json_str)

    # Greek character mapping (Unicode to LaTeX)
    greek_map = {
        '\u03c0': r'\pi',
        '\u03c3': r'\sigma',
        '\u03bc': r'\mu',
        '\u03b3': r'\gamma',
        '\u03b2': r'\beta',
        '\u03b5': r'\epsilon',
        '\u03b1': r'\alpha',
        '\u03b4': r'\delta',
        '\u03b7': r'\eta',
        '\u03b8': r'\theta',
        '\u03bb': r'\lambda',
        '\u03c1': r'\rho',
        '\u03c4': r'\tau',
        '\u03c6': r'\phi',
        '\u03c8': r'\psi',
        '\u03c9': r'\omega',
        '\u0394': r'\Delta',
        '\u03a3': r'\Sigma',
        '\u03a6': r'\Phi',
        '\u03a9': r'\Omega'
    }

    for term in data:
        sd = term.get("structuredDefinition", {})
        if "equationVars" in sd:
            text = sd["equationVars"]
            
            # 1. Strip existing $ (just in case)
            text = text.replace('$', '')

            # 2. Replace unicode Greek letters with LaTeX equivalents
            for char, latex in greek_map.items():
                text = text.replace(char, latex)

            # 3. Handle specific multi-char symbols FIRST
            specific_symbols = [
                'f(x)', 'L_{MLM}', 'CV_{(K)}', 'x_hat_i', 'MSE_k', 'Gain(S, A)', 'Entropy(S)', 
                'f^{(L)}', '\\mu_B', '\\sigma_B^2', 'x_i', 'R_t', 'X_1', 'X_n', 'P(X_i | Parents(X_i))',
                'I(x,y)', 'K(i,j)', 'P(x-i, y-j)', 'W x + b', '\\epsilon', '\\gamma', '\\beta', '\\pi', '\\sigma', '\\mu'
            ]
            
            # Sort symbols by length descending to match longest first
            specific_symbols.sort(key=len, reverse=True)

            placeholders = {}
            for i, sym in enumerate(specific_symbols):
                placeholder = f"VARSYM{i}VAR" 
                placeholders[placeholder] = sym
                text = text.replace(sym, placeholder)

            # 4. Wrap remaining subscripts like u_i, y_i, etc.
            # Only if they are at the start of a sentence or followed by specific words
            text = re.sub(r'(\b[a-zA-Z0-9]+_[a-zA-Z0-9{}()^]+\b)', r'$\1$', text)
            
            # 5. Wrap single letters followed by is/denotes/represents
            text = re.sub(r'\b([a-zA-Z])\b\s+(?=(?:is|denotes|represents|refers|stands for))', r'$\1$ ', text)

            # 6. Restore placeholders
            for placeholder, sym in placeholders.items():
                text = text.replace(placeholder, f"${sym}$")

            # 7. Clean up (gamma) or (epsilon) after a LaTeX symbol
            text = re.sub(r'(\$\\[a-z]+\$)\s+\(([a-z]+)\)', r'\1 ($\2$)', text)

            # 8. Final clean up
            text = text.replace('$$', '$')
            text = text.replace('$$', '$')
            text = re.sub(r'\$(\s+)\$', r'\1', text)
            text = text.replace('  ', ' ')

            sd["equationVars"] = text

    # Save the updated data
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('export const dictionaryData = ' + json.dumps(data, indent=2) + ';')

add_math_symbols()
print("Successfully corrected math symbol formatting.")
