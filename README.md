# tictactoe-player
Reinforcement learning TicTacToe playing in pure Python.

It uses temporal difference to learn a value function for the different states in the finite state space. That is, it updates a `dict` that sees if a move is good.

Some of this code is not well-written. But I'm not planning on improving it significantly.

You can set the decay rate higher and the number of games for training higher for better performance. You can also explore more frequently.
