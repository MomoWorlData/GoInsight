import json
import platform
import subprocess
from typing import List, Tuple

from ..data import Game, SgfTree, Board, Move
from ..data.constants import VALID_COLUMN_GTP, VALID_COLUMN_SGF
from ..features import Analizer
from ..features import Evaluator

class API1:

    def __init__(self, file: str, player: str = "B"):
        self.analizer = Analizer(file, player)
        self.evaluator = Evaluator(self.analizer)
        self.tree = self.analizer.tree

        self.sequence = self.analizer.tree.move_sequence(insert_tuple=True)



    def all_moves_analysis(self) -> json :
        """
        Perform a shallow analysis of all moves in the game.

        :return: List of analysis for each move.
        :rtype: List[dict]
        """

        res = {}

        evaluation_across_game = self.evaluator.classify_game()

        for i in range(len(self.sequence)):
            winrate, score_lead, best_move, score_lead_best_move, next_player = self.analizer.turn_basic_data(i)

            copy_analizer = self.analizer

            current_sequence = self.sequence[:i+1]
            game = Game.from_sgftree(self.tree)

            possible_sequence = current_sequence.append((next_player, best_move))
            game.moves = possible_sequence

            possible_tree = SgfTree.from_game(game)
            copy_analizer.tree = possible_tree

            possible_winrate, possible_score_lead, _, _, _ = copy_analizer.turn_basic_data(i+1)

            score_across_game = self.analizer.game_score_lead()


            res[f"turn_{i}"] = {
                "winrate": winrate,
                "score_lead": score_lead,
                "best_move": best_move,
                "score_lead_best_move": score_lead_best_move,
                "next_player": next_player,
                "possible_winrate": possible_winrate,
                "possible_score_lead": possible_score_lead,
                "evaluation": evaluation_across_game[i],
            }

        res["score_across_game"] = score_across_game
        res["evaluation_across_game"] = evaluation_across_game

        return res


