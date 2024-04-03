import streamlit as st

# Initialize categorized_df in session state if not already initialized

if 'categorized_df' not in st.session_state or st.session_state['categorized_df'] is None:
    st.session_state['categorized_df'] = pd.DataFrame()

# Check if categorized_df contains data
if st.session_state['categorized_df'].empty:
    st.error("No data available for visualization. Please categorize your expenses first.")
else:
    categorized_df = st.session_state['categorized_df']

    if 'Category' not in categorized_df.columns:
        st.error("No category information found. Please categorize your expenses first.")
    else:
        categorized_df['Type'] = categorized_df['Category'].apply(lambda x: 'Fixed' if x in st.session_state['fixed_exp'] else 'Variable')

        st.write("Categorized Expenses:")
        st.write(categorized_df)
