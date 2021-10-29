# Author: Kenny Seng
# Date: 3/12/2020
# Description: Replicates the abstract board game called Xiangqi. Includes all of the game's pieces and the board.
#              The game ends when one general is put into checkmate.


class XiangqiGame:
    """Represents the game board. Can return the game state and determine if a specified player is in check.
    Also responsible for making moves."""

    def __init__(self):
        """Initializes the board, the pieces for both sides, the game state as UNFINISHED, and the turn count as 1."""
        # Rows are labeled 1-10 and Columns are labeled a-i
        # Row 1 is the red side and row 10 is the black side

        #############################
        # Abbreviations:            #
        # Advisor   -> A            #
        # Cannon    -> C            #
        # Chariot   -> R (for Rook) #
        # Elephant  -> E            #
        # General   -> G            #
        # Horse     -> H            #
        # Soldier   -> S            #
        #############################

        # Red General, back center of red side.
        self.__r_g = General('red', 'e1')

        # Two Advisors on either side of the general; left/ride side
        self.__r_a_l = Advisor('red', 'd1')
        self.__r_a_r = Advisor('red', 'f1')

        # Two Elephants next to the advisors; left/ride side
        self.__r_e_l = Elephant('red', 'c1')
        self.__r_e_r = Elephant('red', 'g1')

        # Two Horses next to the elephants; left/right side
        self.__r_h_l = Horse('red', 'b1')
        self.__r_h_r = Horse('red', 'h1')

        # Two Chariots in the corner; left/right side
        self.__r_r_l = Chariot('red', 'a1')
        self.__r_r_r = Chariot('red', 'i1')

        # Two Cannons at b3 and h3; left/right side
        self.__r_c_l = Cannon('red', 'b3')
        self.__r_c_r = Cannon('red', 'h3')

        # 5 Soldiers evenly spaced out along row 4
        self.__r_s_1 = Soldier('red', 'a4')
        self.__r_s_2 = Soldier('red', 'c4')
        self.__r_s_3 = Soldier('red', 'e4')
        self.__r_s_4 = Soldier('red', 'g4')
        self.__r_s_5 = Soldier('red', 'i4')

        # Black General, back center of black side.
        self.__b_g = General('black', 'e10')

        # Two Advisors on either side of the general - left/right side
        self.__b_a_l = Advisor('black', 'd10')
        self.__b_a_r = Advisor('black', 'f10')

        # Two Elephants next to the advisors; left/right side
        self.__b_e_l = Elephant('black', 'c10')
        self.__b_e_r = Elephant('black', 'g10')

        # Two Horses next to the elephants; left/right side
        self.__b_h_l = Horse('black', 'b10')
        self.__b_h_r = Horse('black', 'h10')

        # Two Chariots in the corner; left/right side
        self.__b_r_l = Chariot('black', 'a10')
        self.__b_r_r = Chariot('black', 'i10')

        # Two Cannons at b8 and h8; left/right side
        self.__b_c_l = Cannon('black', 'b8')
        self.__b_c_r = Cannon('black', 'h8')

        # 5 Soldiers evenly spaced out along row 7
        self.__b_s_1 = Soldier('black', 'a7')
        self.__b_s_2 = Soldier('black', 'c7')
        self.__b_s_3 = Soldier('black', 'e7')
        self.__b_s_4 = Soldier('black', 'g7')
        self.__b_s_5 = Soldier('black', 'i7')

        # Visualization of the board
        ############################################################
        #      Palace(red side): d1-f1, d2-f2, d3-f3               #
        #    a      b     c     d    e     f      g     h     i    #
        # 1 ['rR', 'rH', 'rE', 'rA', 'rG', 'rA', 'rE', 'rH', 'rR'] #
        # 2 ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '] #
        # 3 ['  ', 'rC', '  ', '  ', '  ', '  ', '  ', 'rC', '  '] #
        # 4 ['rS', '  ', 'rS', '  ', 'rS', '  ', 'rS', '  ', 'rS'] #
        # 5 ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '] #
        #   [           River exists between row 5/6             ] #
        # 6 ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '] #
        # 7 ['bS', '  ', 'bS', '  ', 'bS', '  ', 'bS', '  ', 'bS'] #
        # 8 ['  ', 'bC', '  ', '  ', '  ', '  ', '  ', 'rC', '  '] #
        # 9 ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '] #
        # 10 ['bR', 'bH', 'bE', 'bA', 'bG', 'bA', 'bE', 'bH', 'bR']#
        #       Palace (black side): d8-f8, d9-f9, d10-f10         #
        ############################################################

        # Hard coding all of the pieces onto the board
        self.__row_1 = [self.__r_r_l, self.__r_h_l, self.__r_e_l, self.__r_a_l, self.__r_g, self.__r_a_r, self.__r_e_r,
                        self.__r_h_r, self.__r_r_r]
        self.__row_2 = [None, None, None, None, None, None, None, None, None]
        self.__row_3 = [None, self.__r_c_l, None, None, None, None, None, self.__r_c_r, None]
        self.__row_4 = [self.__r_s_1, None, self.__r_s_2, None, self.__r_s_3, None, self.__r_s_4, None, self.__r_s_5]
        self.__row_5 = [None, None, None, None, None, None, None, None, None]
        # River exists between row 5/6
        self.__row_6 = [None, None, None, None, None, None, None, None, None]
        self.__row_7 = [self.__b_s_1, None, self.__b_s_2, None, self.__b_s_3, None, self.__b_s_4, None, self.__b_s_5]
        self.__row_8 = [None, self.__b_c_l, None, None, None, None, None, self.__b_c_r, None]
        self.__row_9 = [None, None, None, None, None, None, None, None, None]
        self.__row_10 = [self.__b_r_l, self.__b_h_l, self.__b_e_l, self.__b_a_l, self.__b_g, self.__b_a_r, self.__b_e_r,
                         self.__b_h_r, self.__b_r_r]

        # The board is a list of rows containing the pieces.
        self.__board = [self.__row_1, self.__row_2, self.__row_3, self.__row_4, self.__row_5, self.__row_6,
                        self.__row_7, self.__row_8, self.__row_9, self.__row_10]

        # Game state starts as UNFINISHED and the turn_count starts as 1.
        self.__game_state = "UNFINISHED"
        self.__turn_counter = 1

    def get_game_state(self):
        """Returns the game state of the board; UNFINISHED, RED_WON, or BLACK_WON"""
        return self.__game_state

    def set_game_state(self, new_state):
        """Updates the game state of the board."""
        self.__game_state = new_state

    def get_general(self, player):
        """Returns the specified general"""
        if player == 'red':
            return self.__r_g
        elif player == 'black':
            return self.__b_g

    def get_board(self):
        """Returns the game board"""
        return self.__board

    def get_turn_counter(self):
        """Returns the turn counter"""
        return self.__turn_counter

    def inc_turn_counter(self):
        """Increments the turn counter"""
        self.__turn_counter += 1

    def is_checkmate(self, player):
        """Determines if the specified player is in checkmate. Checks if the player's General has any legal moves."""
        # Variables for the General's location, row, and col.
        g_loc = self.get_general(player).get_location()
        g_row = int(g_loc[1:])
        g_col = ord(g_loc[0])

        # The four directions a General can move in any given position
        g_w = chr(g_col - 1) + str(g_row)  # west
        g_e = chr(g_col + 1) + str(g_row)  # east
        g_s = chr(g_col) + str(g_row + 1)  # south
        g_n = chr(g_col) + str(g_row - 1)  # north

        # List of possible moves and a flag to determine if the General is still in check.
        possible_moves = [g_n, g_s, g_e, g_w]
        in_check = True

        # From the possible moves, if the general can move there and not be in check, return False.
        for loc in possible_moves:
            if self.get_general(player).can_move(loc):
                if self.get_piece(loc) is not None:
                    temp_piece = self.get_piece(loc)
                elif self.get_piece(loc) is None:
                    temp_piece = None

                # Make the move temporarily
                self.set_piece(None, g_loc)
                self.get_general(player).set_location(loc)
                self.set_piece(self.get_general(player), loc)

                # Determine if the move places the player in check
                if not self.is_in_check(player):
                    in_check = False

                # Undo the move and return the results
                self.set_piece(self.get_general(player), g_loc)
                self.get_general(player).set_location(g_loc)
                self.set_piece(temp_piece, loc)

            if in_check is False:
                return False
        if in_check is True:
            return True

    def is_in_check(self, player):
        """Returns True if the specified player is in check, otherwise returns False"""
        # Temp piece to test valid locations
        temp = Piece('temp', 'temp', 'temp')

        # Variables for the specified General's location, row, and col.
        g_loc = self.get_general(player).get_location()
        g_row = int(g_loc[1:])  # integer representing row
        g_col = ord(g_loc[0])  # integer representing col
        # Variables for the Red General's location, row, and col.
        r_g_loc = self.get_general('red').get_location()
        r_g_row = int(r_g_loc[1:])
        r_g_col = ord(r_g_loc[0])
        # Variables for the Black General's location, row, and col.
        b_g_loc = self.get_general('black').get_location()
        b_g_row = int(b_g_loc[1:])
        b_g_col = ord(b_g_loc[0])

        # General: If Generals are in the same column and there are no pieces between them, they are in check.
        if r_g_col == b_g_col:
            gen_col = self.get_col(r_g_loc[0])[r_g_row:b_g_row - 1]
            counter = 0
            for piece in gen_col:
                if piece is not None:
                    counter += 1
            if counter == 0:
                return True

        # Soldier: Orthogonally checks for Soldiers around the General, depending on location and side.
        s_left = chr(g_col - 1) + str(g_row)
        s_right = chr(g_col + 1) + str(g_row)
        s_below = chr(g_col) + str(g_row + 1)
        s_above = chr(g_col) + str(g_row - 1)

        # Each case checks if the given piece at each location is a Soldier and if they belong to the player.
        if self.get_piece(s_left) is not None:
            if self.get_piece(s_left).get_name() == 'Soldier' and self.get_piece(s_left).get_player() != player:
                return True
        if self.get_piece(s_right) is not None:
            if self.get_piece(s_right).get_name() == 'Soldier' and self.get_piece(s_right).get_player() != player:
                return True
        if player == 'red' and self.get_piece(s_below) is not None:
            if self.get_piece(s_below).get_name() == 'Soldier' and self.get_piece(s_below).get_player() != player:
                return True  # in check
        if player == 'black' and self.get_piece(s_above) is not None:
            if self.get_piece(s_above).get_name() == 'Soldier' and self.get_piece(s_above).get_player() != player:
                return True

        # Horse: Checks the 8 possible ways a Horse can put a General in check.
        h_1 = chr(g_col + 1) + str(g_row + 2)
        h_2 = chr(g_col + 1) + str(g_row - 2)
        h_3 = chr(g_col + 2) + str(g_row + 1)
        h_4 = chr(g_col + 2) + str(g_row - 1)
        h_5 = chr(g_col - 1) + str(g_row + 2)
        h_6 = chr(g_col - 1) + str(g_row - 2)
        h_7 = chr(g_col - 2) + str(g_row + 1)
        h_8 = chr(g_col - 2) + str(g_row - 1)

        # Two lists; one of possible locations, one of actual locations on the board
        pos_h = [h_1, h_2, h_3, h_4, h_5, h_6, h_7, h_8]
        test_h = []
        # For each possible location, if it is on the board, add it to test_h
        for h in pos_h:
            if temp.can_move(h):
                test_h.append(h)
        # For each board location, if there is a Horse, check if the Horse is an enemy and if it can reach the General.
        for h in test_h:
            if self.get_piece(h) is not None:
                if self.get_piece(h).get_name() == 'Horse' and self.get_piece(h).get_player() != player:
                    if self.is_horse_blocked(self.get_piece(h), g_loc) is False:
                        return True

        # Chariot: Checks if there is a Chariot in the same row/col as the General, and if there are any pieces
        # between them.
        # Variables for the lists holding the pieces of each row and column of the General
        r_row = self.get_board()[g_row - 1]
        r_col = self.get_col(g_loc[0])

        for piece in r_col:
            if piece is not None:
                if piece.get_name() == 'RChariot' and piece.get_player() != player:
                    p_row = int(piece.get_location()[1:])
                    if p_row < g_row:
                        temp = r_col[p_row:g_row - 1]  # Sublist of the spaces between the Chariot and the General
                        counter = 0
                        for item in temp:
                            if item is not None:  # If there is a piece in that sublist, counter is incremented
                                counter += 1
                        if counter == 0:  # If no pieces, Chariot put General in check
                            return True
                    elif p_row > g_row:
                        temp = r_col[g_row:p_row - 1]  # Different sublist depending on direction
                        counter = 0
                        for item in temp:
                            if item is not None:  # If there is a piece in that sublist, counter is incremented
                                counter += 1
                        if counter == 0:  # If no pieces, Chariot put General in check
                            return True

        for piece in r_row:
            if piece is not None:
                if piece.get_name() == 'RChariot' and piece.get_player() != player:
                    # The letter of each column is converted to the corresponding integer on the board.
                    p_col = ord(piece.get_location()[0]) - 97
                    if p_col < g_col - 97:
                        temp = r_row[p_col + 1:g_col - 97]
                        counter = 0
                        for item in temp:
                            if item is not None:
                                counter += 1
                        if counter == 0:
                            return True
                    elif p_col > g_col - 97:
                        temp = r_row[g_col - 97:p_col - 1]
                        counter = 0
                        for item in temp:
                            if item is not None:
                                counter += 1
                        if counter == 0:
                            return True

        # Cannon: Checks if there is a Cannon in the same row/col as the General, and if there is a single piece
        # between them.

        for piece in r_col:
            if piece is not None:
                if piece.get_name() == 'Cannon' and piece.get_player() != player:
                    p_row = int(piece.get_location()[1:])
                    if p_row < g_row:
                        temp = r_col[p_row:g_row - 1]  # Sublist of the spaces between the Chariot and the General
                        counter = 0
                        for item in temp:
                            if item is not None:  # If there is a piece in that sublist, counter is incremented
                                counter += 1
                        if counter == 1:  # If only a single piece, Cannon put General in check.
                            return True
                    elif p_row > g_row:
                        temp = r_col[g_row:p_row - 1]  # Different sublist depending on orientation
                        counter = 0
                        for item in temp:
                            if item is not None:  # If there is a piece in that sublist, counter is incremented
                                counter += 1
                        if counter == 1:  # If only a single piece, Cannon put General in check.
                            return True

        for piece in r_row:
            if piece is not None:
                if piece.get_name() == 'Cannon' and piece.get_player() != player:
                    p_col = ord(piece.get_location()[0]) - 97
                    if p_col < g_col - 97:
                        temp = r_row[p_col:g_col - 97 - 1]
                        counter = 0
                        for item in temp:
                            if item is not None:
                                counter += 1
                        if counter == 1:  # if only a single piece, Cannon put General in check.
                            return True
                    elif p_col > g_col - 97:
                        temp = r_row[g_col - 97:p_col - 1]
                        counter = 0
                        for item in temp:
                            if item is not None:
                                counter += 1
                        if counter == 1:  # if only a single piece, Cannon put General in check.
                            return True
        return False

    def is_horse_blocked(self, horse, square_to):
        """Determines if a Horse in the 8 possible check locations around a General is blocked by another piece."""
        square_from = horse.get_location()
        if horse.can_move(square_to):
            # Variables to convert each row/col into their respective integers
            row_to = int(square_to[1:])
            col_to = ord((square_to[0])) - 97
            row_from = int(square_from[1:])
            col_from = ord(square_from[0]) - 97

            # Case 1: If desired move is up 2 and left/right one, check horse' NORTH
            if row_to - row_from == -2 and abs(col_from - col_to) == 1:
                temp = chr(col_from + 97) + str(row_from - 1)
                if self.get_piece(temp) is not None:
                    return True

            # Case 2: If desired move is down 2 and left/right one, check horse' SOUTH
            if row_to - row_from == 2 and abs(col_from - col_to) == 1:
                temp = chr(col_from + 97) + str(row_from + 1)
                if self.get_piece(temp) is not None:
                    return True

            # Case 3: If desired move is right 2 and up/down one, check horse' EAST
            if abs(row_to - row_from) == 1 and col_to - col_from == 2:
                temp = chr(col_from + 97 + 1) + str(row_from)
                if self.get_piece(temp) is not None:
                    return True

            # Case 4: If desired move is left 2 and up/down one, check horse' WEST
            if abs(row_to - row_from) == 1 and col_to - col_from == -2:
                temp = chr(col_from + 97 - 1) + str(row_from)
                if self.get_piece(temp) is not None:
                    return True
        return False

    def make_move(self, square_from, square_to):
        """Determines if the desired move can be made. If so, move is made, game_state is updated, and returns True.
         Else, if the move is invalid, or if the game has already been won, returns False"""
        # Variables for the pieces at square_from and square_to (if any, or if None)
        p1 = self.get_piece(square_from)
        p2 = self.get_piece(square_to)

        # Red or Black has already won
        if self.get_game_state() != 'UNFINISHED':
            print("Game has already finished. " + self.get_game_state() + '.')
            return False

        # There is no piece at square_from; invalid move
        if p1 is None:
            print("There is no piece at " + square_from + '. Invalid move.')
            return False

        # Red has every odd turn (1,3,5..), check to see which player's piece is at square_from
        if self.get_turn_counter() % 2 == 1 and p1.get_player() == 'black':
            print("Invalid move - it is not Black's turn!")
            return False
        # Black has every even turn (2,4,6..), check to see which player's piece is at square_from
        if self.get_turn_counter() % 2 == 0 and p1.get_player() == 'red':
            print("Invalid move - it is not Red's turn!")
            return False

        # If the square_to exists on the board
        if p1.can_move(square_to):
            row_to = int(square_to[1:])
            col_to = ord((square_to[0])) - 97
            row_from = int(square_from[1:])
            col_from = ord(square_from[0]) - 97

            # Checks if the Horse is blocked in the direction of square_to
            if p1.get_name() == 'Horse':
                # Case 1: If desired move is down 2 and left/right one, check horse' NORTH works
                if row_to - row_from == -2 and abs(col_from - col_to) == 1:
                    temp = chr(col_from + 97) + str(row_from - 1)
                    if self.get_piece(temp) is not None:
                        print("Invalid move! Horse is blocked to the NORTH.")
                        self.print_board()
                        return False

                # Case 2: If desired move is up 2 and left/right one, check horse' SOUTH
                if row_to - row_from == 2 and abs(col_from - col_to) == 1:
                    temp = chr(col_from + 97) + str(row_from + 1)
                    if self.get_piece(temp) is not None:
                        print("Invalid move! Horse is blocked to the SOUTH.")
                        self.print_board()
                        return False

                # Case 3: If desired move is right 2 and up/down one, check horse' EAST works
                if abs(row_to - row_from) == 1 and col_to - col_from == 2:
                    temp = chr(col_from + 97 + 1) + str(row_from)
                    if self.get_piece(temp) is not None:
                        print("Invalid move! Horse is blocked to the EAST.")
                        self.print_board()
                        return False

                # Case 4: If desired move is left 2 and up/down one, check horse' WEST
                if abs(row_to - row_from) == 1 and col_to - col_from == -2:
                    temp = chr(col_from + 97 - 1) + str(row_from)
                    if self.get_piece(temp) is not None:
                        print("Invalid move! Horse is blocked to the WEST.")
                        self.print_board()
                        return False

            # Checks if the Elephant is blocked
            if p1.get_name() == 'Elephant':
                temp = chr(int((col_from + col_to) / 2) + 97) + str(int((row_from + row_to) / 2))
                if self.get_piece(temp) is not None:
                    print("Invalid move! Elephant is blocked.")
                    self.print_board()
                    return False

            # Checks if the Chariot is blocked
            if p1.get_name() == 'RChariot':
                # Vertical Movement
                if col_from == col_to:
                    counter = 0
                    if row_to > row_from:
                        r_col = self.get_col(square_from[0])[row_from:row_to - 1]
                    if row_to < row_from:
                        r_col = self.get_col(square_from[0])[row_to:row_from - 1]
                    for piece in r_col:
                        if piece is not None:
                            counter += 1
                    if counter != 0:
                        print("Invalid move! Chariot is blocked.")
                        self.print_board()
                        return False
                # Horizontal Movement
                if row_from == row_to:
                    counter = 0
                    if col_to > col_from:
                        r_row = self.get_board()[row_to - 1][col_from + 1:col_to]
                    if col_to < col_from:
                        r_row = self.get_board()[row_to - 1][col_to + 1:col_from]
                    for piece in r_row:
                        if piece is not None:
                            counter += 1
                    if counter != 0:
                        print("Invalid move! Chariot is blocked.")
                        self.print_board()
                        return False

            # Checks if the Cannon has something to capture and/or if there is a piece to jump over.
            if p1.get_name() == 'Cannon':
                # Vertical Movement
                if col_from == col_to:
                    counter = 0
                    if row_to > row_from:
                        r_col = self.get_col(square_from[0])[row_from:row_to - 1]
                    if row_to < row_from:
                        r_col = self.get_col(square_from[0])[row_to:row_from - 1]
                    for piece in r_col:
                        if piece is not None:
                            counter += 1
                    if counter == 1 and p2 is None:
                        print("Invalid move! Cannon is blocked with nothing to capture.")
                        self.print_board()
                        return False
                    if counter != 1 and p2 is not None:
                        print("Invalid move! Cannon does not have a single piece to jump over.")
                        self.print_board()
                        return False

                # Horizontal Movement
                if row_from == row_to:
                    counter = 0
                    if col_to > col_from:
                        r_row = self.get_board()[row_to - 1][col_from + 1:col_to]
                    if col_to < col_from:
                        r_row = self.get_board()[row_to - 1][col_to + 1:col_from]
                    for piece in r_row:
                        if piece is not None:
                            counter += 1
                    if counter == 1 and p2 is None:
                        print("Invalid move! Cannon is blocked with nothing to capture.")
                        self.print_board()
                        return False
                    if counter != 1 and p2 is not None:
                        print("Invalid move! Cannon does not have a single piece to jump over.")
                        self.print_board()
                        return False

            # If square_to is empty or if piece at square_to is the enemy
            if p2 is None or p1.get_player() != p2.get_player():
                # Move to the new location or capture the enemy at the new location
                self.set_piece(None, square_from)
                p1.set_location(square_to)
                self.set_piece(p1, square_to)
                # If this move puts you in check, revert the move and return False.
                if self.get_turn_counter() % 2 == 1 and self.is_in_check('red'):
                    self.set_piece(p1, square_from)
                    p1.set_location(square_from)
                    self.set_piece(p2, square_to)
                    print("Invalid move - Red is in check or move puts Red in check!")
                    self.print_board()
                    return False
                # If this move puts you in check, revert the move and return False.
                if self.get_turn_counter() % 2 == 0 and self.is_in_check('black'):
                    self.set_piece(p1, square_from)
                    p1.set_location(square_from)
                    self.set_piece(p2, square_to)
                    print("Invalid move - Black is in check or move puts Black in check!")
                    self.print_board()
                    return False

                # Print statements for moving and/or checking
                if p2 is None:
                    if self.get_turn_counter() % 2 == 0 and self.is_in_check('red'):  # black turn and red in check
                        print(p1.get_player()[0].upper() + p1.get_player()[
                                                           1:] + ' ' + p1.get_name() + ' at ' + square_from + ' moves to ' + square_to + ' and puts the Red General in check!')
                    elif self.get_turn_counter() % 2 == 1 and self.is_in_check('black'):  # red turn and black in check
                        print(p1.get_player()[0].upper() + p1.get_player()[
                                                           1:] + ' ' + p1.get_name() + ' at ' + square_from + ' moves to ' + square_to + ' and puts the Black General in check!')
                    else:
                        print(p1.get_player()[0].upper() + p1.get_player()[
                                                           1:] + ' ' + p1.get_name() + ' at ' + square_from + ' moves to ' + square_to + '.')

                # Print statements for capturing and/or checking
                if p2 is not None:
                    if self.get_turn_counter() % 2 == 0 and self.is_in_check('red'):  # black turn and red in check
                        print(p1.get_player()[0].upper() + p1.get_player()[
                                                           1:] + ' ' + p1.get_name() + ' at ' + square_from + ' captures ' +
                              p2.get_player()[0].upper() + p2.get_player()[
                                                           1:] + ' ' + p2.get_name() + ' at ' + square_to + ' and puts the Red General in check!')
                    elif self.get_turn_counter() % 2 == 1 and self.is_in_check('black'):  # red turn and black in check
                        print(p1.get_player()[0].upper() + p1.get_player()[
                                                           1:] + ' ' + p1.get_name() + ' at ' + square_from + ' captures ' +
                              p2.get_player()[0].upper() + p2.get_player()[
                                                           1:] + ' ' + p2.get_name() + ' at ' + square_to + ' and puts the Black General in check!')
                    else:
                        print(p1.get_player()[0].upper() + p1.get_player()[
                                                           1:] + ' ' + p1.get_name() + ' at ' + square_from + ' captures ' +
                              p2.get_player()[0].upper() + p2.get_player()[
                                                           1:] + ' ' + p2.get_name() + ' at ' + square_to + '.')

                # Increment the turn and print the board.
                self.inc_turn_counter()  # turn has been made, increment the turn to the next player
                self.print_board()

                # If any moves lead to check mate, game is over.
                if self.is_checkmate('red'):
                    self.set_game_state("BLACK_WON")
                    print("Red has no more legal moves; CHECKMATE - BLACK WINS!")
                    return False
                if self.is_checkmate('black'):
                    self.set_game_state("RED_WON")
                    print("Black has no more legal moves; CHECKMATE - RED WINS!")
                    return False

                return True
            elif self.get_game_state() == 'UNFINISHED':
                print("Invalid move - cannot capture own piece!")
                self.print_board()
                return False

        else:
            print("Invalid move - " + p1.get_player()[0].upper() + p1.get_player()[
                                                                   1:] + ' ' + p1.get_name() + " at " + square_from + " cannot move to " + square_to)
            self.print_board()
            return False

    def print_board(self):
        """Prints the game board"""
        for row in self.get_board():
            temp = '['
            for piece in row:
                if piece is None:
                    temp += "    ,"
                else:

                    temp += ' ' + (piece.get_player()[0] + piece.get_name()[0]) + ', '
            print(temp + ']')
        temp = self.get_turn_counter()
        if temp % 2 == 1:
            print("Red's turn")
        elif temp % 2 == 0:
            print("Black's turn")
        print()

    def get_col(self, col):
        """Returns a list of the specified column of the board"""
        board = self.get_board()
        temp_col = []
        for row in board:
            temp_col.append(row[ord(col) - 97])
        return temp_col

    def get_piece(self, location):
        """Returns the piece at the specified location"""
        row = int(location[1:])
        col = location[0]

        board = self.get_board()
        return board[row - 1][ord(col) - 97]

    def set_piece(self, piece, location):
        """Sets the piece at the specified location"""
        row = int(location[1:])
        col = location[0]
        board = self.get_board()
        board[row - 1][ord(col) - 97] = piece


class Piece:
    """Represents a game piece. Contains the current location of the given piece and the desired location."""

    def __init__(self, player, name, location):
        """Initializes the piece's player, name, and location."""
        # Red or Black
        self.__player = player
        # What type of piece
        self.__name = name
        # Location on board via algebraic notation
        self.__location = location

    def get_player(self):
        """Returns the Piece's player"""
        return self.__player

    def get_name(self):
        """Returns the Piece's name"""
        return self.__name

    def get_location(self):
        """Returns the Piece's location"""
        return self.__location

    def set_location(self, location):
        """Sets the Piece's location"""
        self.__location = location

    def can_move(self, square_to):
        """Checks if the desired location to move to is on the board."""
        row_to = int(square_to[1:])
        col_to = ord((square_to[0])) - 97
        if 1 <= row_to <= 10 and 0 <= col_to <= 8:
            return True
        # Cannot move to the same square.
        elif self.get_location() == square_to:
            return False
        else:
            return False


class General(Piece):
    """Represents the General. Can only move/capture orthogonally one space within the palace.
    Generals cannot face each other."""

    def __init__(self, player, location):
        """Calls Piece's __init__ with General as the name"""
        super().__init__(player, 'General', location)

    def can_move(self, square_to):
        """Determines if the General can move to the specified location. Must stay in the palace.
        Can only move one space orthogonally"""

        player = super().get_player()
        if super().can_move(square_to) is True:
            # 9 Possible locations a general can move to orthogonally
            red_palace = ['d1', 'd2', 'd3', 'e1', 'e2', 'e3', 'f1', 'f2', 'f3']
            black_palace = ['d8', 'd9', 'd10', 'e8', 'e9', 'e10', 'f8', 'f9', 'f10']

            row_to = int(square_to[1:])
            col_to = ord((square_to[0])) - 97
            row_from = int(super().get_location()[1:])
            col_from = ord(super().get_location()[0]) - 97

            # If the location is within one space orthogonally and in the palace, can move.
            if player == 'red' and square_to in red_palace:
                if (row_from == row_to and abs(col_to - col_from) == 1) or (
                        col_to == col_from and abs(row_to - row_from) == 1):
                    return True
            if player == 'black' and square_to in black_palace:
                if (row_from == row_to and abs(col_to - col_from) == 1) or (
                        col_to == col_from and abs(row_to - row_from) == 1):
                    return True
        else:
            return False


class Advisor(Piece):
    """Represents the Advisor. Can only move/capture diagonally one space within then palace."""

    def __init__(self, player, location):
        """Calls Piece's __init__ with Advisor as the name"""
        super().__init__(player, 'Advisor', location)

    def can_move(self, square_to):
        """Determines if the Advisor can move to the specified location. Must stay in the palace.
        Can only move diagonally one space."""

        player = self.get_player()
        if super().can_move(square_to) is True:
            # Only five locations in the palace due to diagonal restriction
            red_palace = ['d1', 'd3', 'e2', 'f1', 'f3']
            black_palace = ['d8', 'd10', 'e9', 'f8', 'f10']

            row_to = int(square_to[1:])
            col_to = ord((square_to[0])) - 97
            row_from = int(super().get_location()[1:])
            col_from = ord(super().get_location()[0]) - 97

            # If the space is within one space diagonally and in the palace, can move.
            if player == 'red' and square_to in red_palace:
                if abs(row_from - row_to) == 1 and abs(col_to - col_from) == 1:
                    return True
            if player == 'black' and square_to in black_palace:
                if abs(row_from - row_to) == 1 and abs(col_to - col_from) == 1:
                    return True
        else:
            return False


class Elephant(Piece):
    """Represents the Elephant. Can only move/capture diagonally two spaces and may not jump over other pieces.
    Elephants cannot cross the river - they serve as defensive pieces."""

    def __init__(self, player, location):  # Elephant
        """Calls Piece's __init__ with Elephant as the name"""
        super().__init__(player, 'Elephant', location)

    def can_move(self, square_to):
        """Determines if the Elephant can move to the specified location. Can move two spaces diagonally.
        Cannot cross the river, cannot jump over pieces."""

        player = self.get_player()
        if super().can_move(square_to) is True:
            # 7 Possible Locations for either side.
            red_side = ['c1', 'g1', 'a3', 'e3', 'i3', 'c5', 'g5']
            black_side = ['c6', 'g6', 'a8', 'e8', 'i8', 'c10', 'g10']

            row_to = int(square_to[1:])  # first letter
            col_to = ord((square_to[0])) - 97  # second letter (10)
            row_from = int(super().get_location()[1:])
            col_from = ord(super().get_location()[0]) - 97

            # If the location is within 2 spaces diagonally.
            if player == 'red' and square_to in red_side:
                if abs(row_from - row_to) == 2 and abs(col_to - col_from) == 2:
                    return True
            if player == 'black' and square_to in black_side:
                if abs(row_from - row_to) == 2 and abs(col_to - col_from) == 2:
                    return True
        else:
            return False


class Horse(Piece):
    """Represents the Horse. Can only move/capture one space orthogonally and then one space diagonally.
    Horses cannot jump over pieces, and can be blocked by pieces located orthogonally from it."""

    def __init__(self, player, location):
        """Calls Piece's __init__ with Horse as the name"""
        super().__init__(player, 'Horse', location)

    def can_move(self, square_to):
        """Determines if the Horse can move to the specified location. Moves one space orthogonally then one space
        diagonally. Cannot jump over pieces; can be blocked orthogonally."""
        if super().can_move(square_to) is True:
            row_to = int(square_to[1:])
            col_to = ord((square_to[0])) - 97
            row_from = int(super().get_location()[1:])
            col_from = ord(super().get_location()[0]) - 97

            # If the location is within 2 spaces in one direction and 1 in the other.
            if abs(row_from - row_to) == 1 and abs(col_to - col_from) == 2:
                return True
            elif abs(row_from - row_to) == 2 and abs(col_to - col_from) == 1:
                return True
        else:
            return False


class Chariot(Piece):
    """Represents the Chariot. Can move/capture any distance orthogonally.
    Chariots cannot jump over pieces."""

    def __init__(self, player, location):
        """Calls Piece's __init__ with RChariot as the name. R is used as the abbreviation for printing the board."""
        super().__init__(player, 'RChariot', location)

    def can_move(self, square_to):
        """Determines if the Chariot can move to the specified location. Moves/capture any distance orthogonally.
        Chariots cannot jump over pieces."""
        if super().can_move(square_to) is True:
            row_to = int(square_to[1:])
            col_to = ord((square_to[0])) - 97
            row_from = int(super().get_location()[1:])
            col_from = ord(super().get_location()[0]) - 97

            # If within the same row or column, can move.
            if row_to == row_from or col_to == col_from:
                return True
        else:
            return False


class Cannon(Piece):
    """Represents the Cannon. Moves like a chariot, any distance orthogonally. However, to capture, the
    Cannon must jump over a single piece(friend or foe) along the path of attack."""

    def __init__(self, player, location):
        """Calls Piece's __init__ with Cannon as the name."""
        super().__init__(player, 'Cannon', location)

    def can_move(self, square_to):
        """Determines if the Cannon can move to the specified location. Moves any distance orthogonally.
            To capture, Cannon must jump over a single piece(friend or foe) along the path of attack."""
        if super().can_move(square_to) is True:
            row_to = int(square_to[1:])
            col_to = ord((square_to[0])) - 97
            row_from = int(super().get_location()[1:])
            col_from = ord(super().get_location()[0]) - 97

            # If within the same row or column, can move.
            if row_to == row_from or col_to == col_from:
                return True
        else:
            return False


class Soldier(Piece):
    """Represents the Soldier. Can only move/capture by advancing one space forward until they cross the river.
    After a Soldier has crossed the river, they may also move and capture one space horizontally.
    Soldiers cannot move backward, and therefore cannot retreat. Once soldiers hit the last rank of the board,
    they may only move horizontally."""

    def __init__(self, player, location):
        """Calls Piece's __init__ with Soldier as the name."""
        super().__init__(player, 'Soldier', location)

    def can_move(self, square_to):
        """Determines if the Soldier can move to the specified location. Moves one direction forward. Can move
        horizontally if the river has been crossed."""
        player = self.get_player()
        if super().can_move(square_to) is True:
            row_to = int(square_to[1:])
            col_to = ord((square_to[0])) - 97
            row_from = int(super().get_location()[1:])
            col_from = ord(super().get_location()[0]) - 97

            # Horizontal movement if past the river
            if player == 'red' and row_from > 5:
                if row_to == row_from and abs(col_to - col_from) == 1:
                    return True

            # Vertical movement, cannot retreat
            if player == 'red':
                if col_to == col_from and (row_to - row_from) == 1:
                    return True

            # Horizontal movement if past the river
            if player == 'black' and row_from <= 5:
                if row_to == row_from and abs(col_to - col_from) == 1:
                    return True

            # Vertical movement, cannot retreat
            if player == 'black':
                if col_to == col_from and (row_to - row_from) == -1:
                    return True
        else:
            return False


game = XiangqiGame()
move_result = game.make_move('c1', 'e3')
black_in_check = game.is_in_check('black')
game.make_move('e7', 'e6')
state = game.get_game_state()
