valve_factors = {
    "A": {
        # "0":0,
        # "1":0,
        # "...":0,
        # "3":0
    },
    "B": {},
    "C": {},
    "D": {},
}


def compute(vertices):# -> list[bool] | list:
    # child nodes for each node
    paths = {}
    for i in vertices:
        if i["fromNode"] not in paths:
            paths[i["fromNode"]] = []
        paths[i["fromNode"]].append(i["toNode"])

    # call recursive function for each valve (get valve factors for each exit)
    for i in range(12):
        recurse(str(i), str(i), 1.0, paths)

    # brute force valves with given factors to match result
    return find_valve_comb()


def find_valve_comb():# -> list[bool] | list:
    for count in range(2**12 + 1):
        comb = [bool(int(x)) for x in f"{count:012b}"]

        """
        print(f"Count is: {count}")
        print(f"Combination is: ", end="")
        print(*comb, sep=" ")

        print(f"Value for A is: {value(comb,valve_factors['A'])}")
        print(f"Value for B is: {value(comb,valve_factors['B'])}")
        print(f"Value for C is: {value(comb,valve_factors['C'])}")
        print(f"Value for D is: {value(comb,valve_factors['D'])}")
        """

        if (
            value(comb, valve_factors["A"]) == 8
            and value(comb, valve_factors["B"]) == 8
            and value(comb, valve_factors["C"]) == 10
            and value(comb, valve_factors["D"]) == 6
        ):
            return comb
        count += 1

    return []


def value(bool_array: list[bool], dic: dict[str, float]) -> int:
    x = 0
    for i in range(len(bool_array)):
        if str(i) in dic:
            x += bool_array[i] * dic[str(i)] * 4
    return int(x)


def recurse(start: str, origin: str, factor: float, paths: dict) -> None:
    if start in ["A", "B", "C", "D"]:
        if not origin in valve_factors[start]:
            valve_factors[start][origin] = 0

        valve_factors[start][origin] += factor

    elif len(paths[start]) > 1:
        recurse(paths[start][0], origin, factor * 0.5, paths)
        recurse(paths[start][1], origin, factor * 0.5, paths)
    else:
        recurse(paths[start][0], origin, factor, paths)
