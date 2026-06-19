import os
import sys
import pandas as pd
import streamlit as st
import plotly.express as px

# Ensure the root directory is in the path so we can import from src
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_dir not in sys.path:
    sys.path.append(root_dir)

from src.demand_analysis import load_data, CLEANED_CARS_PATH
from src.data_cleaning import PROCESSED_STATIONS_PATH
from src.load_simulation import run_simulation, map_capacity_rating

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
    
    # Extract unique states for filters
    all_states = sorted(list(set(cars_df['state'].dropna().unique().tolist()) | set(stations_df['state_province'].dropna().unique().tolist())))
    
    # 5. Sidebar Layout & Filters
    st.sidebar.image("app/assets/electric-car.png", width=120)
    st.sidebar.markdown("### EV & Hybrid Planner Filters")
    
    selected_state = st.sidebar.selectbox("Select State:", ["All States"] + all_states)
    charger_filter = st.sidebar.selectbox("Select Charger Type:", ["All", "AC only", "DC Fast/Ultra only"])
    selected_risk = st.sidebar.selectbox("Select Grid Risk Level:", ["All Levels", "Low", "Medium", "High"])
    
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
    
    # 6. Apply Data Filtering & Recalculate Simulation
    
    # Apply charger type filter
    filtered_stations = stations_df.copy()
    if charger_filter == "AC only":
        filtered_stations = filtered_stations[filtered_stations['is_fast_dc'] == False]
    elif charger_filter == "DC Fast/Ultra only":
        filtered_stations = filtered_stations[filtered_stations['is_fast_dc'] == True]
        
    # Run simulation on filtered stations
    sim_df = run_simulation(filtered_stations, cf_min=cf_min, low_threshold=low_thresh, high_threshold=high_thresh)
    
    # Apply state filter to simulation
    if selected_state != "All States":
        sim_df = sim_df[sim_df['state_province'] == selected_state]
        
    # Apply risk level filter to simulation
    if selected_risk != "All Levels":
        sim_df = sim_df[sim_df['grid_risk_level'] == selected_risk]
        
    # Filter cars df based on state
    filtered_cars = cars_df.copy()
    if selected_state != "All States":
        filtered_cars = filtered_cars[filtered_cars['state'] == selected_state]
        
    # Filter stations df for map based on state & active risk levels
    map_stations = filtered_stations.copy()
    if selected_state != "All States":
        map_stations = map_stations[map_stations['state_province'] == selected_state]
    valid_states = set(sim_df['state_province'].tolist())
    map_stations = map_stations[map_stations['state_province'].isin(valid_states)]
    
    # Calculate top level KPI metrics
    total_evs = len(filtered_cars)
    total_stations = len(map_stations)
    total_ports = int(map_stations['ports'].sum())
    ratio = total_evs / total_ports if total_ports > 0 else 0.0
    
    # 7. Render KPI cards row at the top of the app
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    with kpi_col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-lbl">Total EVs & Hybrids</div>
                <div class="metric-val">{total_evs:,}</div>
            </div>
        """, unsafe_allow_html=True)
    with kpi_col2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-lbl">Charging Stations</div>
                <div class="metric-val">{total_stations:,}</div>
            </div>
        """, unsafe_allow_html=True)
    with kpi_col3:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-lbl">Charger Ports</div>
                <div class="metric-val">{total_ports:,}</div>
            </div>
        """, unsafe_allow_html=True)
    with kpi_col4:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-lbl">EV-to-Port Ratio</div>
                <div class="metric-val">{ratio:.1f}</div>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Create Tabs for the four segments
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Dashboard Overview", 
        "🚗 EV & Hybrid Adoption", 
        "🔌 Interactive Map View", 
        "⚡ Grid Load Simulation"
    ])
    
    # ==================== TAB 1: DASHBOARD OVERVIEW ====================
    with tab1:
        st.markdown("### 📊 System Overview & Risk Analysis")
        st.markdown(
            "This tab provides a summary of grid risk distribution across states "
            "and defines how risk levels are classified based on simulated peak demand."
        )
        
        st.markdown("---")
        
        # Risk classification details
        st.markdown("#### ℹ️ Grid Risk Level Definitions")
        risk_desc_col1, risk_desc_col2, risk_desc_col3 = st.columns(3)
        with risk_desc_col1:
            st.success("**🟢 Low Risk** (< 500 kW)\n\nCharging demand and peak coincident load are within standard utility margins. Minor to no local grid capacity upgrades needed.")
        with risk_desc_col2:
            st.warning("**🟡 Medium Risk** (500 kW - 1,500 kW)\n\nEstimated peak load is increasing. Local infrastructure should be monitored for potential congestion during peak hours.")
        with risk_desc_col3:
            st.error("**🔴 High Risk** (>= 1,500 kW)\n\nEstimated coincident peak load is high. Location may require electrical capacity review, feeder additions, or smart charging management.")
            
        st.markdown("---")
        
        # Risk distribution chart & table
        chart_c, table_c = st.columns([2, 1])
        with chart_c:
            st.markdown("#### State-Level Grid Risk Distribution")
            if not sim_df.empty:
                # Group by risk level
                risk_counts = sim_df['grid_risk_level'].value_counts().reset_index()
                risk_counts.columns = ['Risk Level', 'Number of States']
                
                # Make sure all levels exist
                for lvl in ['Low', 'Medium', 'High']:
                    if lvl not in risk_counts['Risk Level'].values:
                        risk_counts = pd.concat([risk_counts, pd.DataFrame([{'Risk Level': lvl, 'Number of States': 0}])], ignore_index=True)
                
                risk_counts['order'] = risk_counts['Risk Level'].map({'Low': 1, 'Medium': 2, 'High': 3})
                risk_counts = risk_counts.sort_values(by='order').drop(columns='order')
                
                fig_risk = px.bar(
                    risk_counts,
                    x='Risk Level',
                    y='Number of States',
                    color='Risk Level',
                    color_discrete_map={'High': '#EF4444', 'Medium': '#F59E0B', 'Low': '#10B981'},
                    category_orders={'Risk Level': ['Low', 'Medium', 'High']}
                )
                fig_risk.update_layout(
                    font_family="Outfit, sans-serif",
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    margin=dict(l=0, r=0, t=10, b=0),
                    showlegend=False
                )
                st.plotly_chart(fig_risk, use_container_width=True)
            else:
                st.warning("No data matches active filters.")
                
        with table_c:
            st.markdown("#### Locations Overview")
            if not sim_df.empty:
                overview_table = sim_df[['state_province', 'grid_risk_level']].copy()
                overview_table.columns = ['State', 'Risk Level']
                st.dataframe(
                    overview_table,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "State": st.column_config.TextColumn("State"),
                        "Risk Level": st.column_config.TextColumn("Risk Level")
                    }
                )
            else:
                st.warning("No data available.")

    # ==================== TAB 2: EV & HYBRID ADOPTION ====================
    with tab2:
        st.markdown("### 🚗 EV & Hybrid Adoption Analysis")
        
        # Aggregated distribution by state
        dist_cars_df = filtered_cars.groupby('state').size().reset_index(name='count')
        dist_cars_df = dist_cars_df.sort_values(by='count', ascending=True).reset_index(drop=True)
        
        # Visualization Row
        chart_col, table_col = st.columns([2, 1])
        
        with chart_col:
            st.markdown("#### Vehicle Distribution by State")
            if not dist_cars_df.empty:
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
            else:
                st.warning("No registration records match current filters.")
            
        with table_col:
            st.markdown("#### Adoption Table")
            if not dist_cars_df.empty:
                desc_cars_table = dist_cars_df.sort_values(by='count', ascending=False).copy()
                desc_cars_table.columns = ['State', 'Vehicle Count']
                st.dataframe(
                    desc_cars_table,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "State": st.column_config.TextColumn("State", help="Malaysian state name."),
                        "Vehicle Count": st.column_config.NumberColumn("Vehicle Count", format="%d", help="Clean registered EV & Hybrid vehicle count.")
                    }
                )
            else:
                st.warning("No data available.")

    # ==================== TAB 3: INTERACTIVE MAP VIEW ====================
    with tab3:
        st.markdown("### 🔌 Interactive Charging Infrastructure Map")
        st.markdown(
            "Hover over a station marker to view details. Marker size reflects the number of ports, "
            "and marker color reflects the simulated load risk of its state."
        )
        
        if not map_stations.empty:
            state_risk_map = dict(zip(sim_df['state_province'], sim_df['grid_risk_level']))
            map_stations['state_risk'] = map_stations['state_province'].map(state_risk_map).fillna('Low')
            
            map_stations['power_kw'] = map_stations.apply(
                lambda r: map_capacity_rating(r.get('power_kw'), r.get('power_class'), r.get('is_fast_dc')),
                axis=1
            )
            
            fig_map = px.scatter_mapbox(
                map_stations,
                lat="latitude",
                lon="longitude",
                hover_name="name",
                hover_data={"latitude": False, "longitude": False, "ports": True, "power_kw": True, "state_risk": True},
                color="state_risk",
                color_discrete_map={'High': '#EF4444', 'Medium': '#F59E0B', 'Low': '#10B981'},
                category_orders={'state_risk': ['Low', 'Medium', 'High']},
                size="ports",
                size_max=15,
                zoom=5,
                height=600,
                mapbox_style="open-street-map"
            )
            
            fig_map.update_layout(
                font_family="Outfit, sans-serif",
                margin=dict(l=0, r=0, t=0, b=0),
                legend=dict(title=dict(text='State Risk Level'), orientation="h", yanchor="bottom", y=0.01, xanchor="left", x=0.01)
            )
            st.plotly_chart(fig_map, use_container_width=True)
            
            # Detailed stations table
            st.markdown("#### Charger Station Details")
            display_stations = map_stations[['name', 'city', 'state_province', 'ports', 'power_kw', 'power_class', 'is_fast_dc']].copy()
            display_stations.columns = ['Name', 'City', 'State', 'Ports', 'Power (kW)', 'Power Class', 'DC Fast?']
            st.dataframe(
                display_stations.sort_values(by='Ports', ascending=False),
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Name": st.column_config.TextColumn("Name"),
                    "City": st.column_config.TextColumn("City"),
                    "State": st.column_config.TextColumn("State"),
                    "Ports": st.column_config.NumberColumn("Ports", format="%d"),
                    "Power (kW)": st.column_config.NumberColumn("Power (kW)", format="%.1f"),
                    "Power Class": st.column_config.TextColumn("Power Class"),
                    "DC Fast?": st.column_config.BooleanColumn("DC Fast?")
                }
            )
        else:
            st.warning("No charging stations match the current filter selection.")

    # ==================== TAB 4: GRID LOAD SIMULATION ====================
    with tab4:
        st.markdown("### ⚡ Coincident Grid Load Simulation")
        st.markdown(
            "This simulation estimates the peak power demand on the utility grid "
            "based on the coincident use of chargers. As the number of ports in a state increases, "
            "the probability of simultaneous peak load decreases (modeled via coincidence factor)."
        )
        
        if not sim_df.empty:
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
                
            # Explainer container for grid risk levels
            with st.expander("ℹ️ Understanding Coincidence Factors", expanded=False):
                st.markdown("""
                    **What is the Coincidence Factor?**
                    The coincidence factor represents the probability that multiple chargers draw peak power simultaneously. As the number of ports in a state grows, this factor decreases non-linearly (from 100% down to the user-defined baseline), since it is highly unlikely that all chargers operate at maximum capacity at the exact same moment.
                """)
                
            st.markdown("---")
            
            # Visualization Row
            chart_col, table_col = st.columns([2, 1])
            
            with chart_col:
                st.markdown("#### Peak Grid Load by State")
                
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
                st.markdown("#### Grid Risk Summary")
                
                display_sim_df = sim_df[[
                    'state_province', 'total_ports', 'installed_capacity_kw', 'coincident_peak_load_kw', 'grid_risk_level'
                ]].copy()
                display_sim_df.columns = ['State', 'Ports', 'Capacity (kW)', 'Peak Load (kW)', 'Risk Level']
                
                st.dataframe(
                    display_sim_df,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "State": st.column_config.TextColumn("State", help="Malaysian state name."),
                        "Ports": st.column_config.NumberColumn("Ports", format="%d", help="Total charging ports available."),
                        "Capacity (kW)": st.column_config.NumberColumn("Capacity (kW)", format="%.1f", help="Total raw capacity summed."),
                        "Peak Load (kW)": st.column_config.NumberColumn("Peak Load (kW)", format="%.1f", help="Simulated coincident peak load."),
                        "Risk Level": st.column_config.TextColumn("Risk Level", help="Grid load risk classification.")
                    }
                )
        else:
            st.warning("No simulation matches active filters.")

except Exception as e:
    st.error(f"Error loading dashboard data: {e}")
