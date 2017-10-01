import numpy as np
import cv2
import pyautogui as pgui
import time

class MemorySolver:
    def start_game(self):
        pgui.PAUSE = 0.3
        pgui.click(self.locate('img/new_game.png'))
        pgui.click(self.locate('img/continue.png'))
        pgui.click()
    
    def level_one(self):
        pgui.PAUSE = 0.2
        # the locations of the cards
        locations = self.locate_all('img/symbol_1.png')

        # a list containing the images as well as the locations
        cards = []
        
        # iterate over each card and take a screenshot
        shot_width = 20
        for cur_loc in locations:
            pgui.moveTo(cur_loc)
            pgui.click()
            screenshot = pgui.screenshot(region=(cur_loc[0] - shot_width/2, cur_loc[1] - shot_width/2, shot_width, shot_width))
            cur_img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
            cards.append({"img":cur_img, "loc":cur_loc})

        # find the matches
        pgui.PAUSE=0.15
        while len(cards) > 1:
            cur_card = cards.pop(0)
            for i, match_card in enumerate(cards):
                if self.is_match(cur_card['img'], match_card['img']):
                    pgui.click(cur_card['loc'])
                    pgui.click(match_card['loc'])
                    cards.pop(i)
                    break
        # click next level
        time.sleep(0.5)
        pgui.click(self.locate('img/next_level.png'))

    def level_two(self):
        pgui.PAUSE=0.2
        time.sleep(0.3)
        pgui.click(self.locate('img/start_level.png'))
        
        time.sleep(0.3)
        locations = self.locate_all('img/symbol_2.png')

        # a list containing the images as well as the locations
        cards = []
        
        # iterate over each card and take a screenshot
        shot_width = 40
        for cur_loc in locations:
            pgui.moveTo(cur_loc)
            pgui.click()
            screenshot = pgui.screenshot(region=(cur_loc[0] - shot_width/2, cur_loc[1] - shot_width/2, shot_width, shot_width))
            cur_img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
            cards.append({"img":cur_img, "loc":cur_loc})

        # get the classes of the cards
        classes = self.get_classes(cards)

        # find the matches
        pgui.PAUSE=0.15
        while len(classes) > 1:
            cur_card = classes.pop(0)
            for i, match_card in enumerate(classes):
                if cur_card['class'] == match_card['class']:
                    pgui.click(cur_card['loc'])
                    pgui.click(match_card['loc'])
                    classes.pop(i)
                    break
        # click next level
        time.sleep(0.5)
        pgui.click(self.locate('img/next_level.png'))

    def get_classes(self, cards):
        # first load all the reference pictures
        references = []
        for i in range(12):
            references.append((cv2.imread('img/level_two/'+str(i)+'0.png', cv2.IMREAD_GRAYSCALE), cv2.imread('img/level_two/'+str(i)+'1.png', cv2.IMREAD_GRAYSCALE)))

        # now match the classes
        classes = []
        for cur_card in cards:
            for i, cur_reference in enumerate(references):
                if self.is_match(cur_card['img'], cur_reference[0], 0.70) or self.is_match(cur_card['img'], cur_reference[1], 0.70):
                    classes.append({"class":i, "loc":cur_card['loc']})
        return classes

    def screens_level_two(self):
        pgui.PAUSE=0.5
        locations = self.locate_all('img/symbol_2.png')

        # iterate over each card and take a screenshot
        shot_width = 40
        for i, cur_loc in enumerate(locations):
            pgui.moveTo(cur_loc)
            pgui.click()
            screenshot = pgui.screenshot(str(i)+'.png', region=(cur_loc[0] - shot_width/2, cur_loc[1] - shot_width/2, shot_width, shot_width))

    def level_three(self):
        pgui.PAUSE = 0.2
        time.sleep(0.3)
        pgui.click(self.locate('img/start_level.png'))
        
        # the locations of the cards
        locations = self.locate_all('img/symbol_3.png')

        # a list containing the images as well as the locations
        cards = []
        
        # iterate over each card and take a screenshot
        shot_width = 85
        shot_height = 35
        for cur_loc in locations:
            pgui.moveTo(cur_loc)
            pgui.click()
            screenshot = pgui.screenshot(region=(cur_loc[0] - shot_width/2, cur_loc[1] - shot_height/2, shot_width, shot_height))
            cur_img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
            cards.append({"img":cur_img, "loc":cur_loc})

        # find the matches
        pgui.PAUSE=0.2
        while len(cards) > 1:
            cur_card = cards.pop(0)
            for i, match_card in enumerate(cards):
                if self.is_match(cur_card['img'], match_card['img']):
                    pgui.moveTo(cur_card['loc'])
                    pgui.click()
                    pgui.moveTo(match_card['loc'])
                    pgui.click()
                    cards.pop(i)
                    break


    def is_match(self, img1, img2, threshold=0.9):
        res = cv2.matchTemplate(img1, img2, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        if max_val >= threshold:
            return True
        else:
            return False

    def locate(self, template):
        # read the template
        temp = cv2.imread(template, cv2.IMREAD_GRAYSCALE)
        width, height = temp.shape[::-1]
        screen = cv2.cvtColor(np.array(pgui.screenshot()), cv2.COLOR_RGB2GRAY)

        # get the position of the match
        res = cv2.matchTemplate(screen, temp, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        # return the coordinates of the center
        return (max_loc[0] + width/2, max_loc[1] + height/2)

    def locate_all(self, template, threshold=0.95):
        # read the template
        temp = cv2.imread(template, cv2.IMREAD_GRAYSCALE)
        width, height = temp.shape[::-1]
        screen = cv2.cvtColor(np.array(pgui.screenshot()), cv2.COLOR_RGB2GRAY)

        # get the position of the match
        res = cv2.matchTemplate(screen, temp, cv2.TM_CCOEFF_NORMED)
        locations = np.where( res >= threshold )
        points = []
        for cur_loc in zip(*locations[::-1]):
            points.append((cur_loc[0] + width/2, cur_loc[1] + height/2))
        return points

    def solve(self):
        self.start_game()
        self.level_one()
        self.level_two()
        self.level_three()

    
if __name__ == '__main__':
    solver = MemorySolver()
    solver.solve()
