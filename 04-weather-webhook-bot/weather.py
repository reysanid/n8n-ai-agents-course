import requests
city = input ("نام شهر را وارد کنید: ") 
url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
response = requests.get(url)
data = response.json()
first_result = data["results"][0]
lat = first_result["latitude"]
lon = first_result["longitude"]
weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
weather_response = requests.get(weather_url)
weather_data = weather_response.json()
temperature = weather_data["current_weather"]["temperature"]
print(f"شهر: {city}, دما: {temperature}")
api_key = "mysecrettoken123"
headers = {"Authorization": f"Bearer {api_key}"}
payload = {"city": city, "temperature": temperature}
post_response = requests.post("https://postman-echo.com/post", json=payload, headers=headers)
print(post_response.json())
webhook_response = requests.post("https://webhook.site/b2cc5168-a532-4734-b16d-80279d374215", json=payload)
print("وضعیت ارسال به webhook:", webhook_response.status_code)
