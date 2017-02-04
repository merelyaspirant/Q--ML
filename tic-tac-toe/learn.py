from World import *
import ast
import sys

MAX_LPLAYS = 50000
class Player:
	def __init__(self, P):
		self.id = P
		self.World_score = 5.0
		self.Q = {}
		self.states = []
		self.actions = []
		self.MAX_states = pow(3,9)
		self.MAX_actions = 9
		self.walk_reward = -0.1
		self.rec_states = 0
		self.rec_state = []
		self.last_s = 0
		self.last_a = 0
		if P == 1:
			self.sym = 'X'
		else:
			self.sym = '0'
	
	def reset(self):
		self.World_score = 5.0
		self.rec_states = 0
		self.rec_state = []
		self.last_s = 0
		self.last_a = 0
	
	def save_state(self, s, a):
		temp = [s,a]
		self.rec_state.append(temp)
		self.rec_states += 1
		
	def initialize_train(self):
		for i in range(self.MAX_states):
			self.states.append(i)
		for j in range(self.MAX_actions):
			self.actions.append(j)
		for k in self.states:
			for l in self.actions:
				self.Q[k,l] = 10.0

	def max_Q(self,s, b):
		act, val = (None, None)
		for j in self.actions:
			x = j/3
			y = j%3
			if b.fields[x,y] is '.':
				if val is None or self.Q[s,j] > val:
					act = j
					val = self.Q[s,j]
		return act,val

	def update_Q(self, s, a, r, future_val, alpha, discount):
		self.Q[s,a] = self.Q[s,a] + alpha*(r + discount * future_val - self.Q[s,a])
#		self.Q[s,a] = self.Q[s,a] + alpha*(r + discount * future_val)

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

slow_down = True
def calc_move(g, P1, P2):
	global slow_down
	alpha = 0.7
	discount = 0.2

	P = P1
	reverse = 1
	plays = 0
	while plays < MAX_LPLAYS:
		s1 = get_state(g.board)
		act, val = P.max_Q(s1, g.board)
		s2 = P.next_state(s1, act) #if next state is won or tied, nothing to do with s2
		x = act/3
		y = act%3
#		print "inside calc move \n",x,y
		res = g.move(P.sym, x, y)

		P.save_state(s1, act)

		if res is 'tied':
			r = 0
			future_val = 0.5
			for m in range(2):
				if m == 0:
					P = P1
				else:
					P = P2
				for k in range(P.rec_states):
					[s_curr, act_curr] = P.rec_state[P.rec_states - 1 - k]
					if k == 0:
						P.update_Q(s_curr, act_curr, r, future_val, alpha, discount)
					else:
						[s_last, act_last] = P.rec_state[P.rec_states - k]
						future_val = P.Q[s_last, act_last]
						P.update_Q(s_curr, act_curr, r, future_val, alpha, discount)

			if (plays % 700) == 0:
				print "plays" , plays
				if discount < 1:
					discount += 0.01


			if slow_down == True:
				print "iter %d,discount %f %s Match Tied, Score %f\n" % (plays, discount, P.sym, P.World_score)
			P1.reset()
			P2.reset()
			if (plays % 2) == 0:
				if reverse:
					reverse = 0
					P = P2
				else:
					reverse = 1
					P = P1
#			sleep(1)
			plays += 1

		elif res is 'won':
			r = 0.5
			m = 0
			future_val = 1.0

			while m < 2:
				for k in range(P.rec_states):
					[s_curr, act_curr] = P.rec_state[P.rec_states - 1 - k]
					if k == 0:
						P.update_Q(s_curr, act_curr, r, future_val, alpha, discount)
					else:
						[s_last, act_last] = P.rec_state[P.rec_states - k]
						future_val = P.Q[s_last, act_last]
						P.update_Q(s_curr, act_curr, r, future_val, alpha, discount)

				if P is P1:
					P = P2
				else:
					P = P1
				future_val = -1.0
				r = 0
				m += 1
			if (plays % 700) == 0:
				print "plays" , plays
				if discount < 1:
					discount += 0.01

			if slow_down == True:
				print "iter %d, %s Match Won, Score %f discount %f\n" % (plays, P.sym, P.World_score, discount)
				for i in P1.actions:
					print P1.Q[0,i]

				for i in P2.actions:
					print P2.Q[0,i]
		
			P1.reset()
			P2.reset()

			if (plays % 2) == 0:
				if reverse:
					reverse = 0
					P = P2
				else:
					reverse = 1
					P = P1
#			sleep(0.5)
			plays += 1
			

		else:
			if P is P1:
				P = P2
			else:
				P = P1


		if slow_down == True:
			sleep(0.25)
	
	fout = open('Q1-mat', 'w')
	fout.write(str(P1.Q))
	print "DATA1 written"
	fout.close()

	fout = open('Q2-mat', 'w')
	fout.write(str(P2.Q))
	print "DATA2 written"
	fout.close()


def enjoy_game(g, Q1, Q2):
	more = True

	while more:
		print "Enter 1 to play 1st or 2 for 2nd or enter to quit\n"
		d = int(raw_input())
		if d == 1:
			P = Player(1)
			g.myturn = True
			g.player_sym = 'X'
			C = Player(2)
			C.initialize_train()
			C.Q = Q2
			g.myturn = True
		elif d == 2:
			P = Player(2)
			g.myturn = False
			g.player_sym = '0'
			C = Player(1)
			C.initialize_train()
			C.Q = Q1
		else:
			print "EXIT\n"
			sys.exit()
		
		while True:
			if g.myturn == False:
				if g.match_over == True:
					g.match_over = False
					break;
				print "Computer Turn\n"
				s1 = get_state(g.board)
				act, val = C.max_Q(s1, g.board)
				x = act/3
				y = act%3
				res = g.move(C.sym, x, y)
				if res is 'won':
					print "%s WON\n" % (C.sym)
					break
				elif res is 'tied':
					print "Match TIED\n"
					break
				else:
					g.myturn = True

def play():
  print "Play"
  print "LOADING Q-MATRIX ...."
  with open('Q2-mat','r') as inf:
    Q2 = ast.literal_eval(inf.read())
  inf.close()
  with open('Q1-mat','r') as inf:
    Q1 = ast.literal_eval(inf.read())
  inf.close()

  g = GUI('play')

  t1 = threading.Thread(target=enjoy_game, args=(g, Q1, Q2, ))
  t1.daemon = True
  t1.start()

  g.mainloop()

def take_input():
	global slow_down
	while True:
		l = str(raw_input())
		if l is 's':
			slow_down = True
		elif l is 'f':
			slow_down = False
		else:
			print 'input s for slowing down & f to paceup'
		
def train():
  print "Train\n"
  P1 = Player(1)
  P2 = Player(2)
  P1.initialize_train()
  P2.initialize_train()

  inp = str(raw_input("enter l to load models\n"))
  if inp is 'l':
    with open('Q1-mat','r') as inf:
      P1.Q = ast.literal_eval(inf.read())
    inf.close()
    with open('Q2-mat','r') as inf:
      P2.Q = ast.literal_eval(inf.read())
    inf.close()
    
  g = GUI('train')
  t1 = threading.Thread(target=calc_move, args=(g, P1, P2, ))
  t1.daemon = True
  t1.start()
  t2 = threading.Thread(target=take_input)
  t2.daemon = True
  t2.start()

  g.mainloop()

if __name__ == '__main__':

  print "Enter 't' to train & 'r' to play"
  ch = str(raw_input('-->'))
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


