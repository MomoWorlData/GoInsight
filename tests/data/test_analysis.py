from typing import Optional, Tuple, TYPE_CHECKING, List
VALID_COLUMN_GTP = "ABCDEFGHJKLMNOPQRSTUVWXYZ"
import pytest
from src.features import analysis

def test_analizer_initialization():
    """
    Test the initialization of the Analizer class.
    """
    analizer = analysis.Analizer("games/sapindenoel.sgf", player="B")
    assert analizer.player == "B"
    assert analizer.tree is not None
    assert analizer.game_analysis is None
    assert analizer.turn_analysis == {}

def test_deep_turn_analysis():
    """
    Test the deep_game_analysis method of the Analizer class.
    """
    analizer = analysis.Analizer("games/sapindenoel.sgf", player="B")
    analizer.deep_turn_analysis(turn =3, selection=['A1','A2','B1','B2'], invert_selection=False)
    print(analizer.turn_analysis[3])
    assert 1==2  # Placeholder assertion to indicate incomplete test