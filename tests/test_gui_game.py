from battleship.gui.game import ShipPlacementScreen
import unittest
from unittest.mock import MagicMock, Mock, patch


@patch('battleship.logic')
@patch('battleship.logic.ai')
@patch('battleship.resources')
@patch('battleship.util.image')
@patch('battleship.translation')
class ShipPlacementScreenTestCase(unittest.TestCase):

    def test_connection_error(self,
                              mock_translation, mock_battleship_util_image,
                              battleship_resources, battleship_logic_ai,
                              battleship_logic):
            sps = object.__new__(ShipPlacementScreen)
            sps.root = MagicMock()
            sps.is_ready = MagicMock()
            sps.message = MagicMock()
            #with patch('battleship.translation') as target_mock:
            #    sps.connection_error()
            sps.connection_error()
            sps.is_ready.set.assert_called_with(False)
            sps.message.set.assert_called_once()
            sps.root.game.queue == None
            assert sps.root.game.queue == None
            assert sps.root.game.thread == None
    
    def test_ready1(self,
                    mock_translation, mock_battleship_util_image,
                    battleship_resources, battleship_logic_ai,
                    battleship_logic):
        sps = object.__new__(ShipPlacementScreen)
        sps.root = MagicMock()
        sps.is_ready = MagicMock()
        sps.is_ready.get = MagicMock(return_value=True)
        sps.root.game.mode = 'single'
        sps.ready()
        sps.is_ready.get.assert_called_once()
        assert sps.root.game.thread.name == 'Thread-1 (play)'
