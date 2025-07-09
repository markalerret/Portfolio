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
    
    data=load_data()

    # Dataset characteristics section
    st.subheader("Dataset Characteristics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Customers", f"{len(data)}")

    with col2:
        st.metric("Total Features", len(data.columns))

    with col3:
        churn_rate = (data['Churn'] == 'Yes').mean()
        st.metric("Overall Churn Rate", f"{churn_rate:.1%}")

    with col4:
        avg_tenure = data['tenure'].mean()
        st.metric("Average Tenure", f"{avg_tenure:.1f} months")

    st.markdown("---")

    # Data types breakdown
    st.subheader("Data Types & Structure")

    col1, col2 = st.columns(2)

    with col1:
        st.write("Categorical Variables (16):")
        categorical_cols = data.select_dtypes(include=['object']).columns.tolist()
        categorical_cols.remove('customerID') #remove ID column
        categorical_cols.remove('Churn') #remove churn column
        for col in categorical_cols:
            unique_count = data[col].nunique()
            st.write(f"{col}: {unique_count} unique values")

        st.write("")

        #Add target variable separately
        st.write("Target Variable")
        st.write(f"Churn: {data['Churn'].nunique()} classes (Yes/No)")

    with col2:
        st.write("Numerical Variables (3):")
        numerical_cols = data[['tenure', 'MonthlyCharges', 'TotalCharges']].describe()
        st.dataframe(numerical_cols.round(2))

    st.markdown("---")

    #Data quality section
    st.subheader("Data Quality Assessment")

    col1, col2 = st.columns(2)

    with col1:
        st.success("Quality Checks Passed:")
        st.write("- No missing values after cleaning")
        st.write("- No duplicate records")
        st.write("- Business Logic Validated")
        st.write("- Data Types Corrected")

    with col2:
        st.info("Data Cleaning Applied:")
        st.write("- TotalCharges Issue: 11 customers with 0 tenure had empty TotalCharges")
        st.write("- Root Cause: New customers haven't accumulated charges")
        st.write("- Solution: Set TotalCharges = 0 for tenure = 0 customers")
        st.write("- Validation: Confirmed business logic consistency")

    st.markdown("---")

    # Sample data preview
    st.subheader("Sample Data Preview")
    st.write("First 10 rows of the cleaned dataset:")
    st.dataframe(data.head(10))


def show_key_drivers():
    st.header("Key Churn Drivers")
    
    data = load_data()

    st.markdown("""
    Analysis of categorical variables reveals three primary drivers of customer churn,
    each representing different aspects of customer behavior and service preferences.
    """)

    #Create headers above the columns
    header_col1, header_col2, header_col3 = st.columns(3)
    with header_col1:
        st.markdown("<h4 style-'text-align=center; margin-bottom: 10px;'>Contract Type</h4>", unsafe_allow_html=True)
    with header_col2:
        st.markdown("<h4 style-'text-align=center; margin-bottom: 10px;'>Payment Method</h4>", unsafe_allow_html=True)
    with header_col3:
        st.markdown("<h4 style-'text-align=center; margin-bottom: 10px;'>Internet Service</h4>", unsafe_allow_html=True)

    # Create three columns for the charts
    col1, col2, col3 = st.columns(3)

    with col1:
        contract_churn = get_churn_by_category(data, "Contract")

        fig1 = px.bar(
            x = contract_churn.index.tolist(),
            y = contract_churn.values.tolist(),
            labels = {'x': 'Contract Type', 'y':'Churn Rate'},
            color = contract_churn.values,
            color_continuous_scale='Reds'
        )
        fig1.update_layout(
            showlegend=False, 
            height=400,
            margin=dict(l=60, r=60, t=40, b=120),
            xaxis=dict(
                title = "",
                tickangle=45,
                tickfont=dict(size=10),
                automargin=False
            ),
            yaxis=dict(
                tickfont=dict(size=10),
                automargin=False
            ),
        )
        st.plotly_chart(fig1, use_container_width=True)

        st.write("Churn Rates:")
        for contract, rate in contract_churn.items():
            st.write(f"{contract}: {rate:.1%}")

    with col2:
        payment_churn = get_churn_by_category(data, 'PaymentMethod')

        fig2 = px.bar(
            x = payment_churn.index.tolist(),
            y = payment_churn.values.tolist(),
            labels = {'x': 'Payment Method', 'y': 'Churn Rate'},
            color = payment_churn.values,
            color_continuous_scale = 'Blues'
        )
        fig2.update_layout(
            showlegend=False, 
            height=400,
            margin=dict(l=60, r=60, t=25, b=120),
            xaxis=dict(
                title="",
                tickangle=45,
                tickfont=dict(size=10),
                automargin=False
            ),
            yaxis=dict(
                tickfont=dict(size=10),
                automargin=False
            ),
        )
        st.plotly_chart(fig2, use_container_width=True)

        st.write("Churn Rates:")
        for payment, rate in payment_churn.items():
            st.write(f"{payment}: {rate:.1%}")

    with col3:
        internet_churn = get_churn_by_category(data, 'InternetService')

        fig3 = px.bar(
            x = internet_churn.index.tolist(),
            y = internet_churn.values.tolist(),
            labels = {'x': 'Internet Service', 'y': 'Churn Rate'},
            color = internet_churn.values,
            color_continuous_scale = 'Greens'
        )
        fig3.update_layout(
            showlegend=False, 
            height=400,
            margin=dict(l=60, r=60, t=40, b=120),
            xaxis=dict(
                title="",
                tickangle=45,
                tickfont=dict(size=10),
                automargin=False
            ),
            yaxis=dict(
                tickfont=dict(size=10),
                automargin=False
            ),
        )
        st.plotly_chart(fig3, use_container_width=True)

        st.write("Churn Rates:")
        for service, rate in internet_churn.items():
            st.write(f"{service}: {rate:.1%}")

    # Add summart insights
    st.markdown("---")
    st.subheader("Key Insights")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("""
        Contract Commitment Effect
                
        Month-to-month customers show 15x higher churn that two-year customers, highlighting the importance of customer commitment.        
        """)

    with col2:
        st.info("""
        Payment Method Signal
                
        Automatic payment methods correlate with 3x better retention, suggesting customer engagement level affects churn risk.
        """)

    with col3:
        st.info("""
        Service Paradox
                
        Premium fiber service shows highest churn despite higher pricing, indicating potential value perception issues.
        """)


def show_fiber_analysis():
    st.header("Fiber Optic Deep Dive")
    
    data = load_data()

    # Introduction
    st.markdown("""
    The 'Perfect Storm' Discovery
                
    Fiber Optic customers don't just have high churn, they stack multiple risk factors that compound into a business problem.
    """)

    st.markdown("---")

    # Key metrics section
    st.subheader("Fiber Customer Risk Profile")

    fiber_data = data[data['InternetService'] == 'Fiber optic']

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Fiber Customers", f"{len(fiber_data):,}")

    with col2:
        fiber_churn = (fiber_data['Churn'] == 'Yes').mean()
        st.metric("Fiber Churn Rate", f"{fiber_churn:.1%}")

    with col3:
        month_to_month_pct = (fiber_data['Contract'] == 'Month-to-month').mean()
        st.metric("Month-to-Month", f"{month_to_month_pct:.1%}")

    with col4:
        electronic_check_pct = (fiber_data['PaymentMethod'] == 'Electronic check').mean()
        st.metric("Electronic Check", f"{electronic_check_pct:.1%}")

    st.markdown("---")

    # Comparison visualization
    st.subheader("Fiber vs Non-fiber Customer Comparison")

    # Create comparison data
    comparison_metrics = {
        'Customer Type': ['Fiber Optic', 'Non-Fiber'],
        'Churn Rate': [
            (data[data['InternetService'] == 'Fiber optic']['Churn'] == 'Yes').mean(),
            (data[data['InternetService'] != 'Fiber optic']['Churn'] == 'Yes').mean()
        ],
        'Month-to-month %': [
            (data[data['InternetService'] == 'Fiber optic']['Contract'] == 'Month-to-month').mean(),
            (data[data['InternetService'] != 'Fiber optic']['Contract'] == 'Month-to-month').mean()
        ],
        'Electronic Check %': [
            (data[data['InternetService'] == 'Fiber optic']['PaymentMethod'] == 'Electronic check').mean(),
            (data[data['InternetService'] != 'Fiber optic']['PaymentMethod'] == 'Electronic check').mean()
        ]
    }

    # Create comparison chart
    fig = go.Figure()

    fig.add_trace(go.Bar(
        name='Fiber Optic',
        x=['Churn Rate', 'Month-to-Month %', 'Electronic Check %'],
        y=[comparison_metrics['Churn Rate'][0],
           comparison_metrics['Month-to-month %'][0],
           comparison_metrics['Electronic Check %'][0]],
        marker_color='lightcoral'
    ))


def show_risk_analysis():
    st.header("Risk Score Analysis")
    st.write()


def show_recommendations():
    st.header("Business Recommendations")
    st.write()

if __name__ == "__main__":
    main()