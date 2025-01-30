buildings = [
    # Préhistoire
    {"name": "Campfire", "cost": lambda x: (x**1.15)*15, "tps_boost": 0.1},
    {"name": "Farming", "cost": lambda x: (x**1.15)*100, "tps_boost": 1},
    {"name": "Painting", "cost": lambda x: (x**1.15)*1100, "tps_boost": 8},
    {"name": "Hunting", "cost": lambda x: (x**1.15)*12000, "tps_boost": 47},
    
    # Antiquité
    {"name": "Aqueduct", "cost": lambda x: (x**1.15)*130000, "tps_boost": 260},
    {"name": "Pyramid", "cost": lambda x: (x**1.15)*1400000, "tps_boost": 1400},
    {"name": "Temple", "cost": lambda x: (x**1.15)*20000000, "tps_boost": 7800},
    {"name": "Cash", "cost": lambda x: (x**1.15)*330000000, "tps_boost": 44000},
    
    # Moyen Âge
    {"name": "Printing", "cost": lambda x: (x**1.15)*5100000000, "tps_boost": 260000},
    {"name": "School", "cost": lambda x: (x**1.15)*75000000000, "tps_boost": 1600000},
    {"name": "Church", "cost": lambda x: (x**1.15)*1000000000000, "tps_boost": 10000000},
    {"name": "Castle", "cost": lambda x: (x**1.15)*14000000000000, "tps_boost": 65000000},
    
    # Temps Modernes
    {"name": "Steam Engine", "cost": lambda x: (x**1.15)*170000000000000, "tps_boost": 430000000},
    {"name": "Rail", "cost": lambda x: (x**1.15)*2100000000000000, "tps_boost": 2900000000},
    {"name": "Factory", "cost": lambda x: (x**1.15)*26000000000000000, "tps_boost": 21000000000},
    {"name": "Car", "cost": lambda x: (x**1.15)*310000000000000000, "tps_boost": 150000000000},
    
    # Époque Contemporaine
    {"name": "Electronic", "cost": lambda x: (x**1.15)*7100000000000000000, "tps_boost": 1100000000000},
    {"name": "Internet", "cost": lambda x: (x**1.15)*12000000000000000000000, "tps_boost": 8300000000000},
    {"name": "Rocket", "cost": lambda x: (x**1.15)*1900000000000000000000000, "tps_boost": 64000000000000},
    {"name": "Nuclear Central", "cost": lambda x: (x**1.15)*540000000000000000000000000, "tps_boost": 510000000000000},
    
    # Futur
    {"name": "AI", "cost": lambda x: (x**1.15)*30000000000000000000000000000, "tps_boost": 4000000000000000},
    {"name": "Antimatter Central", "cost": lambda x: (x**1.15)*4200000000000000000000000000000, "tps_boost": 31000000000000000},
    {"name": "Spaceship", "cost": lambda x: (x**1.15)*630000000000000000000000000000000, "tps_boost": 240000000000000000}
    #{"name": "Time Machine", "cost": 100000000000000000000000000000000000, "tps_boost": },
]