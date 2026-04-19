import re

def surgical_math_final_pass():
    filepath = 'src/data.js'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. First, clean all "equation" fields (ensure no $)
    def clean_eq(match):
        eq = match.group(1)
        clean_eq = eq.replace('$', '')
        return f'"equation": "{clean_eq}"'
    content = re.sub(r'"equation": "(.*?)"', clean_eq, content)

    # 2. Fix the specific Q-learning equationVars (Line 2394)
    # The grep showed: "$ Q(s,a)$ is the current Q-value for a state-action pair. $\alpha$ $ (alpha) is the learning rate. $ r $ is the observed reward. $\gamma$ (gamma) is the discount factor. max $ Q(s',a')$ is the maximum expected future reward from the next state s'."
    
    content = content.replace(r'max $ Q(s\',a\')$', r'$\max_{a\'} Q(s\', a\')$')
    content = content.replace(r'$\lambda3', r'$\gamma$') # Just in case
    content = content.replace(r'$\alpha$ $', r'$\alpha$')
    content = content.replace(r'$\gamma$ $', r'$\gamma$')

    # 3. Clean up "smashed" text in equationVars
    def clean_vars(match):
        text = match.group(1)
        # Fix variables like "x is" -> "$x$ is"
        # But let's be very specific to avoid over-fixing
        text = text.replace('  ', ' ')
        text = text.replace('$ $', ' ')
        text = text.replace('$$', '$')
        
        # Fix common Greek wrapping issues
        greeks = ['alpha', 'beta', 'gamma', 'delta', 'epsilon', 'theta', 'lambda', 'mu', 'pi', 'sigma', 'phi']
        for g in greeks:
            text = text.replace('$\\' + g + ' $', '$\\' + g + '$')
            text = text.replace('$\\' + g + ' (', '$\\' + g + '$ (')
            
        return f'"equationVars": "{text}"'

    content = re.sub(r'"equationVars": "(.*?)"', clean_vars, content)

    # 4. Fix specific known broken ones
    content = content.replace(r'$F_m (x)', r'$F_m(x)$')
    content = content.replace(r'V^$\pi $(s)', r'$V^{\pi}(s)$')
    content = content.replace(r'$E_$\pi', r'$E_{\pi}')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

surgical_math_final_pass()
print("Surgical final pass completed.")
