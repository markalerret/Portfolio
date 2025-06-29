# Executive Summary - Key Insights for Dashboard
executive_summary = """
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
"""



# Data Overview Section for Dashboard
data_overview="""
## Data overview & Quality

### Dataset Characteristics
- **Total Customers**: 7,043
- **Features**: 19 (16 categorical, 3 numerical)
- **Target Variable**: Customer Churn (Yes/No)
-**Overall Churn Rate**: 26.5%

### Data Quality Assessment
**No missing values after cleaning**
**No duplicate records**
**Business logic validated** (Internet service dependencies confirmed)
**Data types corrected** (TotalCharges converted from object to numeric)

### Key Data Quality Fix
- **Issue Found**: 11 customers with 0 tenure had empty TotalCharges
- **Root Cause**: New customers haven't accumulated charges yet
- **Solution**: Set TotalCharges to 0 for tenure = 0 customers
- **Business Logic**: Conservative approach, validated consistency
"""

# Data overview statistics for dashboard
def get_data_overview_stats():
    stats = {
        'total customers': len(data),
        'churn_rate': (data['Churn'] == 'Yes').mean(),
        'avg_tenure': data['tenure'].mean(),
        'avg_monthly_charges': data['MonthlyCharges'].mean(),
        'avg_total_monthly_charges': data['TotalCharges'].mean()
    }
    return stats



# Key Churn Drivers Section for Dashboard
key_drivers_summary="""
## Key Churn Drivers Analysis

### 1. Contract Type - Strongest Predictor
**Customer commitment level directly correlates with retention**
- Month-to-month: 42.7% churn rate
- One year: 11.3% churn rate
- Two year: 2.8% churn rate

**Business Impact**: 15x difference between highest and lowest risk contract types

### 2. Payment Method - Operational Behavior Signal
**Payment automation strongly indicates customer engagement**
- Electronic check: 45.3% churn rate (highest risk)
- Mailed check: 19.1% churn rate
- Bank Transfer (automatic): 16.7% churn rate
- Credit card (automatic): 15.2% churn rate (lowest risk)

**Key Insight**: Automatic payment methods correlate with 3x better retention

### 3. Internet Service Type - Premium Service Paradox
**Higher-priced service shows unexpected churn pattern**
- Fiber optic: 41.9% churn rate (premium service, high churn)
- DSL: 19.0% churn rate (standard service, moderate churn)
- No internet: 7.4% churn rate (basic service, low churn)

**Surprising Finding**: Most expensive service has highest churn rate
"""

# functions to generate the key driver visualizations for Streamlit
def create_contract_chart():
    contract_churn = data.groupby('Contract')['Churn'].apply(lambda x: (x == 'Yes').mean())
    return contract_churn

def create_payment_chart():
    payment_churn = data.groupby('PaymentMethod')['Churn'].apply(lambda x: (x == 'Yes').mean())
    return payment_churn

def create_internet_chart():
    internet_churn = data.groupby('InternetService')['Churn'].apply(lambda x: (x == 'Yes').mean())
    return internet_churn

#Key metrics for dashboard cards/KPIs
key_driver_metrics = {
    'contract_range': '2.8% - 42.7%'
    'payment_range': '15.2% - 45.3%'
    'internet_range': '7.4% - 41.9%'
}



#Fiber Optic Deep Dive Section for Dashboard
fiber_optic_analysis = """
## Deep Dive: The Fiber Optic Problem

### The "Perfect Storm" Discovery
**Fiber optic customers don't just have high churn - they stack multiple risk factors

### Fiber Customer Risk Profile
- **41.9% churn rate** (2.2x higher than DSL customers)
- **3,096 total fiber customers** in dataset
- **Premium pricing**: 89.7% pay $70-$110/month
- **Low commitment**: 69% have month-to-month contracts
- **Problematic payments**: 52% use electronic check

### Root Cause Analysis
**This explains multiple churn patterns we observed:**

1. **Electronic Check high Churn** Driven by fiber customer overlap
2. **$70-$110 Monthly Charge Churn** Driven by fiber pricing tier
3. **Premium Service Paradox** High price + low commitment = churn

##The Compound Effect
**Individual Risk Factors**:
- Month-to-month contracts: 42.7% churn
- Electronic check payments: 45.3% churn
- Fiber optic service: 41.9% churn

**Combined Effect**: Customers with all three factors show 60%_ churn rates

### Business Implications
- **Acquisition Problem**: Attracting wrong customer segment for premium service
- **Value Perception Gap**: Customers don't see fiber as worth premium price
- **Commitment Mismatch**: Premium service needs premium customer commitment
"""

# Functions for fiber optic analysis in Streamlit
def get_fiber_customer_profile():
    fiber_data = data[data['InternetService'] == 'Fiber optic']
    profile = {
        'total_customers': len(fiber_data),
        'churn_rate': fiber_data['Churn'] == 'Yes'.mean(),
        'month_to_month_pct': (fiber_data['Contract'] == 'Month-to-month').mean(),
        'electronic_check_pct': (fiber_data['PaymentMethod'] == 'Electronic check').mean(),
        'premium_price_pct': ((fiber_data['MonthlyCharges'] >= 70) &
                              (fiber_data['MonthlyCharges'] <= 110)).mean(),
        'avg_monthly_charges': fiber_data['MonthlyCharges'].mean()
    }
    return profile

def create_fiber_comparison_chart():
    #Compare fiber vs non-fiber customers across key metrics
    comparison_data = {
        'Contract_MonthtoMonth': [
            (data[data['InternetService'] == 'Fiber optic']['Contract'] == 'Month-to-month').mean(),
            (data[data['InternetService'] != 'Fiber optic']['Contract'] == 'Month-to-month').mean()
        ],
        'Payment_ElectronicCheck': [
            (data[data['InternetService'] == 'Fiber optic']['PaymentMethod'] == 'Electronic check').mean(),
            (data[data['InternetService'] != 'Fiber optic']['PaymentMethod'] == 'Electronic check').mean()
        ],
        'Churn_rate': [
            (data[data['InternetService'] == 'Fiber optic']['Churn'] == 'Yes').mean(),
            (data[data['InternetService'] != 'Fiber optic']['Churn'] == 'Yes').mean()
        ]
    }
    return comparison_data



#Risk Cosre Analysis Section for Dashboard
risk_score_analysis = """
## Risk Score Analysis - Quantifying Compound Risk

### Risk Scoring Model
**Created composite risk score (0-7) based on three key factors:**

**Contract Risk** (0-3 points):
- Two year contract: 0 points
- One year contract: 1 point
- Month-to-month: 3 points

**Payment Risk** (0-2 points):
- Automatic payments: 0 points
- Mailed check: 1 point
- Electronic check: 2 points

**Service Risk** (0-2 points)
- No internet: 0 points
- DSL: 1 point
- Fiber optic: 2 points

### Key Findings
**Risk compounds exponentially, not linearly:**
- **Score 0-1**: 7-13% churn rate (low risk)
- **Score 2-4**: 15-35% churn rate (moderate risk)
- **Score 5-6**: 35-44% churn rate (high risk)
- **Score 7**: 60% churn rate (extreme risk)

### Business Value
**Risk score enables:**
- **Proactive intervention** for high-risk customers
- **Targeted retention programs** by risk tier
- **Customer segmentation** for different strategies
- **Predictive modeling** Foundation for ML algorithms
"""

#Functions for risk score analysis in Streamlit
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

def get_risk_score_distribution():
    """Get risk score distribution for dashboard"""
    risk_scores = calculate_risk_scores()
    risk_churn = data.groupby(risk_scores)['Churn'].apply(lambda x: (x == 'Yes').mean())
    risk_counts = risk_scores.value_counts().sort_index()

    return {
        'scores': risk_churn.index.tolist(),
        'churn_rates': risk_churn.values.tolist(),
        'customer_counts': [risk_counts[score] for score in risk_churn.index]
    }

def create_risk_score_insights():
    """Key insights for risk score dashboard cards"""
    risk_data = get_risk_score_distribution()
    return {
        'lowest_risk_churn': min(risk_data['churn_rates']),
        'highest_risk_churn': max(risk_data['churn_rates']),
        'risk_multiplier': max(risk_data['churn_rates']) / min(risk_data['churn_rates']),
        'high_risk_customers': sum([count for score, count in zip(risk_data['scores'], risk_data['customer_counts']) if score >= 6])
    }



# Business Recommendations Section for Dashboard
business_recommendations = """
## Business Recommendations - Actionable Insights

### Priority 1: Fix Fiber Optic Customer Acquisition
**Problem**: Attracting commitment-averse customersto premium service
**Solutions**:
- **Contract Incentives**: Offer 20-30% disctount for fiber customers who sign 1+ year contracts
- **Automatic Payment Rewards**: Additional 5-10% discount for automatic payment setup
- **Target Audience Shift**: Focus marketing on customers seeking long-term, premium service

**Expected Impact**: Could reduce fiber churn from 41.9% to ~25% (saving ~500 customers annually)

### Priority 2: Implement Risk-Based Retnetion Program
**Problem**: Reactive approach to churn - customers leave before intervention
**Solutions**:
- **Risk Score 6-7 customers**: Immediate outreach with retention offers
- **Risk Score 4-5 customers**: Proactive engagement and service optimization
- **Risk Score 0-3 customers**: Loyalty programs and upselling opportunities

**Expected Impact**: 10-15% reduction in overall churn through targeted intervention

### Priority 3: Payment Method Migration Campaign
**Problem**: Electronic check customers have 3x higher churn than automatic payments
**Solutions**:
- **Automatic Payment Incentives**: $5-$10/month discount for switching
- **Education Campaign**: Highlight convenience and reliability benefits
- **Gradual Migration**: Start with new customers, then target existing high-risk customers

**Expected Impact**: Could improve retention by 20-30% for converted customers

### Priority 4 Early Customer Experience Enhancement
**Problem**: Majority of churn happens in month 1
**Solutions**:
- **30-Day Success Program**: Enhancing onboarding and check-ins for new customers
- **First Month Guarantee**: Risk-free trail period to build confidence
- **Dedicated Support**: Special support line for customers in first 60 days

**Expected Impact**: 15-25% reduction in early churn rates

### Priority 5: Contract Strategy Overhaul
**Problem**: 42.7% churn rate for month-to-month customers
**Solutions**:
- **Contract Graduation Program**: Incentivize moves from month-to-month to annual
- **Flexible Contracts**: 6-month options as stepping stone to longer commitments
- **Lock-in Benefits**: Exclusive features/pricing only available with contracts

**Expected Impact**: 5-10% shift to longer contracts could reduce overall churn by 3-5%
"""

#Functions for recommendations dashboard
def calculate_business_impact():
    """Calculate potential business impact of recommendations"""
    current_customers = len(data)
    current_churn_rate = (data['Churn'] == 'Yes').mean()
    current_annual_churn = current_customers * current_churn_rate

    #Estimate revenue impact (assuming average customer value)
    avg_monthly_revenue = data['MonthlyCharges'].mean()
    avg_customer_lifetime = data['Tenure'].mean()
    avg_customer_value = avg_monthly_revenue * avg_customer_lifetime

    impact_scenarios = {
        'fiber_fix': {
            'customers_saved': int(len(data[data['InternetService'] == 'Fiber optic']) * 0.17), #17% improvement
            'revenue_impact': int(len(data[data['InternetService'] == 'Fiber optic']) * 0.17 * avg_customer_value)
        },
        'payment_migration': {
            'customers_saved': int(len(data[data['PaymentMethod'] == 'Electronic check']) * 0.25), #25% improvement
            'revenue_impact': int(len(data[data['PaymentMethd'] == 'Electronic check']) * .025 * avg_customer_value)
        },
        'overall_impact': {
            'churn_reduction': 0.05, #5% overall churn reduction
            'customers_saved': int(current_customers * 0.05),
            'revenue_impact': int(current_customers * 0.05 * avg_customer_value)
        }
    }

    return impact_scenarios

def get_recommendation_priorities():
    """Get prioritized recommendations with metrics"""
    return {
        'priority_1': {
            'title': 'Fix Fiber Optic Acquisition',
            'impact': 'High',
            'effort': 'Medium',
            'timeline': '3-6 months'
        },
        'priority_2': {
            'title': 'Risk-Based Retention Program',
            'impact': 'High',
            'effort': 'Low',
            'timeline': '1-2 months'
        },
        'priority_3': {
            'title': 'Payment Method Migration',
            'impact': 'Medium',
            'effort': 'Low',
            'timeline': '2-3 months'
        }
    }