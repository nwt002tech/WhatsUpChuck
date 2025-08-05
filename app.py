import streamlit as st
from datetime import date
from supabase_client import supabase

st.set_page_config(page_title="WhatsUpChuck", layout="wide")
st.markdown(
    "<h1 style='text-align: center; color: #f63366;'>🎸 WhatsUpChuck</h1>"
    "<p style='text-align: center; font-size: 18px;'>Find Local Live Entertainment</p>",
    unsafe_allow_html=True
)

# Optional test connection check
try:
    test = supabase.table("events").select("*").limit(1).execute()
    st.success("✅ Connected to Supabase")
except Exception as e:
    st.error(f"❌ Supabase connection failed: {e}")
    st.stop()

st.markdown("---")

menu = st.sidebar.radio("📋 Menu", ["🔍 Search Events", "📥 Submit Event"])

if menu == "🔍 Search Events":
    st.subheader("🎯 Filter Events")
    with st.container():
        col1, col2, col3 = st.columns(3)
        with col1:
            city = st.text_input("Search by City")
        with col2:
            artist = st.text_input("Search by Artist")
        with col3:
            venue = st.text_input("Search by Venue")

    filters = []
    if city:
        filters.append(("city", "ilike", f"%{city}%"))
    if artist:
        filters.append(("artist_name", "ilike", f"%{artist}%"))
    if venue:
        filters.append(("venue_name", "ilike", f"%{venue}%"))

    query = supabase.table("events")
    for f in filters:
        query = query.filter(*f)

    try:
        data = query.select("*").order("event_date", desc=False).execute()
    except Exception as e:
        st.error(f"Error fetching events: {e}")
        st.stop()

    st.markdown("### 🎵 Upcoming Events")
    if data and data.data:
        for row in data.data:
            with st.container():
                st.markdown(f"<h4 style='margin-bottom: 0;'>{row['artist_name']}</h4>", unsafe_allow_html=True)
                st.markdown(
                    f"📍 <strong>{row['venue_name']}</strong>, {row['city']}  <br/>"
                    f"📅 {row['event_date']}",
                    unsafe_allow_html=True
                )
                if row.get("flyer_url"):
                    st.image(row["flyer_url"], use_column_width=True)
                st.markdown("<hr style='border-top: 1px solid #ccc;'>", unsafe_allow_html=True)
    else:
        st.info("No events found. Try different filters.")

elif menu == "📥 Submit Event":
    st.subheader("📅 Submit a New Event")
    st.markdown("Fill in the details below to add your local event.")

    with st.form("event_form"):
        artist = st.text_input("Artist Name")
        venue = st.text_input("Venue Name")
        city = st.text_input("City")
        event_date = st.date_input("Event Date", value=date.today())
        flyer_url = st.text_input("Flyer Image URL (optional)")
        submitted = st.form_submit_button("Submit Event")

        if submitted:
            if not artist or not venue or not city:
                st.error("⚠️ Please fill out all required fields.")
            else:
                try:
                    supabase.table("events").insert({
                        "artist_name": artist,
                        "venue_name": venue,
                        "city": city,
                        "event_date": str(event_date),
                        "flyer_url": flyer_url or None
                    }).execute()
                    st.success("🎉 Your event has been submitted!")
                except Exception as e:
                    st.error(f"❌ Error submitting event: {e}")
