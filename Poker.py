import random
import sys

class poker:
    
    balances = {"Guest": 1000, "Finny827": 10000, "Guest2": 500}
    suits = ["♣", "♦", "♥", "♠"]
    cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

    def __init__(self):
        s = input("Enter your username: ")
        with open('database.txt', 'r') as file:
            for line in file.readlines():
                username, balance = line.strip().split(',')
                if username == s:
                    self.username = s
                    self.balance = int(balance)
        self.hand = []
        self.bet_amount = 0

    def deal(self):
        self.hand = []
        while len(self.hand) < 5:
            x = random.randint(0, 12)
            z = random.randint(0,3)
            temp_card = self.cards[x]
            temp_suit = self.suits[z]

            card = temp_card + temp_suit
            if len(self.hand) == 0:
                self.hand.append(card)
                continue
            elif self.check_deck(card) == True:
                continue
            else:
                self.hand.append(card)


    # returns true if card is already in the hand and false otherwise
    def check_deck(self, card):
        if len(self.hand) == 0:
            return False
        for i in range(len(self.hand)):
            if self.hand[i] == card:
                return True
            
        return False
    def print_cards(self):
        x = ''
        for i in range(len(self.hand)):
            x += self.hand[i] + ' '
        print(x)

    def start_bet(self):
        if self.balance == 0:
            self.change_balance()
            sys.exit(1)
        print('Balance: ' + str(self.balance))
        a = (input('Ready to play[y/n]?'))
        if a == 'y':
            self.balance = int(self.balance)
            self.bet_amount = input('Enter a bet:')
            self.bet_amount = int(self.bet_amount)
            self.balance = self.balance - self.bet_amount

        elif a == 'n':
            self.change_balance()
            print('Come Back Soon!')
            sys.exit(1)

    def new_card(self):
        while True:
            x = random.randint(0, 12)
            z = random.randint(0,3)
            temp_card = self.cards[x]
            temp_suit = self.suits[z]

            card = temp_card + temp_suit
            if self.check_deck(card) == True:
                continue
            else:
                return card



    def play_poker(self):
        print("After you make your bet cards will be dealt in hands of 5 cards")
        print("For each card enter H for hold and N for a new card")
        self.start_bet()
        self.deal()
        self.print_cards()
        line = sys.stdin.readline().split()
        for i in range(len(line)):
            if line[i] == 'N':
                self.hand[i] = self.new_card()
        self.print_cards()
        self.hand = sorted(self.hand)
        self.outcome()
        self.balance += self.bet_amount
                
    def outcome(self):
        hand_suits = []
        hand_values = []
        for card in self.hand:
            hand_values.append(card[:-1])
            hand_suits.append(card[-1])

        # check for flush
        if len(set(hand_suits)) == 1:
            # check for straight flush
            values = sorted(hand_values, key=lambda x: self.cards.index(x))
            if values == ['10', 'J', 'Q', 'K', 'A']:
                self.balance += self.bet_amount * 250
                print("Royal flush!")
            elif self.is_consecutive(values):
                self.balance += self.bet_amount * 50
                print("Straight flush!")
            else:
                self.balance += self.bet_amount * 6
                print("Flush!")
        
        # check for straight
        elif self.is_consecutive(sorted(hand_values, key=lambda x: self.cards.index(x))):
            self.balance += self.bet_amount * 4
            print("Straight!")
        
        # check for four of a kind
        elif len(set(hand_values)) == 2 and (hand_values.count(hand_values[0]) == 1 or hand_values.count(hand_values[0]) == 4):
            self.balance += self.bet_amount * 25
            print("Four of a kind!")
        
        # check for full house
        elif len(set(hand_values)) == 2:
            self.balance += self.bet_amount * 8
            print("Full house!")
        
        # check for three of a kind
        elif len(set(hand_values)) == 3 and (hand_values.count(hand_values[0]) == 1 or hand_values.count(hand_values[2]) == 1):
            self.balance += self.bet_amount * 3
            print("Three of a kind!")
        
        # check for two pairs
        elif len(set(hand_values)) == 3:
            pairs = [v for v in hand_values if hand_values.count(v) == 2]
            if len(pairs) == 2:
                self.balance += self.bet_amount * 2
                print("Two pairs!")
        
        # check for one pair
        elif len(set(hand_values)) == 4:
            self.balance += self.bet_amount
            print("One pair!")
        
        # otherwise, it's a high card hand
        else:
            self.balance = self.balance - self.bet_amount
            print("Loser!")
    
    def is_consecutive(self, values):
        return all(self.cards.index(values[i]) + 1 == self.cards.index(values[i+1]) for i in range(len(values)-1))

    def change_balance(self):
        lines = []
        with open('database.txt', 'r') as file:
            for line in file.readlines():
                username, balance = line.strip().split(',')
                if username == self.username:
                    # Update the balance
                    balance = self.balance
                lines.append(f"{username},{balance}\n")
        
        with open('database.txt', 'w') as file:
            file.writelines(lines)

game = poker()
while True: 
    game.play_poker()


