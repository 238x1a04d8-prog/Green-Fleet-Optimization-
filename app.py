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

def _ensure_column(cur, table_name, column_name, column_type):
    """Add a column only when it does not already exist."""
    existing = {
        row[1]
        for row in cur.execute(
            f"PRAGMA table_info({table_name})"
        ).fetchall()
    }

    if column_name not in existing:
        cur.execute(
            f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}"
        )


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

    # These columns are added only for NEW records. Existing history is
    # preserved exactly as it is and is never overwritten or recalculated.
    prediction_extra_columns = {
        "available_fuels_json": "TEXT",
        "wind_speed": "REAL",
        "wave_height": "REAL",
        "current_speed": "REAL",
        "chart_fuels_json": "TEXT",
        "chart_values_json": "TEXT",
        "chart_emissions_json": "TEXT",
    }

    for column_name, column_type in prediction_extra_columns.items():
        _ensure_column(
            cur,
            "predictions",
            column_name,
            column_type
        )

    # One saved voyage report represents one complete voyage run.
    # voyage_segments remains unchanged for the existing history table.
    cur.execute("""
        CREATE TABLE IF NOT EXISTS voyage_reports (
            report_id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            start_port TEXT,
            end_port TEXT,
            start_lat REAL,
            start_lon REAL,
            end_lat REAL,
            end_lon REAL,
            route_distance REAL,
            segments INTEGER,
            segment_mode TEXT,
            route_seed INTEGER,
            vessel_type TEXT,
            capacity REAL,
            speed REAL,
            cargo REAL,
            current_fuel TEXT,
            available_fuels_json TEXT,
            total_fuel REAL,
            total_cost REAL,
            total_co2 REAL,
            total_hours REAL,
            conditions_json TEXT,
            segment_display_json TEXT,
            sensor_timeline_json TEXT,
            fuel_plan_json TEXT
        )
    """)

    _ensure_column(cur, "voyage_reports", "sensor_timeline_json", "TEXT")
    _ensure_column(cur, "voyage_reports", "fuel_plan_json", "TEXT")

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
    co2_reduction,
    available_fuels=None,
    wind_speed=0.0,
    wave_height=0.0,
    current_speed=0.0
):
    """Save the prediction plus a complete snapshot for later reopening."""
    available_fuels = list(available_fuels or [fuel_type])

    # Save the exact graph data used by this run so an old report does not
    # change later if today's sidebar values or model code are different.
    chart_fuels = list(available_fuels)
    chart_values = [
        predict_fuel(
            capacity,
            best_solution["speed"],
            distance,
            fuel,
            weather,
            wind_speed,
            wave_height,
            current_speed
        )
        for fuel in chart_fuels
    ]
    chart_emissions = [
        calculate_co2(value, fuel)
        for fuel, value in zip(chart_fuels, chart_values)
    ]

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
            co2_reduction,
            available_fuels_json,
            wind_speed,
            wave_height,
            current_speed,
            chart_fuels_json,
            chart_values_json,
            chart_emissions_json
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
        co2_reduction,
        json.dumps(available_fuels),
        wind_speed,
        wave_height,
        current_speed,
        json.dumps(chart_fuels),
        json.dumps(chart_values),
        json.dumps(chart_emissions)
    ))

    conn.commit()
    conn.close()


def load_prediction_record(record_id):
    conn = sqlite3.connect(DB_NAME)
    row = pd.read_sql_query(
        "SELECT * FROM predictions WHERE id = ?",
        conn,
        params=(int(record_id),)
    )
    conn.close()
    return row.iloc[0].to_dict() if not row.empty else None

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



def save_voyage_report(
    created_at, start_port, end_port, start_lat, start_lon, end_lat, end_lon,
    route_distance, segments, segment_mode, route_seed, vessel_type, capacity,
    speed, cargo, current_fuel, available_fuels, total_fuel, total_cost,
    total_co2, total_hours, conditions, segment_display, sensor_timeline=None, fuel_plan=None
):
    conn = sqlite3.connect(DB_NAME)
    conn.execute("""
        INSERT INTO voyage_reports (
            created_at, start_port, end_port, start_lat, start_lon, end_lat, end_lon,
            route_distance, segments, segment_mode, route_seed, vessel_type, capacity,
            speed, cargo, current_fuel, available_fuels_json, total_fuel, total_cost,
            total_co2, total_hours, conditions_json, segment_display_json,
            sensor_timeline_json, fuel_plan_json
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        created_at, start_port, end_port, start_lat, start_lon, end_lat, end_lon,
        route_distance, int(segments), segment_mode, int(route_seed), vessel_type, capacity,
        speed, cargo, current_fuel, json.dumps(list(available_fuels)), total_fuel,
        total_cost, total_co2, total_hours, json.dumps(conditions),
        json.dumps(segment_display), json.dumps(sensor_timeline or []), json.dumps(fuel_plan or {})
    ))
    conn.commit()
    conn.close()


def load_voyage_report_by_timestamp(created_at):
    conn = sqlite3.connect(DB_NAME)
    row = pd.read_sql_query(
        "SELECT * FROM voyage_reports WHERE created_at = ? ORDER BY report_id DESC LIMIT 1",
        conn,
        params=(created_at,)
    )
    conn.close()
    return row.iloc[0].to_dict() if not row.empty else None


def parse_json_list(value, default=None):
    if default is None:
        default = []
    if value is None or value == "":
        return list(default)
    try:
        parsed = json.loads(value)
        return parsed if isinstance(parsed, list) else list(default)
    except Exception:
        return list(default)


def parse_json_object(value, default=None):
    if default is None:
        default = []
    if value is None or value == "":
        return default
    try:
        parsed = json.loads(value)
        return parsed if isinstance(parsed, (list, dict)) else default
    except Exception:
        return default

def clear_voyage_segment_history():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("DELETE FROM voyage_segments")
    conn.execute("DELETE FROM voyage_reports")
    conn.commit()
    conn.close()


# ============================================================
# PREDICTED SENSOR + SHIP HEALTH ENGINE
# ============================================================

WEATHER_SEVERITY = {
    "Calm Sea": 0.0, "Normal": 0.20, "Moderate": 0.45,
    "Heavy Weather": 0.75, "Storm": 1.00,
}

def predict_ship_sensors(segment_no, speed_knots, fuel_name, weather_name, wind_knots, wave_m, current_knots, fuel_remaining_pct=100.0):
    """Generate deterministic prototype sensor readings from voyage conditions."""
    severity = WEATHER_SEVERITY.get(weather_name, 0.25)
    speed_load = max(0.0, (float(speed_knots) - 12.0) / 12.0)
    wave_load = max(0.0, float(wave_m) - 1.5) / 4.0
    wind_load = max(0.0, float(wind_knots) - 15.0) / 30.0
    current_load = max(0.0, float(current_knots) - 0.8) / 3.0
    fuel_heat_factor = {"Diesel": 1.00, "Petrol": 1.04, "LNG": 0.94, "Methanol": 0.98, "Hydrogen": 0.90, "Ammonia": 0.93}.get(str(fuel_name).strip(), 1.0)
    load = max(0.0, 0.55 + speed_load * 0.35 + severity * 0.45 + wave_load * 0.18 + wind_load * 0.10 + current_load * 0.08)
    engine_temp = 68.0 + 34.0 * load * fuel_heat_factor
    coolant_temp = 62.0 + 25.0 * load
    fuel_temp = 32.0 + 12.0 * load + severity * 5.0
    rpm = 1050.0 + float(speed_knots) * 42.0 + severity * 170.0
    vibration = 1.3 + float(speed_knots) * 0.075 + wave_load * 2.2 + severity * 2.6
    oil_pressure = 5.4 - max(0.0, load - 0.95) * 1.8 - max(0.0, vibration - 3.0) * 0.12
    voltage = 24.6 - max(0.0, load - 0.9) * 1.7
    exhaust_temp = 285.0 + 220.0 * load + severity * 70.0
    leak_score = 0.0
    if vibration > 4.8: leak_score += 0.35
    if wave_m > 4.5: leak_score += 0.25
    if engine_temp > 108: leak_score += 0.25
    return {
        "segment": int(segment_no), "engine_temperature_c": round(engine_temp, 1),
        "coolant_temperature_c": round(coolant_temp, 1), "fuel_temperature_c": round(fuel_temp, 1),
        "engine_rpm": round(rpm, 0), "vibration_mm_s": round(vibration, 2),
        "oil_pressure_bar": round(max(oil_pressure, 2.5), 2), "voltage_v": round(max(voltage, 21.5), 2),
        "exhaust_temperature_c": round(exhaust_temp, 0), "leakage_probability": round(min(1.0, leak_score) * 100.0, 1),
        "fuel_remaining_pct": round(max(0.0, float(fuel_remaining_pct)), 1), "load_index": round(load * 100.0, 1),
    }

def analyze_ship_condition(sensor, weather_name, wind_knots, wave_m, speed_knots, fuel_name, fuel_margin_t):
    reasons, actions, critical, warning = [], [], [], []
    temp, vib, oil, exhaust, leakage = (sensor["engine_temperature_c"], sensor["vibration_mm_s"], sensor["oil_pressure_bar"], sensor["exhaust_temperature_c"], sensor["leakage_probability"])
    if temp >= 115: critical.append("Engine temperature is critically high")
    elif temp >= 100: warning.append("Engine temperature is above the normal prototype range")
    if vib >= 6.0: critical.append("Engine vibration is critically high")
    elif vib >= 4.5: warning.append("Engine vibration is elevated")
    if oil < 3.5: critical.append("Oil pressure is critically low")
    elif oil < 4.2: warning.append("Oil pressure is below the preferred prototype range")
    if exhaust >= 560: critical.append("Exhaust temperature is critically high")
    elif exhaust >= 500: warning.append("Exhaust temperature is high")
    if leakage >= 70: critical.append("Possible leakage condition detected")
    elif leakage >= 40: warning.append("Leakage risk is elevated")
    if speed_knots >= 20 and (wave_m >= 3.5 or wind_knots >= 30):
        reasons.append("High vessel speed is increasing engine load in rough conditions")
        actions.append("Reduce speed to lower engine load and fuel consumption")
    if wave_m >= 3.5:
        reasons.append("High waves increase vessel resistance")
        actions.append("Operate at a safer/reduced speed for the current sea state")
    if wind_knots >= 30: reasons.append("Strong wind is increasing resistance and power demand")
    if weather_name in ("Heavy Weather", "Storm"): reasons.append(f"{weather_name} is increasing the modeled operating load")
    if temp >= 100 and (speed_knots >= 18 or wave_m >= 3.5): reasons.append("Engine heat is consistent with increased load from speed/weather")
    if fuel_margin_t < 0:
        critical.append("Projected remaining fuel is below the modeled requirement")
        actions.append("Reduce consumption and identify a suitable refueling option if available")
    elif fuel_margin_t < 0.10:
        warning.append("Fuel reserve margin is becoming small")
        actions.append("Monitor fuel burn closely and recalculate the remaining voyage")
    if critical: status, primary = "🔴 CRITICAL", (actions[0] if actions else "Move to a safe operating condition and inspect the affected system")
    elif warning: status, primary = "🟠 HIGH RISK", (actions[0] if actions else "Reduce load/speed and continue close monitoring")
    elif reasons: status, primary = "🟡 WARNING", (actions[0] if actions else "Continue with increased monitoring")
    else: status, primary = "🟢 NORMAL", "Continue planned operation and monitor conditions"
    if not reasons and status != "🟢 NORMAL": reasons.append("One or more monitored values crossed the prototype alert threshold")
    return {"status": status, "reasons": list(dict.fromkeys(reasons)), "alerts": list(dict.fromkeys(critical + warning)), "actions": list(dict.fromkeys(actions)), "primary_action": primary, "fuel_name": fuel_name}

def build_sensor_timeline(conditions, segment_fuels, segment_speeds, segment_consumptions, recommended_start_fuel_t):
    rows, remaining = [], float(recommended_start_fuel_t)
    for idx, cond in enumerate(conditions):
        consumption = float(segment_consumptions[idx]); remaining = max(0.0, remaining - consumption)
        pct = (remaining / recommended_start_fuel_t * 100.0) if recommended_start_fuel_t > 0 else 0.0
        sensor = predict_ship_sensors(int(cond["segment"]), segment_speeds[idx], segment_fuels[idx], cond["weather"], cond["wind_speed"], cond["wave_height"], cond["current_speed"], pct)
        rows.append({**sensor, "weather": cond["weather"], "wind_knots": round(float(cond["wind_speed"]), 1), "wave_m": round(float(cond["wave_height"]), 1), "current_knots": round(float(cond["current_speed"]), 1), "fuel": segment_fuels[idx], "speed_knots": round(float(segment_speeds[idx]), 1), "fuel_consumption_t": round(consumption, 2), "fuel_remaining_t": round(remaining, 2)})
    return rows

def calculate_fuel_plan(total_fuel_t, conditions, capacity_t):
    severities = [WEATHER_SEVERITY.get(c.get("weather"), 0.25) for c in conditions]; max_severity = max(severities) if severities else 0.0
    weather_reserve_pct = 0.08 + max_severity * 0.12; operational_reserve_pct = 0.07
    reserve_pct = min(0.30, weather_reserve_pct + operational_reserve_pct); reserve_t = float(total_fuel_t) * reserve_pct
    return {"base_requirement_t": round(float(total_fuel_t), 2), "weather_reserve_pct": round(weather_reserve_pct * 100.0, 1), "operational_reserve_pct": round(operational_reserve_pct * 100.0, 1), "total_reserve_t": round(reserve_t, 2), "recommended_start_fuel_t": round(float(total_fuel_t) + reserve_t, 2), "reserve_percent": round(reserve_pct * 100.0, 1), "capacity_check_t": round(float(capacity_t) * 0.10, 2)}


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

# Distinct colors used when a graph contains voyage segments
# (S1, S2, S3, ...) rather than fuel names.
SEGMENT_COLORS = [
    "#3B82F6",  # blue
    "#EF4444",  # red
    "#22C55E",  # green
    "#F59E0B",  # amber
    "#A855F7",  # purple
    "#06B6D4",  # cyan
    "#EC4899",  # pink
    "#84CC16",  # lime
    "#F97316",  # orange
    "#6366F1"   # indigo
]


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

    colors = []

    for index, fuel in enumerate(fuels):

        # Fuel comparison graphs keep the fixed fuel-specific colors.
        if fuel in FUEL_COLORS:
            colors.append(FUEL_COLORS[fuel])

        # Voyage segment graphs use a different color for each segment
        # so S1, S2, S3, ... are visually easy to distinguish.
        else:
            colors.append(
                SEGMENT_COLORS[index % len(SEGMENT_COLORS)]
            )

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
# COMPANY FLEET + CUSTOMER ORDER OPTIMIZATION
# ============================================================

CONTAINER_TYPES = {
    "20 ft": {"payload_t": 18.0, "label": "20 ft standard container"},
    "40 ft": {"payload_t": 26.0, "label": "40 ft standard container"},
    "40 ft High Cube": {"payload_t": 28.0, "label": "40 ft High Cube container"},
}


def generate_sample_fleet(n_ships=100):
    """Create demo fleet data when a company has not uploaded its own data."""
    ports = list(WORLD_PORTS.keys())
    fuels = list(fuel_data.keys())
    vessel_types = ["Container Ship", "Bulk Carrier", "Tanker", "Cargo Ship"]
    rows = []

    for i in range(1, int(n_ships) + 1):
        rng = np.random.default_rng(2026 + i)
        capacity_t = float(rng.choice([2500, 4000, 6000, 8000, 10000, 12000, 16000, 20000]))
        fuel = fuels[(i - 1) % len(fuels)]
        max_speed = float(rng.choice([16, 17, 18, 19, 20, 21]))
        min_speed = float(max(7, max_speed - rng.choice([6, 7, 8])))
        tank = float(capacity_t * rng.uniform(3.5, 6.5))
        avg_consumption = float(max(8, capacity_t / 1000 * rng.uniform(1.5, 2.8)))
        status = "Available" if i % 11 != 0 else "Maintenance"
        health = "Normal" if i % 13 != 0 else ("Warning" if i % 7 != 0 else "High Risk")
        rows.append({
            "Ship_ID": f"S{i:03d}",
            "Vessel_Type": vessel_types[(i - 1) % len(vessel_types)],
            "Capacity_t": round(capacity_t, 0),
            "Fuel": fuel,
            "Fuel_Tank_t": round(tank, 1),
            "Max_Speed_kn": max_speed,
            "Min_Speed_kn": min_speed,
            "Current_Location": ports[(i * 7) % len(ports)],
            "Availability": status,
            "Health": health,
            "Avg_Consumption_t_per_1000km": round(avg_consumption, 2),
        })
    return pd.DataFrame(rows)


def normalize_fleet_dataframe(df):
    """Accept common company CSV/Excel column names and normalize them."""
    data = df.copy()
    data.columns = [str(c).strip() for c in data.columns]
    aliases = {
        "ship_id": ["ship_id", "ship id", "ship", "vessel_id", "vessel id", "name"],
        "vessel_type": ["vessel_type", "vessel type", "ship_type", "ship type", "type"],
        "capacity_t": ["capacity_t", "capacity", "capacity tonnes", "capacity_tonnes", "cargo capacity"],
        "fuel": ["fuel", "fuel_type", "fuel type", "current fuel"],
        "fuel_tank_t": ["fuel_tank_t", "fuel tank", "fuel tank tonnes", "tank capacity"],
        "max_speed_kn": ["max_speed_kn", "max speed", "max speed knots", "maximum speed"],
        "min_speed_kn": ["min_speed_kn", "min speed", "min speed knots", "minimum speed"],
        "current_location": ["current_location", "current location", "location", "port", "current port"],
        "availability": ["availability", "status", "available"],
        "health": ["health", "health status", "condition"],
        "avg_consumption_t_per_1000km": ["avg_consumption_t_per_1000km", "avg consumption", "consumption", "fuel consumption"],
    }
    lower_map = {str(c).strip().lower(): c for c in data.columns}
    renamed = {}
    for target, choices in aliases.items():
        for choice in choices:
            if choice.lower() in lower_map:
                renamed[lower_map[choice.lower()]] = target
                break
    data = data.rename(columns=renamed)

    defaults = generate_sample_fleet(max(len(data), 1))
    required_defaults = {
        "Ship_ID": "ship_id", "Vessel_Type": "vessel_type", "Capacity_t": "capacity_t",
        "Fuel": "fuel", "Fuel_Tank_t": "fuel_tank_t", "Max_Speed_kn": "max_speed_kn",
        "Min_Speed_kn": "min_speed_kn", "Current_Location": "current_location",
        "Availability": "availability", "Health": "health",
        "Avg_Consumption_t_per_1000km": "avg_consumption_t_per_1000km",
    }
    for target, source in required_defaults.items():
        if source not in data.columns:
            data[source] = defaults[target].values[:len(data)]

    for col in ["capacity_t", "fuel_tank_t", "max_speed_kn", "min_speed_kn", "avg_consumption_t_per_1000km"]:
        data[col] = pd.to_numeric(data[col], errors="coerce")
    data["capacity_t"] = data["capacity_t"].fillna(5000).clip(lower=100)
    data["fuel_tank_t"] = data["fuel_tank_t"].fillna(data["capacity_t"] * 4)
    data["max_speed_kn"] = data["max_speed_kn"].fillna(18).clip(lower=5)
    data["min_speed_kn"] = data["min_speed_kn"].fillna(8).clip(lower=3)
    data["avg_consumption_t_per_1000km"] = data["avg_consumption_t_per_1000km"].fillna(data["capacity_t"] / 1000 * 2)
    data["fuel"] = data["fuel"].astype(str).str.strip().where(data["fuel"].astype(str).str.strip().isin(fuel_data), "Diesel")
    data["availability"] = data["availability"].astype(str).str.strip().replace({"nan": "Available", "available": "Available", "AVAILABLE": "Available"})
    data["health"] = data["health"].astype(str).str.strip().replace({"nan": "Normal", "normal": "Normal"})
    data["current_location"] = data["current_location"].astype(str).str.strip()
    data["ship_id"] = data["ship_id"].astype(str).str.strip()
    data["vessel_type"] = data["vessel_type"].astype(str).str.strip()

    return data[
        ["ship_id", "vessel_type", "capacity_t", "fuel", "fuel_tank_t",
         "max_speed_kn", "min_speed_kn", "current_location", "availability",
         "health", "avg_consumption_t_per_1000km"]
    ].reset_index(drop=True)


def port_distance_km(port_a, port_b):
    if port_a not in WORLD_PORTS or port_b not in WORLD_PORTS:
        return 0.0
    return haversine_km(*WORLD_PORTS[port_a], *WORLD_PORTS[port_b])


def fleet_order_optimization(fleet_df, origin, destination, cargo_t, deadline_days, weather, wind_speed, wave_height, current_speed):
    """Select the smallest practical fleet first, then rank ships by cost/ETA/health."""
    route_km = port_distance_km(origin, destination)
    if route_km <= 0:
        return None

    working = fleet_df.copy()
    working["reposition_km"] = working["current_location"].apply(lambda x: port_distance_km(x, origin))
    working["voyage_km"] = route_km + working["reposition_km"]
    working["weather_factor"] = [
        environmental_factor(weather, wind_speed, wave_height, current_speed)
        for _ in range(len(working))
    ]
    working["planned_speed_kn"] = np.minimum(
        working["max_speed_kn"],
        np.maximum(working["min_speed_kn"], 16.0)
    )
    working["eta_days"] = working["voyage_km"] / (working["planned_speed_kn"] * 1.852 * 24)
    working["fuel_t"] = (
        working["avg_consumption_t_per_1000km"]
        * working["voyage_km"] / 1000
        * working["weather_factor"]
    )
    working["fuel_cost"] = working.apply(lambda r: r["fuel_t"] * fuel_data[r["fuel"]]["cost"], axis=1)
    working["co2_t"] = working.apply(lambda r: r["fuel_t"] * fuel_data[r["fuel"]]["co2_factor"], axis=1)

    eligible = working[
        (working["availability"].str.lower() == "available")
        & (~working["health"].str.lower().isin(["critical", "high risk", "maintenance"]))
        & (working["capacity_t"] > 0)
    ].copy()

    if eligible.empty:
        return {"route_km": route_km, "eligible": eligible, "selected": eligible, "cargo_shortfall": cargo_t}

    health_penalty = eligible["health"].str.lower().map({"warning": 1.0, "normal": 0.0}).fillna(0.5)
    fuel_rank = eligible["fuel_cost"] / eligible["capacity_t"].replace(0, np.nan)
    eta_penalty = np.maximum(eligible["eta_days"] - float(deadline_days), 0) * 10000
    eligible["selection_score"] = (
        fuel_rank * 0.50
        + eligible["co2_t"] / eligible["capacity_t"] * 0.25
        + eligible["reposition_km"] / 1000 * 0.10
        + eta_penalty
        + health_penalty * 50
    )
    eligible = eligible.sort_values(["selection_score", "capacity_t"], ascending=[True, False]).reset_index(drop=True)

    selected_rows = []
    carried = 0.0
    for _, row in eligible.iterrows():
        selected_rows.append(row)
        carried += float(row["capacity_t"])
        if carried >= cargo_t:
            break

    selected = pd.DataFrame(selected_rows)
    return {
        "route_km": route_km,
        "eligible": eligible,
        "selected": selected,
        "cargo_shortfall": max(0.0, cargo_t - carried),
    }


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
# COMPANY FLEET ORDER PLANNER
# ============================================================

st.markdown(
    '<div class="section-title">'
    '🏢 Company Fleet & Customer Order Optimization'
    '</div>',
    unsafe_allow_html=True
)

st.info(
    "Upload the company's real fleet data when available. "
    "If no fleet file is available, the prototype can generate a simulated N-ship fleet for demonstration."
)

fleet_setup_1, fleet_setup_2 = st.columns(2)

with fleet_setup_1:
    fleet_count = st.number_input(
        "Number of ships (N)",
        min_value=1,
        max_value=5000,
        value=100,
        step=1,
        key="fleet_count_n"
    )

with fleet_setup_2:
    fleet_file = st.file_uploader(
        "📤 Upload company fleet CSV / Excel",
        type=["csv", "xlsx", "xls"],
        key="company_fleet_upload"
    )

if fleet_file is not None:
    try:
        if fleet_file.name.lower().endswith(".csv"):
            uploaded_fleet = pd.read_csv(fleet_file)
        else:
            uploaded_fleet = pd.read_excel(fleet_file)
        st.session_state["company_fleet_df"] = normalize_fleet_dataframe(uploaded_fleet)
        st.session_state["company_fleet_source"] = f"Company upload: {fleet_file.name}"
    except Exception as fleet_error:
        st.error(f"Could not read the fleet file: {fleet_error}")

# Keep the fleet dataframe robust across Streamlit reruns and older
# session-state data created by earlier versions of this feature.
if "company_fleet_df" not in st.session_state:
    st.session_state["company_fleet_df"] = generate_sample_fleet(int(fleet_count))
    st.session_state["company_fleet_source"] = "Simulated fleet"

# If the user is using the simulated fleet and changes N, regenerate the
# sample fleet so the requested N is actually reflected.
if (
    st.session_state.get("company_fleet_source") == "Simulated fleet"
    and len(st.session_state.get("company_fleet_df", pd.DataFrame())) != int(fleet_count)
):
    st.session_state["company_fleet_df"] = generate_sample_fleet(int(fleet_count))

# Normalize BOTH uploaded and previously-created session data. This also
# adds missing columns such as availability/health from older app versions.
try:
    st.session_state["company_fleet_df"] = normalize_fleet_dataframe(
        st.session_state["company_fleet_df"]
    )
except Exception as fleet_normalize_error:
    st.warning(
        f"Fleet data needed repair, so a sample fleet was created: {fleet_normalize_error}"
    )
    st.session_state["company_fleet_df"] = generate_sample_fleet(int(fleet_count))
    st.session_state["company_fleet_source"] = "Simulated fleet"

fleet_df = st.session_state["company_fleet_df"].copy()

# Defensive checks prevent a single missing/invalid column from crashing
# the dashboard.
if "availability" not in fleet_df.columns:
    fleet_df["availability"] = "Available"
if "capacity_t" not in fleet_df.columns:
    fleet_df["capacity_t"] = 5000.0

available_mask = (
    fleet_df["availability"]
    .astype(str)
    .str.strip()
    .str.lower()
    .eq("available")
)

fc1, fc2, fc3 = st.columns(3)
with fc1:
    st.metric("Fleet Ships", len(fleet_df))
with fc2:
    st.metric("Available Ships", int(available_mask.sum()))
with fc3:
    st.metric(
        "Total Capacity",
        f"{pd.to_numeric(fleet_df['capacity_t'], errors='coerce').fillna(0).sum():,.0f} t"
    )

st.caption(f"Fleet source: **{st.session_state.get('company_fleet_source', 'Simulated fleet')}**")

with st.expander("🔎 View / verify fleet data", expanded=False):
    st.dataframe(
        fleet_df.rename(columns={
            "ship_id": "Ship ID",
            "vessel_type": "Vessel Type",
            "capacity_t": "Capacity (t)",
            "fuel": "Fuel",
            "fuel_tank_t": "Fuel Tank (t)",
            "max_speed_kn": "Max Speed (kn)",
            "min_speed_kn": "Min Speed (kn)",
            "current_location": "Current Location",
            "availability": "Availability",
            "health": "Health",
            "avg_consumption_t_per_1000km": "Avg Consumption (t/1000 km)"
        }),
        use_container_width=True,
        hide_index=True
    )

st.markdown("### 📦 Customer Order")

order1, order2, order3 = st.columns(3)
with order1:
    order_origin = st.selectbox(
        "From",
        list(WORLD_PORTS.keys()),
        index=list(WORLD_PORTS.keys()).index("Chennai, India") if "Chennai, India" in WORLD_PORTS else 0,
        key="fleet_order_origin"
    )
with order2:
    order_destination = st.selectbox(
        "To",
        list(WORLD_PORTS.keys()),
        index=list(WORLD_PORTS.keys()).index("Mumbai, India") if "Mumbai, India" in WORLD_PORTS else 1,
        key="fleet_order_destination"
    )
with order3:
    order_cargo_t = st.number_input(
        "Customer Cargo (tonnes)",
        min_value=100.0,
        max_value=10000000.0,
        value=100000.0,
        step=1000.0,
        key="fleet_order_cargo"
    )

order4, order5, order6 = st.columns(3)
with order4:
    order_deadline_days = st.number_input(
        "Required Delivery (days)",
        min_value=1.0,
        max_value=365.0,
        value=5.0,
        step=0.5,
        key="fleet_order_deadline"
    )
with order5:
    container_type = st.selectbox(
        "Container Size",
        list(CONTAINER_TYPES.keys()),
        key="fleet_container_type"
    )
with order6:
    order_weather = st.selectbox(
        "Route Weather",
        ["Normal", "Calm Sea", "Moderate", "Heavy Weather", "Storm"],
        key="fleet_order_weather"
    )

weather_inputs_1, weather_inputs_2, weather_inputs_3 = st.columns(3)
with weather_inputs_1:
    order_wind = st.number_input("Route Wind (knots)", 0.0, 40.0, 10.0, 1.0, key="fleet_order_wind")
with weather_inputs_2:
    order_wave = st.number_input("Route Wave Height (m)", 0.1, 8.0, 1.2, 0.1, key="fleet_order_wave")
with weather_inputs_3:
    order_current = st.number_input("Route Current (knots)", 0.0, 5.0, 0.6, 0.1, key="fleet_order_current")

optimize_fleet_button = st.button(
    "⚛️ Find Best Ships for Customer Order",
    type="primary",
    use_container_width=True,
    key="optimize_company_fleet"
)

if optimize_fleet_button:
    if order_origin == order_destination:
        st.error("From and To ports must be different.")
    else:
        fleet_result = fleet_order_optimization(
            fleet_df,
            order_origin,
            order_destination,
            float(order_cargo_t),
            float(order_deadline_days),
            order_weather,
            float(order_wind),
            float(order_wave),
            float(order_current)
        )
        st.session_state["fleet_order_result"] = fleet_result
        st.session_state["fleet_order_meta"] = {
            "origin": order_origin,
            "destination": order_destination,
            "cargo_t": float(order_cargo_t),
            "deadline_days": float(order_deadline_days),
            "container_type": container_type,
            "weather": order_weather,
            "wind": float(order_wind),
            "wave": float(order_wave),
            "current": float(order_current),
        }

if "fleet_order_result" in st.session_state:
    result = st.session_state["fleet_order_result"]
    meta = st.session_state["fleet_order_meta"]
    selected = result["selected"].copy()
    route_km = float(result["route_km"])
    container_payload = CONTAINER_TYPES[meta["container_type"]]["payload_t"]
    required_containers = int(math.ceil(meta["cargo_t"] / container_payload))

    if selected.empty or result["cargo_shortfall"] > 0:
        assigned_capacity = float(selected["capacity_t"].sum()) if not selected.empty else 0.0
        st.error(
            f"⚠️ Fleet capacity is insufficient. Customer requested {meta['cargo_t']:,.0f} t, "
            f"but only {assigned_capacity:,.0f} t is currently assignable from eligible ships. "
            f"Shortfall: {result['cargo_shortfall']:,.0f} t."
        )
    else:
        selected["Cargo_Assigned_t"] = 0.0
        remaining = float(meta["cargo_t"])
        for idx in selected.index:
            assigned = min(float(selected.loc[idx, "capacity_t"]), remaining)
            selected.loc[idx, "Cargo_Assigned_t"] = assigned
            remaining -= assigned
            if remaining <= 0:
                break
        selected["Container_Count"] = np.ceil(selected["Cargo_Assigned_t"] / container_payload).astype(int)

        total_fuel = float(selected["fuel_t"].sum())
        total_cost = float(selected["fuel_cost"].sum())
        total_co2 = float(selected["co2_t"].sum())
        max_eta = float(selected["eta_days"].max())
        total_capacity = float(selected["capacity_t"].sum())
        reserve_fuel = total_fuel * 0.10
        recommended_fuel = total_fuel + reserve_fuel

        st.success(
            f"✅ Recommended fleet: **{len(selected)} ships** for {meta['cargo_t']:,.0f} tonnes. "
            f"Route distance: **{route_km:,.0f} km**."
        )

        km1, km2, km3, km4 = st.columns(4)
        km1.metric("Ships Selected", len(selected))
        km2.metric("Containers", f"{required_containers:,}")
        km3.metric("Estimated Fuel", f"{recommended_fuel:,.2f} t")
        km4.metric("Estimated CO₂", f"{total_co2:,.2f} t")

        km5, km6, km7 = st.columns(3)
        km5.metric("Fuel Cost", f"₹{total_cost:,.0f}")
        km6.metric("Fleet Capacity", f"{total_capacity:,.0f} t")
        km7.metric("Latest ETA", f"{max_eta:.2f} days")

        if max_eta <= meta["deadline_days"]:
            st.success(f"🟢 Delivery target met: estimated fleet ETA {max_eta:.2f} days ≤ {meta['deadline_days']:.2f} days.")
        else:
            st.warning(f"🟡 Delivery target risk: estimated fleet ETA {max_eta:.2f} days > {meta['deadline_days']:.2f} days.")

        display_selected = selected[[
            "ship_id", "current_location", "capacity_t", "cargo_assigned_t", "container_count",
            "fuel", "fuel_t", "fuel_cost", "co2_t", "planned_speed_kn", "eta_days", "health"
        ]].copy()
        display_selected.columns = [
            "Ship ID", "Current Location", "Capacity (t)", "Cargo Assigned (t)", "Containers",
            "Fuel", "Fuel (t)", "Fuel Cost (₹)", "CO₂ (t)", "Planned Speed (kn)", "ETA (days)", "Health"
        ]
        st.markdown("#### 🚢 Selected Ships & Cargo Allocation")
        st.dataframe(display_selected, use_container_width=True, hide_index=True)

        st.markdown("#### 🧠 Why these ships were selected")
        st.write(
            "The prototype first removes unavailable/high-risk ships, then compares the remaining ships using "
            "capacity, fuel consumption/cost, CO₂, repositioning distance, delivery time and health. "
            "It keeps selecting the best-ranked ships until the customer cargo requirement is satisfied."
        )

        st.caption(
            "Prototype note: fleet data and sensor/health values can be simulated for demonstration. "
            "Real deployment should use approved company telemetry, vessel specifications, weather data and qualified operational decisions."
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
            co2_reduction,
            available_fuels,
            wind_speed_now,
            wave_height_now,
            current_speed_now

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

    voyage_created_at = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
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

            voyage_created_at,

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

    segment_fuels = [row[9] for row in voyage_rows]
    segment_speeds = [row[10] for row in voyage_rows]
    segment_consumptions = [row[11] for row in voyage_rows]
    fuel_plan = calculate_fuel_plan(total_fuel, conditions, capacity)
    sensor_timeline = build_sensor_timeline(conditions, segment_fuels, segment_speeds, segment_consumptions, fuel_plan["recommended_start_fuel_t"])
    for i, sensor_row in enumerate(sensor_timeline):
        remaining_need = sum(segment_consumptions[i + 1:])
        margin = sensor_row["fuel_remaining_t"] - remaining_need
        sensor_row["fuel_margin_t"] = round(margin, 2)
        sensor_row["health"] = analyze_ship_condition(sensor_row, sensor_row["weather"], sensor_row["wind_knots"], sensor_row["wave_m"], sensor_row["speed_knots"], sensor_row["fuel"], margin)

    save_voyage_segments(
        voyage_rows
    )

    save_voyage_report(
        voyage_created_at,
        start_port,
        end_port,
        start_lat,
        start_lon,
        end_lat,
        end_lon,
        route_distance,
        int(segments),
        segment_mode,
        int(route_seed),
        vessel_type,
        capacity,
        speed,
        cargo,
        fuel_type,
        available_fuels,
        total_fuel,
        total_cost,
        total_co2,
        total_hours,
        conditions,
        segment_display,
        sensor_timeline,
        fuel_plan
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
        "sensor_timeline"
    ] = sensor_timeline

    st.session_state[
        "fuel_plan"
    ] = fuel_plan

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
# VOYAGE FUEL PLANNING + PREDICTED SENSOR HEALTH
# ============================================================

st.markdown('<div class="section-title">⛽ Voyage Fuel Planning & Ship Health Prediction</div>', unsafe_allow_html=True)

if st.session_state.get("voyage_done", False):
    sensor_timeline = st.session_state.get("sensor_timeline", [])
    fuel_plan = st.session_state.get("fuel_plan", {})
else:
    temp_conditions = conditions
    temp_fuels, temp_speeds, temp_consumptions = [], [], []
    for cond in temp_conditions:
        temp_best = optimize_single_segment(capacity, segment_distance, speed, cargo, available_fuels, cond["weather"], cond["wind_speed"], cond["wave_height"], cond["current_speed"])
        temp_fuels.append(temp_best["fuel"]); temp_speeds.append(temp_best["speed"]); temp_consumptions.append(temp_best["fuel_consumption"])
    fuel_plan = calculate_fuel_plan(sum(temp_consumptions), temp_conditions, capacity)
    sensor_timeline = build_sensor_timeline(temp_conditions, temp_fuels, temp_speeds, temp_consumptions, fuel_plan["recommended_start_fuel_t"])
    for i, sensor_row in enumerate(sensor_timeline):
        remaining_need = sum(temp_consumptions[i + 1:]); margin = sensor_row["fuel_remaining_t"] - remaining_need
        sensor_row["fuel_margin_t"] = round(margin, 2)
        sensor_row["health"] = analyze_ship_condition(sensor_row, sensor_row["weather"], sensor_row["wind_knots"], sensor_row["wave_m"], sensor_row["speed_knots"], sensor_row["fuel"], margin)

fp1, fp2, fp3, fp4 = st.columns(4)
fp1.metric("Base Voyage Fuel", f"{fuel_plan.get('base_requirement_t', 0):.2f} t")
fp2.metric("Weather Reserve", f"{fuel_plan.get('weather_reserve_pct', 0):.1f}%")
fp3.metric("Reserve Fuel", f"{fuel_plan.get('total_reserve_t', 0):.2f} t")
fp4.metric("Recommended Start Fuel", f"{fuel_plan.get('recommended_start_fuel_t', 0):.2f} t")
st.info(f"⛽ Recommended starting fuel: {fuel_plan.get('recommended_start_fuel_t', 0):.2f} t. This includes a modeled reserve that grows with heavier simulated weather.")

if sensor_timeline:
    sensor_df = pd.DataFrame([{
        "Segment": r["segment"], "Weather": r["weather"], "Engine Temp (°C)": r["engine_temperature_c"],
        "RPM": r["engine_rpm"], "Vibration (mm/s)": r["vibration_mm_s"], "Oil Pressure (bar)": r["oil_pressure_bar"],
        "Fuel Level (%)": r["fuel_remaining_pct"], "Fuel Remaining (t)": r["fuel_remaining_t"], "Fuel Margin (t)": r["fuel_margin_t"], "Health": r["health"]["status"]
    } for r in sensor_timeline])
    st.markdown("### 📡 Predicted Onboard Sensor Timeline")
    st.dataframe(sensor_df, use_container_width=True, hide_index=True)

    sensor_idx = min(max(step - 1, 0), len(sensor_timeline) - 1)
    selected_sensor = sensor_timeline[sensor_idx]; health = selected_sensor["health"]
    st.markdown("### 🧠 Ship Condition Decision Support")
    h1, h2, h3 = st.columns(3)
    h1.metric("Ship Status", health["status"]); h2.metric("Engine Temperature", f"{selected_sensor['engine_temperature_c']:.1f} °C"); h3.metric("Fuel Remaining", f"{selected_sensor['fuel_remaining_t']:.2f} t")
    s1, s2, s3, s4 = st.columns(4)
    s1.metric("RPM", f"{selected_sensor['engine_rpm']:.0f}"); s2.metric("Vibration", f"{selected_sensor['vibration_mm_s']:.2f} mm/s"); s3.metric("Oil Pressure", f"{selected_sensor['oil_pressure_bar']:.2f} bar"); s4.metric("Exhaust Temp", f"{selected_sensor['exhaust_temperature_c']:.0f} °C")
    s5, s6, s7, s8 = st.columns(4)
    s5.metric("Coolant Temp", f"{selected_sensor['coolant_temperature_c']:.1f} °C"); s6.metric("Fuel Temp", f"{selected_sensor['fuel_temperature_c']:.1f} °C"); s7.metric("Voltage", f"{selected_sensor['voltage_v']:.2f} V"); s8.metric("Leak Risk", f"{selected_sensor['leakage_probability']:.1f}%")

    if health["status"] == "🔴 CRITICAL": st.error("🚨 CRITICAL ALERT — Follow approved vessel procedures and qualified crew instructions.")
    elif health["status"] == "🟠 HIGH RISK": st.warning("⚠️ HIGH-RISK ALERT — Operating conditions need close attention and corrective action.")
    elif health["status"] == "🟡 WARNING": st.warning("🟡 WARNING — A monitored condition is becoming abnormal.")
    else: st.success("🟢 NORMAL — No prototype threshold is currently indicating an abnormal ship condition.")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### 🔍 Why did the alert happen?")
        for reason in (health["reasons"] or ["No abnormal cause identified in the current prototype model."]): st.write(f"• {reason}")
        if health["alerts"]:
            st.markdown("#### 🚨 Detected Issues")
            for item in health["alerts"]: st.write(f"• {item}")
    with c2:
        st.markdown("#### 💡 Recommended Action")
        st.info(health["primary_action"])
        for action in health["actions"]: st.write(f"• {action}")
        st.markdown("#### ⛽ Fuel Decision")
        if selected_sensor["fuel_margin_t"] < 0:
            st.error(f"Fuel risk: about {abs(selected_sensor['fuel_margin_t']):.2f} t below the modeled remaining requirement. Reduce consumption and consider refueling if available.")
        elif selected_sensor["fuel_margin_t"] < fuel_plan.get("total_reserve_t", 0) * 0.35:
            st.warning("Fuel reserve is becoming tight. Recalculate the remaining voyage if weather or speed changes.")
        else:
            st.success(f"Fuel margin is positive: {selected_sensor['fuel_margin_t']:.2f} t above the modeled remaining requirement.")

    st.markdown("#### 📈 Predicted Sensor Trends")
    trend_df = pd.DataFrame([{
        "Segment": r["segment"], "Engine Temperature (°C)": r["engine_temperature_c"], "Coolant Temperature (°C)": r["coolant_temperature_c"],
        "Vibration (mm/s)": r["vibration_mm_s"], "Exhaust Temperature (°C)": r["exhaust_temperature_c"], "Fuel Remaining (t)": r["fuel_remaining_t"]
    } for r in sensor_timeline])
    st.line_chart(trend_df.set_index("Segment"))
    st.caption("Prototype note: these are predicted/simulated sensor readings. Real deployment requires validated telemetry, manufacturer limits, approved alarms and qualified crew decisions.")


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

            st.session_state.pop(
                "selected_prediction_id",
                None
            )

            st.rerun()

    st.caption(
        "💡 Click/select any row to reopen that exact saved prediction report. "
        "The report uses the saved values from that run, not today's sidebar inputs."
    )

    prediction_event = st.dataframe(

        history_df,

        use_container_width=True,

        hide_index=True,

        on_select="rerun",

        selection_mode="single-row",

        key="prediction_history_table"

    )

    selected_prediction_rows = prediction_event.selection.rows

    if selected_prediction_rows:

        selected_index = int(
            selected_prediction_rows[0]
        )

        selected_prediction_id = int(
            history_df.iloc[
                selected_index
            ]["ID"]
        )

        st.session_state[
            "selected_prediction_id"
        ] = selected_prediction_id

    else:

        # When the user unchecks/deselects the row, immediately close
        # the saved report by clearing the remembered selection.
        st.session_state.pop(
            "selected_prediction_id",
            None
        )

    selected_prediction_id = st.session_state.get(
        "selected_prediction_id"
    )

    if selected_prediction_id is not None:

        record = load_prediction_record(
            selected_prediction_id
        )

        if record is not None:

            st.markdown(

                '<div class="section-title">'
                '📋 Complete Saved Prediction Report'
                '</div>',

                unsafe_allow_html=True

            )

            st.info(
                "🔒 This report is a saved snapshot. "
                "Changing the sidebar now will not change this historical result."
            )

            report_top1, report_top2 = st.columns(
                [1, 1]
            )

            with report_top1:

                st.markdown(
                    f"""
                    <div class="card">
                    <h3>📥 Original Inputs</h3>
                    <b>Record ID:</b> {int(record['id'])}<br>
                    <b>Date & Time:</b> {record['created_at']}<br>
                    <b>Vessel:</b> {record['vessel_type']}<br>
                    <b>Capacity:</b> {float(record['capacity']):,.0f} tonnes<br>
                    <b>Speed:</b> {float(record['speed']):.1f} knots<br>
                    <b>Distance:</b> {float(record['distance']):,.1f} km<br>
                    <b>Cargo Demand:</b> {float(record['cargo']):,.0f} tonnes<br>
                    <b>Current Fuel:</b> {record['current_fuel']}<br>
                    <b>Fuel Price:</b> ₹{float(record['fuel_price']):,.0f}/tonne<br>
                    <b>Weather:</b> {record['weather']}<br>
                    <b>Wind:</b> {record.get('wind_speed') if record.get('wind_speed') is not None else 'Not saved in legacy record'} kn<br>
                    <b>Wave:</b> {record.get('wave_height') if record.get('wave_height') is not None else 'Not saved in legacy record'} m<br>
                    <b>Current:</b> {record.get('current_speed') if record.get('current_speed') is not None else 'Not saved in legacy record'} kn<br>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with report_top2:

                st.markdown(
                    f"""
                    <div class="success-box">
                    <h3>📤 Saved Optimization Result</h3>
                    <b>Recommended Fuel:</b> {record['optimized_fuel_type']}<br>
                    <b>Recommended Speed:</b> {float(record['optimized_speed']):.1f} knots<br>
                    <b>Optimized Fuel:</b> {float(record['optimized_fuel']):.4f} tonnes<br>
                    <b>Optimized Cost:</b> ₹{float(record['optimized_cost']):,.2f}<br>
                    <b>Optimized CO₂:</b> {float(record['optimized_co2']):.4f} tonnes<br><br>
                    <b>Fuel Saving:</b> {float(record['fuel_saving']):.2f}%<br>
                    <b>Cost Saving:</b> {float(record['cost_saving']):.2f}%<br>
                    <b>CO₂ Reduction:</b> {float(record['co2_reduction']):.2f}%
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            available_saved = parse_json_list(
                record.get("available_fuels_json"),
                [record["current_fuel"]]
            )

            st.markdown(
                '<div class="section-title">'
                '⛽ Saved Fuel Availability'
                '</div>',
                unsafe_allow_html=True
            )

            st.write(
                "**Available Fuels in That Run:** "
                + ", ".join(str(x) for x in available_saved)
            )

            comparison_saved = pd.DataFrame({
                "Metric": [
                    "Fuel Consumption (t)",
                    "Fuel Cost (₹)",
                    "CO₂ Emissions (t)"
                ],
                "Current Plan": [
                    float(record["predicted_fuel"]),
                    float(record["initial_cost"]),
                    float(record["initial_co2"])
                ],
                "Optimized Plan": [
                    float(record["optimized_fuel"]),
                    float(record["optimized_cost"]),
                    float(record["optimized_co2"])
                ]
            })

            st.dataframe(
                comparison_saved,
                use_container_width=True,
                hide_index=True
            )

            saved_chart_fuels = parse_json_list(
                record.get("chart_fuels_json"),
                []
            )
            saved_chart_values = parse_json_list(
                record.get("chart_values_json"),
                []
            )
            saved_chart_emissions = parse_json_list(
                record.get("chart_emissions_json"),
                []
            )

            # Legacy records did not have chart snapshots. In that case,
            # show a historical current-vs-optimized comparison instead of
            # recalculating the old record from today's inputs.
            if not saved_chart_fuels or not saved_chart_values:

                saved_chart_fuels = [
                    "Current Plan",
                    "Optimized Plan"
                ]

                saved_chart_values = [
                    float(record["predicted_fuel"]),
                    float(record["optimized_fuel"])
                ]

                saved_chart_emissions = [
                    float(record["initial_co2"]),
                    float(record["optimized_co2"])
                ]

            st.markdown(
                '<div class="section-title">'
                '📊 Saved Fuel Consumption Graph'
                '</div>',
                unsafe_allow_html=True
            )

            historical_fuel_fig = create_3d_bar_chart(
                saved_chart_fuels,
                saved_chart_values,
                "Saved Fuel Consumption Comparison",
                "Fuel (tonnes)"
            )

            st.pyplot(
                historical_fuel_fig,
                use_container_width=True
            )

            plt.close(
                historical_fuel_fig
            )

            st.markdown(
                '<div class="section-title">'
                '🌱 Saved CO₂ Graph'
                '</div>',
                unsafe_allow_html=True
            )

            historical_co2_fig = create_3d_bar_chart(
                saved_chart_fuels,
                saved_chart_emissions,
                "Saved CO₂ Comparison",
                "CO₂ (tonnes)"
            )

            st.pyplot(
                historical_co2_fig,
                use_container_width=True
            )

            plt.close(
                historical_co2_fig
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

            st.session_state.pop(
                "selected_voyage_segment_id",
                None
            )

            st.rerun()

    st.caption(
        "💡 Click/select any segment row to reopen the saved voyage report for that run."
    )

    voyage_event = st.dataframe(

        segment_history,

        use_container_width=True,

        hide_index=True,

        on_select="rerun",

        selection_mode="single-row",

        key="voyage_history_table"

    )

    selected_voyage_rows = voyage_event.selection.rows

    if selected_voyage_rows:

        selected_voyage_index = int(
            selected_voyage_rows[0]
        )

        selected_voyage_id = int(
            segment_history.iloc[
                selected_voyage_index
            ]["ID"]
        )

        st.session_state[
            "selected_voyage_segment_id"
        ] = selected_voyage_id

    else:

        # When the user unchecks/deselects the row, immediately close
        # the complete saved voyage report.
        st.session_state.pop(
            "selected_voyage_segment_id",
            None
        )

    selected_voyage_id = st.session_state.get(
        "selected_voyage_segment_id"
    )

    if selected_voyage_id is not None:

        selected_segment = segment_history[
            segment_history["ID"] == selected_voyage_id
        ]

        if not selected_segment.empty:

            selected_segment = selected_segment.iloc[0]

            voyage_report = load_voyage_report_by_timestamp(
                selected_segment["Date & Time"]
            )

            st.markdown(
                '<div class="section-title">'
                '📋 Complete Saved Voyage Report'
                '</div>',
                unsafe_allow_html=True
            )

            if voyage_report is not None:

                st.info(
                    "🔒 This is the saved voyage snapshot from that run. "
                    "Current sidebar values do not modify it."
                )

                report_route_1, report_route_2 = st.columns(2)

                with report_route_1:

                    st.markdown(
                        f"""
                        <div class="card">
                        <h3>🗺️ Route</h3>
                        <b>Run Date & Time:</b> {voyage_report['created_at']}<br>
                        <b>Start:</b> {voyage_report['start_port']}<br>
                        <b>Destination:</b> {voyage_report['end_port']}<br>
                        <b>Route Distance:</b> {float(voyage_report['route_distance']):,.1f} km<br>
                        <b>Segments:</b> {int(voyage_report['segments'])}<br>
                        <b>Condition Mode:</b> {voyage_report['segment_mode']}<br>
                        <b>Simulation Seed:</b> {int(voyage_report['route_seed'])}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                with report_route_2:

                    voyage_available = parse_json_list(
                        voyage_report.get("available_fuels_json"),
                        [voyage_report.get("current_fuel", "Unknown")]
                    )

                    st.markdown(
                        f"""
                        <div class="card">
                        <h3>⚙️ Vessel Inputs</h3>
                        <b>Vessel:</b> {voyage_report['vessel_type']}<br>
                        <b>Capacity:</b> {float(voyage_report['capacity']):,.0f} tonnes<br>
                        <b>Planned Speed:</b> {float(voyage_report['speed']):.1f} knots<br>
                        <b>Cargo Demand:</b> {float(voyage_report['cargo']):,.0f} tonnes<br>
                        <b>Current Fuel:</b> {voyage_report['current_fuel']}<br>
                        <b>Available Fuels:</b> {', '.join(str(x) for x in voyage_available)}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                vt1, vt2, vt3, vt4 = st.columns(4)

                vt1.metric(
                    "Total Fuel",
                    f"{float(voyage_report['total_fuel']):.2f} t"
                )

                vt2.metric(
                    "Total Cost",
                    f"₹{float(voyage_report['total_cost'])/100000:.2f} L"
                )

                vt3.metric(
                    "Total CO₂",
                    f"{float(voyage_report['total_co2']):.2f} t"
                )

                vt4.metric(
                    "Estimated ETA",
                    f"{float(voyage_report['total_hours']):.1f} h"
                )

                saved_segment_display = parse_json_object(
                    voyage_report.get("segment_display_json"),
                    []
                )

                if saved_segment_display:

                    saved_voyage_df = pd.DataFrame(
                        saved_segment_display
                    )

                    st.markdown(
                        '<div class="section-title">'
                        '📋 Saved Segment-by-Segment Plan'
                        '</div>',
                        unsafe_allow_html=True
                    )

                    st.dataframe(
                        saved_voyage_df,
                        use_container_width=True,
                        hide_index=True
                    )

                    saved_fuel_by_segment = saved_voyage_df[
                        "Fuel (t)"
                    ].astype(float).tolist()

                    saved_co2_by_segment = saved_voyage_df[
                        "CO₂ (t)"
                    ].astype(float).tolist()

                    segment_labels = [
                        f"S{int(x)}"
                        for x in saved_voyage_df["Segment"]
                    ]

                    st.markdown(
                        '<div class="section-title">'
                        '📈 Saved Fuel by Segment'
                        '</div>',
                        unsafe_allow_html=True
                    )

                    segment_fuel_fig = create_3d_bar_chart(
                        segment_labels,
                        saved_fuel_by_segment,
                        "Saved Voyage Fuel by Segment",
                        "Fuel (tonnes)"
                    )

                    st.pyplot(
                        segment_fuel_fig,
                        use_container_width=True
                    )

                    plt.close(
                        segment_fuel_fig
                    )

                    st.markdown(
                        '<div class="section-title">'
                        '🌱 Saved CO₂ by Segment'
                        '</div>',
                        unsafe_allow_html=True
                    )

                    segment_co2_fig = create_3d_bar_chart(
                        segment_labels,
                        saved_co2_by_segment,
                        "Saved Voyage CO₂ by Segment",
                        "CO₂ (tonnes)"
                    )

                    st.pyplot(
                        segment_co2_fig,
                        use_container_width=True
                    )

                    plt.close(
                        segment_co2_fig
                    )

                # Saved route map from the historical route.
                try:

                    import pydeck as pdk

                    route_points_saved = pd.DataFrame({
                        "latitude": np.linspace(
                            float(voyage_report["start_lat"]),
                            float(voyage_report["end_lat"]),
                            50
                        ),
                        "longitude": np.linspace(
                            float(voyage_report["start_lon"]),
                            float(voyage_report["end_lon"]),
                            50
                        )
                    })

                    saved_route_layer = pdk.Layer(
                        "PathLayer",
                        data=[{
                            "path": route_points_saved[
                                ["longitude", "latitude"]
                            ].values.tolist()
                        }],
                        get_path="path",
                        get_width=5,
                        get_color=[72, 224, 160],
                        pickable=False
                    )

                    saved_point_layer = pdk.Layer(
                        "ScatterplotLayer",
                        data=pd.DataFrame({
                            "latitude": [
                                float(voyage_report["start_lat"]),
                                float(voyage_report["end_lat"])
                            ],
                            "longitude": [
                                float(voyage_report["start_lon"]),
                                float(voyage_report["end_lon"])
                            ]
                        }),
                        get_position=["longitude", "latitude"],
                        get_radius=70000,
                        get_fill_color=[255, 80, 80],
                        pickable=False
                    )

                    saved_view = pdk.ViewState(
                        latitude=(
                            float(voyage_report["start_lat"])
                            + float(voyage_report["end_lat"])
                        ) / 2,
                        longitude=(
                            float(voyage_report["start_lon"])
                            + float(voyage_report["end_lon"])
                        ) / 2,
                        zoom=2.5
                    )

                    st.markdown(
                        '<div class="section-title">'
                        '🗺️ Saved Route Map'
                        '</div>',
                        unsafe_allow_html=True
                    )

                    st.pydeck_chart(
                        pdk.Deck(
                            layers=[
                                saved_route_layer,
                                saved_point_layer
                            ],
                            initial_view_state=saved_view
                        ),
                        use_container_width=True
                    )

                except Exception:
                    pass



                saved_sensor_timeline = parse_json_object(voyage_report.get("sensor_timeline_json"), [])
                saved_fuel_plan = parse_json_object(voyage_report.get("fuel_plan_json"), {})
                if saved_sensor_timeline:
                    st.markdown("### 📡 Saved Predicted Sensor & Health Report")
                    sf1, sf2, sf3, sf4 = st.columns(4)
                    sf1.metric("Recommended Start Fuel", f"{float(saved_fuel_plan.get('recommended_start_fuel_t', 0)):.2f} t")
                    sf2.metric("Base Fuel", f"{float(saved_fuel_plan.get('base_requirement_t', 0)):.2f} t")
                    sf3.metric("Weather Reserve", f"{float(saved_fuel_plan.get('weather_reserve_pct', 0)):.1f}%")
                    sf4.metric("Reserve Fuel", f"{float(saved_fuel_plan.get('total_reserve_t', 0)):.2f} t")
                    saved_sensor_df = pd.DataFrame([{
                        "Segment": x.get("segment"), "Weather": x.get("weather"), "Engine Temp (°C)": x.get("engine_temperature_c"),
                        "RPM": x.get("engine_rpm"), "Vibration": x.get("vibration_mm_s"), "Fuel Remaining (t)": x.get("fuel_remaining_t"),
                        "Fuel Margin (t)": x.get("fuel_margin_t"), "Health": x.get("health", {}).get("status", "Legacy")
                    } for x in saved_sensor_timeline])
                    st.dataframe(saved_sensor_df, use_container_width=True, hide_index=True)
                    selected_no = int(selected_segment.get("Segment", 1))
                    saved_sensor = saved_sensor_timeline[min(max(selected_no - 1, 0), len(saved_sensor_timeline) - 1)]
                    saved_health = saved_sensor.get("health", {})
                    rr1, rr2 = st.columns(2)
                    with rr1:
                        st.write(f"**Possible reasons:** {', '.join(saved_health.get('reasons', [])) or 'No abnormal cause identified.'}")
                    with rr2:
                        st.write(f"**Recommended action:** {saved_health.get('primary_action', 'Continue monitoring.')}")

            else:
                    # Legacy voyage records were saved before complete voyage
                    # snapshots existed. Never recalculate them from today's data.
                    st.warning(
                        "This is a legacy voyage record created before the complete "
                        "saved-voyage snapshot feature was added. The original segment "
                        "values below are preserved exactly; route-level details were not "
                        "stored in that older record."
                    )

                    legacy_col1, legacy_col2 = st.columns(2)

                    with legacy_col1:

                        st.markdown(
                            f"""
                            <div class="card">
                            <h3>📋 Selected Saved Segment</h3>
                            <b>ID:</b> {int(selected_segment['ID'])}<br>
                            <b>Date & Time:</b> {selected_segment['Date & Time']}<br>
                            <b>Segment:</b> {int(selected_segment['Segment'])}<br>
                            <b>Distance:</b> {float(selected_segment['Distance (km)']):,.2f} km<br>
                            <b>Weather:</b> {selected_segment['Weather']}<br>
                            <b>Wind:</b> {float(selected_segment['Wind (knots)']):.2f} kn<br>
                            <b>Wave:</b> {float(selected_segment['Wave (m)']):.2f} m<br>
                            <b>Current:</b> {float(selected_segment['Current (knots)']):.2f} kn
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    with legacy_col2:

                        st.markdown(
                            f"""
                            <div class="success-box">
                            <h3>📤 Saved Segment Result</h3>
                            <b>Fuel:</b> {selected_segment['Fuel']}<br>
                            <b>Speed:</b> {float(selected_segment['Speed (knots)']):.1f} kn<br>
                            <b>Fuel Consumption:</b> {float(selected_segment['Fuel (t)']):.4f} t<br>
                            <b>CO₂:</b> {float(selected_segment['CO₂ (t)']):.4f} t<br>
                            <b>Cost:</b> ₹{float(selected_segment['Cost (₹)']):,.2f}<br>
                            <b>Alert:</b> {selected_segment['Alert']}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    legacy_fuel_fig = create_3d_bar_chart(
                        ["Saved Segment Fuel"],
                        [float(selected_segment["Fuel (t)"])],
                        "Saved Segment Fuel",
                        "Fuel (tonnes)"
                    )

                    st.pyplot(
                        legacy_fuel_fig,
                        use_container_width=True
                    )

                    plt.close(
                        legacy_fuel_fig
                    )

else:

    st.info(
        "No dynamic voyage results saved yet."
    )

