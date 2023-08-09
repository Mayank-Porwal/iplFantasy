class PlayerCategories:
    WK: str = 'wk'
    BWL: str = 'bowler'
    AR: str = 'ar'
    BAT: str = 'batsman'

    @classmethod
    def get_all_categories(cls) -> list[str]:
        return [value for name, value in vars(cls).items() if name.isupper()]
