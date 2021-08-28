"""This is the main file to start the game."""


import sys
import pygame as p
import ai
import breakthru_engine
import move_recordings
import breakthru_properties


def main():
    p.init()
    bp = breakthru_properties.BoardProperties()
    screen = p.display.set_mode(
        (bp.width + bp.piece_Size + bp.inf_width,
         bp.height + bp.piece_Size))
    clock = p.time.Clock()
    screen.fill(p.Color('white'))
    gb = breakthru_engine.GameBoard()
    moves, captures = gb.valid_moves()
    start_play = False
    bp.load_images()
    mode_selection = True
    game_start = True
    click_chosen = ()
    click_chosen_set = []
    AI = ai.AI(bp.max_depth, bp.IDS)
    AI.choose_team = 0
    track = True

    while mode_selection:
        pos = bp.mode_selection(screen)
        for e in p.event.get():
            if e.type == p.QUIT:
                p.quit()
                sys.exit()
            if e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                if pos[0].collidepoint(location):
                    AI.choose_team = 0
                elif pos[1].collidepoint(location):
                    AI.choose_team = 1
                elif pos[2].collidepoint(location):
                    AI.choose_team = 2
                mode_selection = False
        screen.fill(p.Color("gray"))
        bp.mode_selection(screen)
        clock.tick(bp.max_animation)
        p.display.flip()

    while game_start:
        time_consumed = AI.time_consumed
        bp.draw_game(
            screen,
            gb,
            moves,
            captures,
            click_chosen,
            time_consumed)
        if gb.game_continue:
            if gb.turn_team != 0:
                for e in p.event.get():
                    if e.type == p.QUIT:
                        game_start = False

                    elif gb.gold_move and AI.choose_team == 1 and track:
                        track = False
                        AI.ai_move(gb)
                        bp.draw_game(screen, gb, moves, captures,
                                     click_chosen, time_consumed)
                        # if move in moves:
                        #     # print('4')
                        #     gb.makeMove(move)
                        #     start_play = True
                        #     click_chosen = ()  # reset
                        #     click_chosen_set = []
                        # elif move in captures:
                        #     # print('5')
                        #     gb.makeCapture(move)
                        #     start_play = True
                        #     click_chosen = ()  # reset
                        #     click_chosen_set = []
                        start_play = True
                        click_chosen = ()
                        click_chosen_set = []

                    elif not gb.gold_move and AI.choose_team == 2 and track:
                        track = False
                        # print('AI2')
                        AI.ai_move(gb)
                        bp.draw_game(screen, gb, moves, captures,
                                     click_chosen, time_consumed)
                        start_play = True
                        click_chosen = ()
                        click_chosen_set = []

                    # Mouse handler

                    elif e.type == p.MOUSEBUTTONDOWN and track:
                        location = p.mouse.get_pos()  # (x, y) location of mouse
                        col = (location[0] - bp.piece_Size) // bp.piece_Size
                        row = (location[1] - bp.piece_Size) // bp.piece_Size
                        if col > 10 or row > 10:
                            click_chosen = ()
                            click_chosen_set = []
                            break
                        if click_chosen == (
                                row, col):
                            click_chosen = ()
                            click_chosen_set = []
                        else:
                            click_chosen = (row, col)
                            click_chosen_set.append(click_chosen)
                        if len(click_chosen_set) == 2:
                            move = move_recordings.MyMoveRecording(
                                click_chosen_set[0], click_chosen_set[1], gb.board)
                            if len(moves) == 0 and len(captures) == 0:
                                print("The game is staleMate!")
                            if move in moves:
                                # print('4')
                                gb.moves(move)
                                start_play = True
                                click_chosen = ()
                                click_chosen_set = []
                            elif move in captures:
                                # print('5')
                                gb.moves(move)
                                start_play = True
                                click_chosen = ()
                                click_chosen_set = []
                            # if move in moves:
                            #     # print('4')
                            #     gb.moves(move)
                            #     start_play = True
                            #     click_chosen = ()
                            #     click_chosen_set = []
                            # elif move in captures:
                            #     # print('5')
                            #     gb.moves(move)
                            #     start_play = True
                            #     click_chosen = ()  # reset
                            #     click_chosen_set = []

                            else:
                                # print('6')
                                click_chosen_set = [click_chosen]

                    # key handler
                    elif e.type == p.KEYDOWN:
                        if e.key == p.K_z:  # undo when 'z' is pressed
                            gb.retrieve_move()
                            start_play = True
                            # animation = False
                        # if e.key == p.K_r:  # reset the board when 'r' is pressed
                        #     gb = breakthruEngine.my_Game_Board()
                        #     moves = gb.valid_Moves()
                        #     click_chosen = ()
                        #     click_chosen_set = []
                        #     start_play = False
                        #     animation = False
                if start_play:
                    # if animation:
                    #     drawAnimation(gb.moveLog[-1], screen, gb.board, clock)
                    moves, captures = gb.valid_moves()
                    track = True
                    start_play = False
                    # animation = False
            screen.fill(p.Color('gray'))
            bp.draw_game(
                screen,
                gb,
                moves,
                captures,
                click_chosen,
                time_consumed)
            # if gb.checkMate:
            #     # game_over = True
            #     if not gb.goldToMove:
            #         drawNotations(screen, 'Game Over!')
            #     elif gb.goldToMove and 'bK' not in gb.board:
            #         drawNotations(screen, 'Game Over!')
            # elif gb.staleMate:
            #     # game_over = True
            #     drawNotations(screen, 'Draw Game!')
            clock.tick(bp.max_animation)
            p.display.flip()
            if gb.turn_team == 0:
                gb.turn_team = 1
        else:
            font = p.font.SysFont("calibri", 32)
            text = font.render(
                gb.result,
                True,
                p.Color("black"),
                p.Color("gray"))
            text_rect = text.get_rect()
            text_rect.center = (
                (bp.width + bp.piece_Size + bp.inf_width) / 2,
                bp.width / 2)
            bp.draw_game(
                screen,
                gb,
                moves,
                captures,
                click_chosen,
                time_consumed)
            screen.blit(text, text_rect)
            p.display.flip()
            for e in p.event.get():
                if e.type == p.QUIT:
                    game_start = False

    p.quit()


if __name__ == '__main__':
    main()
