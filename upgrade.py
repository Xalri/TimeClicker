from math import e
import buildings

class Upgrades:
    def __init__(self):
        self.buildings = buildings
        self.upgrades = [
        {"name": "upgrade1", "cost": 100, "effect_type": "cps", "effect_value": 1},
        {"name": "upgrade2", "cost": 1000, "effect_type": "click", "effect_value": 10},
        
        
        ### UPGRADES BUILDINGS
        # Préhistoire
        {"name": "Flint", "cost": 10000, "effect_type": "building", "effect_value": 10, "building": "campfire", "epoch": 0},
        {"name": "Hoe", "cost": 10000, "effect_type": "building", "effect_value": 10, "building": "farming", "epoch": 0},
        {"name": "Brush", "cost": 10000, "effect_type": "building", "effect_value": 10, "building": "painting", "epoch": 0},
        {"name": "Weapons", "cost": 10000, "effect_type": "building", "effect_value": 10, "building": "hunting", "epoch": 0},

        # Antiquité
        {"name": "Stone", "cost": 10000, "effect_type": "building", "effect_value": 10, "building": "acqueduct", "epoch": 1},
        {"name": "Maths", "cost": 10000, "effect_type": "building", "effect_value": 10, "building": "pyramid", "epoch": 1},
        {"name": "Artefact", "cost": 10000, "effect_type": "building", "effect_value": 10, "building": "temple", "epoch": 1},
        {"name": "Gold", "cost": 10000, "effect_type": "building", "effect_value": 10, "building": "cash", "epoch": 1},
        
        # Moyen Âge
        {"name": "Paper", "cost": 10000, "effect_type": "building", "effect_value": 10, "building": "printing", "epoch": 2},
        {"name": "Students", "cost": 10000, "effect_type": "building", "effect_value": 10, "building": "school", "epoch": 2},
        {"name": "Monk", "cost": 10000, "effect_type": "building", "effect_value": 10, "building": "church", "epoch": 2},
        {"name": "Soldier", "cost": 10000, "effect_type": "building", "effect_value": 10, "building": "castle", "epoch": 2},
        
        # Temps Modernes
        {"name": "Engineers", "cost": 10000, "effect_type": "building", "effect_value": 10, "building": "steam engine", "epoch": 3},
        {"name": "Locomotive", "cost": 10000, "effect_type": "building", "effect_value": 10, "building": "rail", "epoch": 3},
        {"name": "Coal", "cost": 10000, "effect_type": "building", "effect_value": 10, "building": "factory", "epoch": 3},
        {"name": "Drivers", "cost": 10000, "effect_type": "building", "effect_value": 10, "building": "car", "epoch": 3},
        
        # Époque Contemporaine
        {"name": "Printed Circuit", "cost": 10000, "effect_type": "building", "effect_value": 10, "building": "electronic", "epoch": 4},
        {"name": "Servers", "cost": 10000, "effect_type": "building", "effect_value": 10, "building": "internet", "epoch": 4},
        {"name": "Fuel", "cost": 10000, "effect_type": "building", "effect_value": 10, "building": "rocket", "epoch": 4},
        {"name": "Uranium", "cost": 10000, "effect_type": "building", "effect_value": 10, "building": "nuclear central", "epoch": 4},
    
        # Futur
        {"name": "Devlopment", "cost": 10000, "effect_type": "building", "effect_value": 10, "building": "ai", "epoch": 5},
        {"name": "Black Hole", "cost": 10000, "effect_type": "building", "effect_value": 10, "building": "antimatter central", "epoch": 5},
        {"name": "Reactor", "cost": 10000, "effect_type": "building", "effect_value": 10, "building": "spaceship", "epoch": 5},
        ] #à faire: cost =cout du dixieme batiment, purchased, effect_value ?



        # Coefficients de coût selon l'époque
        self.epochCostMultipliers = [0.25, 0.5, 1, 1.5, 2, 3]

        # Seuils d'achat des upgrades
        self.upgradeThresholds = [10, 25, 50, 100, 200, 500]

        # Ajout du coût et de l'effet de chaque upgrade
        for upgrade in self.upgrades:
            buildingsName = upgrade["building"]
            if buildingsName in self.buildings:
                baseCost = self.buildings[buildingsName]["cost"]
                epochMultiplier = self.epochCostMultipliers[upgrade["epoch"]]
                upgrade["cost"] = baseCost * epochMultiplier
                upgrade["effect"] = 4  # Multiplie la production par 4
                upgrade["purchased"] = 0  # Compteur des achats de l'upgrade

    def buy_upgrade(self, upgradeName, timeUnits):
        """
        Permet d'acheter une upgrade.
        """
        for upgrade in self.upgrades:
            if upgrade["name"] == upgradeName:
                buildingsName = upgrade["building"]

                # Vérification que le bâtiment associé existe
                if buildingsName not in self.buildings:
                    return False

                building = self.buildings[buildingName]
                ownedCount = building["count"]

                # Vérification des conditions d'achat
                if upgrade["purchased"] >= len(self.upgradeThresholds):
                    return False  # Toutes les upgrades ont déjà été achetées

                requiredBuildingCount = self.upgradeThresholds[upgrade["purchased"]]
                if ownedCount < requiredBuildingCount:
                    return False  # Pas assez de bâtiments pour débloquer l'upgrade

                if time_units < upgrade["cost"]:
                    return False  # Pas assez de ressources

                # Achat réussi
                time_units -= upgrade["cost"]
                building["tps_boost"] *= upgrade["effect"]  # Application de l'effet
                upgrade["purchased"] += 1  # Augmenter le compteur d'upgrades achetées

                return True  # Achat réussi
        return False  # Upgrade non trouvée

    def can_afford(self, upgradeName, timeUnits):
        """
        Vérifie si une upgrade est achetable.
        """
        for upgrade in self.upgrades:
            if upgrade["name"] == upgradeName:
                return timeUnits >= upgrade["cost"]
        return False
