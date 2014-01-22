from pygame.locals import *
import pygame
import os


GRAV = 700


class Player(pygame.sprite.Sprite):
    def __init__(self, game, pos):
        self.game = game
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([25,50])
        self.image.fill((0,0,255))
        self.rect = self.image.get_rect(topleft=(pos[0],pos[1]))
        self.true_location = list(self.rect.topleft)
        self.dx = 0
        self.dy = 0
        self.jump_power = 0
        self.max_jump_power = -375

        self.speed = 300

        self.moving = False
        self.fall = False

    #Credit for most Collision Detection goes to Mekire

    def get_position(self,obstacles):
        """Calculate where our player will end up this frame including
        collisions."""
        if not self.fall:
            self.check_falling(obstacles)
        else:
            self.fall = self.check_collisions((0,self.dy),1,obstacles)
        if self.dx:
            self.check_collisions((self.dx,0),0,obstacles)

    def check_falling(self,obstacles):
        """Checks one pixel below the player to see if the player is still on
        the ground."""
        test_rect = self.rect.move((0,1))
        obs_list = [obs.rect for obs in obstacles]
        if test_rect.collidelist(obs_list) == -1:
            self.fall = True


    def check_collisions(self,offset,index,obstacles):
        """This function checks if a collision would occur after moving offset
        pixels.  If a collision is detected position is decremented by one pixel
        and retested.  This continues until we find exactly how far we can
        safely move, or we decide we can't move."""
        unaltered = True

        self.true_location[index] += offset[index]
        self.rect[index] = self.true_location[index]
        
        while pygame.sprite.spritecollideany(self, obstacles):
            self.rect[index] += (1 if offset[index]<0 else -1)
            unaltered = False
            self.true_location[index] = self.rect[index] 
        return unaltered

    def jump(self):
        """Called when the user presses the jump button."""
        if not self.fall:
            self.jump_power = self.max_jump_power
            self.fall = True

    def update(self, dt):
        mx , my = pygame.mouse.get_pos()
        keys = self.game.keys_pressed
        self.dx = 0
        self.dy = self.jump_power*dt
    
        if 1 in keys:
            if keys[K_d]:
                 self.dx += self.speed*dt
            if keys[K_a]:
                 self.dx -= self.speed*dt
                 
        self.get_position(self.game.solids)

        if self.fall:
            self.jump_power += GRAV*dt
        else:
            self.jump_power = 0

         

            
