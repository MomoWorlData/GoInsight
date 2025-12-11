import json

from ..features import Analizer
from ..features import Evaluator

from typing import Dict, List, Optional, Tuple

class API:
    def __init__(self, file: str, player: str = "B"):
        self.analizer = Analizer(file, player)
        self.evaluator = Evaluator(self.analizer)

    def all_moves_analysis(self) -> str:
        """
        Perform a shallow analysis of all moves in the game.
        This API should be called at the very start when the client is loading the analysis.

        The JSON formatted string contains the following information:

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
    
    def deep_turn_area_analysis(
        self,
        turn: int,
        corner1: Optional[Tuple[int, int]] = None,
        corner2: Optional[Tuple[int, int]] = None,
        invert_selection: bool = False,
    ) -> str:
        """
        Run a deep KataGo analysis on a specific turn with an optional area filter.
        This API should be called during the analysis, when the player ask for an in
        depth analysis of a turn with a possible area filter.

        This API requires an int for the turn to analyze but also accepts two board
        coordinates defining an area and a boolean to decide whether KataGo should
        focus on that area or avoid it.

        :param turn: 0-indexed turn number to analyze.
        :type turn: int
        :param corner1: First corner of the selection area (e.g., (0, 0) for top-left).
        :type corner1: Optional[Tuple[int, int]]
        :param corner2: Second corner of the selection area (e.g., (18, 18) for bottom-right).
        :type corner2: Optional[Tuple[int, int]]
        :param invert_selection: When True, KataGo will avoid the selected area
                                 instead of focusing on it.
        :type invert_selection: bool
        :returns: A JSON formatted string containing a list of the best moves found in order.
        :rtype: str

        The JSON output is an array of move objects, structured as follows:

        .. code-block:: json

            [
                {
                    "move": "D4",
                    "scoreLead": 0.472021208,
                    "possibleVariation": ["D4", "C4", "E4", "F3", "F2"]
                },
                {
                    "move": "Q16",
                    "scoreLead": 0.319342157,
                    "possibleVariation": ["Q16", "R16", "P16", "R17", "P17"]
                }
            ]

        Each object in the array represents a suggested move and contains:

        - **move** (*str*): The suggested move in GTP format (e.g., "C3", "pass").
        - **scoreLead** (*float*): The expected score lead for the current player if this move is played.
        - **possibleVariation** (*list[str]*): A short sequence of moves representing the
          most likely continuation (principal variation) after the suggested move.
        """

        # If an area is selected, get the list of moves contained in it
        selection: Optional[List[str]] = None
        if corner1 is not None and corner2 is not None:
            # Creation of a Game object to have a modelisation of the board
            game = self.analizer.tree.to_game()
            selection = game.board.area_selection_positions(corner1, corner2)

        # Deep analysis of the turn with the selected move filter
        self.analizer.deep_turn_analysis(
            turn=turn,
            selection=selection,
            invert_selection=invert_selection,
        )

        # Prepare JSON output
        data = self.analizer.turn_advanced_data(turn)

        # Format to JSON and return
        json_output = json.dumps(data, indent=4)
        return json_output
