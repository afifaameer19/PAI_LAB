import numpy as np

class GridWorldMDP:
    def __init__(self, size, goal, trap):
        self.size = size
        self.goal = goal
        self.trap = trap

        self.state_space = [(i, j) for i in range(size) for j in range(size)]
        self.action_space = ['UP', 'DOWN', 'LEFT', 'RIGHT']

        self.transitions = self.build_transitions()
        self.rewards = self.build_rewards()

    def build_transitions(self):
        transitions = {}

        for state in self.state_space:
            transitions[state] = {}

            for action in self.action_space:
                i, j = state

                if action == 'UP':
                    next_state = (max(i - 1, 0), j)
                elif action == 'DOWN':
                    next_state = (min(i + 1, self.size - 1), j)
                elif action == 'LEFT':
                    next_state = (i, max(j - 1, 0))
                elif action == 'RIGHT':
                    next_state = (i, min(j + 1, self.size - 1))

                transitions[state][action] = [(1.0, next_state)]

        return transitions

    def build_rewards(self):
        rewards = {}

        for state in self.state_space:
            if state == self.goal:
                rewards[state] = 0
            elif state == self.trap:
                rewards[state] = -10
            else:
                rewards[state] = -1

        return rewards


# ---------------- VALUE ITERATION ----------------
def value_iteration(mdp, gamma=0.9, epsilon=0.01):
    state_values = {state: 0.0 for state in mdp.state_space}

    while True:
        delta = 0

        for state in mdp.state_space:
            if state == mdp.goal or state == mdp.trap:
                continue

            v = state_values[state]

            new_value = max([
                sum([
                    p * (mdp.rewards[next_state] + gamma * state_values[next_state])
                    for (p, next_state) in mdp.transitions[state][action]
                ])
                for action in mdp.action_space
            ])

            state_values[state] = new_value
            delta = max(delta, abs(v - new_value))

        if delta < epsilon:
            break

    return state_values


# ---------------- POLICY ITERATION ----------------
def policy_iteration(mdp, gamma=0.9):
    # Initialize random policy
    policy = {state: np.random.choice(mdp.action_space) for state in mdp.state_space}
    state_values = {state: 0.0 for state in mdp.state_space}

    while True:
        # Policy Evaluation
        while True:
            delta = 0

            for state in mdp.state_space:
                if state == mdp.goal or state == mdp.trap:
                    continue

                v = state_values[state]
                action = policy[state]

                new_value = sum([
                    p * (mdp.rewards[next_state] + gamma * state_values[next_state])
                    for (p, next_state) in mdp.transitions[state][action]
                ])

                state_values[state] = new_value
                delta = max(delta, abs(v - new_value))

            if delta < 0.01:
                break

        # Policy Improvement
        policy_stable = True

        for state in mdp.state_space:
            if state == mdp.goal or state == mdp.trap:
                continue

            old_action = policy[state]

            best_action = max(
                mdp.action_space,
                key=lambda action: sum([
                    p * (mdp.rewards[next_state] + gamma * state_values[next_state])
                    for (p, next_state) in mdp.transitions[state][action]
                ])
            )

            policy[state] = best_action

            if old_action != best_action:
                policy_stable = False

        if policy_stable:
            break

    return policy, state_values


# ---------------- EXAMPLE USAGE ----------------
if __name__ == "__main__":
    size = 3
    goal = (2, 2)
    trap = (1, 1)

    mdp = GridWorldMDP(size, goal, trap)

    # Value Iteration
    values = value_iteration(mdp)
    print("Value Iteration Results:")
    for state, value in values.items():
        print(f"State: {state}, Value: {value:.2f}")

    # Policy Iteration
    policy, state_values = policy_iteration(mdp)
    print("\nPolicy Iteration Results:")
    for state, action in policy.items():
        print(f"State: {state}, Action: {action}")
