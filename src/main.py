import asyncio
import logging
import multiprocessing
import os
import uvicorn

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def run_web():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    uvicorn.run("web:app", host="0.0.0.0", port=7860, reload=False)


def run_bot():
    from bot import main as bot_main
    asyncio.run(bot_main())


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    web_process = multiprocessing.Process(target=run_web, name="WebUI")
    bot_process = multiprocessing.Process(target=run_bot, name="TelegramBot")

    try:
        logger.info("Starting WebUI...")
        web_process.start()
        logger.info("Starting Bot...")
        bot_process.start()
        web_process.join()
        bot_process.join()
    except KeyboardInterrupt:
        logger.info("Shutting down...")
        web_process.terminate()
        bot_process.terminate()
        web_process.join()
        bot_process.join()
