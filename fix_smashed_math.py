import json
import re

def fix_smashed_math():
    filepath = 'src/data.js'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # We process the text directly to avoid JSON escape issues
    def clean_math_errors(match):
        text = match.group(1)
        
        # 1. Strip ALL existing $ to start clean
        text = text.replace('$', '')
        
        # 2. Fix specific known smashed variables
        # Format: "X is" -> "$X$ is"
        # We target capital letters and single letters followed by "is", "represents", etc.
        text = re.sub(r'\b([a-zA-Z])\b(?=\s+(?:is|denotes|represents|refers|stands for))', r'$\1$', text)
        
        # 3. Handle subscripts and functions like f(x), g(x)
        text = re.sub(r'\b([a-zA-Z](?:\([a-zA-Z0-9_,]*\)|_[a-zA-Z0-9_{}:-]*))\b', r'$\1$', text)
        
        # 4. Specifically fix the "L is the reconstruction loss" pattern
        text = re.sub(r'\bL\b(?=\s+is\s+the\s+reconstruction\s+loss)', r'$L$', text)

        # 5. Fix common Greek names left in text
        greek_names = ['alpha', 'beta', 'gamma', 'delta', 'epsilon', 'zeta', 'eta', 'theta', 'iota', 'kappa', 'lambda', 'mu', 'nu', 'xi', 'omicron', 'pi', 'rho', 'sigma', 'tau', 'upsilon', 'phi', 'chi', 'psi', 'omega']
        for name in greek_names:
            # Only if it's like "gamma is"
            text = re.sub(r'\b' + name + r'\b(?=\s+is)', r'$\\' + name + r'$', text)

        # 6. Ensure spaces around every $...$ block
        # Add space after $...$ if missing
        text = re.sub(r'(\$[^\$]+\$)([a-zA-Z])', r'\1 \2', text)
        # Add space before $...$ if missing
        text = re.sub(r'([a-zA-Z])(\$[^\$]+\$)', r'\1 \2', text)
        
        # 7. Clean up double spaces and double $$
        text = text.replace('$$', '$')
        text = text.replace('  ', ' ')
        
        return f'"equationVars": "{text}"'

    new_content = re.sub(r'"equationVars": "(.*?)"', clean_math_errors, content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

fix_smashed_math()
print("Surgical fix for smashed math and mismatched dollar signs applied.")
