import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sqlite3
from datetime import datetime
import math

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Quantum-Inspired Green Fleet Management",
    page_icon="🚢",
    layout="wide"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.main-title {
    font-size: 36px;
    font-weight: 800;
    text-align: center;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    font-size: 17px;
    margin-bottom: 25px;
}

.section-title {
    font-size: 25px;
    font-weight: 700;
    margin-top: 25px;
    margin-bottom: 15px;
}

.metric-box {
    padding: 15px;
    border-radius: 10px;
    text-align: center;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# DATABASE
# ============================================================

DB_NAME = "fleet_database.db"


def init_database():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            capacity REAL,
            speed REAL,
            distance REAL,
            fuel_type TEXT,
            weather TEXT,
            wind REAL,
            wave REAL,
            current REAL,
            fuel_consumption REAL,
            cost REAL,
            co2 REAL,
            green_score REAL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS voyage_segments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            segment INTEGER,
            latitude REAL,
            longitude REAL,
            distance REAL,
            speed REAL,
            fuel_type TEXT,
            weather TEXT,
            wind REAL,
            wave REAL,
            current REAL,
            fuel_consumption REAL,
            cost REAL,
            co2 REAL,
            alert TEXT
        )
    """)

    conn.commit()
    conn.close()


init_database()

# ============================================================
# PREDICTION DATABASE FUNCTIONS
# ============================================================

def save_prediction(
    capacity,
    speed,
    distance,
    fuel_type,
    weather,
    wind,
    wave,
    current,
    fuel_consumption,
    cost,
    co2,
    green_score
):

    conn = sqlite3.connect(DB_NAME)

    conn.execute("""
        INSERT INTO predictions (
            timestamp,
            capacity,
            speed,
            distance,
            fuel_type,
            weather,
            wind,
            wave,
            current,
            fuel_consumption,
            cost,
            co2,
            green_score
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        capacity,
        speed,
        distance,
        fuel_type,
        weather,
        wind,
        wave,
        current,
        fuel_consumption,
        cost,
        co2,
        green_score
    ))

    conn.commit()
    conn.close()


def load_prediction_history(limit=20):

    conn = sqlite3.connect(DB_NAME)

    df = pd.read_sql_query(
        f"""
        SELECT *
        FROM predictions
        ORDER BY id DESC
        LIMIT {limit}
        """,
        conn
    )

    conn.close()

    return df


def clear_prediction_history():

    conn = sqlite3.connect(DB_NAME)

    conn.execute("DELETE FROM predictions")

    conn.commit()
    conn.close()


# ============================================================
# VOYAGE DATABASE FUNCTIONS
# ============================================================

def save_voyage_segments(rows):

    conn = sqlite3.connect(DB_NAME)

    conn.executemany("""
        INSERT INTO voyage_segments (
            timestamp,
            segment,
            latitude,
            longitude,
            distance,
            speed,
            fuel_type,
            weather,
            wind,
            wave,
            current,
            fuel_consumption,
            cost,
            co2,
            alert
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, rows)

    conn.commit()
    conn.close()


def load_segment_history(limit=50):

    conn = sqlite3.connect(DB_NAME)

    df = pd.read_sql_query(
        f"""
        SELECT *
        FROM voyage_segments
        ORDER BY id DESC
        LIMIT {limit}
        """,
        conn
    )

    conn.close()

    return df


# ============================================================
# NEW: CLEAR VOYAGE HISTORY
# ============================================================

def clear_voyage_history():

    # Delete voyage records from SQLite
    conn = sqlite3.connect(DB_NAME)

    conn.execute("DELETE FROM voyage_segments")

    conn.commit()
    conn.close()

    # Clear current voyage data from Streamlit session
    voyage_keys = [
        "voyage_conditions",
        "voyage_segments_df",
        "voyage_total_fuel",
        "voyage_total_cost",
        "voyage_total_co2",
        "voyage_hours",
        "route",
        "voyage_done"
    ]

    for key in voyage_keys:

        if key in st.session_state:
            del st.session_state[key]

    # Reset live tracking
    st.session_state["track_step"] = 0


# ============================================================
# FUEL DATA
# ============================================================

FUEL_DATA = {

    "Diesel": {
        "consumption_factor": 1.00,
        "co2_factor": 3.20,
        "cost": 65000,
        "green_score": 35
    },

    "Petrol": {
        "consumption_factor": 1.08,
        "co2_factor": 3.10,
        "cost": 70000,
        "green_score": 30
    },

    "LNG": {
        "consumption_factor": 0.94,
        "co2_factor": 2.75,
        "cost": 57000,
        "green_score": 62
    },

    "Methanol": {
        "consumption_factor": 1.02,
        "co2_factor": 1.95,
        "cost": 61000,
        "green_score": 75
    },

    "Hydrogen": {
        "consumption_factor": 0.72,
        "co2_factor": 0.55,
        "cost": 92000,
        "green_score": 91
    },

    "Ammonia": {
        "consumption_factor": 0.86,
        "co2_factor": 0.30,
        "cost": 72000,
        "green_score": 88
    }
}


# ============================================================
# WEATHER DATA
# ============================================================

WEATHER_FACTORS = {

    "Calm Sea": 0.92,
    "Normal": 1.00,
    "Moderate": 1.08,
    "Heavy Weather": 1.18,
    "Storm": 1.32

}


# ============================================================
# FUEL CONSUMPTION MODEL
# ============================================================

def base_fuel(
    capacity,
    speed,
    distance,
    fuel
):

    fuel_factor = FUEL_DATA[fuel]["consumption_factor"]

    base = (
        capacity
        * distance
        * (speed / 15) ** 3
        * 0.00001
    )

    return base * fuel_factor


# ============================================================
# ENVIRONMENTAL FACTOR
# ============================================================

def environmental_factor(
    weather,
    wind,
    wave,
    current
):

    weather_factor = WEATHER_FACTORS[weather]

    wind_factor = 1 + (wind / 100)

    wave_factor = 1 + (wave / 10)

    current_factor = 1 + (current / 5)

    factor = (
        weather_factor
        * wind_factor
        * wave_factor
        * current_factor
    )

    return factor


# ============================================================
# PREDICT FUEL
# ============================================================

def predict_fuel(
    capacity,
    speed,
    distance,
    fuel,
    weather,
    wind,
    wave,
    current
):

    base = base_fuel(
        capacity,
        speed,
        distance,
        fuel
    )

    environmental = environmental_factor(
        weather,
        wind,
        wave,
        current
    )

    return base * environmental


# ============================================================
# CO2 CALCULATION
# ============================================================

def calculate_co2(
    fuel_consumption,
    fuel
):

    return (
        fuel_consumption
        * FUEL_DATA[fuel]["co2_factor"]
    )


# ============================================================
# HAVERSINE DISTANCE
# ============================================================

def haversine_km(
    lat1,
    lon1,
    lat2,
    lon2
):

    R = 6371

    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)

    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        math.sin(dlat / 2) ** 2
        +
        math.cos(lat1)
        * math.cos(lat2)
        * math.sin(dlon / 2) ** 2
    )

    c = 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a)
    )

    return R * c


# ============================================================
# INTERPOLATE POSITION
# ============================================================

def interpolate_position(
    start,
    end,
    fraction
):

    lat = (
        start[0]
        + (end[0] - start[0]) * fraction
    )

    lon = (
        start[1]
        + (end[1] - start[1]) * fraction
    )

    return lat, lon


# ============================================================
# GENERATE SEGMENT CONDITIONS
# ============================================================

def generate_segment_conditions(
    segments
):

    conditions = []

    weather_list = list(
        WEATHER_FACTORS.keys()
    )

    for i in range(segments):

        weather = np.random.choice(
            weather_list
        )

        wind = round(
            np.random.uniform(5, 35),
            2
        )

        wave = round(
            np.random.uniform(0.5, 5),
            2
        )

        current = round(
            np.random.uniform(-2, 2),
            2
        )

        conditions.append({

            "weather": weather,
            "wind": wind,
            "wave": wave,
            "current": current

        })

    return conditions


# ============================================================
# ALERT LEVEL
# ============================================================

def alert_level(weather):

    if weather == "Storm":

        return "🔴 Critical"

    elif weather == "Heavy Weather":

        return "🟠 Warning"

    elif weather == "Moderate":

        return "🟡 Moderate"

    else:

        return "🟢 Safe"


# ============================================================
# QUANTUM-INSPIRED OPTIMIZATION
# ============================================================

def optimize_single_segment(
    capacity,
    distance,
    requested_speed,
    available_fuels,
    weather,
    wind,
    wave,
    current
):

    results = []

    speed_candidates = np.arange(
        max(8, requested_speed - 3),
        requested_speed + 3.1,
        0.5
    )

    for candidate_speed in speed_candidates:

        for fuel in available_fuels:

            fuel_consumption = predict_fuel(
                capacity,
                candidate_speed,
                distance,
                fuel,
                weather,
                wind,
                wave,
                current
            )

            cost = (
                fuel_consumption
                * FUEL_DATA[fuel]["cost"]
            )

            co2 = calculate_co2(
                fuel_consumption,
                fuel
            )

            cargo_penalty = 0

            objective = (
                cost * 0.55
                +
                co2 * 12000 * 0.35
                +
                abs(
                    candidate_speed - 17
                )
                * cost
                * 0.03
                +
                cargo_penalty
            )

            results.append({

                "speed": candidate_speed,
                "fuel": fuel,
                "fuel_consumption": fuel_consumption,
                "cost": cost,
                "co2": co2,
                "objective": objective

            })

    result_df = pd.DataFrame(results)

    best = result_df.sort_values(
        "objective"
    ).iloc[0]

    return best, result_df


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🚢 Quantum-Inspired Optimization & Prediction Framework for Green Fleet Management</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">AI + Optimization for Fuel Efficiency, Cost Reduction and Green Maritime Operations</div>',
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("⚙️ System Controls")

capacity = st.sidebar.number_input(
    "Ship Capacity (tons)",
    min_value=100.0,
    value=5000.0,
    step=100.0
)

speed = st.sidebar.number_input(
    "Cruising Speed (knots)",
    min_value=5.0,
    max_value=40.0,
    value=17.0,
    step=0.5
)

distance = st.sidebar.number_input(
    "Distance (km)",
    min_value=10.0,
    value=500.0,
    step=10.0
)

fuel_type = st.sidebar.selectbox(
    "Fuel Type",
    list(FUEL_DATA.keys())
)

weather = st.sidebar.selectbox(
    "Weather Condition",
    list(WEATHER_FACTORS.keys())
)

wind = st.sidebar.slider(
    "Wind Speed (%)",
    0.0,
    50.0,
    10.0
)

wave = st.sidebar.slider(
    "Wave Height (m)",
    0.0,
    10.0,
    2.0
)

current = st.sidebar.slider(
    "Current (m/s)",
    -5.0,
    5.0,
    0.0
)


# ============================================================
# CURRENT FUEL PREDICTION
# ============================================================

st.markdown(
    '<div class="section-title">⛽ Current Fuel Prediction</div>',
    unsafe_allow_html=True
)

if st.button(
    "🔮 Predict Fuel Consumption",
    use_container_width=True
):

    fuel_consumption = predict_fuel(
        capacity,
        speed,
        distance,
        fuel_type,
        weather,
        wind,
        wave,
        current
    )

    cost = (
        fuel_consumption
        * FUEL_DATA[fuel_type]["cost"]
    )

    co2 = calculate_co2(
        fuel_consumption,
        fuel_type
    )

    green_score = FUEL_DATA[
        fuel_type
    ]["green_score"]

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Fuel Consumption",
        f"{fuel_consumption:.2f}"
    )

    c2.metric(
        "Estimated Cost",
        f"₹{cost:,.0f}"
    )

    c3.metric(
        "CO₂ Emissions",
        f"{co2:.2f}"
    )

    c4.metric(
        "Green Score",
        f"{green_score}/100"
    )

    save_prediction(
        capacity,
        speed,
        distance,
        fuel_type,
        weather,
        wind,
        wave,
        current,
        fuel_consumption,
        cost,
        co2,
        green_score
    )

    st.success(
        "Prediction saved successfully!"
    )


# ============================================================
# FUEL COMPARISON
# ============================================================

st.markdown(
    '<div class="section-title">🔋 Fuel Comparison</div>',
    unsafe_allow_html=True
)

fuel_comparison = []

for fuel in FUEL_DATA:

    fc = predict_fuel(
        capacity,
        speed,
        distance,
        fuel,
        weather,
        wind,
        wave,
        current
    )

    fuel_cost = (
        fc
        * FUEL_DATA[fuel]["cost"]
    )

    fuel_co2 = calculate_co2(
        fc,
        fuel
    )

    fuel_comparison.append({

        "Fuel": fuel,
        "Consumption": round(fc, 2),
        "Cost": round(fuel_cost, 2),
        "CO₂": round(fuel_co2, 2),
        "Green Score":
            FUEL_DATA[fuel]["green_score"]

    })

fuel_df = pd.DataFrame(
    fuel_comparison
)

st.dataframe(
    fuel_df,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# OPTIMIZATION
# ============================================================

st.markdown(
    '<div class="section-title">⚛️ Quantum-Inspired Optimization</div>',
    unsafe_allow_html=True
)

available_fuels = st.multiselect(
    "Select Available Fuels",
    list(FUEL_DATA.keys()),
    default=["Diesel", "LNG", "Methanol"]
)

if st.button(
    "⚛️ Run Optimization",
    use_container_width=True
):

    if not available_fuels:

        st.error(
            "Please select at least one fuel."
        )

    else:

        best, optimization_df = optimize_single_segment(
            capacity,
            distance,
            speed,
            available_fuels,
            weather,
            wind,
            wave,
            current
        )

        o1, o2, o3, o4 = st.columns(4)

        o1.metric(
            "Recommended Fuel",
            best["fuel"]
        )

        o2.metric(
            "Optimized Speed",
            f"{best['speed']:.1f} knots"
        )

        o3.metric(
            "Fuel",
            f"{best['fuel_consumption']:.2f}"
        )

        o4.metric(
            "CO₂",
            f"{best['co2']:.2f}"
        )

        st.success(
            f"Recommended combination: "
            f"{best['fuel']} at "
            f"{best['speed']:.1f} knots"
        )

        st.dataframe(
            optimization_df.sort_values(
                "objective"
            ).head(20),
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# OPTIMIZATION GRAPH
# ============================================================

if "optimization_df" in st.session_state:

    pass


# ============================================================
# PREDICTION HISTORY
# ============================================================

st.markdown(
    '<div class="section-title">📊 Prediction History</div>',
    unsafe_allow_html=True
)

prediction_history = load_prediction_history()

if not prediction_history.empty:

    pc1, pc2 = st.columns([5, 1])

    with pc2:

        if st.button(
            "🗑️ Clear History",
            use_container_width=True
        ):

            clear_prediction_history()

            st.success(
                "Prediction history cleared successfully!"
            )

            st.rerun()

    st.dataframe(
        prediction_history,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No prediction history available."
    )


# ============================================================
# DYNAMIC VOYAGE
# ============================================================

st.markdown(
    '<div class="section-title">🧭 Dynamic Voyage Optimization</div>',
    unsafe_allow_html=True
)

vc1, vc2 = st.columns(2)

with vc1:

    start_lat = st.number_input(
        "Start Latitude",
        value=13.0827,
        format="%.4f"
    )

    start_lon = st.number_input(
        "Start Longitude",
        value=80.2707,
        format="%.4f"
    )

with vc2:

    end_lat = st.number_input(
        "Destination Latitude",
        value=9.9312,
        format="%.4f"
    )

    end_lon = st.number_input(
        "Destination Longitude",
        value=76.2673,
        format="%.4f"
    )


segment_count = st.slider(
    "Number of Voyage Segments",
    2,
    20,
    6
)

simulation_mode = st.radio(
    "Condition Mode",
    [
        "Dynamic Simulation",
        "Manual Conditions"
    ]
)


# ============================================================
# MANUAL CONDITIONS
# ============================================================

manual_conditions = []

if simulation_mode == "Manual Conditions":

    st.markdown(
        "### Enter Conditions for Each Segment"
    )

    for i in range(segment_count):

        mc1, mc2, mc3, mc4 = st.columns(4)

        with mc1:

            m_weather = st.selectbox(
                f"Segment {i+1} Weather",
                list(WEATHER_FACTORS.keys()),
                key=f"weather_{i}"
            )

        with mc2:

            m_wind = st.number_input(
                f"Segment {i+1} Wind",
                0.0,
                50.0,
                10.0,
                key=f"wind_{i}"
            )

        with mc3:

            m_wave = st.number_input(
                f"Segment {i+1} Wave",
                0.0,
                10.0,
                2.0,
                key=f"wave_{i}"
            )

        with mc4:

            m_current = st.number_input(
                f"Segment {i+1} Current",
                -5.0,
                5.0,
                0.0,
                key=f"current_{i}"
            )

        manual_conditions.append({

            "weather": m_weather,
            "wind": m_wind,
            "wave": m_wave,
            "current": m_current

        })


# ============================================================
# RUN VOYAGE
# ============================================================

if st.button(
    "🚢 Run Dynamic Voyage Optimization",
    use_container_width=True
):

    route_start = (
        start_lat,
        start_lon
    )

    route_end = (
        end_lat,
        end_lon
    )

    total_distance = haversine_km(
        start_lat,
        start_lon,
        end_lat,
        end_lon
    )

    segment_distance = (
        total_distance
        / segment_count
    )

    if simulation_mode == "Dynamic Simulation":

        conditions = generate_segment_conditions(
            segment_count
        )

    else:

        conditions = manual_conditions

    voyage_rows = []

    total_fuel = 0
    total_cost = 0
    total_co2 = 0
    total_hours = 0

    voyage_results = []

    for i in range(segment_count):

        fraction = (
            i / segment_count
        )

        lat, lon = interpolate_position(
            route_start,
            route_end,
            fraction
        )

        cond = conditions[i]

        best, _ = optimize_single_segment(
            capacity,
            segment_distance,
            speed,
            available_fuels
            if available_fuels
            else ["Diesel"],
            cond["weather"],
            cond["wind"],
            cond["wave"],
            cond["current"]
        )

        seg_fuel = float(
            best["fuel_consumption"]
        )

        seg_cost = float(
            best["cost"]
        )

        seg_co2 = float(
            best["co2"]
        )

        seg_speed = float(
            best["speed"]
        )

        seg_fuel_type = best["fuel"]

        seg_hours = (
            segment_distance
            / (seg_speed * 1.852)
        )

        total_fuel += seg_fuel
        total_cost += seg_cost
        total_co2 += seg_co2
        total_hours += seg_hours

        alert = alert_level(
            cond["weather"]
        )

        voyage_results.append({

            "Segment": i + 1,
            "Latitude": round(lat, 5),
            "Longitude": round(lon, 5),
            "Distance": round(
                segment_distance,
                2
            ),
            "Speed": round(
                seg_speed,
                2
            ),
            "Fuel": seg_fuel_type,
            "Weather": cond["weather"],
            "Wind": cond["wind"],
            "Wave": cond["wave"],
            "Current": cond["current"],
            "Fuel Consumption": round(
                seg_fuel,
                2
            ),
            "Cost": round(
                seg_cost,
                2
            ),
            "CO₂": round(
                seg_co2,
                2
            ),
            "Alert": alert

        })

        voyage_rows.append((

            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

            i + 1,

            lat,
            lon,

            segment_distance,

            seg_speed,

            seg_fuel_type,

            cond["weather"],

            cond["wind"],
            cond["wave"],
            cond["current"],

            seg_fuel,
            seg_cost,
            seg_co2,

            alert

        ))

    voyage_df = pd.DataFrame(
        voyage_results
    )

    save_voyage_segments(
        voyage_rows
    )

    st.session_state[
        "voyage_conditions"
    ] = conditions

    st.session_state[
        "voyage_segments_df"
    ] = voyage_df

    st.session_state[
        "voyage_total_fuel"
    ] = total_fuel

    st.session_state[
        "voyage_total_cost"
    ] = total_cost

    st.session_state[
        "voyage_total_co2"
    ] = total_co2

    st.session_state[
        "voyage_hours"
    ] = total_hours

    st.session_state[
        "route"
    ] = (
        route_start,
        route_end
    )

    st.session_state[
        "voyage_done"
    ] = True

    st.session_state[
        "track_step"
    ] = 0

    st.success(
        "Dynamic voyage optimization completed successfully!"
    )


# ============================================================
# VOYAGE RESULTS
# ============================================================

if st.session_state.get(
    "voyage_done",
    False
):

    st.markdown(
        '<div class="section-title">📈 Voyage Results</div>',
        unsafe_allow_html=True
    )

    total_fuel = st.session_state[
        "voyage_total_fuel"
    ]

    total_cost = st.session_state[
        "voyage_total_cost"
    ]

    total_co2 = st.session_state[
        "voyage_total_co2"
    ]

    total_hours = st.session_state[
        "voyage_hours"
    ]

    r1, r2, r3, r4 = st.columns(4)

    r1.metric(
        "Total Fuel",
        f"{total_fuel:.2f}"
    )

    r2.metric(
        "Total Cost",
        f"₹{total_cost:,.0f}"
    )

    r3.metric(
        "Total CO₂",
        f"{total_co2:.2f}"
    )

    r4.metric(
        "Voyage Time",
        f"{total_hours:.2f} hrs"
    )

    voyage_df = st.session_state[
        "voyage_segments_df"
    ]

    st.dataframe(
        voyage_df,
        use_container_width=True,
        hide_index=True
    )

    # ========================================================
    # VOYAGE GRAPHS
    # ========================================================

    g1, g2 = st.columns(2)

    with g1:

        fig1, ax1 = plt.subplots()

        ax1.plot(
            voyage_df["Segment"],
            voyage_df["Fuel Consumption"],
            marker="o"
        )

        ax1.set_xlabel(
            "Segment"
        )

        ax1.set_ylabel(
            "Fuel Consumption"
        )

        ax1.set_title(
            "Fuel Consumption by Segment"
        )

        st.pyplot(fig1)

    with g2:

        fig2, ax2 = plt.subplots()

        ax2.plot(
            voyage_df["Segment"],
            voyage_df["CO₂"],
            marker="o"
        )

        ax2.set_xlabel(
            "Segment"
        )

        ax2.set_ylabel(
            "CO₂"
        )

        ax2.set_title(
            "CO₂ Emissions by Segment"
        )

        st.pyplot(fig2)


# ============================================================
# LIVE TRACKING
# ============================================================

st.markdown(
    '<div class="section-title">📍 Live Voyage Tracking</div>',
    unsafe_allow_html=True
)

if "track_step" not in st.session_state:

    st.session_state[
        "track_step"
    ] = 0


if st.session_state.get(
    "voyage_done",
    False
):

    voyage_df = st.session_state[
        "voyage_segments_df"
    ]

    total_segments = len(
        voyage_df
    )

    tc1, tc2 = st.columns(2)

    with tc1:

        if st.button(
            "▶️ Next Live Update",
            use_container_width=True
        ):

            if (
                st.session_state[
                    "track_step"
                ]
                <
                total_segments - 1
            ):

                st.session_state[
                    "track_step"
                ] += 1

            st.rerun()

    with tc2:

        if st.button(
            "🔄 Reset Tracking",
            use_container_width=True
        ):

            st.session_state[
                "track_step"
            ] = 0

            st.rerun()

    step = st.session_state[
        "track_step"
    ]

    current_segment = voyage_df.iloc[
        step
    ]

    t1, t2, t3, t4 = st.columns(4)

    t1.metric(
        "Current Segment",
        f"{step + 1}/{total_segments}"
    )

    t2.metric(
        "Latitude",
        f"{current_segment['Latitude']:.5f}"
    )

    t3.metric(
        "Longitude",
        f"{current_segment['Longitude']:.5f}"
    )

    t4.metric(
        "Weather",
        current_segment["Weather"]
    )

    st.info(
        f"🚢 Vessel is currently at "
        f"Segment {step + 1} | "
        f"Fuel: {current_segment['Fuel']} | "
        f"Speed: {current_segment['Speed']:.1f} knots | "
        f"Alert: {current_segment['Alert']}"
    )

    # ========================================================
    # ROUTE PLOT
    # ========================================================

    route_start, route_end = st.session_state[
        "route"
    ]

    fig3, ax3 = plt.subplots()

    ax3.plot(
        [route_start[1], route_end[1]],
        [route_start[0], route_end[0]],
        linestyle="--",
        marker="o"
    )

    ax3.scatter(
        current_segment["Longitude"],
        current_segment["Latitude"],
        s=150
    )

    ax3.set_xlabel(
        "Longitude"
    )

    ax3.set_ylabel(
        "Latitude"
    )

    ax3.set_title(
        "Live Vessel Tracking"
    )

    st.pyplot(fig3)

else:

    st.info(
        "Run Dynamic Voyage Optimization first to start live tracking."
    )


# ============================================================
# VOYAGE SEGMENT HISTORY
# ============================================================

st.markdown(
    '<div class="section-title">🧭 Voyage Segment History</div>',
    unsafe_allow_html=True
)

segment_history = load_segment_history()

if not segment_history.empty:

    vc1, vc2 = st.columns([5, 1])

    with vc2:

        if st.button(
            "🗑️ Clear Voyage History",
            use_container_width=True
        ):

            clear_voyage_history()

            st.success(
                "Voyage history cleared successfully!"
            )

            st.rerun()

    st.dataframe(
        segment_history,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No dynamic voyage results saved yet."
    )


# ============================================================
# DECISION EXPLANATION
# ============================================================

st.markdown(
    '<div class="section-title">🧠 Decision Explanation</div>',
    unsafe_allow_html=True
)

st.write("""
### How the system works

**1. Prediction**

The system estimates fuel consumption using:

- Ship capacity
- Vessel speed
- Voyage distance
- Fuel type
- Weather
- Wind
- Wave conditions
- Ocean current

**2. Optimization**

The quantum-inspired optimization layer evaluates different:

- Speeds
- Fuel choices
- Operating conditions

and selects a feasible combination with a lower overall objective.

**3. Objective**

The optimization considers:

- Fuel cost
- CO₂ emissions
- Speed deviation
- Operational constraints

**4. Dynamic Voyage**

The complete voyage is divided into multiple segments.

Each segment can have different:

- Weather
- Wind
- Wave
- Current
- Speed
- Fuel choice

**5. Live Tracking**

The vessel position is simulated segment-by-segment so that the dashboard can show the current vessel location and operating condition.
""")


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "Quantum-Inspired Optimization and Prediction Framework for Green Fleet Management"
)
