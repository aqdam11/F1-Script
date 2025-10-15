drivers = {
    "Oscar Piastri": 324,
    "Lando Norris": 299,
    "Max Verstappen": 255,
    "George Russel": 212,
    "Charles Leclerc": 165,
    "Lewis Hamilton": 121,
    "Kimi Antoneli": 78,
    "Alexander Albon": 70,
    "Isack Hadjar": 39,
    "Nico Hulkenberg": 37,
    "Lance Stroll": 32,
    "Carlos Sainz": 31,
    "Liam Lawson": 30,
    "Fernando Alonso": 30,
    "Esteban Ocon": 28,
    "Pierre Gasly": 20,
    "Yuki Tsunoda": 20,
    "Gabriel Bortoleto": 18,
    "Oliver Bearman": 16,
    "Franco Coalopinto": 0
}

# Points for positions 1..10 (11..20 = 0)
points_system = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]

# map position -> points for positions 1..20
pos_points = {pos: (points_system[pos-1] if 1 <= pos <= 10 else 0) for pos in range(1, 21)}

remaining_races = 7
max_points_per_driver = remaining_races * pos_points[1]  # usually 7 * 25 = 175

# Ask user for input
driver_name = input("Enter the driver name: ")

if driver_name not in drivers:
    print("Driver not found!")
else:
    current_points = drivers[driver_name]
    max_possible_points = current_points + max_points_per_driver

    print(f"\n--- Championship Chances for {driver_name} ---")
    print(f"Current points: {current_points}")
    print(f"Maximum possible points (if {driver_name} scores the maximum in remaining races): {max_possible_points}")

    # Find the current leader
    leader = max(drivers, key=drivers.get)
    leader_points = drivers[leader]

    print(f"Current leader: {leader} with {leader_points} points")

    # Conditions for winning
    needed_gap = max_possible_points - leader_points

    if needed_gap <= 0 and driver_name != leader:
        print(f"❌ {driver_name} cannot mathematically win the championship.")
    else:
        print(f"✅ {driver_name} can still win!")
        print("To win, {0} must score close to maximum points, while rivals must stay below {1}.".format(
            driver_name, max_possible_points))

        # Simple estimated probability (just for fun)
        chance = round((needed_gap / max_points_per_driver) * 100, 2)
        if chance < 0:
            chance = 5.0
        elif chance > 100:
            chance = 95.0
        print(f"Estimated winning chance: {chance}%")

    # Show scenario per race for the selected driver (we assume driver takes the highest available points per race
    # until their 'max' is reached — in practice this will usually be P1 in all races)
    print("\n--- Assumed {0} finishes (to reach max_possible_points) ---".format(driver_name))
    needed_for_driver = max_possible_points - current_points
    driver_plan = []
    for r in range(remaining_races):
        # pick the best (lowest number) position that doesn't exceed remaining need
        chosen_pos = None
        for pos in range(1, 21):
            if pos_points[pos] <= needed_for_driver:
                chosen_pos = pos
                break
        if chosen_pos is None:
            chosen_pos = 11  # outside top10
        driver_plan.append(chosen_pos)
        needed_for_driver -= pos_points[chosen_pos]
    for i, p in enumerate(driver_plan, start=1):
        if p <= 10:
            print(f"  Race {i}: P{p} ({pos_points[p]} pts)")
        else:
            print(f"  Race {i}: outside top 10 (0 pts)")

    # Show max allowed for rivals per race taking into account that the selected driver occupies
    # the positions in driver_plan (so rivals cannot also be P1 in races where the selected driver is P1).
    print("\n--- Rivals Maximum Allowed Finishes (per race, independent per rival) ---")
    for rival, rival_points in drivers.items():
        if rival == driver_name:
            continue
        # Only consider rivals who currently have >= the selected driver's current points (close threats)
        if rival_points < current_points:
            continue

        max_allowed_total = max_possible_points - 1  # rival must stay strictly below this
        allowed_gap = max_allowed_total - rival_points
        if allowed_gap < 0:
            print(f"\n{rival} (current {rival_points} pts) already exceeds the allowed total -> {rival} would need to score negative points (impossible)")
            continue

        print(f"\n{rival} (current {rival_points} pts) can earn at most {allowed_gap} more points:")
        remaining = allowed_gap
        for race_idx in range(remaining_races):
            reserved_pos = driver_plan[race_idx]
            # available positions in this race (1..20) except reserved_pos
            chosen_pos = None
            for pos in range(1, 21):
                if pos == reserved_pos:
                    continue
                pts = pos_points[pos]
                # pick the best (lowest pos number) position that doesn't exceed remaining budget
                if pts <= remaining:
                    chosen_pos = pos
                    break
            if chosen_pos is None:
                # can't afford any points in this race
                print(f"  Race {race_idx+1}: must finish outside top 10 (0 points)")
            else:
                if chosen_pos <= 10:
                    print(f"  Race {race_idx+1}: at most P{chosen_pos} ({pos_points[chosen_pos]} pts)")
                    remaining -= pos_points[chosen_pos]
                else:
                    print(f"  Race {race_idx+1}: must finish outside top 10 (0 points)")
                    # remaining unchanged (0 pts)
            if remaining <= 0:
                # remaining races must be outside top10
                for r in range(race_idx+1, remaining_races):
                    print(f"  Race {r+1}: must finish outside top 10 (0 points)")
                break

