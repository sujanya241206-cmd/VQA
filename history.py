import streamlit as st
import sys
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Add parent directory to path
#sys.path.append(str(Path(__file__).parent.parent))

from storage import StorageManager

# Page configuration
#st.set_page_config(
#    page_title="History & Analytics",
#    page_icon="📊",
#    layout="wide"
#)

# Load CSS
def load_css():
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #1e1e2e 0%, #2d1b3d 50%, #1a1a2e 100%);
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e1e2e 0%, #2d1b3d 100%);
    }
    
    .card {
        background: rgba(255, 255, 255, 0.05);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin: 1rem 0;
    }
    
    .main-header {
        text-align: center;
        color: #ffffff;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .sub-header {
        text-align: center;
        color: #b8b8d0;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    h1, h2, h3 {
        color: #ffffff !important;
    }
    
    p, label, .stMarkdown {
        color: #e0e0e0 !important;
    }
    
    [data-testid="stMetricValue"] {
        color: #667eea;
        font-size: 2rem;
    }
    
    .stDataFrame {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

load_css()

# Initialize storage manager
storage_manager = StorageManager()

# Check authentication
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login to access this page")
    st.stop()

def main():
    st.markdown('<h1 class="main-header">History & Analytics</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">View your past interactions and insights</p>', unsafe_allow_html=True)
    
    # Get user statistics
    stats = storage_manager.get_statistics(st.session_state.username)
    
    # Display metrics
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Queries",
            stats['total_queries']
        )
    
    with col2:
        st.metric(
            "Average Confidence",
            f"{stats['average_confidence']:.1%}" if stats['average_confidence'] > 0 else "N/A"
        )
    
    with col3:
        st.metric(
            "Unique Images",
            stats['unique_images']
        )
    
    with col4:
        if stats['most_recent']:
            st.metric(
                "Last Activity",
                stats['most_recent']
            )
        else:
            st.metric("Last Activity", "N/A")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Get user history
    df = storage_manager.get_history_dataframe(st.session_state.username)
    
    if not df.empty:
        # Analytics section
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Analytics")
        
        tab1, tab2 = st.tabs(["Queries Over Time", "Confidence Analysis"])
        
        with tab1:
            # Queries over time
            if 'timestamp' in df.columns:
                df['date'] = pd.to_datetime(df['timestamp']).dt.date
                queries_by_date = df.groupby('date').size().reset_index(name='count')
                
                fig = px.line(
                    queries_by_date,
                    x='date',
                    y='count',
                    title='Number of Queries Over Time',
                    labels={'date': 'Date', 'count': 'Number of Queries'}
                )
                
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='#e0e0e0',
                    title_font_color='#ffffff',
                    xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                    yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
                )
                
                fig.update_traces(line_color='#667eea')
                
                st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            # Confidence distribution
            if 'confidence' in df.columns:
                fig = px.histogram(
                    df,
                    x='confidence',
                    nbins=20,
                    title='Confidence Score Distribution',
                    labels={'confidence': 'Confidence Score', 'count': 'Frequency'}
                )
                
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='#e0e0e0',
                    title_font_color='#ffffff',
                    xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                    yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
                )
                
                fig.update_traces(marker_color='#764ba2')
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Average confidence over time
                if 'timestamp' in df.columns:
                    df['date'] = pd.to_datetime(df['timestamp']).dt.date
                    avg_conf_by_date = df.groupby('date')['confidence'].mean().reset_index()
                    
                    fig2 = px.line(
                        avg_conf_by_date,
                        x='date',
                        y='confidence',
                        title='Average Confidence Over Time',
                        labels={'date': 'Date', 'confidence': 'Average Confidence'}
                    )
                    
                    fig2.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font_color='#e0e0e0',
                        title_font_color='#ffffff',
                        xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                        yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
                    )
                    
                    fig2.update_traces(line_color='#667eea')
                    
                    st.plotly_chart(fig2, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # History table
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Interaction History")
        
        # Prepare display dataframe
        display_df = df.copy()
        
        if 'timestamp' in display_df.columns:
            display_df['timestamp'] = pd.to_datetime(display_df['timestamp']).dt.strftime('%Y-%m-%d %H:%M')
        
        # Select columns to display
        columns_to_show = ['id', 'image_name', 'question', 'answer', 'confidence', 'timestamp']
        columns_to_show = [col for col in columns_to_show if col in display_df.columns]
        
        # Sort by timestamp descending
        if 'timestamp' in display_df.columns:
            display_df = display_df.sort_values('timestamp', ascending=False)
        
        st.dataframe(
            display_df[columns_to_show],
            use_container_width=True,
            hide_index=True
        )
        
        # Export options
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col2:
            csv = display_df.to_csv(index=False)
            st.download_button(
                "Download CSV",
                csv,
                "vqa_history.csv",
                "text/csv",
                use_container_width=True
            )
        
        with col3:
            if st.button("Clear History", use_container_width=True):
                if st.session_state.get('confirm_clear', False):
                    storage_manager.clear_user_history(st.session_state.username)
                    st.success("History cleared!")
                    st.session_state.confirm_clear = False
                    st.rerun()
                else:
                    st.session_state.confirm_clear = True
                    st.warning("Click again to confirm")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Story history section
        story_df = df[df['story'].notna()] if 'story' in df.columns else pd.DataFrame()
        
        if not story_df.empty:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### Generated Stories")
            
            for idx, row in story_df.iterrows():
                with st.expander(f"{row['image_name']} - {row['story_style']} ({row['timestamp']})"):
                    st.markdown(f"**Style:** {row['story_style']}")
                    st.markdown("**Story:**")
                    st.write(row['story'])
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    else:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.info("No history available yet. Start using the VQA page to see your interactions here!")
        st.markdown('</div>', unsafe_allow_html=True)

#if __name__ == "__main__":
#   main()
