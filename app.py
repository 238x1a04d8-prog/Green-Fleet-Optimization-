import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sqlite3
from datetime import datetime
import math
import json

# ============================================================
# QUANTUM PREDICTORS - GREEN FLEET OPTIMIZATION
# ============================================================
DB_NAME = "fleet_database.db"

# ============================================================
# WORLDWIDE PORT DATABASE
# ============================================================
WORLD_PORTS = {
    "Chennai, India": (13.0827, 80.2707), "Mumbai, India": (19.0760, 72.8777),
    "Kochi, India": (9.9312, 76.2673), "Visakhapatnam, India": (17.6868, 83.2185),
    "Kolkata, India": (22.5726, 88.3639), "Kandla, India": (23.0333, 70.2167),
    "Mundra, India": (22.8390, 69.7210), "Goa, India": (15.4909, 73.8278),
    "Tuticorin, India": (8.7642, 78.1348), "Paradip, India": (20.2961, 86.7025),
    "Singapore": (1.2903, 103.8519), "Port Klang, Malaysia": (3.0, 101.4),
    "Tanjung Pelepas, Malaysia": (1.36, 103.55), "Jakarta, Indonesia": (-6.104, 106.88),
    "Surabaya, Indonesia": (-7.205, 112.73), "Colombo, Sri Lanka": (6.9271, 79.8612),
    "Dubai, UAE": (25.276, 55.2962), "Abu Dhabi, UAE": (24.4539, 54.3773),
    "Jebel Ali, UAE": (24.9857, 55.0273), "Doha, Qatar": (25.2854, 51.531),
    "Dammam, Saudi Arabia": (26.4207, 50.0888), "Jeddah, Saudi Arabia": (21.4858, 39.1925),
    "Muscat, Oman": (23.588, 58.3829), "Karachi, Pakistan": (24.8607, 67.0011),
    "Chittagong, Bangladesh": (22.3569, 91.7832), "Yangon, Myanmar": (16.8409, 96.1735),
    "Bangkok, Thailand": (13.7563, 100.5018), "Ho Chi Minh City, Vietnam": (10.8231, 106.6297),
    "Haiphong, Vietnam": (20.8449, 106.6881), "Manila, Philippines": (14.5995, 120.9842),
    "Hong Kong": (22.3193, 114.1694), "Shanghai, China": (31.2304, 121.4737),
    "Ningbo, China": (29.8683, 121.544), "Shenzhen, China": (22.5431, 114.0579),
    "Guangzhou, China": (23.1291, 113.2644), "Qingdao, China": (36.0671, 120.3826),
    "Tianjin, China": (39.3434, 117.3616), "Dalian, China": (38.914, 121.6147),
    "Busan, South Korea": (35.1796, 129.0756), "Incheon, South Korea": (37.4563, 126.7052),
    "Tokyo, Japan": (35.6762, 139.6503), "Yokohama, Japan": (35.4437, 139.638),
    "Osaka, Japan": (34.6937, 135.5023), "Nagoya, Japan": (35.1815, 136.9066),
    "Taipei, Taiwan": (25.033, 121.5654), "Kaohsiung, Taiwan": (22.6273, 120.3014),
    "Vladivostok, Russia": (43.1155, 131.8855), "Rotterdam, Netherlands": (51.9244, 4.4777),
    "Amsterdam, Netherlands": (52.3676, 4.9041), "Antwerp, Belgium": (51.2194, 4.4025),
    "Hamburg, Germany": (53.5511, 9.9937), "Bremerhaven, Germany": (53.5396, 8.5809),
    "London, UK": (51.5074, -0.1278), "Southampton, UK": (50.9097, -1.4044),
    "Liverpool, UK": (53.4084, -2.9916), "Le Havre, France": (49.4944, 0.1079),
    "Marseille, France": (43.2965, 5.3698), "Barcelona, Spain": (41.3874, 2.1686),
    "Valencia, Spain": (39.4699, -0.3763), "Lisbon, Portugal": (38.7223, -9.1393),
    "Genoa, Italy": (44.4056, 8.9463), "Naples, Italy": (40.8518, 14.2681),
    "Piraeus, Greece": (37.9838, 23.7275), "Istanbul, Turkey": (41.0082, 28.9784),
    "Athens, Greece": (37.9838, 23.7275), "Gdansk, Poland": (54.352, 18.6466),
    "Helsinki, Finland": (60.1699, 24.9384), "Cape Town, South Africa": (-33.9249, 18.4241),
    "Durban, South Africa": (-29.8587, 31.0218), "Port Elizabeth, South Africa": (-33.9608, 25.6022),
    "Lagos, Nigeria": (6.5244, 3.3792), "Port Harcourt, Nigeria": (4.8156, 7.0498),
    "Alexandria, Egypt": (31.2001, 29.9187), "Port Said, Egypt": (31.2653, 32.3019),
    "Casablanca, Morocco": (33.5731, -7.5898), "Tangier, Morocco": (35.7595, -5.834),
    "Mombasa, Kenya": (-4.0435, 39.6682), "Dar es Salaam, Tanzania": (-6.7924, 39.2083),
    "New York, USA": (40.7128, -74.006), "Los Angeles, USA": (34.0522, -118.2437),
    "Long Beach, USA": (33.7701, -118.1937), "Houston, USA": (29.7604, -95.3698),
    "Miami, USA": (25.7617, -80.1918), "New Orleans, USA": (29.9511, -90.0715),
    "Savannah, USA": (32.0809, -81.0912), "Seattle, USA": (47.6062, -122.3321),
    "Oakland, USA": (37.8044, -122.2712), "Vancouver, Canada": (49.2827, -123.1207),
    "Montreal, Canada": (45.5017, -73.5673), "Halifax, Canada": (44.6488, -63.5752),
    "Manzanillo, Mexico": (19.1138, -104.3385), "Veracruz, Mexico": (19.1738, -96.1342),
    "Santos, Brazil": (-23.9608, -46.3336), "Rio de Janeiro, Brazil": (-22.9068, -43.1729),
    "Buenos Aires, Argentina": (-34.6037, -58.3816), "Montevideo, Uruguay": (-34.9011, -56.1645),
    "Valparaiso, Chile": (-33.0472, -71.6127), "Callao, Peru": (-12.0464, -77.0428),
    "Guayaquil, Ecuador": (-2.1709, -79.9224), "Cartagena, Colombia": (10.391, -75.4794),
    "Sydney, Australia": (-33.8688, 151.2093), "Melbourne, Australia": (-37.8136, 144.9631),
    "Brisbane, Australia": (-27.4698, 153.0251), "Perth, Australia": (-31.9505, 115.8605),
    "Adelaide, Australia": (-34.9285, 138.6007), "Fremantle, Australia": (-32.0569, 115.7439),
    "Auckland, New Zealand": (-36.8509, 174.7645), "Wellington, New Zealand": (-41.2866, 174.7756),
    "Suva, Fiji": (-18.1416, 178.4419)
}
PORT_NAMES = list(WORLD_PORTS.keys())

fuel_data = {
    "Diesel": {"consumption_factor": 1.00, "co2_factor": 3.20, "cost": 65000, "green_score": 35},
    "Petrol": {"consumption_factor": 1.08, "co2_factor": 3.10, "cost": 70000, "green_score": 30},
    "LNG": {"consumption_factor": 0.94, "co2_factor": 2.75, "cost": 57000, "green_score": 62},
    "Methanol": {"consumption_factor": 1.02, "co2_factor": 1.95, "cost": 61000, "green_score": 75},
    "Hydrogen": {"consumption_factor": 0.72, "co2_factor": 0.55, "cost": 92000, "green_score": 91},
    "Ammonia": {"consumption_factor": 0.86, "co2_factor": 0.30, "cost": 72000, "green_score": 88}
}
FUEL_COLORS = {"Diesel": "#4B5563", "Petrol": "#22C55E", "LNG": "#3B82F6", "Methanol": "#F97316", "Hydrogen": "#A855F7", "Ammonia": "#FACC15"}
weather_factor_map = {"Calm Sea": 0.92, "Normal": 1.00, "Moderate": 1.08, "Heavy Weather": 1.18, "Storm": 1.32}

# ============================================================
# DATABASE + MIGRATION
# ============================================================
def add_column_if_missing(conn, table, column, definition):
    cols = [r[1] for r in conn.execute(f"PRAGMA table_info({table})").fetchall()]
    if column not in cols:
        conn.execute(f"ALTER TABLE {table} ADD COLUMN {column} {definition}")

def init_database():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT, created_at TEXT NOT NULL, vessel_type TEXT NOT NULL,
        capacity REAL NOT NULL, speed REAL NOT NULL, distance REAL NOT NULL, cargo REAL NOT NULL,
        current_fuel TEXT NOT NULL, fuel_price REAL NOT NULL, weather TEXT NOT NULL,
        predicted_fuel REAL NOT NULL, initial_cost REAL NOT NULL, initial_co2 REAL NOT NULL,
        optimized_fuel_type TEXT, optimized_speed REAL, optimized_fuel REAL, optimized_cost REAL,
        optimized_co2 REAL, fuel_saving REAL, cost_saving REAL, co2_reduction REAL)""")
    cur.execute("""CREATE TABLE IF NOT EXISTS voyage_runs (
        run_id INTEGER PRIMARY KEY AUTOINCREMENT, created_at TEXT NOT NULL, start_port TEXT,
        end_port TEXT, route_distance REAL, segments INTEGER, segment_mode TEXT, vessel_type TEXT,
        capacity REAL, speed REAL, cargo REAL, current_fuel TEXT, available_fuels TEXT,
        total_fuel REAL, total_cost REAL, total_co2 REAL, total_hours REAL)""")
    cur.execute("""CREATE TABLE IF NOT EXISTS voyage_segments (
        id INTEGER PRIMARY KEY AUTOINCREMENT, created_at TEXT NOT NULL, segment_no INTEGER NOT NULL,
        distance_km REAL NOT NULL, weather TEXT NOT NULL, wind_speed REAL NOT NULL,
        wind_direction REAL NOT NULL, wave_height REAL NOT NULL, current_speed REAL NOT NULL,
        current_direction REAL NOT NULL, selected_fuel TEXT NOT NULL, selected_speed REAL NOT NULL,
        fuel_consumption REAL NOT NULL, co2 REAL NOT NULL, cost REAL NOT NULL, alert TEXT NOT NULL)""")
    # New snapshot fields. Old database records remain usable.
    for c, d in [("available_fuels", "TEXT"), ("wind_speed", "REAL"), ("wave_height", "REAL"), ("current_speed", "REAL")]:
        add_column_if_missing(conn, "predictions", c, d)
    add_column_if_missing(conn, "voyage_segments", "run_id", "INTEGER")
    conn.commit(); conn.close()

init_database()

# ============================================================
# DATABASE HELPERS
# ============================================================
def save_prediction(vessel_type, capacity, speed, distance, cargo, fuel_type, fuel_price, weather,
                    wind, wave, current, available_fuels, initial_fuel, initial_cost, initial_co2,
                    best, fuel_saving, cost_saving, co2_reduction):
    conn = sqlite3.connect(DB_NAME)
    conn.execute("""INSERT INTO predictions
        (created_at,vessel_type,capacity,speed,distance,cargo,current_fuel,fuel_price,weather,
         predicted_fuel,initial_cost,initial_co2,optimized_fuel_type,optimized_speed,optimized_fuel,
         optimized_cost,optimized_co2,fuel_saving,cost_saving,co2_reduction,available_fuels,
         wind_speed,wave_height,current_speed)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"), vessel_type, capacity, speed, distance, cargo,
        fuel_type, fuel_price, weather, initial_fuel, initial_cost, initial_co2, best["fuel"],
        best["speed"], best["fuel_consumption"], best["cost"], best["co2"], fuel_saving,
        cost_saving, co2_reduction, json.dumps(available_fuels), wind, wave, current))
    conn.commit(); conn.close()

def load_prediction_history(limit=50):
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("""SELECT id AS ID, created_at AS "Date & Time", vessel_type AS Vessel,
        capacity AS "Capacity (t)", speed AS "Speed (knots)", distance AS "Distance (km)", cargo AS "Cargo (t)",
        current_fuel AS "Current Fuel", weather AS Weather, predicted_fuel AS "Predicted Fuel (t)",
        initial_cost AS "Initial Cost (₹)", initial_co2 AS "Initial CO₂ (t)", optimized_fuel_type AS "Optimized Fuel",
        optimized_speed AS "Optimized Speed", optimized_fuel AS "Optimized Fuel (t)", optimized_cost AS "Optimized Cost (₹)",
        optimized_co2 AS "Optimized CO₂ (t)", fuel_saving AS "Fuel Saving (%)", cost_saving AS "Cost Saving (%)",
        co2_reduction AS "CO₂ Reduction (%)" FROM predictions ORDER BY id DESC LIMIT ?""", conn, params=(limit,))
    conn.close(); return df

def get_prediction_record(record_id):
    conn = sqlite3.connect(DB_NAME)
    row = pd.read_sql_query("SELECT * FROM predictions WHERE id=?", conn, params=(int(record_id),))
    conn.close(); return row.iloc[0] if not row.empty else None

def clear_prediction_history():
    conn = sqlite3.connect(DB_NAME); conn.execute("DELETE FROM predictions"); conn.commit(); conn.close()

def save_voyage_run(meta, segment_rows):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""INSERT INTO voyage_runs
        (created_at,start_port,end_port,route_distance,segments,segment_mode,vessel_type,capacity,speed,cargo,
         current_fuel,available_fuels,total_fuel,total_cost,total_co2,total_hours)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", meta)
    run_id = cur.lastrowid
    cur.executemany("""INSERT INTO voyage_segments
        (created_at,segment_no,distance_km,weather,wind_speed,wind_direction,wave_height,current_speed,
         current_direction,selected_fuel,selected_speed,fuel_consumption,co2,cost,alert,run_id)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", [tuple(r) + (run_id,) for r in segment_rows])
    conn.commit(); conn.close(); return run_id

def load_segment_history(limit=100):
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("""SELECT id AS ID, created_at AS "Date & Time", segment_no AS Segment,
        distance_km AS "Distance (km)", weather AS Weather, wind_speed AS "Wind (knots)",
        wave_height AS "Wave (m)", current_speed AS "Current (knots)", selected_fuel AS Fuel,
        selected_speed AS "Speed (knots)", fuel_consumption AS "Fuel (t)", co2 AS "CO₂ (t)",
        cost AS "Cost (₹)", alert AS Alert FROM voyage_segments ORDER BY id DESC LIMIT ?""", conn, params=(limit,))
    conn.close(); return df

def get_segment_record(record_id):
    conn = sqlite3.connect(DB_NAME)
    row = pd.read_sql_query("SELECT * FROM voyage_segments WHERE id=?", conn, params=(int(record_id),))
    conn.close(); return row.iloc[0] if not row.empty else None

def get_voyage_run(run_id):
    conn = sqlite3.connect(DB_NAME)
    run = pd.read_sql_query("SELECT * FROM voyage_runs WHERE run_id=?", conn, params=(int(run_id),))
    seg = pd.read_sql_query("SELECT * FROM voyage_segments WHERE run_id=? ORDER BY segment_no", conn, params=(int(run_id),))
    conn.close(); return (run.iloc[0] if not run.empty else None), seg

def clear_voyage_segment_history():
    conn = sqlite3.connect(DB_NAME); conn.execute("DELETE FROM voyage_segments"); conn.execute("DELETE FROM voyage_runs"); conn.commit(); conn.close()

# ============================================================
# MODEL FUNCTIONS
# ============================================================
def base_fuel(capacity, speed, distance, fuel):
    return (capacity / 10000) * (distance / 1000) * 2.0 * (speed / 18) ** 2.3 * fuel_data[fuel]["consumption_factor"]

def environmental_factor(weather, wind_speed, wave_height, current_speed):
    return weather_factor_map.get(weather, 1.0) * (1 + max(0, wind_speed - 8) * 0.012) * (1 + max(0, wave_height - 1) * 0.075) * (1 + max(0, current_speed - 0.5) * 0.06)

def predict_fuel(capacity, speed, distance, fuel, weather="Normal", wind_speed=8, wave_height=1, current_speed=0.5):
    return base_fuel(capacity, speed, distance, fuel) * environmental_factor(weather, wind_speed, wave_height, current_speed)

def calculate_co2(amount, fuel): return amount * fuel_data[fuel]["co2_factor"]

def haversine_km(lat1, lon1, lat2, lon2):
    r=6371.0; p1=math.radians(lat1); p2=math.radians(lat2); dp=math.radians(lat2-lat1); dl=math.radians(lon2-lon1)
    a=math.sin(dp/2)**2+math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return 2*r*math.asin(math.sqrt(a))

def interpolate_position(lat1, lon1, lat2, lon2, progress): return lat1+(lat2-lat1)*progress, lon1+(lon2-lon1)*progress

def generate_segment_conditions(n, seed=42):
    rng=np.random.default_rng(seed); rows=[]
    choices=["Calm Sea","Normal","Moderate","Heavy Weather"]; probs=[.20,.45,.25,.10]
    for i in range(n):
        weather=rng.choice(choices,p=probs)
        wind=float(np.clip(rng.normal(12 if weather!="Calm Sea" else 6,3),2,30))
        wave=float(np.clip(rng.normal(1.7 if weather in ["Moderate","Heavy Weather"] else .9,.5),.2,5.5))
        current=float(np.clip(rng.normal(1.1,.4),.1,3.0))
        rows.append({"segment":i+1,"weather":weather,"wind_speed":wind,"wind_direction":float(rng.integers(0,360)),"wave_height":wave,"current_speed":current,"current_direction":float(rng.integers(0,360))})
    return rows

def alert_level(weather, wind, wave):
    if weather=="Storm" or wind>=25 or wave>=4.5: return "🔴 Severe"
    if weather=="Heavy Weather" or wind>=18 or wave>=3: return "🟠 Caution"
    return "🟢 Normal"

def optimize_single_segment(capacity,distance,requested_speed,cargo,available_fuels,weather,wind,wave,current):
    speeds=sorted(set(round(float(np.clip(s,8,25)),1) for s in [requested_speed-2,requested_speed-1,requested_speed,requested_speed+1,requested_speed+2]))
    best=None; best_score=float("inf")
    for fuel in available_fuels:
        for sp in speeds:
            consumption=predict_fuel(capacity,sp,distance,fuel,weather,wind,wave,current)
            cost=consumption*fuel_data[fuel]["cost"]; co2=calculate_co2(consumption,fuel)
            penalty=0 if cargo<=capacity else 1_000_000+(cargo-capacity)*1000
            score=cost*.55+co2*12000*.35+abs(sp-17)*cost*.03+penalty
            if score<best_score:
                best_score=score; best={"fuel":fuel,"speed":sp,"fuel_consumption":consumption,"cost":cost,"co2":co2,"score":score}
    return best

# ============================================================
# GRAPHS
# ============================================================
def create_3d_bar_chart(fuels, values, title, ylabel):
    fig=plt.figure(figsize=(10,5.8)); ax=fig.add_subplot(111,projection="3d")
    values=np.array(values,dtype=float); total=float(values.sum()); percentages=(values/total*100) if total>0 else np.zeros(len(values))
    x=np.arange(len(fuels)); dx=np.full(len(fuels),.65); dy=np.full(len(fuels),.65); dz=values
    colors=[FUEL_COLORS.get(f,"#48e0a0") for f in fuels]
    ax.bar3d(x,np.zeros(len(fuels)),np.zeros(len(fuels)),dx,dy,dz,color=colors,edgecolor="white",linewidth=.8,shade=True,alpha=.95)
    maxv=float(values.max()) if len(values) else 1; maxv=max(maxv,1)
    for i,(fuel,val,pct) in enumerate(zip(fuels,values,percentages)):
        ax.text(i+.325,.325,val+maxv*.10,f"{pct:.1f}%",ha="center",va="bottom",fontsize=11,fontweight="bold",color="black")
        ax.text(i+.325,.325,val+maxv*.035,f"{val:.2f} t",ha="center",va="bottom",fontsize=8,color="black")
    ax.set_xticks(x+.325); ax.set_xticklabels(fuels,rotation=20,ha="right",fontsize=9); ax.set_yticks([]); ax.set_zlabel(ylabel,fontsize=10)
    ax.set_title(title,fontsize=15,fontweight="bold",pad=20); ax.set_zlim(0,maxv*1.28); ax.view_init(elev=22,azim=-60); ax.set_box_aspect((max(len(fuels),4),1.2,4)); ax.grid(True,alpha=.2)
    ax.xaxis.pane.set_alpha(.08); ax.yaxis.pane.set_alpha(.05); ax.zaxis.pane.set_alpha(.05); fig.tight_layout(); return fig

def render_prediction_report(record):
    st.markdown("## 📋 Complete Saved Prediction Report")
    st.caption(f"Record ID: {int(record['id'])} • Saved on {record['created_at']}")
    left,right=st.columns(2)
    with left:
        st.markdown("### 📥 Inputs used on that day")
        data={"Vessel":record["vessel_type"],"Capacity (t)":record["capacity"],"Speed (knots)":record["speed"],"Distance (km)":record["distance"],"Cargo (t)":record["cargo"],"Current Fuel":record["current_fuel"],"Fuel Price (₹/t)":record["fuel_price"],"Weather":record["weather"],"Wind (knots)":record["wind_speed"],"Wave (m)":record["wave_height"],"Current (knots)":record["current_speed"]}
        try: fuels=json.loads(record["available_fuels"]) if record["available_fuels"] else [record["current_fuel"]]
        except Exception: fuels=[record["current_fuel"]]
        data["Available Fuels"]=", ".join(fuels); st.dataframe(pd.DataFrame(list(data.items()),columns=["Input","Value"]),hide_index=True,use_container_width=True)
    with right:
        st.markdown("### 📤 Outputs produced on that day")
        out={"Predicted Fuel (t)":record["predicted_fuel"],"Initial Cost (₹)":record["initial_cost"],"Initial CO₂ (t)":record["initial_co2"],"Optimized Fuel":record["optimized_fuel_type"],"Optimized Speed (knots)":record["optimized_speed"],"Optimized Fuel (t)":record["optimized_fuel"],"Optimized Cost (₹)":record["optimized_cost"],"Optimized CO₂ (t)":record["optimized_co2"],"Fuel Saving (%)":record["fuel_saving"],"Cost Saving (%)":record["cost_saving"],"CO₂ Reduction (%)":record["co2_reduction"]}
        st.dataframe(pd.DataFrame(list(out.items()),columns=["Output","Value"]),hide_index=True,use_container_width=True)
    st.markdown("### 📊 Graphs from the saved run")
    fuels=json.loads(record["available_fuels"]) if record["available_fuels"] else [record["current_fuel"]]
    vals=[predict_fuel(record["capacity"],record["optimized_speed"],record["distance"],f,record["weather"],record["wind_speed"] or 8,record["wave_height"] or 1,record["current_speed"] or .5) for f in fuels]
    co2=[calculate_co2(v,f) for v,f in zip(vals,fuels)]
    g1,g2=st.columns(2)
    with g1:
        fig=create_3d_bar_chart(fuels,vals,"Saved Fuel Comparison","Fuel (tonnes)"); st.pyplot(fig,use_container_width=True); plt.close(fig)
    with g2:
        fig=create_3d_bar_chart(fuels,co2,"Saved CO₂ Comparison","CO₂ (tonnes)"); st.pyplot(fig,use_container_width=True); plt.close(fig)
    st.success(f"This report is a snapshot of record #{int(record['id'])}. Changing today's sidebar inputs will not change this saved report.")

def render_voyage_report(segment_record):
    run_id=segment_record["run_id"]
    st.markdown("## 🧭 Complete Saved Voyage Report")
    if pd.isna(run_id):
        st.caption(f"Segment record ID: {int(segment_record['id'])} • This is an older record created before complete voyage-run snapshots were added.")
        st.dataframe(pd.DataFrame({"Field":["Date & Time","Segment","Distance (km)","Weather","Wind (knots)","Wave (m)","Current (knots)","Fuel","Speed (knots)","Fuel (t)","CO₂ (t)","Cost (₹)","Alert"],"Value":[segment_record['created_at'],segment_record['segment_no'],segment_record['distance_km'],segment_record['weather'],segment_record['wind_speed'],segment_record['wave_height'],segment_record['current_speed'],segment_record['selected_fuel'],segment_record['selected_speed'],segment_record['fuel_consumption'],segment_record['co2'],segment_record['cost'],segment_record['alert']]}),hide_index=True,use_container_width=True)
        return
    run,seg=get_voyage_run(int(run_id))
    if run is None: return
    st.caption(f"Voyage Run #{int(run['run_id'])} • Saved on {run['created_at']}")
    a,b=st.columns(2)
    with a:
        st.markdown("### 📥 Voyage Inputs")
        inp={"Start Port":run["start_port"],"Destination":run["end_port"],"Route Distance (km)":run["route_distance"],"Segments":run["segments"],"Condition Mode":run["segment_mode"],"Vessel":run["vessel_type"],"Capacity (t)":run["capacity"],"Requested Speed (knots)":run["speed"],"Cargo (t)":run["cargo"],"Current Fuel":run["current_fuel"]}
        try: inp["Available Fuels"]=", ".join(json.loads(run["available_fuels"]))
        except Exception: inp["Available Fuels"]=run["available_fuels"]
        st.dataframe(pd.DataFrame(list(inp.items()),columns=["Input","Value"]),hide_index=True,use_container_width=True)
    with b:
        st.markdown("### 📤 Voyage Outputs")
        st.dataframe(pd.DataFrame(list({"Total Fuel (t)":run["total_fuel"],"Total Cost (₹)":run["total_cost"],"Total CO₂ (t)":run["total_co2"],"Estimated ETA (h)":run["total_hours"]}.items()),columns=["Output","Value"]),hide_index=True,use_container_width=True)
    st.markdown("### 📋 Segment-by-Segment Saved Plan")
    display=seg[["segment_no","distance_km","weather","wind_speed","wave_height","current_speed","selected_fuel","selected_speed","fuel_consumption","co2","cost","alert"]].copy()
    display.columns=["Segment","Distance (km)","Weather","Wind (kn)","Wave (m)","Current (kn)","Best Fuel","Best Speed","Fuel (t)","CO₂ (t)","Cost (₹)","Alert"]
    st.dataframe(display,hide_index=True,use_container_width=True)
    g1,g2=st.columns(2)
    with g1:
        fig,ax=plt.subplots(figsize=(8,4)); ax.plot(display["Segment"],display["Fuel (t)"],marker="o"); ax.set_title("Saved Fuel by Segment"); ax.set_xlabel("Segment"); ax.set_ylabel("Fuel (t)"); st.pyplot(fig,use_container_width=True); plt.close(fig)
    with g2:
        fig,ax=plt.subplots(figsize=(8,4)); ax.plot(display["Segment"],display["CO₂ (t)"],marker="o"); ax.set_title("Saved CO₂ by Segment"); ax.set_xlabel("Segment"); ax.set_ylabel("CO₂ (t)"); st.pyplot(fig,use_container_width=True); plt.close(fig)
    st.success(f"This report reopens the complete saved voyage run #{int(run['run_id'])}, including its original route, inputs, segment conditions, outputs and graphs.")

# ============================================================
# PAGE
# ============================================================
st.set_page_config(page_title="Quantum Predictors | Green Fleet",page_icon="🚢",layout="wide")
st.markdown("""<style>
.stApp{background:linear-gradient(135deg,#06141c,#09242a);color:white}.main-title{font-size:45px;font-weight:800;color:#48e0a0;text-align:center}.subtitle{text-align:center;color:#a8c1c8;font-size:18px;margin-bottom:30px}.section-title{color:#48e0a0;font-size:28px;font-weight:700;margin-top:30px}.card{background:#0d252d;border:1px solid #1d4a52;border-radius:15px;padding:20px;margin-bottom:15px}.metric-card{background:#0d252d;border:1px solid #24545c;border-radius:15px;padding:20px;text-align:center}.metric-title{color:#8ba9b1;font-size:14px}.metric-value{color:#48e0a0;font-size:30px;font-weight:800}.small-text{color:#8ba9b1;font-size:13px}.success-box{background:#0b3028;border:1px solid #32c98b;border-radius:15px;padding:25px}
</style>""",unsafe_allow_html=True)
st.markdown('<div class="main-title">⚛️ Quantum Predictors</div>',unsafe_allow_html=True)
st.markdown('<div class="subtitle">Quantum-Inspired Fuel Consumption Prediction & Green Fleet Optimization<br>Dynamic Voyage Monitoring • Engineering Day Prototype</div>',unsafe_allow_html=True)

# ============================================================
# SIDEBAR
# ============================================================
st.sidebar.title("⚙️ Fleet Configuration")
vessel_type=st.sidebar.selectbox("Vessel Type",["Container Ship","Bulk Carrier","Tanker","Cargo Ship"])
capacity=st.sidebar.number_input("Vessel Capacity (tonnes)",1000,200000,50000,1000)
speed=st.sidebar.number_input("Current / Planned Speed (knots)",5.0,30.0,18.0,.5)
distance=st.sidebar.number_input("Total Voyage Distance (km)",100,50000,2500,100)
cargo=st.sidebar.number_input("Cargo Demand (tonnes)",100,200000,40000,1000)
fuel_type=st.sidebar.selectbox("Current Fuel",list(fuel_data.keys()))
available_fuels=st.sidebar.multiselect("Available Fuels for This Vessel",list(fuel_data.keys()),default=["Diesel","LNG","Methanol","Hydrogen","Ammonia"])
if not available_fuels:
    st.sidebar.error("Select at least one available fuel."); available_fuels=[fuel_type]
fuel_price=st.sidebar.number_input("Current Fuel Price (₹ / tonne)",1000,200000,65000,1000)
weather=st.sidebar.selectbox("Current Operating Condition",["Normal","Calm Sea","Moderate","Heavy Weather","Storm"])
wind_speed_now=st.sidebar.number_input("Current Wind Speed (knots)",0.0,40.0,10.0,1.0)
wave_height_now=st.sidebar.number_input("Current Wave Height (m)",.1,8.0,1.2,.1)
current_speed_now=st.sidebar.number_input("Current Speed (knots)",0.0,5.0,.6,.1)
predict_button=st.sidebar.button("🚀 Predict & Optimize",use_container_width=True)

# ============================================================
# DASHBOARD
# ============================================================
initial_fuel=predict_fuel(capacity,speed,distance,fuel_type,weather,wind_speed_now,wave_height_now,current_speed_now); initial_cost=initial_fuel*fuel_price; initial_co2=calculate_co2(initial_fuel,fuel_type); green_score=fuel_data[fuel_type]["green_score"]
st.markdown('<div class="section-title">📊 Fleet Prediction Dashboard</div>',unsafe_allow_html=True)
cols=st.columns(4)
for c,title,value,sub in [(cols[0],"Predicted Fuel",f"{initial_fuel:.2f}","tonnes"),(cols[1],"Estimated Cost",f"₹{initial_cost/100000:.2f}L","current-fuel estimate"),(cols[2],"CO₂ Emission",f"{initial_co2:.2f}","tonnes"),(cols[3],"Green Score",str(green_score),"out of 100")]:
    c.markdown(f'<div class="metric-card"><div class="metric-title">{title}</div><div class="metric-value">{value}</div><div class="small-text">{sub}</div></div>',unsafe_allow_html=True)
st.markdown('<div class="section-title">🌊 Current Vessel Conditions</div>',unsafe_allow_html=True)
for c,title,value in zip(st.columns(5),["Weather","Wind","Waves","Current","Alert"],[weather,f"{wind_speed_now:.1f} kn",f"{wave_height_now:.1f} m",f"{current_speed_now:.1f} kn",alert_level(weather,wind_speed_now,wave_height_now)]): c.metric(title,value)
st.markdown('<div class="section-title">🤖 Fuel Prediction</div>',unsafe_allow_html=True)
st.markdown(f'<div class="card"><b>Vessel:</b> {vessel_type}<br><b>Capacity:</b> {capacity:,} tonnes<br><b>Cargo Demand:</b> {cargo:,} tonnes<br><b>Distance:</b> {distance:,} km<br><b>Current Fuel:</b> {fuel_type}<br><b>Available Fuels:</b> {", ".join(available_fuels)}<br><b>Speed:</b> {speed:.1f} knots<br><b>Environment:</b> {weather}, wind {wind_speed_now:.1f} kn, waves {wave_height_now:.1f} m, current {current_speed_now:.1f} kn</div>',unsafe_allow_html=True)
st.markdown('<div class="section-title">🌍 Green Fuel Comparison</div>',unsafe_allow_html=True)
fuel_df=pd.DataFrame([{"Fuel":f,"Available":"Yes" if f in available_fuels else "No","CO₂ Factor":fuel_data[f]["co2_factor"],"Approx. Price ₹/tonne":fuel_data[f]["cost"],"Green Score":fuel_data[f]["green_score"]} for f in fuel_data]); st.dataframe(fuel_df,use_container_width=True,hide_index=True)

# ============================================================
# PREDICT & OPTIMIZE
# ============================================================
if predict_button and cargo>capacity: st.error("Cargo demand is greater than vessel capacity. Please correct the input.")
elif predict_button:
    with st.spinner("⚛️ Comparing fuel + speed combinations..."):
        best_solution=optimize_single_segment(capacity,distance,speed,cargo,available_fuels,weather,wind_speed_now,wave_height_now,current_speed_now)
    optimized_fuel=best_solution["fuel_consumption"]; optimized_cost=best_solution["cost"]; optimized_co2=best_solution["co2"]
    fuel_saving=(initial_fuel-optimized_fuel)/initial_fuel*100 if initial_fuel else 0; cost_saving=(initial_cost-optimized_cost)/initial_cost*100 if initial_cost else 0; co2_reduction=(initial_co2-optimized_co2)/initial_co2*100 if initial_co2 else 0
    save_prediction(vessel_type,capacity,speed,distance,cargo,fuel_type,fuel_price,weather,wind_speed_now,wave_height_now,current_speed_now,available_fuels,initial_fuel,initial_cost,initial_co2,best_solution,fuel_saving,cost_saving,co2_reduction)
    st.markdown('<div class="section-title">⚛️ Quantum-Inspired Optimization Result</div>',unsafe_allow_html=True)
    st.markdown(f'<div class="success-box"><h2>🚢 Recommended Green Fleet Plan</h2><h3>Recommended Fuel: {best_solution["fuel"]}</h3><p>Recommended Operating Speed: <b>{best_solution["speed"]:.1f} knots</b></p><p>Predicted Fuel Consumption: <b>{optimized_fuel:.2f} tonnes</b></p><p>Estimated Fuel Cost: <b>₹{optimized_cost:,.0f}</b></p><p>Estimated CO₂ Emissions: <b>{optimized_co2:.2f} tonnes</b></p><p>Available-fuel constraint: <b>{", ".join(available_fuels)}</b></p></div>',unsafe_allow_html=True)
    for c,title,value in zip(st.columns(3),["Fuel Saving","Cost Saving","CO₂ Reduction"],[f"{fuel_saving:.2f}%",f"{cost_saving:.2f}%",f"{co2_reduction:.2f}%"]): c.metric(title,value)
    st.dataframe(pd.DataFrame({"Metric":["Fuel Consumption (t)","Fuel Cost (₹)","CO₂ Emissions (t)"],"Current Plan":[initial_fuel,initial_cost,initial_co2],"Optimized Plan":[optimized_fuel,optimized_cost,optimized_co2]}),use_container_width=True,hide_index=True)
    chart_fuels=list(available_fuels); values=[predict_fuel(capacity,best_solution["speed"],distance,f,weather,wind_speed_now,wave_height_now,current_speed_now) for f in chart_fuels]; emissions=[calculate_co2(v,f) for v,f in zip(chart_fuels,values)]
    graph_left,graph_right=st.columns([1,1.7])
    with graph_left:
        st.markdown('<div class="section-title">💡 Decision Explanation</div>',unsafe_allow_html=True)
        st.markdown(f'<div class="card">The optimizer compared only the fuels available to this vessel.<br><br>It tested several nearby operating speeds and evaluated fuel cost, CO₂ emissions and speed penalty.<br><br><b>Selected Fuel:</b><br>{best_solution["fuel"]}<br><br><b>Selected Speed:</b><br>{best_solution["speed"]:.1f} knots<br><br><b>Fuel Consumption:</b><br>{optimized_fuel:.2f} tonnes<br><br><b>CO₂:</b><br>{optimized_co2:.2f} tonnes<br><br><b>Available Fuels:</b><br>{", ".join(chart_fuels)}<br><br>The percentage shown on the graph represents each selected fuel share of the displayed total consumption.<br><br><b>Note:</b> This is a quantum-inspired classical prototype, not a physical quantum computer.</div>',unsafe_allow_html=True)
    with graph_right:
        st.markdown('<div class="section-title">📈 3D Fuel Consumption Comparison</div>',unsafe_allow_html=True); fig=create_3d_bar_chart(chart_fuels,values,"Available Fuel Consumption","Fuel (tonnes)"); st.pyplot(fig,use_container_width=True); plt.close(fig)
        st.markdown('<div class="section-title">🌱 3D CO₂ Comparison</div>',unsafe_allow_html=True); fig=create_3d_bar_chart(chart_fuels,emissions,"Available Fuel CO₂ Comparison","CO₂ (tonnes)"); st.pyplot(fig,use_container_width=True); plt.close(fig)

# ============================================================
# DYNAMIC VOYAGE
# ============================================================
st.markdown('<div class="section-title">🧭 Dynamic Voyage Optimization</div>',unsafe_allow_html=True)
st.markdown('<div class="card">Weather is not assumed to remain constant for the whole trip. The voyage is divided into route segments. Each segment can have different wind, wave, current and weather conditions.</div>',unsafe_allow_html=True)
st.markdown("### 🌍 Worldwide Route Selection")
v1,v2,v3=st.columns(3)
with v1:
    start_port=st.selectbox("Start Port",PORT_NAMES,index=PORT_NAMES.index("Chennai, India"),key="start_port_select"); start_lat,start_lon=WORLD_PORTS[start_port]; st.caption(f"📍 {start_lat:.4f}, {start_lon:.4f}")
with v2:
    end_port=st.selectbox("Destination Port",PORT_NAMES,index=PORT_NAMES.index("Mumbai, India"),key="destination_port_select"); end_lat,end_lon=WORLD_PORTS[end_port]; st.caption(f"📍 {end_lat:.4f}, {end_lon:.4f}")
with v3:
    segments=st.number_input("Number of Voyage Segments",2,30,6,1); segment_mode=st.selectbox("Condition Mode",["Dynamic Simulation","Manual Conditions"]); route_seed=st.number_input("Simulation Seed",1,99999,42,1)
route_distance=haversine_km(start_lat,start_lon,end_lat,end_lon); segment_distance=route_distance/segments
st.info(f"🛳️ Estimated route distance: {route_distance:,.0f} km • {segments} segments • about {segment_distance:,.0f} km per segment")
manual_conditions=[]
if segment_mode=="Manual Conditions":
    st.write("Enter conditions for each segment:")
    for i in range(int(segments)):
        a,b,c,d=st.columns(4)
        with a: mw=st.selectbox(f"S{i+1} Weather",["Calm Sea","Normal","Moderate","Heavy Weather","Storm"],key=f"mw_{i}")
        with b: mwind=st.number_input(f"S{i+1} Wind (kn)",0.0,40.0,10.0,1.0,key=f"mwind_{i}")
        with c: mwave=st.number_input(f"S{i+1} Wave (m)",.1,8.0,1.2,.1,key=f"mwave_{i}")
        with d: mcurrent=st.number_input(f"S{i+1} Current (kn)",0.0,5.0,.6,.1,key=f"mcur_{i}")
        manual_conditions.append({"segment":i+1,"weather":mw,"wind_speed":mwind,"wind_direction":0.0,"wave_height":mwave,"current_speed":mcurrent,"current_direction":0.0})
run_voyage=st.button("🧭 Run Dynamic Voyage Optimization",use_container_width=True)
if run_voyage:
    conditions=manual_conditions if segment_mode=="Manual Conditions" else generate_segment_conditions(int(segments),seed=int(route_seed))
    voyage_rows=[]; total_fuel=total_cost=total_co2=total_hours=0.0; display=[]
    for cond in conditions:
        best=optimize_single_segment(capacity,segment_distance,speed,cargo,available_fuels,cond["weather"],cond["wind_speed"],cond["wave_height"],cond["current_speed"]); hours=segment_distance/(best["speed"]*1.852); total_hours+=hours; total_fuel+=best["fuel_consumption"]; total_cost+=best["cost"]; total_co2+=best["co2"]; alert=alert_level(cond["weather"],cond["wind_speed"],cond["wave_height"])
        display.append({"Segment":cond["segment"],"Distance (km)":round(segment_distance,1),"Weather":cond["weather"],"Wind (kn)":round(cond["wind_speed"],1),"Wave (m)":round(cond["wave_height"],1),"Current (kn)":round(cond["current_speed"],1),"Best Fuel":best["fuel"],"Best Speed":round(best["speed"],1),"Fuel (t)":round(best["fuel_consumption"],2),"CO₂ (t)":round(best["co2"],2),"Cost (₹)":round(best["cost"],0),"Alert":alert})
        voyage_rows.append((datetime.now().strftime("%Y-%m-%d %H:%M:%S"),int(cond["segment"]),segment_distance,cond["weather"],cond["wind_speed"],cond["wind_direction"],cond["wave_height"],cond["current_speed"],cond["current_direction"],best["fuel"],best["speed"],best["fuel_consumption"],best["co2"],best["cost"],alert))
    meta=(datetime.now().strftime("%Y-%m-%d %H:%M:%S"),start_port,end_port,route_distance,int(segments),segment_mode,vessel_type,capacity,speed,cargo,fuel_type,json.dumps(available_fuels),total_fuel,total_cost,total_co2,total_hours)
    run_id=save_voyage_run(meta,voyage_rows)
    st.session_state.update({"voyage_conditions":conditions,"voyage_segments_df":pd.DataFrame(display),"voyage_total_fuel":total_fuel,"voyage_total_cost":total_cost,"voyage_total_co2":total_co2,"voyage_hours":total_hours,"route":(start_port,end_port,start_lat,start_lon,end_lat,end_lon),"voyage_done":True,"track_step":0,"voyage_run_id":run_id})

if st.session_state.get("voyage_done",False):
    total_fuel=st.session_state["voyage_total_fuel"]; total_cost=st.session_state["voyage_total_cost"]; total_co2=st.session_state["voyage_total_co2"]; total_hours=st.session_state["voyage_hours"]; voyage_df=st.session_state["voyage_segments_df"]
    st.markdown('<div class="section-title">📋 Segment-by-Segment Voyage Plan</div>',unsafe_allow_html=True); st.dataframe(voyage_df,use_container_width=True,hide_index=True)
    for c,title,value in zip(st.columns(4),["Total Fuel","Total Cost","Total CO₂","Estimated ETA"],[f"{total_fuel:.2f} t",f"₹{total_cost/100000:.2f} L",f"{total_co2:.2f} t",f"{total_hours:.1f} h"]): c.metric(title,value)
    st.markdown('<div class="section-title">🌦️ Changing Weather Across Voyage</div>',unsafe_allow_html=True); fig,ax=plt.subplots(figsize=(10,4)); ax.plot(voyage_df["Segment"],voyage_df["Wave (m)"],marker="o",label="Wave height"); ax.plot(voyage_df["Segment"],voyage_df["Wind (kn)"],marker="o",label="Wind speed"); ax.set_xlabel("Voyage Segment"); ax.set_ylabel("Condition value"); ax.set_title("Dynamic Environmental Conditions"); ax.legend(); st.pyplot(fig); plt.close(fig)

# ============================================================
# LIVE MONITORING + MAP
# ============================================================
st.markdown('<div class="section-title">📡 Live Voyage Monitoring</div>',unsafe_allow_html=True)
st.markdown('<div class="card"><b>Demo mode:</b> the dashboard simulates an onboard GPS/AIS-style feed. Each update moves the vessel along the selected route and changes monitored environmental conditions.</div>',unsafe_allow_html=True)
if "track_step" not in st.session_state: st.session_state["track_step"]=0
track_col1,track_col2,track_col3=st.columns(3)
with track_col1:
    if st.button("▶️ Next Live Update",use_container_width=True): st.session_state["track_step"]=min(st.session_state["track_step"]+1,int(segments))
with track_col2:
    if st.button("🔄 Reset Tracking",use_container_width=True): st.session_state["track_step"]=0
with track_col3:
    st.session_state["track_step"]=st.number_input("Tracking Segment",0,int(segments),int(st.session_state["track_step"]),1)
step=int(st.session_state["track_step"]); progress=step/max(1,int(segments)); cur_lat,cur_lon=interpolate_position(start_lat,start_lon,end_lat,end_lon,progress)
conditions=st.session_state.get("voyage_conditions",generate_segment_conditions(int(segments),seed=int(route_seed))); active=conditions[min(max(step-1,0),len(conditions)-1)]
if step==0: active_weather,active_wind,active_wave,active_current,active_fuel,active_speed=weather,wind_speed_now,wave_height_now,current_speed_now,fuel_type,speed
else:
    active_weather,active_wind,active_wave,active_current=active["weather"],active["wind_speed"],active["wave_height"],active["current_speed"]; live_best=optimize_single_segment(capacity,segment_distance,speed,cargo,available_fuels,active_weather,active_wind,active_wave,active_current); active_fuel,active_speed=live_best["fuel"],live_best["speed"]
live_fuel_rate=predict_fuel(capacity,active_speed,max(segment_distance,1),active_fuel,active_weather,active_wind,active_wave,active_current); live_co2=calculate_co2(live_fuel_rate,active_fuel); live_alert=alert_level(active_weather,active_wind,active_wave)
for c,title,value in zip(st.columns(6),["GPS Latitude","GPS Longitude","Progress","Live Speed","Live Fuel","Alert"],[f"{cur_lat:.4f}°",f"{cur_lon:.4f}°",f"{progress*100:.1f}%",f"{active_speed:.1f} kn",active_fuel,live_alert]): c.metric(title,value)
for c,title,value in zip(st.columns(4),["Weather","Wind","Wave","Current"],[active_weather,f"{active_wind:.1f} kn",f"{active_wave:.1f} m",f"{active_current:.1f} kn"]): c.metric(title,value)
st.markdown(f'<div class="card"><b>Route:</b> {start_port} → {end_port}<br><b>Live position:</b> {cur_lat:.4f}, {cur_lon:.4f}<br><b>Active segment:</b> {max(step,1)} / {segments}<br><b>Current environmental condition:</b> {active_weather}<br><b>Predicted fuel for active segment:</b> {live_fuel_rate:.2f} tonnes<br><b>Estimated CO₂ for active segment:</b> {live_co2:.2f} tonnes<br><b>Decision:</b> The system can recalculate the recommended fuel and speed when monitored conditions change.</div>',unsafe_allow_html=True)
st.markdown('<div class="section-title">🗺️ Live Worldwide Voyage Map</div>',unsafe_allow_html=True)
route_points=pd.DataFrame({"latitude":np.linspace(start_lat,end_lat,50),"longitude":np.linspace(start_lon,end_lon,50)}); map_data=pd.DataFrame({"latitude":[start_lat,cur_lat,end_lat],"longitude":[start_lon,cur_lon,end_lon]})
try:
    import pydeck as pdk
    route_layer=pdk.Layer("PathLayer",data=[{"path":route_points[["longitude","latitude"]].values.tolist()}],get_path="path",get_width=5,get_color=[72,224,160],pickable=False); point_layer=pdk.Layer("ScatterplotLayer",data=map_data,get_position=["longitude","latitude"],get_radius=70000,get_fill_color=[255,80,80],pickable=True); view_state=pdk.ViewState(latitude=(start_lat+end_lat)/2,longitude=(start_lon+end_lon)/2,zoom=2.5); st.pydeck_chart(pdk.Deck(layers=[route_layer,point_layer],initial_view_state=view_state,tooltip={"text":"Latitude: {latitude}\nLongitude: {longitude}"}),use_container_width=True)
except Exception: st.map(map_data,latitude="latitude",longitude="longitude",zoom=2,use_container_width=True)
st.markdown(f'<div class="card"><b>🟢 Start Port:</b> {start_port} ({start_lat:.4f}, {start_lon:.4f})<br><br><b>🚢 Current Vessel:</b> ({cur_lat:.4f}, {cur_lon:.4f})<br><br><b>🔴 Destination:</b> {end_port} ({end_lat:.4f}, {end_lon:.4f})<br><br><b>🌍 Route Distance:</b> {route_distance:,.0f} km</div>',unsafe_allow_html=True)
if live_alert=="🔴 Severe": st.error("⚠️ Severe conditions detected. In a real deployment, an approved navigation/weather system should be consulted and operating decisions should be made by qualified personnel.")
elif live_alert=="🟠 Caution": st.warning("⚠️ Caution: environmental resistance is elevated. The optimizer can recalculate the local fuel/speed plan.")
else: st.success("✅ Conditions are within the prototype's normal monitoring range.")

# ============================================================
# SYSTEM FLOW
# ============================================================
st.markdown('<div class="section-title">🔬 How the Integrated System Works</div>',unsafe_allow_html=True)
for c,title,text in zip(st.columns(3),["01 🤖 Prediction","02 ⚛️ Optimization","03 📡 Live Monitoring"],["Vessel capacity, speed, distance, fuel and environmental conditions are used to estimate fuel consumption.","The prototype searches feasible fuel + speed combinations and minimizes a combined cost/emission/speed objective.","GPS position and changing weather conditions are monitored. When conditions change, the local plan can be recalculated."]): c.markdown(f'<div class="card"><h3>{title}</h3>{text}</div>',unsafe_allow_html=True)

# ============================================================
# CLICKABLE PREDICTION HISTORY
# ============================================================
st.markdown('<div class="section-title">🗄️ Prediction History</div>',unsafe_allow_html=True)
history_df=load_prediction_history()
if not history_df.empty:
    hc1,hc2=st.columns([5,1])
    with hc2:
        if st.button("🗑️ Clear History",use_container_width=True,key="clear_prediction_history"): clear_prediction_history(); st.session_state.pop("selected_prediction_id",None); st.rerun()
    event=st.dataframe(history_df,use_container_width=True,hide_index=True,on_select="rerun",selection_mode="single-row",key="prediction_history_table")
    selected_rows=event.selection.rows if hasattr(event,"selection") else []
    if selected_rows:
        record_id=int(history_df.iloc[selected_rows[0]]["ID"]); st.session_state["selected_prediction_id"]=record_id
    selected_id=st.session_state.get("selected_prediction_id")
    if selected_id:
        record=get_prediction_record(selected_id)
        if record is not None:
            with st.container(border=True): render_prediction_report(record)
else: st.info("No prediction history yet. Click Predict & Optimize to save a result.")

# ============================================================
# CLICKABLE VOYAGE HISTORY
# ============================================================
st.markdown('<div class="section-title">🧭 Voyage Segment History</div>',unsafe_allow_html=True)
segment_history=load_segment_history()
if not segment_history.empty:
    sh1,sh2=st.columns([5,1])
    with sh2:
        if st.button("🗑️ Clear Voyage History",use_container_width=True,key="clear_voyage_history"): clear_voyage_segment_history(); st.session_state.pop("selected_segment_id",None); st.rerun()
    event2=st.dataframe(segment_history,use_container_width=True,hide_index=True,on_select="rerun",selection_mode="single-row",key="voyage_history_table")
    selected_rows2=event2.selection.rows if hasattr(event2,"selection") else []
    if selected_rows2:
        segment_id=int(segment_history.iloc[selected_rows2[0]]["ID"]); st.session_state["selected_segment_id"]=segment_id
    selected_seg_id=st.session_state.get("selected_segment_id")
    if selected_seg_id:
        seg_record=get_segment_record(selected_seg_id)
        if seg_record is not None:
            with st.container(border=True): render_voyage_report(seg_record)
else: st.info("No dynamic voyage results saved yet.")
