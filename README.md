# Metro-simulator

A Python-based simulator that models Delhi Metro routes, travel times, peak-hour scheduling, and journey planning between stations.
---

# Features

- Load metro network data from `metro_data.txt`
- Convert raw data into structured dictionary format
- Calculate travel time between stations
- Peak and non-peak metro scheduling logic
- Next metro arrival prediction
- Full journey planner with interchange support
- Multi-line route handling (Blue, Yellow, Green, Magenta, etc.)

---

# How It Works

- Metro data is read from a CSV-style text file
- Each line contains:
  Line, Source Station, Destination Station, Travel Time, Interchange(Y/N)
- The system builds a graph-like structure internally
- Travel time is computed by summing segment durations
- Interchanges are detected for multi-line routes

---

# Metro Timing Rules

- Metro starts at **06:00 AM (360 mins)**
- Ends at **11:00 PM (1380 mins)**

# Peak Hours:
- 08:00–10:00
- 17:00–19:00  
Frequency: every **4 minutes**

# Non-Peak Hours:
Frequency: every **8 minutes**

---

# 🚉 Main Functions

- `journey_planner()` → Finds best route + fare + arrival time
- `metro_arrival()` → Calculates next train time
- `travel_time()` → Computes journey duration
- `to_dict()` → Converts dataset into structured form

---

# ▶️ How to Run

```bash
python metro_simulator.py