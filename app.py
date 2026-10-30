
import streamlit as st
import numpy as np
import plotly.graph_objects as go

from biomechanics import resistance_profile
from ai_analysis import analyse_comparison


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="RepMechanics",
    page_icon="💪",
    layout="wide",
)

st.title("💪 RepMechanics")
st.subheader("Resistance Profile Comparison")

st.write(
    "Explore how exercise geometry changes external elbow "
    "torque throughout the range of motion of different "
    "biceps curl variations."
)


# --------------------------------------------------
# Exercise configurations
# --------------------------------------------------

# These angles represent illustrative upper-arm
# orientations relative to vertically downward.
#
# Positive = upper arm tilted forward
# Negative = upper arm tilted backward
#
# These are not experimentally measured values.

EXERCISES = {
    "Standing Curl": 0,
    "Spider Curl": 55,
    "Preacher Curl": 45,
    "Incline Curl": -20,
}


# --------------------------------------------------
# Exercise selection
# --------------------------------------------------

col1, col2 = st.columns(2)

with col1:
    st.header("Exercise A")

    exercise_a = st.selectbox(
        "Select exercise A",
        list(EXERCISES.keys()),
        index=0,
    )

    angle_a = st.slider(
        "Upper-arm angle A (°)",
        min_value=-60,
        max_value=90,
        value=EXERCISES[exercise_a],
        key=f"angle_a_{exercise_a}",
    )

with col2:
    st.header("Exercise B")

    exercise_b = st.selectbox(
        "Select exercise B",
        list(EXERCISES.keys()),
        index=2,
    )

    angle_b = st.slider(
        "Upper-arm angle B (°)",
        min_value=-60,
        max_value=90,
        value=EXERCISES[exercise_b],
        key=f"angle_b_{exercise_b}",
    )


# --------------------------------------------------
# Load and body measurements
# --------------------------------------------------

st.divider()
st.header("Load & Body Measurements")

mass = st.slider(
    "External load (kg)",
    min_value=1,
    max_value=40,
    value=10,
)

length = st.slider(
    "Elbow-to-load distance (m)",
    min_value=0.20,
    max_value=0.50,
    value=0.35,
    step=0.01,
)

normalised = st.toggle(
    "Show normalised resistance (%)",
    value=False,
)


# --------------------------------------------------
# Calculate resistance profiles
# --------------------------------------------------

angles_a, torques_a, percentages_a = resistance_profile(
    upper_arm_angle_deg=angle_a,
    mass_kg=mass,
    forearm_length_m=length,
)

angles_b, torques_b, percentages_b = resistance_profile(
    upper_arm_angle_deg=angle_b,
    mass_kg=mass,
    forearm_length_m=length,
)

values_a = percentages_a if normalised else torques_a
values_b = percentages_b if normalised else torques_b


# --------------------------------------------------
# Resistance profile visualisation
# --------------------------------------------------

st.divider()
st.header("Resistance Profile Visualisation")

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=angles_a,
        y=values_a,
        mode="lines",
        name=exercise_a,
        line=dict(
            color="#636EFA",
            width=3,
        ),
    )
)

fig.add_trace(
    go.Scatter(
        x=angles_b,
        y=values_b,
        mode="lines",
        name=exercise_b,
        line=dict(
            color="#EF553B",
            width=3,
        ),
    )
)

fig.update_layout(
    title="External Elbow Torque Across Range of Motion",
    xaxis_title="Elbow Flexion (degrees)",
    yaxis_title=(
        "Normalised External Torque (%)"
        if normalised
        else "External Elbow Torque (Nm)"
    ),
    hovermode="x unified",
    template="plotly_white",
    height=500,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
    ),
)

st.plotly_chart(
    fig,
    use_container_width=True,
)


# --------------------------------------------------
# Peak torque comparison
# --------------------------------------------------

st.header("Comparison Results")

peak_a = int(np.argmax(torques_a))
peak_b = int(np.argmax(torques_b))

result_col1, result_col2 = st.columns(2)

with result_col1:
    st.metric(
        f"{exercise_a} — Peak Torque",
        f"{torques_a[peak_a]:.2f} Nm",
    )

    st.write(
        f"Peak at approximately "
        f"{angles_a[peak_a]:.0f}° elbow flexion"
    )

with result_col2:
    st.metric(
        f"{exercise_b} — Peak Torque",
        f"{torques_b[peak_b]:.2f} Nm",
    )

    st.write(
        f"Peak at approximately "
        f"{angles_b[peak_b]:.0f}° elbow flexion"
    )


# --------------------------------------------------
# Model assumptions and limitations
# --------------------------------------------------

st.info(
    "This application uses a simplified, quasi-static "
    "two-dimensional biomechanics model. Exercise presets "
    "use illustrative upper-arm orientations rather than "
    "measured exercise geometry. External elbow torque "
    "is not equivalent to muscle force or muscle activation. "
    "Arm segment weight, acceleration, and three-dimensional "
    "movement are not included."
)

with st.expander("How are these resistance profiles calculated?"):
    st.markdown(
        """
        RepMechanics estimates the external torque produced
        by a free weight about the elbow joint.

        The basic relationship is:

        $$
        \\tau = mgL|\\sin(\\phi)|
        $$

        Where:

        - **τ:** External elbow torque (Nm)
        - **m:** External load mass (kg)
        - **g:** Gravitational acceleration (9.81 m/s²)
        - **L:** Distance from elbow to load centre of mass (m)
        - **φ:** Forearm orientation relative to gravity

        The forearm orientation is estimated from the
        elbow flexion angle and upper-arm orientation.

        Changing the upper-arm angle shifts the
        calculated resistance profile.

        **Important limitations:**

        - The model assumes slow, controlled movement.
        - It does not calculate internal muscle forces.
        - It assumes the load acts at a fixed distance
          along the forearm.
        - The exercise configurations are illustrative.
        - Actual bench angle and upper-arm orientation
          may differ.
        """
    )


# --------------------------------------------------
# NVIDIA Nemotron AI analysis
# --------------------------------------------------

st.divider()
st.header("AI Biomechanics Analysis")

st.write(
    "NVIDIA Nemotron analyses the calculated resistance "
    "profiles and explains how external mechanical demand "
    "changes throughout the movement."
)

st.caption(
    "Powered by NVIDIA Nemotron 3.5 Lightning "
    "through Nebius Token Factory."
)

if st.button(
    "Analyse with NVIDIA Nemotron",
    type="primary",
):
    with st.spinner("Nemotron is analysing your comparison..."):
        try:
            analysis = analyse_comparison(
                exercise_a=exercise_a,
                exercise_b=exercise_b,
                angles_a=angles_a,
                torques_a=torques_a,
                angles_b=angles_b,
                torques_b=torques_b,
            )

            if analysis:
                st.success("Analysis complete")
                st.markdown(analysis)
            else:
                st.warning(
                    "Nemotron returned an empty response."
                )

        except Exception as error:
            st.error(
                f"AI analysis failed: {error}"
            )


# --------------------------------------------------
# Footer
# --------------------------------------------------

st.divider()

st.caption(
    "RepMechanics | Nebius × NVIDIA Global AI Hackathon 2026"
)
