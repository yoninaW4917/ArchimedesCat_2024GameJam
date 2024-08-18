import fileLoader
import pygame
from objects.block import Block
import utils
from objects.water import Water

CAT_IMAGES = [
    (fileLoader.loadImage("skinnyCat.png"), (11, 70)),
    (fileLoader.loadImage("normalCat.png"), (71, 130)),
    (fileLoader.loadImage("fatCat.png"), (131, 190))
]
SLIDER_IMAGE = pygame.transform.scale(fileLoader.loadImage("slider.png"), (40, 120))
CAT_PAW_IMAGE = pygame.transform.scale(fileLoader.loadImage("catPaw.png"), (15, 15))


class Player:
    def __init__(self, startingPos: tuple[int, int] = (0, 0), sizeIn: tuple = (100, 100)) -> None:
        # Position is the bottom left corner!
        self.startingPos = startingPos  # Store startingPos as an instance variable
        self.pos = [startingPos[0], startingPos[1]]
        self.velo = [0, 0]

        # Sets shown velocity
        self.svelo = [0, 0]

        # This is the image size
        self.size = [sizeIn[0], sizeIn[1]]

        #DEATH COUNT
        self.death_count = 0        
        # Initialize a font object
        self.font = fileLoader.loadFont(None, 36)


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

        self.keyBinds: dict[str, int] = {
            "right": pygame.K_RIGHT,
            "left": pygame.K_LEFT,
            "jump": pygame.K_UP,
            "scaleUp": pygame.K_c,
            "scaleDown": pygame.K_x,
            "scaleConfirm": pygame.K_SPACE,
        }

    # Add these variables in your class initialization
    wallJumpCooldown = 0  # Cooldown counter
    wallJumpCooldownTime = 10  # Number of frames to wait before allowing direction changes after a wall jump

    def update(self, keysDownIn: dict[str, bool], blocks: list[Block], waters : list[Water]) -> None:
        # Scale logic
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

                # Apply the size change without affecting velocity
                newCatSize = 100 + self.scaleTimer / 60 * 100
                self.catSize = newCatSize
                self.showSlider = 0
                self.scaleDirection = 1  # Reset direction for next time
                print(self.catSize)

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

        # Y-axis collision detection and handling
        self.pos[1] += svelo[1]
        onGround = False  # Track if player is on the ground

        for block in blocks:
            blockData = block.get()

            if (self.pos[0] + width > blockData['x'] and
                    self.pos[0] < blockData['x'] + blockData['w'] and
                    self.pos[1] + height > blockData['y'] and
                    self.pos[1] < blockData['y'] + blockData['h']):

                if self.velo[1] > 0:  # Moving down
                    self.pos[1] = blockData['y'] - height
                    onGround = True  # Player is on the ground
                elif self.velo[1] < 0:  # Moving up
                    self.pos[1] = blockData['y'] + blockData['h']

                self.velo[1] = 0  # Stop vertical movement
        for water in waters:
            waterData = water.get()
            width = self.size[0] * self.catSize / 100
            height = self.size[1] * self.catSize / 100
            yUndo = False

            # Check for collision on the X and Y axes
            if (self.pos[0] + width > waterData['x'] and
                self.pos[0] < waterData['x'] + waterData['w'] and
                self.pos[1] + height > waterData['y'] and
                self.pos[1] < waterData['y'] + waterData['h']):

                # Collision detected, resolve it
                self.pos[1] -= self.velo[1]  # Undo the Y movement
                self.velo[1] = 0             # Stop the Y velocity
                yUndo = True

                # Death handling
                self.pos = [self.startingPos[0], self.startingPos[1]]
                self.death_count += 1

                # if self.death_count >= 3:
                #     # Change level to 1 here or go to game over screen
                #     return

            if not yUndo:
                self.pos[1] -= self.velo[1]  # Undo the Y movement
        if onGround:
            if keysDownIn[self.keyBinds["jump"]]:
                self.velo[1] -= 10 * self.catSize / 100

        # Wall jumping
        if onWall != 0:
            if keysDownIn[self.keyBinds["jump"]]:
                # Apply a jump force upwards
                self.velo[1] -= 5 * self.catSize / 100  # Adjust this value to control jump strength

                # Apply a force to move away from the wall
                self.velo[0] = -15 * min(1, 100 / self.catSize) if onWall == 1 else 15 * min(1, 100 / self.catSize)  # Adjust this value to control horizontal movement away from the wall

                # Optionally adjust the position slightly to prevent getting stuck
                self.pos[0] += -15 * min(1, 100 / self.catSize) if onWall == 1 else 15 * min(1, 100 / self.catSize)  # You may need to adjust or remove this line based on how the character interacts with the wall

                # Prevent continuous wall jumping and set cooldown
                self.wallJumpCooldown = self.wallJumpCooldownTime
                onWall = 0

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

    def draw(self, surfaceIn: pygame.Surface) -> None:
        # Draw the player
        cat_width = self.size[0] * self.catSize / 100
        cat_height = self.size[1] * self.catSize / 100
        surfaceIn.blit(pygame.transform.scale(self.image, (cat_width, cat_height)), self.pos)

        # Draw the slider if needed
        if self.showSlider != 0:
            # Position the slider at the bottom right corner of the cat
            sliderPos = (self.pos[0] + cat_width + 20, self.pos[1] - 100)
            surfaceIn.blit(SLIDER_IMAGE, sliderPos)

            # Draw the cat paw based on the current scale
            pawPos = (sliderPos[0] + 10, sliderPos[1] + 60 - int(self.scaleTimer))
            surfaceIn.blit(CAT_PAW_IMAGE, pawPos)
        # Render the death count
        death_count_text = self.font.render(f'Deaths: {self.death_count}', True, (0, 0, 0))
        surfaceIn.blit(death_count_text, (10, 10))  # Position the text at the top-left corner

