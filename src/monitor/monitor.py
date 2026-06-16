import logging
import time
from state_manager.models import SessionState
from state_manager.state_manager import StateManager
from .processes import get_launcher_pids, is_game_running, kill_process
logger = logging.getLogger(__name__)



class Monitor:
    def __init__(self, state_manager: StateManager, poll_interval: int = 10):
        self._sm = state_manager
        self._poll_interval = poll_interval
        self._game_was_running = False
        self._grace_active = False
        self._running = False


    def run(self) -> None:
        self._running = True
        logger.info("monitor started")
        while self._running:
            try:

                self._tick()
            except Exception:
                logger.exception("unhandled error in monitor tick")
            time.sleep(self._poll_interval)

    def stop(self) -> None:
        self._running = False
        logger.info("monitor stopped")

    def _tick(self) -> None:
        state = self._sm.get()
        game_running = is_game_running()
        launcher_pids = get_launcher_pids()


        if game_running and not self._game_was_running:
            logger.info("game started")

        if not game_running and self._game_was_running:
            logger.info("game ended")
            self._sm.decrement_game()
            self._grace_active = False

        if state.active:
            self._grace_active = False
        else:
            if game_running and self._game_was_running and not self._grace_active:
                logger.info("session expired mid-game — grace period active")
                self._grace_active = True

            if not self._grace_active:
                for pid in launcher_pids:
                    logger.info("session inactive — killing pid %d", pid)
                    kill_process(pid)

        self._game_was_running = game_running
