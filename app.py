import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sqlite3
from datetime import datetime
import math

# ============================================================
# QUANTUM PREDICTORS - GREEN FLEET OPTIMIZATION
# ============================================================

DB_NAME = "fleet_database.db"

# ============================================================
# WORLDWIDE PORT DATABASE
# ============================================================

WORLD_PORTS = {
    # INDIA
    "Chennai, India": (13.0827, 80.2707),
    "Mumbai, India": (19.0760, 72.8777),
    "Kochi, India": (9.9312, 76.2673),
    "Visakhapatnam, India": (17.6868, 83.2185),
    "Kolkata, India": (22.5726, 88.3639),
    "Kandla, India": (23.0333, 70.2167),
    "Mundra, India": (22.8390, 69.7210),
    "Goa, India": (15.4909, 73.8278),
    "Tuticorin, India": (8.7642, 78.1348),
    "Paradip, India": (20.2961, 86.7025),

    # ASIA
    "Singapore": (1.2903, 103.8519),
    "Port Klang, Malaysia": (3.0000, 101.4000),
    "Tanjung Pelepas, Malaysia": (1.3600, 103.5500),
    "Jakarta, Indonesia": (-6.1040, 106.8800),
    "Surabaya, Indonesia": (-7.2050, 112.7300),
    "Colombo, Sri Lanka": (6.9271, 79.8612),
    "Dubai, UAE": (25.2760, 55.2962),
    "Abu Dhabi, UAE": (24.4539, 54.3773),
    "Jebel Ali, UAE": (24.9857, 55.0273),
    "Doha, Qatar": (25.2854, 51.5310),
    "Dammam, Saudi Arabia": (26.4207, 50.0888),
    "Jeddah, Saudi Arabia": (21.4858, 39.1925),
    "Muscat, Oman": (23.5880, 58.3829),
    "Karachi, Pakistan": (24.8607, 67.0011),
    "Chittagong, Bangladesh": (22.3569, 91.7832),
    "Yangon, Myanmar": (16.8409, 96.1735),
    "Bangkok, Thailand": (13.7563, 100.5018),
    "Ho Chi Minh City, Vietnam": (10.8231, 106.6297),
    "Haiphong, Vietnam": (20.8449, 106.6881),
    "Manila, Philippines": (14.5995, 120.9842),
    "Hong Kong": (22.3193, 114.1694),
    "Shanghai, China": (31.2304, 121.4737),
    "Ningbo, China": (29.8683, 121.5440),
    "Shenzhen, China": (22.5431, 114.0579),
    "Guangzhou, China": (23.1291, 113.2644),
    "Qingdao, China": (36.0671, 120.3826),
    "Tianjin, China": (39.3434, 117.3616),
    "Dalian, China": (38.9140, 121.6147),
    "Busan, South Korea": (35.1796, 129.0756),
    "Incheon, South Korea": (37.4563, 126.7052),
    "Tokyo, Japan": (35.6762, 139.6503),
    "Yokohama, Japan": (35.4437, 139.6380),
    "Osaka, Japan": (34.6937, 135.5023),
    "Nagoya, Japan": (35.1815, 136.9066),
    "Taipei, Taiwan": (25.0330, 121.5654),
    "Kaohsiung, Taiwan": (22.6273, 120.3014),
    "Vladivostok, Russia": (43.1155, 131.8855),

    # EUROPE
    "Rotterdam, Netherlands": (51.9244, 4.4777),
    "Amsterdam, Netherlands": (52.3676, 4.9041),
    "Antwerp, Belgium": (51.2194, 4.4025),
    "Hamburg, Germany": (53.5511, 9.9937),
    "Bremerhaven, Germany": (53.5396, 8.5809),
    "London, UK": (51.5074, -0.1278),
    "Southampton, UK": (50.9097, -1.4044),
    "Liverpool, UK": (53.4084, -2.9916),
    "Le Havre, France": (49.4944, 0.1079),
    "Marseille, France": (43.2965, 5.3698),
    "Barcelona, Spain": (41.3874, 2.1686),
    "Valencia, Spain": (39.4699, -0.3763),
    "Lisbon, Portugal": (38.7223, -9.1393),
    "Genoa, Italy": (44.4056, 8.9463),
    "Naples, Italy": (40.8518, 14.2681),
    "Piraeus, Greece": (37.9838, 23.7275),
    "Istanbul, Turkey": (41.0082, 28.9784),
    "Athens, Greece": (37.9838, 23.7275),
    "Gdansk, Poland": (54.3520, 18.6466),
    "Helsinki, Finland": (60.1699, 24.9384),

    # AFRICA
    "Cape Town, South Africa": (-33.9249, 18.4241),
    "Durban, South Africa": (-29.8587, 31.0218),
    "Port Elizabeth, South Africa": (-33.9608, 25.6022),
    "Lagos, Nigeria": (6.5244, 3.3792),
    "Port Harcourt, Nigeria": (4.8156, 7.0498),
    "Alexandria, Egypt": (31.2001, 29.9187),
    "Port Said, Egypt": (31.2653, 32.3019),
    "Casablanca, Morocco": (33.5731, -7.5898),
    "Tangier, Morocco": (35.7595, -5.8340),
    "Mombasa, Kenya": (-4.0435, 39.6682),
    "Dar es Salaam, Tanzania": (-6.7924, 39.2083),

    # NORTH AMERICA
    "New York, USA": (40.7128, -74.0060),
    "Los Angeles, USA": (34.0522, -118.2437),
    "Long Beach, USA": (33.7701, -118.1937),
    "Houston, USA": (29.7604, -95.3698),
    "Miami, USA": (25.7617, -80.1918),
    "New Orleans, USA": (29.9511, -90.0715),
    "Savannah, USA": (32.0809, -81.0912),
    "Seattle, USA": (47.6062, -122.3321),
    "Oakland, USA": (37.8044, -122.2712),
    "Vancouver, Canada": (49.2827, -123.1207),
    "Montreal, Canada": (45.5017, -73.5673),
    "Halifax, Canada": (44.6488, -63.5752),
    "Manzanillo, Mexico": (19.1138, -104.3385),
    "Veracruz, Mexico": (19.1738, -96.1342),

    # SOUTH AMERICA
    "Santos, Brazil": (-23.9608, -46.3336),
    "Rio de Janeiro, Brazil": (-22.9068, -43.1729),
    "Buenos Aires, Argentina": (-34.6037, -58.3816),
    "Montevideo, Uruguay": (-34.9011, -56.1645),
    "Valparaiso, Chile": (-33.0472, -71.6127),
    "Callao, Peru": (-12.0464, -77.0428),
    "Guayaquil, Ecuador": (-2.1709, -79.9224),
    "Cartagena, Colombia": (10.3910, -75.4794),

    # AUSTRALIA / OCEANIA
    "Sydney, Australia": (-33.8688, 151.2093),
    "Melbourne, Australia": (-37.8136, 144.9631),
    "Brisbane, Australia": (-27.4698, 153.0251),
    "Perth, Australia": (-31.9505, 115.8605),
    "Adelaide, Australia": (-34.9285, 138.6007),
    "Fremantle, Australia": (-32.0569, 115.7439),
    "Auckland, New Zealand": (-36.8509, 174.7645),
    "Wellington, New Zealand": (-41.2866, 174.7756),
    "Suva, Fiji": (-18.1416, 178.4419),
}

PORT_NAMES = list(WORLD_PORTS.keys())


# ============================================================
# DATABASE
# ============================================================

def init_database():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            vessel_type TEXT NOT NULL,
            capacity REAL NOT NULL,
            speed REAL NOT NULL,
            distance REAL NOT NULL,
            cargo REAL NOT NULL,
            current_fuel TEXT NOT NULL,
            fuel_price REAL NOT NULL,
            weather TEXT NOT NULL,
            predicted_fuel REAL NOT NULL,
            initial_cost REAL NOT NULL,
            initial_co2 REAL NOT NULL,
            optimized_fuel_type TEXT,
            optimized_speed REAL,
            optimized_fuel REAL,
            optimized_cost REAL,
            optimized_co2 REAL,
            fuel_saving REAL,
            cost_saving REAL,
            co2_reduction REAL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS voyage_segments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            segment_no INTEGER NOT NULL,
            distance_km REAL NOT NULL,
            weather TEXT NOT NULL,
            wind_speed REAL NOT NULL,
            wind_direction REAL NOT NULL,
            wave_height REAL NOT NULL,
            current_speed REAL NOT NULL,
            current_direction REAL NOT NULL,
            selected_fuel TEXT NOT NULL,
            selected_speed REAL NOT NULL,
            fuel_consumption REAL NOT NULL,
            co2 REAL NOT NULL,
            cost REAL NOT NULL,
            alert TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def save_prediction(
    vessel_type,
    capacity,
    speed,
    distance,
    cargo,
    fuel_type,
    fuel_price,
    weather,
    initial_fuel,
    initial_cost,
    initial_co2,
    best_solution,
    fuel_saving,
    cost_saving,
    co2_reduction
):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO predictions (
            created_at,
            vessel_type,
            capacity,
            speed,
            distance,
            cargo,
            current_fuel,
            fuel_price,
            weather,
            predicted_fuel,
            initial_cost,
            initial_co2,
            optimized_fuel_type,
            optimized_speed,
            optimized_fuel,
            optimized_cost,
            optimized_co2,
            fuel_saving,
            cost_saving,
            co2_reduction
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        vessel_type,
        capacity,
        speed,
        distance,
        cargo,
        fuel_type,
        fuel_price,
        weather,
        initial_fuel,
        initial_cost,
        initial_co2,
        best_solution["fuel"],
        best_solution["speed"],
        best_solution["fuel_consumption"],
        best_solution["cost"],
        best_solution["co2"],
        fuel_saving,
        cost_saving,
        co2_reduction
    ))

    conn.commit()
    conn.close()


def load_prediction_history(limit=20):
    conn = sqlite3.connect(DB_NAME)

    df = pd.read_sql_query("""
        SELECT
            id AS ID,
            created_at AS "Date & Time",
            vessel_type AS "Vessel",
            capacity AS "Capacity (t)",
            speed AS "Speed (knots)",
            distance AS "Distance (km)",
            cargo AS "Cargo (t)",
            current_fuel AS "Current Fuel",
            weather AS "Weather",
            predicted_fuel AS "Predicted Fuel (t)",
            initial_cost AS "Initial Cost (₹)",
            initial_co2 AS "Initial CO₂ (t)",
            optimized_fuel_type AS "Optimized Fuel",
            optimized_speed AS "Optimized Speed",
            optimized_fuel AS "Optimized Fuel (t)",
            optimized_cost AS "Optimized Cost (₹)",
            optimized_co2 AS "Optimized CO₂ (t)",
            fuel_saving AS "Fuel Saving (%)",
            cost_saving AS "Cost Saving (%)",
            co2_reduction AS "CO₂ Reduction (%)"
        FROM predictions
        ORDER BY id DESC
        LIMIT ?
    """, conn, params=(limit,))

    conn.close()
    return df


def clear_prediction_history():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("DELETE FROM predictions")
    conn.commit()
    conn.close()


def save_voyage_segments(rows):
    conn = sqlite3.connect(DB_NAME)

    conn.executemany("""
        INSERT INTO voyage_segments (
            created_at,
            segment_no,
            distance_km,
            weather,
            wind_speed,
            wind_direction,
            wave_height,
            current_speed,
            current_direction,
            selected_fuel,
            selected_speed,
            fuel_consumption,
            co2,
            cost,
            alert
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, rows)

    conn.commit()
    conn.close()


def load_segment_history(limit=50):
    conn = sqlite3.connect(DB_NAME)

    df = pd.read_sql_query("""
        SELECT
            id AS ID,
            created_at AS "Date & Time",
            segment_no AS "Segment",
            distance_km AS "Distance (km)",
            weather AS Weather,
            wind_speed AS "Wind (knots)",
            wave_height AS "Wave (m)",
            current_speed AS "Current (knots)",
            selected_fuel AS "Fuel",
            selected_speed AS "Speed (knots)",
            fuel_consumption AS "Fuel (t)",
            co2 AS "CO₂ (t)",
            cost AS "Cost (₹)",
            alert AS Alert
        FROM voyage_segments
        ORDER BY id DESC
        LIMIT ?
    """, conn, params=(limit,))

    conn.close()
    return df


def clear_voyage_segment_history():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("DELETE FROM voyage_segments")
    conn.commit()
    conn.close()


init_database()


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Quantum Predictors | Green Fleet",
    page_icon="🚢",
    layout="wide"
)


# ============================================================
# CSS
# ============================================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #06141c, #09242a);
    color: white;
}

.main-title {
    font-size: 45px;
    font-weight: 800;
    color: #48e0a0;
    text-align: center;
}

.subtitle {
    text-align: center;
    color: #a8c1c8;
    font-size: 18px;
    margin-bottom: 30px;
}

.section-title {
    color: #48e0a0;
    font-size: 28px;
    font-weight: 700;
    margin-top: 30px;
}

.card {
    background: #0d252d;
    border: 1px solid #1d4a52;
    border-radius: 15px;
    padding: 20px;
    margin-bottom: 15px;
}

.metric-card {
    background: #0d252d;
    border: 1px solid #24545c;
    border-radius: 15px;
    padding: 20px;
    text-align: center;
}

.metric-title {
    color: #8ba9b1;
    font-size: 14px;
}

.metric-value {
    color: #48e0a0;
    font-size: 30px;
    font-weight: 800;
}

.small-text {
    color: #8ba9b1;
    font-size: 13px;
}

.success-box {
    background: #0b3028;
    border: 1px solid #32c98b;
    border-radius: 15px;
    padding: 25px;
}

.warning-box {
    background: #302a0b;
    border: 1px solid #d8b84d;
    border-radius: 15px;
    padding: 18px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# FUEL DATA
# ============================================================

fuel_data = {

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
# FUEL COLORS FOR 3D GRAPHS
# ============================================================

FUEL_COLORS = {

    "Diesel": "#4B5563",

    "Petrol": "#22C55E",

    "LNG": "#3B82F6",

    "Methanol": "#F97316",

    "Hydrogen": "#A855F7",

    "Ammonia": "#FACC15"

}


weather_factor_map = {

    "Calm Sea": 0.92,
    "Normal": 1.00,
    "Moderate": 1.08,
    "Heavy Weather": 1.18,
    "Storm": 1.32

}


# ============================================================
# 3D GRAPH FUNCTION
# ============================================================

def create_3d_bar_chart(
    fuels,
    values,
    title,
    ylabel
):

    fig = plt.figure(
        figsize=(10, 5.8)
    )

    ax = fig.add_subplot(
        111,
        projection="3d"
    )

    values = np.array(
        values,
        dtype=float
    )

    total = float(
        np.sum(values)
    )

    if total > 0:

        percentages = (
            values / total
        ) * 100

    else:

        percentages = np.zeros(
            len(values)
        )

    x = np.arange(
        len(fuels)
    )

    y = np.zeros(
        len(fuels)
    )

    z = np.zeros(
        len(fuels)
    )

    dx = np.full(
        len(fuels),
        0.65
    )

    dy = np.full(
        len(fuels),
        0.65
    )

    dz = values

    colors = [

        FUEL_COLORS.get(
            fuel,
            "#48e0a0"
        )

        for fuel in fuels

    ]

    ax.bar3d(

        x,
        y,
        z,

        dx,
        dy,
        dz,

        color=colors,

        edgecolor="white",

        linewidth=0.8,

        shade=True,

        alpha=0.95

    )

    max_value = (

        float(np.max(values))
        if len(values) > 0
        else 1.0

    )

    if max_value <= 0:
        max_value = 1.0

    for i, (
        fuel,
        value,
        percentage
    ) in enumerate(

        zip(
            fuels,
            values,
            percentages
        )

    ):

        # Percentage above each bar

        ax.text(

            i + 0.325,

            0.325,

            value
            + max_value * 0.10,

            f"{percentage:.1f}%",

            ha="center",

            va="bottom",

            fontsize=11,

            fontweight="bold",

            color="black"

        )

        # Actual value above bar

        ax.text(

            i + 0.325,

            0.325,

            value
            + max_value * 0.035,

            f"{value:.2f} t",

            ha="center",

            va="bottom",

            fontsize=8,

            color="black"

        )

    ax.set_xticks(
        x + 0.325
    )

    ax.set_xticklabels(

        fuels,

        rotation=20,

        ha="right",

        fontsize=9

    )

    ax.set_yticks([])

    ax.set_zlabel(
        ylabel,
        fontsize=10
    )

    ax.set_title(

        title,

        fontsize=15,

        fontweight="bold",

        pad=20

    )

    ax.set_zlim(

        0,

        max_value * 1.28

    )

    ax.view_init(

        elev=22,

        azim=-60

    )

    ax.set_box_aspect(

        (
            max(len(fuels), 4),
            1.2,
            4
        )

    )

    ax.grid(
        True,
        alpha=0.2
    )

    ax.xaxis.pane.set_alpha(
        0.08
    )

    ax.yaxis.pane.set_alpha(
        0.05
    )

    ax.zaxis.pane.set_alpha(
        0.05
    )

    fig.tight_layout()

    return fig


# ============================================================
# MODEL FUNCTIONS
# ============================================================

def base_fuel(
    capacity,
    speed,
    distance,
    fuel
):

    base = (
        (capacity / 10000)
        * (distance / 1000)
        * 2.0
    )

    speed_factor = (
        speed / 18
    ) ** 2.3

    return (
        base
        * speed_factor
        * fuel_data[fuel]["consumption_factor"]
    )


def environmental_factor(
    weather,
    wind_speed,
    wave_height,
    current_speed
):

    wf = weather_factor_map.get(
        weather,
        1.0
    )

    wind_effect = (
        1
        + max(0, wind_speed - 8)
        * 0.012
    )

    wave_effect = (
        1
        + max(0, wave_height - 1)
        * 0.075
    )

    current_effect = (
        1
        + max(0, current_speed - 0.5)
        * 0.06
    )

    return (
        wf
        * wind_effect
        * wave_effect
        * current_effect
    )


def predict_fuel(
    capacity,
    speed,
    distance,
    fuel,
    weather="Normal",
    wind_speed=8,
    wave_height=1,
    current_speed=0.5
):

    return (
        base_fuel(
            capacity,
            speed,
            distance,
            fuel
        )
        * environmental_factor(
            weather,
            wind_speed,
            wave_height,
            current_speed
        )
    )


def calculate_co2(
    fuel_amount,
    fuel
):

    return (
        fuel_amount
        * fuel_data[fuel]["co2_factor"]
    )


def haversine_km(
    lat1,
    lon1,
    lat2,
    lon2
):

    r = 6371.0

    p1 = math.radians(lat1)
    p2 = math.radians(lat2)

    dp = math.radians(
        lat2 - lat1
    )

    dl = math.radians(
        lon2 - lon1
    )

    a = (
        math.sin(dp / 2) ** 2
        +
        math.cos(p1)
        * math.cos(p2)
        * math.sin(dl / 2) ** 2
    )

    return (
        2
        * r
        * math.asin(
            math.sqrt(a)
        )
    )


def interpolate_position(
    lat1,
    lon1,
    lat2,
    lon2,
    progress
):

    return (

        lat1
        + (lat2 - lat1)
        * progress,

        lon1
        + (lon2 - lon1)
        * progress

    )


def generate_segment_conditions(
    n,
    mode="Dynamic Simulation",
    seed=42
):

    rng = np.random.default_rng(
        seed
    )

    rows = []

    weather_choices = [

        "Calm Sea",
        "Normal",
        "Moderate",
        "Heavy Weather"

    ]

    probs = [

        0.20,
        0.45,
        0.25,
        0.10

    ]

    for i in range(n):

        weather = rng.choice(

            weather_choices,

            p=probs

        )

        wind = float(

            np.clip(

                rng.normal(

                    12
                    if weather != "Calm Sea"
                    else 6,

                    3

                ),

                2,
                30

            )

        )

        wave = float(

            np.clip(

                rng.normal(

                    1.7

                    if weather
                    in [
                        "Moderate",
                        "Heavy Weather"
                    ]

                    else 0.9,

                    0.5

                ),

                0.2,
                5.5

            )

        )

        current = float(

            np.clip(

                rng.normal(

                    1.1,
                    0.4

                ),

                0.1,
                3.0

            )

        )

        wind_dir = float(

            rng.integers(
                0,
                360
            )

        )

        current_dir = float(

            rng.integers(
                0,
                360
            )

        )

        rows.append({

            "segment": i + 1,

            "weather": weather,

            "wind_speed": wind,

            "wind_direction": wind_dir,

            "wave_height": wave,

            "current_speed": current,

            "current_direction":
                current_dir

        })

    return rows


def alert_level(
    weather,
    wind,
    wave
):

    if (

        weather == "Storm"

        or wind >= 25

        or wave >= 4.5

    ):

        return "🔴 Severe"

    if (

        weather == "Heavy Weather"

        or wind >= 18

        or wave >= 3

    ):

        return "🟠 Caution"

    return "🟢 Normal"


def optimize_single_segment(
    capacity,
    distance,
    requested_speed,
    cargo,
    available_fuels,
    weather,
    wind,
    wave,
    current
):

    raw_speeds = [

        requested_speed - 2,
        requested_speed - 1,
        requested_speed,
        requested_speed + 1,
        requested_speed + 2

    ]

    candidate_speeds = sorted(

        set(

            round(

                float(

                    np.clip(
                        s,
                        8,
                        25
                    )

                ),

                1

            )

            for s in raw_speeds

        )

    )

    best = None

    best_score = float(
        "inf"
    )

    for fuel in available_fuels:

        for candidate_speed in candidate_speeds:

            consumption = predict_fuel(

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

                consumption
                * fuel_data[fuel]["cost"]

            )

            co2 = calculate_co2(

                consumption,
                fuel

            )

            cargo_penalty = 0

            if cargo > capacity:

                cargo_penalty = (

                    1_000_000

                    + (

                        cargo - capacity

                    ) * 1000

                )

            score = (

                cost * 0.55

                + co2 * 12000 * 0.35

                + abs(
                    candidate_speed - 17
                )
                * cost
                * 0.03

                + cargo_penalty

            )

            if score < best_score:

                best_score = score

                best = {

                    "fuel": fuel,

                    "speed":
                        candidate_speed,

                    "fuel_consumption":
                        consumption,

                    "cost":
                        cost,

                    "co2":
                        co2,

                    "score":
                        score

                }

    return best


# ============================================================
# HEADER
# ============================================================

st.markdown(

    '<div class="main-title">'
    '⚛️ Quantum Predictors'
    '</div>',

    unsafe_allow_html=True

)

st.markdown(

    '<div class="subtitle">'
    'Quantum-Inspired Fuel Consumption Prediction '
    '& Green Fleet Optimization'
    '<br>'
    'Dynamic Voyage Monitoring • Engineering Day Prototype'
    '</div>',

    unsafe_allow_html=True

)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title(
    "⚙️ Fleet Configuration"
)

vessel_type = st.sidebar.selectbox(

    "Vessel Type",

    [
        "Container Ship",
        "Bulk Carrier",
        "Tanker",
        "Cargo Ship"
    ]

)

capacity = st.sidebar.number_input(

    "Vessel Capacity (tonnes)",

    min_value=1000,

    max_value=200000,

    value=50000,

    step=1000

)

speed = st.sidebar.number_input(

    "Current / Planned Speed (knots)",

    min_value=5.0,

    max_value=30.0,

    value=18.0,

    step=0.5

)

distance = st.sidebar.number_input(

    "Total Voyage Distance (km)",

    min_value=100,

    max_value=50000,

    value=2500,

    step=100

)

cargo = st.sidebar.number_input(

    "Cargo Demand (tonnes)",

    min_value=100,

    max_value=200000,

    value=40000,

    step=1000

)

fuel_type = st.sidebar.selectbox(

    "Current Fuel",

    list(fuel_data.keys())

)

available_fuels = st.sidebar.multiselect(

    "Available Fuels for This Vessel",

    list(fuel_data.keys()),

    default=[

        "Diesel",
        "LNG",
        "Methanol",
        "Hydrogen",
        "Ammonia"

    ]

)

if not available_fuels:

    st.sidebar.error(
        "Select at least one available fuel."
    )

    available_fuels = [
        fuel_type
    ]

fuel_price = st.sidebar.number_input(

    "Current Fuel Price (₹ / tonne)",

    min_value=1000,

    max_value=200000,

    value=65000,

    step=1000

)

weather = st.sidebar.selectbox(

    "Current Operating Condition",

    [
        "Normal",
        "Calm Sea",
        "Moderate",
        "Heavy Weather",
        "Storm"
    ]

)

wind_speed_now = st.sidebar.number_input(

    "Current Wind Speed (knots)",

    0.0,
    40.0,
    10.0,
    1.0

)

wave_height_now = st.sidebar.number_input(

    "Current Wave Height (m)",

    0.1,
    8.0,
    1.2,
    0.1

)

current_speed_now = st.sidebar.number_input(

    "Current Speed (knots)",

    0.0,
    5.0,
    0.6,
    0.1

)

predict_button = st.sidebar.button(

    "🚀 Predict & Optimize",

    use_container_width=True

)


# ============================================================
# TOP DASHBOARD
# ============================================================

initial_fuel = predict_fuel(

    capacity,
    speed,
    distance,
    fuel_type,
    weather,
    wind_speed_now,
    wave_height_now,
    current_speed_now

)

initial_cost = (

    initial_fuel
    * fuel_price

)

initial_co2 = calculate_co2(

    initial_fuel,
    fuel_type

)

green_score = (

    fuel_data[fuel_type]["green_score"]

)

st.markdown(

    '<div class="section-title">'
    '📊 Fleet Prediction Dashboard'
    '</div>',

    unsafe_allow_html=True

)

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.markdown(

        f"""
        <div class="metric-card">
        <div class="metric-title">
        Predicted Fuel
        </div>
        <div class="metric-value">
        {initial_fuel:.2f}
        </div>
        <div class="small-text">
        tonnes
        </div>
        </div>
        """,

        unsafe_allow_html=True

    )

with col2:

    st.markdown(

        f"""
        <div class="metric-card">
        <div class="metric-title">
        Estimated Cost
        </div>
        <div class="metric-value">
        ₹{initial_cost/100000:.2f}L
        </div>
        <div class="small-text">
        current-fuel estimate
        </div>
        </div>
        """,

        unsafe_allow_html=True

    )

with col3:

    st.markdown(

        f"""
        <div class="metric-card">
        <div class="metric-title">
        CO₂ Emission
        </div>
        <div class="metric-value">
        {initial_co2:.2f}
        </div>
        <div class="small-text">
        tonnes
        </div>
        </div>
        """,

        unsafe_allow_html=True

    )

with col4:

    st.markdown(

        f"""
        <div class="metric-card">
        <div class="metric-title">
        Green Score
        </div>
        <div class="metric-value">
        {green_score}
        </div>
        <div class="small-text">
        out of 100
        </div>
        </div>
        """,

        unsafe_allow_html=True

    )


# ============================================================
# CURRENT CONDITIONS
# ============================================================

st.markdown(

    '<div class="section-title">'
    '🌊 Current Vessel Conditions'
    '</div>',

    unsafe_allow_html=True

)

cc1, cc2, cc3, cc4, cc5 = st.columns(5)

cc1.metric(
    "Weather",
    weather
)

cc2.metric(
    "Wind",
    f"{wind_speed_now:.1f} kn"
)

cc3.metric(
    "Waves",
    f"{wave_height_now:.1f} m"
)

cc4.metric(
    "Current",
    f"{current_speed_now:.1f} kn"
)

cc5.metric(

    "Alert",

    alert_level(

        weather,
        wind_speed_now,
        wave_height_now

    )

)


# ============================================================
# PREDICTION SUMMARY
# ============================================================

st.markdown(

    '<div class="section-title">'
    '🤖 Fuel Prediction'
    '</div>',

    unsafe_allow_html=True

)

st.markdown(

    f"""
    <div class="card">

    <b>Vessel:</b>
    {vessel_type}
    <br>

    <b>Capacity:</b>
    {capacity:,} tonnes
    <br>

    <b>Cargo Demand:</b>
    {cargo:,} tonnes
    <br>

    <b>Distance:</b>
    {distance:,} km
    <br>

    <b>Current Fuel:</b>
    {fuel_type}
    <br>

    <b>Available Fuels:</b>
    {', '.join(available_fuels)}
    <br>

    <b>Speed:</b>
    {speed:.1f} knots
    <br>

    <b>Environment:</b>
    {weather},
    wind {wind_speed_now:.1f} kn,
    waves {wave_height_now:.1f} m,
    current {current_speed_now:.1f} kn

    </div>
    """,

    unsafe_allow_html=True

)


# ============================================================
# STATIC FUEL COMPARISON
# ============================================================

st.markdown(

    '<div class="section-title">'
    '🌍 Green Fuel Comparison'
    '</div>',

    unsafe_allow_html=True

)

fuel_df = pd.DataFrame([

    {

        "Fuel": f,

        "Available":
            "Yes"
            if f in available_fuels
            else "No",

        "CO₂ Factor":
            fuel_data[f]["co2_factor"],

        "Approx. Price ₹/tonne":
            fuel_data[f]["cost"],

        "Green Score":
            fuel_data[f]["green_score"]

    }

    for f in fuel_data

])

st.dataframe(

    fuel_df,

    use_container_width=True,

    hide_index=True

)


# ============================================================
# OPTIMIZATION
# ============================================================

if predict_button:

    if cargo > capacity:

        st.error(

            "Cargo demand is greater than vessel capacity. "
            "Please correct the input."

        )

    else:

        with st.spinner(

            "⚛️ Comparing fuel + speed combinations..."

        ):

            best_solution = optimize_single_segment(

                capacity,
                distance,
                speed,
                cargo,
                available_fuels,
                weather,
                wind_speed_now,
                wave_height_now,
                current_speed_now

            )

        optimized_fuel = (
            best_solution["fuel_consumption"]
        )

        optimized_cost = (
            best_solution["cost"]
        )

        optimized_co2 = (
            best_solution["co2"]
        )

        fuel_saving = (

            (
                initial_fuel
                - optimized_fuel
            )
            / initial_fuel

        ) * 100 if initial_fuel else 0

        cost_saving = (

            (
                initial_cost
                - optimized_cost
            )
            / initial_cost

        ) * 100 if initial_cost else 0

        co2_reduction = (

            (
                initial_co2
                - optimized_co2
            )
            / initial_co2

        ) * 100 if initial_co2 else 0

        save_prediction(

            vessel_type,
            capacity,
            speed,
            distance,
            cargo,
            fuel_type,
            fuel_price,
            weather,
            initial_fuel,
            initial_cost,
            initial_co2,
            best_solution,
            fuel_saving,
            cost_saving,
            co2_reduction

        )

        st.markdown(

            '<div class="section-title">'
            '⚛️ Quantum-Inspired Optimization Result'
            '</div>',

            unsafe_allow_html=True

        )

        st.markdown(

            f"""
            <div class="success-box">

            <h2>
            🚢 Recommended Green Fleet Plan
            </h2>

            <h3>
            Recommended Fuel:
            {best_solution['fuel']}
            </h3>

            <p>
            Recommended Operating Speed:
            <b>
            {best_solution['speed']:.1f} knots
            </b>
            </p>

            <p>
            Predicted Fuel Consumption:
            <b>
            {optimized_fuel:.2f} tonnes
            </b>
            </p>

            <p>
            Estimated Fuel Cost:
            <b>
            ₹{optimized_cost:,.0f}
            </b>
            </p>

            <p>
            Estimated CO₂ Emissions:
            <b>
            {optimized_co2:.2f} tonnes
            </b>
            </p>

            <p>
            Available-fuel constraint:
            <b>
            {', '.join(available_fuels)}
            </b>
            </p>

            </div>
            """,

            unsafe_allow_html=True

        )

        s1, s2, s3 = st.columns(3)

        s1.metric(
            "Fuel Saving",
            f"{fuel_saving:.2f}%"
        )

        s2.metric(
            "Cost Saving",
            f"{cost_saving:.2f}%"
        )

        s3.metric(
            "CO₂ Reduction",
            f"{co2_reduction:.2f}%"
        )

        comparison = pd.DataFrame({

            "Metric": [

                "Fuel Consumption (t)",
                "Fuel Cost (₹)",
                "CO₂ Emissions (t)"

            ],

            "Current Plan": [

                initial_fuel,
                initial_cost,
                initial_co2

            ],

            "Optimized Plan": [

                optimized_fuel,
                optimized_cost,
                optimized_co2

            ]

        })

        st.dataframe(

            comparison,

            use_container_width=True,

            hide_index=True

        )


        # ====================================================
        # CALCULATE GRAPH DATA
        # ====================================================

        chart_fuels = list(
            available_fuels
        )

        values = [

            predict_fuel(

                capacity,

                best_solution["speed"],

                distance,

                fuel,

                weather,

                wind_speed_now,

                wave_height_now,

                current_speed_now

            )

            for fuel in chart_fuels

        ]

        emissions = [

            calculate_co2(

                value,

                fuel

            )

            for fuel, value in zip(

                chart_fuels,
                values

            )

        ]


        # ====================================================
        # GRAPHS ON RIGHT SIDE
        # ====================================================

        graph_left, graph_right = st.columns(

            [1, 1.7]

        )


        # ----------------------------------------------------
        # LEFT SIDE - DECISION
        # ----------------------------------------------------

        with graph_left:

            st.markdown(

                '<div class="section-title">'
                '💡 Decision Explanation'
                '</div>',

                unsafe_allow_html=True

            )

            st.markdown(

                f"""
                <div class="card">

                The optimizer compared only the fuels
                available to this vessel.

                <br><br>

                It tested several nearby operating speeds
                and evaluated fuel cost, CO₂ emissions
                and speed penalty.

                <br><br>

                <b>Selected Fuel:</b><br>
                {best_solution['fuel']}

                <br><br>

                <b>Selected Speed:</b><br>
                {best_solution['speed']:.1f} knots

                <br><br>

                <b>Fuel Consumption:</b><br>
                {optimized_fuel:.2f} tonnes

                <br><br>

                <b>CO₂:</b><br>
                {optimized_co2:.2f} tonnes

                <br><br>

                <b>Available Fuels:</b><br>
                {', '.join(chart_fuels)}

                <br><br>

                The percentage shown on the graph represents
                the fuel's share of the total consumption
                among the selected fuels.

                <br><br>

                <b>Note:</b>
                This is a quantum-inspired classical prototype,
                not a physical quantum computer.

                </div>
                """,

                unsafe_allow_html=True

            )


        # ----------------------------------------------------
        # RIGHT SIDE - FUEL GRAPH
        # ----------------------------------------------------

        with graph_right:

            st.markdown(

                '<div class="section-title">'
                '📈 3D Fuel Consumption Comparison'
                '</div>',

                unsafe_allow_html=True

            )

            fuel_fig = create_3d_bar_chart(

                chart_fuels,

                values,

                "Available Fuel Consumption",

                "Fuel (tonnes)"

            )

            st.pyplot(

                fuel_fig,

                use_container_width=True

            )

            plt.close(
                fuel_fig
            )


            # ------------------------------------------------
            # CO2 GRAPH
            # ------------------------------------------------

            st.markdown(

                '<div class="section-title">'
                '🌱 3D CO₂ Comparison'
                '</div>',

                unsafe_allow_html=True

            )

            co2_fig = create_3d_bar_chart(

                chart_fuels,

                emissions,

                "Available Fuel CO₂ Comparison",

                "CO₂ (tonnes)"

            )

            st.pyplot(

                co2_fig,

                use_container_width=True

            )

            plt.close(
                co2_fig
            )


# ============================================================
# DYNAMIC VOYAGE OPTIMIZATION
# ============================================================

st.markdown(

    '<div class="section-title">'
    '🧭 Dynamic Voyage Optimization'
    '</div>',

    unsafe_allow_html=True

)

st.markdown(

    """
    <div class="card">

    Weather is not assumed to remain constant for the whole trip.
    The voyage is divided into route segments.

    Each segment can have different wind, wave, current and weather
    conditions, and the optimizer can select a local fuel/speed plan.

    </div>
    """,

    unsafe_allow_html=True

)


# ============================================================
# WORLDWIDE ROUTE SELECTION
# ============================================================

st.markdown(
    "### 🌍 Worldwide Route Selection"
)

v1, v2, v3 = st.columns(3)


with v1:

    start_port = st.selectbox(

        "Start Port",

        PORT_NAMES,

        index=PORT_NAMES.index(
            "Chennai, India"
        ),

        key="start_port_select"

    )

    start_lat, start_lon = WORLD_PORTS[
        start_port
    ]

    st.caption(

        f"📍 {start_lat:.4f}, "
        f"{start_lon:.4f}"

    )


with v2:

    end_port = st.selectbox(

        "Destination Port",

        PORT_NAMES,

        index=PORT_NAMES.index(
            "Mumbai, India"
        ),

        key="destination_port_select"

    )

    end_lat, end_lon = WORLD_PORTS[
        end_port
    ]

    st.caption(

        f"📍 {end_lat:.4f}, "
        f"{end_lon:.4f}"

    )


with v3:

    segments = st.number_input(

        "Number of Voyage Segments",

        2,
        30,
        6,
        1

    )

    segment_mode = st.selectbox(

        "Condition Mode",

        [
            "Dynamic Simulation",
            "Manual Conditions"
        ]

    )

    route_seed = st.number_input(

        "Simulation Seed",

        1,
        99999,
        42,
        1

    )


# ============================================================
# ROUTE DISTANCE
# ============================================================

route_distance = haversine_km(

    start_lat,
    start_lon,
    end_lat,
    end_lon

)

segment_distance = (

    route_distance
    / segments

)

st.info(

    f"🛳️ Estimated route distance: "
    f"{route_distance:,.0f} km • "
    f"{segments} segments • "
    f"about {segment_distance:,.0f} km per segment"

)


# ============================================================
# MANUAL CONDITIONS
# ============================================================

manual_conditions = []

if segment_mode == "Manual Conditions":

    st.write(
        "Enter conditions for each segment:"
    )

    for i in range(
        int(segments)
    ):

        a, b, c, d = st.columns(4)

        with a:

            mw = st.selectbox(

                f"S{i+1} Weather",

                [
                    "Calm Sea",
                    "Normal",
                    "Moderate",
                    "Heavy Weather",
                    "Storm"
                ],

                key=f"mw_{i}"

            )

        with b:

            mwind = st.number_input(

                f"S{i+1} Wind (kn)",

                0.0,
                40.0,
                10.0,
                1.0,

                key=f"mwind_{i}"

            )

        with c:

            mwave = st.number_input(

                f"S{i+1} Wave (m)",

                0.1,
                8.0,
                1.2,
                0.1,

                key=f"mwave_{i}"

            )

        with d:

            mcurrent = st.number_input(

                f"S{i+1} Current (kn)",

                0.0,
                5.0,
                0.6,
                0.1,

                key=f"mcur_{i}"

            )

        manual_conditions.append({

            "segment": i + 1,

            "weather": mw,

            "wind_speed": mwind,

            "wind_direction": 0.0,

            "wave_height": mwave,

            "current_speed": mcurrent,

            "current_direction": 0.0

        })


# ============================================================
# RUN VOYAGE
# ============================================================

run_voyage = st.button(

    "🧭 Run Dynamic Voyage Optimization",

    use_container_width=True

)


if run_voyage:

    conditions = (

        manual_conditions

        if segment_mode
        == "Manual Conditions"

        else generate_segment_conditions(

            int(segments),

            seed=int(route_seed)

        )

    )

    voyage_rows = []

    total_fuel = 0.0

    total_cost = 0.0

    total_co2 = 0.0

    total_hours = 0.0

    segment_display = []

    for cond in conditions:

        best = optimize_single_segment(

            capacity,

            segment_distance,

            speed,

            cargo,

            available_fuels,

            cond["weather"],

            cond["wind_speed"],

            cond["wave_height"],

            cond["current_speed"]

        )

        hours = (

            segment_distance
            / (
                best["speed"]
                * 1.852
            )

        )

        total_hours += hours

        total_fuel += (
            best["fuel_consumption"]
        )

        total_cost += (
            best["cost"]
        )

        total_co2 += (
            best["co2"]
        )

        alert = alert_level(

            cond["weather"],
            cond["wind_speed"],
            cond["wave_height"]

        )

        segment_display.append({

            "Segment":
                cond["segment"],

            "Distance (km)":
                round(
                    segment_distance,
                    1
                ),

            "Weather":
                cond["weather"],

            "Wind (kn)":
                round(
                    cond["wind_speed"],
                    1
                ),

            "Wave (m)":
                round(
                    cond["wave_height"],
                    1
                ),

            "Current (kn)":
                round(
                    cond["current_speed"],
                    1
                ),

            "Best Fuel":
                best["fuel"],

            "Best Speed":
                round(
                    best["speed"],
                    1
                ),

            "Fuel (t)":
                round(
                    best["fuel_consumption"],
                    2
                ),

            "CO₂ (t)":
                round(
                    best["co2"],
                    2
                ),

            "Cost (₹)":
                round(
                    best["cost"],
                    0
                ),

            "Alert":
                alert

        })

        voyage_rows.append((

            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

            int(
                cond["segment"]
            ),

            segment_distance,

            cond["weather"],

            cond["wind_speed"],

            cond["wind_direction"],

            cond["wave_height"],

            cond["current_speed"],

            cond["current_direction"],

            best["fuel"],

            best["speed"],

            best["fuel_consumption"],

            best["co2"],

            best["cost"],

            alert

        ))

    save_voyage_segments(
        voyage_rows
    )

    st.session_state[
        "voyage_conditions"
    ] = conditions

    st.session_state[
        "voyage_segments_df"
    ] = pd.DataFrame(
        segment_display
    )

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

        start_port,
        end_port,

        start_lat,
        start_lon,

        end_lat,
        end_lon

    )

    st.session_state[
        "voyage_done"
    ] = True

    st.session_state[
        "track_step"
    ] = 0


# ============================================================
# VOYAGE RESULTS
# ============================================================

if st.session_state.get(
    "voyage_done",
    False
):

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

    voyage_df = st.session_state[
        "voyage_segments_df"
    ]

    st.markdown(

        '<div class="section-title">'
        '📋 Segment-by-Segment Voyage Plan'
        '</div>',

        unsafe_allow_html=True

    )

    st.dataframe(

        voyage_df,

        use_container_width=True,

        hide_index=True

    )

    t1, t2, t3, t4 = st.columns(4)

    t1.metric(
        "Total Fuel",
        f"{total_fuel:.2f} t"
    )

    t2.metric(
        "Total Cost",
        f"₹{total_cost/100000:.2f} L"
    )

    t3.metric(
        "Total CO₂",
        f"{total_co2:.2f} t"
    )

    t4.metric(
        "Estimated ETA",
        f"{total_hours:.1f} h"
    )

    st.markdown(

        '<div class="section-title">'
        '🌦️ Changing Weather Across Voyage'
        '</div>',

        unsafe_allow_html=True

    )

    fig3, ax3 = plt.subplots(
        figsize=(10, 4)
    )

    ax3.plot(

        voyage_df["Segment"],

        voyage_df["Wave (m)"],

        marker="o",

        label="Wave height"

    )

    ax3.plot(

        voyage_df["Segment"],

        voyage_df["Wind (kn)"],

        marker="o",

        label="Wind speed"

    )

    ax3.set_xlabel(
        "Voyage Segment"
    )

    ax3.set_ylabel(
        "Condition value"
    )

    ax3.set_title(
        "Dynamic Environmental Conditions"
    )

    ax3.legend()

    st.pyplot(fig3)

    plt.close(fig3)


# ============================================================
# LIVE VOYAGE MONITORING
# ============================================================

st.markdown(

    '<div class="section-title">'
    '📡 Live Voyage Monitoring'
    '</div>',

    unsafe_allow_html=True

)

st.markdown(

    """
    <div class="card">

    <b>Demo mode:</b>
    the dashboard simulates an onboard GPS/AIS-style feed.

    Each update moves the vessel along the selected route
    and changes the monitored environmental conditions.

    A real deployment would replace this simulated feed
    with actual GPS/AIS, ship telemetry or approved
    weather-data sources.

    </div>
    """,

    unsafe_allow_html=True

)


if "track_step" not in st.session_state:

    st.session_state[
        "track_step"
    ] = 0


track_col1, track_col2, track_col3 = st.columns(3)


with track_col1:

    if st.button(

        "▶️ Next Live Update",

        use_container_width=True

    ):

        st.session_state[
            "track_step"
        ] = min(

            st.session_state[
                "track_step"
            ] + 1,

            int(segments)

        )


with track_col2:

    if st.button(

        "🔄 Reset Tracking",

        use_container_width=True

    ):

        st.session_state[
            "track_step"
        ] = 0


with track_col3:

    st.session_state[
        "track_step"
    ] = st.number_input(

        "Tracking Segment",

        0,

        int(segments),

        int(

            st.session_state[
                "track_step"
            ]

        ),

        1

    )


step = int(

    st.session_state[
        "track_step"
    ]

)

progress = (

    step
    / max(
        1,
        int(segments)
    )

)


cur_lat, cur_lon = interpolate_position(

    start_lat,
    start_lon,

    end_lat,
    end_lon,

    progress

)


if st.session_state.get(
    "voyage_done",
    False
):

    conditions = st.session_state[
        "voyage_conditions"
    ]

else:

    conditions = generate_segment_conditions(

        int(segments),

        seed=int(route_seed)

    )


active_index = min(

    max(
        step - 1,
        0
    ),

    len(conditions) - 1

)

active = conditions[
    active_index
]


if step == 0:

    active_weather = weather

    active_wind = wind_speed_now

    active_wave = wave_height_now

    active_current = current_speed_now

    active_fuel = fuel_type

    active_speed = speed

else:

    active_weather = active[
        "weather"
    ]

    active_wind = active[
        "wind_speed"
    ]

    active_wave = active[
        "wave_height"
    ]

    active_current = active[
        "current_speed"
    ]

    live_best = optimize_single_segment(

        capacity,

        segment_distance,

        speed,

        cargo,

        available_fuels,

        active_weather,

        active_wind,

        active_wave,

        active_current

    )

    active_fuel = live_best[
        "fuel"
    ]

    active_speed = live_best[
        "speed"
    ]


live_fuel_rate = predict_fuel(

    capacity,

    active_speed,

    max(
        segment_distance,
        1
    ),

    active_fuel,

    active_weather,

    active_wind,

    active_wave,

    active_current

)


live_co2 = calculate_co2(

    live_fuel_rate,

    active_fuel

)


live_alert = alert_level(

    active_weather,

    active_wind,

    active_wave

)


lm1, lm2, lm3, lm4, lm5, lm6 = st.columns(6)

lm1.metric(

    "GPS Latitude",

    f"{cur_lat:.4f}°"

)

lm2.metric(

    "GPS Longitude",

    f"{cur_lon:.4f}°"

)

lm3.metric(

    "Progress",

    f"{progress*100:.1f}%"

)

lm4.metric(

    "Live Speed",

    f"{active_speed:.1f} kn"

)

lm5.metric(

    "Live Fuel",

    active_fuel

)

lm6.metric(

    "Alert",

    live_alert

)


lm7, lm8, lm9, lm10 = st.columns(4)

lm7.metric(

    "Weather",

    active_weather

)

lm8.metric(

    "Wind",

    f"{active_wind:.1f} kn"

)

lm9.metric(

    "Wave",

    f"{active_wave:.1f} m"

)

lm10.metric(

    "Current",

    f"{active_current:.1f} kn"

)


st.markdown(

    f"""
    <div class="card">

    <b>Route:</b>
    {start_port} → {end_port}

    <br>

    <b>Live position:</b>
    {cur_lat:.4f}, {cur_lon:.4f}

    <br>

    <b>Active segment:</b>
    {max(step, 1)} / {segments}

    <br>

    <b>Current environmental condition:</b>
    {active_weather}

    <br>

    <b>Predicted fuel for active segment:</b>
    {live_fuel_rate:.2f} tonnes

    <br>

    <b>Estimated CO₂ for active segment:</b>
    {live_co2:.2f} tonnes

    <br>

    <b>Decision:</b>
    The system can recalculate the recommended fuel
    and speed when monitored conditions change.

    </div>
    """,

    unsafe_allow_html=True

)


# ============================================================
# INTERACTIVE WORLDWIDE VOYAGE MAP
# ============================================================

st.markdown(

    '<div class="section-title">'
    '🗺️ Live Worldwide Voyage Map'
    '</div>',

    unsafe_allow_html=True

)


route_points = pd.DataFrame({

    "latitude": np.linspace(

        start_lat,
        end_lat,
        50

    ),

    "longitude": np.linspace(

        start_lon,
        end_lon,
        50

    )

})


map_data = pd.DataFrame({

    "latitude": [

        start_lat,
        cur_lat,
        end_lat

    ],

    "longitude": [

        start_lon,
        cur_lon,
        end_lon

    ]

})


try:

    import pydeck as pdk

    route_layer = pdk.Layer(

        "PathLayer",

        data=[{

            "path":

                route_points[
                    [
                        "longitude",
                        "latitude"
                    ]
                ].values.tolist()

        }],

        get_path="path",

        get_width=5,

        get_color=[

            72,
            224,
            160

        ],

        pickable=False

    )


    point_layer = pdk.Layer(

        "ScatterplotLayer",

        data=map_data,

        get_position=[

            "longitude",
            "latitude"

        ],

        get_radius=70000,

        get_fill_color=[

            255,
            80,
            80

        ],

        pickable=True

    )


    view_state = pdk.ViewState(

        latitude=(

            start_lat
            + end_lat

        ) / 2,

        longitude=(

            start_lon
            + end_lon

        ) / 2,

        zoom=2.5

    )


    deck = pdk.Deck(

        layers=[

            route_layer,
            point_layer

        ],

        initial_view_state=view_state,

        tooltip={

            "text":
            "Latitude: {latitude}\n"
            "Longitude: {longitude}"

        }

    )


    st.pydeck_chart(

        deck,

        use_container_width=True

    )

except Exception:

    st.map(

        map_data,

        latitude="latitude",

        longitude="longitude",

        zoom=2,

        use_container_width=True

    )


st.markdown(

    f"""
    <div class="card">

    <b>🟢 Start Port:</b>
    {start_port}
    ({start_lat:.4f}, {start_lon:.4f})

    <br><br>

    <b>🚢 Current Vessel:</b>
    ({cur_lat:.4f}, {cur_lon:.4f})

    <br><br>

    <b>🔴 Destination:</b>
    {end_port}
    ({end_lat:.4f}, {end_lon:.4f})

    <br><br>

    <b>🌍 Route Distance:</b>
    {route_distance:,.0f} km

    </div>
    """,

    unsafe_allow_html=True

)


# ============================================================
# ALERTS
# ============================================================

if live_alert == "🔴 Severe":

    st.error(

        "⚠️ Severe conditions detected. "
        "In a real deployment, an approved navigation/"
        "weather system should be consulted and operating "
        "decisions should be made by qualified personnel."

    )

elif live_alert == "🟠 Caution":

    st.warning(

        "⚠️ Caution: environmental resistance is elevated. "
        "The optimizer can recalculate the local "
        "fuel/speed plan."

    )

else:

    st.success(

        "✅ Conditions are within the prototype's "
        "normal monitoring range."

    )


# ============================================================
# SYSTEM FLOW
# ============================================================

st.markdown(

    '<div class="section-title">'
    '🔬 How the Integrated System Works'
    '</div>',

    unsafe_allow_html=True

)

c1, c2, c3 = st.columns(3)


with c1:

    st.markdown(

        """
        <div class="card">

        <h3>01 🤖 Prediction</h3>

        Vessel capacity, speed, distance, fuel and
        environmental conditions are used to estimate
        fuel consumption.

        </div>
        """,

        unsafe_allow_html=True

    )


with c2:

    st.markdown(

        """
        <div class="card">

        <h3>02 ⚛️ Optimization</h3>

        The prototype searches feasible fuel + speed
        combinations and minimizes a combined
        cost/emission/speed objective.

        </div>
        """,

        unsafe_allow_html=True

    )


with c3:

    st.markdown(

        """
        <div class="card">

        <h3>03 📡 Live Monitoring</h3>

        GPS position and changing weather conditions
        are monitored. When conditions change,
        the local plan can be recalculated.

        </div>
        """,

        unsafe_allow_html=True

    )


# ============================================================
# DATABASE HISTORY - PREDICTIONS
# ============================================================

st.markdown(

    '<div class="section-title">'
    '🗄️ Prediction History'
    '</div>',

    unsafe_allow_html=True

)

history_df = load_prediction_history()


if not history_df.empty:

    hc1, hc2 = st.columns(
        [5, 1]
    )

    with hc2:

        if st.button(

            "🗑️ Clear History",

            use_container_width=True,

            key="clear_prediction_history"

        ):

            clear_prediction_history()

            st.rerun()

    st.dataframe(

        history_df,

        use_container_width=True,

        hide_index=True

    )

else:

    st.info(

        "No prediction history yet. "
        "Click Predict & Optimize to save a result."

    )


# ============================================================
# VOYAGE SEGMENT HISTORY
# ============================================================

st.markdown(

    '<div class="section-title">'
    '🧭 Voyage Segment History'
    '</div>',

    unsafe_allow_html=True

)

segment_history = load_segment_history()


if not segment_history.empty:

    sh1, sh2 = st.columns(
        [5, 1]
    )

    with sh2:

        if st.button(

            "🗑️ Clear Voyage History",

            use_container_width=True,

            key="clear_voyage_history"

        ):

            clear_voyage_segment_history()

            st.session_state[
                "voyage_done"
            ] = False

            if "voyage_segments_df" in st.session_state:

                del st.session_state[
                    "voyage_segments_df"
                ]

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
