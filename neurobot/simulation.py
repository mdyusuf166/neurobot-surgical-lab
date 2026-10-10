"""Abstract 2D precision-task world. Not an anatomical/clinical simulator."""
WIDTH, HEIGHT, CELL = 12, 9, 48
START=(1,7)
TARGET=(10,1)
OBSTACLES={(4,2),(4,3),(4,4),(7,4),(7,5),(7,6),(2,2),(3,2),(9,3),(9,4)}
DELTAS={(0,-1):(0,-1),(1,0):(1,0),(0,1):(0,1),(-1,0):(-1,0)}

class SurgicalToyWorld:
    def __init__(self):
        self.start=START; self.target=TARGET; self.obstacles=set(OBSTACLES)
        self.reset()

    def reset(self):
        self.position=self.start; self.steps=0; self.path=[self.position]

    def at_target(self):
        return self.position==self.target

    def move(self,delta):
        dx,dy=delta; x,y=self.position; nxt=(x+dx,y+dy)
        if (nxt[0]<0 or nxt[0]>=WIDTH or nxt[1]<0 or nxt[1]>=HEIGHT or nxt in self.obstacles):
            return {"event":"blocked","reward":-1.0,"position":self.position}
        self.position=nxt; self.steps+=1; self.path.append(nxt)
        if self.at_target(): return {"event":"target_reached","reward":2.0,"position":nxt}
        return {"event":"move","reward":-0.01,"position":nxt}

    def snapshot(self):
        x,y=self.position
        return {"position":self.position,"target_delta":(self.target[0]-x,self.target[1]-y),"steps":self.steps}
