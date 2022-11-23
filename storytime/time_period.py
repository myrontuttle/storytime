from typing import Optional

import random


class TimePeriod:
    """The time period a scene takes place in."""

    # Time periods
    eras = [
        "Prehistoric",  # Before written history
        "Ancient",  # 3000 BC - 500 AD
        "Medieval",  # From the 5th to the 15th century
        "Renaissance",  # 16th-17th centuries
        "Colonial",  # 1800s
        "Modern",  # 1900s
        "Contemporary",  # 2000s
        "Future",  # 2100s and beyond
    ]

    # Seasons
    seasons = [
        "Spring",
        "Summer",
        "Autumn",
        "Winter",
    ]

    # Times of day
    times_of_day = [
        "midnight",
        "pre-dawn",
        "dawn",
        "morning",
        "midday",
        "afternoon",
        "evening",
        "dusk",
        "night",
    ]

    def __init__(
        self,
        era: Optional[str] = None,
        season: Optional[str] = None,
        time_of_day: Optional[str] = None,
    ):
        if era:
            self.era = era
        else:
            self.era = random.choice(self.eras)
        if season:
            self.season = season
        else:
            self.season = random.choice(self.seasons)
        if time_of_day:
            self.time_of_day = time_of_day
        else:
            self.time_of_day = random.choice(self.times_of_day)

    def __str__(self) -> str:
        return f"{self.era} {self.season} {self.time_of_day}"

    @classmethod
    def advance_time_of_day(cls, time_period: "TimePeriod") -> "TimePeriod":
        """Advance the time of day to next."""
        current_time_of_day_index = cls.times_of_day.index(
            time_period.time_of_day
        )
        if current_time_of_day_index == len(cls.times_of_day) - 1:
            next_time_of_day_index = 0
        else:
            next_time_of_day_index = current_time_of_day_index + 1
        next_time_of_day = cls.times_of_day[next_time_of_day_index]
        return cls(time_period.era, time_period.season, next_time_of_day)

    @classmethod
    def advance_season(cls, time_period: "TimePeriod") -> "TimePeriod":
        """Advance the season to next."""
        current_season_index = cls.seasons.index(time_period.season)
        if current_season_index == len(cls.seasons) - 1:
            next_season_index = 0
        else:
            next_season_index = current_season_index + 1
        next_season = cls.seasons[next_season_index]
        return cls(time_period.era, next_season, time_period.time_of_day)

    @classmethod
    def advance_era(cls, time_period: "TimePeriod") -> "TimePeriod":
        """Advance the era to next."""
        current_era_index = cls.eras.index(time_period.era)
        if current_era_index == len(cls.eras) - 1:
            # TODO: Consider staying in the future
            next_era_index = 0
        else:
            next_era_index = current_era_index + 1
        next_era = cls.eras[next_era_index]
        return cls(next_era, time_period.season, time_period.time_of_day)
