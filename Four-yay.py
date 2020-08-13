import pygame
import math, cmath
from time import sleep
import random


def a(path, t, n):
    phase = -1 * n * 2 * math.pi * 1j * t / (len(path))
    unit_pos = cmath.exp(phase)
    tp = (complex(path[t][0], path[t][1]) * unit_pos)
    return tp

def intg(path, n):
    tot = 0
    for i in range(len(path)):
        tot += a(path, i, n)

    tot /= len(path)
    
    return tot

pygame.init()

win_wd = 1080
win_ht = 720
win = pygame.display.set_mode((win_wd,win_ht))
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
clock = pygame.time.Clock()
font_1 = pygame.font.Font(r"C:\WINDOWS\Fonts\ARIALN.TTF", 36)
trace = pygame.Rect(win_wd - 100, 20, 100, 50)
prec = pygame.Rect(win_wd - 100, 100, 100, 50)
reset = pygame.Rect(win_wd - 100, 180, 100, 50)

def draw_circle(win, center, radius):
    try:
        pygame.draw.circle(win, WHITE, (center[0], center[1]), radius, 2)
    except ValueError:
        pygame.draw.circle(win, WHITE, (center[0], center[1]), 0, 0)

def draw_line(win, radius, angle, start):
    end = (int(radius * math.cos(angle) + start[0]), int(radius * math.sin(angle) + start[1]))
    pygame.draw.line(win, WHITE, start, end, 2)
    return end


run = True
steps = 0
endpts = []
precision = 1
step_size = 0.05

start = True
drawing = False
tracing = True

while run:
    clock.tick(24)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if trace.collidepoint(event.pos) and not start:
                if tracing == True:
                    tracing = False
                elif tracing == False:
                    tracing = True

            elif prec.collidepoint(event.pos) and not drawing:
                pass

            elif reset.collidepoint(event.pos) and not drawing:
                pass

            else:
                drawing = True
                start = False
                win.fill(BLACK)
                path = [event.pos]

        elif event.type == pygame.MOUSEBUTTONUP:
            if trace.collidepoint(event.pos) and not drawing:
                pass

            elif reset.collidepoint(event.pos) and not drawing:
                win.fill(BLACK)
                steps = 0
                endpts = []
                precision = 1

                start = True
                drawing = False
                tracing = True

            elif prec.collidepoint(event.pos) and not drawing:
                precision += 1
                coeffs = []
                steps = 0
                endpts = []
                for i in range(precision):
                    if i % 2 == 0:
                        coeffs.append(intg(path, -(i//2)))
                    elif i % 2 == 1:
                        coeffs.append(intg(path, (i+1)//2))

                angle = [cmath.phase(c) for c in coeffs]
                radius = [int(abs(c)) for c in coeffs]
            
            else:
                drawing = False
                path = [(i[0] - win_wd//2, i[1] - win_ht//2) for i in path]
                coeffs = []
                steps = 0
                endpts = []
                for i in range(precision):
                    if i % 2 == 0:
                        coeffs.append(intg(path, -(i//2)))
                    elif i % 2 == 1:
                        coeffs.append(intg(path, (i+1)//2))

                angle = [cmath.phase(c) for c in coeffs]
                radius = [int(abs(c)) for c in coeffs]

    if drawing:
        path.append(pygame.mouse.get_pos())
        pygame.draw.line(win, WHITE, path[-1], path[-2], 1)
        
    if not drawing and not start:
        win.fill(BLACK)
        end = (win_wd//2, win_ht//2)
        for i in range(precision):
            if i % 2 == 0:
                angle_change = -step_size * (i//2)
            elif i % 2 == 1:
                angle_change = step_size * ((i+1)//2)

            draw_circle(win, end, radius[i])
            end = draw_line(win, radius[i], angle[i], end)
            angle[i] += angle_change

        pygame.draw.rect(win, WHITE, trace)
        win.blit(font_1.render("TRACE", True, BLACK), trace)

        pygame.draw.rect(win, WHITE, prec)
        win.blit(font_1.render("PREC", True, BLACK), prec)

        pygame.draw.rect(win, WHITE, reset)
        win.blit(font_1.render("RESET", True, BLACK), reset)
        
        endpts.append(end)
        steps += 1
        if steps >= 2*math.pi//step_size:
            steps = 0
            endpts = []
        if tracing:
            for i in range(1, len(endpts)):
                pygame.draw.line(win, GREEN, endpts[i], endpts[i-1], 2)
            
    
    pygame.display.update()


