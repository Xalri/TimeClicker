import buildings

class Timeline:
    def __init__(self):
        self.timeline = [
            {"name": "Préhistoire", "cost": (buildings[1][1] + buildings[2][1] + buildings[3][1] + buildings[4][1]) * 1.15**10, "unlocked": False}, 
            {"name": "Antiquité", "cost": (buildings[5][1] + buildings[6][1] + buildings[7][1] + buildings[8][1]) * 1.15**20, "unlocked": False},
            {"name": "Moyen Age", "cost": (buildings[9][1] + buildings[10][1] + buildings[11][1] + buildings[12][1]) * 1.15**30, "unlocked": False},
            {"name": "Temps Modernes", "cost": (buildings[13][1] + buildings[14][1] + buildings[15][1] + buildings[16][1]) * 1.15**40, "unlocked": False},
            {"name": "Epoque Contemporaine", "cost": (buildings[17][1] + buildings[18][1] + buildings[19][1] + buildings[20][1]) * 1.15**50, "unlocked": False},
            {"name": "Futur", "cost": (buildings[21][1] + buildings[22][1] + buildings[23][1] + buildings[24][1]) * 1.15**60, "unlocked": False}
        ] # cout : buildinngs dernierment débloqués (ou tout ceux débloqués donc changer)

    def buildings_allowed(self):
        """Débloque les bâtiments selon les périodes achetées."""
        for index, period in self.timeline:
            if period["unlocked"]:
                startIndex = index * 4  # Chaque période débloque 4 bâtiments
                for i in range(startIndex, startIndex + 4):
                    if i < len(buildings):
                        buildings[i]["allowed"] = True

    def buy_timeline(self, tlIndex, timeUnits):
        """Achète une période si possible."""
        if 0 <= tlIndex < len(self.timeline):
            period = self.timeline[tlIndex]
            if self.can_afford(tlIndex, timeUnits):
                time_units -= period["cost"]  # Retire le coût
                period["unlocked"] = True  # Débloque la période
                self.buildings_allowed()  # Met à jour les bâtiments disponibles
        return time_units

    def can_afford(self, tlIndex, timeUnits):
        """Vérifie si on a assez de ressources pour acheter la période."""
        return timeUnits >= self.timeline[tlIndex]["cost"]