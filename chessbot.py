#!/usr/bin/python3.8
# Main file to run for function with lichess.org
# Most code is borrowed from berserk documentation
# and adjusted for use in this project
import berserk
import threading
import chess
import testgame

# Game class used for accepting challenges and streaming ongoing games
class Game(threading.Thread):
    def __init__(self, client, game_id, **kwargs):
        super().__init__(**kwargs)
        self.game_id = game_id
        self.client = client
        self.stream = client.bots.stream_game_state(game_id)
        self.current_state = next(self.stream)
        self.mess = 1

    # Responds to move with one of its own or responds to chat message
    def run(self):
        for event in self.stream:
            if event['type'] == 'gameState':
                self.handle_state_change(event)
            elif event['type'] == 'chatLine':
                self.handle_chat_line(event)

    # Makes a move if the game state has changed
    def handle_state_change(self, game_state):
        # Creates the board locally from list of moves played in the game
        board = chess.Board()
        moves = game_state['moves']
        move_list = moves.split()
        for m in move_list:
            board.push(chess.Move.from_uci(m))
            
        if board.turn == chess.BLACK:
            print("Generating move...")
            client.bots.make_move(self.game_id, testgame.getMove2(board))

    # Says one simple message in response to chat
    def handle_chat_line(self, chat_line):
        if self.mess == 1:
            client.bots.post_message(self.game_id, 'Prepare to lose')
            self.mess = 0

# Function to be adjusted if type of game wants to be evaluated before accepting
def should_accept(self, chal=""):
    return True

if __name__ == "__main__":
    # Key for bot API (please don't abuse...)
    session = berserk.TokenSession("t7b1Sb9Zp788Fp5b")
    client = berserk.Client(session=session)

    # Used to show that the program has successfully connected to bot with API
    print(client.account.get_email())

    # Loops through incoming events the bot recieves
    for event in client.bots.stream_incoming_events():
        # Accepts any challenges
        if event['type'] == 'challenge':
            if should_accept(event):
                client.bots.accept_challenge(event['challenge']['id'])
        # If a game has started we launch a Game object to play the moves
        elif event['type'] == 'gameStart':
            game = Game(client, event['game']['id'])
            game.run()
