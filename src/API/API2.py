"""API endpoint for deep turn analysis with optional board area selection.

This module exposes an API that triggers KataGo's deep turn analysis for a
specific move, optionally restricting or excluding a rectangular area of the
board.
"""
from typing import Dict, List, Optional, Tuple

from ..data import Board, Game
from ..features import Analizer


class API2:
    """
    Provide access to deep turn analysis with area-based move filtering.

    Args:
        file (str): Path to the SGF file to analyze.
        player (str): Perspective used by the analyzer ('B' or 'W').
    """

    def __init__(self, file: str, player: str = "B"):
        self.analizer = Analizer(file, player)
        self.tree = self.analizer.tree
        self.game = Game.from_sgftree(self.tree)
        self.board = Board(self.game, size=self.game.size, moves=self.game.moves)

    def deep_turn_area_analysis(
        self,
        turn: int,
        corner1: Optional[Tuple[int, int]] = None,
        corner2: Optional[Tuple[int, int]] = None,
        invert_selection: bool = False,
    ) -> Dict[str, object]:
        """
        Run a deep KataGo analysis on a specific turn with an optional area filter.

        The API accepts two board coordinates defining a rectangle and a boolean to
        decide whether KataGo should focus on that rectangle or avoid it.

        Args:
            turn (int): Turn index to analyze.
            corner1 (Tuple[int, int], optional): First corner of the selection area.
            corner2 (Tuple[int, int], optional): Second corner of the selection area.
            invert_selection (bool): When True, KataGo will avoid the selected area
                instead of focusing on it.

        Returns:
            Dict[str, object]: Aggregated analysis data, including the top moves and
            their continuations when available.
        """

        selection: Optional[List[str]] = None
        if corner1 is not None and corner2 is not None:
            selection = self.board.area_selection_positions(corner1, corner2)

        self.analizer.deep_turn_analysis(
            turn=turn,
            selection=selection,
            invert_selection=invert_selection,
        )

        analysis_entries = self.analizer.turn_analysis.get(turn, [])
        if not analysis_entries:
            return {
                "turn": turn,
                "selection": selection,
                "invert_selection": invert_selection,
                "best_moves": [],
            }

        latest_entry = analysis_entries[-1]
        move_infos: List[Dict[str, object]] = latest_entry.get("moveInfos", [])

        if selection:
            if invert_selection:
                filtered_moves = [
                    info for info in move_infos if info.get("move") not in selection
                ]
            else:
                filtered_moves = [
                    info for info in move_infos if info.get("move") in selection
                ]
            if filtered_moves:
                move_infos = filtered_moves

        best_moves = [
            {
                "move": info.get("move"),
                "winrate": info.get("winrate"),
                "scoreLead": info.get("scoreLead"),
                "policy": info.get("policy"),
                "pv": info.get("pv"),
            }
            for info in move_infos
        ]

        return {
            "turn": turn,
            "selection": selection,
            "invert_selection": invert_selection,
            "best_moves": best_moves,
            "raw_analysis": analysis_entries,
        }