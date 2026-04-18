import json

filepath = 'C:/Users/ashis/.gemini/antigravity/scratch/ai-dictionary-app/src/data.js'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

json_str = content.replace('export const dictionaryData = ', '').rstrip(';\n')
terms = json.loads(json_str)

equations = {
    "Artificial intelligence": r"AI \approx \max_{\pi} \mathbb{E} \left[ \sum_{t=0}^\infty \gamma^t R_t \right]",
    "Machine learning": r"\min_{\theta} \frac{1}{N} \sum_{i=1}^N \mathcal{L}(y_i, f_\theta(x_i))",
    "Deep learning": r"f(x) = f^{(L)}(f^{(L-1)}(\dots f^{(1)}(x) \dots))",
    "Neural network": r"y = \sigma(W x + b)",
    "Transformer": r"\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V",
    "Large language model": r"P(w_t | w_{1:t-1}) = \text{softmax}(W \cdot h_t)",
    "Support vector machine": r"\min_{w, b} \frac{1}{2} \|w\|^2 \text{ subject to } y_i(w \cdot x_i + b) \ge 1",
    "Decision tree": r"\text{Gain}(S, A) = \text{Entropy}(S) - \sum_{v \in \text{Values}(A)} \frac{|S_v|}{|S|} \text{Entropy}(S_v)",
    "Random forest": r"\hat{f}_{rf}(x) = \frac{1}{B} \sum_{b=1}^B \hat{f}_b(x)",
    "K-means clustering": r"\min_{C} \sum_{k=1}^K \sum_{x \in C_k} \|x - \mu_k\|^2",
    "Reinforcement learning": r"V^\pi(s) = \mathbb{E}_\pi \left[ \sum_{k=0}^\infty \gamma^k r_{t+k+1} \mid S_t = s \right]",
    "Q-learning": r"Q(s,a) \leftarrow Q(s,a) + \alpha [r + \gamma \max_{a'} Q(s',a') - Q(s,a)]",
    "Markov decision process": r"P(S_{t+1}=s', R_{t+1}=r \mid S_t=s, A_t=a)",
    "Natural language processing": r"P(w_1, \dots, w_n) = \prod_{i=1}^n P(w_i | w_1 \dots w_{i-1})",
    "Computer vision": r"I(x,y) = \sum_{i} \sum_{j} K(i,j) \cdot P(x-i, y-j)",
    "Convolutional neural network": r"(f * g)(t) \triangleq \int_{-\infty}^{\infty} f(\tau) g(t - \tau) \, d\tau",
    "Recurrent neural network": r"h_t = \sigma(W_{hh} h_{t-1} + W_{xh} x_t + b_h)",
    "Long short-term memory": r"f_t = \sigma(W_f \cdot [h_{t-1}, x_t] + b_f)",
    "Generative adversarial network": r"\min_G \max_D V(D, G) = \mathbb{E}_{x}[\log D(x)] + \mathbb{E}_{z}[\log(1 - D(G(z)))]",
    "Autoencoder": r"\mathcal{L}(x, g(f(x))) = \|x - g(f(x))\|^2",
    "Principal component analysis": r"\Sigma = \frac{1}{n-1} X^T X = V \Lambda V^T",
    "Overfitting": r"E_{train}(f) \ll E_{test}(f)",
    "Cross-validation": r"CV_{(K)} = \frac{1}{K} \sum_{k=1}^K \text{MSE}_k",
    "Hyperparameter optimization": r"\theta^* = \arg\min_{\theta \in \Theta} \mathcal{L}(A_\theta(X_{train}), X_{val})",
    "Activation function": r"f(x) = \begin{cases} x & \text{if } x > 0 \\ 0 & \text{otherwise} \end{cases}",
    "Softmax function": r"\sigma(\mathbf{z})_i = \frac{e^{z_i}}{\sum_{j=1}^K e^{z_j}}",
    "Rectifier": r"f(x) = \max(0, x)",
    "Batch normalization": r"\hat{x}_i = \frac{x_i - \mu_B}{\sqrt{\sigma_B^2 + \epsilon}} \gamma + \beta",
    "Dropout": r"y = f(W \cdot (\mathbf{r} * \mathbf{x}) + b)",
    "Word embedding": r"\text{sim}(A, B) = \frac{A \cdot B}{\|A\| \|B\|}",
    "Word2vec": r"J(\theta) = -\frac{1}{T} \sum_{t=1}^T \sum_{-c \le j \le c, j \neq 0} \log P(w_{t+j} | w_t)",
    "BERT": r"\mathcal{L}_{MLM} = - \sum_{x \in M} \log P(x | \tilde{X})",
    "Generative pre-trained": r"L = \sum_i \log P(u_i | u_{i-k}, \dots, u_{i-1}; \Theta)",
    "Turing test": r"P(\text{Human} | \text{Resp}_A) = P(\text{Human} | \text{Resp}_B)",
    "Expert system": r"\text{IF } Condition \text{ THEN } Action",
    "Fuzzy logic": r"\mu_A(x) \in [0, 1]",
    "Genetic algorithm": r"f(x_i) > f(x_j) \implies P(\text{select } x_i) > P(\text{select } x_j)",
    "Swarm intelligence": r"v_i(t+1) = w v_i(t) + c_1 r_1 (p_i - x_i(t)) + c_2 r_2 (g - x_i(t))",
    "Bayesian network": r"P(X_1, \dots, X_n) = \prod_{i=1}^n P(X_i | \text{Parents}(X_i))",
    "Hidden Markov model": r"P(Y, X) = P(Y_1) P(X_1 | Y_1) \prod_{t=2}^T P(Y_t | Y_{t-1}) P(X_t | Y_t)",
    "Naive Bayes classifier": r"\hat{y} = \arg\max_y P(y) \prod_{i=1}^n P(x_i | y)",
    "Logistic regression": r"P(y=1|x) = \frac{1}{1 + e^{-(\beta_0 + \beta_1 x)}}",
    "Linear regression": r"y = \beta_0 + \beta_1 x + \epsilon",
    "Lasso": r"\min_{\beta} \left\{ \frac{1}{N} \|y - X\beta\|^2_2 + \lambda \|\beta\|_1 \right\}",
    "Ridge regression": r"\min_{\beta} \left\{ \|y - X\beta\|^2_2 + \lambda \|\beta\|^2_2 \right\}",
    "Elastic net regularization": r"\min_{\beta} \left\{ \frac{1}{2N} \|y - X\beta\|^2_2 + \lambda_1 \|\beta\|_1 + \frac{\lambda_2}{2} \|\beta\|^2_2 \right\}",
    "Ensemble learning": r"H(x) = \text{sign}\left(\sum_{t=1}^T \alpha_t h_t(x)\right)",
    "Gradient boosting": r"F_m(x) = F_{m-1}(x) + \gamma_m h_m(x)",
    "Backpropagation": r"\frac{\partial E}{\partial w_{ij}} = \delta_j o_i",
    "Gradient descent": r"\theta_{t+1} = \theta_t - \alpha \nabla_\theta J(\theta_t)"
}

for term in terms:
    t_name = term["title"]
    eq = None
    for k, v in equations.items():
        if k.lower() in t_name.lower() or t_name.lower() in k.lower():
            eq = v
            break
    if not eq:
        eq = r"f(x) = y"
    term["equation"] = eq

with open(filepath, 'w', encoding='utf-8') as f:
    f.write('export const dictionaryData = ')
    f.write(json.dumps(terms, indent=2))
    f.write(';\n')
print("Added equations to data.js")
