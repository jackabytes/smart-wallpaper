import hashlib
import json
from datetime import datetime
from zoneinfo import ZoneInfo
CONFIG_FILE = "config.json"
OUTPUT_FILE = "wallpaper.json"
def load_config():
    with open(CONFIG_FILE, "r", encoding="utf-8") as file:
        return json.load(file)
def time_to_minutes(value):
    hour, minute = map(int, value.split(":"))
    return hour * 60 + minute
def get_current_time(config):
    timezone_name = config["location"]["timezone"]
    return datetime.now(ZoneInfo(timezone_name))
def get_period(config, now):
    current = now.hour * 60 + now.minute
    schedule = config["schedule"]
    for period, settings in schedule.items():
        start = time_to_minutes(settings["start"])
        end = time_to_minutes(settings["end"])
        if start < end:
            if start <= current < end:
                return period
        else:
            # Period crosses midnight.
            if current >= start or current < end:
                return period
    return "night"
def choose_video(config, period, now):
    videos = config["wallpapers"].get(period, [])
    if not videos:
        raise ValueError(
            f"No wallpapers configured for period: {period}"
        )
    # Keep the selected video stable for the entire period.
    #
    # The GitHub workflow runs every 15 minutes, so using random.choice()
    # would otherwise potentially change the video every workflow run.
    #
    # The date + period produces a repeatable selection for that period.
    selection_key = f"{now.date().isoformat()}-{period}"
    digest = hashlib.sha256(
        selection_key.encode("utf-8")
    ).hexdigest()
    index = int(digest, 16) % len(videos)
    return videos[index]
def generate_wallpaper():
    config = load_config()
    now = get_current_time(config)
    period = get_period(config, now)
    video_url = choose_video(
        config,
        period,
        now
    )
    wallpaper = [
        {
            "title": period.capitalize(),
            "url_1080p": video_url
        }
    ]
    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            wallpaper,
            file,
            indent=2
        )
    print(
        f"Time: {now.strftime('%Y-%m-%d %H:%M:%S %Z')}"
    )
    print(
        f"Period: {period}"
    )
    print(
        f"Wallpaper: {video_url}"
    )
if __name__ == "__main__":
    generate_wallpaper()