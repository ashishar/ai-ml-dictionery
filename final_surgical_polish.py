import re

def final_surgical_polish():
    filepath = 'src/data.js'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Fix the specific corrupted patterns seen in the file
    content = content.replace(r'$\u $ 03c3', r'$\sigma$')
    content = content.replace(r'$\u $ 03bc', r'$\mu$')
    content = content.replace(r'$\u $ 03c0', r'$\pi$')
    content = content.replace(r'$\u $ 03b3', r'$\gamma$')
    content = content.replace(r'$\u $ 03b1', r'$\alpha$')
    content = content.replace(r'$\u $ 03b2', r'$\beta$')
    content = content.replace(r'$\u $ 03b5', r'$\epsilon$')
    content = content.replace(r'$\u$03b2', r'$\beta$')
    content = content.replace(r'$\u $ 03c3_B^2', r'$\sigma_B^2$')
    content = content.replace(r'$\u $ 03bc_B', r'$\mu_B$')
    content = content.replace(r'$\u $ 03b3', r'$\gamma$')

    # 2. Fix the nested/broken math from previous scripts
    content = content.replace(r'$L_{MLM $ }', r'$L_{MLM}$')
    content = content.replace(r'$CV_${(K)}', r'$CV_{(K)}$')
    content = content.replace(r'$x_hat_i $', r'$\hat{x}_i$')
    content = content.replace(r'$X_tilde $', r'$\tilde{X}$')
    content = content.replace(r'P( $ X_i $ | Parents( $ X_i $ ))', r'$P(X_i \mid \text{Parents}(X_i))$')
    content = content.replace(r'P($X_1$... $ X_n $ )', r'$P(X_1, \dots, X_n)$')

    # 3. Targeted replacements for equationVars specifically
    def clean_ev(match):
        text = match.group(1)
        
        # Cleanup Greek characters that might still be raw or escaped
        greek = {
            'u03c3': r'\sigma', 'u03bc': r'\mu', 'u03c0': r'\pi', 'u03b3': r'\gamma',
            'u03b1': r'\alpha', 'u03b2': r'\beta', 'u03b5': r'\epsilon', 'u039b': r'\Lambda',
            'u03a3': r'\Sigma', 'u03bb': r'\lambda'
        }
        for code, latex in greek.items():
            text = text.replace('\\' + code, latex)
            text = text.replace(code, latex)

        # Standardize subscripts
        text = re.sub(r'([a-zA-Z])_([a-zA-Z0-9])', r'$\1_\2$', text)
        
        # Standardize functions
        text = re.sub(r'\b([a-zA-Z]\([^\)]+\))', r'$\1$', text)
        
        # Cleanup double/messy dollar signs
        text = text.replace('$$', '$')
        
        # Add spaces around $ blocks
        text = re.sub(r'(\$[^\$]+\$)([a-zA-Z])', r'\1 \2', text)
        text = re.sub(r'([a-zA-Z])(\$[^\$]+\$)', r'\1 \2', text)
        
        # Fix periods followed by $
        text = re.sub(r'\.([\$])', r'. \1', text)
        
        # Fix specific word boundary issues
        text = text.replace('denotes the', ' denotes the')
        text = text.replace('is the', ' is the')
        
        return f'"equationVars": "{text}"'

    new_content = re.sub(r'"equationVars": "(.*?)"', clean_ev, content)

    # 4. Global cleanup of "$\u $ 0xxx"
    new_content = re.sub(r'\$\\u \$ [0-9a-f]{4}', lambda m: "$" + chr(int(m.group(0)[6:], 16)) + "$", new_content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

final_surgical_polish()
print("Surgical math polish completed.")
