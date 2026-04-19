import json
import re

def fix_math_final():
    filepath = 'src/data.js'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # We process the text directly instead of JSON to avoid escape issues
    def replace_vars(match):
        vars_text = match.group(1)
        
        # Unicode to LaTeX wrapped in $
        greek_map = {
            '\u03c0': r'$\pi$', '\u03b3': r'$\gamma$', '\u03b1': r'$\alpha$', '\u03b5': r'$\epsilon$',
            '\u03bc': r'$\mu$', '\u03c3': r'$\sigma$', '\u03b2': r'$\beta$', '\u0394': r'$\Delta$',
            '\u03a3': r'$\Sigma$', '\u039b': r'$\Lambda$', '\u03b7': r'$\eta$', '\u03b8': r'$\theta$',
            '\u03bb': r'$\lambda$', '\u03c1': r'$\rho$', '\u03c4': r'$\tau$', '\u03c6': r'$\phi$',
            '\u03c8': r'$\psi$', '\u03c9': r'$\omega$', '\u03f5': r'$\epsilon$'
        }
        
        for char, latex in greek_map.items():
            vars_text = vars_text.replace(char, latex)
            
        # Clean up double $$
        vars_text = vars_text.replace('$$', '$')
        
        # Remove redundant (gamma) etc.
        vars_text = re.sub(r'(\$\\[a-z]+\$)\s+\((?:gamma|alpha|pi|mu|sigma|epsilon|lambda|delta)\)', r'\1', vars_text)
        
        return f'"equationVars": "{vars_text}"'

    # Match "equationVars": "..."
    new_content = re.sub(r'"equationVars": "(.*?)"', replace_vars, content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

fix_math_final()
print("Surgical Unicode Greek replacement applied to equationVars.")
