import json
import re

def fix_math_surgical():
    filepath = 'src/data.js'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Clean up the export string to parse as JSON
    json_str = content.replace('export const dictionaryData = ', '').rstrip(';\n')
    data = json.loads(json_str)

    # Greek Unicode to LaTeX mapping
    greek_to_latex = {
        '\u03c0': r'\pi',
        '\u03b3': r'\gamma',
        '\u03b1': r'\alpha',
        '\u03b5': r'\epsilon',
        '\u03bc': r'\mu',
        '\u03c3': r'\sigma',
        '\u03b2': r'\beta',
        '\u0394': r'\Delta',
        '\u03a3': r'\Sigma',
        '\u039b': r'\Lambda'
    }

    # Complex blocks to handle first
    complex_blocks = [
        r'V^\pi(s)', r'E_\pi', r'r_{t+k+1}', r'Q(s,a)', r'max Q(s\',a\')', 
        r'L_{MLM}', r'CV_{(K)}', r'x_hat_i', r'mu_B', r'sigma_B^2', 
        r'Gain(S, A)', r'Entropy(S)', r'f(x)', r'f_b(x)', r'f_rf(x)', r'MSE_k'
    ]
    complex_blocks.sort(key=len, reverse=True)

    # Individual Greek letters
    greek_letters = [
        r'\pi', r'\gamma', r'\alpha', r'\epsilon', r'\mu', r'\sigma', r'\beta', r'\Delta', r'\Sigma', r'\Lambda'
    ]

    for term in data:
        sd = term.get("structuredDefinition", {})
        if "equationVars" in sd:
            text = sd["equationVars"]
            
            # 1. Clean up any existing messed up dollar signs
            text = text.replace('$', '')

            # 2. Replace unicode Greek with LaTeX
            for char, latex in greek_to_latex.items():
                text = text.replace(char, latex)

            # 3. Protect complex blocks with wrapping
            for block in complex_blocks:
                text = text.replace(block, f'${block}$')

            # 4. Protect individual Greek letters with wrapping
            for letter in greek_letters:
                # Avoid wrapping if already wrapped
                text = text.replace(letter, f'${letter}$')

            # 5. Wrap single character variables followed by 'is', 'denotes', etc.
            text = re.sub(r'\b([a-zA-Z])\b(?=\s+(?:is|denotes|represents|refers|stands for))', r'$\1$', text)

            # 6. Final cleanup of nested or double dollar signs
            text = text.replace('$$', '$')
            text = text.replace('$$', '$')
            
            # 7. Add spaces around $ blocks for readability
            text = re.sub(r'(\$[^\$]+\$)([a-zA-Z0-9])', r'\1 \2', text)
            text = re.sub(r'([a-zA-Z0-9])(\$[^\$]+\$)', r'\2 \1', text) # Wait, this one should be \1 \2
            text = re.sub(r'([a-zA-Z0-9])(\$[^\$]+\$)', r'\1 \2', text)

            # 8. Specific parenthetical cleanup
            text = re.sub(r'(\$\\[a-z]+\$)\s+\((?:gamma|alpha|pi|mu|sigma|epsilon)\)', r'\1', text)
            
            # Final space cleanup
            text = text.replace('  ', ' ')
            text = text.strip()

            sd["equationVars"] = text

    # Save the updated data
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('export const dictionaryData = ' + json.dumps(data, indent=2) + ';')

fix_math_surgical()
print("Successfully applied refined surgical math formatting.")
