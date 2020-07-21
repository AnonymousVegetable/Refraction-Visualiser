"""
Refraction visualiser

Controls - 'a', 'd' keys change angle of incidence - hold 'space' for finer precision
           '1', '2' keys change refraction index value for top medium
           '9', '0' keys change refraction index value for bottom medium

"""


import pygame
import time
import math
import numpy

pygame.init()

resolution = (1500, 900)

window = pygame.display.set_mode(resolution)

myfont = pygame.font.SysFont('Comic Sans MS', 30)

n1 = 1.000
n2 = 1.000

running = True

i = math.pi/2

aPressed = False
dPressed = False
spacePressed = False


incidenceAngle = (math.pi/2 - i) * 180 / math.pi

while(running):
    for event in pygame.event.get():

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            if event.key == pygame.K_d:
                dPressed = True
            if event.key == pygame.K_a:
                aPressed = True
            if event.key == pygame.K_SPACE:
                spacePressed = True

            if event.key == pygame.K_1:
                n1 += 0.2
            if event.key == pygame.K_2:
                n1 -= 0.2
            if event.key == pygame.K_9:
                n2 += 0.2
            if event.key == pygame.K_0:
                n2 -= 0.2

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                dPressed = False
            if event.key == pygame.K_a:
                aPressed = False
            if event.key == pygame.K_SPACE:
                spacePressed = False
        if event.type == pygame.QUIT:
            running = False

    if aPressed & spacePressed:
        if incidenceAngle > -90:
            i += math.pi / 3600
            incidenceAngle = (math.pi / 2 - i) * 180 / math.pi
            if incidenceAngle < -90:
                incidenceAngle = (-math.pi / 2) * 180 / math.pi
    elif aPressed:
        if incidenceAngle > -90:
            i += math.pi / 360
            incidenceAngle = (math.pi / 2 - i) * 180 / math.pi
            if incidenceAngle < -90:
                incidenceAngle = (-math.pi / 2) * 180 / math.pi


    if dPressed & spacePressed:
        if incidenceAngle < 90:
            i -= math.pi / 3600
            incidenceAngle = (math.pi / 2 - i) * 180 / math.pi

            if incidenceAngle > 90:
                incidenceAngle = (math.pi / 2) * 180 / math.pi
    elif dPressed:
        if incidenceAngle < 90:
            i -= math.pi / 360
            incidenceAngle = (math.pi / 2 - i) * 180 / math.pi

            if incidenceAngle > 90:
                incidenceAngle = (math.pi / 2) * 180 / math.pi

    window.fill(pygame.Color("black"))

    radius = (resolution[1]/2)/numpy.sin(i)




    # Inbound Ray
    origin = [int(resolution[0]/2), 0]
    boundary = [radius * numpy.cos(i) + origin[0], radius * numpy.sin(i) + origin[1]]

    pygame.draw.circle(window, (255, 255, 0), origin, 20, )

    pygame.draw.line(window, (255, 255, 255), (0, resolution[1]/2), (resolution[0], resolution[1]/2))

    #Outbound Ray
    outboundOrigin = boundary

    sinTheta2 = n1 * numpy.sin(incidenceAngle * math.pi / 180) / n2

    scalingFactor = 10000

    if sinTheta2 > 1 or sinTheta2 < -1:              # Reflects upon critical angle
        refractionAngle = (180 - incidenceAngle)


    else:
        refractionAngle = numpy.arcsin(sinTheta2) * 180 / math.pi

    outboundBoundary = (scalingFactor * (numpy.sin(refractionAngle * math.pi / 180)) + outboundOrigin[0],
                        scalingFactor * numpy.cos(refractionAngle * math.pi / 180) + outboundOrigin[1])

    if incidenceAngle < 90 and incidenceAngle > - 90:
        pygame.draw.aaline(window, (0, 0, 255), origin, boundary, 10)
        pygame.draw.aaline(window, (0, 255, 0), outboundOrigin, outboundBoundary, 10)

    n1Text = myfont.render("n = " + str(round(n1, 1)), False, (255, 255, 255))
    window.blit(n1Text, (50,50))
    n2Text = myfont.render("n = " + str(round(n2,1)), False, (255, 255, 255))
    window.blit(n2Text, (50, resolution[1] - 80))
    incText = myfont.render(str(round(incidenceAngle, 1)) + u'\N{DEGREE SIGN}', False, (0, 0, 255))
    window.blit(incText, (resolution[0]/2 + 60, resolution[1]/2 - 50))
    refText = myfont.render(str(round(refractionAngle, 1)) + u'\N{DEGREE SIGN}', False, (0, 255, 0))
    window.blit(refText, (resolution[0]/2 + 60, resolution[1]/2 + 20))


    time.sleep(0.03)

    pygame.display.flip()





