from ps1_partition import get_partitions
import time
import os

#================================
# Part A: Transporting Space Cows
#================================

def load_cows(filename:str) -> dict[str,int]:
    if not isinstance(filename, str):
        raise TypeError("filename must be a string")
    if len(filename) == 0:
        raise ValueError("filename cannot be an empty string")
    _, ext = os.path.splitext(filename)
    if ext.lower() != '.txt':
        raise ValueError("filename must be a .txt file")
    with open(os.path.abspath(filename), 'r') as file:
        data:list[str] = file.readlines()
    if len(data) == 0:
        raise ValueError("file is empty")
    cow_dict:dict[str,int] = {}
    for data_line in data:
        name, weight = data_line.strip().replace('\n','').split(',')
        cow_dict[name] = int(weight)
    return cow_dict

def greedy_cow_transport(cows:dict[str,int],limit:int=10) -> list[list[str]]:
    current_trip:list[str] = []
    current_weight:int = 0
    trips_list:list[list[str]] = []
    cows_copy:dict[str,int] = cows.copy()

    while len(cows_copy) > 0:
        cows_sorted:list[tuple[str,int]] = sorted(cows_copy.items(), key=lambda item: item[1], reverse=True)
        for cow, weight in cows_sorted:
            if current_weight == limit:
                break
            if current_weight + weight <= limit:
                current_trip.append(cow)
                current_weight += weight
        trips_list.append(current_trip)
        for cow in current_trip:
            del cows_copy[cow]
        current_trip:list[str] = []
        current_weight:int = 0

    return trips_list

def brute_force_cow_transport(cows:dict[str,int],limit:int=10) -> list[list[str]]:
    cows_copy:dict[str,int] = cows.copy()
    cows_sorted:list[tuple[str,int]] = sorted(cows_copy.items(), key=lambda item: item[1], reverse=True)
    cows_list:list[str] = [cow for cow, weight in cows_sorted]
    for partition in get_partitions(cows_list):
        for trip in partition:
            trip_weight = sum(cows[cow] for cow in trip)
            if trip_weight > limit:
                break
        else:
            return partition
    return []

def compare_cow_transport_algorithms(filename:str) -> None:
    cows:dict[str,int] = load_cows(filename)
    start_greedy:float = time.time()
    greedy_result:list[list[str]] = greedy_cow_transport(cows)
    end_greedy:float = time.time()
    start_brute:float = time.time()
    brute_result:list[list[str]] = brute_force_cow_transport(cows)
    end_brute:float = time.time()
    print("\nGreedy Algorithm:")
    print(f"Number of trips: {len(greedy_result)}")
    print(f"Time taken: {end_greedy - start_greedy} seconds")
    print("\nBrute Force Algorithm:")
    print(f"Number of trips: {len(brute_result)}")
    print(f"Time taken: {end_brute - start_brute} seconds")

if __name__ == '__main__':
    compare_cow_transport_algorithms("6.0002\\ps1\\ps1_cow_data.txt")
    compare_cow_transport_algorithms("6.0002\\ps1\\ps1_cow_data_2.txt")
