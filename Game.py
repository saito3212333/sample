import Deck
import Player

class Game:
	def __init__(self):
		name1 = input("p1 name")
		name2 = input("p2 name")
		self.deck = Deck.Deck()
		self.p1 = Player.Player(name1)
		self.p2 = Player.Player(name2)
		
	def wins(self,winner):
		w = f"{winner} wins this round"
		print(w)
	
	def draw(self,p1n,p1c,p2n,p2c):
		d = f"{p1n} draw {p1c} {p2n} drew {p2c}"
		print(d)
		
				
	def play_game(self):
		cards = self.deck.cards
		print("beggining War")
		while len(cards) >= 2:
			m = "q to quit. Any key to play:"
			response = input(m)
			if response == "q":
				break
			p1c = self.deck.rm_card()
			p2c = self.deck.rm_card()	
			p1n = self.p1.name
			p2n = self.p2.name
			self.draw(p1n,p1c,p2n,p2c)
			if p1c > p2c:
				self.p1.wins +=1
				self.wins(self.p1.name)
			else:
				self.p2.wins +=1
				self.wins(self.p2.name)
		
		win = self.winner(self.p1,self.p2)
		print(f"War is over.{win} wins")
		
	def winner(self,p1,p2):
		if p1.wins > p2.wins:
			return p1.name
		if p1.wins < p2.wins:
			return p2.name
		return "It was a tie!"
		
game = Game()
game.play_game()
