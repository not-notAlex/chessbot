#!/usr/bin/python3.8
import berserk
import threading
import chess
import testgame

class Game(threading.Thread):
    def __init__(self, client, game_id, **kwargs):
        super().__init__(**kwargs)
        self.game_id = game_id
        self.client = client
        self.stream = client.bots.stream_game_state(game_id)
        self.current_state = next(self.stream)
        self.mess = 1

    def run(self):
        for event in self.stream:
            if event['type'] == 'gameState':
                self.handle_state_change(event)
            elif event['type'] == 'chatLine':
                self.handle_chat_line(event)

    def handle_state_change(self, game_state):
        b = chess.Board()
        moves = game_state['moves']
        move_list = moves.split()
        for m in move_list:
            b.push(chess.Move.from_uci(m))
        if b.turn == chess.BLACK:
            print("Generating move...")
            client.bots.make_move(self.game_id, testgame.getMove(b))

    def handle_chat_line(self, chat_line):
        if self.mess == 1:
            client.bots.post_message(self.game_id, 'Prepare to lose')
            self.mess = 0

def should_accept(self, chal=""):
    return True

if __name__ == "__main__":
    session = berserk.TokenSession("t7b1Sb9Zp788Fp5b")
    client = berserk.Client(session=session)

    print(client.account.get_email())

    is_polite = True
    for event in client.bots.stream_incoming_events():
        if event['type'] == 'challenge':
            if should_accept(event):
                client.bots.accept_challenge(event['challenge']['id'])
            elif is_polite:
                client.bots.decline_challenge(event['id'])
        elif event['type'] == 'gameStart':
            game = Game(client, event['game']['id'])
            game.run()
