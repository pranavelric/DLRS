import tkinter
import PIL.Image
import PIL.ImageTk
import sys
from cv2 import cv2
from functools import partial
import time
import threading
import imutils


def capture():
    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi', fourcc, 20.0, (650, 360))

    # loop runs if capturing has been initialized.
    while(cap.isOpened()):

        ret, fam = cap.read()
        if ret == True:
            out.write(fam)
            cv2.imshow('Original', fam)

            if cv2.waitKey(1) & 0xFF == ord('a'):
                break
        else:
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()


stream = cv2.VideoCapture('output.avi')
flag = True


def play(speed):

    stream = cv2.VideoCapture('output.avi')
    print(f'speed is {speed}')
    global flag
    frame1 = stream.get(cv2.CAP_PROP_POS_FRAMES)
    stream.set(cv2.CAP_PROP_POS_FRAMES, frame1 + speed)
    grabbed, frame = stream.read()
    # if not grabbed:
    #     exit()

    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, anchor=tkinter.NW, image=frame)
    if flag:
        canvas.create_text(120, 25, fill='green',
                           font='Times 20 italic bold', text="Decision Pending")
    flag = not flag


def pending(decision):
    # display firest decison pending,wait for one sec,then display sponsor,wait 1.5 sec,then display anser
    frame = cv2.cvtColor(cv2.imread('decision.png'), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.create_image(0, 0, anchor=tkinter.NW, image=frame)
    canvas.image = frame

    time.sleep(1)

    frame = cv2.cvtColor(cv2.imread('693479.jpg'), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, anchor=tkinter.NW, image=frame)

    time.sleep(2)
    img = cv2.imread(
        'out.png') if decision == 'out' else cv2.imread('notout.png')
    frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, anchor=tkinter.NW, image=frame)


def out():
    # run pending funtion using thread
    thread = threading.Thread(target=pending, args=("out",))
    thread.daemon = 1
    thread.start()
    print("Player is out")


def notOut():
    # run pending funtion using thread
    thread = threading.Thread(target=pending, args=("not out",))
    thread.daemon = 1
    thread.start()
    print("Player is  not out")


def exit():
    print("Closing DLRS system")
    time.sleep(1)
    sys.exit()


SET_WIDTH = 650
SET_HEIGHT = 368

window = tkinter.Tk()
window.title("Pranav 3rd Empire review")
window.configure(bg='black')

img = cv2.imread('background1.jpeg')
cv_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
cv_img = imutils.resize(cv_img, width=SET_WIDTH, height=SET_HEIGHT)
canvas = tkinter.Canvas(window, width=SET_WIDTH, height=SET_HEIGHT)
photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))
# canvas.image = photo
image_on_canvas = canvas.create_image(0, 0, anchor=tkinter.NW, image=photo)
canvas.pack()

# buttons to control playback
btn = tkinter.Button(window, text="<< Previous(fast)",
                     width=92, bg='blue', command=partial(play, -25))
btn.pack()

btn = tkinter.Button(window, text="< Previous(Slow)",
                     width=92, command=partial(play, -2))
btn.pack()

btn = tkinter.Button(window, text="Next(fast) >>",
                     width=92, command=partial(play, 25))
btn.pack()

btn = tkinter.Button(window, text="Next(slow) >",
                     width=92, command=partial(play, 2))
btn.pack()

btn = tkinter.Button(window, text="Give Out", width=92, command=out)
btn.pack()

btn = tkinter.Button(window, text="Give Not Out", width=92, command=notOut)
btn.pack()


btn = tkinter.Button(window, text="Capture", width=92,
                     bg='yellow', fg='black', command=capture)
btn.pack()


btn = tkinter.Button(window, text="Exit", width=92,
                     bg='red', fg='black', command=exit)
btn.pack()

window.mainloop()
