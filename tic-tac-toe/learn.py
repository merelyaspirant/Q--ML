from World import *

class Player:
	def __init__(self, P):
		self.id = P
		self.World_score = 5.0
		self.Q = {}
		self.states = []
		self.actions = []
		self.MAX_states = pow(3,9)
		self.MAX_actions = 9
		self.walk_reward = -0.4
		self.last_s = 0
		self.last_a = 0
		if P == 1:
			self.sym = 'X'
		else:
			self.sym = '0'

	def initialize_train(self):
		for i in range(self.MAX_states):
			self.states.append(i)
		for j in range(self.MAX_actions):
			self.actions.append(j)
		for k in self.states:
			for l in self.actions:
				self.Q[k,l] = 20.0

	def max_Q(self,s, b):
		act, val = (None, None)
		for j in self.actions:
			x = j/3
			y = j%3
			if b.fields[x,y] is '.':
				if val is None or self.Q[s,j] > val:
					act = j
					val = self.Q[s,j]
		if act == 0:
#			for j in self.actions:
#				print " " , self.Q[s,j]
			print len(self.Q)
			print len(self.actions)
		return act,val

	def update_Q(self, s, a, r, future_val, alpha, discount):
		self.Q[s,a] = self.Q[s,a] + alpha*(r + discount * future_val - self.Q[s,a])


	def next_state(self, s1, a):
		s2 = s1 + self.id*pow(3,a)
		return s2

def get_state(b):
	i = 0
	state = 0
	for x in range(b.size):
		for y in range(b.size):
			if b.fields[x,y] == 'X':
				T = 1
			elif b.fields[x,y] == '0':
				T = 2
			else:
				T = 0
			state = state + T*pow(3,i)
			i += 1
	return state

def calc_move(g, P1, P2):
	alpha = 0.9
	discount = 0.6

	P = P1
	reverse = 1
	while True:
#		print "calc_move\n"
		s1 = get_state(g.board)
#		print "s1 > \n", s1
		act, val = P.max_Q(s1, g.board)
		s2 = P.next_state(s1, act) #if next state is won or tied, nothing to do with s2
		x = act/3
		y = act%3
#		print "inside calc move \n",x,y
		res = g.move(P.sym, x, y)

		P.last_a = act
		P.last_s = s1

		if res is 'tied':
			r = -P.World_score
			P.World_score += P.walk_reward
			r += P.World_score
			future_val = 0.5
			P.update_Q(s1, act, r, future_val, alpha, discount)
			print "Match Tied, Score %f\n", P.World_score
			P1.World_score = P2.World_score = 5.0
			if reverse:
				reverse = 0
				P = P2
			else:
				reverse = 1
				P = P1
#			sleep(1)

		elif res is 'won':
			r = -P.World_score
			P.World_score += 0
			r += P.World_score
			future_val = 1.0
			P.update_Q(s1, act, r, future_val, alpha, discount)
			if P is P1:
				r = -P2.World_score
				P2.World_score += P2.walk_reward
				r += P2.World_score
				future_val = -1
				P2.update_Q(P2.last_s, P2.last_a, r, future_val, alpha, discount)
			else:
				r = -P1.World_score
				P1.World_score += P1.walk_reward
				r += P1.World_score
				future_val = -1
				P1.update_Q(P1.last_s, P1.last_a, r, future_val, alpha, discount)

			print " %s Match Won, Score %f\n" % (P.sym, P.World_score)
			P1.World_score = P2.World_score = 5.0
			if reverse:
				reverse = 0
				P = P2
			else:
				reverse = 1
				P = P1
			sleep(0.5)

		else:
			r = -P.World_score
			P.World_score += P.walk_reward
			r += P.World_score
			future_val ,a = P.max_Q(s2, g.board)
			P.update_Q(s1, act, r, future_val, alpha, discount)
			if P is P1:
				P = P2

			else:
				P = P1
#		print "Q1 %r\n" , Q1
#		print "Q2 %r\n" , Q2
		sleep(0.25)

def calc2_move(g):
	turn = 'X'
	for j in actions:
		x = j/3
		y = j%3
		g.move(turn, x, y)
		sleep(0.5)
		if turn is 'X':
			turn = '0'
		else:
			turn = 'X'

def play():
  print "Play\n"
  g = GUI('play')
  g.mainloop()

def train():
  print "Train\n"
  P1 = Player(1)
  P2 = Player(2)
  P1.initialize_train()
  P2.initialize_train()

  g = GUI('train')
  t = threading.Thread(target=calc_move, args=(g, P1, P2, ))
  t.daemon = True
  t.start()
  g.mainloop()

if __name__ == '__main__':

  print "Enter 't' to train & 'r' to play"
  ch = str(raw_input('-->\n'))
  if ch == 't':
    train()
    print "Model Trained\n"
    if 'yes' in str(raw_input("Enter 'yes' to play\n")):
  	  play()
    else:
      sys.exit()
  elif ch == 'r':
    play()
  else:
    sys.exit()


