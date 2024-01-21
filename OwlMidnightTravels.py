import simplegui
from user304_rsf8mD0BOQ_1 import Vector
from user308_8AWTHK4jq32O0xk_1 import LEVELS #imports the levels for different platforms from a different codeskulptor py file.

# game settings and assets are stored here
SETTINGS = {
    "height": 500,
    "width": 800,
    "spritewalk_w": 192,
    "spritewalk_h": 32,
    "life": 3,
    "columns": 6,
    "rows": 1,
    "img": {
        "bg": "https://cdn.discordapp.com/attachments/1074339508138549258/1087179009038745720/Untitled_design_1.png",
        "cloud": "https://cdn.discordapp.com/attachments/1074339508138549258/1087178734953570314/1cloud.png",
        "platform": "https://cdn.discordapp.com/attachments/1074339508138549258/1087161661900722206/dirtpixel.png",
        "owl": "https://cdn.discordapp.com/attachments/1074158438709481542/1078074931255967764/Owlet_Monster_Walk_6.png",
        #adds a flipped version of the sprite for when the sprite turns around
        "owl_flipped": "https://media.discordapp.net/attachments/1088489689494863975/1088490385992597594/Owlet_Monster_flipped.png",
        "heart": "https://freesvg.org/img/1646656079PixelArt-Heart-1.png",
    },
    "sounds": {
        "bg": "https://cdn.discordapp.com/attachments/1087198228388270112/1088789917695492096/kim-lightyear-leave-the-world-tonight-chiptune-edit-loop-132102.mp3",
        "die": "https://cdn.discordapp.com/attachments/1087198228388270112/1088821104249946152/negative_beeps-6008.mp3",
        "next_level": "https://cdn.discordapp.com/attachments/1087198228388270112/1088821919425511484/short-success-sound-glockenspiel-treasure-video-game-6346.mp3",
        "lose": "https://cdn.discordapp.com/attachments/1087198228388270112/1088821069185568809/kl-peach-game-over-iii-142453.mp3",
        "win": "https://cdn.discordapp.com/attachments/1087198228388270112/1088821724700753940/level-win-6416.mp3",
        "menu": "https://cdn.discordapp.com/attachments/1087198228388270112/1088789917695492096/kim-lightyear-leave-the-world-tonight-chiptune-edit-loop-132102.mp3",
    },
}

#class with variables representing a rectangle
class Rect:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.width = w
        self.height = h

#stores the base variables for game objects
class GameObject:
    def __init__(self, pos):
        self.pos = pos
        self.vel = Vector(0, 0)
        self.acc = Vector(0, 0)

    def update(self):
        self.vel = Vector(self.vel.x + self.acc.x, self.vel.y + self.acc.y)
        self.pos = Vector(self.pos.x + self.vel.x, self.pos.y + self.vel.y)
        self.acc = Vector(0, 0)

    def applyForce(self, f):
        self.acc = Vector(self.acc.x + f.x, self.acc.y + f.y)

    def draw(self, canvas):
        pass

    def getRect(self):
        return Rect(self.pos.x - 16, self.pos.y - 16, 32, 32)

    def setPos(self, p):
        self.pos = p

    
    def collide(self, a, b):
        rect = a.getRect()
        r = b.getRect()
        if (
            r.x < rect.x + rect.width
            and r.x + r.width > rect.x
            and r.y < rect.y + rect.height
            and r.height + r.y > rect.y
        ):
            return True
        return False

class Owlsprite(GameObject):
    #initializes the details of the owl sprite sheet
    def __init__(self, pos):
        super().__init__(pos)
        self.sprite_right = Spritesheet(SETTINGS["img"]["owl"], 6, 1, (50, 70))
        self.sprite_left = Spritesheet(SETTINGS["img"]["owl_flipped"], 6, 1, (50, 70))
        self.current_sprite = self.sprite_right
        self.speed = 5
        self.jumpCount = 0

    def update(self):
        super().update()

        self.applyForce(Vector(0, 0.58))  # gravity

        if self.pos.y >= 420:
            self.pos.y = 420
            self.jumpCount = 0
            self.vel = Vector(self.vel.x, 0)

        self.current_sprite.setPos(self.pos)
        # self.vel.multiply(0.85)

    def draw(self, canvas):
        self.current_sprite.draw(canvas)

    def jump(self):
        if self.vel.y < 0:
            return
        if self.jumpCount < 2:
            self.applyForce(Vector(0, -12.81))  # jump force
            self.jumpCount += 1

    def switch_sprite(self, direction):
        if direction == "left":
            self.current_sprite = self.sprite_left
        else:
            self.current_sprite = self.sprite_right


class Platform(GameObject):
    #initializes the details of the platforms
    def __init__(self, pos, rows, cols):
        super().__init__(pos)
        self.pos = pos
        self.rows = rows
        self.cols = cols
        self.visible = True
        self.img = simplegui.load_image(SETTINGS["img"]["platform"])

    def draw(self, canvas):
        x = self.pos.x
        y = self.pos.y

        #loop through the rows and columns of the platform
        for row in range(0, self.rows):
            for col in range(0, self.cols):
                x += 32
                canvas.draw_image(
                    self.img,
                    (self.img.get_width() / 2, self.img.get_height() / 2),
                    (self.img.get_width(), self.img.get_height()),
                    (x, y),
                    (32, 32),
                )
            #Resets the position of x to the start of the row and move down to the next row
            x = self.pos.x
            y += 16

    #returns the rect dimensions for the platform
    def getRect(self):
        return Rect(
            self.pos.x + 16, self.pos.y - 32, self.cols * 32, self.rows * 32 + 32
        )

    #calculates the collision of the owl with the wall(platform)
    def onWallCollide(self, owl):
        wallRect = self.getRect()
        owlRect = owl.getRect()

        if owlRect.y + owlRect.height > wallRect.y > owlRect.y:
            diff = owlRect.y + owlRect.height - wallRect.y
            owl.vel = Vector(owl.vel.x, 0)
            owl.jumpCount = 0
            owl.setPos(Vector(owl.pos.x, owlRect.y - diff + 16))
            return self.rows
        # left
        elif (
            owlRect.y + owlRect.height < wallRect.y + wallRect.height
            and owlRect.x + owlRect.width > wallRect.x > owlRect.x
        ):
            diff = owlRect.x + owlRect.width - wallRect.x
            owl.setPos(Vector(owlRect.x - diff, owlRect.y))
            owl.vel = Vector(0, owl.vel.y)
            return self.rows
        # right
        elif (
            owlRect.y + owlRect.height < wallRect.y + wallRect.height
            and owlRect.x < wallRect.x + wallRect.width
            and owlRect.x + owlRect.width > wallRect.x
        ):
            diff = wallRect.x + wallRect.width - owlRect.x
            owl.setPos(Vector(owlRect.x + diff, owlRect.y))
            owl.vel = Vector(0, owl.vel.y)
            return self.rows
        # bottom
        elif wallRect.y + wallRect.height > owlRect.y > wallRect.y:
            diff = wallRect.y + wallRect.height - owlRect.y
            owl.vel = Vector(owl.vel.x, 0)
            owl.setPos(Vector(owl.pos.x, owlRect.y + diff + 16))
            return self.rows

    #to check if the platform is visible on the screen and not outside the canvas
    def is_visible(self):
        self.visible = not (
            self.pos.x + self.getRect().width < 0 or self.pos.x > SETTINGS["width"]
        )

#Initializes the cloud object details
class Cloud(GameObject):
    def __init__(self, pos, width=1.0, height=1.0):
        super().__init__(pos)
        self.pos = pos
        self.height = height
        self.width = width
        self.img = simplegui.load_image(SETTINGS["img"]["cloud"])
        self.vel = [0.7, 0]  # velocity of the cloud

    def draw(self, canvas):
        canvas.draw_image(
            self.img,
            (self.img.get_width() / 2, self.img.get_height() / 2),
            (self.img.get_width(), self.img.get_height()),
            (self.pos[0], self.pos[1]),
            (
                self.img.get_width() / self.width,
                self.img.get_height() / self.height,
            ),
        )

    #Updates the position of the cloud
    def update(self):
        self.pos[0] += self.vel[0]
        if self.pos[0] > SETTINGS["width"] + self.img.get_width():
            self.pos[0] = -self.img.get_width()


# keyboard inputs for the sprite
class Keyboard:
    def __init__(self):
        self.right = False
        self.left = False
        self.space = False

    def keyDown(self, key):
        if key == simplegui.KEY_MAP["right"]:
            self.right = True
        elif key == simplegui.KEY_MAP["left"]:
            self.left = True
        if key == simplegui.KEY_MAP["space"]:
            self.space = True

    def keyUp(self, key):
        if key == simplegui.KEY_MAP["right"]:
            self.right = False
        elif key == simplegui.KEY_MAP["left"]:
            self.left = False
        if key == simplegui.KEY_MAP["space"]:
            self.space = False

#initializes the details of the sprite sheet
class Spritesheet:
    def __init__(self, img_url, columns, rows, dest_size):
        self.dest_size = dest_size
        self.pos = Vector(0, 0)
        self.img = simplegui.load_image(img_url)
        self.columns = columns
        self.rows = rows
        self.frame_width = SETTINGS["spritewalk_w"] / columns
        self.frame_height = SETTINGS["spritewalk_h"] / rows
        self.frame_centre_x = self.frame_width / 2
        self.frame_centre_y = self.frame_height / 2
        self.frame_index = [0, 0]
        self.vel = Vector()
        self.rotation = 0

    def next_frame(self):
        self.frame_index[0] = (self.frame_index[0] + 1) % self.columns
        if self.frame_index[0] == 0:
            self.frame_index[1] = (self.frame_index[1] + 1) % self.rows

    def draw(self, canvas):
        source_centre = (
            self.frame_width * self.frame_index[0] + self.frame_centre_x,
            self.frame_height * self.frame_index[1] + self.frame_centre_y,
        )

        source_size = (self.frame_width, self.frame_height)

        canvas.draw_image(
            self.img,
            source_centre,
            source_size,
            self.pos.get_p(),
            self.dest_size,
            self.rotation,
        )

    def setPos(self, pos):
        self.pos = pos

#keeps track of the times and animations of objects
class Clock:
    def __init__(self, frame_duration):
        self.time = 0
        self.frame_duration = frame_duration
        self.has_transitioned = False

    def tick(self):
        self.time += 1
        self.has_transitioned = False

    def transition(self):
        if self.time % self.frame_duration == 0 and not self.has_transitioned:
            self.has_transitioned = True
            return True
        return False


class Game:
    __instance = None
    #to create just one instance
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(Game, cls).__new__(cls)
            cls.__instance.__initialized = False
        return cls.__instance

    def __init__(self):
        if self.__initialized:
            return
        self.__initialized = True
        # load cloud image
        self.cloud_image = simplegui.load_image(SETTINGS["img"]["cloud"])

        # Load the sound file
        self.sound = simplegui.load_sound(SETTINGS["sounds"]["menu"])
        # Play the sound file in a loop
        self.sound.play()
        self.sound.set_volume(0.3)  # Set the volume (0 to 1)

        # background
        self.bg_image = simplegui.load_image(SETTINGS["img"]["bg"])
        # heart
        self.heart = simplegui.load_image(SETTINGS["img"]["heart"])

        self.playing = False
        self.message = "Press Space to restart"
        self.level = 0
        self.life = SETTINGS["life"]
        self.finished_level = False

        self.platforms = []
        self.owl = Owlsprite(Vector(120, 100))

        # initializes clouds
        self.clouds = [
            Cloud([5, 30]),
            Cloud([-200, 30], width=1.5, height=1.5),
            Cloud([-350, 50], width=1.5, height=1.5),
            Cloud([100, 150], width=1.8, height=1.8),
            Cloud([400, 50], width=1.8, height=1.8),
        ]
        self.clock = Clock(5)
        self.kbd = Keyboard()

        self.frame = simplegui.create_frame(
            "Owl's Midnight Travels", SETTINGS["width"], SETTINGS["height"]
        )
        self.frame.set_draw_handler(self.draw_menu_frame)
        self.frame.set_keydown_handler(self.kbd.keyDown)
        self.frame.set_keyup_handler(self.kbd.keyUp)
        self.frame.start()

    #start the next level
    def start_level(self):
        self.playing = True
        self.owl = Owlsprite(Vector(120, 100))
        diff = self.owl.pos.x - SETTINGS["width"] / 2
        self.owl.pos.x -= diff
        del self.platforms
        self.platforms = []

        #loads in the platforms from the level py
        for platform in LEVELS[self.level]:
            self.platforms.append(
                Platform(
                    platform["pos"],
                    platform["row"],
                    platform["cols"],
                )
            )
            self.platforms[0].is_visible()

        self.move_platforms()

    #Adds text on the menu screen
    def draw_menu_frame(self, canvas):
        self.draw_bg(canvas)
        canvas.draw_text("Welcome!", [300, 100], 48, "White")
        canvas.draw_text("Instructions :", [100, 150], 35, "White")
        canvas.draw_text("1. Jump onto different platforms until you reach the last 3 rows platform!", [100, 200], 20, "White")
        canvas.draw_text("2. Make sure you avoid the 2 rows platform as it will take away your life.", [100, 250], 20, "White")
        canvas.draw_text("3. You have 3 lifes total until you get a Game-over :(", [100, 300], 20, "White")
        canvas.draw_text("Press Space to Start", [200, 400], 48, "White")
        if self.kbd.space:
            self.kbd.space = False
            self.game_frame()
    
    #Adds a screen with text in between each level transition
    def draw_between_level_frame(self, canvas):
        self.draw_bg(canvas)
        text = "Press Space to Start the Next Level"
        canvas.draw_text(
            text, (SETTINGS["width"] / 2 - 250, SETTINGS["height"] / 2), 36, "White"
        )
        if self.kbd.space:
            self.kbd.space = False
            self.game_frame()

    #Shows a screen when the player loses a life
    def draw_died_frame(self, canvas):
        self.playing = False
        self.draw_bg(canvas)
        canvas.draw_text("You Died!", [300, 200], 48, "Red")
        canvas.draw_text(self.message, [200, 300], 48, "Red")
        canvas.draw_text(f"You have {self.life} life(s) left.", [170, 400], 48, "Red")
        if self.kbd.space:
            self.kbd.space = False
            self.game_frame()

    #Shows a screen when the player loses all their lifes
    def draw_game_over_frame(self, canvas):
        self.playing = False
        self.level = 0
        self.life = SETTINGS["life"]
        self.draw_bg(canvas)
        self.playing = False
        self.draw_bg(canvas)
        canvas.draw_text("Game Over!", [300, 200], 48, "Red")
        canvas.draw_text(self.message, [200, 300], 48, "Red")
        if self.kbd.space:
            self.kbd.space = False
            self.game_frame()

    #Shows a screen telling the player that they have finshed the game and won
    def draw_win_frame(self, canvas):
        self.playing = False
        self.level = 0
        self.life = SETTINGS["life"]
        self.draw_bg(canvas)
        canvas.draw_text("You won!", [300, 200], 48, "Green")
        canvas.draw_text(self.message, [200, 300], 48, "Green")
        if self.kbd.space:
            self.kbd.space = False
            self.game_frame()

    def game_frame(self):
        self.start_level()
        self.frame.set_draw_handler(self.draw)
        self.play_a_sound(SETTINGS["sounds"]["bg"])

    def draw(self, canvas):
        # Draw the background image first
        self.draw_bg(canvas)

        for cloud in self.clouds:
            cloud.update()
            # draw cloud
            cloud.draw(canvas)

        self.clock.tick()
        self.update()

        self.owl.update()

        diff = self.owl.pos.x - SETTINGS["width"] / 2
        if diff:
            self.owl.pos.x -= diff
            for platform in self.platforms:
                platform.pos.x -= diff
                platform.is_visible()

        self.owl.draw(canvas)

        self.move_platforms(canvas)

        self.draw_heart(canvas)

    def draw_bg(self, canvas):
        canvas.draw_image(
            self.bg_image,
            (self.bg_image.get_width() / 2, self.bg_image.get_height() / 2),
            (self.bg_image.get_width(), self.bg_image.get_height()),
            (SETTINGS["width"] / 2, SETTINGS["height"] / 2),
            (SETTINGS["width"], SETTINGS["height"]),
        )

    #draws the heart object to visualize the number of life(s) the user has left
    def draw_heart(self, canvas):
        canvas.draw_text(f"{self.life}x", [620, 450], 32, "Red")
        canvas.draw_image(
            self.heart,
            (self.heart.get_width() / 2, self.heart.get_height() / 2),
            (self.heart.get_width(), self.heart.get_height()),
            (700, 420),
            (
                self.heart.get_width() / 8,
                self.heart.get_height() / 8,
            ),
        )
    #updates the sprite location with keyboard input
    def update(self):
        updated = False
        if self.kbd.space:
            self.owl.jump()
            updated = True
        if self.kbd.right:
            self.owl.vel.x = self.owl.speed
            self.owl.switch_sprite("right")
            self.owl.current_sprite.next_frame()
            updated = True
        elif self.kbd.left:
            self.owl.vel.x = -self.owl.speed
            self.owl.switch_sprite("left")
            self.owl.current_sprite.next_frame()
            updated = True
        if not updated:
            self.owl.vel = Vector(0, self.owl.vel.y)
        if self.owl.pos.y == 420:
            self.life -= 1
            self.check_life()
    
    #decides what happens when the player runs out of all their lifes
    def check_life(self):
        if self.life > 0:
            self.frame.set_draw_handler(self.draw_died_frame) #Shows the screen for when the player dies, but still has lifes remaining
            self.play_a_sound(SETTINGS["sounds"]["die"])
        else:
            self.frame.set_draw_handler(self.draw_game_over_frame) #Shows the gameover screen
            self.play_a_sound(SETTINGS["sounds"]["lose"])

    #moves the platform on the canvas and checks for collision between the owl and the platform
    def move_platforms(self, canvas=None):
        for platform in self.platforms:
            if platform.visible:
                platform.update()
                if self.owl.collide(self.owl, platform):
                    platform_row = platform.onWallCollide(self.owl)
                    if platform_row == 3:
                        self.level += 1
                        if self.level == len(LEVELS): #sets the condition to win/finish the game
                            self.frame.set_draw_handler(self.draw_win_frame)
                            self.play_a_sound(SETTINGS["sounds"]["win"])
                        else:
                            self.play_a_sound(SETTINGS["sounds"]["next_level"])
                            self.frame.set_draw_handler(self.draw_between_level_frame)
                    elif platform_row == 2: #if the row of the platform is two, the player loses a life / this is to act as enemies and to add a challenge
                        self.life -= 1
                        self.check_life()
                if canvas:
                    platform.draw(canvas)

    # to play the sound and set the sound volume
    def play_a_sound(self, sound):
        self.sound.pause()
        self.sound = simplegui.load_sound(sound)
        self.sound.play()
        self.sound.set_volume(0.3)


game = Game()
