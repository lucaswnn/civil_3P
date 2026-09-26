import logging

from civil_3P.application.application import Application


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    application = Application()

    raise SystemExit(application.run())
