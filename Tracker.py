import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from streamlit_extras.switch_page_button import switch_page
from datetime import datetime
from statementParser import BankStatement

# Initialize session state if not already initialized
if 'categorized_df' not in st.session_state or st.session_state['categorized_df'] is None:
    st.session_state['categorized_df'] = pd.DataFrame()

if 'fixed_exp' not in st.session_state:
    st.session_state['fixed_exp'] = set()

if 'variable_exp' not in st.session_state:
    st.session_state['variable_exp'] = set()

# Define your page configurations
st.set_page_config(
    page_title="Expense Tracker",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Function to set theme
def set_theme(theme):
    if theme == 'Dark':
        st.markdown(
            """
            <style>
            .streamlit-container {
                color: white;
                background-color: #1E1E1E;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <style>
            .streamlit-container {
                color: black;
                background-color: white;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

# Function to display About page
def about():
    st.title("About Expense Tracker ℹ️")
    st.write("Welcome to Expense Tracker! 💰")
    st.write("This application helps you track your expenses and visualize your spending habits. 📊")
    st.write("Features include:")
    st.write("- Uploading bank statements in PDF format 📄")
    st.write("- Categorizing expenses as fixed or variable 📋")
    st.write("- Adding new expenses manually 🛒")
    st.write("- Displaying total expenses and remaining balance 💸")
    st.write("- Visualizing expenses by category 📈")
    st.write("- Choosing between light and dark themes 🌓")
    st.write("Feel free to explore and manage your expenses efficiently! 😊")
    st.write("Made with ❤️ by [Your Name]")
    st.write("Find the source code on [GitHub](https://github.com/yourusername/expense-tracker)")

# Title
st.title('Personal Expense Tracker 💼')

# Date input for start and end dates
start_date = st.date_input('Start Date', datetime.now().date().replace(month=1, day=1))
end_date = st.date_input('End Date')

# Store start and end dates in session state
st.session_state['start_date'] = start_date
st.session_state['end_date'] = end_date

# Select bank option
bank_option = st.selectbox("Select Bank 🏦", ("Kotak Mahindhra Bank","State Bank Of India","Bank Of India","Indian Overseas Bank"))

# Button to proceed to the next step
if st.button('Next ➡️'):
    st.session_state['selected_bank'] = bank_option
    switch_page("Create_Categories")

# Display selected bank if available in session state
if 'selected_bank' in st.session_state:
    selected_bank = st.session_state['selected_bank']
    st.write(f"Selected Bank: {selected_bank}")

# Add file upload option
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

# Parse statement and display expenses and amounts
if uploaded_file is not None:
    statement_parser = BankStatement(uploaded_file)
    df = statement_parser.parse_statement_as_df()

    st.write("Expenses:")
    st.write(df['Description'])

    st.write("Amounts:")
    st.write(df['Debit'])

    # Button to navigate to the visualization page
    if st.button("Visualize 📊"):
        switch_page("Visualize")

    # Store parsed data in session state
    st.session_state['categorized_df'] = df

# Done button to finish categorizing expenses
if st.button("Done ✅"):
    # Validate fixed and variable expenses
    fixed_exp = st.session_state['fixed_exp']
    variable_exp = st.session_state['variable_exp']

    if not fixed_exp and not variable_exp:
        st.error("Both Fixed and Variable expenses are empty. Please categorize your expenses properly.")
    elif fixed_exp & variable_exp:
        st.error("Fixed and Variable expenses cannot have common values between them. Please review your categorization.")
    else:
        switch_page("Home")

# Dropdown menu for selecting categories
categories = ["Groceries", "Utilities", "Transportation", "Entertainment", "Healthcare", "Education", "Other"]
selected_category = st.selectbox("Select a category 📋", categories)

# Add button to assign selected category to expenses
if st.button("Assign Category ✔️"):
    # Assign selected category to expenses
    selected_expenses = st.multiselect("Select expenses to assign category", df['Description'].unique())
    if selected_category:
        if selected_category == "Fixed":
            st.session_state['fixed_exp'].update(selected_expenses)
        elif selected_category == "Variable":
            st.session_state['variable_exp'].update(selected_expenses)
        st.success("Category assigned successfully!")

# Load existing data or create new dataframe
def load_data():
    return pd.read_csv("Expenses2.csv")  # Replace "Expenses2.csv" with your dataset filename

data = load_data()  # Load the DataFrame

# Add opening balance
with st.sidebar:
    st.subheader('Set Opening Balance 💰')
    opening_balance = st.number_input('Opening Balance', value=0.00, step=1.00)

# Function to add a new expense
def add_expense(date, category, amount):
    global data

    if opening_balance == 0:
        st.error("Please enter the opening balance before adding an expense.")
    else:
        new_expense = pd.DataFrame({'Date': [date], 'Category': [category], 'Amount': [amount]})
        data = pd.concat([data, new_expense], ignore_index=True)
        st.session_state.display_all_expenses = False
        st.success('Expense added successfully!')

# Add expense section
with st.sidebar:
    st.subheader('Add New Expense 🛒')
    date_expense = st.date_input('Date (Expense)', key='date_expense')
    category_expense = st.selectbox('Category (Expense)', ['Food', 'Transportation', 'Shopping', 'Utilities', 'Entertainment', 'Others'], key='category_expense')
    amount_expense = st.number_input('Amount (Expense)', value=0.00, step=1.00, key='amount_expense')

    if st.button('Add Expense ➕'):
        add_expense(date_expense, category_expense, amount_expense)

# Button to add more expenses
if st.sidebar.button('Add More Expenses ➕'):
    with st.sidebar.expander("Add Another Expense"):
        date_new_expense = st.date_input('Date (New Expense)', key='date_new_expense')
        category_new_expense = st.selectbox('Category (New Expense)', ['Food', 'Transportation', 'Shopping', 'Utilities', 'Entertainment', 'Others'], key='category_new_expense')
        amount_new_expense = st.number_input('Amount (New Expense)', value=0.00, step=1.00, key='amount_new_expense')
        if st.button('Add New Expense ➕'):
            add_expense(date_new_expense, category_new_expense, amount_new_expense)

# Button to display all expenses
if st.button('Display All Expenses 📄'):
    st.session_state.display_all_expenses = True

# Show current data
if not st.session_state.get('display_all_expenses', False):
    st.subheader('Current Expenses')
    st.write(data.tail())
else:
    st.subheader('All Expenses')
    st.write(data)

# Show total expenses
st.subheader('Total Expenses 💸')
total_expenses = data['Amount'].sum()
st.write(f'Total expenses: ${total_expenses:.2f}')

# Calculate and display remaining balance
if opening_balance != 0:
    remaining_balance = opening_balance - total_expenses
    st.subheader('Remaining Balance 💰')
    st.write(f'Remaining balance: ${remaining_balance:.2f}')

# Button to visualize
if st.button('Visualize 📊'):
    # Visualization: Expenses by Category
    st.subheader('Expenses by Category 📊')
    fig = px.pie(data, names='Category', title='Expenses by Category')
    st.plotly_chart(fig, use_container_width=True)
    # Visualization: Stock Chart
    st.subheader('Stock Chart 📈')
    fig = go.Figure(data=[go.Candlestick(x=data['Date'],
                    open=data['Amount'],
                    high=data['Amount'],
                    low=data['Amount'],
                    close=data['Amount'])])
    st.plotly_chart(fig)

    # Visualization: Function Plot
    st.subheader('Function Plot 📈')
    x = np.linspace(-10, 10, 100)
    y = np.sin(x)
    fig = px.line(x=x, y=y, labels={'x': 'X', 'y': 'sin(X)'}, title='Sin Function')
    st.plotly_chart(fig)

    # Visualization: Waterfall Chart
    st.subheader('Waterfall Chart 📉')
    fig = go.Figure(go.Waterfall(
        name="20", orientation="v",
        measure=["relative", "relative", "total", "relative", "relative", "total"],
        x=["Sales", "Consulting", "Net revenue", "Purchases", "Other expenses", "Profit before tax"],
        textposition="outside",
        text=["+60", "+80", "", "-40", "-20", "Total"],
        y=[60, 80, 0, -40, -20, 0],
        connector={"line":{"color":"rgb(63, 63, 63)"}},
    ))
    st.plotly_chart(fig)

    # Animated 3D scatter plot
    st.subheader('Animated 3D Scatter Plot of Expenses over Time 📈')
    fig = px.scatter_3d(data, x='Date', y='Category', z='Amount', color='Category',
                        animation_frame='Date', range_z=[0, data['Amount'].max()],
                        title='Animated 3D Scatter Plot of Expenses')
    fig.update_layout(scene=dict(zaxis=dict(title='Amount')))
    st.plotly_chart(fig, use_container_width=True)

    # Additional 3D plot 1
    st.subheader('3D Scatter Plot of Expenses by Date and Amount 📈')
    fig = px.scatter_3d(data, x='Date', y='Category', z='Amount', color='Category', size='Amount',
                        title='3D Scatter Plot of Expenses by Date and Amount')
    st.plotly_chart(fig, use_container_width=True)

    # Additional 3D plot 2
    st.subheader('3D Surface Plot of Expenses by Date and Category 📈')
    fig = px.scatter_3d(data, x='Date', y='Category', z='Amount', color='Amount',
                        title='3D Surface Plot of Expenses by Date and Category')
    fig.update_traces(marker=dict(size=5))
    fig.update_layout(scene=dict(zaxis=dict(title='Amount')))
    st.plotly_chart(fig, use_container_width=True)
    
    # Visualization: 3D Scatter Plot
    st.subheader('3D Scatter Plot 📊')
    fig = px.scatter_3d(data, x='Date', y='Amount', z='Category', color='Category')
    st.plotly_chart(fig)

    

# Button to switch to the About page
if st.button("About ℹ️"):
    about()
