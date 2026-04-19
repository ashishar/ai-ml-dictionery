import re

def fix_backslashes():
    filepath = 'src/data.js'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find LaTeX commands in equationVars and ensure they have double backslashes
    # Note: If they already have double, we don't want triple.
    
    def double_backslash(match):
        text = match.group(1)
        # Replace \ (not followed by another \) with \\
        # Actually, in the JS file, they should be stored as \\
        # If they are stored as \, it breaks JSON.
        
        # Let's fix specific common ones
        text = text.replace('\\dots', '\\\\dots')
        text = text.replace('\\mid', '\\\\mid')
        text = text.replace('\\pi', '\\\\pi')
        text = text.replace('\\gamma', '\\\\gamma')
        text = text.replace('\\alpha', '\\\\alpha')
        text = text.replace('\\sigma', '\\\\sigma')
        text = text.replace('\\mu', '\\\\mu')
        text = text.replace('\\epsilon', '\\\\epsilon')
        text = text.replace('\\beta', '\\\\beta')
        text = text.replace('\\hat', '\\\\hat')
        text = text.replace('\\max', '\\\\max')
        
        # Clean up triple backslashes to double
        text = text.replace('\\\\\\', '\\\\')
        
        return f'"equationVars": "{text}"'

    new_content = re.sub(r'"equationVars": "(.*?)"', double_backslash, content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

fix_backslashes()
print("Surgical backslash normalization applied.")
