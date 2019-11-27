# tictactoe-player
Reinforcement learning TicTacToe playing in pure Python.

It uses temporal difference to learn a value function for the different states in the finite state space. That is, it updates a `dict` that sees if a move is good.

Some of this code is not well-written. But I'm not planning on improving it significantly.

I think the decay rate is too high. It remains ~0.3 at the end of 10000 plays. You may set it lower. Or you may set the number of games for training higher. Or both.
