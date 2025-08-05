import streamlit as st
from supabase_client import supabase
from datetime import date

st.set_page_config(page_title="WhatsUpChuck", layout="centered")

st.title("🎸 WhatsUpChuck – Local Live Entertainment")

menu = st.sidebar.radio("Menu", ["Search Events", "Submit Event"])

if menu == "Search Events":
    st.subheader("🔍 Search Events")
    city = st.text_input("Search by city")
    artist = st.text_input("Search by artist")
    venue = st.text_input("Search by venue")

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
    data = query.order("event_date", desc=False).execute()

    if data.data:
        for row in data.data:
            st.markdown(f"### {row['artist_name']}")
            st.write(f"📍 {row['venue_name']}, {row['city']}")
            st.write(f"📅 {row['event_date']}")
            if row.get("flyer_url"):
                st.image(row["flyer_url"], width=300)
            st.markdown("---")
    else:
        st.info("No events found. Try different filters.")

elif menu == "Submit Event":
    st.subheader("📥 Submit a New Event")

    with st.form("event_form"):
        artist = st.text_input("Artist Name")
        venue = st.text_input("Venue Name")
        city = st.text_input("City")
        event_date = st.date_input("Event Date", value=date.today())
        flyer_url = st.text_input("Flyer Image URL (optional)")
        submitted = st.form_submit_button("Submit Event")

        if submitted:
            if not artist or not venue or not city:
                st.error("Please fill out all required fields.")
            else:
                supabase.table("events").insert({
                    "artist_name": artist,
                    "venue_name": venue,
                    "city": city,
                    "event_date": str(event_date),
                    "flyer_url": flyer_url or None
                }).execute()
                st.success("Event submitted successfully!")
