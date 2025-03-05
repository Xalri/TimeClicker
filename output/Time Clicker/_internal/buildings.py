buildings = [
    # Préhistoire
    {"name": "Campfire", "cost": lambda x: (1.15**x)*15, "tps_boost": 0.1},
    {"name": "Farming", "cost": lambda x: (1.15**x)*100, "tps_boost": 1},
    {"name": "Painting", "cost": lambda x: (1.15**x)*1100, "tps_boost": 8},
    {"name": "Hunting", "cost": lambda x: (1.15**x)*12000, "tps_boost": 47},
    
    # Antiquité
    {"name": "Aqueduct", "cost": lambda x: (1.15**x)*130000, "tps_boost": 260},
    {"name": "Pyramid", "cost": lambda x: (1.15**x)*1400000, "tps_boost": 1400},
    {"name": "Temple", "cost": lambda x: (1.15**x)*20000000, "tps_boost": 7800},
    {"name": "Cash", "cost": lambda x: (1.15**x)*330000000, "tps_boost": 44000},
    
    # Moyen Âge
    {"name": "Printing", "cost": lambda x: (1.15**x)*5100000000, "tps_boost": 260000},
    {"name": "School", "cost": lambda x: (1.15**x)*75000000000, "tps_boost": 1600000},
    {"name": "Church", "cost": lambda x: (1.15**x)*1000000000000, "tps_boost": 10000000},
    {"name": "Castle", "cost": lambda x: (1.15**x)*14000000000000, "tps_boost": 65000000},
    
    # Temps Modernes
    {"name": "Steam Engine", "cost": lambda x: (1.15**x)*170000000000000, "tps_boost": 430000000},
    {"name": "Rail", "cost": lambda x: (1.15**x)*2100000000000000, "tps_boost": 2900000000},
    {"name": "Factory", "cost": lambda x: (1.15**x)*26000000000000000, "tps_boost": 21000000000},
    {"name": "Car", "cost": lambda x: (1.15**x)*310000000000000000, "tps_boost": 150000000000},
    
    # Époque Contemporaine
    {"name": "Electronic", "cost": lambda x: (1.15**x)*7100000000000000000, "tps_boost": 1100000000000},
    {"name": "Internet", "cost": lambda x: (1.15**x)*12000000000000000000000, "tps_boost": 8300000000000},
    {"name": "Rocket", "cost": lambda x: (1.15**x)*1900000000000000000000000, "tps_boost": 64000000000000},
    {"name": "Nuclear Central", "cost": lambda x: (1.15**x)*540000000000000000000000000, "tps_boost": 510000000000000},
    
    # Futur
    {"name": "AI", "cost": lambda x: (1.15**x)*30000000000000000000000000000, "tps_boost": 4000000000000000},
    {"name": "Antimatter Central", "cost": lambda x: (1.15**x)*4200000000000000000000000000000, "tps_boost": 31000000000000000},
    {"name": "Spaceship", "cost": lambda x: (1.15**x)*630000000000000000000000000000000, "tps_boost": 240000000000000000},
    {"name": "Time Machine", "cost": lambda x: (1.15**x)*100000000000000000000000000000000000, "tps_boost": 0},
]



630000000000000000000000000000000