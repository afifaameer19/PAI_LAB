# States
states = ['Rainy', 'Sunny']

# Observations
observations = ['walk', 'shop', 'clean']

# Initial probabilities
pi = {
    'Rainy': 0.6,
    'Sunny': 0.4
}

# Transition probabilities
A = {
    'Rainy': {'Rainy': 0.7, 'Sunny': 0.3},
    'Sunny': {'Rainy': 0.4, 'Sunny': 0.6}
}

# Emission probabilities
B = {
    'Rainy': {'walk': 0.1, 'shop': 0.4, 'clean': 0.5},
    'Sunny': {'walk': 0.6, 'shop': 0.3, 'clean': 0.1}
}

# Forward Algorithm
alpha = []

# Step 1: Initialization
alpha_1 = {}
for state in states:
    alpha_1[state] = pi[state] * B[state][observations[0]]
alpha.append(alpha_1)

# Step 2: Induction
for t in range(1, len(observations)):
    alpha_t = {}
    for curr_state in states:
        total = 0
        for prev_state in states:
            total += alpha[t-1][prev_state] * A[prev_state][curr_state]
        alpha_t[curr_state] = total * B[curr_state][observations[t]]
    alpha.append(alpha_t)

# Step 3: Termination
probability = sum(alpha[-1][state] for state in states)

# Print results
for t, step in enumerate(alpha, start=1):
    print(f"Step {t}: {step}")

print("\nFinal Probability:", probability)