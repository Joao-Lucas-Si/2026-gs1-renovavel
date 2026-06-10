import os
import sys

from threading import Thread
from time import sleep

# class _Getch:
#     """Gets a single character from standard input.  Does not echo to the screen."""

#     def __init__(self):
#         try:
#             self.impl = _GetchWindows()

#         except ImportError:
#             self.impl = _GetchUnix()

#     def __call__(self):
#         char = self.impl()
#         if char == "\x03":
#             raise KeyboardInterrupt
#         return char


# class _GetchUnix:
#     def __init__(self):
#         import tty, sys
#         tty.setraw(sys.stdin.fileno())

#     def __call__(self):
#         import sys, tty, termios

#         #fd = sys.stdin.fileno()
#         #old_settings = termios.tcgetattr(fd)
#         try:

#             ch = sys.stdin.read(2)
#         finally:
#             pass
#             #termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
#         return ch


# class _GetchWindows:
#     def __init__(self):
#         import msvcrt

#     def __call__(self):
#         import msvcrt

#         return msvcrt.getch() # type: ignore


# getch = _Getch()


class Pressionado:
    char: str | int

    def __init__(self, char: str | int, limite: int = 5) -> None:
        self.char = char


pressionados: list[Pressionado] = []


def estaPressionado(tecla: str | int, remove: bool = True) -> bool:
    global pressionados
    esta = tecla in list(map(lambda x: x.char, pressionados))
    if esta and remove:
        pressionados = [
            pressionado for pressionado in pressionados if pressionado.char != tecla
        ]
    return esta


def obterTecla(remove: bool = True):
    global pressionados
    if len(pressionados) == 0:
        return None
    esta = pressionados[0].char
    if esta and remove:
        pressionados = [
            pressionado for pressionado in pressionados if pressionado.char != esta
        ]
    return esta


oldterm = None
fd = None

# class CapturaInputBase(Thread, ABC):
#     pass


class CapturaInput(Thread):

    def run(self):
        global pressionados
        if os.name == "nt":
            import msvcrt

            while True:
                a = ""
                if msvcrt.kbhit():
                    a = msvcrt.getch().decode("utf-8")
                # print(repr(a))
                if a != "":
                    pressionados.append(Pressionado(a))

                sleep(0.05)
        else:
            while True:
                a = sys.stdin.read(1)
              

                if a != "":
                    pressionados.append(Pressionado(a))

                sleep(0.05)

        # def m(stdscr: curses.window):
        #     stdscr.nodelay(True)

        #     while True:
        #         a = stdscr.getch()
        #         print(a)
        #         for pressionado in pressionados:
        #             pressionado.limite-=1
        #             if pressionado.limite <= 0:
        #                 pressionado = [pressionado for pressionado in pressionados if pressionado.limite > 0]
        #         pressionados.append(Pressionado(a))

        #         sleep(1)
        # curses.wrapper(m)

    # @staticmethod
    # def on_press(key: keyboard.Key|keyboard.KeyCode|None):
    #     print(key)
    #     # for pressionado in pressionados:
    #     #     pressionado.limite-=1
    #     #     if pressionado.limite <= 0:
    #     #         pressionado = [pressionado for pressionado in pressionados if pressionado.limite > 0]
    #     #     pressionados.append(Pressionado(key))

    @staticmethod
    def iniciar():
        if os.name == "nt":
            pass
        else:
            import termios
            import fcntl

            global fd, oldterm
            fd = sys.stdin.fileno()
            oldterm = termios.tcgetattr(fd)
            newattr = termios.tcgetattr(fd)
            newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
            termios.tcsetattr(fd, termios.TCSANOW, newattr)
            oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
            fcntl.fcntl(fd, fcntl.F_SETFL, os.O_NDELAY)
        tarefa.start()
        # with keyboard.Listener(on_press=CapturaInput.on_press) as listener:
        #     listener.join()

    @staticmethod
    def finalizar():
        if os.name != "nt":
            global fd, oldterm
            import termios
            if fd != None and oldterm != None:
                termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)


tarefa = CapturaInput()
