import fileLoader
import pygame
from objects.block import Block
import utils
from objects.scale import Scale
from objects.fish import Fish
import math
from objects.poof import Poof


CAT_IMAGES = [
    (fileLoader.loadImage("skinnyCat.png"), (11, 70)),
    (fileLoader.loadImage("normalCat.png"), (71, 130)),
    (fileLoader.loadImage("fatCat.png"), (131, 190))
]
SLIDER_IMAGE = pygame.transform.scale(fileLoader.loadImage("slider.png"), (40, 120))
CAT_PAW_IMAGE = pygame.transform.scale(fileLoader.loadImage("catPaw.png"), (15, 15))

class Player():
    def __init__(self, startingPos: list[int, int] = (0, 0), sizeIn: list = (100, 100), poof: Poof = None) -> None:
        # POS IS THE BOTTOM LEFT CORNER!
        self.startingPos = startingPos  # Store startingPos as an instance variable
        self.pos = [startingPos[0], startingPos[1]]
        self.velo = [0, 0]

        # Sets shown velocity
        self.svelo = [0, 0]

        # Sets direction
        self.direction = 1

        # Sets images
        self.s_walk = [fileLoader.loadImage(f"small/small_walk-{i}.png") for i in range(6)]
        self.s_jump = [fileLoader.loadImage(f"small/small_jump-{i}.png") for i in range(10)]
        self.s_idle = [fileLoader.loadImage("small/small_walk-0.png"),
                       fileLoader.loadImage("small/small_walk-1.png")]

        self.m_walk = [fileLoader.loadImage(f"medium/medium_walk-{i}.png") for i in range(6)]
        self.m_jump = [fileLoader.loadImage(f"medium/medium_jump-{i}.png") for i in range(8)]
        self.m_idle = [fileLoader.loadImage("medium/medium_walk-0.png"),
                       fileLoader.loadImage("medium/medium_jump-1.png")]

        self.l_walk = [fileLoader.loadImage(f"large/large_walk-{i}.png") for i in range(7)]
        self.l_jump = [fileLoader.loadImage(f"large/large_jump-{i}.png") for i in range(13)]
        self.l_idle = [fileLoader.loadImage("large/large_jump-0.png"),
                       fileLoader.loadImage("large/large_jump-1.png")]

        # Drawing variables
        self.val = 0
        self.frame = 0

        # Sets state
        self.state = "idle" # Can be set to walking, jumping
        self.sizeState = "medium"

        # This is the image size
        self.size = [sizeIn[0], sizeIn[1]]

        # This is the slider value
        self.catSize = 100

        self.scaleTimer = 0
        self.scaleDirection = 1  # 1 for moving up, -1 for moving down

        self.image = CAT_IMAGES[1][0]

        # 0 for no, 1 for down, -1 for up
        self.showSlider = 0

        # Determines whether time should be slowed
        self.slowTime = 0

        # Wall jump variables
        self.wallJumpCooldown = 0
        self.wallJumpCooldownTime = 10

        # Initialize fish and scales variables
        self.fish_count = 0
        self.scale_count = 0
        self.scale_count_level = 0
        # Initialize a font object
        self.font = fileLoader.loadFont('./stepalange-font/Stepalange-x3BLm.otf', 36)

        # Poof
        self.poof = poof

        # Jumping
        self.jump_frame = 0
        self.jump_timer = 0
        self.landing_frame = 0
        self.onGround = True

        self.keyBinds: dict[str, int] = {
            "right": pygame.K_RIGHT,
            "left": pygame.K_LEFT,
            "jump": pygame.K_UP,
            "scaleUp": pygame.K_c,
            "scaleDown": pygame.K_x,
            "scaleConfirm": pygame.K_SPACE,
        }

        #Death counter
        self.death = 0

        #Timer
        self.timer = pygame.time.get_ticks()
    # Add these variables in your class initialization
    wallJumpCooldown = 0  # Cooldown counter
    wallJumpCooldownTime = 10  # Number of frames to wait before allowing direction changes after a wall jump

    #function to reset the scales when you die
    def resetScales(self, scales: list[Scale]) -> None:
        for scale in scales:
            scale.reset()
            print("Scale reset")

    #function to get and set scale_count_per_level to make sure you can only collect the scales once and if u die it subtracts
    def get_scale_count_level(self) -> int:
        return self.scale_count_level
    def set_scale_count_level(self, value: int) -> None:
        self.scale_count_level = value
        print("Scale count level set to", value)

    def update(self, keysDownIn: dict[str, bool], blocks: list[Block], scales: list[Scale], fishes: list[Fish]) -> None:
        # Scale logic

        if self.pos[0] < 0 or self.pos[0] > 1920 or self.pos[1] < 0 or self.pos[1] > 1080:
            print("DEATH - cat evaporated")
            self.pos = [self.startingPos[0], self.startingPos[1]]
            self.catSize = 100
            self.death += 1
            self.resetScales(scales)
            self.scale_count = self.scale_count - self.scale_count_level
            self.scale_count_level = 0


        if (keysDownIn[self.keyBinds["scaleUp"]] or keysDownIn[self.keyBinds["scaleDown"]]) and self.showSlider == 0:
            self.showSlider = 1
            if keysDownIn[self.keyBinds["scaleUp"]]:
                self.scaleDirection = 1
            if keysDownIn[self.keyBinds["scaleDown"]]:
                self.scaleDirection = -1
            self.slowTime = True

        if self.showSlider != 0:
            # Update the scaleTimer and reverse direction if it hits the bounds
            self.scaleTimer += self.scaleDirection * 1

            if self.scaleTimer >= 60:  # Reached the top of the slider
                self.scaleTimer = 60
                self.scaleDirection = -1  # Reverse direction
            elif self.scaleTimer <= -45:  # Reached the bottom of the slider
                self.scaleTimer = -45
                self.scaleDirection = 1  # Reverse direction

            if keysDownIn[self.keyBinds["scaleConfirm"]]:
                # Check for potential collisions before resizing
                self.handlePreResizeCollision(blocks)

                self.poof.isDrawing = True


                # Apply the size change without affecting velocity
                newCatSize = 100 + self.scaleTimer / 60 * 100

                self.poof.size = "lar" if newCatSize >= 160 else "med"

                # Get current dimensions of the player
                width = self.size[0] * newCatSize / 100
                height = self.size[1] * newCatSize / 100

                for block in blocks:
                    blockData = block.get()
                    if (self.pos[0] + width > blockData['x'] and
                            self.pos[0] < blockData['x'] + blockData['w'] and
                            self.pos[1] + height > blockData['y'] and
                            self.pos[1] < blockData['y'] + blockData['h']):
                        print("DEATH - cat squashed")
                        self.pos = [self.startingPos[0], self.startingPos[1]]
                        self.catSize = 100
                        self.death += 1
                        self.resetScales(scales)
                        self.scale_count = self.scale_count - self.scale_count_level
                        self.scale_count_level = 0



                self.pos[0] += (self.catSize - newCatSize) / 4
                self.pos[1] += (self.catSize - newCatSize) / 4

                self.catSize = newCatSize

                self.showSlider = 0
                self.scaleDirection = 1  # Reset direction for next time

                self.slowTime = False



        # Update velocities based on key presses
        if self.wallJumpCooldown > 0:
            self.wallJumpCooldown -= 1  # Decrement cooldown counter
        else:
            self.velo[0] = (keysDownIn[self.keyBinds["right"]] - keysDownIn[self.keyBinds["left"]]) * 5

        # Apply gravity
        gravity_effect = 0.4 * 75 / self.catSize
        if self.slowTime:
            gravity_effect *= 0.01  # Apply slowdown to gravity effect

        self.velo[1] += gravity_effect

        # Get current dimensions of the player
        width = self.size[0] * self.catSize / 100
        height = self.size[1] * self.catSize / 100

        # Apply slow time effects
        if self.slowTime:
            svelo = [v * 0.01 for v in self.velo]
        else:
            svelo = self.velo

        # X-axis collision detection and handling
        self.pos[0] += svelo[0]
        onWall = 0

        for block in blocks:
            blockData = block.get()

            # Check if there is a collision
            if (self.pos[0] + width > blockData['x'] and
                    self.pos[0] < blockData['x'] + blockData['w'] and
                    self.pos[1] + height > blockData['y'] and
                    self.pos[1] < blockData['y'] + blockData['h']):

                if self.velo[0] > 0:  # Moving right
                    if self.pos[0] + width > blockData['x']:
                        self.pos[0] = blockData['x'] - width  # Adjust position
                        onWall = 1  # Indicate collision with wall on the right

                elif self.velo[0] < 0:  # Moving left
                    if self.pos[0] < blockData['x'] + blockData['w']:
                        self.pos[0] = blockData['x'] + blockData['w']  # Adjust position
                        onWall = -1  # Indicate collision with wall on the left

                if blockData["water"] == True:
                    if onWall != 0:
                        print("DEATH - water")
                        self.pos = [self.startingPos[0], self.startingPos[1]]
                        self.catSize = 100
                        self.death += 1
                        self.resetScales(scales)
                        self.scale_count = self.scale_count - self.scale_count_level
                        self.scale_count_level = 0


        # Y-axis collision detection and handling
        self.pos[1] += svelo[1]
        self.onGround = False  # Track if player is on the ground
        onRoof = False # Track if player is on the roof

        for block in blocks:
            blockData = block.get()

            if (self.pos[0] + width > blockData['x'] and
                    self.pos[0] < blockData['x'] + blockData['w'] and
                    self.pos[1] + height > blockData['y'] and
                    self.pos[1] < blockData['y'] + blockData['h']):

                if self.velo[1] > 0:  # Moving down
                    self.pos[1] = blockData['y'] - height
                    self.onGround = True  # Player is on the ground
                elif self.velo[1] < 0:  # Moving up
                    self.pos[1] = blockData['y'] + blockData['h']
                    onRoof = True # Player is on the roof

                if blockData["water"] == True:
                    if onRoof or self.onGround:
                        print("DEATH - water")
                        self.pos = [self.startingPos[0], self.startingPos[1]]
                        self.catSize = 100
                        self.death += 1
                        self.resetScales(scales)
                        self.scale_count = self.scale_count - self.scale_count_level
                        self.scale_count_level = 0



                self.velo[1] = 0  # Stop vertical movement

        for scale in scales:
            scaleData = scale.get()
            width = self.size[0] * self.catSize / 100
            height = self.size[1] * self.catSize / 100

            # Check for collision on the X and Y axes
            if (self.pos[0] + width > scaleData['x'] and
                self.pos[0] < scaleData['x'] + scaleData['w'] and
                self.pos[1] + height > scaleData['y'] and
                self.pos[1] < scaleData['y'] + scaleData['h']):

                # Collision detected, collect the scale
                if not scale.collected:
                    self.scale_count += 1
                    self.scale_count_level += 1
                    scale.collected = True

        if self.onGround:
            if keysDownIn[self.keyBinds["jump"]]:
                self.velo[1] -= 10 * self.catSize / 100
                self.state = "jumping"
                self.jump_frame = 0  # Start the jump animation
                self.jump_timer = 0
                self.landing_frame = -1  # Reset landing frames
            elif self.landing_frame != -1:
                self.jump_frame = self.landing_frame
                # Continue with landing frames if necessary
                if self.sizeState == "medium":
                    if self.landing_frame >= 6 and self.landing_frame < 8:
                        self.landing_frame += 1
                    elif self.landing_frame >= 8:
                        self.landing_frame = -1  # Reset after landing frames are done
                if self.sizeState == "small":
                    if self.landing_frame >= 7 and self.landing_frame < 10:
                        self.landing_frame += 1
                    elif self.landing_frame >= 10:
                        self.landing_frame = -1
        else:
            if self.velo[1] < 0:
                self.jump_frame = 3  # Play the 4th jump frame
            elif self.velo[1] == 0 and not self.onGround:
                if self.sizeState == "medium":
                    self.jump_frame = 4  # Play the 5th jump frame as long as velocity is decreasing
                elif self.sizeState == "small":
                    self.jump_frame = 3
            elif self.velo[1] >= 0:
                if self.sizeState == "medium":
                    self.jump_frame = 5
                elif self.sizeState == "small":
                    if self.jump_timer == 0:
                        self.jump_frame = 4
                    elif self.jump_timer == 1:
                        self.jump_frame = 5
                    elif self.jump_timer == 2:
                        self.jump_frame = 6
                    self.jump_frame += 1


        if self.sizeState == "medium":
            if not self.onGround and self.jump_frame >= 5:
                self.state = "landing"
                self.landing_frame = 6  # Start playing landing frames
        elif self.sizeState == "small":
            if not self.onGround and self.jump_frame >= 6:
                self.state = "landing"
                self.landing_frame = 7

        # Wall jumping
        if onWall != 0:
            if keysDownIn[self.keyBinds["jump"]]:
                # Apply a jump force upwards
                self.velo[1] -= 5 * self.catSize / 100  # Adjust this value to control jump strength
                self.velo[1] = utils.clamp(self.velo[1], -16, 9999)

                # Apply a force to move away from the wall
                self.velo[0] = -15 * min(1, 100 / self.catSize) if onWall == 1 else 15 * min(1, 100 / self.catSize)  # Adjust this value to control horizontal movement away from the wall

                # Optionally adjust the position slightly to prevent getting stuck
                self.pos[0] += -15 * min(1, 100 / self.catSize) if onWall == 1 else 15 * min(1, 100 / self.catSize)  # You may need to adjust or remove this line based on how the character interacts with the wall

                # Prevent continuous wall jumping and set cooldown
                self.wallJumpCooldown = self.wallJumpCooldownTime
                onWall = 0

        if not self.onGround:
            self.state = "jumping"
        else:
            if self.velo[0] != 0:
                self.state = "walking"
            else:
                self.state = "idle"

        if self.velo[0] > 0:
            self.direction = 1
        if self.velo[0] < 0:
            self.direction = 0

        if self.catSize < 72:
            self.sizeState = "small"
        elif self.catSize < 160:
            self.sizeState = "medium"
        else:
            self.sizeState = "large"

        for fish in fishes:
            fishData = fish.get()

            # Check for collision on the X and Y axes
            if (self.pos[0] + width > fishData['x'] and
                self.pos[0] < fishData['x'] + fishData['w'] and
                self.pos[1] + height > fishData['y'] and
                self.pos[1] < fishData['y'] + fishData['h']):

                # Collision detected, collect the fish
                return True

    def handlePreResizeCollision(self, blocks: list[Block]) -> None:
        """Adjust position before resizing to avoid clipping into walls."""
        # Get the new dimensions if resizing would occur
        newCatSize = 100 + self.scaleTimer / 60 * 100
        newWidth = self.size[0] * newCatSize / 100
        newHeight = self.size[1] * newCatSize / 100

        # Check X-axis collision before resizing
        for block in blocks:
            blockData = block.get()

            if (self.pos[0] + newWidth > blockData['x'] and
                    self.pos[0] < blockData['x'] + blockData['w'] and
                    self.pos[1] + newHeight > blockData['y'] and
                    self.pos[1] < blockData['y'] + blockData['h']):

                if self.pos[0] + newWidth > blockData['x'] and self.pos[0] < blockData['x']:
                    self.pos[0] = blockData['x'] - newWidth  # Move the player to the left of the block
                elif self.pos[0] < blockData['x'] + blockData['w'] and self.pos[0] + newWidth > blockData['x'] + \
                        blockData['w']:
                    self.pos[0] = blockData['x'] + blockData['w']  # Move the player to the right of the block

            # Check Y-axis collision before resizing
            if (self.pos[0] + newWidth > blockData['x'] and
                    self.pos[0] < blockData['x'] + blockData['w'] and
                    self.pos[1] + newHeight > blockData['y'] and
                    self.pos[1] < blockData['y'] + blockData['h']):

                if self.pos[1] + newHeight > blockData['y'] and self.pos[1] < blockData['y']:
                    self.pos[1] = blockData['y'] - newHeight  # Move the player above the block
                elif self.pos[1] < blockData['y'] + blockData['h'] and self.pos[1] + newHeight > blockData['y'] + \
                        blockData['h']:
                    self.pos[1] = blockData['y'] + blockData['h']  # Move the player below the block
    #Timer Functions
    def minutes(self, milliseconds: int) -> int:
        return milliseconds // 60000
    def seconds(self, milliseconds: int) -> int:
        return (milliseconds // 1000) % 60
    def milliseconds(self, milliseconds: int) -> int:
        return milliseconds % 1000

    def draw(self, surfaceIn: pygame.Surface) -> None:
        # Draw the player
        cat_width = self.size[0] * self.catSize / 100
        cat_height = self.size[1] * self.catSize / 100

        if self.sizeState == "small":

            if self.state == "jumping":
                if self.jump_frame < 7:
                    current_image = self.s_jump[self.jump_frame]
                scale = self.catSize / 168
                dimensions = (scale * 168, scale * 144)

            elif self.state == "landing":
                current_image = self.m_jump[self.landing_frame]
                scale = self.catSize / 168
                dimensions = (scale * 168, scale * 144)

            if self.state == "walking":
                current_image = self.s_walk[self.frame]
                self.val += 1
                self.frame = math.floor(self.val / 30) % 6 if self.frame < 6 else 0
                scale = self.catSize / 234
                dimensions = (scale * 234, scale * 160)

            if self.state == "idle":
                self.frame = 0
                current_image = self.s_idle[self.frame]
                scale = self.catSize / 234
                dimensions = (scale * 234, scale * 160)

        elif self.sizeState == "medium":

            if self.state == "jumping":
                if self.jump_frame < 3:
                    current_image = self.m_jump[self.jump_frame]
                elif self.jump_frame == 3:
                    current_image = self.m_jump[3]  # Play the 4th jump frame until vertical velocity reaches 0
                elif self.jump_frame == 4:
                    current_image = self.m_jump[4]  # Play the 5th jump frame as long as velocity is decreasing
                else:
                    current_image = self.m_jump[5 + (self.jump_timer // 5)]
                scale = self.catSize / 258
                dimensions = (scale * 258, scale * 240)

            elif self.state == "landing":
                current_image = self.m_jump[self.landing_frame]
                scale = self.catSize / 258
                dimensions = (scale * 258, scale * 240)

            if self.state == "walking":
                current_image = self.m_walk[self.frame]
                self.val += 1
                self.frame = math.floor(self.val / 15) % 6
                scale = self.catSize / 234
                dimensions = (scale * 234, scale * 160)

            if self.state == "idle":
                self.frame = 0
                current_image = self.m_idle[self.frame]
                scale = self.catSize / 248
                dimensions = (scale * 248, scale * 168)

        elif self.sizeState == "large":

            if self.state == "jumping":
                print("hello world")

            if self.state == "walking":
                current_image = self.l_walk[self.frame]
                self.val += 1
                self.frame = math.floor(self.val / 30) % 6
                scale = self.catSize / 448
                dimensions = (scale * 448, scale * 328)

            if self.state == "idle":
                current_image = self.l_idle[self.frame]
                self.frame = 0
                scale = self.catSize / 448
                dimensions = (scale * 448, scale * 328)

        current_image = pygame.transform.scale(current_image, dimensions)
        current_image = pygame.transform.flip(current_image, (self.direction != 1), False)
        surfaceIn.blit(current_image, [self.pos[0], self.pos[1]+50])

        self.poof.draw([self.pos[0], self.pos[1]], self.catSize, surfaceIn)



        # Draw the slider if needed
        if self.showSlider != 0:
            # Position the slider at the bottom right corner of the cat
            sliderPos = (self.pos[0] + cat_width + 20, self.pos[1] - 100)
            surfaceIn.blit(SLIDER_IMAGE, sliderPos)

            # Draw the cat paw based on the current scale
            pawPos = (sliderPos[0] + 25, sliderPos[1] + 60 - int(self.scaleTimer))
            surfaceIn.blit(CAT_PAW_IMAGE, pawPos)

        #Counting the scales and fish
        self.bg_rect = pygame.image.load("./assets/images/UI/bg_gradient.png")
        self.bg_rect = pygame.Surface.convert_alpha(self.bg_rect)
        surfaceIn.blit(self.bg_rect, (0, 0))
        scale_count_text = self.font.render(f'Scales: {self.scale_count}', True, (255, 255, 255))
        surfaceIn.blit(scale_count_text, (100, 100))  # Position the text at the top-left corner of the screen
#        fish_count_text = self.font.render(f'Fish: {self.fish_count}', True, (0, 0, 0))
#       surfaceIn.blit(fish_count_text, (500, 100))  # Position the text at the top-left corner of the screen
        timer_text = self.font.render(f'Time: {int(self.minutes(pygame.time.get_ticks() - self.timer)) }:{int(self.seconds(pygame.time.get_ticks() - self.timer)) }:{int(self.milliseconds(pygame.time.get_ticks() - self.timer)) }', True, (255, 255, 255))
        surfaceIn.blit(timer_text, (1500, 100))
