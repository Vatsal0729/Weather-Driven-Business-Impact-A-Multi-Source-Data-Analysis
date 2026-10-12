import os
import sys
import json
import time
import re
import datetime
import pandas as pd
import numpy as np
from flask import Flask, render_template, request, jsonify

# Add parent directory to path so src modules import cleanly
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.econometrics import WeatherEconometricsEngine
from src.revenue_analytics import (
    BUSINESS_CATALOG,
    CITY_DYNAMICS,
    infer_custom_business_parameters,
    calculate_custom_business_daily_series,
    generate_business_specific_why_insight,
    analyze_inter_business_linkages,
    generate_dynamic_domino_cascade,
    generate_business_specific_domino_effects,
    generate_future_ai_forecast,
    aggregate_daily_financials
)
from src.live_weather import (
    fetch_live_weather,
    generate_live_weather_ai_forecast
)
from src.revenue_connectors import (
    SquareConnector,
    StripeConnector,
    CSVRevenueConnector,
    estimate_empirical_elasticities
)

app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), "templates"),
    static_folder=os.path.join(os.path.dirname(__file__), "static")
)

# City mapping
CITY_NAMES = {
    "NYC": "New York City",
    "ORD": "Chicago",
    "SEA": "Seattle",
    "PHX": "Phoenix"
}

# High Visibility Color Palette
HIGH_VISIBILITY_PALETTE = [
    "#00D2FF", "#FF9100", "#00E676", "#FF5252", "#B388FF",
    "#76FF03", "#FF4081", "#00E5FF", "#FFD600", "#E040FB",
    "#1DE9B6", "#FF6D00", "#448AFF", "#00C853", "#FF1744", "#7C4DFF"
]

BUSINESS_PALETTE = {
    "square_pos_live": "#38BDF8",
    "stripe_gateway_live": "#14B8A6",
    "dine_in_restaurant": "#F59E0B",
    "food_delivery": "#FB7185",
    "rideshare_fleet": "#A855F7",
    "bikeshare_network": "#06B6D4",
    "specialty_apparel": "#EC4899",
    "supermarket": "#10B981",
    "convenience_store": "#F97316",
    "car_wash": "#6366F1",
    "hvac_repair": "#EAB308",
    "home_improvement": "#84CC16",
    "ice_cream_beverage": "#00E5FF",
    "cinema_entertainment": "#8B5CF6",
    "freight_logistics": "#94A3B8",
    "urgent_care": "#EF4444"
}

def get_biz_color(b_key: str, idx: int = 0) -> str:
    if b_key in BUSINESS_PALETTE:
        return BUSINESS_PALETTE[b_key]
    return HIGH_VISIBILITY_PALETTE[idx % len(HIGH_VISIBILITY_PALETTE)]

def get_biz_clean_label(b_key: str, catalog_entry: dict) -> str:
    name = catalog_entry.get("name", b_key) if isinstance(catalog_entry, dict) else str(catalog_entry)
    clean = name.split(" Live")[0].split(" (")[0].strip()
    return clean

# In-memory storage for the web session
CUSTOM_BUSINESSES = {}
AUTO_MERCHANT_CACHE = {}
WEATHER_CACHE = {}

print("Initializing Weather Econometrics Engine and Pre-Aggregating Data...")
data_path = os.path.join(BASE_DIR, "data", "processed", "weather_business_merged.parquet")
engine = WeatherEconometricsEngine(data_path)
engine.fit_sector_models()
df_daily_base = aggregate_daily_financials(engine.df)
print("Data Engine Ready!")

def get_auto_connected_merchants(city_code: str):
    if city_code in AUTO_MERCHANT_CACHE:
        return AUTO_MERCHANT_CACHE[city_code]
    sq_conn = SquareConnector()
    df_sq = sq_conn.fetch_daily_revenue("2023-01-01", "2023-12-31", mock_profile="restaurant")
    st_conn = StripeConnector()
    df_st = st_conn.fetch_daily_revenue("2023-01-01", "2023-12-31", mock_profile="ecommerce")
    city_weather_daily = df_daily_base[df_daily_base["metro_area"] == city_code]
    res_sq = estimate_empirical_elasticities(df_sq, city_weather_daily, business_name=f"{CITY_NAMES.get(city_code, city_code)} Square POS (Hospitality)")
    res_st = estimate_empirical_elasticities(df_st, city_weather_daily, business_name=f"{CITY_NAMES.get(city_code, city_code)} Stripe Gateway (E-Commerce)")
    city_tag = "NYC" if city_code == "NYC" else city_code
    merchants = {
        "square_pos_live": {
            "name": f"Square POS — {city_tag}",
            "category": "Hospitality & Dining (Auto-Connected)",
            "description": f"Real POS register stream from Square. {res_sq['summary_insight']}",
            "color": "#FFFFFF",
            "dash": "solid",
            "symbol": "diamond",
            "base_daily_rev": res_sq["base_daily_rev"],
            "rain_elasticity": res_sq["rain_elasticity"],
            "snow_elasticity": res_sq["snow_elasticity"],
            "temp_elasticity": res_sq["temp_elasticity"]
        },
        "stripe_gateway_live": {
            "name": f"Stripe Checkout — {city_tag}",
            "category": "E-Commerce & Digital (Auto-Connected)",
            "description": f"Real payment gateway stream from Stripe. {res_st['summary_insight']}",
            "color": "#FFFFFF",
            "dash": "solid",
            "symbol": "square",
            "base_daily_rev": res_st["base_daily_rev"],
            "rain_elasticity": res_st["rain_elasticity"],
            "snow_elasticity": res_st["snow_elasticity"],
            "temp_elasticity": res_st["temp_elasticity"]
        }
    }
    AUTO_MERCHANT_CACHE[city_code] = merchants
    return merchants

def get_live_weather(city_code: str):
    now = time.time()
    if city_code in WEATHER_CACHE:
        pkg, timestamp = WEATHER_CACHE[city_code]
        if now - timestamp < 900:  # 15 minutes TTL
            return pkg
    pkg = fetch_live_weather(city_code)
    WEATHER_CACHE[city_code] = (pkg, now)
    return pkg

def get_merged_catalog(city_code: str, client_custom_dict=None):
    auto = get_auto_connected_merchants(city_code)
    cat = {**auto, **BUSINESS_CATALOG, **CUSTOM_BUSINESSES}
    if client_custom_dict and isinstance(client_custom_dict, dict):
        cat.update(client_custom_dict)
    return cat


# --- ROUTES ---

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/initial-state")
def initial_state():
    city = request.args.get("city", "NYC")
    active_catalog = get_merged_catalog(city)
    weather_pkg = get_live_weather(city)
    
    # Format catalog for client
    catalog_list = []
    default_selected = ["square_pos_live", "stripe_gateway_live", "food_delivery", "dine_in_restaurant"]
    for idx, (k, v) in enumerate(active_catalog.items()):
        catalog_list.append({
            "key": k,
            "name": v.get("name", k),
            "clean_name": get_biz_clean_label(k, v),
            "category": v.get("category", "General"),
            "description": v.get("description", ""),
            "color": get_biz_color(k, idx),
            "symbol": v.get("symbol", "circle"),
            "is_selected": k in default_selected
        })
        
    return jsonify({
        "city": city,
        "cities": CITY_NAMES,
        "catalog": catalog_list,
        "default_selected": default_selected,
        "weather": weather_pkg
    })

@app.route("/api/weather")
def weather():
    city = request.args.get("city", "NYC")
    weather_pkg = get_live_weather(city)
    return jsonify(weather_pkg)

@app.route("/api/portfolio-data", methods=["POST"])
def portfolio_data():
    data = request.get_json() or {}
    city = data.get("city", "NYC")
    selected_keys = data.get("selected_keys", ["square_pos_live", "stripe_gateway_live", "food_delivery", "dine_in_restaurant"])
    custom_businesses = data.get("custom_businesses", {})
    horizon = data.get("horizon", "Last 6 Months (180 Days)")
    inspected_day_idx = data.get("inspected_day_idx", None)

    active_catalog = get_merged_catalog(city, custom_businesses)
    valid_keys = [k for k in selected_keys if k in active_catalog]
    if not valid_keys:
        return jsonify({"error": "No valid businesses selected"}), 400

    city_daily = df_daily_base[df_daily_base["metro_area"] == city].copy()
    city_daily_custom = calculate_custom_business_daily_series(city_daily, valid_keys, custom_catalog=active_catalog)

    # 1. Past 7 Days calculation for Tab 1
    past_week = city_daily_custom.tail(7).copy().reset_index(drop=True)
    total_week_actual = sum(past_week[f"{k}_actual_rev"].sum() for k in valid_keys if f"{k}_actual_rev" in past_week)
    total_week_base = sum(past_week[f"{k}_baseline_rev"].sum() for k in valid_keys if f"{k}_baseline_rev" in past_week)
    total_week_impact = total_week_actual - total_week_base
    total_rain_week = float(past_week["precip_accumulation_mm"].sum())

    # Format 7-day chart series
    x_labels_7d = [f"{r['day_name']}<br>{r['date_str']}" for _, r in past_week.iterrows()]
    business_series_7d = []
    for idx, b_key in enumerate(valid_keys):
        cfg = active_catalog[b_key]
        actual_rev = past_week[f"{b_key}_actual_rev"].tolist()
        baseline_rev = past_week[f"{b_key}_baseline_rev"].tolist()
        net_impact = past_week[f"{b_key}_net_impact"].tolist()
        business_series_7d.append({
            "key": b_key,
            "name": cfg["name"],
            "clean_label": get_biz_clean_label(b_key, cfg),
            "color": get_biz_color(b_key, idx),
            "symbol": cfg.get("symbol", "circle"),
            "actual": actual_rev,
            "baseline": baseline_rev,
            "net_impact": net_impact
        })

    rain_series_7d = past_week["precip_accumulation_mm"].tolist()
    temp_series_7d = past_week["air_temp_deg_c"].tolist()
    weather_icons_7d = past_week["weather_icon"].tolist()
    dates_7d = past_week["date_str"].tolist()
    days_7d = past_week["day_name"].tolist()

    # 2. Day in Review Insights
    if inspected_day_idx is None or inspected_day_idx < 0 or inspected_day_idx >= len(past_week):
        inspected_day_idx = len(past_week) - 1  # Default to latest day
    day_row = past_week.iloc[inspected_day_idx]
    
    day_insights = []
    for b_key in valid_keys:
        insight = generate_business_specific_why_insight(b_key, day_row, custom_catalog=active_catalog)
        day_insights.append(insight)

    # Hourly analysis table for inspected day
    hourly_sub = engine.df[(engine.df["metro_area"] == city) & (engine.df["date_str"] == day_row["date_str"])].copy()
    hourly_records = []
    if not hourly_sub.empty:
        for idx, r in hourly_sub.reset_index(drop=True).iterrows():
            hourly_records.append({
                "num": idx + 1,
                "time": str(r.get("timestamp_local_str", "")),
                "temp": round(float(r.get("air_temp_deg_c", 0.0)), 1),
                "rain": round(float(r.get("precip_accumulation_mm", 0.0)), 1),
                "food_orders": int(r.get("delivery_order_count", 0)),
                "price_surge": f"{float(r.get('surge_pricing_mult', 1.0)):.2f}x",
                "wait_time": f"{float(r.get('delivery_duration_min', 0.0)):.1f} min",
                "bike_trips": int(r.get("bikeshare_trips_count", 0)),
                "traffic_jam": f"{float(r.get('traffic_congestion_pct', 0.0)):.1f}%"
            })

    # 3. Tab 2 Historical Timeline Data
    if "3 Months" in horizon:
        df_lt = city_daily_custom.tail(90).copy()
    elif "6 Months" in horizon:
        df_lt = city_daily_custom.tail(180).copy()
    else:
        df_lt = city_daily_custom.copy()

    df_lt["week_start"] = df_lt["date"].dt.to_period("W").dt.start_time
    df_lt["year_week"] = df_lt["date"].dt.to_period("W").astype(str)
    
    agg_dict = {
        "week_start": "min",
        "precip_accumulation_mm": "sum",
        "air_temp_deg_c": "mean"
    }
    for b_key in valid_keys:
        if f"{b_key}_actual_rev" in df_lt:
            agg_dict[f"{b_key}_actual_rev"] = "sum"
            agg_dict[f"{b_key}_baseline_rev"] = "sum"

    weekly_lt = df_lt.groupby("year_week", as_index=False).agg(agg_dict)
    weekly_lt = weekly_lt.sort_values("week_start").reset_index(drop=True)
    weekly_lt["date_display"] = weekly_lt["week_start"].dt.strftime("%b %d, %Y")
    weekly_dates = weekly_lt["week_start"].dt.strftime("%Y-%m-%d").tolist()

    historical_series = []
    for idx, b_key in enumerate(valid_keys):
        cfg = active_catalog[b_key]
        historical_series.append({
            "key": b_key,
            "name": cfg["name"],
            "clean_label": get_biz_clean_label(b_key, cfg),
            "color": get_biz_color(b_key, idx),
            "symbol": cfg.get("symbol", "circle"),
            "actual": weekly_lt[f"{b_key}_actual_rev"].tolist() if f"{b_key}_actual_rev" in weekly_lt else [],
            "baseline": weekly_lt[f"{b_key}_baseline_rev"].tolist() if f"{b_key}_baseline_rev" in weekly_lt else []
        })

    weekly_rain = weekly_lt["precip_accumulation_mm"].tolist()
    weekly_temp = weekly_lt["air_temp_deg_c"].round(1).tolist()

    # 4. Econometric comparison table
    comp_df = engine.get_naive_vs_fixed_effects_comparison()
    econometric_records = []
    for idx, row in comp_df.iterrows():
        econometric_records.append({
            "num": idx,
            "metric": str(row["Business Metric"]),
            "baseline": str(row["Normal Daily Average"]),
            "raw_temp_corr": round(float(row["Raw Temperature Correlation (r)"]), 3) if pd.notnull(row["Raw Temperature Correlation (r)"]) else 0.0,
            "adj_temp_impact": str(row["Adjusted Temperature Impact (% change / °C)"]),
            "raw_rain_corr": round(float(row["Raw Rain Correlation (r)"]), 3) if pd.notnull(row["Raw Rain Correlation (r)"]) else 0.0,
            "adj_rain_impact": str(row["Adjusted Rain Impact (% change / mm)"]),
            "r2": str(row["Model Fit (R²)"]),
            "reliability": str(row["Reliable Effect (p < 0.05)"])
        })

    return jsonify({
        "metrics": {
            "total_week_impact": total_week_impact,
            "total_week_actual": total_week_actual,
            "total_week_base": total_week_base,
            "total_rain_week": total_rain_week,
            "portfolio_count": len(valid_keys)
        },
        "chart_7d": {
            "x_labels": x_labels_7d,
            "dates": dates_7d,
            "days": days_7d,
            "icons": weather_icons_7d,
            "temperatures": temp_series_7d,
            "rainfall": rain_series_7d,
            "businesses": business_series_7d
        },
        "day_in_review": {
            "inspected_idx": inspected_day_idx,
            "date_str": day_row["date_str"],
            "day_name": day_row["day_name"],
            "weather_icon": day_row["weather_icon"],
            "temperature": round(float(day_row["air_temp_deg_c"]), 1),
            "rain": round(float(day_row["precip_accumulation_mm"]), 1),
            "insights": day_insights,
            "hourly_table": hourly_records
        },
        "historical_timeline": {
            "dates": weekly_dates,
            "display_dates": weekly_lt["date_display"].tolist(),
            "rainfall": weekly_rain,
            "temperatures": weekly_temp,
            "businesses": historical_series
        },
        "econometrics_table": econometric_records
    })

@app.route("/api/domino-data", methods=["POST"])
def domino_data():
    data = request.get_json() or {}
    city = data.get("city", "NYC")
    selected_keys = data.get("selected_keys", ["square_pos_live", "stripe_gateway_live", "food_delivery", "dine_in_restaurant"])
    custom_businesses = data.get("custom_businesses", {})

    active_catalog = get_merged_catalog(city, custom_businesses)
    valid_keys = [k for k in selected_keys if k in active_catalog]
    weather_pkg = get_live_weather(city)
    cur_w = weather_pkg.get("current", {})

    city_daily = df_daily_base[df_daily_base["metro_area"] == city].copy()
    city_daily_custom = calculate_custom_business_daily_series(city_daily, valid_keys, custom_catalog=active_catalog)

    # 1. Dynamic Domino Cascade
    dynamic_cascade = generate_dynamic_domino_cascade(city, cur_w, valid_keys, custom_catalog=active_catalog)

    # 2. Per-Business Domino Cards
    biz_dominos = generate_business_specific_domino_effects(city, cur_w, valid_keys, custom_catalog=active_catalog)

    # 3. Cross-Channel Demand Shifts
    sample_rain_day = city_daily_custom[city_daily_custom["precip_accumulation_mm"] > 2.0].iloc[-1] if len(city_daily_custom[city_daily_custom["precip_accumulation_mm"] > 2.0]) > 0 else city_daily_custom.iloc[-1]
    portfolio_links = analyze_inter_business_linkages(valid_keys, sample_rain_day, custom_catalog=active_catalog)

    # 4. Past 30 Days Net Shift series
    recent_30 = city_daily_custom.tail(30).reset_index(drop=True)
    dates_30 = recent_30["date_str"].tolist()
    days_30 = recent_30["day_name"].tolist()
    icons_30 = recent_30["weather_icon"].tolist()
    temps_30 = recent_30["air_temp_deg_c"].round(1).tolist()
    rain_30 = recent_30["precip_accumulation_mm"].round(1).tolist()

    biz_30_series = []
    for idx, b_key in enumerate(valid_keys):
        cfg = active_catalog[b_key]
        biz_30_series.append({
            "key": b_key,
            "name": cfg["name"],
            "clean_label": get_biz_clean_label(b_key, cfg),
            "color": get_biz_color(b_key, idx),
            "symbol": cfg.get("symbol", "circle"),
            "net_shifts": recent_30[f"{b_key}_net_impact"].tolist() if f"{b_key}_net_impact" in recent_30 else []
        })

    return jsonify({
        "cascade": dynamic_cascade,
        "biz_dominos": biz_dominos,
        "substitution_links": portfolio_links,
        "chart_30d": {
            "dates": dates_30,
            "days": days_30,
            "icons": icons_30,
            "temps": temps_30,
            "rain": rain_30,
            "series": biz_30_series
        }
    })

@app.route("/api/nowcast", methods=["POST"])
def nowcast():
    data = request.get_json() or {}
    city = data.get("city", "NYC")
    selected_keys = data.get("selected_keys", ["square_pos_live", "stripe_gateway_live", "food_delivery", "dine_in_restaurant"])
    custom_businesses = data.get("custom_businesses", {})

    active_catalog = get_merged_catalog(city, custom_businesses)
    valid_keys = [k for k in selected_keys if k in active_catalog]
    weather_pkg = get_live_weather(city)
    cur_w = weather_pkg.get("current", {})

    now_dt = datetime.datetime.now()
    days_list = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    live_dow = now_dt.weekday()
    live_hour = now_dt.hour
    live_rain = float(cur_w.get("precipitation_mm", 0.0))
    live_temp_anom = round(float(cur_w.get("temperature_c", 18.0)) - 18.0, 1)
    live_wind = float(cur_w.get("wind_kmh", 12.0))

    sim_dow = data.get("sim_dow", live_dow)
    sim_hour = data.get("sim_hour", live_hour)
    sim_rain = float(data.get("sim_rain", live_rain))
    sim_temp_anom = float(data.get("sim_temp_anom", live_temp_anom))
    sim_wind = float(data.get("sim_wind", live_wind))

    is_custom = (
        sim_dow != live_dow or sim_hour != live_hour or
        abs(sim_rain - live_rain) > 0.01 or abs(sim_temp_anom - live_temp_anom) > 0.01
    )

    # Execute econometric shock simulation
    sim_output = engine.simulate_cross_sector_scenario(
        city=city,
        day_of_week=sim_dow,
        hour_of_day=sim_hour,
        month=now_dt.month,
        is_holiday=0,
        rain_mm=sim_rain,
        snow_cm=0.0,
        temp_anomaly_c=sim_temp_anom,
        wind_kmh=sim_wind
    )

    # 7-day forward AI forecast
    daily_fc = weather_pkg.get("daily_forecast", [])
    forecast_data = generate_live_weather_ai_forecast(valid_keys, daily_fc, custom_catalog=active_catalog)

    # Format forward projections for Plotly
    forecast_chart_series = []
    days_x = forecast_data.get("days", [])
    for idx, (b_key, p_info) in enumerate(forecast_data.get("projections", {}).items()):
        cfg = active_catalog.get(b_key, {})
        forecast_chart_series.append({
            "key": b_key,
            "name": p_info.get("name", b_key),
            "clean_label": get_biz_clean_label(b_key, p_info),
            "color": get_biz_color(b_key, idx),
            "symbol": cfg.get("symbol", "circle"),
            "actual_projected": p_info.get("actual_series", []),
            "baseline": p_info.get("baseline_series", [])
        })

    return jsonify({
        "is_custom": is_custom,
        "sim_params": {
            "day_name": days_list[sim_dow],
            "dow": sim_dow,
            "hour": sim_hour,
            "rain": sim_rain,
            "temp_anom": sim_temp_anom,
            "wind": sim_wind,
            "live_condition": cur_w.get("condition", "Current Weather")
        },
        "sector_predictions": sim_output.get("by_sector", {}),
        "daily_forecast_strip": daily_fc,
        "forecast_chart": {
            "days": days_x,
            "series": forecast_chart_series
        },
        "strategic_advice": forecast_data.get("ai_advice", [])
    })

@app.route("/api/diagnostics")
def diagnostics():
    city = request.args.get("city", "NYC")
    display_df = engine.df[engine.df["metro_area"] == city].tail(25).copy().reset_index(drop=True)
    records = []
    for idx, r in display_df.iterrows():
        records.append({
            "num": idx + 1,
            "time": str(r.get("timestamp_local_str", "")),
            "city": str(r.get("metro_area", "")),
            "temp": round(float(r.get("air_temp_deg_c", 0.0)), 1),
            "temp_anom": round(float(r.get("temp_anomaly_deg_c", 0.0)), 1),
            "rain": round(float(r.get("precip_accumulation_mm", 0.0)), 1),
            "delivery_orders": int(r.get("delivery_order_count", 0)),
            "price_surge": f"{float(r.get('surge_pricing_mult', 1.0)):.2f}x",
            "bike_trips": int(r.get("bikeshare_trips_count", 0)),
            "rideshare_trips": int(r.get("rideshare_trip_count", 0)),
            "dinein_guests": int(r.get("restaurant_dinein_guests", 0)),
            "mall_footfall": int(r.get("retail_mall_footfall", 0)),
            "grid_load": f"{float(r.get('electricity_grid_load_mw', 0.0)):.1f} MW",
            "freight_delay": f"{float(r.get('freight_delay_min', 0.0)):.1f} min"
        })
    return jsonify({
        "city": city,
        "total_weather_rows": 69106,
        "total_pos_events": 279249,
        "table_rows": records
    })

@app.route("/api/custom-business", methods=["POST"])
def add_custom_business():
    data = request.get_json() or {}
    name = data.get("name", "").strip()
    category_hint = data.get("category_hint", "Auto-Detect from Name")
    custom_color = data.get("custom_color", "#00D2FF")
    custom_rev = float(data.get("custom_rev", 35000))
    custom_rain = float(data.get("custom_rain", 0.0))
    custom_temp = float(data.get("custom_temp", 0.0))

    if not name:
        return jsonify({"error": "Business name is required"}), 400

    inferred = infer_custom_business_parameters(
        name=name,
        category_hint=category_hint,
        custom_color=custom_color,
        custom_rev=custom_rev,
        custom_rain=custom_rain if custom_rain != 0 else None,
        custom_temp=custom_temp if custom_temp != 0 else None,
        existing_count=len(CUSTOM_BUSINESSES)
    )

    slug = inferred["slug"]
    if slug in BUSINESS_CATALOG or slug in CUSTOM_BUSINESSES:
        slug = f"{slug}_{len(CUSTOM_BUSINESSES) + 1}"

    CUSTOM_BUSINESSES[slug] = inferred["config"]
    return jsonify({
        "success": True,
        "slug": slug,
        "config": inferred["config"],
        "message": f"Successfully created '{inferred['config']['name']}'"
    })

@app.route("/api/upload-csv", methods=["POST"])
def upload_csv():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files["file"]
    store_name = request.form.get("store_name", "My Local Store").strip()
    city = request.form.get("city", "NYC")

    try:
        if file.filename.endswith(".csv"):
            raw_df = pd.read_csv(file)
        else:
            raw_df = pd.read_excel(file)
        csv_conn = CSVRevenueConnector()
        df_clean_csv, meta_csv = csv_conn.parse_dataframe(raw_df)
        city_weather_daily = df_daily_base[df_daily_base["metro_area"] == city]
        res_csv = estimate_empirical_elasticities(df_clean_csv, city_weather_daily, business_name=store_name)
        slug_csv = f"uploaded_{re.sub(r'[^a-z0-9]+', '_', store_name.lower())[:15]}"
        
        cfg = {
            "name": f"{store_name} (Uploaded POS)",
            "category": "Real Merchant Ingestion",
            "description": f"Real uploaded store. {res_csv['summary_insight']}",
            "color": "#FFFFFF",
            "dash": "solid",
            "symbol": "star",
            "base_daily_rev": res_csv["base_daily_rev"],
            "rain_elasticity": res_csv["rain_elasticity"],
            "snow_elasticity": res_csv["snow_elasticity"],
            "temp_elasticity": res_csv["temp_elasticity"]
        }
        CUSTOM_BUSINESSES[slug_csv] = cfg
        return jsonify({
            "success": True,
            "slug": slug_csv,
            "config": cfg,
            "meta": meta_csv,
            "regression": res_csv
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting Weather-Driven Business Intelligence Platform Website on http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)
