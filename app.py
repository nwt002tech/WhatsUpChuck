import streamlit as st
from supabase_client import supabase
from datetime import date, timedelta
import time

# Modern page config
st.set_page_config(
    page_title="WhatsUpChuck",
    page_icon="🎸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS for modern cards and responsive design
st.markdown("""
<style>
    .card {
        background-color: #192841;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        transition: transform 0.3s;
    }
    .card:hover {
        transform: translateY(-5px);
    }
    .event-date {
        background: #8A2BE2;
        color: white !important;
        border-radius: 5px;
        padding: 5px 10px;
        display: inline-block;
        font-weight: bold;
    }
    @media (max-width: 768px) {
        .stColumn {
            width: 100% !important;
        }
        [data-testid="column"] {
            width: 100% !important;
            flex: unset !important;
        }
    }
    .stButton>button {
        background: linear-gradient(45deg, #8A2BE2, #4B0082) !important;
        color: white !important;
        border: none;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.05);
    }
    .stTextInput>div>div>input {
        background-color: #0E1117 !important;
        color: white !important;
    }
    .stDateInput>div>div>input {
        background-color: #0E1117 !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("🎸 WhatsUpChuck")
st.caption("Discover local live entertainment")

# Modern sidebar with icons
with st.sidebar:
    st.title("Navigation")
    menu = st.radio("", ["🔍 Search Events", "📥 Submit Event"], label_visibility="collapsed")

# Search Events Section
if "🔍 Search Events" in menu:
    st.subheader("Find Live Events")
    
    # Responsive filter columns
    col1, col2, col3 = st.columns([1,1,1], gap="small")
    with col1:
        city = st.text_input("📍 City")
    with col2:
        artist = st.text_input("🎤 Artist")
    with col3:
        venue = st.text_input("🏟️ Venue")
    
    # Date range filter
    today = date.today()
    next_month = today + timedelta(days=30)
    date_range = st.date_input("📅 Date Range", (today, next_month))
    
    # Search button with loading state
    if st.button("Search", use_container_width=True):
        with st.spinner("Finding events..."):
            try:
                # Initialize query
                query = supabase.table("events")
                
                # Apply text filters
                if city:
                    query = query.filter("city", "ilike", f"%{city}%")
                if artist:
                    query = query.filter("artist_name", "ilike", f"%{artist}%")
                if venue:
                    query = query.filter("venue_name", "ilike", f"%{venue}%")
                
                # Apply date range filter
                if len(date_range) == 2:
                    start_date, end_date = date_range
                    query = query.filter("event_date", "gte", str(start_date))
                    query = query.filter("event_date", "lte", str(end_date))
                
                # Execute query
                data = query.order("event_date", desc=False).execute()
                events = data.data
                
                if not events:
                    st.info("No events found. Try different filters.")
                    st.stop()
                    
                # Responsive card layout
                cols = st.columns(3)
                for i, row in enumerate(events):
                    with cols[i % 3]:
                        with st.container():
                            st.markdown(f"<div class='card'>", unsafe_allow_html=True)
                            
                            # Date badge
                            st.markdown(f"<div class='event-date'>{row['event_date']}</div>", 
                                       unsafe_allow_html=True)
                            
                            # Artist header
                            st.subheader(f"{row['artist_name']}")
                            
                            # Venue info
                            st.markdown(f"📍 **{row['venue_name']}**, {row['city']}")
                            
                            # Flyer image
                            if row.get("flyer_url"):
                                st.image(row["flyer_url"], use_column_width=True)
                            
                            st.markdown("</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error fetching events: {str(e)}")

# Submit Event Section
else:
    st.subheader("Submit New Event")
    
    with st.form("event_form", clear_on_submit=True):
        # Responsive form layout
        col1, col2 = st.columns(2)
        with col1:
            artist = st.text_input("Artist Name*", placeholder="Enter artist/band name")
            venue = st.text_input("Venue Name*", placeholder="Enter venue name")
            city = st.text_input("City*", placeholder="Enter city")
        with col2:
            event_date = st.date_input("Event Date*", value=date.today())
            flyer_url = st.text_input("Flyer Image URL", placeholder="https://...")
        
        # Form validation
        submitted = st.form_submit_button("Submit Event", type="primary")
        if submitted:
            if not artist or not venue or not city:
                st.error("Please fill all required fields (*)")
            else:
                # Show loading animation
                with st.spinner("Submitting..."):
                    try:
                        supabase.table("events").insert({
                            "artist_name": artist,
                            "venue_name": venue,
                            "city": city,
                            "event_date": str(event_date),
                            "flyer_url": flyer_url or None
                        }).execute()
                        time.sleep(1.5)  # Simulate processing
                        st.success("Event submitted successfully! 🎉")
                    except Exception as e:
                        st.error(f"Error submitting event: {str(e)}")