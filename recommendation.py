from schemas import SurveyCreate

CARS_DB = [
    {"name": "Maruti Alto K10", "budget": "Under 5 lakh", "type": "Hatchback", "fuel": "Petrol", "usage": "City"},
    {"name": "Hyundai i20", "budget": "5-10 lakh", "type": "Hatchback", "fuel": "Petrol", "usage": "City"},
    {"name": "Maruti Swift Dzire", "budget": "5-10 lakh", "type": "Sedan", "fuel": "Petrol", "usage": "City"},
    {"name": "Honda City", "budget": "10-15 lakh", "type": "Sedan", "fuel": "Petrol", "usage": "Both"},
    {"name": "Hyundai Creta", "budget": "10-15 lakh", "type": "SUV", "fuel": "Petrol", "usage": "Both"},
    {"name": "Tata Nexon", "budget": "10-15 lakh", "type": "SUV", "fuel": "Petrol", "usage": "Both"},
    {"name": "Mahindra XUV700", "budget": "15+ lakh", "type": "SUV", "fuel": "Diesel", "usage": "Both"},
    {"name": "Tata Tiago EV", "budget": "5-10 lakh", "type": "Hatchback", "fuel": "Electric", "usage": "City"},
    {"name": "Toyota Innova Crysta", "budget": "15+ lakh", "type": "SUV", "fuel": "Diesel", "usage": "Highway"},
    {"name": "Kia Seltos", "budget": "10-15 lakh", "type": "SUV", "fuel": "Petrol", "usage": "Both"},
    {"name": "Tata Safari", "budget": "15+ lakh", "type": "SUV", "fuel": "Diesel", "usage": "Highway"},
    {"name": "Mahindra Thar", "budget": "15+ lakh", "type": "SUV", "fuel": "Diesel", "usage": "Both"},
    {"name": "Maruti Baleno", "budget": "5-10 lakh", "type": "Hatchback", "fuel": "Petrol", "usage": "City"},
    {"name": "Hyundai Verna", "budget": "10-15 lakh", "type": "Sedan", "fuel": "Petrol", "usage": "Both"},
    {"name": "MG Hector", "budget": "15+ lakh", "type": "SUV", "fuel": "Petrol", "usage": "Both"},
    {"name": "Honda Elevate", "budget": "10-15 lakh", "type": "SUV", "fuel": "Petrol", "usage": "Both"},
    {"name": "Mahindra Scorpio-N", "budget": "15+ lakh", "type": "SUV", "fuel": "Diesel", "usage": "Both"},
    {"name": "Maruti WagonR", "budget": "Under 5 lakh", "type": "Hatchback", "fuel": "Petrol", "usage": "City"},
    {"name": "Hyundai Alcazar", "budget": "15+ lakh", "type": "SUV", "fuel": "Diesel", "usage": "Both"},
    {"name": "MG Astor", "budget": "10-15 lakh", "type": "SUV", "fuel": "Petrol", "usage": "Both"}
]

def recommend_cars(data: SurveyCreate):
    results = []
    
    for car in CARS_DB:
        score = 0
        max_score = 40
        reasons = []
        
        # Priority Checks (Since priority can be multiple, we check for presence)
        priorities = data.priority.lower()

        # Budget match (High weight)
        if car["budget"] == data.budget:
            score += 15
            reasons.append("Perfectly fits your budget")
            if "budget" in priorities:
                score += 10 # Bonus for hitting budget priority
        elif (car["budget"] == "5-10 lakh" and data.budget == "Under 5 lakh") or \
             (car["budget"] == "10-15 lakh" and data.budget == "5-10 lakh"):
             score += 5
             reasons.append("Slightly above budget, but good value")
             
        # Feature Priority matches
        if "performance" in priorities and car["name"] in ["Honda City", "Kia Seltos", "Mahindra XUV700", "Mahindra Scorpio-N", "Hyundai Verna"]:
            score += 8
            reasons.append("Excellent performance metrics")
            
        if "comfort" in priorities and car["name"] in ["Toyota Innova Crysta", "Honda City", "Hyundai Creta", "MG Hector", "Tata Safari", "Hyundai Alcazar"]:
            score += 8
            reasons.append("Highly rated for passenger comfort")
            
        if "status" in priorities and car["name"] in ["Mahindra XUV700", "Hyundai Creta", "Toyota Innova Crysta", "Mahindra Thar", "Tata Safari", "Mahindra Scorpio-N"]:
            score += 8
            reasons.append("Strong road presence and status")

        # Fuel Match
        if car["fuel"].lower() == data.fuel_type.lower():
            score += 10
            reasons.append(f"Matches preferred fuel type ({data.fuel_type})")
            
        # EV Interest
        if car["fuel"] == "Electric":
            if data.ev_interest.lower() == "yes":
                score += 15
                reasons.append("Great EV option")
            elif data.ev_interest.lower() == "no":
                score -= 20
                
        # Type match
        if car["type"].lower() == data.car_type.lower():
            score += 10
            reasons.append(f"Matches preferred body style ({data.car_type})")
            
        # Usage match
        if car["usage"].lower() == data.driving_area.lower() or car["usage"] == "Both":
            score += 5
            reasons.append("Suitable for your driving area")
            
        percentage = min(int((score / max_score) * 100), 100)
        percentage = max(percentage, 10) # Minimum 10% match
        
        if len(reasons) == 0:
            reasons.append("Alternative option based on general criteria")
            
        results.append({
            "name": car["name"],
            "match_percentage": percentage,
            "reasons": list(set(reasons))[:2] # Max 2 reasons
        })
        
    results = sorted(results, key=lambda x: x["match_percentage"], reverse=True)
    return results[:5] # Return top 5

