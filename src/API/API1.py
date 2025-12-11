import json

from ..data import Game, SgfTree
from ..features import Analizer
from ..features import Evaluator

from typing import Dict

class API1:

    def __init__(self, file: str, player: str = "B"):
        self.analizer = Analizer(file, player)
        self.evaluator = Evaluator(self.analizer)



    def all_moves_analysis(self) -> str:
        """
        Perform a shallow analysis of all moves in the game.

        The JSON fomatted string cointains the following informations:

        * `turnData`:
            * `[turn_number]` (starting at 0):
                * `winrate`: winrate at current turn
                * `scoreLead`: scoreLead at current turn
                * `bestMove`: engine best move
                * `bestMoveScoreLead`: scoreLead after playing the best move
                * `nextPlayer`: color of the player for next turn ('B' or 'W')
                * `classification`: player move's classifciation ('BEST', 'EXCELLENT', ...)
        * `scoreLeadList`: ordered list of scoreLead over the game to plot the scoreLead graph

        :return: JSON formatted analysis data.
        :rtype: str
        """

        res = {"turnData": Dict()}

        # Perform game analysis
        self.analizer.game_analysis()
        classification_across_game = self.evaluator.classify_game()

        # Prepare JSON output
        for i in range(len(classification_across_game)):

            data = self.analizer.turn_basic_data(i)
            
            res["turnData"][i] = {
                "winrate":           data[0],
                "scoreLead":         data[1],
                "bestMove":          data[2],
                "bestMoveScoreLead": data[3],
                "nextPlayer":        data[4],
                "classification":    classification_across_game[i],
            }

            res["scoreLeadList"] = self.analizer.game_score_lead()

        json_output = json.dumps(res, indent=4)

        return json_output
