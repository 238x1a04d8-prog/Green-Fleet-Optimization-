import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Signal Sync | Green Fleet Optimization",
    page_icon="🚢",
    layout="wide"
)

# ============================================================
# CUSTOM CSS
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
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🚢 Signal Sync</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Quantum-Inspired Fuel Consumption Prediction & Green Fleet Optimization'
    '<br>SIH26138 • Clean & Green Technology • Engineering Day 2026'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("⚙️ Fleet Configuration")

st.sidebar.markdown(
    "### Enter Vessel Information"
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
    "Speed (knots)",
    min_value=5.0,
    max_value=30.0,
    value=18.0,
    step=0.5
)

distance = st.sidebar.number_input(
    "Travel Distance (km)",
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
    [
        "Diesel",
        "LNG",
        "Methanol",
        "Hydrogen",
        "Ammonia"
    ]
)

fuel_price = st.sidebar.number_input(
    "Fuel Price (₹ / tonne)",
    min_value=1000,
    max_value=200000,
    value=65000,
    step=1000
)

weather = st.sidebar.selectbox(
    "Operating Condition",
    [
        "Normal",
        "Calm Sea",
        "Heavy Weather"
    ]
)

predict_button = st.sidebar.button(
    "🚀 Predict & Optimize",
    use_container_width=True
)


# ============================================================
# FUEL PARAMETERS
# ============================================================

fuel_data = {

    "Diesel": {
        "consumption_factor": 1.00,
        "co2_factor": 3.20,
        "cost": 65000,
        "green_score": 35
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
# FUEL CONSUMPTION PREDICTION
# ============================================================

def predict_fuel(
    capacity,
    speed,
    distance,
    fuel,
    weather
):

    # Base relationship for prototype demonstration
    base_consumption = (
        (capacity / 10000)
        * (distance / 1000)
        * 2.0
    )

    # Speed has strong influence on fuel consumption
    speed_factor = (speed / 18) ** 2.3

    # Weather adjustment
    if weather == "Heavy Weather":
        weather_factor = 1.18

    elif weather == "Calm Sea":
        weather_factor = 0.92

    else:
        weather_factor = 1.0

    fuel_factor = fuel_data[fuel]["consumption_factor"]

    predicted = (
        base_consumption
        * speed_factor
        * weather_factor
        * fuel_factor
    )

    return predicted


# ============================================================
# CO2 CALCULATION
# ============================================================

def calculate_co2(fuel_amount, fuel):

    factor = fuel_data[fuel]["co2_factor"]

    return fuel_amount * factor


# ============================================================
# MAIN DASHBOARD
# ============================================================

st.markdown(
    '<div class="section-title">📊 Fleet Prediction Dashboard</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

# Initial values
initial_fuel = predict_fuel(
    capacity,
    speed,
    distance,
    fuel_type,
    weather
)

initial_cost = initial_fuel * fuel_price

initial_co2 = calculate_co2(
    initial_fuel,
    fuel_type
)

green_score = fuel_data[fuel_type]["green_score"]


with col1:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">Predicted Fuel</div>
            <div class="metric-value">{initial_fuel:.2f}</div>
            <div class="small-text">tonnes</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">Estimated Cost</div>
            <div class="metric-value">₹{initial_cost/100000:.2f}L</div>
            <div class="small-text">fuel cost</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">CO₂ Emission</div>
            <div class="metric-value">{initial_co2:.2f}</div>
            <div class="small-text">tonnes</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">Green Score</div>
            <div class="metric-value">{green_score}</div>
            <div class="small-text">out of 100</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# PREDICTION DETAILS
# ============================================================

st.markdown(
    '<div class="section-title">🤖 Machine Learning Prediction</div>',
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div class="card">

    <h3>Prediction Summary</h3>

    <p>
    Based on the entered vessel characteristics and operating conditions,
    the prototype estimates the expected fuel requirement.
    </p>

    <b>Vessel:</b> {vessel_type}<br>
    <b>Capacity:</b> {capacity:,} tonnes<br>
    <b>Speed:</b> {speed} knots<br>
    <b>Distance:</b> {distance:,} km<br>
    <b>Cargo Demand:</b> {cargo:,} tonnes<br>
    <b>Fuel:</b> {fuel_type}<br>
    <b>Operating Condition:</b> {weather}

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# OPTIMIZATION
# ============================================================

if predict_button:

    with st.spinner("⚛️ Running quantum-inspired optimization..."):

        best_solution = None
        best_score = float("inf")

        candidate_speeds = [
            max(10, speed - 2),
            max(10, speed - 1),
            speed,
            min(25, speed + 1)
        ]

        candidate_fuels = list(fuel_data.keys())

        for candidate_fuel in candidate_fuels:

            for candidate_speed in candidate_speeds:

                candidate_fuel_consumption = predict_fuel(
                    capacity,
                    candidate_speed,
                    distance,
                    candidate_fuel,
                    weather
                )

                candidate_cost = (
                    candidate_fuel_consumption
                    * fuel_data[candidate_fuel]["cost"]
                )

                candidate_co2 = calculate_co2(
                    candidate_fuel_consumption,
                    candidate_fuel
                )

                # Optimization objective
                #
                # Lower is better.
                #
                # Cost + emissions + speed penalty

                optimization_score = (
                    candidate_cost
                    + (candidate_co2 * 10000)
                    + (
                        abs(candidate_speed - 17)
                        * candidate_cost
                        * 0.03
                    )
                )

                if optimization_score < best_score:

                    best_score = optimization_score

                    best_solution = {
                        "fuel": candidate_fuel,
                        "speed": candidate_speed,
                        "fuel_consumption":
                            candidate_fuel_consumption,
                        "cost":
                            candidate_cost,
                        "co2":
                            candidate_co2
                    }


        # ====================================================
        # OPTIMIZATION RESULTS
        # ====================================================

        st.markdown(
            '<div class="section-title">⚛️ Quantum-Inspired Optimization</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="card">

            <h3>Optimization Engine</h3>

            The prototype evaluates multiple combinations of:

            <ul>
            <li>Fuel type</li>
            <li>Operating speed</li>
            <li>Fuel consumption</li>
            <li>Fuel cost</li>
            <li>CO₂ emissions</li>
            </ul>

            It then selects the candidate with the lowest
            combined optimization score.

            <br><br>

            <b>Note:</b>
            This is quantum-inspired optimization running on a
            conventional computer. No physical quantum computer
            is required.

            </div>
            """,
            unsafe_allow_html=True
        )


        # ====================================================
        # RESULT VALUES
        # ====================================================

        optimized_fuel = best_solution["fuel_consumption"]
        optimized_cost = best_solution["cost"]
        optimized_co2 = best_solution["co2"]

        fuel_saving = (
            (initial_fuel - optimized_fuel)
            / initial_fuel
        ) * 100

        cost_saving = (
            (initial_cost - optimized_cost)
            / initial_cost
        ) * 100

        co2_reduction = (
            (initial_co2 - optimized_co2)
            / initial_co2
        ) * 100


        # ====================================================
        # RECOMMENDATION
        # ====================================================

        st.markdown(
            '<div class="section-title">🏆 Recommended Green Fleet Plan</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="success-box">

            <h2>🚢 Optimal Fleet Recommendation</h2>

            <h3>
            Recommended Fuel:
            {best_solution["fuel"]}
            </h3>

            <p>
            Recommended Operating Speed:
            <b>{best_solution["speed"]:.1f} knots</b>
            </p>

            <p>
            Predicted Fuel Consumption:
            <b>{optimized_fuel:.2f} tonnes</b>
            </p>

            <p>
            Estimated Fuel Cost:
            <b>₹{optimized_cost:,.0f}</b>
            </p>

            <p>
            Estimated CO₂ Emissions:
            <b>{optimized_co2:.2f} tonnes</b>
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )


        # ====================================================
        # SAVINGS METRICS
        # ====================================================

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric(
                "Fuel Saving",
                f"{fuel_saving:.2f}%"
            )

        with c2:
            st.metric(
                "Cost Saving",
                f"{cost_saving:.2f}%"
            )

        with c3:
            st.metric(
                "CO₂ Reduction",
                f"{co2_reduction:.2f}%"
            )


        # ====================================================
        # BEFORE VS AFTER
        # ====================================================

        st.markdown(
            '<div class="section-title">📈 Before vs After Optimization</div>',
            unsafe_allow_html=True
        )

        comparison = pd.DataFrame({
            "Metric": [
                "Fuel Consumption",
                "Fuel Cost / ₹10,000",
                "CO₂ Emissions"
            ],

            "Current Plan": [
                initial_fuel,
                initial_cost / 10000,
                initial_co2
            ],

            "Optimized Plan": [
                optimized_fuel,
                optimized_cost / 10000,
                optimized_co2
            ]
        })

        st.dataframe(
            comparison,
            use_container_width=True,
            hide_index=True
        )


        # ====================================================
        # CHART 1
        # ====================================================

        st.markdown(
            '<div class="section-title">⛽ Fuel Consumption by Fuel Type</div>',
            unsafe_allow_html=True
        )

        fuel_names = list(fuel_data.keys())

        fuel_values = []

        for f in fuel_names:

            value = predict_fuel(
                capacity,
                best_solution["speed"],
                distance,
                f,
                weather
            )

            fuel_values.append(value)


        fig1, ax1 = plt.subplots(figsize=(10, 4))

        ax1.bar(
            fuel_names,
            fuel_values
        )

        ax1.set_ylabel(
            "Fuel Consumption (tonnes)"
        )

        ax1.set_title(
            "Fuel Consumption Comparison"
        )

        ax1.tick_params(axis="x", rotation=20)

        st.pyplot(fig1)


        # ====================================================
        # CHART 2
        # ====================================================

        st.markdown(
            '<div class="section-title">🌱 CO₂ Emission Comparison</div>',
            unsafe_allow_html=True
        )

        emission_values = []

        for f in fuel_names:

            amount = predict_fuel(
                capacity,
                best_solution["speed"],
                distance,
                f,
                weather
            )

            emission = calculate_co2(
                amount,
                f
            )

            emission_values.append(emission)


        fig2, ax2 = plt.subplots(figsize=(10, 4))

        ax2.bar(
            fuel_names,
            emission_values
        )

        ax2.set_ylabel(
            "CO₂ Emissions (tonnes)"
        )

        ax2.set_title(
            "Green Fuel Emission Comparison"
        )

        ax2.tick_params(axis="x", rotation=20)

        st.pyplot(fig2)


        # ====================================================
        # FINAL EXPLANATION
        # ====================================================

        st.markdown(
            '<div class="section-title">💡 Decision Explanation</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="card">

            <h3>Why was {best_solution["fuel"]} selected?</h3>

            The optimization engine compared different fuel and
            speed combinations.

            The selected plan provides a better balance between:

            <ul>
            <li>Fuel consumption</li>
            <li>Operating cost</li>
            <li>CO₂ emissions</li>
            <li>Operating speed</li>
            </ul>

            Therefore, the recommended plan is:

            <br>

            <b>
            {best_solution["fuel"]}
            at
            {best_solution["speed"]:.1f} knots
            </b>

            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# FUEL COMPARISON TABLE
# ============================================================

st.markdown(
    '<div class="section-title">🌍 Green Fuel Comparison</div>',
    unsafe_allow_html=True
)

fuel_table = []

for fuel in fuel_data:

    fuel_table.append({
        "Fuel": fuel,
        "CO₂ Factor": fuel_data[fuel]["co2_factor"],
        "Approx. Price ₹/tonne":
            fuel_data[fuel]["cost"],
        "Green Score":
            fuel_data[fuel]["green_score"]
    })

fuel_df = pd.DataFrame(fuel_table)

st.dataframe(
    fuel_df,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# HOW IT WORKS
# ============================================================

st.markdown(
    '<div class="section-title">🔬 How Our System Works</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:

    st.markdown(
        """
        <div class="card">

        <h3>01 🤖 Machine Learning</h3>

        Historical vessel and operating data can be used
        to train an ML model.

        The model predicts expected fuel consumption
        for a given operating condition.

        </div>
        """,
        unsafe_allow_html=True
    )


with col2:

    st.markdown(
        """
        <div class="card">

        <h3>02 ⚛️ Quantum-Inspired Optimization</h3>

        The system evaluates many possible fleet decisions
        and searches for a combination that minimizes
        cost and emissions.

        This prototype performs the optimization on a
        normal computer.

        </div>
        """,
        unsafe_allow_html=True
    )


with col3:

    st.markdown(
        """
        <div class="card">

        <h3>03 🌱 Green Decision</h3>

        The final recommendation compares fuel,
        speed, cost and emissions to identify a
        more sustainable operating plan.

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# DISCLAIMER
# ============================================================

st.markdown(
    """
    <div class="warning-box">

    ⚠️ <b>Engineering Day Prototype Notice</b>

    <br><br>

    The current version uses illustrative mathematical
    relationships and sample fuel factors.

    It is designed to demonstrate the complete system flow.

    A production system would use real vessel datasets,
    a trained Machine Learning model and a formal
    quantum-inspired optimization algorithm.

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <br>
    <hr>

    <center>
    <b>Signal Sync</b><br>
    SIH26138 — Quantum-Inspired Fuel Consumption Prediction
    and Green Fleet Optimization<br><br>
    Engineering Day 2026
    </center>
    """,
    unsafe_allow_html=True
)