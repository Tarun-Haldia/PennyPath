import networkx as nx
from geopy.distance import geodesic
from flask import Flask, render_template, request

app = Flask(__name__)
airport_coordinates = {
    "DEL": {"state": "Delhi", "coords": (28.5575, 77.1235)},
    "BOM": {"state": "Maharashtra", "coords": (19.0896, 72.8656)},
    "BLR": {"state": "Karnataka", "coords": (13.1986, 77.7067)},
    "HYD": {"state": "Telangana", "coords": (17.2313, 78.4294)},
    "MAA": {"state": "Tamil Nadu", "coords": (13.0888, 80.2785)},
    "CCU": {"state": "West Bengal", "coords": (22.6548, 88.4467)},
    "AMD": {"state": "Gujarat", "coords": (23.0333, 72.6167)},
    "PNQ": {"state": "Maharashtra", "coords": (18.5810, 73.9226)},
    "GOI": {"state": "Goa", "coords": (15.3801, 73.8294)},
    "JAI": {"state": "Rajasthan", "coords": (26.8200, 75.7804)},
    "BLK": {"state": "Madhya Pradesh", "coords": (23.2582, 77.4116)},
    "ATQ": {"state": "Punjab", "coords": (31.6492, 74.8288)},
    "IXC": {"state": "Punjab", "coords": (30.6742, 76.7910)},
    "TRZ": {"state": "Tamil Nadu", "coords": (10.8183, 78.6930)},
    "IXB": {"state": "West Bengal", "coords": (26.7026, 88.3475)},
    "IXR": {"state": "Jharkhand", "coords": (23.3444, 85.3344)},
    "STV": {"state": "Gujarat", "coords": (21.1700, 73.0223)},
    "IXA": {"state": "Tripura", "coords": (23.7454, 91.2702)},
    "IXE": {"state": "Karnataka", "coords": (12.8700, 74.8830)},
    "VEV": {"state": "Assam", "coords": (27.4739, 95.2682)},
    "SBY": {"state": "Maharashtra", "coords": (19.7660, 74.4821)},
    "IXT": {"state": "Arunachal Pradesh", "coords": (26.6527, 92.7904)},
    "IXD": {"state": "Uttar Pradesh", "coords": (25.4471, 81.8483)},
    "NAG": {"state": "Maharashtra", "coords": (21.0922, 79.0590)},
    "LKO": {"state": "Uttar Pradesh", "coords": (26.7600, 80.8895)},
    "GWL": {"state": "Madhya Pradesh", "coords": (26.2270, 78.1853)},
    "VNS": {"state": "Uttar Pradesh", "coords": (25.4358, 82.8777)}
}
def calculate_distance(src, dst):
    coord1 = airport_coordinates.get(src, {}).get("coords")  # Get coordinates
    coord2 = airport_coordinates.get(dst, {}).get("coords")
    if coord1 and coord2:
        return geodesic(coord1, coord2).kilometers
    return None




def calculate_fare(distance):
    if distance < 1000:
        return 1500
    elif 1000 <= distance < 2499:
        return 3000
    elif 2500 <= distance < 4000:
        return 4500 + int((distance - 2000) / 400 * 150)  # more deterministic
    return 0

# Build graph
G = nx.DiGraph()
for src in airport_coordinates:
    for dst in airport_coordinates:
        if src != dst:
            distance = calculate_distance(src, dst)
            fare = calculate_fare(distance)
            duration = round(distance / 600 * 1.1, 2)  # Adjust duration calculation
            G.add_edge(src, dst, fare=fare, duration=duration)

def calculate_compensated_fare(route):
    # Get the base fare (sum of individual fares for each leg)
    total_fare = sum(G[route[i]][route[i+1]]['fare'] for i in range(len(route) - 1))
    
    # Apply compensation for stop durations
    stop_duration = 0
    for i in range(1, len(route) - 1):  # Stops are always in the middle of the route
        stop_duration += G[route[i-1]][route[i]]['duration'] + G[route[i]][route[i+1]]['duration']
        
    # Apply discounts based on stop duration
    if stop_duration > 5:
        total_fare -= 300  # ₹300 discount if stop is longer than 5 hrs
    elif stop_duration > 3:
        total_fare -= 500  # ₹500 discount if stop is longer than 3 hrs
    
    return total_fare

# Route-finding function with compensation for indirect routes
def find_route_with_compensation(source, destination, optimize_by="fare", max_stops=2):
    try:
        # Get all possible paths based on max stops
        all_paths = list(nx.all_simple_paths(G, source, destination, cutoff=max_stops + 1))

        # Separate direct and indirect routes
        direct_routes = []
        indirect_routes = []

        for path in all_paths:
            total_fare = sum(G[path[i]][path[i+1]]['fare'] for i in range(len(path) - 1))
            total_duration = sum(G[path[i]][path[i+1]]['duration'] for i in range(len(path) - 1))
            
            # Check if it's a direct flight (single stop path)
            if len(path) == 2:  # Direct flight (Source → Destination)
                direct_routes.append({
                    "route": path,
                    "total_fare": total_fare,
                    "total_duration": round(total_duration, 2)
                })
            else:  # Indirect flight (More than 2 stops)
                # Apply stop compensation to fare
                compensated_fare = calculate_compensated_fare(path)
                indirect_routes.append({
                    "route": path,
                    "total_fare": compensated_fare,
                    "total_duration": round(total_duration, 2)
                })

        # Sort both direct and indirect routes by fare in ascending order
        direct_routes_sorted = sorted(direct_routes, key=lambda x: x['total_fare'])
        indirect_routes_sorted = sorted(indirect_routes, key=lambda x: x['total_fare'])

        # Print top 5 direct and indirect routes
        print("\n Direct Routes sorted by Fare or Duration Balance:")
        for route_info in direct_routes_sorted[:5]:
            print(" → ".join(route_info["route"]), f"| Fare: ₹{route_info['total_fare']} | Duration: {route_info['total_duration']} hrs")

        print("\n🛣️ Top 5 Indirect Routes sorted by Fare or Duration Balance:")
        for route_info in indirect_routes_sorted[:5]:
            print(" → ".join(route_info["route"]), f"| Fare: ₹{route_info['total_fare']} | Duration: {route_info['total_duration']} hrs")

        return direct_routes_sorted, indirect_routes_sorted
    except Exception as e:
        return f"Error: {str(e)}"

# # 🛫 Input from user
# source = input("Enter source airport IATA code (e.g., DEL): ").strip().upper()
# destination = input("Enter destination airport IATA code (e.g., BOM): ").strip().upper()
# optimize = input("Optimize by 'fare' or 'duration': ").strip().lower()
# max_stops = int(input("Enter max number of stops allowed (0 for direct, 1 or 2 for indirect): "))

# # 🔍 Show route
# result = find_route_with_compensation(source, destination, optimize_by=optimize, max_stops=max_stops)
# print("\n📍 Route Details:")
# if isinstance(result, dict):
#     print(" → ".join(result["route"]))
#     print(f"Total Fare: ₹{result['total_fare']}")
#     print(f"Total Duration: {result['total_duration']} hrs")
# else:
#     print(result)

@app.route('/', methods=['GET', 'POST'])
def home():
    results = None
    if request.method == 'POST':
        source = request.form['source']
        destination = request.form['destination']
        optimize = request.form['optimize']
        max_stops = int(request.form['max_stops'])

        direct_routes, indirect_routes = find_route_with_compensation(source, destination, optimize, max_stops)
        results = {
            "direct": direct_routes,
            "indirect": indirect_routes[:5]
        }
    
    # Pass airport codes, states, and coordinates to the template
    airports_info = {
        code: {"state": details["state"], "coords": details["coords"]}
        for code, details in airport_coordinates.items()
    }
    
    return render_template('index.html', airports_info=airports_info, results=results)

if __name__ == '__main__':
    app.run(debug=True)
