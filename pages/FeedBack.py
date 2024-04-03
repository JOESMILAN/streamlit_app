import streamlit as st

# Function to save feedback
def save_feedback(feedback):
    with open("feedback.txt", "a") as f:
        f.write(feedback + "\n")
    st.success("🚀 Feedback saved successfully! Thank you! 🌟")

def main():
    # Add a title and GIF with reduced size
    st.image("redheadphone.gif")  # Adjust width as needed
    st.title("Feedback Form 📝")

    # Create a text area for providing feedback
    feedback = st.text_area("Provide Feedback 📢")

    # Button to save feedback
    if st.button("Submit Feedback ✔️"):
        if feedback:
            save_feedback(feedback)
        else:
            st.warning("⚠️ Please provide feedback before submitting. ⚠️")

if __name__ == "__main__":
    main()
