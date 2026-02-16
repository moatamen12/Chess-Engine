"""
handle user input and display the current game state
"""
from Chess import ChessEngine
import pygame as p


BOARD_WIDTH = BOARD_WIDTH = 600
DIMENSION = 8
SQUIRE_SIZE = BOARD_WIDTH // DIMENSION
MAX_FSB = 15 # FOR ANIMATION
IMAGES = {}
DARK_GRAY = (80, 80, 80)
LIGHT_GRAY = (235, 235, 235)
x = 0
y = 0


# for loading the images
def load_images():
    p.init()

    pieces = ["bR", "bN", "bB", "bQ", "bK", "bp", "wR","wN",  "wB", "wQ", "wK", "wp"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece +".png"), (SQUIRE_SIZE, SQUIRE_SIZE))

def main():
    screen = p.display.set_mode((BOARD_WIDTH, BOARD_WIDTH))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    game_stat = ChessEngine.GameState()

    load_images()

    # events loop
    running =True
    sq_selected = () #track the last click of hte user
    player_clickes = [] #keeps track of the use clicks for moving the pieces
    while running:


        for e in p.event.get():
            # to close the app
            if e.type == p.QUIT:
                running = False

            # moving the pieces
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0]//SQUIRE_SIZE
                row = location[1]//SQUIRE_SIZE
                # if the user double click the same sq
                if sq_selected == (row, col):
                    sq_selected = ()
                    player_clickes = []
                # if the user try to move an empty sq
                elif len(player_clickes) == 1 and (game_stat.board[player_clickes[0][0]][player_clickes[0][1]] == "--") :
                    sq_selected = () #rest user clicks
                    player_clickes = []
                else:
                    sq_selected = (row, col)
                    player_clickes.append(sq_selected) #append user clickes
                if len(player_clickes) == 2:
                    move = ChessEngine.Move(player_clickes[0], player_clickes[1], game_stat.board)
                    print(move.get_chess_notation())
                    game_stat.make_move(move)
                    sq_selected = () #rest user clicks
                    player_clickes = []
        # drow the gs
        drawGameState(screen, game_stat)
        clock.tick(MAX_FSB)
        p.display.flip()


def drawGameState(screen, game_stat):
    drow_board(screen) #drow the sq on thr board

    drow_pieces(screen, game_stat.board) #drow the pieces on the sq

# draw tha board
def drow_board(screen):
    colors = [p.Color("gray"), p.Color("dark green")]
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = colors[(row+col) % 2]
            p.draw.rect(screen, color,p.Rect(col*SQUIRE_SIZE,row*SQUIRE_SIZE,SQUIRE_SIZE,SQUIRE_SIZE))

# draw the pieces
def drow_pieces(screen, board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(col*SQUIRE_SIZE,row*SQUIRE_SIZE,SQUIRE_SIZE,SQUIRE_SIZE))

if __name__ == '__main__':
    main()