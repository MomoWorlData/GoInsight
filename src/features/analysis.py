import json
import platform
import subprocess
from typing import List, Tuple

from ..data import Game, SgfTree
from .constants import GAME_ANALYSIS_CONFIG_PATH, MODEL_DIR, NEURALNET_PATH, TURN_ANALYSIS_CONFIG_PATH

class Analizer:
    """
    Used to analyze different aspects of a game.

    :param file: Path to the SGF file of the game.
    :type file: str
    :param player: Protagonist of the analysis ('B' or 'W').
    :type player: str

    :ivar tree: SGF tree of the game.
    :vartype tree: SgfTree
    :ivar player: Protagonist of the analysis ('B' or 'W').
    :vartype player: str
    :ivar game_analysis: Shallow analysis of the full game.
    :vartype game_analysis: Any
    :ivar turn_analysis: Deep analysis of specific turn (dict key represents the turn).
    :vartype turn_analysis: dict[int, Any]

    :raises ValueError: If player is not 'B' or 'W'.
    """
    def __init__(self, file: str, player: str = "B"):
        self.tree = SgfTree.from_sgf(file)

        if player != "B" and player != "W":
            raise ValueError(f"Analizer(file, player) -- The value of player must be 'B' or 'W' not: {player}")
        self.player = player

        self.game_analysis = None
        self.turn_analysis = dict()

    def shalow_game_analysis(self):
        """
        This function performs an analysis of a Go game using KataGo.
        """
        # Katago selection depending on OS
        if platform.system() == "Darwin":
            model = "katago"
        elif platform.system() == "Linux":
            model = "/".join([MODEL_DIR, "katago"])
        else:
            model = "/".join([MODEL_DIR, "katago.exe"])

        # Obtaining data from SGF tree
        game = Game.from_sgftree(self.tree)
        moves_list = self.tree.move_sequence(insert_tuple=True)
        rules = game.ruleset
        komi = game.komi
        x, y = game.size
        initial_stones = [("B", sgf_pos) for sgf_pos in (game.AB or [])] + \
                         [("W", sgf_pos) for sgf_pos in (game.AW or [])]
        
        # Building input json
        json_input = {
            "id": "game_analysis",
            "moves": moves_list,
            "rules": rules,
            "komi": komi,
            "boardXSize": x,
            "boardYSize": y,
            "initialStones": initial_stones,
            "analyzeTurns": [turn for turn in range(0, len(moves_list))],
        }

        # Command declaration
        command = [
        model,
        "analysis",
        "-model", NEURALNET_PATH,
        "-config", GAME_ANALYSIS_CONFIG_PATH
        ]

        # Running the command
        process = subprocess.run(
            command,
            input=json.dumps(json_input) + "\n",
            capture_output=True,
            text=True,
            check=True,
        )

        # Capturing output
        output_lines = [line for line in process.stdout.splitlines() if line.strip()]
        output_data = [json.loads(line) for line in output_lines]

        # Sort by turn
        sorted_output_data = sorted(output_data, key=lambda x: x["turnNumber"])

        self.game_analysis = sorted_output_data

    def deep_turn_analysis(
            self,
            turn: int,
            selection: List[str] = None,
            invert_selection: bool = False
        ):
        """
        This function performs an analysis of a Go move in depth using KataGo.

        :param turn: Turn of the game to analyze (starts at 0).
        :type turn: int
        :param selection: List of positions in GTP format that KataGo must use (e.g.: ["C3", "Q4", "pass"]).
        :type selection: list[str], optional
        :param invert_selection: If true, the selection can't be used by KataGo. Defaults to False.
        :type invert_selection: bool
        """
        # Katago selection depending on OS
        if platform.system() == "Darwin":
            model = "katago"
        elif platform.system() == "Linux":
            model = "/".join([MODEL_DIR, "katago"])
        else:
            model = "/".join([MODEL_DIR, "katago.exe"])

        # Obtaining data from SGF tree
        game = Game.from_sgftree(self.tree)
        moves_list = self.tree.move_sequence(insert_tuple=True)
        rules = game.ruleset
        komi = game.komi
        x, y = game.size
        initial_stones = [("B", sgf_pos) for sgf_pos in (game.AB or [])] + \
                         [("W", sgf_pos) for sgf_pos in (game.AW or [])]
        
        # Building input json
        json_input = {
            "id": "game_analysis",
            "moves": moves_list,
            "rules": rules,
            "komi": komi,
            "boardXSize": x,
            "boardYSize": y,
            "initialStones": initial_stones,
            "analyzeTurns": [turn],
        }

        if selection:
            selected_moves = [{"player": moves_list[turn][0], "moves": selection, "untilDepth": turn + 10}]
            if invert_selection:
                json_input["avoidMoves"] = selected_moves
            else:
                json_input["allowMoves"] = selected_moves

        # Command declaration
        command = [
        model,
        "analysis",
        "-model", NEURALNET_PATH,
        "-config", TURN_ANALYSIS_CONFIG_PATH
        ]

        # Running the command
        process = subprocess.run(
            command,
            input=json.dumps(json_input) + "\n",
            capture_output=True,
            text=True,
            check=True,
        )

        # Capturing output
        output_lines = [line for line in process.stdout.splitlines() if line.strip()]
        output_data = [json.loads(line) for line in output_lines]

        self.turn_analysis[turn] = output_data

    def game_score_lead(self) -> List[float]:
        """
        This function returns the score lead of black over the course of the game.

        :returns: List of the score lead at every turn.
        :rtype: list[float]

        :raises ValueError: If the game analysis is not done yet.
        """
        if self.game_analysis is None:
            raise ValueError(f"Analizer.game_score_lead() -- Run the game analysis before this: Analizer.game_analysis = None")

        # Extract the score lead
        return [data["rootInfo"]["scoreLead"] for data in self.game_analysis]
    
    def turn_basic_data(self, turn: int) -> Tuple[float, float, str, float]:
        """
        This function returns the basic infos to display on the analysis UI.
        All data is from the perspective of the Analyzer's selected player.

        :param turn: Selected turn.
        :type turn: int

        :returns:
            - **Winrate of the position** (`float`): The probability (0.0 to 1.0) of the selected player winning from the current position.
            - **Score lead of the position** (`float`): The expected score difference (in points) for the selected player.
            - **KataGo best move in GTP format** (`str`): The move KataGo considers optimal.
            - **Score lead after KataGo best move** (`float`): The expected score difference for the selected player if the best move is played.
            - **Next turn player** (`str`): The color ('B' or 'W') who is to play next.

        :rtype: tuple[float, float, str, float, str]

        :raises ValueError: If the turn selected is not in the game.
        """
        if turn >= len(self.game_analysis):
            raise ValueError(f"Analizer.turn_basic_data(turn) -- The turn selected is not in the game analysis: turn = {turn}")

        turn_analysis = self.game_analysis[turn]

        winrate = turn_analysis["rootInfo"]["winrate"]
        score_lead = turn_analysis["rootInfo"]["scoreLead"]
        best_move, score_lead_best_move = [(move["move"], move["scoreLead"]) for move in turn_analysis["moveInfos"] if move["order"] == 0][0]
        next_player = "BW"[turn_analysis["rootInfo"]["currentPlayer"] == "B"]

        if self.player == "W":
            winrate = 1 - winrate
            score_lead = -score_lead
            score_lead_best_move = -score_lead_best_move

        return winrate, score_lead, best_move, score_lead_best_move, next_player
    
    def turn_advanced_data(self, turn) -> Tuple[int]:
        """
        Docstring for turn_advanced_data
        
        :param self: Description
        :param turn: Description
        :return: Description
        :rtype: Tuple[()]
        """
        pass


if __name__ == "__main__":
    analizer = Analizer("games/sapindenoel_tronque.sgf")
    analizer.shalow_game_analysis()
    list_score_lead = analizer.game_score_lead()

    print("turn | scoreLead")
    for i, score_lead in enumerate(list_score_lead):
        if i < 10:
            print(f"{i}    | {score_lead}")
        elif i < 100:
            print(f"{i}   | {score_lead}")
        else:
            print(f"{i}  | {score_lead}")

    print(analizer.turn_basic_data(10))
