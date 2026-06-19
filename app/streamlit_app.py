import os
import sys
import streamlit as st
import plotly.express as px

# Ensure the root directory is in the path so we can import from src
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_dir not in sys.path:
    sys.path.append(root_dir)

from src.demand_analysis import load_data, CLEANED_CARS_PATH
from src.data_cleaning import PROCESSED_STATIONS_PATH
from src.load_simulation import run_simulation

# 1. Page Configuration
st.set_page_config(
    page_title="EV Charging Planner - Demand Analytics",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Premium Styling via Injecting CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    .main-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #10B981, #3B82F6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    
    .sub-title {
        font-size: 1.1rem;
        color: #6B7280;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background-color: #F9FAFB;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    
    .metric-val {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1F2937;
    }
    
    .metric-lbl {
        font-size: 0.9rem;
        font-weight: 500;
        color: #6B7280;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Main Title
st.markdown('<div class="main-title">⚡ EV Charging Station Demand Planner</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Green Community Transition • Malaysia EV & Hybrid Adoption & Infrastructure Analytics</div>', unsafe_allow_html=True)

# 4. Load Data
@st.cache_data
def get_datasets():
    cars_df = load_data(CLEANED_CARS_PATH)
    stations_df = load_data(PROCESSED_STATIONS_PATH)
    return cars_df, stations_df

try:
    cars_df, stations_df = get_datasets()
    
    # 5. Sidebar Layout (Focusing on EV & Hybrid)
    st.sidebar.image("app/assets/electric-car.png", width=120)
    st.sidebar.markdown("### EV & Hybrid Adoption Planner")
    st.sidebar.info(
        "This planner is focused on Electric Vehicles (EVs) and "
        "Hybrid Vehicles (PHEV/HEV) to assist Charging Point Operators in "
        "analyzing adoption and identifying infrastructure coverage gaps in Malaysia."
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ⚡ Grid Load Simulation Settings")
    cf_min = st.sidebar.slider(
        "Min Coincidence Factor (CF_min):",
        min_value=0.05,
        max_value=0.50,
        value=0.20,
        step=0.05,
        help="Baseline coincidence factor for large numbers of chargers."
    )
    low_thresh = st.sidebar.slider(
        "Low-Risk Threshold (kW):",
        min_value=100,
        max_value=1000,
        value=500,
        step=50,
        help="Peak loads below this value are classified as Low risk."
    )
    high_thresh = st.sidebar.slider(
        "High-Risk Threshold (kW):",
        min_value=1000,
        max_value=3000,
        value=1500,
        step=100,
        help="Peak loads above this value are classified as High risk."
    )
    
    # Create Tabs for the three segments
    tab1, tab2, tab3 = st.tabs(["🚗 EV & Hybrid Adoption", "🔌 Charging Infrastructure", "⚡ Grid Load Simulation"])
    
    # ==================== TAB 1: ADOPTION ANALYTICS ====================
    with tab1:
        # Aggregated distribution by state
        dist_cars_df = cars_df.groupby('state').size().reset_index(name='count')
        dist_cars_df = dist_cars_df.sort_values(by='count', ascending=True).reset_index(drop=True) # Ascending for horizontal bar chart
        
        # Metric Cards Row
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-lbl">Total EVs & Hybrids</div>
                    <div class="metric-val">{len(cars_df):,}</div>
                </div>
            """, unsafe_allow_html=True)
            
        with col2:
            # Get state with highest count
            if len(dist_cars_df) > 0:
                top_state_row = dist_cars_df.sort_values(by='count', ascending=False).iloc[0]
                top_state = top_state_row['state']
                top_count = top_state_row['count']
                top_display = f"{top_state} ({top_count:,})"
            else:
                top_display = "N/A"
                
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-lbl">Top Adoption Location</div>
                    <div class="metric-val" style="font-size: 1.8rem; line-height: 2.2rem; padding-top: 0.2rem;">{top_display}</div>
                </div>
            """, unsafe_allow_html=True)
            
        with col3:
            if len(dist_cars_df) > 0:
                avg_evs = int(dist_cars_df['count'].mean())
            else:
                avg_evs = 0
                
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-lbl">Average per State</div>
                    <div class="metric-val">{avg_evs:,}</div>
                </div>
            """, unsafe_allow_html=True)
            
        st.markdown("---")
        
        # Visualization Row
        chart_col, table_col = st.columns([2, 1])
        
        with chart_col:
            st.markdown("### EV & Hybrid Distribution by State")
            fig = px.bar(
                dist_cars_df,
                x='count',
                y='state',
                orientation='h',
                labels={'count': 'Number of Vehicles', 'state': 'State'},
                color='count',
                color_continuous_scale=px.colors.sequential.Viridis
            )
            fig.update_layout(
                font_family="Outfit, sans-serif",
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=0, r=0, t=10, b=0),
                coloraxis_showscale=False
            )
            st.plotly_chart(fig, use_container_width=True)
            
        with table_col:
            st.markdown("### Adoption Table")
            desc_cars_table = dist_cars_df.sort_values(by='count', ascending=False).copy()
            desc_cars_table.columns = ['State', 'Vehicle Count']
            st.dataframe(
                desc_cars_table,
                use_container_width=True,
                hide_index=True
            )

    # ==================== TAB 2: CHARGING INFRASTRUCTURE ====================
    with tab2:
        # Aggregated distribution by state
        dist_stations_df = stations_df.groupby('state_province').size().reset_index(name='count')
        dist_stations_df = dist_stations_df.sort_values(by='count', ascending=True).reset_index(drop=True)
        
        total_ports = int(stations_df['ports'].fillna(0).sum())
        total_power = stations_df['power_kw'].fillna(0).sum() / 1000.0 # in MW
        
        # Metric Cards Row
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-lbl">Total Charging Stations</div>
                    <div class="metric-val">{len(stations_df):,} <span style="font-size: 1.1rem; color: #3B82F6; font-weight: 500;">({total_ports:,} Ports)</span></div>
                </div>
            """, unsafe_allow_html=True)
            
        with col2:
            if len(dist_stations_df) > 0:
                top_station_row = dist_stations_df.sort_values(by='count', ascending=False).iloc[0]
                top_state = top_station_row['state_province']
                top_count = top_station_row['count']
                top_display = f"{top_state} ({top_count:,})"
            else:
                top_display = "N/A"
                
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-lbl">Top Infrastructure Location</div>
                    <div class="metric-val" style="font-size: 1.8rem; line-height: 2.2rem; padding-top: 0.2rem;">{top_display}</div>
                </div>
            """, unsafe_allow_html=True)
            
        with col3:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-lbl">Total Power Capacity</div>
                    <div class="metric-val">{total_power:.1f} MW</div>
                </div>
            """, unsafe_allow_html=True)
            
        st.markdown("---")
        
        # Visualization Row
        chart_col, table_col = st.columns([2, 1])
        
        with chart_col:
            st.markdown("### Charging Station Distribution by State")
            fig = px.bar(
                dist_stations_df,
                x='count',
                y='state_province',
                orientation='h',
                labels={'count': 'Number of Stations', 'state_province': 'State'},
                color='count',
                color_continuous_scale=px.colors.sequential.Cividis
            )
            fig.update_layout(
                font_family="Outfit, sans-serif",
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=0, r=0, t=10, b=0),
                coloraxis_showscale=False
            )
            st.plotly_chart(fig, use_container_width=True)
            
        with table_col:
            st.markdown("### Infrastructure Table")
            desc_stations_table = dist_stations_df.sort_values(by='count', ascending=False).copy()
            desc_stations_table.columns = ['State', 'Station Count']
            st.dataframe(
                desc_stations_table,
                use_container_width=True,
                hide_index=True
            )

    # ==================== TAB 3: GRID LOAD SIMULATION ====================
    with tab3:
        st.markdown("### ⚡ Coincident Grid Load Simulation")
        st.markdown(
            "This simulation estimates the peak power demand on the utility grid "
            "based on the coincident use of chargers. As the number of ports in a state increases, "
            "the probability of simultaneous peak load decreases (modeled via coincidence factor)."
        )
        
        # Run simulation with sidebar parameters
        sim_df = run_simulation(stations_df, cf_min=cf_min, low_threshold=low_thresh, high_threshold=high_thresh)
        
        # Calculate summary metrics for the simulation
        total_peak_mw = sim_df['coincident_peak_load_kw'].sum() / 1000.0
        high_risk_states = len(sim_df[sim_df['grid_risk_level'] == 'High'])
        avg_cf = sim_df['coincidence_factor'].mean()
        
        # Metric Cards Row
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-lbl">Simulated Peak Grid Load</div>
                    <div class="metric-val">{total_peak_mw:.2f} MW</div>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-lbl">High-Risk States</div>
                    <div class="metric-val" style="color: {'#EF4444' if high_risk_states > 0 else '#1F2937'};">{high_risk_states}</div>
                </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-lbl">Average Coincidence Factor</div>
                    <div class="metric-val">{avg_cf:.2%}</div>
                </div>
            """, unsafe_allow_html=True)
            
        st.markdown("---")
        
        # Visualization Row
        chart_col, table_col = st.columns([2, 1])
        
        with chart_col:
            st.markdown("### Peak Grid Load & Risk Level by State")
            
            # Map risk level to premium color mapping
            risk_colors = {'High': '#EF4444', 'Medium': '#F59E0B', 'Low': '#10B981'}
            
            # Use sort ascending for horizontal bar chart
            sorted_sim_df = sim_df.sort_values(by='coincident_peak_load_kw', ascending=True).copy()
            
            fig = px.bar(
                sorted_sim_df,
                x='coincident_peak_load_kw',
                y='state_province',
                orientation='h',
                labels={'coincident_peak_load_kw': 'Peak Load (kW)', 'state_province': 'State'},
                color='grid_risk_level',
                color_discrete_map=risk_colors,
                category_orders={'grid_risk_level': ['Low', 'Medium', 'High']}
            )
            
            fig.update_layout(
                font_family="Outfit, sans-serif",
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=0, r=0, t=10, b=0),
                legend=dict(title=dict(text='Grid Risk Level'), orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig, use_container_width=True)
            
        with table_col:
            st.markdown("### Grid Risk Summary")
            
            display_sim_df = sim_df[[
                'state_province', 'total_ports', 'installed_capacity_kw', 'coincident_peak_load_kw', 'grid_risk_level'
            ]].copy()
            display_sim_df.columns = ['State', 'Ports', 'Capacity (kW)', 'Peak Load (kW)', 'Risk Level']
            
            st.dataframe(
                display_sim_df,
                use_container_width=True,
                hide_index=True
            )

except Exception as e:
    st.error(f"Error loading dashboard data: {e}")
