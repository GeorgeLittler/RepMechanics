
# RepMechanics

**Explore and compare resistance profiles of strength-training exercises using biomechanics and AI.**

Built for the Nebius × NVIDIA Global AI Hackathon 2026.

## Overview

RepMechanics is an interactive biomechanics application that estimates how external joint torque changes throughout the range of motion of resistance-training exercises.

The current prototype focuses on four biceps curl variations:

- Standing Curl
- Spider Curl
- Preacher Curl
- Incline Curl

Users can adjust exercise geometry, external load and elbow-to-load distance, then compare the resulting resistance profiles.

NVIDIA Nemotron interprets the calculated results and explains how mechanical resistance differs between exercises.

## Features

- Interactive exercise comparison
- Adjustable upper-arm orientation
- Customisable external load and arm measurements
- External elbow torque visualisation
- Normalised resistance-profile comparisons
- Peak torque and joint-angle calculations
- AI biomechanics interpretation using NVIDIA Nemotron

## How It Works

### 1. Biomechanics Engine

RepMechanics uses a simplified quasi-static 2D model.

External elbow torque is calculated using:

    torque = mass * gravity * distance * abs(sin(angle))

The angle represents the forearm's orientation relative to gravity.

The engine generates torque estimates throughout the elbow's range of motion.

### 2. Visualisation

Streamlit and Plotly display the resulting torque curves, allowing users to compare how exercise geometry changes the distribution of external resistance.

### 3. NVIDIA Nemotron Integration

RepMechanics uses NVIDIA Nemotron 3.5 Lightning through Nebius Token Factory.

The application sends structured biomechanics results to Nemotron, which explains the differences between exercises.

The physics calculations are performed in Python. Nemotron interprets the results rather than generating the numerical curves.

## Technology Stack

- Python
- NumPy
- Streamlit
- Plotly
- NVIDIA Nemotron 3.5 Lightning
- Nebius Token Factory
- OpenAI-compatible API

## Installation

Clone the repository and enter its directory.

Create a virtual environment:

    python3 -m venv .venv
    source .venv/bin/activate

Install dependencies:

    pip install -r requirements.txt

Create a `.env` file using `.env.example` as a template.

Add your Nebius Token Factory API key and model configuration.

Run the application:

    streamlit run app.py

## Limitations

The current MVP uses illustrative exercise geometries rather than measured human movement.

It assumes:
- A quasi-static movement
- Two-dimensional motion
- A constant distance between the elbow and load
- A fixed upper-arm orientation during each exercise
- Gravitational loading from a free weight

It does not currently account for arm segment weight, movement acceleration, three-dimensional motion or individual muscle forces.

Results are theoretical estimates, not experimentally validated measurements.

## Future Development

RepMechanics is an ongoing project.

Planned improvements include:

- Smartphone video analysis
- Computer vision joint tracking
- Automatic exercise recognition
- Movement-specific geometry estimation
- More exercise variations
- Improved biomechanics modelling
- Validation against recorded movement data

## Licence

MIT License.
