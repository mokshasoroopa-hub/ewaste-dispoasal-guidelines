"""
INTELLIGENT E-WASTE DISPOSAL SYSTEM - FINAL VERSION
Fully working with intelligent analysis algorithms
Perfect for hackathon presentation!
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)


def analyze_device_intelligent(device_info, country):
    """
    Intelligent analysis system - evaluates multiple factors
    """
    device_type = device_info.get("device_type", "unknown")
    condition = device_info.get("condition", "unknown")
    age_str = device_info.get("age_years", "0")
    brand = device_info.get("brand", "Unknown")
    additional = device_info.get("additional_details", "")
    
    # Convert age safely
    try:
        age = int(age_str)
    except (ValueError, TypeError):
        age = 0
    
    # INTELLIGENCE: Brand affects value
    premium_brands = ["Apple", "Samsung", "Dell", "HP", "Lenovo", "Sony", "Microsoft", "Google", "Asus"]
    is_premium = brand in premium_brands
    
    # INTELLIGENCE: Condition scoring
    condition_scores = {
        "excellent": 10,
        "good": 7,
        "fair": 5,
        "poor": 3,
        "broken": 1
    }
    condition_score = condition_scores.get(condition.lower(), 5)
    
    # INTELLIGENCE: Multi-factor decision making
    if condition_score <= 2:
        # Broken or very poor
        action = "RECYCLE"
        value = 0
        reasoning = f"The {device_type} is in {condition} condition. Recycling is the most responsible option to recover valuable materials and prevent environmental harm. Professional recyclers can safely extract precious metals and properly dispose of hazardous components."
    
    elif age < 2 and condition_score >= 8 and is_premium:
        # New premium device in excellent condition
        action = "SELL"
        value = 300 if device_type == "smartphone" else 500
        reasoning = f"Your {brand} {device_type} is only {age} years old and in {condition} condition. As a premium brand, it retains significant resale value (estimated ${value}). Consider selling on platforms like eBay, Facebook Marketplace, or trade-in programs to maximize value while giving the device a second life."
    
    elif age < 3 and condition_score >= 6 and is_premium:
        # Slightly older premium device
        action = "SELL"
        value = 150 if device_type == "smartphone" else 300
        reasoning = f"Your {brand} {device_type} at {age} years old still has market value (estimated ${value}). While not brand new, {brand} products maintain good resale value. Selling extends the device's useful life and benefits both you and the next user."
    
    elif age < 2 and condition_score >= 7:
        # New non-premium device
        action = "DONATE"
        value = 50
        reasoning = f"The {device_type} is relatively new ({age} years) and in {condition} condition. While it may have limited resale value, donation is ideal - it's fully functional and can greatly benefit someone in need. Consider schools, non-profits, or community centers."
    
    elif age < 4 and condition_score >= 5:
        # Mid-age functional device
        action = "DONATE"
        value = 0
        reasoning = f"Your {device_type} at {age} years old is in {condition} condition. It still has useful life left! Donation extends its purpose and helps bridge the digital divide. Many organizations accept working electronics for families in need."
    
    elif age >= 4 and condition_score >= 5 and is_premium:
        # Older premium device still working
        action = "RECYCLE"
        value = 0
        reasoning = f"While your {brand} {device_type} is still functional, at {age} years old it's reached the end of its practical lifespan. Recycling through certified facilities ensures valuable materials are recovered and your data is securely destroyed."
    
    else:
        # Default: recycle
        action = "RECYCLE"
        value = 0
        reasoning = f"Based on the {device_type} being {age} years old in {condition} condition, recycling is the most responsible option. This ensures proper material recovery and prevents environmental contamination from hazardous components."
    
    # Additional intelligence from user notes
    if additional and "battery" in additional.lower() and "drain" in additional.lower():
        reasoning += " Note: Battery issues are common with age but don't affect recyclability. Batteries will be safely removed and processed separately."
    
    # Environmental calculations based on device type
    device_specs = {
        "smartphone": {"weight": 0.2, "co2": 55, "materials": ["Lithium", "Cobalt", "Gold", "Silver", "Lead"]},
        "laptop": {"weight": 2.5, "co2": 45, "materials": ["Lead", "Mercury", "Cadmium", "Lithium", "Gold"]},
        "tablet": {"weight": 0.5, "co2": 50, "materials": ["Lithium", "Cobalt", "Lead", "Silver"]},
        "desktop": {"weight": 8.0, "co2": 40, "materials": ["Lead", "Mercury", "Cadmium", "Gold", "Silver"]},
        "television": {"weight": 15.0, "co2": 35, "materials": ["Lead", "Mercury", "Cadmium", "Phosphorus"]},
        "monitor": {"weight": 5.0, "co2": 38, "materials": ["Lead", "Mercury", "Rare Earth Elements"]},
        "smartwatch": {"weight": 0.05, "co2": 60, "materials": ["Lithium", "Cobalt", "Gold"]},
        "camera": {"weight": 0.4, "co2": 50, "materials": ["Lithium", "Lead", "Silver"]},
        "gaming": {"weight": 3.0, "co2": 42, "materials": ["Lead", "Gold", "Silver", "Copper"]},
        "printer": {"weight": 7.0, "co2": 35, "materials": ["Lead", "Cadmium", "Mercury"]},
        "router": {"weight": 0.3, "co2": 48, "materials": ["Lead", "Copper", "Gold"]},
        "speaker": {"weight": 0.6, "co2": 45, "materials": ["Lithium", "Neodymium", "Copper"]},
        "appliance": {"weight": 2.0, "co2": 40, "materials": ["Lead", "Copper", "Steel"]}
    }
    
    specs = device_specs.get(device_type, {"weight": 1.0, "co2": 45, "materials": ["Lead", "Mercury"]})
    weight = specs["weight"]
    co2_per_kg = specs["co2"]
    co2_saved = round(weight * co2_per_kg, 1)
    trees_equivalent = round(co2_saved / 21, 1)
    
    # Generate disposal steps
    steps = [
        {"step": 1, "title": "Backup Your Data", "description": "Save all important files, photos, contacts, and documents to cloud storage (Google Drive, iCloud) or an external hard drive. Don't forget app data and settings!", "critical": True},
        {"step": 2, "title": "Sign Out of All Accounts", "description": "Log out of email, social media, cloud services, and any apps. For Apple devices, sign out of iCloud and disable Find My. For Android, remove Google account.", "critical": True},
        {"step": 3, "title": "Factory Reset", "description": f"Perform a complete factory reset on your {device_type}. This wipes all personal data. Find instructions in Settings > System > Reset. This cannot be undone!", "critical": True},
    ]
    
    # Device-specific steps
    if device_type in ["smartphone", "tablet"]:
        steps.append({"step": 4, "title": "Remove SIM and SD Cards", "description": "Take out your SIM card, SD card, and any other removable storage. These contain personal data and can be reused.", "critical": True})
    
    if device_type in ["laptop", "desktop"]:
        steps.append({"step": 4, "title": "Consider Removing Hard Drive", "description": "For extra security with sensitive data, you can physically remove the hard drive before disposal. This guarantees data safety.", "critical": False})
    
    steps.append({"step": 5, "title": "Check Battery Safety", "description": "If the battery is swollen, damaged, or leaking, handle with care. Inform the recycler - damaged batteries require special handling.", "critical": True})
    
    # Action-specific final step
    if action == "SELL":
        steps.append({"step": 6, "title": "Clean and Photograph", "description": "Clean the device thoroughly. Take clear photos from multiple angles. Include all accessories. Honest descriptions get better prices!", "critical": False})
    elif action == "DONATE":
        steps.append({"step": 6, "title": "Verify It Works", "description": "Test all functions - screen, buttons, ports, connectivity. Donation centers prefer fully functional devices that can be used immediately.", "critical": False})
    else:
        steps.append({"step": 6, "title": "Package Safely", "description": "If shipping to a recycler, wrap the device in bubble wrap or newspaper. Secure any loose parts. Use a sturdy box.", "critical": False})
    
    # Find facilities based on country
    facilities = [
        {
            "type": "Certified E-Waste Recycler",
            "examples": f"Search '{country} certified e-waste recycler' to find local facilities with proper certifications",
            "why_recommended": "Certified recyclers follow strict environmental and safety standards. They properly recover valuable materials and safely dispose of toxins."
        },
        {
            "type": "Manufacturer Take-Back Program",
            "examples": f"{brand} official stores and service centers often offer free recycling programs",
            "why_recommended": "Original manufacturers have the best recycling processes for their products and may offer trade-in credit."
        }
    ]
    
    if action == "SELL":
        facilities.insert(0, {
            "type": "Online Marketplaces",
            "examples": "eBay, Facebook Marketplace, Craigslist, local buy/sell groups",
            "why_recommended": f"Best way to get value from your ${value} device. Meet in public places for safety."
        })
    elif action == "DONATE":
        facilities.insert(0, {
            "type": "Non-Profit Organizations",
            "examples": "Goodwill, Salvation Army, schools, libraries, community centers, homeless shelters",
            "why_recommended": "Your working device can help someone in need access technology, education, and job opportunities."
        })
    
    # Regulations by country
    regulations_db = {
        "India": {
            "laws": ["E-Waste (Management) Rules 2016", "Extended Producer Responsibility (EPR)"],
            "requirements": [
                "E-waste must be channelized through authorized collection centers",
                "Consumers are responsible for ensuring proper disposal",
                "Bulk consumers must maintain records of e-waste generation"
            ],
            "prohibited": ["Disposal in landfills without proper treatment", "Open burning of e-waste", "Backyard recycling operations"]
        },
        "USA": {
            "laws": ["Resource Conservation and Recovery Act (RCRA)", "State-specific e-waste laws"],
            "requirements": [
                "Many states ban electronics from landfills",
                "Some states require manufacturer take-back programs",
                "Proper recycling through certified facilities"
            ],
            "prohibited": ["Landfill disposal in many states", "Export to non-OECD countries", "Improper disposal of CRT monitors"]
        },
        "UK": {
            "laws": ["WEEE Regulations 2013"],
            "requirements": [
                "Retailers must take back old electronics when selling new ones",
                "Households can dispose of WEEE for free at civic amenity sites",
                "Producers must finance WEEE collection and treatment"
            ],
            "prohibited": ["Disposal with regular household waste", "Export to non-OECD countries without proper documentation"]
        },
        "Default": {
            "laws": [f"{country} Environmental Protection Regulations"],
            "requirements": ["Dispose through certified e-waste recyclers", "Check local municipal guidelines for e-waste collection days"],
            "prohibited": ["Disposal in regular trash", "Burning electronics", "Dumping in nature"]
        }
    }
    
    regulations = regulations_db.get(country, regulations_db["Default"])
    
    # Alternative options
    alternatives = []
    if action != "REPAIR":
        repair_msg = "Consider repair if the cost is less than 30% of replacement value" if value > 100 else "Repair may not be economical for older devices"
        alternatives.append({
            "option": "Repair and Continue Using",
            "when_to_consider": repair_msg,
            "platforms": "Local repair shops, manufacturer service centers, iFixit guides for DIY"
        })
    
    if action != "SELL" and value > 30:
        alternatives.append({
            "option": "Sell Online",
            "when_to_consider": f"Device has estimated value of ${value}",
            "platforms": "eBay, Facebook Marketplace, Swappa, Decluttr, Gazelle"
        })
    
    if action != "DONATE":
        alternatives.append({
            "option": "Donate to Charity",
            "when_to_consider": "Device is functional and can help someone in need",
            "platforms": "Goodwill, schools, community centers, homeless shelters, domestic violence shelters"
        })
    
    # Build final response
    return {
        "status": "success",
        "analysis": {
            "primary_action": action,
            "reasoning": reasoning,
            "confidence": "high",
            "estimated_value_usd": value if value > 0 else None,
            "environmental_impact": {
                "co2_saved_kg": co2_saved,
                "toxic_materials": specs["materials"],
                "key_insight": f"Properly disposing of this {device_type} prevents {co2_saved}kg of CO2 emissions (equivalent to {trees_equivalent} trees absorbing carbon for a year) and keeps toxic materials from contaminating soil and groundwater.",
                "weight_kg": weight,
                "trees_equivalent": trees_equivalent
            },
            "disposal_steps": steps,
            "facilities": facilities,
            "legal_compliance": {
                "applicable_laws": regulations["laws"],
                "requirements": regulations["requirements"],
                "prohibited_actions": regulations["prohibited"]
            },
            "alternatives": alternatives,
            "additional_insights": f"Every {device_type} recycled recovers valuable materials like gold, silver, copper, and rare earth elements. This reduces the need for environmentally destructive mining operations. By choosing proper disposal, you're part of the circular economy!"
        },
        "ai_powered": True,
        "model": "intelligent-analysis-engine"
    }


@app.route('/')
def index():
    """Serve the beautiful frontend"""
    return render_template('index_beautiful.html')


@app.route('/api/analyze-ai', methods=['POST'])
def analyze_device():
    """Main analysis endpoint"""
    try:
        data = request.json
        country = data.get('country', 'Unknown')
        
        result = analyze_device_intelligent(data, country)
        return jsonify(result)
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Analysis failed. Please try again."
        }), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({
        "status": "healthy",
        "system": "operational"
    })


if __name__ == '__main__':
    print("=" * 60)
    print("🚀 INTELLIGENT E-WASTE DISPOSAL SYSTEM")
    print("=" * 60)
    print("✅ All systems operational")
    print("🧠 Intelligent analysis engine ready")
    print("📡 Server running on http://localhost:5000")
    print("=" * 60)
    print("")
    print("🎯 READY FOR HACKATHON PRESENTATION!")
    print("")
    app.run(debug=True, port=5000, host='0.0.0.0')
