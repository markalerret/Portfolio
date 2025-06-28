import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt

def show_data_explorer(data):
    """Enhanced Data Explorer page with comprehensive EDA"""
    
    if data is None:
        st.error("No data available to explore.")
        return
    
    st.markdown("## 🔍 Data Explorer")
    st.markdown("Comprehensive analysis of the customer churn dataset")
    
    # Sidebar filters for the entire page
    st.sidebar.markdown("### 🎛️ Data Filters")
    
    # Filter by churn status
    churn_filter = st.sidebar.selectbox(
        "Filter by Churn Status:",
        ["All Customers", "Churned Only", "Active Only"]
    )
    
    # Apply filter
    if churn_filter == "Churned Only" and 'Churn' in data.columns:
        filtered_data = data[data['Churn'] == 'Yes']
    elif churn_filter == "Active Only" and 'Churn' in data.columns:
        filtered_data = data[data['Churn'] == 'No']
    else:
        filtered_data = data
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Dataset Overview", "📈 Numerical Analysis", "📋 Categorical Analysis", "🔗 Relationships"])
    
    with tab1:
        show_dataset_overview(data, filtered_data)
    
    with tab2:
        show_numerical_analysis(data, filtered_data)
    
    with tab3:
        show_categorical_analysis(data, filtered_data)
    
    with tab4:
        show_relationships_analysis(data, filtered_data)

def show_dataset_overview(data, filtered_data):
    """Dataset overview section"""
    
    st.markdown("### 📋 Dataset Summary")
    
    # Dataset info cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Customers", f"{len(data):,}")
    with col2:
        st.metric("Features", len(data.columns))
    with col3:
        st.metric("Filtered View", f"{len(filtered_data):,}")
    with col4:
        if 'Churn' in data.columns:
            churn_rate = (data['Churn'].value_counts().get('Yes', 0) / len(data)) * 100
            st.metric("Overall Churn Rate", f"{churn_rate:.1f}%")
    
    st.markdown("---")
    
    # Data quality information
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 🧹 Data Quality")
        st.success("✅ **Clean Dataset**: All missing values handled")
        st.info("📝 **Data Cleaning Applied**: 11 missing values in TotalCharges (tenure=0 customers) converted to zeros")
        st.info("🔧 **Data Types**: TotalCharges converted to numeric format")
    
    with col2:
        st.markdown("### 📊 Basic Statistics")
        
        # Identify numerical columns
        numerical_cols = data.select_dtypes(include=[np.number]).columns.tolist()
        
        if numerical_cols:
            stats_data = filtered_data[numerical_cols].describe().round(2)
            st.dataframe(stats_data, use_container_width=True)
    
    # Data preview
    st.markdown("### 👀 Data Preview")
    show_all = st.checkbox("Show all columns", value=False)
    
    if show_all:
        st.dataframe(filtered_data.head(10), use_container_width=True)
    else:
        # Show key columns
        key_cols = ['customerID', 'tenure', 'MonthlyCharges', 'TotalCharges', 'Contract', 'Churn']
        available_cols = [col for col in key_cols if col in filtered_data.columns]
        if available_cols:
            st.dataframe(filtered_data[available_cols].head(10), use_container_width=True)
        else:
            st.dataframe(filtered_data.head(10), use_container_width=True)

def show_numerical_analysis(data, filtered_data):
    """Numerical variables analysis"""
    
    st.markdown("### 📈 Numerical Variables Analysis")
    
    # Get numerical columns
    numerical_cols = filtered_data.select_dtypes(include=[np.number]).columns.tolist()
    
    if not numerical_cols:
        st.warning("No numerical columns found in the dataset.")
        return
    
    # Variable selector
    selected_var = st.selectbox(
        "Select a numerical variable to analyze:",
        numerical_cols,
        key="numerical_selector"
    )
    
    if selected_var:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Distribution plot
            fig = px.histogram(
                filtered_data, 
                x=selected_var,
                nbins=30,
                title=f"Distribution of {selected_var}",
                color_discrete_sequence=['#1f77b4']
            )
            fig.update_layout(
                xaxis_title=selected_var,
                yaxis_title="Count",
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Summary statistics
            st.markdown(f"**{selected_var} Statistics**")
            stats = filtered_data[selected_var].describe()
            for stat, value in stats.items():
                if isinstance(value, (int, float)):
                    st.metric(stat.title(), f"{value:.2f}")
        
        # Churn comparison if churn column exists
        if 'Churn' in data.columns:
            st.markdown(f"### {selected_var} by Churn Status")
            
            fig = px.box(
                filtered_data,
                x='Churn',
                y=selected_var,
                title=f"{selected_var} Distribution by Churn Status",
                color='Churn',
                color_discrete_map={'Yes': '#ff7f0e', 'No': '#1f77b4'}
            )
            st.plotly_chart(fig, use_container_width=True)

def show_categorical_analysis(data, filtered_data):
    """Categorical variables analysis"""
    
    st.markdown("### 📋 Categorical Variables Analysis")
    
    # Get categorical columns
    categorical_cols = filtered_data.select_dtypes(include=['object']).columns.tolist()
    # Remove customerID if it exists
    categorical_cols = [col for col in categorical_cols if col not in ['customerID', 'Customer ID']]
    
    if not categorical_cols:
        st.warning("No categorical columns found in the dataset.")
        return
    
    # Variable selector
    selected_var = st.selectbox(
        "Select a categorical variable to analyze:",
        categorical_cols,
        key="categorical_selector"
    )
    
    if selected_var:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Value counts
            value_counts = filtered_data[selected_var].value_counts()
            
            fig = px.bar(
                x=value_counts.index,
                y=value_counts.values,
                title=f"Distribution of {selected_var}",
                labels={'x': selected_var, 'y': 'Count'},
                color_discrete_sequence=['#1f77b4']
            )
            fig.update_layout(xaxis_title=selected_var, yaxis_title="Count")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Summary info
            st.markdown(f"**{selected_var} Summary**")
            st.metric("Unique Values", len(value_counts))
            st.metric("Most Common", value_counts.index[0])
            st.metric("Most Common %", f"{(value_counts.iloc[0]/len(filtered_data)*100):.1f}%")
            
            # Show value counts table
            st.markdown("**Value Counts:**")
            value_counts_df = pd.DataFrame({
                'Value': value_counts.index,
                'Count': value_counts.values,
                'Percentage': (value_counts.values / len(filtered_data) * 100).round(1)
            })
            st.dataframe(value_counts_df, hide_index=True)
        
        # Churn analysis if churn column exists
        if 'Churn' in data.columns and selected_var != 'Churn':
            st.markdown(f"### Churn Rate by {selected_var}")
            
            # Calculate churn rate by category
            churn_by_category = filtered_data.groupby(selected_var)['Churn'].apply(
                lambda x: (x == 'Yes').mean() * 100
            ).sort_values(ascending=False)
            
            fig = px.bar(
                x=churn_by_category.index,
                y=churn_by_category.values,
                title=f"Churn Rate by {selected_var}",
                labels={'x': selected_var, 'y': 'Churn Rate (%)'},
                color=churn_by_category.values,
                color_continuous_scale='Reds'
            )
            fig.update_layout(xaxis_title=selected_var, yaxis_title="Churn Rate (%)")
            st.plotly_chart(fig, use_container_width=True)

def show_relationships_analysis(data, filtered_data):
    """Relationships and correlation analysis"""
    
    st.markdown("### 🔗 Variable Relationships")
    
    # Correlation heatmap for numerical variables
    numerical_cols = filtered_data.select_dtypes(include=[np.number]).columns.tolist()
    
    if len(numerical_cols) > 1:
        st.markdown("#### Correlation Matrix")
        
        correlation_matrix = filtered_data[numerical_cols].corr()
        
        fig = px.imshow(
            correlation_matrix,
            title="Correlation Heatmap of Numerical Variables",
            color_continuous_scale='RdBu',
            aspect='auto'
        )
        fig.update_layout(
            width=600,
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Show strongest correlations
        st.markdown("#### Strongest Correlations")
        
        # Get correlation pairs (excluding diagonal)
        corr_pairs = []
        for i in range(len(correlation_matrix.columns)):
            for j in range(i+1, len(correlation_matrix.columns)):
                var1 = correlation_matrix.columns[i]
                var2 = correlation_matrix.columns[j]
                corr_value = correlation_matrix.iloc[i, j]
                corr_pairs.append({
                    'Variable 1': var1,
                    'Variable 2': var2,
                    'Correlation': corr_value
                })
        
        corr_df = pd.DataFrame(corr_pairs)
        corr_df['Abs Correlation'] = abs(corr_df['Correlation'])
        corr_df = corr_df.sort_values('Abs Correlation', ascending=False).head(5)
        
        for _, row in corr_df.iterrows():
            correlation_strength = "Strong" if abs(row['Correlation']) > 0.7 else "Moderate" if abs(row['Correlation']) > 0.3 else "Weak"
            st.write(f"**{row['Variable 1']}** ↔ **{row['Variable 2']}**: {row['Correlation']:.3f} ({correlation_strength})")
    
    # Scatter plot analysis
    if len(numerical_cols) >= 2:
        st.markdown("#### Scatter Plot Analysis")
        
        col1, col2 = st.columns(2)
        with col1:
            x_var = st.selectbox("X-axis variable:", numerical_cols, key="scatter_x")
        with col2:
            y_var = st.selectbox("Y-axis variable:", [col for col in numerical_cols if col != x_var], key="scatter_y")
        
        if x_var and y_var:
            color_by = 'Churn' if 'Churn' in filtered_data.columns else None
            
            fig = px.scatter(
                filtered_data,
                x=x_var,
                y=y_var,
                color=color_by,
                title=f"{y_var} vs {x_var}",
                color_discrete_map={'Yes': '#ff7f0e', 'No': '#1f77b4'} if color_by else None
            )
            st.plotly_chart(fig, use_container_width=True)