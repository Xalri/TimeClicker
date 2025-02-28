import math


UPGRADES = [
    ### TEMPLATE UPGRADE
    # {"name": "upgrade1.1", "cost": 1000, "effect_type": "building", "effect_value": 2, "unlock": 10, "building_name": "Campfire"},
    # {"name": "upgrade1.2", "cost": 10000, "effect_type": "building", "effect_value": 2, "unlock": 20, "building_name": "Campfire"},
    # {"name": "upgrade1.3", "cost": 100000, "effect_type": "building", "effect_value": 2, "unlock": 50, "building_name": "Campfire"},
    
    # {"name": "upgrade2.1", "cost": 1000, "effect_type": "building", "effect_value": 2, "unlock": 10, "building_name": "Farming"},
    # {"name": "upgrade2.2", "cost": 10000, "effect_type": "building", "effect_value": 2, "unlock": 20, "building_name": "Farming"},
    # {"name": "upgrade2.3", "cost": 100000, "effect_type": "building", "effect_value": 2, "unlock": 50, "building_name": "Farming"},
    
    ### UPGRADES BUILDINGS
    # Préhistoire
    {"name": "Flint", "cost": 10000, "effect_type": "building", "effect_value": 4, "building_name": "Campfire"},
    {"name": "Hoe", "cost": 10000, "effect_type": "building", "unlock": 20, "effect_value": 2, "building_name": "Farming"},
    {"name": "Brush", "cost": 10000, "effect_type": "building", "unlock": 50, "effect_value": 2, "building_name": "Painting"},
    {"name": "Weapons", "cost": 10000, "effect_type": "building", "unlock": 100, "effect_value": 2, "building_name": "Hunting"},

    # # Antiquité
    {"name": "Stone", "cost": 10000, "effect_type": "building", "unlock": 10, "effect_value": 2, "building_name": "Aqueduct"},
    {"name": "Maths", "cost": 10000, "effect_type": "building", "unlock": 20, "effect_value": 2, "building_name": "Pyramid"},
    {"name": "Artefact", "cost": 10000, "effect_type": "building", "unlock": 50, "effect_value": 2, "building_name": "Temple"},
    {"name": "Gold", "cost": 10000, "effect_type": "building", "unlock": 100, "effect_value": 2, "building_name": "Cash"},
    
    # # Moyen Âge
    {"name": "Paper", "cost": 10000, "effect_type": "building", "unlock": 10, "effect_value": 2, "building_name": "Printing"},
    {"name": "Students", "cost": 10000, "effect_type": "building", "effect_value": 2, "unlock": 20, "building_name": "School"},
    {"name": "Monk", "cost": 10000, "effect_type": "building", "effect_value": 2, "unlock": 50, "building_name": "Church"},
    {"name": "Soldier", "cost": 10000, "effect_type": "building", "effect_value": 2, "unlock": 100, "building_name": "Castle"},
    
    # # Temps Modernes
    {"name": "Engineers", "cost": 10000, "effect_type": "building", "unlock": 10, "effect_value": 2, "building_name": "Steam Engine"},
    {"name": "Locomotive", "cost": 10000, "effect_type": "building", "effect_value": 2, "unlock": 20, "building_name": "Rail"},
    {"name": "Coal", "cost": 10000, "effect_type": "building", "effect_value": 2, "unlock": 50, "building_name": "Factory"},
    {"name": "Drivers", "cost": 10000, "effect_type": "building", "effect_value": 2, "unlock": 100, "building_name": "Car"},
    
    # # Époque Contemporaine
    {"name": "Printed Circuit", "cost": 10000, "effect_type": "building", "unlock": 10, "effect_value": 2, "building_name": "Electronic"},
    {"name": "Servers", "cost": 10000, "effect_type": "building", "effect_value": 2, "unlock": 20, "building_name": "Internet"},
    {"name": "Fuel", "cost": 10000, "effect_type": "building", "effect_value": 2, "unlock": 50, "building_name": "Rocket"},
    {"name": "Uranium", "cost": 10000, "effect_type": "building", "effect_value": 2, "unlock": 100, "building_name": "Nuclear Central"},
    
    # # Futur
    {"name": "Development", "cost": 10000, "effect_type": "building", "effect_value": 2, "unlock": 10, "building_name": "AI"},
    {"name": "Black Hole", "cost": 10000, "effect_type": "building", "effect_value": 2, "unlock": 20, "building_name": "Antimatter Central"},
    {"name": "Reactor", "cost": 10000, "effect_type": "building", "effect_value": 2, "unlock": 50, "building_name": "Spaceship"},
]

TIMELINE_UPGRADE = {"name": "Time", "cost": lambda x:  30 + (2 * 10**35 - 30) / (1 + math.exp(-0.1 * (x - 1789))), "effect_type": "timeline"}

treshold = [10, 20, 50, 100, 500, 1000]