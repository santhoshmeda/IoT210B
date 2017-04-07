# quiz.py

# Allows a student to take a quiz. There must be a quiz master
from sense_hat import SenseHat
import curses

USER_NAME = "user"
PWD       = "pwd"

answer = 'A'
MIN_ORD  = ord('A')
MAX_ORD  = ord('D')

# add or subtract to the answer
def quiz_add_answer(answer, value):

  # add and wrap
  n = ord(answer)
  n = n + value

  # keep in range
  if n < MIN_ORD:
    n = MIN_ORD
  if n > MAX_ORD:
    n = MAX_ORD

  # return 'A' - 'D'
  return chr(n)


# curses is used to prevent iPad joystick from causing system issues
# as the joystick is mapped to up/down/left/right/enter
stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(1)

# startup shows a 'Q' on a blue background
sense = SenseHat()
sense.show_letter("Q", text_colour=[80,80,80], back_colour=[0,80,80])

# get keys
while True:
  event = sense.stick.wait_for_event()

  # get keyboard input, returns -1 if none available
  c = stdscr.getch()

  # up/down = A-D, Enter = select answer
  dir = str(event[1])
  if str(event[2]) == 'pressed':

    if dir == 'up':
      answer = add_answer(answer, 1)

    elif dir == 'down':
      answer = add_answer(answer, -1)

    elif dir == 'left':
      msg = str(score_right) + '/' + str(score_max)
      sense.show_message(msg)

    # elif dir == 'right':

    elif dir == 'push':
      msg = str(score_right) + '/' + str(score_max)
      sense.show_message(msg)

# done with curses, back to a normal terminal
curses.nocbreak(); stdscr.keypad(0); curses.echo()
curses.endwin()
