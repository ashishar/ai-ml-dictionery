import json
import re

def fix_malformed_math():
    filepath = 'src/data.js'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Clean up the export string to parse as JSON
    json_str = content.replace('export const dictionaryData = ', '').rstrip(';\n')
    data = json.loads(json_str)

    for term in data:
        sd = term.get("structuredDefinition", {})
        if "equationVars" in sd:
            text = sd["equationVars"]
            
            # 1. Fix nested/broken wrapping
            text = text.replace('V^$\\pi$(s)', '$V^\\pi(s)$')
            text = text.replace('$E_$\\pi$', '$E_\\pi$')
            text = text.replace('$r_{t$+k+1}', '$r_{t+k+1}$')
            text = text.replace('max Q(s\',a\')', '$\\max_{a\'} Q(s\',a\')$')
            text = text.replace('f_r$f(x)', '$f_r(x)$') # Fixed Random forest issue
            text = text.replace('f_b(x$)', '$f_b(x)$')
            
            # 2. Fix cases where symbols are smashed against words
            # $symbol$word -> $symbol$ word
            text = re.sub(r'(\$[^\$]+\$)([a-zA-Z])', r'\1 \2', text)
            # word$symbol$ -> word $symbol$
            text = re.sub(r'([a-zA-Z])(\$[^\$]+\$)', r'\1 \2', text)
            
            # 3. Clean up double/triple wrapping
            text = re.sub(r'\$\$+(.*?)\$\$+', r'$\1$', text)
            
            # 4. Specific known bad strings from user examples
            text = text.replace('E_\\pirepresentstheexpectedreturnfollowingthepolicy.', '$E_\\pi$ represents the expected return following the policy.')
            text = text.replace('\\gamma((gamma)isthediscountfactor.)', '$\\gamma$ (gamma) is the discount factor.')
            
            # 5. Handle the (gamma) redundancy
            text = re.sub(r'(\$\\[a-z]+\$)\s+\(\1\)', r'\1', text) # Remove if it was $\gamma$ ($\gamma$)
            
            # 6. Final space clean up
            text = text.replace('  ', ' ')
            text = text.strip()

            sd["equationVars"] = text

    # Save the updated data
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('export const dictionaryData = ' + json.dumps(data, indent=2) + ';')

fix_malformed_math()
print("Successfully fixed malformed math strings and spacing.")
