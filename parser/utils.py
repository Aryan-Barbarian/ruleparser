


def enumerate_combinations(possible_vals, repeats_allowed=False) :
	
	ans = list()
	if len(possible_vals) == 0:
		return [ans]
	
	first = possible_vals.pop(0)

	if len(first) == 0:
		return list();

	for possible in first:
		if not repeats_allowed:
			rest = [[possible_val for possible_val in entry if possible != possible_val] for entry in possible_vals]
		other_possibilities = enumerate_combinations(rest, repeats_allowed)
		for other in other_possibilities:
			other.insert(0, possible)
			ans.append(other)
	return ans

