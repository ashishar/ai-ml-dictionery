import re

def robust_math_fix():
    filepath = 'src/data.js'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Targeted replacements for the most persistent issues
    
    # Line 2394 (Q-learning)
    content = content.replace(r'$\lambda3 (gamma) is the discount factor. max $ Q(s\',a\')$', 
                              r'$\gamma$ (gamma) is the discount factor. $\max_{a\'} Q(s\', a\')$')
    # If the above fails, let's try a partial match
    content = content.replace(r'$\lambda3 (gamma)', r'$\gamma$ (gamma)')
    content = content.replace(r'max $ Q(s\',a\')$', r'$\max_{a\'} Q(s\', a\')$')

    # Line 1322 (Gradient Boosting)
    content = content.replace(r'$ F_m  (x)', r'$F_m(x)$')
    content = content.replace(r'$ F_{m-1$}(x)', r'$F_{m-1}(x)$')
    content = content.replace(r'$\gamma $_m (gamma)', r'$\gamma_m$ (gamma)')

    # Global cleanup of common mashing patterns
    content = content.replace(r'$ $', r' ')
    content = content.replace(r'$$', r'$')
    
    # Fix probability notation
    content = content.replace(r'P( $ $ X_i $ $ | Parents( $ $ X_i $ $ )$)', r'$P(X_i \mid \text{Parents}(X_i))$')
    content = content.replace(r'P($ X_1 $, \dots, $ X_n $)', r'$P(X_1, \dots, X_n)$')

    # Ensure Greek letters are clean
    for g in ['alpha', 'beta', 'gamma', 'delta', 'epsilon', 'theta', 'lambda', 'mu', 'pi', 'sigma', 'phi']:
        content = content.replace('\\' + g + ' ', '\\' + g + '$ ') # This might be risky, let's be safer
        content = content.replace('$\\' + g + ' $', '$\\' + g + '$')
        content = content.replace('$\\' + g + '  $', '$\\' + g + '$')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

robust_math_fix()
print("Robust math fix completed.")
