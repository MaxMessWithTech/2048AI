# 2048 Exhaustive Search Algorithm (AI of sorts) DISCLAIMER: DOES NOT WORK THAT WELL
Created by Max Miller

Uses python and pygame to display the actual 2048 window [ Found in the classes.py and main.py files ] and an Exhaustive Search Algorithm to actually decide the next move [ Found in the algo.py file ]

## About the author
My name is Max Miller and I'm a high school student (currently a freshman as I write this). I've been working on this in my free time at school, so I haven't had time to put too much effort into this. Please keep in mind that this isn't intended to be a perfect algorithm, I've made this all on my own without the help of Google, so it's not based on a great eval algorithm.

## Algorithm Design [ algo.py ]

Basically it uses a exhaustive search to go through every different possibility of what can happen as a result of a move and finds the best one. I tried to add something that would find the average of the evaluation of the set of moves, but for some reason that I haven't been able to discern yet, it makes the performance worse. Additionally, it keeps track of the evaluation of every depth so that it can throw out evaluations that are lower and save some processioning time. Unfortunately this time saver was not enough to allow for a depth higher then 3, there is a threaded version of this in the mainThread.py file, but it still is ridiculously slow and wasn't worth the effort in my opinion 

## Perspective Improvements
Right now I'm focusing on trying to improve the evaluation function so it more accurately predicts the outcome