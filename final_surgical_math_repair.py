import re

def final_surgical_math_repair():
    filepath = 'src/data.js'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Fix the specific broken lines found via grep
    
    # Q-learning (term-??)
    content = content.replace(r'$\lambda3 (gamma) is the discount factor. max $ Q(s\',a\')', r'$\gamma$ (gamma) is the discount factor. $\max_{a\'} Q(s\', a\')$')
    
    # Value function / Reinforcement learning
    content = content.replace(r'V^$\pi $(s) is the value of state s under policy $\pi $. $ E_$\pi $ represents the expected return following the policy. $\gamma $ (gamma) is the discount factor. $ r_{t $+k+1}', 
                              r'$V^{\pi}(s)$ is the value of state s under policy $\pi$. $E_{\pi}$ represents the expected return following the policy. $\gamma$ (gamma) is the discount factor. $r_{t+k+1}$')

    # Gradient boosting
    content = content.replace(r'$ F_m (x) is the model at stage m. $ F_{m-1$}(x) is the previous model. $\gamma $_m (gamma)',
                              r'$F_m(x)$ is the model at stage m. $F_{m-1}(x)$ is the previous model. $\gamma_m$ (gamma)')
    content = content.replace(r'h_m $(x) is the new weak learner', r'$h_m(x)$ is the new weak learner')

    # Fuzzy logic
    content = content.replace(r'$\mu $_A(x) (mu) is the membership function', r'$\mu_A(x)$ (mu) is the membership function')

    # GAN
    content = content.replace(r'p_d $ ata $ is the real data distribution. p_z is the latent noise distribution.',
                              r'$p_{data}$ is the real data distribution. $p_z$ is the latent noise distribution.')

    # GPT
    content = content.replace(r'd_k $ is the dimensionality of the keys', r'$d_k$ is the dimensionality of the keys')

    # 2. General Regex cleanup for common "mashing" patterns
    
    # Fix variables mashed with text: e.g. "x is the..." -> "$x$ is the..."
    # But only in equationVars
    def clean_ev(match):
        text = match.group(1)
        
        # Remove nested/duplicate dollars
        text = text.replace('$$', '$')
        text = re.sub(r'\$\s*\$', ' ', text)
        
        # Fix specific word boundary issues
        text = re.sub(r'([a-zA-Z0-9])\$([a-zA-Z])', r'\1 $ \2', text)
        text = re.sub(r'([a-zA-Z])\$([a-zA-Z0-9])', r'\1 $ \2', text)
        
        # Fix subscript nesting like $_{t+1$ }
        text = re.sub(r'_\{([^}]+)\$ \}', r'_{\1}', text)
        text = re.sub(r'_\$([a-zA-Z0-9])', r'_{\1}', text)
        
        # Ensure Greek letters are wrapped correctly and have space
        greeks = ['alpha', 'beta', 'gamma', 'delta', 'epsilon', 'zeta', 'eta', 'theta', 'iota', 'kappa', 'lambda', 'mu', 'nu', 'xi', 'omicron', 'pi', 'rho', 'sigma', 'tau', 'upsilon', 'phi', 'chi', 'psi', 'omega']
        for g in greeks:
            text = re.sub(r'\\'+g+r'([^a-zA-Z])', r'$\\\1$\2', text) # This might be too broad
        
        return f'"equationVars": "{text}"'

    # I'll do a few more manual ones for safety
    content = content.replace(r'$\mu $_B', r'$\mu_B$')
    content = content.replace(r'$\sigma $_B^2', r'$\sigma_B^2$')
    content = content.replace(r'$\epsilon $ (epsilon) is', r'$\epsilon$ (epsilon) is')
    content = content.replace(r'$\gamma $ and $\beta $ are', r'$\gamma$ and $\beta$ are')
    content = content.replace(r'$\pi $ denotes', r'$\pi$ denotes')
    content = content.replace(r'$ E $ represents', r'$E$ represents')
    content = content.replace(r'$ R_t $ is', r'$R_t$ is')
    content = content.replace(r'$ L $ is', r'$L$ is')
    content = content.replace(r'$ x $ is', r'$x$ is')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

final_surgical_math_repair()
print("Final surgical math repair completed.")
