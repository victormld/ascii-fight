from playscii import GameManager, GameObject
from playscii.input import Input
from threading import Timer
from random import randint

FIGHTER_PUNCH_RENDER = "(=O*_*)=O  "
FIGHTER_RENDER = "(=O*_*)O"
ENEMY_RENDER = "   Q(*_*Q)"
ENEMY_PUNCH_RENDER = " Q=(*_*Q)"

WIDTH, HEIGHT, SPEED = 90, 10, 30

class FightManager(GameManager):
    def __init__(self):
        super().__init__((WIDTH, HEIGHT))
        self.fighter = Fighter(pos=(15, 0))
        self.fighter_punch = FighterPunch(pos=(self.fighter.x,0))
        self.enemy = Enemy(pos=(60, 0))
        self.enemy_punch = EnemyPunch(pos=(self.enemy.x, 0))
        self.fighter_hp = 100
        self.enemy_hp = 100
        self.cooling = False
        
    def setup(self):
        self.time = 0
        self.add_object(self.fighter)
        self.add_object(self.enemy)
        self.set_title("Ascii Fighter")
        
    def update(self):
        self.time += self.delta_time
        #Movimiento de fighter
        if Input.get_key('right') and self.fighter.x < self.width - self.fighter.width:
            self.fighter.x += SPEED * self.delta_time
        elif Input.get_key('left') and self.fighter.x > 0:
            self.fighter.x -= SPEED * self.delta_time
        #Movimiento del fighter_punch
        if Input.get_key('right') and self.fighter_punch.x < self.width - self.fighter_punch.width:
            self.fighter_punch.x += SPEED * self.delta_time
        elif Input.get_key('left') and self.fighter_punch.x > 0:
            self.fighter_punch.x -= SPEED * self.delta_time
        #Llamado a fighter_punch
        if Input.get_key_down('space'):
            if not self.cooling:
                self.cooling = True
                
                self.punch()
                Timer(0.07, self.punch_out).start()
                
                Timer(0.2, self.cool_off).start()
                
        if self.enemy_hp == 0:
            self.set_title("Fighter Wins")
            
        if Input.get_key_down('q'):
            self.quit()
    
    def cool_off(self):
        self.cooling = False
        
    def punch(self):
        self.game_objects.remove(self.fighter)
        self.add_object(self.fighter_punch)
        if self.fighter.on_collision(self.enemy):
            self.enemy_hp -= 20
        
    def punch_out(self):
        self.game_objects.remove(self.fighter_punch)
        self.add_object(self.fighter)
    
        

class Fighter(GameObject):
    def __init__(self, pos):
        super().__init__(pos, FIGHTER_RENDER, (4, 2))
        
    def update(self):
        pass


class FighterPunch(GameObject):
    def __init__(self, pos):
        super().__init__(pos, FIGHTER_PUNCH_RENDER, (4, 2))
        
    def update(self):
        pass
    
class Enemy(GameObject):
    def __init__(self, pos):
        super().__init__(pos, ENEMY_RENDER, (4, 2))
        self.dead = False

    def update(self):
        #if self.y >= -5:
        #    self.y -= ENEMY_SPEED * self.delta_time
        #else:
        #    self.dead = True
        pass

    def check_death(self, bullets):
        for bullet in bullets:
            if bullet.on_collision(self):
                bullet.hit = True
                return True
        return False
    
class EnemyPunch(GameObject):
    def __init__(self, pos):
        super().__init__(pos,ENEMY_PUNCH_RENDER, (4, 2))
        self.dead = False

    def update(self):
        #if self.y >= -5:
        #    self.y -= ENEMY_SPEED * self.delta_time
        #else:
        #    self.dead = True
        pass

    def check_death(self, bullets):
        for bullet in bullets:
            if bullet.on_collision(self):
                bullet.hit = True
                return True
        return False

if __name__ == '__main__':
    game_manager = FightManager()
    game_manager.start()