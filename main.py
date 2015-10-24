import random
import copy

WIN = [set([1,2,3]), set([4,5,6]), set([7,8,9]),
       set([1,4,7]), set([2,5,8]), set([3,6,9]),
       set([1,5,9]), set([3,5,7])]
PLAYER = [{"name":"X","state":set([])},{"name":"O","state":set([])}]
BOARD = set([1,2,3,4,5,6,7,8,9])


#PLAYER = [{"name":"O","state":set([2,3,4])},{"name":"X","state":set([1,5,7])}]
#BOARD = set([6,8,9])

def pick(pls,board,n):
  if n in board:
    board.remove(n)
    pls.add(n)
    return True 
  else:
    return False

def get_next_player(cur):
  if cur == "X":
    return "O"
  else:
    return "X"

def check_win(pls):
  for w in WIN:
    if w.issubset(pls):
      return True
  else:
    return False

def print_board(player, board):
  s = ""
  for i in range(1,10):
    if i in board:
      s += "_ " 
    else: 
      for pl in player:
        if i in pl["state"]:
          s +=  "%s "%(pl["name"])
    if i%3 == 0:
      s +=  "\n"
  print s


def random_pick(pls,board):
  while not (pick(pls,board,int(1+random.random()*9) )):
    pass

def player_pick(pls,board):
  while True:
    x = input(">")
    if pick(pls,board,x):
      break;
    else:
      print "cannot place at %s"%(x)


def search_pick(me,pl,board):
  def search_state_rec(me,cur,state):
    #print "me=%s,cur=%s"%(me,cur)
    if check_win(state[cur]):
      if me == cur:
        return 1.
      else:
        return -1.
    elif len(state["board"]) == 0:
      return 0.
    else:
      score_max, score_min = -2.,2.
      nx = get_next_player(cur)
      for b in state["board"]:
        state_next = copy.deepcopy(state)
        assert pick(state_next[nx],state_next["board"],b)
        score = search_state_rec(me,nx,state_next)
        #print "nx=%s, b=%s, score=%s"%(nx, b, score)
        if me != cur and score > score_max:
          score_max = score
        elif me == cur and score < score_min:
          score_min = score
      if me != cur:
        return score_max 
      else:
        return score_min 

  state = {
    pl[0]["name"]: pl[0]["state"],
    pl[1]["name"]: pl[1]["state"],
    "board":board
  }
  #return search_state_rec(me,cur,state)
  score_max = -2.
  to_pick = 0
  for b in state["board"]:
    state_next = copy.deepcopy(state)
    assert pick(state_next[me],state_next["board"],b)
    score = search_state_rec(me,me,state_next)
    print "me=%s, b=%s, score=%s"%(me, b, score)
    if score > score_max:
      score_max = score
      to_pick = b
    if score == score_max and random.random() > 0.7:
      to_pick = b
  assert pick(state[me],board,to_pick)
    

 
      
def main():
  PLAYING = True 
  print_board(PLAYER,BOARD)
  while PLAYING:
    for pl in PLAYER:
      if pl["name"] == "X":
        search_pick("X", PLAYER, BOARD)
        #random_pick(pl["state"],BOARD) 
      else:
        search_pick("O", PLAYER, BOARD)
        #player_pick(pl["state"],BOARD)
      print_board(PLAYER,BOARD)
      if check_win(pl["state"]):
        print "winner is %s"%(pl["name"])
        PLAYING = False
        break
      if len(BOARD) == 0:
        print "tie"
        PLAYING = False
        break
        
if __name__ == "__main__":
  main()
