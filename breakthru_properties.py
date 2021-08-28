"""This object is built for the properties for the board."""

import pygame as p


class BoardProperties():

    def __init__(self):
        self.width = 512
        self.height = 512
        self.inf_width = 379
        self.dimension = 11
        self.piece_Size = self.width // self.dimension
        self.max_animation = 15
        self.IMAGES = {}
        self.max_depth = 3
        self.IDS = False

    '''load the images for silver piece, gold piece and gold king'''

    def load_images(self):
        images = ['sp', 'gp', 'gK']
        for image in images:
            self.IMAGES[image] = p.transform.scale(p.image.load(
                'images/' + image + '.png'), (self.piece_Size, self.piece_Size))

    ''' draw the board background'''

    def draw_background(self, view):

        colors = p.Color('gray')
        for r in range(self.dimension):
            for c in range(self.dimension):
                # color = colors[((r + c) % 2)]
                p.draw.rect(
                    view,
                    colors,
                    p.Rect(
                        c *
                        self.piece_Size +
                        self.piece_Size,
                        r *
                        self.piece_Size +
                        self.piece_Size,
                        self.piece_Size,
                        self.piece_Size),
                    2)
        p.draw.rect(
            view,
            colors,
            p.Rect(
                self.width +
                self.piece_Size +
                50,
                self.piece_Size +
                self.piece_Size +
                50,
                300,
                500 -
                self.piece_Size *
                2))

    ''' draw the pieces'''

    def draw_pieces(self, view, board, index_to_col, index_to_row):
        font = p.font.SysFont("Calibri", 45)
        half = self.piece_Size / 2
        for row in range(1, self.dimension + 1):
            text = font.render(
                index_to_col[row - 1],
                True,
                p.Color("black"),
                p.Color("gray"))
            text_draw = text.get_rect()
            text_draw.center = (row * self.piece_Size + half, half)
            view.blit(text, text_draw)

            text = font.render(
                index_to_row[row - 1],
                True,
                p.Color("black"),
                p.Color("gray"))
            text_draw = text.get_rect()
            text_draw.center = (half, row * self.piece_Size + half)
            view.blit(text, text_draw)
        # for row in range(dimension - 2, 0):
        #
        #     text = font.render(letters[row], True, p.Color("white"), p.Color("black"))
        #     text_draw = text.get_rect()
        #     text_draw.center = (half, row * size + half)
        #     screen.blit(text, text_draw)
        #
        #     text = font.render(numbers[row], True, p.Color("white"), p.Color("black"))
        #     text_draw = text.get_rect()
        #     text_draw.center = (row * size + half, half)
        #     screen.blit(text, text_draw)

        for row in range(self.dimension):
            for col in range(self.dimension):
                piece = board[row][col]
                if piece != '--':  # not empty square
                    view.blit(
                        self.IMAGES[piece],
                        p.Rect(
                            col *
                            self.piece_Size +
                            self.piece_Size,
                            row *
                            self.piece_Size +
                            self.piece_Size,
                            self.piece_Size,
                            self.piece_Size))

    ''' draw the animation of where the piece can move towards'''

    def draw_animation(self, view, gb, moves, click_chosen):
        if click_chosen != ():
            row, col = click_chosen
            if gb.board[row][col][0] == (
                    'g' if gb.gold_move else 's'):
                s = p.Surface((self.piece_Size, self.piece_Size))
                s.set_alpha(99)
                s.fill((p.Color('black')))
                view.blit(
                    s,
                    (col *
                     self.piece_Size +
                     self.piece_Size,
                     row *
                     self.piece_Size +
                     self.piece_Size))
                s.fill(p.Color('black'))

                for move in moves:
                    if move.start_row == row and move.start_col == col:
                        view.blit(
                            s,
                            (self.piece_Size *
                             move.end_col +
                             self.piece_Size,
                             self.piece_Size *
                             move.end_row +
                             self.piece_Size))

    ''' draw the notations'''
    def draw_notations(self, view, text):
        font = p.font.SysFont('Calibri', 40, True, False)
        notation = font.render(text, 0, p.Color('Gray'))
        notation_location = p.Rect(
            0,
            0,
            self.width,
            self.height).move(
            self.width /
            2 -
            notation.get_width() /
            2,
            self.height /
            2 -
            notation.get_height() /
            2)
        view.blit(notation, notation_location)
        notation = font.render(text, 0, p.Color('black'))
        view.blit(notation, notation_location.move(2, 2))

    '''draw the start interface'''

    def mode_selection(self, view):
        background_image = p.image.load('images/Background.jpeg')
        view.blit(background_image, (0, 0))
        center = p.display.get_surface().get_size()[
            0] / 2 - self.piece_Size * 2
        font = p.font.SysFont("Calibri", 40)
        text = font.render("Breakthru", True, p.Color("black"))
        text_rect = text.get_rect()
        text_rect.center = (self.width - 29, self.piece_Size * 1)
        view.blit(text, text_rect)
        font = p.font.SysFont("Calibri", 20)
        pos1 = p.draw.rect(
            view, p.Color("gray"), p.Rect(
                center, (2 * self.piece_Size), 199, 69), 2)
        text = font.render("Rules", True, p.Color("black"))
        text_rect = text.get_rect()
        text_rect.center = (pos1[0] + 100, pos1[1] + 35)
        view.blit(text, text_rect)
        pos2 = p.draw.rect(
            view, p.Color("gray"), p.Rect(
                center, (5 * self.piece_Size), 199, 69), 2)
        text = font.render("Gold", True, p.Color("black"))
        text_rect = text.get_rect()
        text_rect.center = (pos2[0] + 100, pos2[1] + 35)
        view.blit(text, text_rect)
        pos3 = p.draw.rect(
            view, p.Color("gray"), p.Rect(
                center, (8 * self.piece_Size), 199, 69), 2)
        text = font.render("Silver", True, p.Color("black"))
        text_rect = text.get_rect()
        text_rect.center = (pos3[0] + 100, pos3[1] + 35)
        view.blit(text, text_rect)
        return pos1, pos2, pos3

    '''draw the fight process'''

    def draw_process(self, view, turn, process, time):
        font = p.font.SysFont("Calibri", 19)
        turn = 'Gold' if turn else 'Silver'
        text = font.render(str(turn), True, p.Color("black"))
        text_rect = text.get_rect()
        text_rect.center = (
            self.width + self.piece_Size + 49,
            self.piece_Size / 2 * 3)
        view.blit(text, text_rect)
        text = font.render(
            "Time:" +
            str(time) + 's',
            True,
            p.Color("black"))
        text_rect = text.get_rect()
        text_rect.center = (
            self.width +
            self.piece_Size *
            2 +
            self.inf_width /
            2,
            self.piece_Size /
            2 *
            3)
        view.blit(text, text_rect)

        if len(process) != 0:
            for i in range(len(process)):
                text = font.render(
                    process[len(process) - i - 1], True, p.Color("black"), p.Color("gray"))
                text_rect = text.get_rect()
                text_rect.center = (
                    self.width + self.piece_Size + self.inf_width / 2, 512 - (i + 1) * 30)
                view.blit(text, text_rect)
                if i > 11:
                    break

    # draw the current state of the board

    def draw_game(self, view, gb, moves, captures, click_chosen, time):
        self.draw_background(view)
        self.draw_process(view, gb.gold_move, gb.process, time)
        self.draw_animation(view, gb, moves, click_chosen)
        self.draw_animation(view, gb, captures, click_chosen)
        self.draw_pieces(view, gb.board, gb.index_to_col, gb.index_to_row)
