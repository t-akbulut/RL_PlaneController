from operator import ne
from utils import wrap_180
import time
from Plane import *
from utils import *
from Dqn import *

import threading
batch_size = 32

plane = None

if __name__ == "__main__":
    plane = Plane()
    state_size = 5
    action_size = 2
    agent = Dqn(state_size, action_size)
    #thread_logging = threading.Thread(target=handle_logging)
    #thread_logging.start()
    state = plane.get_state()
    while True:
        action = agent.act(state)
        [state,action,new_state,reward] = plane.act(action)
        agent.memorize(state,action,reward,new_state,False)
        print(state,plane.get_reward(state))
        if len(agent.memory) > batch_size:
                agent.replay(batch_size)
    print("Logging OK")
