"""
TITLE: Pong
ENGINE: Pygame 2 for Python
AUTHOR: LMC II
"""

import sys
import game

def main(*args):

    # System Argument Handling
    if len(args) > 1:
        print('Do Something With Arguments!')
    
    # Start Game
    pong_game = game.Game((640, 480), game.GAME_FPS)
    pong_game.run()

    

if __name__ == '__main__':
    print(__doc__)
    print('Thread:', __name__)
    print('System Arguments:', *sys.argv[1:], '\n')
    main(sys.argv[1:])
