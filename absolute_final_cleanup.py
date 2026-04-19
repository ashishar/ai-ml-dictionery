import re

def absolute_final_cleanup():
    filepath = 'src/data.js'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Targeted artifact removal
    replacements = {
        r'$ $ R_t$': r'$R_t$',
        r'$ MS $ E_k$': r'$MSE_k$',
        r'$ $ X_t $ilde $': r'$\tilde{X}$',
        r'$CV_{(K)}$': r'$CV_{(K)}$', # Ensure this one is clean
        r'$ $ x_i $ $': r'$x_i$',
        r'$ \hat{x}_i $ $ $': r'$\hat{x}_i$',
        r'$y $   is': r'$y$ is',
        r'f(x)': r'$f(x)$',
        r'g()': r'$g()$',
        r'P(x-i, y-j)': r'$P(x-i, y-j)$',
        r'K(i,j)': r'$K(i,j)$',
        r'I(x,y)': r'$I(x,y)$',
        r'CV_{(K)}': r'$CV_{(K)}$'
    }
    
    for old, new in replacements.items():
        content = content.replace(old, new)

    # 2. Fix the nested $ problem globally in equationVars
    def fix_nesting(match):
        text = match.group(1)
        # Remove any internal $ if they are within 3 chars of each other
        text = re.sub(r'\$\s*\$', r' ', text)
        # Ensure only one $ at start and end of blocks that need them
        # This is tricky, let's just do common ones
        return f'"equationVars": "{text}"'

    content = re.sub(r'"equationVars": "(.*?)"', fix_nesting, content)

    # 3. Final spacing polish
    content = content.replace('  ', ' ')
    content = re.sub(r'(\$[^\$]+\$)([a-zA-Z])', r'\1 \2', content)
    content = re.sub(r'([a-zA-Z])(\$[^\$]+\$)', r'\1 \2', content)
    content = content.replace('$$', '$')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

absolute_final_cleanup()
print("Absolute final cleanup completed.")
