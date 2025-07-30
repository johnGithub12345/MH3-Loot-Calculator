# Monster Hunter 3 Average Loot v0.4
# Gives table of average loot from a quest's Main Rewards for each Fate/Luck value
# By john12345 :)

# TO-DO:
# - Subquests
# - Carves
# - Captures
# - Breaks
# - Shinies
# - Import quest / monster data
# - Make it an app / GUI

import random
from tabulate import tabulate

# Percentage chances of receiving loot for non-guaranteed slots for each Fate/Luck value
luck_probabilities = [25, 50, 69, 81, 90]

def average_loot(items_A, item_weights_A, items_B, item_weights_B, trials=10000):
    """
    Prints a table of the average loot from a quest's Main Rewards for each Fate/Luck value.
    
    Args:
        items_A (list of str): List of possible items from Main Rewards Row A.
        item_weights_A (list of float): List of corresponding probabilities (0-1) for each item in Row A.
        items_B (list of str): List of possible items from Main Rewards Row B.
        item_weights_B (list of float): List of corresponding probabilities (0-1) for each item in Row B.
        trials (int, optional): Number of random trials to simulate, default 10,000. 
                                Can be decreased for speed, but be wary of variance in results.

    Returns:
        None
    """

    # Initialise each item's counter for each Fate/Luck value
    # Makes a list of dicts with keys = possible items, values = 0 (for now)
    loot_count_template = dict(zip(items_A, [0]*len(items_A)))
    for item in items_B:
        if item not in loot_count_template:
            loot_count_template[item] = 0
    loot_counts = [0]*5
    for i in range(5):
        loot_counts[i] = loot_count_template.copy()

    # Simulate loot 'trials' times for each Fate/Luck value
    for p in luck_probabilities:
        for i in range(trials):
            # Simulate guaranteed slots' loot
            guaranteed_loot_A = random.choices(items_A, weights = item_weights_A, cum_weights = None, k = 4)
            guaranteed_loot_B = random.choices(items_B, weights = item_weights_B, cum_weights = None, k = 1)

            # Simulate non-guaranteed slots' loot
            rng_loot_A_nested = []
            while len(rng_loot_A_nested) < 4 and random.randint(1,100) < p:
                rng_loot_A_nested.append(random.choices(items_A, weights = item_weights_A, cum_weights = None, k = 1))
            rng_loot_A = [loot for nested_loot in rng_loot_A_nested for loot in nested_loot]

            rng_loot_B_nested = []
            while len(rng_loot_B_nested) < 7 and random.randint(1,100) < p:
                rng_loot_B_nested.append(random.choices(items_B, weights = item_weights_B, cum_weights = None, k = 1))
            rng_loot_B = [loot for nested_loot in rng_loot_B_nested for loot in nested_loot]

            # Sum guaranteed and non-guaranteed slots' loot
            total_loot = guaranteed_loot_A + guaranteed_loot_B + rng_loot_A + rng_loot_B

            # Add simulated loot to the total count for this Fate/Luck value
            for i in range(len(total_loot)):
                loot_counts[luck_probabilities.index(p)][total_loot[i]] += 1

    # Calculate mean loot per quest
    for loot_count in loot_counts:
        for key in loot_count.keys():
            loot_count[key] = loot_count[key] / trials

    # Print the result as a nice table
    keys = list(loot_count_template.keys())
    headers = ["Item", "Horrible", "Bad", "Default", "Good", "Great"]
    table = []
    for key in keys:
        row = [key] + [count[key] for count in loot_counts]
        table.append(row)

    print(tabulate(table, headers=headers, tablefmt="grid", floatfmt=".2f"))


# Example usage with World Eater
row_A_items = ["Timeworn charm", "Shining charm", "Deviljho gem", "Deviljho scalp",
                "Deviljho hide", "Deviljho fang", "Hvy armor sphere"]
row_A_weights = [0.33, 0.19, 0.04, 0.08, 0.17, 0.08, 0.11]
row_B_items = ["Timeworn charm", "Shining charm", "Deviljho gem", "Deviljho scalp",
                "Deviljho hide", "Deviljho fang", "Hvy armor sphere"]
row_B_weights = [0.34, 0.11, 0.03, 0.2, 0.17, 0.06, 0.09]

average_loot(row_A_items, row_A_weights, row_B_items, row_B_weights)