from supabase import create_client
from datetime import datetime, timezone

url = "https://qtayzkwelmrltrxgcoie.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF0YXl6a3dlbG1ybHRyeGdjb2llIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTIyNTYyMjEsImV4cCI6MjA2NzgzMjIyMX0.eR8ywE99kqL5O29faRYCEvmt9NC04ov1BjOILZQk_-g"

supabase = create_client(url, key)

data = {
    "height": 170.0,
    "weight": 65.0,
    "temperature": 36.5,
    "blood_pressure": 120.0,
    "blood_oxygen": 98.0,
    "body_fat_percent": 20.0,
    "bmi": 22.5,
    "label": 0,
    "timestamp": datetime.now(timezone.utc).isoformat()
}

response = supabase.table("user_data").insert(data).execute()
print(response)

