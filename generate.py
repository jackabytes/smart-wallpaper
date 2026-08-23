import json
from datetime import datetime
from zoneinfo import ZoneInfo
from astral import LocationInfo
from astral.sun import sun


# Load configuration
with open("config.json", "r") as file:
    config = json.load(file)


# Location
latitude = config["location"]["latitude"]
longitude = config["location"]["longitude"]
timezone = config["location"]["timezone"]

location = LocationInfo(
    name="Wallpaper",
    region="",
    timezone=timezone,
    latitude=latitude,
    longitude=longitude
)


# Current local time
local_tz = ZoneInfo(timezone)
now = datetime.now(local_tz)


# Today's sunrise and sunset
solar = sun(
    location.observer,
    date=now.date(),
    tzinfo=local_tz
)


sunrise = solar["sunrise"]
sunset = solar["sunset"]


# Work out whether it is currently day or night
test_mode = config.get("solar", {}).get("testMode")

if test_mode == "day":
    wallpaper = config["wallpapers"]["day"]
    title = "Day"
elif test_mode == "night":
    wallpaper = config["wallpapers"]["night"]
    title = "Night"
elif sunrise <= now < sunset:
    wallpaper = config["wallpapers"]["day"]
    title = "Day"
else:
    wallpaper = config["wallpapers"]["night"]
    title = "Night"


# Create Projectivy wallpaper feed
output = [

    {

        "title": title,

        "url_1080p": wallpaper

    }

]


# Write wallpaper.json
with open("wallpaper.json", "w") as file:
    json.dump(output, file, indent=2)


print(f"Local time: {now}")
print(f"Sunrise:    {sunrise}")
print(f"Sunset:     {sunset}")
print(f"Wallpaper:  {title}")
