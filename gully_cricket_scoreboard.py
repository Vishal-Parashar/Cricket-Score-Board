# ============================================================
#           GULLY CRICKET SCOREBOARD - Procedural Python
# ============================================================

# ---------- Global Data Stores ----------
team1_name = ""
team2_name = ""
total_overs = 0

# Team rosters (all players registered before match starts)
team1_players = []   # list of player names
team2_players = []   # list of player names

# Each team's innings data
innings = {
    1: {
        "team": "",
        "batting": {},        # { name: {runs, balls, fours, sixes, out_info} }
        "batting_order": [],  # names in order they came in to bat
        "bowling": {},        # { name: {overs_bowled, balls_bowled, runs_given, wickets} }
        "bowling_order": [],  # names in order they bowled
        "total_runs": 0,
        "wickets": 0,
        "overs": 0,
        "balls": 0,
        "extras": 0,
        "current_striker": "",
        "current_non_striker": "",
        "current_bowler": "",
        "ball_by_ball": []
    },
    2: {
        "team": "",
        "batting": {},
        "batting_order": [],
        "bowling": {},
        "bowling_order": [],
        "total_runs": 0,
        "wickets": 0,
        "overs": 0,
        "balls": 0,
        "extras": 0,
        "current_striker": "",
        "current_non_striker": "",
        "current_bowler": "",
        "ball_by_ball": []
    }
}


# ---------- Helper Functions ----------

def clear_line():
    print("-" * 62)

def double_line():
    print("=" * 62)

def banner(text):
    double_line()
    print(f"  {text}")
    double_line()

def pause():
    input("\n  Press Enter to continue...")

def get_int_input(prompt, min_val=1, max_val=9999):
    while True:
        val = input(f"  {prompt}: ").strip()
        if not val:
            print("  !! Please enter a number.")
            continue
        try:
            num = int(val)
            if num < min_val or num > max_val:
                print(f"  !! Enter a number between {min_val} and {max_val}.")
                continue
            return num
        except ValueError:
            print("  !! Invalid. Enter a valid number.")

def get_text_input(prompt):
    while True:
        val = input(f"  {prompt}: ").strip()
        if val:
            return val
        print("  !! Input cannot be empty. Try again.")

def get_yes_no(prompt):
    while True:
        val = input(f"  {prompt} (yes/no): ").strip().lower()
        if val in ["yes", "y"]:
            return True
        elif val in ["no", "n"]:
            return False
        print("  !! Enter yes or no.")

def pick_from_list(players, prompt, exclude=None):
    """
    Show numbered list and let user pick one.
    exclude: list of names already selected (shown as unavailable).
    Returns the chosen name.
    """
    if exclude is None:
        exclude = []
    print(f"\n  {prompt}")
    clear_line()
    for i, name in enumerate(players, 1):
        if name in exclude:
            print(f"    {i:>2}. {name}  [already selected]")
        else:
            print(f"    {i:>2}. {name}")
    clear_line()

    while True:
        choice = get_int_input(f"Enter number (1-{len(players)})", 1, len(players))
        chosen = players[choice - 1]
        if chosen in exclude:
            print(f"  !! {chosen} is already selected. Pick another.")
        else:
            return chosen


# ---------- Team Registration ----------

def register_team_players(team_name):
    """
    Ask for all player names for a team before the match starts.
    Returns a list of player names.
    """
    banner(f"REGISTER PLAYERS  —  {team_name}")
    print(f"  Enter all players for {team_name}.")
    print("  At least 2 players are required.\n")

    players = []

    while True:
        print(f"\n  Players added ({len(players)}):")
        if players:
            for i, p in enumerate(players, 1):
                print(f"    {i}. {p}")
        else:
            print("    (none yet)")

        print("\n  Options:")
        print("    1. Add a player")
        if len(players) >= 2:
            print("    2. Done — start match")

        choice = input("  Enter choice: ").strip()

        if choice == "1":
            name = get_text_input("Player name")
            if name in players:
                print(f"  !! {name} is already added.")
            else:
                players.append(name)
                print(f"  ✓ {name} added.")

        elif choice == "2" and len(players) >= 2:
            print(f"\n  ✓ {len(players)} players registered for {team_name}.")
            break
        else:
            if len(players) < 2:
                print("  !! Please add at least 2 players first.")
            else:
                print("  !! Invalid choice. Enter 1 or 2.")

    return players


# ---------- Match Setup ----------

def setup_match():
    global team1_name, team2_name, total_overs, team1_players, team2_players

    banner("MATCH SETUP")
    team1_name = get_text_input("Enter Team 1 name")
    team2_name = get_text_input("Enter Team 2 name")
    total_overs = get_int_input("Total overs per innings", 1, 50)
    innings[1]["team"] = team1_name
    innings[2]["team"] = team2_name

    print(f"\n  Match: {team1_name}  vs  {team2_name}  |  {total_overs} overs")
    pause()

    # Register all players for BOTH teams before match begins
    team1_players = register_team_players(team1_name)
    pause()
    team2_players = register_team_players(team2_name)
    pause()


# ---------- Toss ----------

def do_toss():
    banner("TOSS")
    print(f"  1. {team1_name}")
    print(f"  2. {team2_name}")
    winner_num = get_int_input("Who won the toss? Enter 1 or 2", 1, 2)
    toss_winner = team1_name if winner_num == 1 else team2_name

    print(f"\n  {toss_winner} won the toss!")
    print("  Choose to:")
    print("    1. Bat first")
    print("    2. Bowl first (field)")
    decision = get_int_input("Enter 1 or 2", 1, 2)

    if decision == 1:
        batting_first = toss_winner
    else:
        batting_first = team2_name if toss_winner == team1_name else team1_name

    bowling_first = team2_name if batting_first == team1_name else team1_name

    innings[1]["team"] = batting_first
    innings[2]["team"] = bowling_first

    print(f"\n  {batting_first} will BAT first.")
    print(f"  {bowling_first} will BOWL first.")
    pause()


# ---------- Get Team Rosters for an Innings ----------

def get_team_roster_for_innings(inn_num):
    """Return (bat_roster, bowl_roster) for the given innings number."""
    batting_team = innings[inn_num]["team"]
    if batting_team == team1_name:
        return team1_players, team2_players
    else:
        return team2_players, team1_players


# ---------- Scorekeeping Helpers ----------

def get_run_rate(inn):
    total_balls = inn["overs"] * 6 + inn["balls"]
    if total_balls == 0:
        return 0.0
    return round((inn["total_runs"] / total_balls) * 6, 2)

def required_run_rate():
    inn1 = innings[1]
    inn2 = innings[2]
    target = inn1["total_runs"] + 1
    runs_needed = target - inn2["total_runs"]
    balls_remaining = (total_overs * 6) - (inn2["overs"] * 6 + inn2["balls"])
    if balls_remaining <= 0:
        return 0.0
    return round((runs_needed / balls_remaining) * 6, 2)

def show_live_score(inn_num):
    inn = innings[inn_num]
    double_line()
    print(f"  🏏  {inn['team']}  |  Innings {inn_num}")
    print(f"  Score  : {inn['total_runs']}/{inn['wickets']}  "
          f"|  Overs: {inn['overs']}.{inn['balls']}  "
          f"|  RR: {get_run_rate(inn)}")
    print(f"  Extras : {inn['extras']}")
    if inn_num == 2:
        target = innings[1]["total_runs"] + 1
        runs_needed = target - inn["total_runs"]
        balls_rem = (total_overs * 6) - (inn["overs"] * 6 + inn["balls"])
        print(f"  Target : {target}  |  Need: {runs_needed} off {balls_rem} balls"
              f"  |  RRR: {required_run_rate()}")
    clear_line()
    striker = inn["current_striker"]
    non_striker = inn["current_non_striker"]
    if striker and striker in inn["batting"]:
        b = inn["batting"][striker]
        print(f"  * {striker:<24} {b['runs']:>3} ({b['balls']}b)  4s:{b['fours']} 6s:{b['sixes']}")
    if non_striker and non_striker in inn["batting"]:
        b = inn["batting"][non_striker]
        print(f"    {non_striker:<24} {b['runs']:>3} ({b['balls']}b)  4s:{b['fours']} 6s:{b['sixes']}")
    clear_line()
    bowler = inn["current_bowler"]
    if bowler and bowler in inn["bowling"]:
        bw = inn["bowling"][bowler]
        print(f"  Bowler : {bowler}  |  "
              f"{bw['overs_bowled']}.{bw['balls_bowled']} ov  |  "
              f"{bw['runs_given']}R  |  {bw['wickets']}W")
    double_line()


# ---------- Pick Players from Roster ----------

def pick_opening_batsmen(inn_num, bat_roster):
    inn = innings[inn_num]
    banner(f"SELECT OPENING BATSMEN  —  {inn['team']}")

    striker = pick_from_list(bat_roster, "Select STRIKER (faces first ball):", exclude=[])
    inn["batting"][striker] = {"runs": 0, "balls": 0, "fours": 0, "sixes": 0, "out_info": "not out"}
    inn["batting_order"].append(striker)
    inn["current_striker"] = striker
    print(f"  ✓ {striker} will face the first ball.")

    non_striker = pick_from_list(bat_roster, "Select NON-STRIKER:", exclude=[striker])
    inn["batting"][non_striker] = {"runs": 0, "balls": 0, "fours": 0, "sixes": 0, "out_info": "not out"}
    inn["batting_order"].append(non_striker)
    inn["current_non_striker"] = non_striker
    print(f"  ✓ {non_striker} is the non-striker.")


def pick_opening_bowler(inn_num, bowl_roster):
    inn = innings[inn_num]
    bowling_team = innings[3 - inn_num]["team"]
    banner(f"SELECT OPENING BOWLER  —  {bowling_team}")

    bowler = pick_from_list(bowl_roster, "Select opening BOWLER:")
    inn["bowling"][bowler] = {"overs_bowled": 0, "balls_bowled": 0, "runs_given": 0, "wickets": 0}
    inn["bowling_order"].append(bowler)
    inn["current_bowler"] = bowler
    print(f"  ✓ {bowler} will bowl the first over.")


def pick_next_batsman(inn_num, bat_roster):
    """Pick the next batsman from available roster players after a wicket."""
    inn = innings[inn_num]
    already_batted = list(inn["batting"].keys())
    available = [p for p in bat_roster if p not in already_batted]

    if not available:
        print("  !! No more batsmen available in the roster.")
        return None

    print("\n  --- WICKET! Select new batsman ---")
    new_bat = pick_from_list(available, "Select NEXT BATSMAN coming in:")
    inn["batting"][new_bat] = {"runs": 0, "balls": 0, "fours": 0, "sixes": 0, "out_info": "not out"}
    inn["batting_order"].append(new_bat)
    inn["current_striker"] = new_bat
    print(f"  ✓ {new_bat} is the new batsman on strike.")
    return new_bat


def pick_next_bowler(inn_num, bowl_roster):
    """Pick next bowler at end of each over (cannot bowl consecutive overs)."""
    inn = innings[inn_num]
    current = inn["current_bowler"]

    print("\n  --- End of Over: Select next BOWLER ---")
    clear_line()
    print(f"  {'#':<4} {'NAME':<24} {'STATS'}")
    clear_line()
    for i, name in enumerate(bowl_roster, 1):
        tag = ""
        if name == current:
            tag = "  <-- just bowled (cannot bowl again)"
        if name in inn["bowling"]:
            bw = inn["bowling"][name]
            stats = f"{bw['overs_bowled']}.{bw['balls_bowled']} ov, {bw['runs_given']}R, {bw['wickets']}W"
        else:
            stats = "not bowled yet"
        print(f"  {i:<4} {name:<24} {stats}{tag}")
    clear_line()

    while True:
        choice = get_int_input(f"Enter number (1-{len(bowl_roster)})", 1, len(bowl_roster))
        chosen = bowl_roster[choice - 1]
        if chosen == current:
            print(f"  !! {chosen} bowled the last over. Cannot bowl consecutive overs.")
        else:
            if chosen not in inn["bowling"]:
                inn["bowling"][chosen] = {"overs_bowled": 0, "balls_bowled": 0, "runs_given": 0, "wickets": 0}
                inn["bowling_order"].append(chosen)
            inn["current_bowler"] = chosen
            print(f"  ✓ {chosen} will bowl the next over.")
            break


def change_bowler_manually(inn_num, bowl_roster):
    """Mid-over bowler change (e.g. injury)."""
    inn = innings[inn_num]
    print("\n  --- Change Bowler (mid-over) ---")
    clear_line()
    print(f"  {'#':<4} {'NAME':<24} {'STATS'}")
    clear_line()
    for i, name in enumerate(bowl_roster, 1):
        cur_tag = "  <-- current" if name == inn["current_bowler"] else ""
        if name in inn["bowling"]:
            bw = inn["bowling"][name]
            stats = f"{bw['overs_bowled']}.{bw['balls_bowled']} ov, {bw['runs_given']}R, {bw['wickets']}W"
        else:
            stats = "not bowled yet"
        print(f"  {i:<4} {name:<24} {stats}{cur_tag}")
    clear_line()

    choice = get_int_input(f"Select bowler (1-{len(bowl_roster)})", 1, len(bowl_roster))
    chosen = bowl_roster[choice - 1]
    if chosen not in inn["bowling"]:
        inn["bowling"][chosen] = {"overs_bowled": 0, "balls_bowled": 0, "runs_given": 0, "wickets": 0}
        inn["bowling_order"].append(chosen)
    inn["current_bowler"] = chosen
    print(f"  ✓ {chosen} is now bowling.")


# ---------- Ball Recording ----------

def record_ball(inn_num, ball_event):
    inn = innings[inn_num]
    striker = inn["current_striker"]
    bowler = inn["current_bowler"]

    if not striker or not bowler:
        print("  !! Striker or bowler not set.")
        return False

    bat = inn["batting"][striker]
    bwl = inn["bowling"][bowler]
    ball_event = ball_event.strip().lower()
    legal_ball = True

    if ball_event == "w":
        bat["balls"] += 1
        bwl["balls_bowled"] += 1
        bwl["wickets"] += 1
        inn["wickets"] += 1
        print(f"\n  How was {striker} dismissed?")
        print("  1. Bowled")
        print("  2. Caught")
        print("  3. Run Out")
        print("  4. LBW")
        print("  5. Hit Wicket")
        print("  6. Other")
        d = get_int_input("Choice", 1, 6)
        dismissals = {
            1: "b " + bowler,
            2: "c & b " + bowler,
            3: "run out",
            4: "lbw b " + bowler,
            5: "hit wicket b " + bowler,
            6: "out"
        }
        bat["out_info"] = dismissals[d]
        inn["ball_by_ball"].append("W")
        print(f"  ✗  {striker} is OUT!  ({bat['out_info']})")

    elif ball_event in ["wd", "wide"]:
        inn["total_runs"] += 1
        inn["extras"] += 1
        bwl["runs_given"] += 1
        legal_ball = False
        inn["ball_by_ball"].append("wd")
        print("  Wide! +1 extra")

    elif ball_event in ["nb", "no ball"]:
        inn["total_runs"] += 1
        inn["extras"] += 1
        bwl["runs_given"] += 1
        legal_ball = False
        inn["ball_by_ball"].append("nb")
        print("  No Ball! +1 extra  (free hit next ball)")

    elif ball_event in ["lb", "leg bye"]:
        runs = get_int_input("Leg bye runs scored", 0, 6)
        inn["total_runs"] += runs
        inn["extras"] += runs
        inn["ball_by_ball"].append(f"lb{runs}")
        print(f"  Leg Bye: +{runs}")

    elif ball_event.isdigit() and 0 <= int(ball_event) <= 6:
        runs = int(ball_event)
        bat["runs"] += runs
        bat["balls"] += 1
        bwl["balls_bowled"] += 1
        bwl["runs_given"] += runs
        inn["total_runs"] += runs
        if runs == 4:
            bat["fours"] += 1
        if runs == 6:
            bat["sixes"] += 1
        inn["ball_by_ball"].append(str(runs))
        print(f"  {striker}: {runs} run(s)." if runs > 0 else "  Dot ball.")
        if runs % 2 != 0:
            inn["current_striker"], inn["current_non_striker"] = \
                inn["current_non_striker"], inn["current_striker"]
    else:
        print("  !! Unknown input. Use: 0 1 2 3 4 6  W  wd  nb  lb")
        return False

    if legal_ball and ball_event != "w":
        bwl["overs_bowled"] = bwl["balls_bowled"] // 6

    if legal_ball:
        inn["balls"] += 1
        if inn["balls"] == 6:
            inn["balls"] = 0
            inn["overs"] += 1
            bwl["overs_bowled"] = bwl["balls_bowled"] // 6
            print(f"\n  *** End of Over {inn['overs']} ***")
            inn["current_striker"], inn["current_non_striker"] = \
                inn["current_non_striker"], inn["current_striker"]
            return "end_of_over"

    return True


# ---------- Full Scorecard ----------

def show_full_scorecard(inn_num):
    inn = innings[inn_num]
    double_line()
    print(f"  SCORECARD  —  {inn['team']}  (Innings {inn_num})")
    double_line()
    print(f"  Total  : {inn['total_runs']}/{inn['wickets']}  "
          f"Overs: {inn['overs']}.{inn['balls']}  "
          f"RR: {get_run_rate(inn)}")
    print(f"  Extras : {inn['extras']}")
    clear_line()
    print(f"  {'BATSMAN':<24} {'R':>4} {'B':>4} {'4s':>4} {'6s':>4}   STATUS")
    clear_line()
    for name in inn["batting_order"]:
        b = inn["batting"][name]
        print(f"  {name:<24} {b['runs']:>4} {b['balls']:>4} {b['fours']:>4} {b['sixes']:>4}   {b['out_info']}")
    clear_line()
    print(f"\n  {'BOWLER':<24} {'O':>6} {'R':>5} {'W':>4}   ECON")
    clear_line()
    for name in inn["bowling_order"]:
        bw = inn["bowling"][name]
        total_b = bw["overs_bowled"] * 6 + bw["balls_bowled"]
        econ = round((bw["runs_given"] / total_b) * 6, 2) if total_b > 0 else 0.0
        print(f"  {name:<24} {bw['overs_bowled']}.{bw['balls_bowled']:<4} "
              f"{bw['runs_given']:>5} {bw['wickets']:>4}   {econ}")
    clear_line()
    if inn["ball_by_ball"]:
        print("\n  Ball-by-ball:")
        balls = inn["ball_by_ball"]
        for i in range(0, len(balls), 6):
            over_num = i // 6 + 1
            over_balls = balls[i:i + 6]
            over_runs = sum(
                int(b) if b.isdigit() else (1 if b in ["wd", "nb"] else 0)
                for b in over_balls
            )
            print(f"    Over {over_num:>2}: {' | '.join(over_balls)}   [{over_runs} runs]")
    double_line()


# ---------- Match Result ----------

def show_match_result():
    inn1 = innings[1]
    inn2 = innings[2]
    banner("🏆  MATCH RESULT  🏆")
    print(f"\n  {inn1['team']:<26} {inn1['total_runs']}/{inn1['wickets']}"
          f"  in  {inn1['overs']}.{inn1['balls']} overs")
    print(f"  {inn2['team']:<26} {inn2['total_runs']}/{inn2['wickets']}"
          f"  in  {inn2['overs']}.{inn2['balls']} overs")
    clear_line()
    if inn2["total_runs"] > inn1["total_runs"]:
        wkts = max(0, len(inn2["batting"]) - inn2["wickets"] - 1)
        print(f"\n  🏆  {inn2['team']}  WON  by {wkts} wickets!")
    elif inn1["total_runs"] > inn2["total_runs"]:
        diff = inn1["total_runs"] - inn2["total_runs"]
        print(f"\n  🏆  {inn1['team']}  WON  by {diff} runs!")
    else:
        print("\n  🤝  MATCH TIED!")
    double_line()
    print("\n  ---- FULL SCORECARD ----\n")
    show_full_scorecard(1)
    print()
    show_full_scorecard(2)


# ---------- Innings Menu ----------

def innings_menu(inn_num):
    inn = innings[inn_num]
    bat_roster, bowl_roster = get_team_roster_for_innings(inn_num)

    banner(f"INNINGS {inn_num}  —  {inn['team']}  BATTING")

    # Pick all opening players from the registered roster
    pick_opening_batsmen(inn_num, bat_roster)
    pick_opening_bowler(inn_num, bowl_roster)
    pause()

    while True:
        # End: overs completed
        if inn["overs"] >= total_overs:
            print(f"\n  *** {total_overs} overs completed. Innings over! ***")
            break

        # End: all out (no more batsmen available)
        already_batted = list(inn["batting"].keys())
        available_batsmen = [p for p in bat_roster if p not in already_batted]
        if inn["wickets"] >= len(already_batted) - 1 and not available_batsmen:
            print("\n  *** All out! ***")
            break

        # Team 2: target achieved
        if inn_num == 2:
            target = innings[1]["total_runs"] + 1
            if inn["total_runs"] >= target:
                wickets_left = max(0, len(inn["batting"]) - inn["wickets"] - 1)
                print(f"\n  🎉  {inn['team']}  wins by {wickets_left} wickets!")
                break

        show_live_score(inn_num)

        print("  ACTIONS:")
        print("  [0-6]  Runs scored  (0 = dot ball)")
        print("  [W]    Wicket")
        print("  [wd]   Wide")
        print("  [nb]   No Ball")
        print("  [lb]   Leg Bye")
        print("  [cb]   Change Bowler (mid-over)")
        print("  [sc]   Show Full Scorecard")
        print("  [end]  End Innings manually")

        action = input("\n  Enter action: ").strip().lower()

        if action == "end":
            if get_yes_no("End innings now?"):
                break

        elif action == "cb":
            change_bowler_manually(inn_num, bowl_roster)

        elif action == "sc":
            show_full_scorecard(inn_num)
            pause()

        else:
            result = record_ball(inn_num, action)

            # After end of over — pick next bowler from list
            if result == "end_of_over" and inn["overs"] < total_overs:
                pick_next_bowler(inn_num, bowl_roster)

            # After wicket — pick next batsman from list
            if result and action.lower() == "w":
                already_batted = list(inn["batting"].keys())
                remaining = [p for p in bat_roster if p not in already_batted]
                if remaining:
                    pick_next_batsman(inn_num, bat_roster)

    show_full_scorecard(inn_num)
    pause()


# ---------- Main ----------

def main():
    banner("🏏  GULLY CRICKET SCOREBOARD  🏏")
    print("  Welcome! Track every ball of your gully cricket match.")
    pause()

    # Step 1: Match info + register ALL team players upfront
    setup_match()

    # Step 2: Toss
    do_toss()

    # Step 3: 1st Innings
    innings_menu(1)

    # Step 4: Innings break
    banner("INNINGS BREAK")
    target = innings[1]["total_runs"] + 1
    print(f"\n  {innings[2]['team']} needs {target} runs to win in {total_overs} overs.")
    pause()

    # Step 5: 2nd Innings
    innings_menu(2)

    # Step 6: Result
    show_match_result()
    print("\n  Thanks for using Gully Cricket Scoreboard! 🏏\n")


# ---------- Entry Point ----------
if __name__ == "__main__":
    main()
