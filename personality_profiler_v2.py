import streamlit as st
import random
import plotly.graph_objects as go

def main():
    st.title("Personality Color Profiler")
    st.write("Answer the following questions to find out your personality color.")

    questions = [
        {
            "question": "When working on a team project, I prefer to:",
            "options": {
                "Take charge and lead the team": "Red",
                "Socialize and keep the team motivated": "Yellow",
                "Ensure everyone is comfortable and included": "Green",
                "Focus on details and ensure accuracy": "Blue"
            }
        },
        {
            "question": "In a conflict situation, I tend to:",
            "options": {
                "Assert my position strongly": "Red",
                "Persuade others with enthusiasm": "Yellow",
                "Seek harmony and avoid confrontation": "Green",
                "Analyze all aspects before deciding": "Blue"
            }
        },
        {
            "question": "My decision-making style is best described as:",
            "options": {
                "Quick and decisive": "Red",
                "Optimistic and spontaneous": "Yellow",
                "Careful and methodical": "Green",
                "Logical and data-driven": "Blue"
            }
        },
        {
            "question": "I am motivated by:",
            "options": {
                "Challenges and results": "Red",
                "Recognition and approval": "Yellow",
                "Security and appreciation": "Green",
                "Understanding and accuracy": "Blue"
            }
        },
        {
            "question": "I prefer to communicate:",
            "options": {
                "Directly and to the point": "Red",
                "Enthusiastically and persuasively": "Yellow",
                "Patiently and diplomatically": "Green",
                "Precisely and formally": "Blue"
            }
        },
        {
            "question": "Under stress, I am likely to become:",
            "options": {
                "Impatient and demanding": "Red",
                "Disorganized and overly talkative": "Yellow",
                "Indecisive and overly accommodating": "Green",
                "Critical and withdrawn": "Blue"
            }
        },
        {
            "question": "My greatest strength is:",
            "options": {
                "Leadership and determination": "Red",
                "Enthusiasm and charisma": "Yellow",
                "Supportiveness and reliability": "Green",
                "Attention to detail and thoroughness": "Blue"
            }
        },
        {
            "question": "I handle change by:",
            "options": {
                "Driving it forward": "Red",
                "Embracing it with excitement": "Yellow",
                "Preferring stability and consistency": "Green",
                "Analyzing its implications carefully": "Blue"
            }
        },
        {
            "question": "I value:",
            "options": {
                "Efficiency and achievement": "Red",
                "Fun and interaction": "Yellow",
                "Harmony and cooperation": "Green",
                "Quality and accuracy": "Blue"
            }
        },
        {
            "question": "When learning something new, I prefer:",
            "options": {
                "Getting straight to the point": "Red",
                "Interactive and group activities": "Yellow",
                "A steady and supportive environment": "Green",
                "Detailed explanations and data": "Blue"
            }
        },
    ]

    scores = {"Red": 0, "Yellow": 0, "Green": 0, "Blue": 0}

    for idx, q in enumerate(questions):
        st.subheader(f"Question {idx+1}")
        st.write(q['question'])

        # Use session_state to store the shuffled order
        if f"options_{idx}" not in st.session_state:
            options = list(q["options"].items())
            random.shuffle(options)
            st.session_state[f"options_{idx}"] = options

        # Retrieve the consistent shuffle from session_state
        options = st.session_state[f"options_{idx}"]
        labels = [option[0] for option in options]
        label_to_color = dict(options)

        # Updated radio with a non-empty label and hidden visibility
        option = st.radio("Choose an answer:", labels, key=f"radio_{idx}", label_visibility="hidden")
        selected_color = label_to_color[option]
        scores[selected_color] += 1

    if st.button("Submit"):
        total_questions = len(questions)
        percentages = {color: (score / total_questions) * 100 for color, score in scores.items()}
        sorted_percentages = dict(sorted(percentages.items(), key=lambda item: item[1], reverse=True))
        dominant_color = list(sorted_percentages.keys())[0]

        # Map personality color to actual color
        color_map = {
            "Red": "red",
            "Yellow": "gold",
            "Green": "green",
            "Blue": "blue"
        }
        result_color = color_map[dominant_color]

        # Display result with dynamic color
        st.markdown(
            f'<p style="color:{result_color}; font-size:24px;">Your dominant personality color is: <b>{dominant_color}</b></p>',
            unsafe_allow_html=True
        )

        # Display percentage breakdown
        st.subheader("Percentage Breakdown:")
        for color, percent in sorted_percentages.items():
            st.write(f"**{color}:** {percent:.1f}%")

        # Create a radar chart to visualize the percentages
        categories = list(scores.keys())
        values = [percentages[color] for color in categories]
        values += values[:1]  # Repeat the first value to close the circle

        fig = go.Figure(
            data=[
                go.Scatterpolar(
                    r=values,
                    theta=categories + [categories[0]],
                    fill='toself',
                    name='Personality Traits'
                )
            ],
            layout=go.Layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100]
                    )
                ),
                showlegend=False
            )
        )
        st.plotly_chart(fig)

        # Detailed descriptions
        descriptions = {
            "Red": "Leadership Red: You are driven and assertive. You take charge and value efficiency and results.",
            "Yellow": "Sunshine Yellow: You are enthusiastic and sociable. You inspire others with your optimism and enjoy interacting with people.",
            "Green": "Peaceful Green: You are supportive and reliable. You value harmony and work well in team settings.",
            "Blue": "Analytical Blue: You are precise and detail-oriented. You strive for accuracy and quality in your work."
        }

        st.subheader("Personality Descriptions:")
        for color in sorted_percentages:
            st.write(f"**{color}:** {descriptions[color]}")

if __name__ == "__main__":
    main()
