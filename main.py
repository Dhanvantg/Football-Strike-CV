import pygame
import random
import cv2
import mediapipe as mp
import pyautogui

# TODO
# Time-Induced Difficulty
# Sound
# High-Score7
# Better UI

class Mygame():
    def main(self):

        screen_w, screen_h = pyautogui.size()
        cam = cv2.VideoCapture(1)
        pyautogui.FAILSAFE = False
        pose = mp.solutions.pose.Pose()
        old_x, old_y = 0, 0

        # inital speed
        Xspeed = 15
        Yspeed = 30
        livesinit = 5

        paddlespeed = 30
        points = 0
        bgcolor = 0, 0, 0  # black
        size = width, height = 1024, 750

        # initalizing the pygame engine
        pygame.init()
        screen = pygame.display.set_mode(size)

        # creating game objects
        paddle = pygame.image.load('man.png')
        paddlerect = paddle.get_rect()

        ball = pygame.image.load('ball.png')
        ballrect = ball.get_rect()

        #sound = pygame.mixer.Sound('interact.wav')
        #sound.set_volume(10)

        bg = pygame.image.load('bggame1.jpg')

        # arranging the variables for game loop
        paddlerect = paddlerect.move((paddlerect.right / 2), height-125)
        ballrect = ballrect.move(width / 2, height / 2)
        xspeed = Xspeed
        yspeed = Yspeed
        lives = livesinit
        clock = pygame.time.Clock()
        pygame.key.set_repeat(1, 30)
        pygame.mouse.set_visible(0)

        while True:
            clock.tick(500)  # 40 fps

            # events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        exit()

            _, frame = cam.read()
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            output = pose.process(rgb_frame)
            landmarks = output.pose_landmarks
            frame_h, frame_w, _ = frame.shape

            if landmarks:
                landmark = landmarks.landmark
                for id, mark in enumerate([landmark[0]]):
                    x = int(mark.x * screen_w)
                    y = int(mark.y * screen_h)
                    #cv2.circle(frame, (int(mark.x * frame_w), int(mark.y * frame_h)), 3, (0, 255, 0))
                    #if abs(x - old_x) + abs(y - old_y) > 10:
                    paddlerect.centerx = (x*width+paddlerect.right/2)/screen_w
                    old_x, old_y = x, y
            #cv2.imshow('Hover Mouse!', frame)
            #cv2.waitKey(1)


        # check if paddle hit ball
            if paddlerect.top <= ballrect.bottom <= paddlerect.bottom and \
                    ballrect.right >= paddlerect.left and \
                    ballrect.left <= paddlerect.right:

                yspeed = -yspeed
                points += 1
                #sound.play(0)

                # offset
                offset = ballrect.center[0] - paddlerect.center[0]

                # offset>0 means ball hits the RHS of paddle
                # offset<0 means ball hits the LHS of paddle

                if offset > 0:
                    if offset > 30:
                        xspeed = 7
                    elif offset > 23:
                        xspeed = 6
                    elif offset > 17:
                        xspeed = 5
                else:
                    if offset < -30:
                        xspeed = -7
                    elif offset < -23:
                        xspeed = -6
                    elif offset < -17:
                        xspeed = -5

            # move the ball around the screen
            ballrect = ballrect.move(xspeed, yspeed)
            if ballrect.left < 0 or ballrect.right > width:
                xspeed = -xspeed
                #sound.play(0)
            if ballrect.top < 0:
                yspeed = -yspeed
                #sound.play(0)

            # Check the ball has gone past bat
            if ballrect.top > height:
                lives -= 1

                # start a newball
                xspeed = Xspeed
                rand = random.random()
                if random.random() > 0.5:
                    xspeed = -xspeed
                yspeed = Yspeed
                ballrect.center = width * random.random(), height / 3.5
                # Lives exhausted
                if lives == 0:
                    msg = pygame.font.Font(None, 70).render("Game Over", True, (0, 255, 255), bgcolor)
                    msgrect = msg.get_rect()
                    msgrect = msgrect.move(width / 2 - (msgrect.center[0]), height / 3)
                    screen.blit(msg, msgrect)
                    screen.blit(bg, (500, 500))
                    pygame.display.flip()

                    while True:
                        restart = False
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                exit()
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_ESCAPE:
                                    exit()
                                if not (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):
                                    restart = True
                        if restart:
                            screen.fill(bgcolor)
                            lives = livesinit
                            points = 0
                            break


            # Update every objects in the game
            screen.fill(bgcolor)
            screen.blit(bg, (0, 0))

            scoretext = pygame.font.Font(None, 40).render(str(points), True, (0, 255, 255), bgcolor)
            scoretextrect = scoretext.get_rect()
            scoretextrect = scoretextrect.move(width - scoretextrect.right, 0)
            screen.blit(scoretext, scoretextrect)
            screen.blit(ball, ballrect)
            screen.blit(paddle, paddlerect)

            pygame.display.flip()

if __name__ == '__main__':
    br = Mygame()
    br.main()