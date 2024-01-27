# encoding: utf-8

from app import gui
import scheduler


def main():
    scheduler.start_scheduler()
    gui.start()


if __name__ == '__main__':
    main()
