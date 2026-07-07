import os

LINES = {
    "Blue Line 1": {"stations": [], "times": [], "interchange": []},
    "Blue Line 2": {"stations": [], "times": [], "interchange": []},
    "Magenta Line": {"stations": [], "times": [], "interchange": []},
}


def add_station(line, station_name, next_station, travel_time, inter_status):
    stations = LINES[line]["stations"]

    if not stations:
        stations.append(station_name)

    if next_station not in stations:
        stations.append(next_station)

    LINES[line]["times"].append(travel_time)
    LINES[line]["interchange"].append(inter_status)


def read_file(filename = "metro_data.txt"):

    try:
        with open(filename, "r") as f:
            lines = f.readlines()

            for line in lines:
                parts = [p.strip() for p in line.strip().split(",")]

                if len(parts) < 5:
                    continue

                line_name = parts[0]
                station_name = parts[1]
                next_station = parts[2]
                time_part = parts[3].replace('min', '').strip()
                interchange_status = parts[4]

                try:
                    travel_time = int(time_part)
                except ValueError:
                    continue

                if line_name in LINES:
                    add_station(line_name, station_name, next_station, travel_time, interchange_status)

    except FileNotFoundError:
        print(f"Error: The file was not found at .")


read_file()


def hour_cons(h, m):
    return h * 60 + m


def min_cons(total_min):
    total_min = total_min % 1440
    h = total_min // 60
    m = total_min % 60
    return f"{h:02d}:{m:02d}", h, m


def get_freq(curr_time_min):
    morning_peak = (480 <= curr_time_min <= 600)
    evening_peak = (1020 <= curr_time_min <= 1140)

    if morning_peak or evening_peak:
        return 4
    else:
        return 8


def line_data(line_name):
    line_name = line_name.lower().strip()
    for name in LINES:
        if name.lower() == line_name:
            return LINES[name]["stations"], LINES[name]["times"]
    return None, None


def find_line(station):
    found_lines = []
    for name in LINES:
        if station in LINES[name]["stations"]:
            found_lines.append(name)
    return found_lines


def cal_time(start_st, end_st, st_list, t_list):
    try:
        start_idx = st_list.index(start_st)
        end_idx = st_list.index(end_st)
    except ValueError:
        return

    total_time = 0

    if start_idx <= end_idx:
        for i in range(start_idx, end_idx):
            total_time += t_list[i]
    else:
        for i in range(end_idx, start_idx):
            total_time += t_list[i]

    return total_time


def next_metrot(station_name, curr_time_min, line_name):

    SERVICE_START = 360
    SERVICE_END = 1380

    if curr_time_min >= SERVICE_END:
        return None, "Service has ended for today."

    departure = SERVICE_START

    while departure < curr_time_min:
        frequency = get_freq(departure)
        departure += frequency

    if departure > SERVICE_END:
        return None, "Service has ended for today."
    
    frequency = get_freq(departure)

    return departure, frequency


def calculate_fare(travel_minutes):

    if travel_minutes <= 4:
        return 10
    elif travel_minutes <= 9:
        return 20
    elif travel_minutes <= 22:
        return 30
    elif travel_minutes <= 38:
        return 40
    elif travel_minutes <= 58:
        return 50
    else:
        return 60


def find_interchange(line_a, line_b):

    if line_a not in LINES or line_b not in LINES or line_a == line_b:
        return []

    stations_a = LINES[line_a]["stations"]
    stations_b = LINES[line_b]["stations"]
    inter_a = LINES[line_a]["interchange"]
    inter_b = LINES[line_b]["interchange"]

    candidates = []
    for station in set(stations_a) & set(stations_b):
        idx_a = stations_a.index(station)
        idx_b = stations_b.index(station)

        flagged = False
        if idx_a > 0 and inter_a[idx_a - 1] == "Yes":
            flagged = True
        if idx_a < len(inter_a) and inter_a[idx_a] == "Yes":
            flagged = True
        if idx_b > 0 and inter_b[idx_b - 1] == "Yes":
            flagged = True
        if idx_b < len(inter_b) and inter_b[idx_b] == "Yes":
            flagged = True

        if flagged:
            candidates.append(station)

    return candidates


def cal_journey(source, destination, current_time_str):

    try:
        curr_time_min = hour_cons(*map(int, current_time_str.split(':')))
    except ValueError:
        return "Invalid time format."

    source_lines = find_line(source)
    dest_lines = find_line(destination)

    if not source_lines:
        return "Source station not found."
    if not dest_lines:
        return "Destination station not found."

    common_lines = [line for line in source_lines if line in dest_lines]

    if common_lines:
        line_name = common_lines[0]
        st_list, t_list = line_data(line_name)

        next_depart, frequency = next_metrot(source, curr_time_min, line_name)
        if next_depart is None:
            return frequency

        travel_duration = cal_time(source, destination, st_list, t_list)
        if travel_duration is None:
            return "Travel time calculation error."

        final_arrival = next_depart + travel_duration
        total_time = final_arrival - curr_time_min

        return {
            "type": "DIRECT",
            "line": line_name,
            "next_depart": next_depart,
            "final_arrival": final_arrival,
            "total_time": total_time,
            "travel_duration": travel_duration,
            "frequency": frequency,
            "fare": calculate_fare(travel_duration),
        }

    best_result = None

    for source_line in source_lines:
        for dest_line in dest_lines:
            if source_line == dest_line:
                continue

            for interchange_st in find_interchange(source_line, dest_line):
                st_list1, t_list1 = line_data(source_line)
                st_list2, t_list2 = line_data(dest_line)

                time1 = cal_time(source, interchange_st, st_list1, t_list1)
                if time1 is None:
                    continue

                next_depart1, freq1 = next_metrot(source, curr_time_min, source_line)
                if next_depart1 is None:
                    continue

                arrival_interchange = next_depart1 + time1

                time2 = cal_time(interchange_st, destination, st_list2, t_list2)
                if time2 is None:
                    continue

                departure_check_time = arrival_interchange + 3

                next_depart2, freq2 = next_metrot(interchange_st, departure_check_time, dest_line)
                if next_depart2 is None:
                    continue

                final_arrival = next_depart2 + time2
                total_time = final_arrival - curr_time_min

                candidate = {
                    "type": "INTERCHANGE",
                    "source_line": source_line,
                    "dest_line": dest_line,
                    "interchange_st": interchange_st,
                    "next_depart1": next_depart1,
                    "arrival_interchange": arrival_interchange,
                    "next_depart2": next_depart2,
                    "final_arrival": final_arrival,
                    "total_time": total_time,
                    "time1": time1,
                    "time2": time2,
                    "fare": calculate_fare(time1 + time2),
                }

                if best_result is None or candidate["total_time"] < best_result["total_time"]:
                    best_result = candidate

    if best_result is not None:
        return best_result

    return "No route found between these stations."


def journey_planner():

    print("METRO JOURNEY PLANNER")

    print("\n 1. NEXT METRO TIMING")

    try:
        station_input = input("Enter Station: ").strip()
        time_str_next_metro = input("Enter Current Time (HH:MM): ").strip()
        try:
            curr_time_min = hour_cons(*map(int, time_str_next_metro.split(':')))
        except ValueError:
            print("Invalid time format. ")
            return

        possible_lines = find_line(station_input)

        if not possible_lines:
            print("Station not found in the metro network.")
            return

        line_input = possible_lines[0]
        st_list, t_list = line_data(line_input)

        next_depart, frequency = next_metrot(station_input, curr_time_min, line_input)

        if next_depart is None:
            print(f"Next metro at {station_input}: {frequency}")
            return

        print(f"Station: {station_input} ({line_input})")
        print(f"Frequency at this time: {frequency} min")
        print(f"Next metro departs at: {min_cons(next_depart)[0]}")

        subsequent_depart = next_depart
        subsequent_times = []
        for _ in range(3):
            step_frequency = get_freq(subsequent_depart)
            subsequent_depart += step_frequency
            if subsequent_depart <= 1380:
                subsequent_times.append(min_cons(subsequent_depart)[0])
            else:
                break

        if subsequent_times:
            print(f"Subsequent metros: {', '.join(subsequent_times)}")

    except Exception as e:
        print(f"An unexpected error occurred during Next Metro calculation. Error: {e}")
        return

    print(" 2. RIDER JOURNEY PLANNER")

    try:
        source = input("Enter Source Station: ").strip()
        destination = input("Enter Destination Station: ").strip()
        time_journey = input("Enter Time of Travel (HH:MM): ").strip()

        result = cal_journey(source, destination, time_journey)

        if isinstance(result, str):
            print("Journey Plan: Failed")
            print(result)
            return

        print("Journey Plan:")

        if result["type"] == "DIRECT":

            wait_time = result['next_depart'] - hour_cons(*map(int, time_journey.split(':')))

            print(f"Start at {source} ({result['line']})")
            print(f"Next metro departs at: {min_cons(result['next_depart'])[0]}")
            print(f"Arrive at {destination} at {min_cons(result['final_arrival'])[0]}")
            print(f"Total travel time: {result['total_time']} min")
            print(f"Wait at {source}: {wait_time} min")
            print(f"Travel: {result['travel_duration']} min")
            print(f"Fare: Rs {result['fare']}")

        elif result["type"] == "INTERCHANGE":

            wait_time1 = result['next_depart1'] - hour_cons(*map(int, time_journey.split(':')))
            wait_time2 = result['next_depart2'] - (result['arrival_interchange'] + 3)

            print(f"Start at {source} ({result['source_line']})")
            print(f"Next metro departs at: {min_cons(result['next_depart1'])[0]}")
            print(f"Arrive at {result['interchange_st']} at {min_cons(result['arrival_interchange'])[0]}")

            print(f"Transfer to {result['dest_line']} Line")
            print(f"Next {result['dest_line']} metro departs at: {min_cons(result['next_depart2'])[0]}")

            print(f"Arrive at {destination} at {min_cons(result['final_arrival'])[0]}")
            print(f"\nTotal travel time: {result['total_time']} min")
            print(f"Wait at {source}: {wait_time1} min")
            print(f"Platform Change: 3 min")
            print(f"Wait at Interchange: {wait_time2} min")
            print(f"Travel: {result['time1'] + result['time2']} min")
            print(f"Fare: Rs {result['fare']}")

    except Exception as e:
        print(f"An unexpected error occurred during Journey Planner calculation. Error: {e}")


if __name__ == "__main__":
    journey_planner()
