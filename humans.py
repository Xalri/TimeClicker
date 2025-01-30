class Human:
    def __init__(self):
        self.stats = {
            "strength": {"cost": 200, "count": 0},
            "agility": {"cost": 200, "count": 0},
            "intelligence": {"cost": 200, "count": 0}
        }

    def buy_stat(self, stat):
        """Achat d'un paramètre humain (strength, agility, intelligence)"""
        if stat in self.stats:
            stat_data = self.stats[stat]
            if self.can_afford(stat):
                self.stats[stat]["count"] += 1
                self.stats[stat]["cost"] = 200 * (2 ** self.stats[stat]["count"])  # Mise à jour du coût
                self.apply_effect(stat)
            else:
                print(f"Pas assez de ressources pour acheter {stat}.")

    def can_afford(self, stat):
        if self.stats[stat]["cost"]<= TimeUnits: # Vérifie que le paramètre peut être acheté
            return True

    def apply_effect(self, stat):
        """Applique l'effet correspondant au paramètre acheté"""
        if stat == "strength":
            click_value *= 1.5
        elif stat == "agility":
            tps *= 1.5
        elif stat == "intelligence":
            boost *= 1.5
