import json

from ..features import Analizer
from ..features import Evaluator

from typing import Dict

class API:
    def __init__(self, file: str, player: str = "B"):
        self.analizer = Analizer(file, player)
        self.evaluator = Evaluator(self.analizer)

    def all_moves_analysis(self) -> str:
        """
        Perform a shallow analysis of all moves in the game.
        This API should be called at the very start when the client is loading the analysis.

        The JSON fomatted string cointains the following informations:

        .. code-block:: json

            {
                "turnData": {
                    0: {
                        "winrate": float,
                        "scoreLead": float,
                        "bestMove": string,
                        "bestMoveScoreLead": float,
                        "nextPlayer": string,
                        "classification": string
                    },
                    1: {
                        // ... similar structure for turn 1
                    },
                    // ... for all turns in the game
                },
                "scoreLeadList": [
                    float, // Score lead at turn 0
                    float, // Score lead at turn 1
                    // ... for all turns in the game
                ]
            }

        :jsonparam dict turnData: A dictionary where each key is a turn number (as a string, starting from "0")
                                  and its value is another dictionary containing detailed analysis for that turn.
        :jsonparam float turnData.[turn_number].winrate: The probability (0.0 to 1.0) of the selected player winning
                                                         at the start of the current turn.
        :jsonparam float turnData.[turn_number].scoreLead: The expected score difference for the selected player
                                                           at the start of the current turn.
        :jsonparam str turnData.[turn_number].bestMove: The optimal move suggested by the engine for the current
                                                        board position, in GTP format (e.g., "C3", "Q4", "pass").
        :jsonparam float turnData.[turn_number].bestMoveScoreLead: The expected score difference for the selected
                                                                   player if the `bestMove` is played.
        :jsonparam str turnData.[turn_number].nextPlayer: The color ('B' for Black or 'W' for White) of the player
                                                          whose turn it is to make a move.
        :jsonparam str turnData.[turn_number].classification: A qualitative assessment of the actual move played
                                                              by the player in this turn (e.g., 'BEST', 'EXCELLENT',
                                                              'GOOD', 'INACCURACY', 'MISTAKE', 'BLUNDER').
        :jsonparam list[float] scoreLeadList: An ordered list of score leads for the selected player at each turn
                                              of the game, suitable for plotting score lead over the game.

        :return: JSON formatted analysis data.
        :rtype: str
        """

        res = {"turnData": Dict()}

        # Perform game analysis
        self.analizer.shalow_game_analysis()
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

        # Format to JSON and return
        json_output = json.dumps(res, indent=4)
        return json_output
