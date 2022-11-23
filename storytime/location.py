from typing import Optional

import random

LOCATION_GEN_URL = "http://storygen.weebly.com/location.html"


class Location:
    """Where a scene takes place."""

    # Jungle Locales
    jungle_locales = [
        "village",
        "river",
        "riverbank",
        "canopy",
        "undergrowth",
        "clearing",
        "cave",
        "temple",
        "bridge",
        "hut",
    ]

    # Mountain Locales
    mountains_locales = [
        "mountain",
        "pass",
        "village",
        "hut",
        "peak",
        "lake",
        "riverbank",
        "stream",
        "waterfall",
        "cave",
        "canyon",
        "cliff",
        "valley",
        "glacier",
        "plateau",
        "ridge",
        "summit",
    ]

    # Desert Locales
    desert_locales = [
        "oasis",
        "village",
        "camp",
        "dune",
        "cave",
        "canyon",
        "cliff",
        "arch",
        "cactus field",
    ]

    # Forest Locales
    forest_locales = [
        "woods",
        "stream",
        "riverbank",
        "lake",
        "lagoon",
        "swamp",
        "marsh",
        "meadow",
        "canopy",
        "thicket",
        "clearing",
        "gully",
        "grove",
        "hollow",
        "hut",
        "village",
    ]

    # Arctic Locales
    arctic_locales = [
        "village",
        "camp",
        "iceberg",
        "ice shelf",
        "ice cap",
        "glacier",
        "ice cave",
        "ice tunnel",
        "tundra",
        "snowdrift",
        "snowfield",
        "snowbank",
        "snowy mountain",
    ]

    # Ocean Locales
    ocean_locales = [
        "island",
        "beach",
        "open ocean",
        "reef",
        "inlet",
        "bay",
        "cove",
        "cape",
        "fjord",
        "gulf",
        "coast",
        "channel",
    ]

    colonial_ocean_locales = [
        "ship",
        "shipwreck",
        "pirate ship",
        "port",
        "dock",
        "harbor",
        "pier",
        "wharf",
        "quay",
        "barge",
        "brig",
        "frigate",
        "cabin",
        "deck",
        "cargo hold",
    ]

    modern_ocean_locales = [
        "underwater",
        "oceanside hotel",
        "ocean floor",
        "submarine",
        "aircraft carrier",
        "sailboat",
        "yacht",
        "cruise ship",
        "fishing boat",
        "oil rig",
        "oil tanker",
        "tugboat",
        "lounge",
        "dining room",
        "ballroom",
        "casino",
        "bridge",
        "engine room",
        "kitchen",
        "bathroom",
        "stateroom",
        "corridor",
        "stairwell",
    ]

    # Underground Locales
    underground_locales = [
        "cave",
        "tunnel",
        "river",
        "lake",
        "vault",
        "tomb",
        "cavern",
    ]

    medieval_locales = [
        "castle",
        "keep",
        "tower",
        "palace",
        "village",
        "quarry",
        "field",
    ]

    modern_remote_locales = [
        "airstrip",
        "road",
        "facility",
        "bunker",
        "cabin",
        "camp",
        "mine",
        "tunnel",
        "reservation",
        "ghost town",
        "oil field",
        "ruins",
    ]

    # Rural Locales
    rural_locales = [
        "farm",
        "barn",
        "stable",
        "military camp",
        "abandoned military camp",
        "abandoned farm",
        "abandoned house",
        "park",
        "forest",
        "field",
        "pasture",
        "butte",
        "pond",
        "lake",
        "grove",
        "garden",
        "backyard",
        "front yard",
        "porch",
        "patio",
        "deck",
        "school",
        "market",
        "town square",
        "town hall",
        "lodge",
        "ranch",
        "quarry",
        "greenhouse",
        "observatory",
    ]

    # Suburban Locales
    suburban_locales = [
        "house",
        "mansion",
        "apartment",
        "bedroom",
        "kitchen",
        "bathroom",
        "living room",
        "dining room",
        "car wash",
        "car repair shop",
        "rest stop",
        "highway",
        "pet store",
        "motel",
        "mall",
        "shopping center",
        "church",
        "school",
        "university",
        "library",
        "museum",
        "theater",
        "cinema",
        "restroom",
        "outdoor swimming pool",
        "parking lot",
        "parking garage",
        "park",
        "playground",
        "garden",
        "backyard",
        "front yard",
        "retail store",
        "grocery store",
        "pharmacy",
        "main street",
        "ice skating rink",
        "toy store",
        "book store",
        "high school",
        "middle school",
        "elementary school",
        "courthouse",
        "construction site",
        "bank",
        "art studio",
        "gym",
        "pool",
        "theatre",
        "office",
        "conference room",
        "break room",
        "treehouse",
    ]

    # Urban Locales
    urban_locales = [
        "bar",
        "restaurant",
        "cafe",
        "office",
        "building",
        "apartment",
        "penthouse",
        "hotel",
        "factory",
        "warehouse",
        "pier",
        "store",
        "abandoned factory",
        "fast food place",
        "laundromat",
        "daycare center",
        "church",
        "mosque",
        "laboratory",
        "hospital",
        "school",
        "university",
        "library",
        "museum",
        "theater",
        "cinema",
        "concert hall",
        "restroom",
        "bedroom",
        "kitchen",
        "bathroom",
        "living room",
        "dining room",
        "shop",
        "parking lot",
        "parking garage",
        "pharmacy",
        "high-rise",
        "company headquarters",
        "courthouse",
        "construction site",
        "bank",
        "casino",
        "foreign embassy",
        "government building",
        "art studio",
        "art gallery",
        "stadium",
        "arena",
        "gym",
        "pool",
        "diner",
        "movie set",
        "power plant",
        "train yard",
        "conference room",
        "break room",
    ]

    # Sky Locales
    sky_locales = [
        "balloon",
        "blimp",
        "airship",
        "airplane",
        "helicopter",
        "cabin",
        "hangar",
        "airport",
        "airfield",
        "airbase",
    ]

    # Space Locales
    space_locales = [
        "station",
        "docking bay",
        "spacecraft",
        "bar",
        "cabin",
        "office",
        "bridge",
        "cargo hold",
        "laboratory",
        "ship",
        "colony",
        "base",
        "port",
        "moon",
        "alien planet",
        "underground",
        "asteroid",
    ]

    # Locale Dictionaries
    primitive_areas = {
        "mountainous": mountains_locales,
        "ocean": ocean_locales,
        "desert": desert_locales,
        "forest": forest_locales,
        "jungle": jungle_locales,
        "arctic": arctic_locales,
    }

    medieval_areas = {
        "underground": underground_locales,
        "medieval": medieval_locales,
    }

    colonial_areas = {
        "colonial ocean": colonial_ocean_locales,
        "rural": rural_locales,
    }

    modern_areas = {
        "modern ocean": modern_ocean_locales,
        "modern remote": modern_remote_locales,
        "urban": urban_locales,
        "suburban": suburban_locales,
        "sky": sky_locales,
    }

    advanced_areas = {
        "space": space_locales,
    }

    def __init__(
        self,
        era: Optional[str] = None,
        area: Optional[str] = None,
        locale: Optional[str] = None,
    ):
        """Initialize the Area and Locale."""
        self.era = era
        available_areas = self.avail_areas()
        if area:
            self.area = area
        else:
            self.area = random.choice(list(available_areas.keys()))
        if locale:
            self.locale = locale
        else:
            self.locale = random.choice(available_areas[self.area])

    def __str__(self) -> str:
        return f"{self.area}:{self.locale}"

    def avail_areas(self):
        """Return a list of available areas for the given era."""
        if self.era == "Prehistoric" or self.era == "Ancient":
            available_areas = self.primitive_areas
        elif self.era == "Medieval":
            available_areas = {**self.primitive_areas, **self.medieval_areas}
        elif self.era == "Renaissance" or self.era == "Colonial":
            available_areas = {
                **self.primitive_areas,
                **self.medieval_areas,
                **self.colonial_areas,
            }
        elif self.era == "Future":
            available_areas = {**self.modern_areas, **self.advanced_areas}
        else:  # Modern or Contemporary or None
            available_areas = {
                **self.primitive_areas,
                **self.medieval_areas,
                **self.colonial_areas,
                **self.modern_areas,
            }
        return available_areas

    @classmethod
    def new_locale(cls, location: "Location") -> "Location":
        """Select a different locale in the area."""
        available_areas = cls.avail_areas(location)
        possible_locales = [
            v for v in available_areas[location.area] if v != location.locale
        ]
        return cls(
            era=location.era,
            area=location.area,
            locale=random.choice(possible_locales),
        )

    @classmethod
    def new_area(cls, location: "Location") -> "Location":
        """Select a different area in the era."""
        available_areas = cls.avail_areas(location)
        possible_areas = [
            k for k in available_areas.keys() if k != location.area
        ]
        new_a = random.choice(possible_areas)
        return cls(
            era=location.era,
            area=new_a,
            locale=random.choice(available_areas[new_a]),
        )


if __name__ == "__main__":
    loc = Location("Modern")
    print(f"Start in {loc}")
    new_loc = Location.new_locale(loc)
    print(f"New locale in {new_loc}")
    new_area = Location.new_area(new_loc)
    print(f"New area in {new_area}")
