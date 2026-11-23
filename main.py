"""
Courier Planning System
Student: Hirday
Roll No.: 2501060202

Algorithms:
1. Merge Sort: orders parcels by priority (high first), then deadline (early first).
2. 0/1 Knapsack (Dynamic Programming): selects the best-value set of parcels
   that fits the vehicle's weight capacity.
3. Dijkstra: finds shortest paths between locations in a weighted road graph.
4. Nearest Neighbour: builds an approximate multi-stop delivery route.

Run:
    python main.py
Optional:
    python main.py --capacity 30
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple
import argparse
import csv
import heapq
import time


@dataclass
class Parcel:
    parcel_id: str
    destination: str
    weight: int
    value: int
    priority: int
    deadline: str


def merge_sort(items, key):
    """Return a stable sorted copy using Merge Sort."""
    if len(items) <= 1:
        return items[:]
    mid = len(items) // 2
    left = merge_sort(items[:mid], key)
    right = merge_sort(items[mid:], key)
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def parcel_sort_key(parcel):
    # Higher priority first; for equal priority, earlier deadline first.
    return (-parcel.priority, parcel.deadline, parcel.parcel_id)


def knapsack(parcels: List[Parcel], capacity: int):
    """0/1 Knapsack DP. Returns selected parcels and maximum total value."""
    n = len(parcels)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        p = parcels[i - 1]
        for cap in range(capacity + 1):
            dp[i][cap] = dp[i - 1][cap]
            if p.weight <= cap:
                dp[i][cap] = max(
                    dp[i][cap],
                    p.value + dp[i - 1][cap - p.weight]
                )

    selected = []
    cap = capacity
    for i in range(n, 0, -1):
        if dp[i][cap] != dp[i - 1][cap]:
            p = parcels[i - 1]
            selected.append(p)
            cap -= p.weight

    selected.reverse()
    return selected, dp[n][capacity]


def dijkstra(graph: Dict[str, Dict[str, int]], start: str):
    """Return shortest distances and predecessor map from start."""
    distances = {node: float("inf") for node in graph}
    previous = {node: None for node in graph}
    distances[start] = 0
    queue = [(0, start)]

    while queue:
        current_distance, node = heapq.heappop(queue)
        if current_distance != distances[node]:
            continue
        for neighbour, weight in graph[node].items():
            new_distance = current_distance + weight
            if new_distance < distances[neighbour]:
                distances[neighbour] = new_distance
                previous[neighbour] = node
                heapq.heappush(queue, (new_distance, neighbour))
    return distances, previous


def reconstruct_path(previous, destination):
    path = []
    node = destination
    while node is not None:
        path.append(node)
        node = previous[node]
    return list(reversed(path))


def nearest_neighbour(graph, start, destinations):
    """
    Build a route by repeatedly visiting the nearest unvisited destination.
    Distances between every pair are calculated with Dijkstra.
    """
    remaining = set(destinations)
    route = [start]
    total_distance = 0
    current = start

    while remaining:
        distances, _ = dijkstra(graph, current)
        next_stop = min(remaining, key=lambda node: (distances[node], node))
        if distances[next_stop] == float("inf"):
            raise ValueError(f"No route from {current} to {next_stop}")
        total_distance += distances[next_stop]
        route.append(next_stop)
        remaining.remove(next_stop)
        current = next_stop

    distances, _ = dijkstra(graph, current)
    if start in distances and distances[start] != float("inf"):
        total_distance += distances[start]
        route.append(start)
    return route, total_distance


def load_parcels(csv_path):
    parcels = []
    with open(csv_path, newline="", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            parcels.append(Parcel(
                row["parcel_id"], row["destination"], int(row["weight"]),
                int(row["value"]), int(row["priority"]), row["deadline"]
            ))
    return parcels


def build_sample_graph():
    # Undirected road network; distances are illustrative kilometres.
    edges = [
        ("Warehouse", "A", 4), ("Warehouse", "B", 6),
        ("Warehouse", "C", 8), ("A", "B", 2), ("A", "D", 5),
        ("B", "C", 3), ("B", "D", 4), ("B", "E", 7),
        ("C", "E", 2), ("D", "E", 3), ("D", "F", 6),
        ("E", "F", 2)
    ]
    graph = {}
    for u, v, distance in edges:
        graph.setdefault(u, {})[v] = distance
        graph.setdefault(v, {})[u] = distance
    return graph


def main():
    parser = argparse.ArgumentParser(description="Courier Planning System")
    parser.add_argument("--capacity", type=int, default=25,
                        help="Vehicle capacity in kg (default: 25)")
    parser.add_argument("--data", default="parcels.csv",
                        help="CSV file containing parcel records")
    args = parser.parse_args()

    parcels = load_parcels(args.data)
    print("=" * 64)
    print("              COURIER PLANNING SYSTEM")
    print("              Hirday | Roll No. 2501060202")
    print("=" * 64)

    start = time.perf_counter()
    sorted_parcels = merge_sort(parcels, parcel_sort_key)
    sort_time = time.perf_counter() - start

    print("\n1. PARCEL PRIORITIZATION (Merge Sort)")
    print("ID   Destination   Weight   Value   Priority   Deadline")
    for p in sorted_parcels:
        print(f"{p.parcel_id:<4} {p.destination:<12} {p.weight:<8} "
              f"{p.value:<7} {p.priority:<10} {p.deadline}")

    start = time.perf_counter()
    selected, total_value = knapsack(sorted_parcels, args.capacity)
    dp_time = time.perf_counter() - start
    print(f"\n2. VEHICLE LOADING (0/1 Knapsack)")
    print(f"Capacity: {args.capacity} kg")
    print("Selected parcels:", ", ".join(p.parcel_id for p in selected))
    print(f"Total weight: {sum(p.weight for p in selected)} kg")
    print(f"Total delivery value: {total_value}")

    graph = build_sample_graph()
    print("\n3. SHORTEST PATHS (Dijkstra)")
    distances, previous = dijkstra(graph, "Warehouse")
    for destination in sorted(graph):
        if destination != "Warehouse":
            path = reconstruct_path(previous, destination)
            print(f"Warehouse -> {destination}: {distances[destination]} km "
                  f"({' -> '.join(path)})")

    delivery_points = sorted({p.destination for p in selected})
    if delivery_points:
        route, route_distance = nearest_neighbour(
            graph, "Warehouse", delivery_points
        )
        print("\n4. DELIVERY ROUTE (Nearest Neighbour + Dijkstra)")
        print(" -> ".join(route))
        print(f"Approximate round-trip distance: {route_distance} km")
    else:
        print("\nNo parcels fit the selected vehicle capacity.")

    print("\n5. BASIC PERFORMANCE MEASUREMENTS")
    print(f"Merge Sort runtime: {sort_time:.8f} seconds")
    print(f"Knapsack DP runtime: {dp_time:.8f} seconds")
    print("Note: timings depend on computer and dataset size.")
    print("\nSystem completed successfully.")


if __name__ == "__main__":
    main()
