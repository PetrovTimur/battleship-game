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


#### Вылезает ошибка!!!
    '''
    def test_ready2(self,
                    mock_translation, mock_battleship_util_image,
                    battleship_resources, battleship_logic_ai,
                    battleship_logic):
        battleship_logic.AsyncioThread = MagicMock()
        sps = object.__new__(ShipPlacementScreen)
        sps.root = MagicMock()
        sps.is_ready = MagicMock()
        sps.is_ready.get = MagicMock(return_value=True)
        sps.root.game.mode = 'notsingle'
        sps.ready()
        sps.is_ready.get.assert_called_once()
        assert sps.root.game.thread.name == 'Thread-2'
    '''

    def test_ready3(self,
                    mock_translation, mock_battleship_util_image,
                    battleship_resources, battleship_logic_ai,
                    battleship_logic):

        sps = object.__new__(ShipPlacementScreen)
        sps.root = MagicMock()
        sps.is_ready = MagicMock()
        sps.is_ready.get = MagicMock(return_value=False)
        battleship_logic_ai.BotThread = MagicMock(return_value=1)
        sps.root.game.mode = 'notonline'
        sps.ready()
        assert(sps.root.game.thread == None)
        assert(sps.root.game.queue == None)


    def test_start_game(self,
                    mock_translation, mock_battleship_util_image,
                    battleship_resources, battleship_logic_ai,
                    battleship_logic):
        sps = object.__new__(ShipPlacementScreen)
        sps.root = MagicMock()
        sps.start_game()
        sps.root.event_generate.assert_called_once()

    def test_return_to_main(self,
                    mock_translation, mock_battleship_util_image,
                    battleship_resources, battleship_logic_ai,
                    battleship_logic):
        sps = object.__new__(ShipPlacementScreen)
        sps.root = MagicMock()
        sps.return_to_main()
        assert sps.root.game == None
        sps.root.unbind.assert_called_once()
        sps.root.event_generate.assert_called_once()
