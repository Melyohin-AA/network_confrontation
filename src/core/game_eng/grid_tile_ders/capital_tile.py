from game_eng.grid_tile import GridTile


class CapitalGridTile(GridTile):
    @property
    def owners_income(self) -> int:
        return 16

    @property
    def power_growth(self) -> int:
        return 16

    @property
    def power_cap(self) -> int:
        return 256

    @property
    def name(self) -> str:
        return "Контрольный Кластер"

    def conquer(self, team):
        prev_team = self.team
        super().conquer(team)
        team.add_capital_tile(self)
        if prev_team is None:
            return
        prev_team.lose_capital_tile(self)
        if prev_team.defeated:
            self.__conquer_all_tiles_of_team(prev_team)

    def __conquer_all_tiles_of_team(self, team):
        for tile in self.grid.foreach:
            if tile.team == team:
                tile.conquer(self.team)
