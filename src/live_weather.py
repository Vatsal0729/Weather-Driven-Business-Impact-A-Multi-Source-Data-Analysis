"""
Live Weather Intelligence Engine
Integrates real-time meteorological feeds and 7-day forecasts from the Open-Meteo API.
Computes real-time econometric nowcasting and multi-day forward business projections.
"""

import urllib.request
import json
import datetime
import pandas as pd
from typing import Dict, Any, Tuple, List

# Operational Hub Coordinates & Timezones
CITY_GEO = {
    "NYC": {"name": "New York City", "lat": 40.7128, "lon": -74.0060, "timezone": "America/New_York"},
    "ORD": {"name": "Chicago", "lat": 41.8781, "lon": -87.6298, "timezone": "America/Chicago"},
    "SEA": {"name": "Seattle", "lat": 47.6062, "lon": -122.3321, "timezone": "America/Los_Angeles"},
    "PHX": {"name": "Phoenix", "lat": 33.4484, "lon": -112.0740, "timezone": "America/Phoenix"}
}

# WMO Weather Interpretation Codes
WMO_DESCRIPTIONS = {
    0: "Clear Sky",
    1: "Mainly Clear",
    2: "Partly Cloudy",
    3: "Overcast",
    45: "Foggy",
    48: "Depositing Rime Fog",
    51: "Light Drizzle",
    53: "Moderate Drizzle",
    55: "Dense Drizzle",
    61: "Slight Rain",
    63: "Moderate Rain",
    65: "Heavy Downpour",
    71: "Slight Snow Fall",
    73: "Moderate Snow Fall",
    75: "Heavy Snow Fall",
    77: "Snow Grains",
    80: "Slight Rain Showers",
    81: "Moderate Rain Showers",
    82: "Violent Rain Showers",
    85: "Slight Snow Showers",
    86: "Heavy Snow Showers",
    95: "Thunderstorm",
    96: "Thunderstorm with Slight Hail",
    99: "Thunderstorm with Heavy Hail"
}

def decode_wmo_code(code: int) -> str:
    """Map WMO numeric code to standard human-readable text."""
    return WMO_DESCRIPTIONS.get(code, "Variable Weather")


def fetch_live_weather(city_code: str) -> Dict[str, Any]:
    """
    Fetch live weather telemetry and 7-day daily forecast from Open-Meteo.
    Includes fallback heuristics in case of connection interruptions.
    """
    geo = CITY_GEO.get(city_code, CITY_GEO["NYC"])
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={geo['lat']}&longitude={geo['lon']}&"
        f"current=temperature_2m,relative_humidity_2m,precipitation,weather_code,wind_speed_10m&"
        f"daily=temperature_2m_max,temperature_2m_min,precipitation_sum,weather_code,wind_speed_10m_max&"
        f"timezone={urllib.parse.quote(geo['timezone'])}&"
        f"forecast_days=7"
    )

    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "WeatherBusinessImpactEDA/2.0 (Academic/Analytics Pipeline)"}
        )
        with urllib.request.urlopen(req, timeout=8) as response:
            raw_data = json.loads(response.read().decode("utf-8"))

        current_raw = raw_data.get("current", {})
        daily_raw = raw_data.get("daily", {})

        current_cond = decode_wmo_code(current_raw.get("weather_code", 0))
        current_data = {
            "city_code": city_code,
            "city_name": geo["name"],
            "timestamp": current_raw.get("time", datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")),
            "temperature_c": float(current_raw.get("temperature_2m", 18.0)),
            "humidity_pct": float(current_raw.get("relative_humidity_2m", 50.0)),
            "precipitation_mm": float(current_raw.get("precipitation", 0.0)),
            "wind_kmh": float(current_raw.get("wind_speed_10m", 12.0)),
            "weather_code": int(current_raw.get("weather_code", 0)),
            "condition": current_cond,
            "is_live": True,
            "source": "Open-Meteo Live API"
        }

        # Format 7-Day Forecast Days
        forecast_days = []
        dates = daily_raw.get("time", [])
        t_max = daily_raw.get("temperature_2m_max", [])
        t_min = daily_raw.get("temperature_2m_min", [])
        precip = daily_raw.get("precipitation_sum", [])
        w_codes = daily_raw.get("weather_code", [])
        wind_max = daily_raw.get("wind_speed_10m_max", [])

        for idx, date_str in enumerate(dates):
            dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")
            max_c = float(t_max[idx]) if idx < len(t_max) else 20.0
            min_c = float(t_min[idx]) if idx < len(t_min) else 12.0
            avg_c = round((max_c + min_c) / 2.0, 1)
            rain_mm = float(precip[idx]) if idx < len(precip) else 0.0
            code = int(w_codes[idx]) if idx < len(w_codes) else 0
            w_kmh = float(wind_max[idx]) if idx < len(wind_max) else 10.0

            forecast_days.append({
                "date": date_str,
                "day_name": dt.strftime("%a"),
                "display_date": dt.strftime("%a, %b %d"),
                "temp_avg": avg_c,
                "temp_max": max_c,
                "temp_min": min_c,
                "precip_mm": rain_mm,
                "wind_kmh": w_kmh,
                "weather_code": code,
                "condition": decode_wmo_code(code)
            })

        return {
            "status": "SUCCESS",
            "current": current_data,
            "daily_forecast": forecast_days,
            "city_name": geo["name"]
        }

    except Exception as exc:
        # Fallback heuristic in case of internet outage or rate limits
        now = datetime.datetime.now()
        fallback_current = {
            "city_code": city_code,
            "city_name": geo["name"],
            "timestamp": now.strftime("%Y-%m-%dT%H:%M"),
            "temperature_c": 17.5,
            "humidity_pct": 55.0,
            "precipitation_mm": 0.0,
            "wind_kmh": 14.0,
            "weather_code": 1,
            "condition": "Mainly Clear",
            "is_live": False,
            "source": f"Local Fallback Cache ({str(exc)[:40]})"
        }

        fallback_days = []
        for i in range(7):
            dt = now + datetime.timedelta(days=i)
            fallback_days.append({
                "date": dt.strftime("%Y-%m-%d"),
                "day_name": dt.strftime("%a"),
                "display_date": dt.strftime("%a, %b %d"),
                "temp_avg": 17.0 + (i % 3),
                "temp_max": 22.0,
                "temp_min": 12.0,
                "precip_mm": 4.5 if i in [2, 3] else 0.0,
                "wind_kmh": 12.0,
                "weather_code": 61 if i in [2, 3] else 0,
                "condition": "Moderate Rain" if i in [2, 3] else "Clear Sky"
            })

        return {
            "status": "FALLBACK",
            "current": fallback_current,
            "daily_forecast": fallback_days,
            "city_name": geo["name"],
            "error_msg": str(exc)
        }


def generate_live_weather_ai_forecast(
    active_keys: List[str],
    daily_forecast: List[Dict[str, Any]],
    custom_catalog: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Generate daily revenue projections using real upcoming meteorological forecast.
    Calculates day-by-day revenue shifts using business-specific econometric elasticities.
    """
    catalog = custom_catalog
    projections = {}
    total_impact_all = 0.0
    day_labels = [d["display_date"] for d in daily_forecast]

    total_rain_forecast = sum(d["precip_mm"] for d in daily_forecast)
    max_temp_forecast = max(d["temp_max"] for d in daily_forecast)
    min_temp_forecast = min(d["temp_min"] for d in daily_forecast)

    for b_key in active_keys:
        if b_key not in catalog:
            continue
        cfg = catalog[b_key]
        base = cfg["base_daily_rev"]
        series_actual = []
        series_base = []

        for idx, day_info in enumerate(daily_forecast):
            # Calendar day-of-week multiplier
            dt = datetime.datetime.strptime(day_info["date"], "%Y-%m-%d")
            dow_idx = dt.weekday()  # 0=Monday, 6=Sunday
            dow_weights = [0.88, 0.90, 0.95, 1.05, 1.38, 1.48, 1.28]
            dow_m = dow_weights[dow_idx]
            day_base = base * dow_m

            # Weather Shocks
            rain_val = day_info["precip_mm"]
            temp_val = day_info["temp_avg"]

            # Multiplier from rain, heat, and cold
            rain_mult = 1.0 + (rain_val * cfg.get("rain_elasticity", 0.0))

            temp_elasticity = cfg.get("temp_elasticity", 0.0)
            if temp_val > 25.0:
                temp_mult = 1.0 + ((temp_val - 25.0) * temp_elasticity)
            elif temp_val < 5.0 and cfg.get("snow_elasticity", 0.0) != 0:
                temp_mult = 1.0 + ((5.0 - temp_val) * cfg.get("snow_elasticity", 0.0))
            else:
                temp_mult = 1.0

            combined_mult = rain_mult * temp_mult
            day_act = day_base * max(0.15, combined_mult)

            series_base.append(round(day_base, 0))
            series_actual.append(round(day_act, 0))

        projections[b_key] = {
            "name": cfg["name"],
            "color": cfg.get("color", "#FFFFFF"),
            "dash": cfg.get("dash", "solid"),
            "symbol": cfg.get("symbol", "circle"),
            "days": day_labels,
            "actual_series": series_actual,
            "baseline_series": series_base,
            "net_week_impact": sum(series_actual) - sum(series_base)
        }
        total_impact_all += (sum(series_actual) - sum(series_base))

    # Strategic AI Advice tailored to upcoming real weather
    ai_advice = []
    rainy_days = [d["day_name"] for d in daily_forecast if d["precip_mm"] >= 4.0]

    if rainy_days:
        rain_str = ", ".join(rainy_days)
        if "food_delivery" in active_keys:
            ai_advice.append(
                f"Food Delivery Operations: Elevated rain forecasted on {rain_str}. Courier supply is expected to contract by ~18%. "
                "Activate driver surge incentives 30 minutes prior to precipitation windows to maintain fulfillment SLAs."
            )
        if "dine_in_restaurant" in active_keys:
            ai_advice.append(
                f"Restaurant Dining Floor: Precipitation on {rain_str} will suppress walk-ins and patio utilization by up to -45%. "
                "Reassign floor waitstaff to manage takeout dispatch and delivery packaging stations."
            )
        if "retail_apparel" in active_keys:
            ai_advice.append(
                f"Retail Merchandising: Position waterproof apparel, umbrellas, and footwear at entrance end-caps ahead of {rain_str} to capitalize on impulse demand."
            )
        if "car_wash" in active_keys:
            ai_advice.append(
                f"Car Wash Maintenance: Wash volumes will decline sharply on {rain_str}. Schedule bay equipment maintenance and staff training during these downtime intervals."
            )

    if max_temp_forecast >= 32.0:
        if "ice_cream_beverages" in active_keys:
            ai_advice.append(
                f"Cold Beverages & Confectionery: High temperatures reaching {max_temp_forecast:.1f}°C will boost cold refreshment sales by +40%. "
                "Ensure ice machine maintenance and advance replenishment of dairy and syrup stocks."
            )
        if "hvac_home_services" in active_keys:
            ai_advice.append(
                f"HVAC Emergency Dispatch: Summer heat index reaching {max_temp_forecast:.1f}°C will surge residential AC emergency calls. "
                "Place secondary technician shifts on call."
            )

    if not ai_advice:
        ai_advice.append(
            f"Standard Baseline Operations: Mild and stable weather anticipated over the upcoming 7-day period (max rain: {total_rain_forecast:.1f} mm, max temp: {max_temp_forecast:.1f}°C). Maintain normal operational staffing and standard supply replenishment schedules."
        )

    return {
        "weather_desc": f"Live 7-Day Open-Meteo Meteorological Trajectory (Cumulative Rain: {total_rain_forecast:.1f} mm, Temp Range: {min_temp_forecast:.0f}°C to {max_temp_forecast:.0f}°C)",
        "days": day_labels,
        "daily_forecast": daily_forecast,
        "projections": projections,
        "total_impact_all": total_impact_all,
        "ai_advice": ai_advice
    }
