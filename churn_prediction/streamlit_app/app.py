import streamlit as st
import pandas as pd
import numpy as np
import pickle
import sys
import os
from pathlib import Path

# Add the project root to the path so we can import from src/
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# Page configuration
st.set_page_config(
    page_title="Telco Customer Churn Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

# Helper functions
@st.cache_data
def load_data():
    """Load the dataset"""
    try:
        # Adjust path based on your actual data location
        data_path = project_root / "data" / "churn_prediction_data.csv"
        if data_path.exists():
            df = pd.read_csv(data_path)
            return df
        else:
            # Fallback: try to find the CSV file
            st.error(f"Data file not found at {data_path}. Please check the file path.")
            return None
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

@st.cache_resource
def load_model():
    """Load the trained model"""
    try:
        model_path = project_root / "models" / "churn_model.pkl"
        if model_path.exists():
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            return model
        else:
            st.warning("Model file not found. Some features may not work.")
            return None
    except Exception as e:
        st.warning(f"Could not load model: {e}")
        return None

def main():
    # Main title
    st.markdown('<h1 class="main-header">📊 Telco Customer Churn Analysis Dashboard</h1>', unsafe_allow_html=True)
    
    # Sidebar navigation
    st.sidebar.title("🧭 Navigation")
    st.sidebar.markdown("---")
    
    pages = {
        "🏠 Overview": "overview",
        "🔍 Data Explorer": "data_explorer", 
        "🎯 Make Predictions": "predictions",
        "📈 Model Performance": "model_performance",
        "💼 Business Insights": "business_insights"
    }
    
    selected_page = st.sidebar.selectbox("Select a page:", list(pages.keys()))
    
    # Add some sidebar info
    st.sidebar.markdown("---")
    st.sidebar.markdown("### About This Project")
    st.sidebar.info(
        "This dashboard analyzes customer churn patterns using machine learning "
        "to help businesses identify at-risk customers and develop retention strategies."
    )
    
    # Load data once
    df = load_data()
    model = load_model()
    
    # Route to different pages
    page_name = pages[selected_page]
    
    if page_name == "overview":
        show_overview(df, model)
    elif page_name == "data_explorer":
        show_data_explorer(df)
    elif page_name == "predictions":
        show_predictions(df, model)
    elif page_name == "model_performance":
        show_model_performance(df, model)
    elif page_name == "business_insights":
        show_business_insights(df, model)

def show_overview(df, model):
    """Overview/Home page"""
    st.markdown("## 📋 Project Overview")
    
    if df is not None:
        # Key metrics in columns
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_customers = len(df)
            st.metric("Total Customers", f"{total_customers:,}")
        
        with col2:
            if 'Churn' in df.columns:
                churn_rate = (df['Churn'].value_counts().get('Yes', 0) / len(df)) * 100
                st.metric("Churn Rate", f"{churn_rate:.1f}%")
            else:
                st.metric("Churn Rate", "N/A")
        
        with col3:
            if model is not None:
                st.metric("Model Status", "✅ Loaded")
            else:
                st.metric("Model Status", "❌ Not Found")
        
        with col4:
            if df is not None:
                st.metric("Features", f"{len(df.columns)}")
            else:
                st.metric("Features", "N/A")
        
        st.markdown("---")
        
        # Project description
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            ### 🎯 Project Objectives
            
            This project analyzes customer churn patterns in the telecommunications industry using machine learning techniques. The dashboard provides:
            
            - **Interactive data exploration** to understand customer behavior patterns
            - **Real-time predictions** for individual customers or batch processing
            - **Model performance metrics** to evaluate prediction accuracy
            - **Business insights** and actionable recommendations for customer retention
            
            ### 📊 Dataset Information
            
            The analysis uses the Telco Customer Churn dataset, which contains information about:
            - Customer demographics and account information
            - Services subscribed to by customers
            - Customer account status and churn behavior
            """)
        
        with col2:
            st.markdown("### 🚀 Quick Start")
            st.markdown("""
            1. **Explore Data**: Navigate to the Data Explorer to understand the dataset
            2. **Make Predictions**: Use the prediction tool to forecast customer churn
            3. **View Performance**: Check model accuracy and metrics
            4. **Get Insights**: Review business recommendations
            """)
            
            if df is not None:
                st.markdown("### 📈 Dataset Preview")
                st.dataframe(df.head(3), use_container_width=True)
    
    else:
        st.error("Data not loaded. Please check your data file path.")

def show_data_explorer(df):
    """Data exploration page placeholder"""
    st.markdown("## 🔍 Data Explorer")
    st.info("This page will contain interactive data visualizations and exploration tools.")
    
    if df is not None:
        st.dataframe(df.head(10), use_container_width=True)
        st.markdown(f"**Dataset shape:** {df.shape[0]} rows × {df.shape[1]} columns")
    else:
        st.error("No data available to explore.")

def show_predictions(df, model):
    """Predictions page placeholder"""
    st.markdown("## 🎯 Make Predictions")
    st.info("This page will contain the prediction interface for individual customers and batch processing.")
    
    if model is None:
        st.warning("Model not available. Please train and save a model first.")
    else:
        st.success("Model loaded successfully! Prediction interface coming soon.")

def show_model_performance(df, model):
    """Model performance page placeholder"""
    st.markdown("## 📈 Model Performance")
    st.info("This page will show model metrics, confusion matrices, and performance visualizations.")

def show_business_insights(df, model):
    """Business insights page placeholder"""
    st.markdown("## 💼 Business Insights")
    st.info("This page will contain actionable business recommendations and customer segmentation analysis.")

if __name__ == "__main__":
    main()