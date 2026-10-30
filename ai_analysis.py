
import os
import json

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def analyse_comparison(
    exercise_a,
    exercise_b,
    angles_a,
    torques_a,
    angles_b,
    torques_b,
):
    """Interpret calculated resistance profiles using Nemotron."""

    client = OpenAI(
        api_key=os.getenv("NEBIUS_API_KEY"),
        base_url=os.getenv("NEBIUS_BASE_URL"),
        timeout=30.0,
    )

    def summarise_profile(angles, torques):
        # Sample every 15 degrees to keep token usage low.
        samples = [
            {
                "elbow_flexion_deg": round(float(angle), 1),
                "external_torque_nm": round(float(torque), 2),
            }
            for angle, torque in zip(angles, torques)
            if round(float(angle)) % 15 == 0
        ]

        peak_index = int(torques.argmax())

        return {
            "peak_torque_nm": round(float(torques[peak_index]), 2),
            "peak_flexion_deg": round(float(angles[peak_index]), 1),
            "samples": samples,
        }

    comparison = {
        "exercise_a": {
            "name": exercise_a,
            **summarise_profile(angles_a, torques_a),
        },
        "exercise_b": {
            "name": exercise_b,
            **summarise_profile(angles_b, torques_b),
        },
    }

    response = client.chat.completions.create(
        model=os.getenv("NEBIUS_MODEL"),
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a precise biomechanics analysis assistant. "
                    "Interpret the numerical data supplied to you. "
                    "Do not invent measurements or biomechanical findings. "
                    "At 90 degrees of elbow flexion with a vertically "
                    "oriented upper arm, the forearm is approximately "
                    "horizontal. "
                    "External elbow torque is not equivalent to muscle "
                    "activation or internal muscle force. "
                    "The data represents a simplified, quasi-static "
                    "two-dimensional physics model, not experimental "
                    "measurements. "
                    "Explain which exercise has higher external torque "
                    "in the early, middle, and late portions of the "
                    "movement, using the supplied numerical samples. "
                    "If the curves cross, mention approximately where. "
                    "Avoid making unsupported training recommendations. "
                    "Keep the explanation under 250 words."
                ),
            },
            {
                "role": "user",
                "content": (
                    "Compare the following calculated resistance "
                    "profiles:\n\n"
                    + json.dumps(comparison, indent=2)
                ),
            },
        ],
        max_tokens=800,
        extra_body={
            "chat_template_kwargs": {
                "enable_thinking": False
            }
        },
    )

    return response.choices[0].message.content
