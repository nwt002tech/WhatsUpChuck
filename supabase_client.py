from supabase import create_client

# Replace with your actual Supabase project details
url = "https://oqdaycsyoaovxahylgui.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9xZGF5Y3N5b2FvdnhhaHlsZ3VpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQzNTgyNzMsImV4cCI6MjA2OTkzNDI3M30.wl6nyktfkQMAuh9bcjXnSwAB2Mr9qN9zVLTj-rs7Gws"

supabase = create_client(url, key)
