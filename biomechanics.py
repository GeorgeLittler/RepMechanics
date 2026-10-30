
import numpy as np

GRAVITY = 9.81


def external_elbow_torque(
    elbow_flexion_deg,
    upper_arm_angle_deg,
    mass_kg,
    forearm_length_m,
):
    """
    Calculate external elbow torque magnitude.

    Assumptions:
    - Movement occurs in a vertical 2D plane.
    - Upper-arm angle is measured from downward vertical.
    - Positive upper-arm angles tilt forward.
    - Elbow flexion is 0 degrees at full extension.
    - The weight acts along the forearm axis.
    - Movement is quasi-static.
    - Arm segment weight is excluded.
    """
    if mass_kg < 0 or forearm_length_m <= 0:
        raise ValueError("Mass must be nonnegative and length positive.")

    forearm_angle = (
        upper_arm_angle_deg + np.asarray(elbow_flexion_deg)
    )

    torque = (
        mass_kg
        * GRAVITY
        * forearm_length_m
        * np.sin(np.radians(forearm_angle))
    )

    return np.abs(torque)


def resistance_profile(
    upper_arm_angle_deg,
    mass_kg=10.0,
    forearm_length_m=0.35,
    max_flexion_deg=150,
):
    """Generate an estimated resistance profile."""

    angles = np.linspace(0, max_flexion_deg, 151)

    torques = external_elbow_torque(
        angles,
        upper_arm_angle_deg,
        mass_kg,
        forearm_length_m,
    )

    peak = np.max(torques)

    normalised = (
        100 * torques / peak
        if peak > 0
        else np.zeros_like(torques)
    )

    return angles, torques, normalised
