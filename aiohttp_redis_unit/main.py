#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from multiprocessing import Process

from server import main as server_main
from reporter.reporter import main as reporter_main


def main():
    server_process = Process(target=server_main)
    reporter_process = Process(target=reporter_main)
    server_process.start()
    reporter_process.start()
    server_process.join()


if __name__ == '__main__':
    main()
