import fileLoader
import pygame
from objects.block import Block
import utils
from objects.scale import Scale
from objects.fish import Fish

CAT_IMAGES = [
    (fileLoader.loadImage("skinnyCat.png"), (11, 70)),
    (fileLoader.loadImage("normalCat.png"), (71, 130)),
    (fileLoader.loadImage("fatCat.png"), (131, 190))
]
SLIDER_IMAGE = pygame.transform.scale(fileLoader.loadImage("slider.png"), (40, 120))
CAT_PAW_IMAGE = pygame.transform.scale(fileLoader.loadImage("catPaw.png"), (15, 15))

class Player():
    def __init__(self, startingPos: list[int, int] = (0, 0), sizeIn: list = (100, 100)) -> None:
        # POS IS THE BOTTOM LEFT CORNER!
        self.startingPos = startingPos  # Store startingPos as an instance variable
        self.pos = [startingPos[0], startingPos[1]]
        self.velo = [0, 0]

        # Sets shown velocity
        self.svelo = [0, 0]

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

    # Add these variables in your class initialization
    wallJumpCooldown = 0  # Cooldown counter
    wallJumpCooldownTime = 10  # Number of frames to wait before allowing direction changes after a wall jump

    #function to reset the scales when you die
    def resetScales(self, scales: list[Scale]) -> None:
        for scale in scales:
            scale.reset()
            print("Scale reset")

    #function to reset the fish when you die
    def resetFish(self, fishes: list[Fish]) -> None:
        for fish in fishes:
            fish.collectedFish = False

    def update(self, keysDownIn: dict[str, bool], blocks: list[Block], scales: list[Scale], fishes: list[Fish]) -> None:
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
                        self.death += 1
                        self.resetScales(scales)
                        self.resetFish(fishes)

                self.pos[0] += (self.catSize - newCatSize) / 4
                self.pos[1] += (self.catSize - newCatSize) / 4

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

                if blockData["water"] == True:
                    if onWall != 0:
                        print("DEATH - water")
                        self.pos = [self.startingPos[0], self.startingPos[1]]
                        self.death += 1                        
                        self.resetScales(scales)
                        self.resetFish(fishes)

        # Y-axis collision detection and handling
        self.pos[1] += svelo[1]
        onGround = False  # Track if player is on the ground
        onRoof = False # Track if player is on the roof

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
                    onRoof = True # Player is on the roof

                if blockData["water"] == True:
                    if onRoof or onGround:
                        print("DEATH - water")
                        self.pos = [self.startingPos[0], self.startingPos[1]]
                        self.death += 1
                        self.resetScales(scales)
                        self.resetFish(fishes)

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
                self.scale_count += 1
                scale.collected = True

        for fish in fishes:
            fishData = fish.get()

            # Check for collision on the X and Y axes
            if (self.pos[0] + width > fishData['x'] and
                self.pos[0] < fishData['x'] + fishData['w'] and
                self.pos[1] + height > fishData['y'] and
                self.pos[1] < fishData['y'] + fishData['h']):

                # Collision detected, collect the fish
                self.fish_count += 1
                fish.collectedFish = True
                print ("Fish collected", self.fish_count)

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
            pawPos = (sliderPos[0] + 25, sliderPos[1] + 60 - int(self.scaleTimer))
            surfaceIn.blit(CAT_PAW_IMAGE, pawPos)
