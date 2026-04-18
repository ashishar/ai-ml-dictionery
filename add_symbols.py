import json

filepath = 'C:/Users/ashis/.gemini/antigravity/scratch/ai-dictionary-app/src/data.js'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

json_str = content.replace('export const dictionaryData = ', '').rstrip(';\n')
terms = json.loads(json_str)

equation_symbols = {
    "Artificial intelligence": "π denotes the policy or decision-making strategy. E represents the expected value. γ (gamma) is the discount factor for future rewards. R_t is the reward received at time step t.",
    "Machine learning": "θ (theta) represents the model parameters being optimized. N is the total number of training samples. L is the loss function calculating the error. y_i is the actual true label, and f_θ(x_i) is the model's prediction for input x_i.",
    "Deep learning": "f(x) represents the final output of the network. f^(L) denotes the mathematical operation at the L-th layer. x is the initial input vector. The nested structure illustrates the hierarchical, multi-layered processing.",
    "Neural network": "y is the output vector. σ (sigma) is the non-linear activation function. W is the learned weight matrix. x is the input feature vector. b is the learned bias term.",
    "Transformer": "Q represents the Query matrix. K represents the Key matrix. V represents the Value matrix. d_k is the dimensionality of the keys, used as a scaling factor to prevent gradients from vanishing.",
    "Large language model": "P(w_t | w_{1:t-1}) is the conditional probability of the next word given the previous words. W is the output projection weight matrix. h_t is the hidden state representation of the context at step t.",
    "Support vector machine": "w is the normal vector to the hyperplane (determining its orientation). b is the bias or intercept term. y_i is the class label (+1 or -1) of the i-th sample. x_i is the feature vector of the i-th sample.",
    "Decision tree": "Gain(S, A) is the information gain of splitting set S using attribute A. Entropy(S) is the impurity of the current set. S_v is the subset of S where attribute A has value v.",
    "Random forest": "f_rf(x) is the final ensemble prediction. B is the total number of decision trees in the forest. f_b(x) is the prediction of the b-th individual decision tree.",
    "K-means clustering": "C_k represents the k-th cluster. x is a data point belonging to that cluster. μ_k (mu) is the centroid or mean vector of the k-th cluster.",
    "Reinforcement learning": "V^π(s) is the value of state s under policy π. E_π represents the expected return following the policy. γ (gamma) is the discount factor. r_{t+k+1} is the reward received at future steps.",
    "Q-learning": "Q(s,a) is the current Q-value for a state-action pair. α (alpha) is the learning rate. r is the observed reward. γ (gamma) is the discount factor. max Q(s',a') is the maximum expected future reward from the next state s'.",
    "Markov decision process": "P denotes probability. S_{t+1} and S_t are the next and current states. R_{t+1} is the reward. A_t is the action taken. This defines the transition dynamics of the environment.",
    "Natural language processing": "P(w_1...w_n) is the overall probability of a sentence. P(w_i | w_1...w_{i-1}) is the probability of the i-th word conditioned on all preceding words in the sequence.",
    "Computer vision": "I(x,y) is the resulting pixel value at coordinates (x,y). K is the convolution kernel or filter. P is the original image pixel matrix. i and j iterate over the spatial dimensions of the kernel.",
    "Convolutional neural network": "(f * g)(t) represents the convolution operation. f(τ) is the input signal or image. g(t - τ) is the flipped and shifted kernel/filter being applied.",
    "Recurrent neural network": "h_t is the hidden state at time t. σ (sigma) is the activation function. W_{hh} is the hidden-to-hidden weight matrix. W_{xh} is the input-to-hidden weight matrix. x_t is the input at time t. b_h is the bias.",
    "Long short-term memory": "f_t is the forget gate's activation vector. σ (sigma) is the sigmoid function. W_f is the weight matrix for the forget gate. h_{t-1} is the previous hidden state. x_t is the current input. b_f is the bias.",
    "Generative adversarial network": "G is the Generator. D is the Discriminator. V(D, G) is the value function. p_data is the real data distribution. p_z is the latent noise distribution. x is real data, z is noise.",
    "Autoencoder": "L is the reconstruction loss. x is the original input. f(x) is the encoder function mapping to a latent space. g() is the decoder function. g(f(x)) is the reconstructed output.",
    "Principal component analysis": "Σ (Sigma) is the covariance matrix. X is the centered data matrix. n is the number of samples. V is the matrix of eigenvectors (principal components). Λ (Lambda) is the diagonal matrix of eigenvalues.",
    "Overfitting": "E_{train}(f) is the error of the model f on the training dataset. E_{test}(f) is the error of the model on the unseen test dataset. The inequality shows training error is much lower than test error.",
    "Cross-validation": "CV_{(K)} is the cross-validation error estimate. K is the number of folds. MSE_k is the Mean Squared Error computed on the k-th hold-out validation fold.",
    "Hyperparameter optimization": "θ* (theta star) represents the optimal hyperparameters. Θ (capital theta) is the search space. L is the loss function. A_θ is the learning algorithm. X_{train} and X_{val} are the datasets.",
    "Activation function": "f(x) is the output of the function. x is the input value (typically the weighted sum of inputs). This specific example defines the ReLU function, returning x if positive, and 0 otherwise.",
    "Softmax function": "σ(z)_i is the output probability for class i. e is Euler's number. z_i is the raw logit score for class i. K is the total number of classes in the distribution.",
    "Rectifier": "f(x) is the output activation. max(0, x) means the function returns the input x if it is strictly greater than zero, otherwise it clips the output to exactly zero.",
    "Batch normalization": "x_hat_i is the normalized value. x_i is the input. μ_B is the batch mean. σ_B^2 is the batch variance. ε (epsilon) is a small constant. γ and β are learned scaling and shifting parameters.",
    "Dropout": "y is the layer output. f is the activation function. W is the weight matrix. r is a binary mask vector (0s and 1s) drawn from a Bernoulli distribution. x is the input vector. b is the bias.",
    "Word embedding": "sim(A, B) is the cosine similarity between two word vectors. A and B are the word embedding vectors. A · B is their dot product. ||A|| and ||B|| are their respective magnitudes.",
    "Word2vec": "J(θ) is the objective loss function. T is the total number of words. c is the context window size. P(w_{t+j} | w_t) is the probability of predicting the context word given the center word w_t.",
    "BERT": "L_{MLM} is the Masked Language Modeling loss. M is the set of masked tokens. x is the original true token. X_tilde is the corrupted sequence with masks. P is the predicted probability.",
    "Generative pre-trained": "L is the likelihood loss function. u_i is the current token being predicted. k is the size of the context window. Θ (Theta) represents all the neural network parameters.",
    "Turing test": "P denotes probability. 'Human' represents the event that the judge believes the entity is human. Resp_A and Resp_B are the conversational responses from the machine and the actual human.",
    "Expert system": "IF represents the antecedent or conditional trigger. Condition is the logical rule matching the knowledge base. THEN indicates the consequent. Action is the resulting decision or deduction.",
    "Fuzzy logic": "μ_A(x) (mu) is the membership function for set A. x is an element in the universe of discourse. [0, 1] indicates that the membership value is not strictly binary, but a continuous degree of truth.",
    "Genetic algorithm": "f(x) is the fitness function evaluating an individual. x_i and x_j are distinct individuals. P(select) is the probability of being chosen for the next generation's reproduction.",
    "Swarm intelligence": "v_i is the velocity of particle i. w is the inertia weight. c_1 and c_2 are cognitive and social coefficients. r_1 and r_2 are random vectors. p_i is the personal best position. g is the global best position. x_i is current position.",
    "Bayesian network": "P(X_1...X_n) is the joint probability distribution. P(X_i | Parents(X_i)) is the conditional probability of node X_i given its direct parent nodes in the directed acyclic graph.",
    "Hidden Markov model": "P(Y, X) is the joint probability of hidden states Y and observations X. P(Y_t | Y_{t-1}) is the transition probability. P(X_t | Y_t) is the emission probability of seeing X_t given state Y_t.",
    "Naive Bayes classifier": "y_hat is the predicted class. P(y) is the prior probability of class y. P(x_i | y) is the conditional probability of feature x_i given class y. The product symbol assumes all features are conditionally independent.",
    "Logistic regression": "P(y=1|x) is the predicted probability of the positive class. e is Euler's number. β_0 is the intercept. β_1 is the coefficient for feature x.",
    "Linear regression": "y is the dependent target variable. β_0 is the y-intercept. β_1 is the slope coefficient. x is the independent input feature. ε (epsilon) represents the irreducible error or noise.",
    "Lasso": "β represents the coefficients. y is the target vector. X is the feature matrix. ||y - Xβ||^2_2 is the standard squared error. λ (lambda) is the regularization strength. ||β||_1 is the L1 penalty (sum of absolute values).",
    "Ridge regression": "β represents the coefficients. y is the target. X is the input matrix. ||y - Xβ||^2_2 is the data fidelity term. λ is the regularization parameter. ||β||^2_2 is the L2 penalty (sum of squared coefficients).",
    "Elastic net regularization": "β represents the model coefficients. N is the number of samples. λ_1 is the L1 penalty strength (promoting sparsity). λ_2 is the L2 penalty strength (preventing large weights).",
    "Ensemble learning": "H(x) is the strong ensemble prediction. sign() outputs +1 or -1. T is the total number of weak learners. α_t (alpha) is the weight assigned to learner t. h_t(x) is the prediction of the t-th weak learner.",
    "Gradient boosting": "F_m(x) is the model at stage m. F_{m-1}(x) is the previous model. γ_m (gamma) is the step size or learning rate. h_m(x) is the new weak learner trained to predict the pseudo-residuals.",
    "Backpropagation": "∂E/∂w_{ij} is the partial derivative of the Error with respect to the weight. δ_j (delta) is the error term for neuron j. o_i is the output of the preceding neuron i.",
    "Gradient descent": "θ_t is the parameter vector at step t. α (alpha) is the learning rate controlling step size. ∇_θ J(θ_t) is the gradient (vector of partial derivatives) of the objective function J at the current parameters."
}

for term in terms:
    t_name = term["title"]
    
    # 1. Add specific equation symbols mapping
    symbol_str = None
    for k, v in equation_symbols.items():
        if k.lower() in t_name.lower() or t_name.lower() in k.lower():
            symbol_str = v
            break
            
    if symbol_str:
        term["structuredDefinition"]["equationVars"] = symbol_str
        
    # 2. Split long technical definitions into paragraphs
    tech = term["structuredDefinition"]["technical"]
    sentences = [s + '.' for s in tech.split('. ') if s]
    
    # Clean up trailing periods
    for i in range(len(sentences)):
        if sentences[i].endswith('..'):
            sentences[i] = sentences[i][:-1]
            
    if len(sentences) >= 3:
        mid = len(sentences) // 2
        term["structuredDefinition"]["technical"] = ' '.join(sentences[:mid])
        term["structuredDefinition"]["technical2"] = ' '.join(sentences[mid:])

with open(filepath, 'w', encoding='utf-8') as f:
    f.write('export const dictionaryData = ')
    f.write(json.dumps(terms, indent=2))
    f.write(';\n')

print("Symbols defined and paragraphs split.")
