import json
import math


def euclidean_distance(point1, point2):
    """
    Calculate Euclidean distance between two points.
    """
    return math.sqrt((point1[0] - point2[0]) ** 2 +
                     (point1[1] - point2[1]) ** 2)


def load_data(file_name):
    """
    Load JSON file manually.
    """
    with open(file_name, "r") as file:
        data = json.load(file)
    return data


# Find Nearest Agent
def find_nearest_agent(warehouse_location, agents):
    """
    Find nearest agent to a warehouse.
    """
    nearest_agent = None
    minimum_distance = float('inf')

    for agent_id, agent_location in agents.items():
        distance = euclidean_distance(agent_location, warehouse_location)

        if distance < minimum_distance:
            minimum_distance = distance
            nearest_agent = agent_id

    return nearest_agent, minimum_distance



# Simulate Deliveries
def simulate_delivery(data):

    # Convert warehouses into dictionary
    warehouses = {}
    for warehouse in data["warehouses"]:
        warehouses[warehouse["id"]] = warehouse["location"]

    # Convert agents into dictionary
    agents = {}
    for agent in data["agents"]:
        agents[agent["id"]] = agent["location"]

    packages = data["packages"]

    # Report dictionary
    report = {}

    for agent_id in agents:
        report[agent_id] = {
            "packages_delivered": 0,
            "total_distance": 0.0,
            "efficiency": 0.0
        }

    # Process packages
    for package in packages:

        warehouse_id = package["warehouse_id"]
        warehouse_location = warehouses[warehouse_id]
        destination = package["destination"]

        # Find nearest agent
        assigned_agent, distance_to_warehouse = find_nearest_agent(
            warehouse_location,
            agents
        )

        # Warehouse to destination distance
        delivery_distance = euclidean_distance(
            warehouse_location,
            destination
        )

        total_distance = distance_to_warehouse + delivery_distance

        # Update report
        report[assigned_agent]["packages_delivered"] += 1
        report[assigned_agent]["total_distance"] += total_distance

    # Calculate efficiency
    best_agent = None
    best_efficiency = 0

    for agent_id in report:

        delivered = report[agent_id]["packages_delivered"]
        distance = report[agent_id]["total_distance"]

        if distance > 0:
            efficiency = (delivered / distance) * 100
        else:
            efficiency = 0

        report[agent_id]["efficiency"] = round(efficiency, 2)
        report[agent_id]["total_distance"] = round(distance, 2)

        if efficiency > best_efficiency:
            best_efficiency = efficiency
            best_agent = agent_id

    report["best_agent"] = best_agent

    return report


# Save Report
def save_report(report, output_file="report.json"):
    with open(output_file, "w") as file:
        json.dump(report, file, indent=4)



def main():

    # Full path of JSON file
    file_name = r"E:\Python Assignment(Delivery System Test Cases)\python-delivery-system\base_case.json"

    # Load data
    data = load_data(file_name)

    # Simulate delivery system
    report = simulate_delivery(data)

    # Print report
    print("\n===== DELIVERY REPORT =====\n")

    for key, value in report.items():
        print(f"{key} : {value}")

    # Save report
    save_report(report)

    print("\nReport saved to report.json")


if __name__ == "__main__":
    main()
