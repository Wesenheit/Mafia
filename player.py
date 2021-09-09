class Player():

    def __init__(self,name,frac):
        self.name=name
        self.frac=frac
        self.function=''
        self.perm_effects=[]
        self.temp_effects=[]
        self.alive=True
        self.angel=0
    
    def add_temp(self,effect):
        self.temp_effects.append(effect)
    
    def add_perm(self,effect):
        self.perm_effects.append(effect)
    
    def kill_mafia(self):
        if "medic" in self.temp_effects:
            if "pawulon" in self.temp_effects:
                self.alive=False
                return True
            else:
                return False
        else:
            return True

    def add_angel_counter(self):
        self.angel+=1
        if self.angel==2:
            self.alive=False
            return True
        else:
            return False
    
    def check(self):
        if self.frac < 0:
            if self.function=="kokieta":
                return True
            else:
                return False
        else:
            return True

    def kill(self):
        self.alive=False
        return True

    def kill_admin(self):
        self.alive=False
        return True
        
    def check_status(self):
        return self.frac
        