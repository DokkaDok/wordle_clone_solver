import random, pygame, sys
from pygame.locals import *
pygame.init()

all_words = []
random_word = ''

WIN_WIDTH = 560
WIN_HEIGHT = 700

pygame.display.set_caption("Wordle Clone/Solver")

white = (255,255,255)
yellow = (181,159,59,255)
grey = (58,58,60,255)
black = (18,18,19,255)
green = (83,141,78,255)
red = (170,67,68,255)

font = pygame.font.SysFont("Helvetica neue", 46)

def create_array():
    with open('words.txt') as words:
        for word in words:
            all_words.append(word.rstrip('\n').upper())

def check_word(word, window, turns):
    user_guess = ["","","","",""]
    spacing = 0
    color = [grey, grey, grey, grey, grey]
    
    for i in range(5):

        global all_words

        if word[i] not in random_word:
            all_words = [element for element in all_words if word[i] not in element and element.count(word[i]) != 1]
            
        else:
            if word[i] == random_word[i]:
                color[i] = green
                all_words = [element for element in all_words if word[i] == element[i]]

            else:
                if word[i] in random_word:
                    if word.count(word[i]) > 1 and color[word.index(word[i])] != grey:
                        color[i] = grey
                        all_words = [element for element in all_words if word[i] != element[i] and word[i] in element]
                    else:
                        color[i] = yellow
                        all_words = [element for element in all_words if word[i] != element[i] and word[i] in element]
            
        list(word)

        user_guess[i] = font.render(word[i], True, white)
        pygame.draw.rect(window, color[i], pygame.Rect(60 + spacing, 50+ (turns*90), 80, 80))
        window.blit(user_guess[i], (90 + spacing, 80 + (turns*90)))
        spacing += 90
        
        if color == [green, green, green, green, green]:
            return True


def main():
    global random_word
 
    create_array()

    FPS = 30
    clock = pygame.time.Clock()
    
    random_word = random.choice(all_words)
    user_input = ""
    chosen_word = ""
    
    window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    window.fill(black)
    
    for i in range(5):
        for j in range(5):
            pygame.draw.rect(window, grey, pygame.Rect(60+(i*90), 50+(j*90), 80, 80), 2)

    turns = 0
    win = False
    
    print("Word: " + random_word) #solution

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                user_input += event.unicode.upper()
            
                if event.key == pygame.K_RETURN and win == True:
                    main()
                
                if event.key == pygame.K_RETURN and turns == 5:
                    main()
                    
                if event.key == pygame.K_SPACE and win != True:
                    for i in range(5-turns):
                        chosen_word = random.choice(all_words)
                        win = check_word(chosen_word, window, turns)
                        turns += 1
                        window.fill(black,(0,500,500,200))
                        if chosen_word == random_word:
                            break
                    
                if event.key == pygame.K_BACKSPACE or len(user_input) > 5:
                    user_input = user_input[:-1]
                    
                if event.key == pygame.K_RETURN and len(user_input) > 4:
                    win = check_word(user_input, window, turns)
                    turns += 1
                    user_input = ""
                    window.fill(black,(0,500,500,200))
                
            window.fill(black,(0,500,500,200))
            user_guess = font.render(user_input, True, grey)
            window.blit(user_guess, (227, 500))
            Solve = font.render((f"Press SPACE to solve"), True, grey)
            window.blit(Solve, (120, 550))

            Continue = font.render((f"Press ENTER to continue"), True, grey)
            
            if win == True:
                Won = font.render((f"You won! Turns: {turns}"), True, green)
                window.fill(black, (0,500,500,200))
                window.blit(Won, (147, 500))
                window.blit(Continue, (90, 600))
                
            if turns == 5 and win != True:
                Lost = font.render((f"You Lose! Correct word: {random_word}"), True, red)
                window.fill(black, (0,500,500,200))
                window.blit(Lost, (45, 500))
                window.blit(Continue, (90, 600))
            
            pygame.display.update()
            clock.tick(FPS)

main()
