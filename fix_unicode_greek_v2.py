import re

def fix_unicode_greek_v2():
    filepath = 'src/data.js'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Greek characters to LaTeX names
    # We use a dictionary with the actual characters
    greek_to_latex = {
        'σ': '\\sigma', 'μ': '\\mu', 'π': '\\pi', 'γ': '\\gamma', 
        'α': '\\alpha', 'β': '\\beta', 'Δ': '\\Delta', 'Σ': '\\Sigma', 
        'λ': '\\lambda', 'η': '\\eta', 'θ': '\\theta', 'ε': '\\epsilon', 
        'τ': '\\tau', 'φ': '\\phi', 'ψ': '\\psi', 'ω': '\\omega', 
        'Φ': '\\Phi', 'Λ': '\\Lambda'
    }

    def clean_ev(match):
        text = match.group(1)
        
        # 1. Replace the actual Unicode characters
        for char, latex in greek_to_latex.items():
            text = text.replace(char, latex)
            
        # 2. Re-wrap math in $
        # Look for things starting with \ or containing _ or ^
        # and wrap them if not already wrapped
        text = text.replace('$', '')
        
        # Pattern for symbols/functions: \sigma, \sigma(z)_i, x_i, h_{t-1}
        # First, wrap anything with a \
        text = re.sub(r'(\\[a-zA-Z]+(?:\([^\)]*\))?(_[a-zA-Z0-9_{}:-]+)?)', r'$\1$', text)
        
        # Second, wrap plain subscripts
        text = re.sub(r'\b([a-zA-Z][a-zA-Z0-9_{}:-]*_[a-zA-Z0-9_{}:-]*)\b', r'$\1$', text)
        
        # Third, wrap single letter variables
        text = re.sub(r'\b([a-zA-HJ-Z])\b(?=\s+(?:is|denotes|represents|refers|stands for))', r'$\1$', text)
        text = re.sub(r'\bi\b(?=\s+is)', r'$i$', text)
        
        # Clean up double $$
        text = text.replace('$$', '$')
        
        # Ensure spaces around $
        text = re.sub(r'(\$[^\$]+\$)([a-zA-Z])', r'\1 \2', text)
        text = re.sub(r'([a-zA-Z])(\$[^\$]+\$)', r'\1 \2', text)
        
        # Space after period followed by $
        text = re.sub(r'\.([\$])', r'. \1', text)
        
        return f'"equationVars": "{text}"'

    new_content = re.sub(r'"equationVars": "(.*?)"', clean_ev, content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

fix_unicode_greek_v2()
print("Surgical Unicode-to-LaTeX (V2) applied.")
