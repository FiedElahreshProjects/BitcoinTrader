from contextlib import asynccontextmanager
import pytest
from unittest.mock import patch, MagicMock
from apscheduler.schedulers.background import BackgroundScheduler
from BackEnd.tasks.trading import autonomous_trading_logic
from BackEnd.tasks.data_collection import daily_data_collection
import asyncio
import time


#just overrides the Background scheduler makes sure to call the super class constructor and
# makes the add_job and shutdown to MagicMock()
class MockScheduler(BackgroundScheduler):
    def __init__(self):
        super().__init__()
        self.add_job = MagicMock()
        self.shutdown = MagicMock()
        self.start = MagicMock()

@asynccontextmanager
async def lifespan(scheduler):
    daily_data_collection()
    autonomous_trading_logic()
    
    scheduler.add_job(autonomous_trading_logic, 'interval', days=1)
    scheduler.add_job(daily_data_collection, 'interval', days=1)
    scheduler.start()
    yield
    scheduler.shutdown()

def test_scheduler_multiple_jobs():
    scheduler = MockScheduler()

    async def run_lifespan():
        async with lifespan(scheduler=scheduler):
            # Simulate adding more jobs
            scheduler.add_job(daily_data_collection, 'interval', days=2)
            scheduler.add_job(autonomous_trading_logic, 'interval', days=3)

    asyncio.run(run_lifespan())

    # Assertions
    assert scheduler.add_job.call_count == 4  # 2 in lifespan + 2 simulated
    scheduler.shutdown.assert_called_once()



@patch("BackEnd.tasks.trading.autonomous_trading_logic")
@patch("BackEnd.tasks.data_collection.daily_data_collection")
def test_scheduler_execution(mock_daily_data_collection, mock_autonomous_trading_logic):
    """Test that the scheduled jobs execute correctly."""
    # Simulate the scheduler running the tasks
    scheduler = BackgroundScheduler()
    scheduler.add_job(mock_autonomous_trading_logic, 'interval', seconds=1)  # Short interval for testing
    scheduler.add_job(mock_daily_data_collection, 'interval', seconds=1)
    scheduler.start()

    # Allow the scheduler to run for a short time
    
    time.sleep(3)

    # Verify that the scheduled tasks were executed
    assert mock_autonomous_trading_logic.call_count >= 2
    assert mock_daily_data_collection.call_count >= 2

    # Shut down the scheduler
    scheduler.shutdown()


def test_scheduler_shutdown():
    scheduler = MockScheduler()
    # Mock app lifespan context
    async def run_lifespan():
        async with lifespan(scheduler=scheduler):
            pass

    asyncio.run(run_lifespan())

    # Verify that the scheduler was shut down
    scheduler.shutdown.assert_called_once()