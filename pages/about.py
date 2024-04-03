import streamlit as st

# Header and Introduction
st.title("💼 Expense Tracker Dashboard 💰")
st.write("Welcome to the Expense Tracker Dashboard! 📊 Use the sidebar to navigate. 🚀")

# About Page
st.title("About Expense Tracker ℹ️")
st.image("check.gif", use_column_width=True)  # Replace "expense_image.jpg" with your image file
st.markdown("---")

st.write(
    """
This dashboard is designed to help you track and manage your expenses efficiently. 💸 You can upload your bank statements, categorize expenses, visualize spending habits, and more.

### Key Features:
- *Expense Categorization:* Categorize your expenses as fixed or variable to better understand your spending habits. 📋
- *Interactive Visualizations:* Explore your expenses through interactive visualizations like pie charts, bar graphs, and box plots. 📊
- *Data Analysis:* Dive deeper into your spending patterns with summary statistics, total expenses, and remaining balance calculations. 📈

### How to Use:
1. Upload your bank statements using the sidebar option.
2. Categorize your expenses as fixed or variable.
3. Visualize your expenses by category or type.
4. Analyze your spending patterns and track your remaining balance.

Feel free to explore and manage your expenses efficiently! 😊
""")
