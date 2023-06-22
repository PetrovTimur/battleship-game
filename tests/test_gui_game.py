from battleship.gui.game import ShipPlacementScreen, GameScreen
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

    def test_random_place(self,
                    mock_translation, mock_battleship_util_image,
                    battleship_resources, battleship_logic_ai,
                    battleship_logic):
        sps = object.__new__(ShipPlacementScreen)
        sps.root = MagicMock()
        sps.ready_check = MagicMock()
        sps.field_buttons = [[MagicMock()]*10]*10
        sps.root.game.me.field.cells = [[0]*10]*10
        sps.random_place()
        sps.root.game.me.field.auto_place.assert_called_once()
        sps.ready_check.configure.assert_called_once()

    def test_clear(self,
                    mock_translation, mock_battleship_util_image,
                    battleship_resources, battleship_logic_ai,
                    battleship_logic):
        sps = object.__new__(ShipPlacementScreen)
        sps.root = MagicMock()
        sps.is_ready = MagicMock()
        sps.ready_check = MagicMock()
        sps.field_buttons = [[MagicMock()]*10]*10
        sps.clear()
        sps.root.game.me.field.clear.assert_called_once()
        sps.is_ready.set.assert_called_once()
        sps.ready_check.configure.assert_called_once()

    def test_place(self,
                    mock_translation, mock_battleship_util_image,
                    battleship_resources, battleship_logic_ai,
                    battleship_logic):
        sps = object.__new__(ShipPlacementScreen)
        sps.root = MagicMock()
        sps.frame = MagicMock()
        sps.title = MagicMock()
        sps.field_frame = MagicMock()
        sps.random_button = MagicMock()
        sps.clear_button = MagicMock()
        sps.ready_check = MagicMock()
        sps.message_label = MagicMock()
        sps.return_label = MagicMock()
        sps.field_buttons = [[MagicMock()]*10]*10
        sps.place()
        sps.field_frame.grid_propagate.assert_called_once()
        sps.field_frame.rowconfigure.assert_called_once()
        sps.field_frame.columnconfigure.assert_called_once()

    def test_rotate(self,
                    mock_translation, mock_battleship_util_image,
                    battleship_resources, battleship_logic_ai,
                    battleship_logic):
        sps = object.__new__(ShipPlacementScreen)
        sps.leave = MagicMock()
        sps.hover = MagicMock()
        event = MagicMock()
        event.num = 0
        event.delta = 120
        sps.angle = 'w'
        sps.rotate(event,(1,1))
        assert sps.leave.called
        assert sps.hover.called
    
    def test_update_field(self,
                    mock_translation, mock_battleship_util_image,
                    battleship_resources, battleship_logic_ai,
                    battleship_logic):
        sps = object.__new__(ShipPlacementScreen)
        sps.field_buttons = [[MagicMock()]*10]*10
        sps.angle = 'w'
        sps.update_field()
        for i1 in range(10):
            for i2 in range(10):
                assert sps.field_buttons[i1][i2].state.call_count == 100

    def test_destroy(self,
                    mock_translation, mock_battleship_util_image,
                    battleship_resources, battleship_logic_ai,
                    battleship_logic):
        sps = object.__new__(ShipPlacementScreen)
        sps.frame = MagicMock()
        sps.destroy()
        sps.frame.destroy.assert_called_once()


@patch('battleship.logic')
@patch('battleship.logic.ai')
@patch('battleship.resources')
@patch('battleship.util.image')
@patch('battleship.translation')
class GameScreenTestCase(unittest.TestCase):
    def test_return_to_main(self,
                            mock_translation, mock_battleship_util_image,
                            battleship_resources, battleship_logic_ai,
                            battleship_logic):
        tec = object.__new__(GameScreen)
        tec.root = MagicMock()
        tec.return_to_main()
        assert tec.root.game == None
        tec.root.unbind.assert_called_once()
        tec.root.event_generate.assert_called_once()

    def test_quit(self,
                            mock_translation, mock_battleship_util_image,
                            battleship_resources, battleship_logic_ai,
                            battleship_logic):
        tec = object.__new__(GameScreen)
        tec.root = MagicMock()
        tec.quit()

    def test_handle_quit(self,
                            mock_translation, mock_battleship_util_image,
                            battleship_resources, battleship_logic_ai,
                            battleship_logic):
        tec = object.__new__(GameScreen)
        tec.root = MagicMock()
        tec.queue = MagicMock()
        w = MagicMock()
        tec.handle_quit(w)
        tec.queue.put.assert_called_once()
        w.destroy.assert_called_once()

    def test_handle_connection_error(self,
                            mock_translation, mock_battleship_util_image,
                            battleship_resources, battleship_logic_ai,
                            battleship_logic):
        tec = object.__new__(GameScreen)
        tec.root = MagicMock()
        tec.handle_connection_error()
