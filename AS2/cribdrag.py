def xor(a, b):
    #input: two byearrays
    #output: bytearray of their xor
    if len(a) > len(b):
        temp = a
        a = b
        b = temp
    s = []
    for i in range(0, len(a)):
        s.append(a[i] ^ b[i])
    for i in range(len(a), len(b)):
        s.append(b[i])
    return s

def cribpend(a, crib, loc):
    #crib is too small; append it with 0's depending on location
    s = []
    for i in range(0, loc):
        s.append(0)
    for i in range(0, len(crib)):
        s.append(crib[i])
    for i in range(len(crib) + loc, len(a)):
        s.append(0)
    s = s[:len(a)]
    return s

def bit(a):
    #returns bitstring of integer
    s = ""
    while (a != 0):
        if (a % 2 == 0):
            s += "0"
            a /= 2
        else:
            s += "1"
            a -= 1
            a /= 2
    while len(s) < 8:
        s += "0"
    s = s[::-1]
    return s

def s_to_ints(s):
    #convert string to integer list ("bytearray")
    b = []
    for i in range(0, len(s)):
        b.append(ord(s[i]))
    return b
    

def showbytes(a):
    s = ""
    chars = []
    for i in range(65, 91):
        chars.append(i)
    for i in range(97, 123):
        chars.append(i)
    for i in range(44, 47):
        chars.append(i)
    #return string of bytestring
    for i in range(0, len(a)):
        if (a[i] in chars):
            s += chr(a[i])
        elif (a[i] == 0):
            s += " "
        elif (a[i] == 32):
            s += "_"
        else:
            s += "*"
    return s

import pygame
import random
import sys

is_blue = 1
done = 0
x = 30
y = 30
clock = pygame.time.Clock()

p1s = "Seven for the Dwarf-lords in halls of stone."
p2s = "In the land of Mordor where the shadows lie."

#our byte arrays are just integer lists
p1 = s_to_ints(p1s)
p2 = s_to_ints(p2s)
#generate
k = []
for i in range(0, len(p1s)):
    k.append(random.randint(0, 255))

c1 = xor(p1, k)
c2 = xor(p2, k)

f1 = open("ctext0", "rb")
f2 = open("ctext1", "rb")

c1temp = f1.read(400)
c2temp = f2.read(400)

c1 = c1temp[0:44]
c2 = c2temp[0:44]

x = xor(c1, c2)
# b= ""
# for item in x:
#     b += hex(item)
# print(b)
##print showbytes(p1)
##print showbytes(p2)
##print showbytes(c1)
##print showbytes(c2)
##print showbytes(x)


pygame.init()
screen = pygame.display.set_mode((800, 700))
screen.fill((255, 255, 255))
pygame.display.flip()

r = []
is_cap = 0
is_drag = 0
inputting = 0
loc = 0
towrite = 0
while not done:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if (event.pos[0] >= 100 and event.pos[1] >= 390 and event.pos[1] <= 435):
                is_drag = 1
                #start dragging
        if event.type == pygame.MOUSEMOTION and is_drag == 1:
            loc = (event.pos[0] - 100) / 15
            if (loc < 0):
                loc = 0
            if (loc > 43):
                loc = 43
        if event.type == pygame.MOUSEBUTTONUP:
            is_drag = 0
            if (event.pos[0] >= 100 and event.pos[1] >= 390 and event.pos[1] <= 435):
                #override the rest; we don't want to change output
                continue
            charnum = (event.pos[0] - 100)/15
            lineremain = event.pos[1] % 100
            linenum = int((event.pos[1] - 90) / 100)
            charnum = int(charnum)
            if (charnum >= 0 and charnum <= 43 and (lineremain <= 35 or lineremain >= 90) and linenum >= 0 and linenum <= 4):
                towrite = 1
            else:
                towrite = 0
        if event.type == pygame.KEYDOWN and inputting == 1:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                inputting = 0
                continue
            elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                is_cap = 1
            elif event.key == pygame.K_BACKSPACE and len(r) > 0:
                if (is_cap == 1):
                    r = r[:-5]
                else:
                    r = r[:-1]
            else:
                try:
                    this_r = int(event.key)
                    if (is_cap == 1):
                        this_r = max(0, this_r - 32)
                    r.append(this_r)
                except:
                    pass
        if event.type == pygame.KEYDOWN and inputting == 0:
            if (event.key == pygame.K_RETURN):
                inputting = 1
        if event.type == pygame.KEYUP and inputting == 1:
            if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                is_cap = 0
    keys = pygame.key.get_pressed()
##    if keys[pygame.K_BACKSPACE] and len(r) > 0 and inputting == 1:
##        r = r[:-1]
##        clock.tick(15)
            
    screen.fill((255, 255, 255))
    
    myfont = pygame.font.SysFont("Arial", 22, bold=True)
    label = myfont.render("CMPT479 Crib-dragging demo", 1, (0, 0, 0))
    screen.blit(label, (15, 15))
    myfont = pygame.font.SysFont("Arial", 22, italic=True)
    label = myfont.render("Ciphertext 1 (C1):", 1, (0, 125, 0))
    screen.blit(label, (50, 50))
    label = myfont.render("Ciphertext 2 (C2):", 1, (0, 125, 0))
    screen.blit(label, (50, 150))
    label = myfont.render("Xortext (X = C1 XOR C2):", 1, (0, 125, 0))
    screen.blit(label, (50, 250))
    label = myfont.render("Crib (R):", 1, (255, 0, 0))
    screen.blit(label, (50, 350))
    label = myfont.render("Xorcribtext (X XOR R):", 1, (0, 125, 0))
    screen.blit(label, (50, 450))
    myfont = pygame.font.SysFont("monospace", 25)
    label = myfont.render(showbytes(c1), 1, (0, 0, 0))
    screen.blit(label, (100, 100))
    label = myfont.render(showbytes(c2), 1, (0, 0, 0))
    screen.blit(label, (100, 200))
    label = myfont.render(showbytes(x), 1, (0, 0, 0))
    screen.blit(label, (100, 300))
    loc = int(loc)
    rp = cribpend(c1, r, loc) #r, appended
    label = myfont.render(showbytes(rp), 1, (255, 0, 0))
    screen.blit(label, (100, 400))
    xr = xor(x, rp)
    label = myfont.render(showbytes(xr), 1, (0, 0, 0))
    screen.blit(label, (100, 500))
    myfont = pygame.font.SysFont("Arial", 10)
    for j in range(0, 5):
        tx = 100
        ty = 100
        width = 665
        height = 25
        pygame.draw.polygon(screen, (0, 235, 235),
                            ((tx, ty+j*100), (tx+width, ty+j*100),
                             (tx+width, ty+height+j*100), (tx, ty+height+j*100)),
                            2)
    if (inputting == 1):
        j = 3
        pygame.draw.polygon(screen, (255, 0, 0),
                            ((tx, ty+j*100), (tx+width, ty+j*100),
                             (tx+width, ty+height+j*100), (tx, ty+height+j*100)),
                            2)
        pygame.draw.line(screen, (255, 0, 0),
                         (100+(loc+len(r))*15, 400), (100+(loc+len(r))*15, 425)
                         )
    for j in range(0, 5):
        for i in range(0, 44):
            label = myfont.render(str(i), 1, (150, 150, 150))
            screen.blit(label, (100 + i * 15 + 4, 80 + j * 100))
    if (towrite == 1):
        vnames = ["C1", "C2", "Xortext", "R", "Xorcribtext"]
        vname = vnames[linenum]
        vs = [c1, c2, x, rp, xr]
        vstr = str(vs[linenum][charnum])
        vstr += str(" (" + bit(vs[linenum][charnum]) + ")")
        myfont = pygame.font.SysFont("Arial", 18)
        label = myfont.render("Char " + str(charnum) + " of " + vname + ": " + vstr, 1, (0, 0, 0))
        screen.blit(label, (100, 600))
        if linenum == 2:
            s = "C1[{}] XOR C2[{}] = {}({}) XOR {}({}) = {}({})".format(
                charnum, charnum,
                c1[charnum], bit(c1[charnum]),
                c2[charnum], bit(c2[charnum]),
                x[charnum], bit(x[charnum]))
            label = myfont.render(s, 1, (135, 0, 0))
            screen.blit(label, (100, 630))
        if linenum == 4:
            s = "X[{}] XOR R[{}] = {}({}) XOR {}({}) = {}({})".format(
                charnum, charnum,
                x[charnum], bit(x[charnum]),
                rp[charnum], bit(rp[charnum]),
                xr[charnum], bit(xr[charnum]))
            label = myfont.render(s, 1, (135, 0, 0))
            screen.blit(label, (100, 630))
    pygame.display.flip()
    clock.tick(30)
            

