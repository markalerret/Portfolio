#run with this command in terminal
#python -m streamlit run streamlit_app/app.py

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sn
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(
    page_title="Customer Churn Analysis Dashboard",
    layout="wide",
    initial_sidebar_state='expanded'
)

# Load data (you'll need to add your data loading here)
@st.cache_data
def load_data():
    data = pd.read_csv("data/churn_prediction_data.csv")

    # Data cleaning (Based on analysis)
    # 1. TotalCharges
    data.loc[data['tenure'] == 0, 'TotalCharges'] = '0'
    data['TotalCharges'] = pd.to_numeric(data['TotalCharges'])

    # 2. SeniorCitizen
    data['SeniorCitizen'] = data['SeniorCitizen'].astype(str)

    return data

# Helper functions
@st.cache_data
def calculate_risk_scores():
    """recalculate risk scores for dashboard"""
    def calc_score(row):
        score = 0
        #Contract risk
        if row['Contract'] == 'Month-to-month':
            score += 3
        elif row['Contract'] == 'One year':
            score += 1

        #Payment risk
        if row['PaymentMethod'] == 'Electronic check':
            score += 2
        elif row['PaymentMethod'] == 'Mailed check':
            score += 1

        #Service risk
        if row['InternetService'] == 'Fiber optic':
            score += 2
        elif row['InternetService'] == 'DSL':
            score += 1

        return score

    return data.apply(calc_score, axis=1)

@st.cache_data
def get_churn_by_category(data,column):
    """Get churn rates by category for any column"""
    return data.groupby(column)['Churn'].apply(lambda x: (x == 'Yes').mean())


# Main Navigation
def main():
    st.title("Customer Churn Analysis Dashboard")

    # Load data
    data = load_data()
    if data is None:
        st.stop() #Stop execution if data doesn't load

    st.markdown("---")

    # Sidebar navigation
    st.sidebar.title("Navigation")
    pages = {
        "Executive Summary": show_executive_summary,
        "Data Overview": show_data_overview,
        "Key Churn Drivers": show_key_drivers,
        "Fiber Optic Deep Dive": show_fiber_analysis,
        "Risk Score Analysis": show_risk_analysis,
        "Business Recommendations": show_recommendations
    }

    selected_page = st.sidebar.radio("Select Page", list(pages.keys()))

    #Display selected page
    pages[selected_page]()

#Page functions
def show_executive_summary():
    st.header("Executive Summary")

    # Load and test the data
    data = load_data()

    # Display basic data info to confirm it's working
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Customers", f"{len(data):,}")

    with col2:
        churn_rate = (data['Churn'] == 'Yes').mean()
        st.metric("Churn Rate", f"{churn_rate:.1%}")

    with col3:
        avg_tenure = data['tenure'].mean()
        st.metric("Avg Tenure (Months)", f"{avg_tenure:.1f}")

    with col4:
        avg_monthly = data['MonthlyCharges'].mean()
        st.metric("Avg Monthly Charges", f"${avg_monthly:.0f}")

    st.markdown("---")

    st.markdown("""
    ## Customer Churn Analysis - Key Findings

    **Dataset**: 7,043 customers, 27% churn rate

    **Top Churn Drivers**:
    1. **Contract Type**: Month-to-month customers churn at 42.7% vs 2.8% for two-year contracts
    2. **Payment Method**: Electronic check customers churn at 45.3% vs 15.2% for automatic payments
    3. **Internet Service**: Fiber optic customers churn at 41.9% despite premium pricing

    **Major Business Insight**: Fiber optic customers reporesent a "perfect storm" of risk factors
    - 69% have month-to-month contracts
    - 52% pay by electronic check
    - 89.7% pay premium prices ($70-$110/month)
    - Result: Compound risk leading to high churn

    **Risk Model**: Risk scores 0-7 show exponential churn increase (7% to 60%)
    """)

def show_data_overview():
    st.header("Data Overview")
    st.write()


def show_key_drivers():
    st.header("Key Churn Drivers")
    
    data = load_data()

    #Quick interactive chart - Contract Type churn rates
    st.subheader("Contract Type vs Churn Rate")

    contract_churn = get_churn_by_category(data, 'Contract')

    #Show the actual numbers
    st.write("**Exact Churn Rates:**")
    for contract, rate in contract_churn.items():
        st.write(f"- {contract}: {rate:.1%}")

    #Create a simple bar chart
    fig = px.bar(
        x=contract_churn.index.tolist(),
        y=contract_churn.values.tolist(),
        title="Churn Rate by Contract Type",
        labels={'x': 'Contract Type', 'y': 'Churn Rate'},
        color=contract_churn.values,
        color_continuous_scale='Reds'
    )
    fig.update_layout(showlegend=False)

    st.plotly_chart(fig, use_container_width=True)


def show_fiber_analysis():
    st.header("Fiber Optic Deep Dive")
    st.write()


def show_risk_analysis():
    st.header("Risk Score Analysis")
    st.write()


def show_recommendations():
    st.header("Business Recommendations")
    st.write()

if __name__ == "__main__":
    main()