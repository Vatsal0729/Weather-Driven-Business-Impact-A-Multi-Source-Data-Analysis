"""
Multi-Business Revenue Intelligence & Dynamic Catalog Engine.
Strict monochrome black-and-white theme with zero emojis.
Supports 16+ preset enterprise business sectors and dynamic on-the-fly custom business synthesis.
"""

import numpy as np
import pandas as pd
import re

BUSINESS_CATALOG = {
    "food_delivery": {
        "name": "On-Demand Food Delivery",
        "category": "Logistics & Delivery",
        "description": "On-demand food and grocery ordering platform with courier network.",
        "color": "#00D2FF",  # Bright Cyan Blue (High Visibility)
        "dash": "solid",
        "symbol": "circle",
        "base_daily_rev": 65000,
        "rain_elasticity": 0.035,
        "snow_elasticity": 0.085,
        "temp_elasticity": -0.015,
    },
    "dine_in_restaurant": {
        "name": "Dine-In Restaurant & Bistro",
        "category": "Hospitality & Dining",
        "description": "Sit-down restaurant with dining room and outdoor patio seating.",
        "color": "#FF9100",  # Vivid Amber Orange (High Visibility)
        "dash": "solid",
        "symbol": "square",
        "base_daily_rev": 28000,
        "rain_elasticity": -0.045,
        "snow_elasticity": -0.095,
        "temp_elasticity": 0.012,
    },
    "retail_apparel": {
        "name": "Retail Clothing & Rainwear Store",
        "category": "Retail & Commerce",
        "description": "Brick-and-mortar apparel store selling seasonal & weather apparel.",
        "color": "#B388FF",  # Electric Lavender Purple (High Visibility)
        "dash": "solid",
        "symbol": "diamond",
        "base_daily_rev": 35000,
        "rain_elasticity": 0.022,
        "snow_elasticity": 0.065,
        "temp_elasticity": -0.020,
    },
    "rideshare_fleet": {
        "name": "Urban Rideshare & Taxi Fleet",
        "category": "Urban Mobility",
        "description": "City ridesharing & on-demand private mobility transport.",
        "color": "#00E676",  # Vibrant Emerald Green (High Visibility)
        "dash": "solid",
        "symbol": "triangle-up",
        "base_daily_rev": 52000,
        "rain_elasticity": 0.042,
        "snow_elasticity": 0.078,
        "temp_elasticity": -0.010,
    },
    "ice_cream_beverages": {
        "name": "Ice Cream & Cold Beverage Parlor",
        "category": "Food & Beverage",
        "description": "Gelato, frozen treats, and iced refreshment parlors.",
        "color": "#00E5FF",  # Bright Turquoise Aqua (High Visibility)
        "dash": "solid",
        "symbol": "cross",
        "base_daily_rev": 14000,
        "rain_elasticity": -0.055,
        "snow_elasticity": -0.120,
        "temp_elasticity": 0.058,
    },
    "hot_cafe_bakery": {
        "name": "Hot Cafe & Comfort Food Bakery",
        "category": "Food & Beverage",
        "description": "Artisan coffee, hot soups, and fresh warm bakery pastries.",
        "color": "#FF5252",  # Vivid Coral Red (High Visibility)
        "dash": "solid",
        "symbol": "x",
        "base_daily_rev": 18000,
        "rain_elasticity": 0.028,
        "snow_elasticity": 0.045,
        "temp_elasticity": -0.032,
    },
    "bikeshare_operator": {
        "name": "Micromobility & Bike-Share",
        "category": "Urban Mobility",
        "description": "Station-based bike and e-scooter urban rental network.",
        "color": "#76FF03",  # High-Vis Electric Lime (High Visibility)
        "dash": "solid",
        "symbol": "star",
        "base_daily_rev": 16000,
        "rain_elasticity": -0.085,
        "snow_elasticity": -0.180,
        "temp_elasticity": 0.035,
    },
    "freight_logistics": {
        "name": "Freight & Last-Mile Logistics",
        "category": "Supply Chain",
        "description": "Inter-city trucking and regional warehouse dispatch operations.",
        "color": "#E040FB",  # Vibrant Magenta (High Visibility)
        "dash": "solid",
        "symbol": "hexagon",
        "base_daily_rev": 75000,
        "rain_elasticity": -0.018,
        "snow_elasticity": -0.055,
        "temp_elasticity": -0.005,
    },
    "movie_theaters": {
        "name": "Movie Theaters & Indoor Entertainment",
        "category": "Entertainment & Leisure",
        "description": "Cinema multiplexes, bowling alleys, and indoor gaming arcades.",
        "color": "#FF4081",  # Hot Pink (High Visibility)
        "dash": "solid",
        "symbol": "circle-open",
        "base_daily_rev": 26000,
        "rain_elasticity": 0.048,
        "snow_elasticity": 0.035,
        "temp_elasticity": -0.018,
    },
    "gym_fitness": {
        "name": "Gyms & Indoor Fitness Centers",
        "category": "Health & Wellness",
        "description": "Membership health clubs, indoor studios, and gym facilities.",
        "color": "#448AFF",  # Bright Royal Blue (High Visibility)
        "dash": "solid",
        "symbol": "square-open",
        "base_daily_rev": 22000,
        "rain_elasticity": 0.025,
        "snow_elasticity": -0.040,
        "temp_elasticity": -0.022,
    },
    "car_wash": {
        "name": "Car Wash & Auto Detailing",
        "category": "Automotive Services",
        "description": "Automated and full-service vehicle washing facilities.",
        "color": "#1DE9B6",  # Seafoam Teal (High Visibility)
        "dash": "solid",
        "symbol": "diamond-open",
        "base_daily_rev": 12000,
        "rain_elasticity": -0.115,
        "snow_elasticity": -0.160,
        "temp_elasticity": 0.025,
    },
    "golf_theme_park": {
        "name": "Outdoor Golf & Theme Parks",
        "category": "Outdoor Recreation",
        "description": "Golf courses, amusement parks, and outdoor attraction venues.",
        "color": "#00C853",  # Deep Grass Green (High Visibility)
        "dash": "solid",
        "symbol": "triangle-down",
        "base_daily_rev": 45000,
        "rain_elasticity": -0.140,
        "snow_elasticity": -0.220,
        "temp_elasticity": 0.045,
    },
    "pharmacy_clinics": {
        "name": "Pharmacy & Urgent Care Clinics",
        "category": "Healthcare & Pharma",
        "description": "Retail pharmacies, walk-in urgent care, and medical dispensaries.",
        "color": "#FF1744",  # High-Vis Crimson (High Visibility)
        "dash": "solid",
        "symbol": "cross-thin",
        "base_daily_rev": 38000,
        "rain_elasticity": 0.015,
        "snow_elasticity": 0.055,
        "temp_elasticity": -0.038,
    },
    "hvac_home_services": {
        "name": "HVAC & Home Repair Services",
        "category": "Home Services & Utilities",
        "description": "Emergency air conditioning, furnace heating, and plumbing services.",
        "color": "#FF6D00",  # Bright Tangerine Orange (High Visibility)
        "dash": "solid",
        "symbol": "star-open",
        "base_daily_rev": 42000,
        "rain_elasticity": 0.012,
        "snow_elasticity": 0.090,
        "temp_elasticity": 0.065,
    },
    "grocery_supermarket": {
        "name": "Grocery & Supermarket Stores",
        "category": "Retail & Grocery",
        "description": "Large-format grocery stores, food marts, and essential staples.",
        "color": "#FFD600",  # High-Vis Lemon Gold (High Visibility)
        "dash": "solid",
        "symbol": "triangle-up-open",
        "base_daily_rev": 85000,
        "rain_elasticity": 0.010,
        "snow_elasticity": 0.060,
        "temp_elasticity": -0.008,
    },
    "ecommerce_retail": {
        "name": "E-Commerce & Online Marketplace",
        "category": "Digital Commerce",
        "description": "Direct-to-consumer online shopping and package fulfillment.",
        "color": "#7C4DFF",  # Bright Electric Violet (High Visibility)
        "dash": "solid",
        "symbol": "diamond-tall",
        "base_daily_rev": 95000,
        "rain_elasticity": 0.032,
        "snow_elasticity": 0.075,
        "temp_elasticity": -0.015,
    }
}


HIGH_VISIBILITY_PALETTE = [
    "#00D2FF",  # Bright Cyan Blue
    "#FF9100",  # Vivid Amber Orange
    "#00E676",  # Vibrant Emerald Green
    "#FF5252",  # Vivid Coral Red
    "#B388FF",  # Electric Lavender Purple
    "#76FF03",  # High-Vis Electric Lime
    "#FF4081",  # Hot Pink
    "#00E5FF",  # Bright Turquoise Aqua
    "#FFD600",  # High-Vis Lemon Gold
    "#E040FB",  # Vibrant Magenta
    "#1DE9B6",  # Seafoam Teal
    "#FF6D00",  # Bright Tangerine Orange
    "#448AFF",  # Bright Royal Blue
    "#00C853",  # Deep Grass Green
    "#FF1744",  # High-Vis Crimson
    "#7C4DFF",  # Bright Electric Violet
]


def infer_custom_business_parameters(name: str, category_hint: str = None, custom_color: str = None, custom_rev: float = None, custom_rain: float = None, custom_temp: float = None, existing_count: int = 0):
    """
    Synthesizes realistic econometric parameters for a novel user-typed business.
    Assigns a standard high-visibility chart line color if custom_color is not specified.
    """
    clean_name = name.strip()
    slug = re.sub(r'[^a-z0-9]+', '_', clean_name.lower()).strip('_')
    if not slug:
        slug = f"custom_biz_{abs(hash(clean_name)) % 10000}"
        
    lower_n = clean_name.lower()
    
    # Default baseline heuristics
    category = "General Commercial"
    base_rev = 30000.0
    rain_elast = -0.015
    snow_elast = -0.040
    temp_elast = 0.005
    description = f"Custom synthesized business entity: {clean_name}"
    
    # Sector & Keyword Classification Heuristics
    if any(k in lower_n for k in ["outdoor", "golf", "park", "garden", "patio", "boat", "beach", "pool", "surf", "ski", "resort"]):
        category = "Outdoor Recreation"
        base_rev = 45000.0
        rain_elast = -0.135
        snow_elast = -0.210
        temp_elast = 0.040
        description = f"Outdoor recreation & leisure venue: {clean_name}"
    elif any(k in lower_n for k in ["indoor", "arcade", "cinema", "movie", "theater", "bowling", "museum", "escape", "vr", "game"]):
        category = "Indoor Entertainment"
        base_rev = 28000.0
        rain_elast = 0.045
        snow_elast = 0.030
        temp_elast = -0.015
        description = f"Indoor entertainment facility: {clean_name}"
    elif any(k in lower_n for k in ["hvac", "repair", "plumb", "roof", "gutter", "electric", "mechanic", "towing", "locksmith", "handyman"]):
        category = "Home & Emergency Services"
        base_rev = 42000.0
        rain_elast = 0.018
        snow_elast = 0.095
        temp_elast = 0.060
        description = f"Emergency repair and utility contractor: {clean_name}"
    elif any(k in lower_n for k in ["gym", "fitness", "yoga", "pilates", "crossfit", "martial", "dance", "swim"]):
        category = "Health & Fitness"
        base_rev = 22000.0
        rain_elast = 0.022
        snow_elast = -0.045
        temp_elast = -0.020
        description = f"Health, wellness and fitness facility: {clean_name}"
    elif any(k in lower_n for k in ["restaurant", "cafe", "bistro", "diner", "bar", "pub", "brewery", "grill", "bakery", "lounge"]):
        category = "Food & Hospitality"
        base_rev = 29000.0
        rain_elast = -0.040
        snow_elast = -0.075
        temp_elast = 0.010
        description = f"Hospitality food service entity: {clean_name}"
    elif any(k in lower_n for k in ["delivery", "courier", "shipping", "freight", "truck", "warehouse", "logistics", "moving"]):
        category = "Logistics & Transport"
        base_rev = 60000.0
        rain_elast = 0.030
        snow_elast = 0.060
        temp_elast = -0.010
        description = f"Logistics dispatch and transport service: {clean_name}"
    elif any(k in lower_n for k in ["pharmacy", "clinic", "hospital", "doctor", "medical", "dental", "vet", "pet"]):
        category = "Healthcare & Pet Services"
        base_rev = 40000.0
        rain_elast = 0.010
        snow_elast = 0.045
        temp_elast = -0.030
        description = f"Essential healthcare and clinical services: {clean_name}"
    elif any(k in lower_n for k in ["retail", "shop", "store", "boutique", "mall", "market", "outlet", "apparel", "clothing"]):
        category = "Retail & Commerce"
        base_rev = 36000.0
        rain_elast = -0.020
        snow_elast = 0.025
        temp_elast = -0.015
        description = f"Commercial retail store: {clean_name}"
    elif any(k in lower_n for k in ["car wash", "auto wash", "detailing"]):
        category = "Automotive Care"
        base_rev = 14000.0
        rain_elast = -0.120
        snow_elast = -0.170
        temp_elast = 0.030
        description = f"Weather-dependent vehicle cleaning facility: {clean_name}"
    elif any(k in lower_n for k in ["ice cream", "gelato", "frozen", "smoothie", "juice", "slush", "acai"]):
        category = "Chilled Refreshments"
        base_rev = 15000.0
        rain_elast = -0.060
        snow_elast = -0.130
        temp_elast = 0.060
        description = f"Chilled refreshment specialty business: {clean_name}"
    elif any(k in lower_n for k in ["coffee", "tea", "soup", "hot pot", "ramen", "fondue"]):
        category = "Hot Food & Beverages"
        base_rev = 19000.0
        rain_elast = 0.032
        snow_elast = 0.055
        temp_elast = -0.035
        description = f"Hot food and comfort beverage enterprise: {clean_name}"
        
    # User override parameters if specified
    if custom_rev is not None and custom_rev > 0:
        base_rev = float(custom_rev)
    if custom_rain is not None:
        rain_elast = float(custom_rain) / 100.0
    if custom_temp is not None:
        temp_elast = float(custom_temp) / 100.0
        
    if custom_color and str(custom_color).startswith("#"):
        chosen_color = str(custom_color)
    else:
        palette_idx = (existing_count + abs(hash(clean_name))) % len(HIGH_VISIBILITY_PALETTE)
        chosen_color = HIGH_VISIBILITY_PALETTE[palette_idx]
    
    return {
        "slug": slug,
        "config": {
            "name": clean_name,
            "category": category,
            "description": description,
            "color": chosen_color,
            "dash": "solid",
            "symbol": "circle",
            "base_daily_rev": base_rev,
            "rain_elasticity": round(rain_elast, 3),
            "snow_elasticity": round(snow_elast, 3),
            "temp_elasticity": round(temp_elast, 3),
        }
    }


def aggregate_daily_financials(df):
    """Aggregates hourly raw data to daily business level."""
    daily = df.groupby(["metro_area", "date_str"]).agg({
        "precip_accumulation_mm": "sum",
        "snow_depth_delta_cm": "sum",
        "air_temp_deg_c": "mean",
        "temp_anomaly_deg_c": "mean",
        "sustained_wind_kmh": "mean",
        "day_name": "first",
        "month_name": "first"
    }).reset_index()
    
    daily["date"] = pd.to_datetime(daily["date_str"])
    daily = daily.sort_values(["metro_area", "date"]).reset_index(drop=True)
    
    def get_weather_condition(row):
        if row["snow_depth_delta_cm"] > 1.0:
            return "Snow"
        elif row["precip_accumulation_mm"] > 5.0:
            return "Heavy Rain"
        elif row["precip_accumulation_mm"] > 0.5:
            return "Light Rain"
        elif row["air_temp_deg_c"] > 32.0:
            return "Heatwave"
        elif row["air_temp_deg_c"] < 0.0:
            return "Freezing"
        else:
            return "Clear"
            
    daily["weather_icon"] = daily.apply(get_weather_condition, axis=1)
    return daily


def calculate_custom_business_daily_series(df_daily, business_keys, custom_catalog=None):
    """
    Computes daily actual revenue and normal expected baseline revenue line series
    for any combination of selected businesses (preset or custom).
    """
    df = df_daily.copy()
    dow_factors = [0.90, 0.92, 0.96, 1.05, 1.35, 1.45, 1.25]
    catalog = custom_catalog if custom_catalog else BUSINESS_CATALOG
    
    for b_key in business_keys:
        if b_key not in catalog:
            continue
        cfg = catalog[b_key]
        
        base_series = np.array([
            cfg["base_daily_rev"] * dow_factors[d.dayofweek] for d in df["date"]
        ])
        
        rain_effect = df["precip_accumulation_mm"].values * cfg["rain_elasticity"]
        snow_effect = df["snow_depth_delta_cm"].values * cfg["snow_elasticity"]
        temp_effect = df["temp_anomaly_deg_c"].values * cfg["temp_elasticity"]
        
        total_weather_multiplier = np.maximum(0.15, 1.0 + rain_effect + snow_effect + temp_effect)
        
        actual_rev = np.round(base_series * total_weather_multiplier, 2)
        base_rev = np.round(base_series, 2)
        net_impact = np.round(actual_rev - base_rev, 2)
        
        df[f"{b_key}_actual_rev"] = actual_rev
        df[f"{b_key}_baseline_rev"] = base_rev
        df[f"{b_key}_net_impact"] = net_impact
        
    return df


def generate_business_specific_why_insight(b_key, row, custom_catalog=None):
    """
    Generates concise, plain-English explanations for any business (preset or user-created).
    """
    catalog = custom_catalog if custom_catalog else BUSINESS_CATALOG
    if b_key not in catalog:
        return {}
    cfg = catalog[b_key]
    
    actual = row.get(f"{b_key}_actual_rev", 0.0)
    baseline = row.get(f"{b_key}_baseline_rev", 0.0)
    delta = actual - baseline
    pct_change = (delta / baseline * 100.0) if baseline > 0 else 0.0
    
    rain = row["precip_accumulation_mm"]
    snow = row["snow_depth_delta_cm"]
    temp = row["air_temp_deg_c"]
    
    bullets = []
    
    if rain > 4.0 or snow > 1.0:
        if cfg["rain_elasticity"] > 0 or cfg["snow_elasticity"] > 0:
            headline = f"Adverse weather increased customer demand by {pct_change:+.1f}%"
            bullets.append(f"Precipitation prompted consumers to shift activity toward {cfg['name']}.")
            bullets.append(f"Earned {'+$' if delta>=0 else '-$'}{abs(delta):,.0f} above clear-weather baseline.")
        else:
            headline = f"Precipitation reduced customer volume by {abs(pct_change):.1f}%"
            bullets.append(f"Adverse weather caused customer footfall and visits to drop.")
            bullets.append(f"Lost -${abs(delta):,.0f} compared to expected clear-day sales.")
    elif temp > 32.0:
        if cfg["temp_elasticity"] > 0.02:
            headline = f"Heatwave conditions boosted demand by {pct_change:+.1f}%"
            bullets.append(f"High ambient temperatures ({temp:.1f}°C) drove elevated customer activity.")
        elif cfg["temp_elasticity"] < -0.02:
            headline = f"Extreme heat suppressed outdoor activity ({pct_change:+.1f}%)"
            bullets.append("Uncomfortably hot temperatures caused customers to avoid unshaded areas.")
        else:
            headline = f"Warm temperatures supported baseline operations ({pct_change:+.1f}%)"
            bullets.append("Seasonal temperatures maintained steady baseline customer traffic.")
    elif temp < 2.0:
        if cfg["temp_elasticity"] < -0.02:
            headline = f"Cold temperatures ({temp:.1f}°C) boosted revenue by {pct_change:+.1f}%"
            bullets.append("Cold snap spurred immediate consumer demand for winter essentials.")
        else:
            headline = f"Freezing weather caused a {pct_change:+.1f}% shift in customer traffic"
            bullets.append("Low temperatures altered customer transit and shopping habits.")
    else:
        headline = "Clear day; business performed close to normal expected sales"
        bullets.append(f"Revenue was primarily determined by standard {row['day_name']} weekly patterns.")
        
    return {
        "name": cfg["name"],
        "category": cfg.get("category", "General"),
        "actual_rev": actual,
        "baseline_rev": baseline,
        "delta": delta,
        "pct_change": pct_change,
        "headline": headline,
        "bullets": bullets
    }


def analyze_inter_business_linkages(active_keys, row, custom_catalog=None):
    """
    Computes cross-business ripple effects dynamically for any combination of active businesses.
    """
    catalog = custom_catalog if custom_catalog else BUSINESS_CATALOG
    linkages = []
    
    if "dine_in_restaurant" in active_keys and "food_delivery" in active_keys:
        dine_delta = row.get("dine_in_restaurant_net_impact", 0.0)
        deliv_delta = row.get("food_delivery_net_impact", 0.0)
        if dine_delta < 0 and deliv_delta > 0:
            linkages.append({
                "title": "Customer Switch: Dine-In to Food Delivery",
                "summary": f"Dine-in lost -${abs(dine_delta):,.0f} in tables, while Food Delivery gained +${deliv_delta:,.0f} in orders.",
                "chain_steps": [
                    "Step 1: Rain and cold weather start in the evening.",
                    "Step 2: Diners cancel restaurant reservations to avoid traveling outside.",
                    "Step 3: Those same diners order food online from home instead.",
                    "Outcome: Dine-in loses walk-in money, while delivery platforms make extra revenue."
                ],
                "type": "Direct Customer Substitution"
            })
            
    if "bikeshare_operator" in active_keys and "rideshare_fleet" in active_keys:
        bike_delta = row.get("bikeshare_operator_net_impact", 0.0)
        ride_delta = row.get("rideshare_fleet_net_impact", 0.0)
        if bike_delta < 0 and ride_delta > 0:
            linkages.append({
                "title": "Commuter Shift: Bike-Share to Taxis & Rideshares",
                "summary": f"Bicycle trips dropped by -${abs(bike_delta):,.0f}, while Rideshare revenue surged +${ride_delta:,.0f}.",
                "chain_steps": [
                    "Step 1: Wet roads make riding bicycles and scooters dangerous and unpleasant.",
                    "Step 2: Commuters abandon outdoor bike stations.",
                    "Step 3: Commuters open rideshare apps to stay dry in cars.",
                    "Outcome: Bike-sharing loses rental income, while taxi and rideshare companies see surging fares."
                ],
                "type": "Commuter Mode Change"
            })
            
    if "car_wash" in active_keys and "rideshare_fleet" in active_keys:
        rain = row["precip_accumulation_mm"]
        if rain > 3.0:
            linkages.append({
                "title": "Weather Halt: Car Wash Drop vs. Rideshare Surge",
                "summary": "Car washes see immediate volume collapse, while city rideshares experience high surge multipliers.",
                "chain_steps": [
                    "Step 1: Precipitation makes washing private cars futile for vehicle owners.",
                    "Step 2: Car wash bays sit empty with -85% footfall.",
                    "Step 3: Simultaneously, rain forces city travelers into private rideshare vehicles.",
                    "Outcome: Car wash owners experience idle shifts, while rideshare drivers earn surge earnings."
                ],
                "type": "Outdoor Service Postponement"
            })
            
    if "golf_theme_park" in active_keys and "movie_theaters" in active_keys:
        golf_delta = row.get("golf_theme_park_net_impact", 0.0)
        movie_delta = row.get("movie_theaters_net_impact", 0.0)
        if golf_delta < 0 and movie_delta > 0:
            linkages.append({
                "title": "Leisure Substitution: Outdoor Attractions to Indoor Cinema",
                "summary": f"Outdoor golf/parks lost -${abs(golf_delta):,.0f}, while indoor movie theaters gained +${movie_delta:,.0f}.",
                "chain_steps": [
                    "Step 1: Rainy weekend weather shuts down golf courses and outdoor theme park rides.",
                    "Step 2: Families and recreational visitors seek indoor weekend alternatives.",
                    "Step 3: Demand shifts directly to indoor multiplexes, bowling alleys, and arcades.",
                    "Outcome: Outdoor venues experience revenue deficits while indoor venues sell out."
                ],
                "type": "Recreational Substitution"
            })
            
    if "rideshare_fleet" in active_keys and "freight_logistics" in active_keys:
        rain = row["precip_accumulation_mm"]
        if rain > 3.0:
            linkages.append({
                "title": "Traffic Ripple: Car Rush to Trucking & Delivery Delays",
                "summary": "City road traffic jumped +35%, causing freight trucks to lose 25 minutes per trip.",
                "chain_steps": [
                    "Step 1: Rain prompts thousands of commuters to take cars instead of walking or biking.",
                    "Step 2: City streets and highways become congested with extra vehicles.",
                    "Step 3: Freight delivery trucks and warehouse shipments get stuck in traffic jams.",
                    "Outcome: Delivery drivers take longer to complete drop-offs, increasing operating costs."
                ],
                "type": "Indirect Traffic Ripple Effect"
            })
            
    if "ice_cream_beverages" in active_keys and "hot_cafe_bakery" in active_keys:
        ice_delta = row.get("ice_cream_beverages_net_impact", 0.0)
        cafe_delta = row.get("hot_cafe_bakery_net_impact", 0.0)
        if row["air_temp_deg_c"] > 30.0:
            linkages.append({
                "title": "Temperature Preference: Cold Drinks vs Hot Bakeries",
                "summary": f"Cold drinks surged +${ice_delta:,.0f}, while hot baked goods dipped -${abs(cafe_delta):,.0f}.",
                "chain_steps": [
                    "Step 1: Afternoon temperatures spike above 30°C.",
                    "Step 2: Customers seek immediate cooling refreshments and avoid hot food.",
                    "Step 3: Spending redirects from hot coffee and fresh baked pastries to iced drinks and gelato.",
                    "Outcome: Cold treat parlors gain sales, while hot bakeries experience a summer slowdown."
                ],
                "type": "Product Preference Shift"
            })
            
    # Generic linkage for custom user-created pairs if one gains and one loses
    custom_active = [k for k in active_keys if k not in ["food_delivery", "dine_in_restaurant", "rideshare_fleet", "bikeshare_operator", "car_wash", "golf_theme_park", "movie_theaters", "ice_cream_beverages", "hot_cafe_bakery", "freight_logistics"]]
    if len(custom_active) >= 1 and len(linkages) == 0:
        c_k = custom_active[0]
        c_cfg = catalog[c_k]
        c_delta = row.get(f"{c_k}_net_impact", 0.0)
        if c_delta != 0:
            linkages.append({
                "title": f"Custom Business Sensitivity: {c_cfg['name']}",
                "summary": f"{c_cfg['name']} experienced a {'+$' if c_delta>=0 else '-$'}{abs(c_delta):,.0f} weather shift ({c_cfg.get('category', 'Custom')}).",
                "chain_steps": [
                    f"Step 1: Meteorological conditions altered standard consumer behavior in {c_cfg.get('category', 'Custom')}.",
                    f"Step 2: Operational sensitivity (Rain: {c_cfg['rain_elasticity']*100:+.1f}%, Temp: {c_cfg['temp_elasticity']*100:+.1f}%) modulated baseline demand.",
                    f"Outcome: Net revenue deviated by {'+$' if c_delta>=0 else '-$'}{abs(c_delta):,.0f} relative to normal expected sales."
                ],
                "type": "Dynamic Model Output"
            })
            
    return linkages


def generate_future_ai_forecast(active_keys, forecast_event, custom_catalog=None):
    """
    Generates a 7-day forward projection line series and operational recommendations
    for any combination of preset or custom businesses.
    """
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    catalog = custom_catalog if custom_catalog else BUSINESS_CATALOG
    
    if "Rainstorm" in forecast_event:
        weather_profile = [0.0, 0.5, 8.5, 12.0, 4.0, 0.0, 0.0]
        desc = "Rainstorm system forecasted for Wednesday through Friday."
    elif "Blizzard" in forecast_event:
        weather_profile = [0.0, 0.0, 0.0, 5.0, 8.0, 2.0, 0.0]
        desc = "Blizzard and freezing conditions forecasted for Thursday through Saturday."
    elif "Heatwave" in forecast_event:
        weather_profile = [28.0, 32.0, 36.0, 38.0, 39.0, 35.0, 30.0]
        desc = "High-temperature heatwave system with temperatures exceeding 38°C."
    else:
        weather_profile = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        desc = "Clear weather conditions anticipated across the upcoming 7-day window."
        
    projections = {}
    total_impact_all = 0.0
    
    for b_key in active_keys:
        if b_key not in catalog:
            continue
        cfg = catalog[b_key]
        base = cfg["base_daily_rev"]
        series_actual = []
        series_base = []
        
        for i, w_val in enumerate(weather_profile):
            dow_m = [0.88, 0.90, 0.95, 1.05, 1.38, 1.48, 1.28][i]
            day_base = base * dow_m
            
            if "Rain" in forecast_event:
                mult = 1.0 + w_val * cfg["rain_elasticity"]
            elif "Blizzard" in forecast_event:
                mult = 1.0 + w_val * cfg["snow_elasticity"]
            elif "Heatwave" in forecast_event:
                mult = 1.0 + (w_val - 25.0) * cfg["temp_elasticity"]
            else:
                mult = 1.0
                
            day_act = day_base * max(0.15, mult)
            series_base.append(round(day_base, 0))
            series_actual.append(round(day_act, 0))
            
        projections[b_key] = {
            "name": cfg["name"],
            "color": cfg.get("color", "#000000"),
            "dash": cfg.get("dash", "solid"),
            "symbol": cfg.get("symbol", "circle"),
            "days": days,
            "actual_series": series_actual,
            "baseline_series": series_base,
            "net_week_impact": sum(series_actual) - sum(series_base)
        }
        total_impact_all += (sum(series_actual) - sum(series_base))
        
    ai_advice = []
    if "food_delivery" in active_keys and ("Rain" in forecast_event or "Blizzard" in forecast_event):
        ai_advice.append("Food Delivery Staffing: Driver numbers drop by ~20% during rain. Add a small bonus (+3.50 per order) 45 minutes before the storm starts so orders are delivered on time.")
    if "dine_in_restaurant" in active_keys and ("Rain" in forecast_event or "Blizzard" in forecast_event):
        ai_advice.append("Restaurant Operations: Outdoor dining will be empty. Move dining room floor waiters to help pack takeout and delivery boxes in the kitchen.")
    if "car_wash" in active_keys and "Rain" in forecast_event:
        ai_advice.append("Car Wash Operations: Shift staff hours away from rainy Wednesday/Thursday and schedule maximum wash lane capacity for clear post-storm weekend days.")
    if "movie_theaters" in active_keys and "Rain" in forecast_event:
        ai_advice.append("Theater Concessions: Rainy weekend will boost cinema footfall by +35%. Increase popcorn and beverage inventory orders by Tuesday afternoon.")
    if "hvac_home_services" in active_keys and ("Heatwave" in forecast_event or "Blizzard" in forecast_event):
        ai_advice.append("HVAC Dispatch: Extreme temperatures will drive a +65% surge in emergency calls. Put on-call emergency technicians on standby.")
    if "retail_apparel" in active_keys and "Rain" in forecast_event:
        ai_advice.append("Retail Stores: Put umbrellas, raincoats, and waterproof shoes right at the entrance display by Wednesday morning.")
    if "ice_cream_beverages" in active_keys and "Heatwave" in forecast_event:
        ai_advice.append("Cold Drinks Inventory: Sales of cold treats will jump +45%. Double your ice orders and check that refrigerators are running cold.")
    if "golf_theme_park" in active_keys and "Rain" in forecast_event:
        ai_advice.append("Outdoor Venues: Rain will reduce tee times and ticket sales by -75%. Offer indoor simulator discounts or rain-check booking vouchers.")
        
    if not ai_advice:
        ai_advice.append("Standard Operations: Regular conditions expected. Maintain baseline staffing schedules and normal inventory reorder points.")
        
    return {
        "weather_desc": desc,
        "days": days,
        "projections": projections,
        "total_impact_all": total_impact_all,
        "ai_advice": ai_advice
    }
