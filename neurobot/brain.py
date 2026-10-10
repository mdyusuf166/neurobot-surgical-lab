"""Inspectable cognitive scaffold: planner + bounded episodic memory.
Neural-network learning is intentionally a later phase; this file does not claim human-level cognition.
"""
from collections import deque
from .simulation import WIDTH, HEIGHT

class CognitiveBrain:
    def __init__(self):
        self.episodic_memory=deque(maxlen=500)
        self.planner_name="BFS safety-constrained baseline"

    def reset_episode(self):
        self.episodic_memory.clear()

    def remember(self,observation,event):
        self.episodic_memory.append({
            "observation":observation,
            "event":event.get("event","unknown"),
            "reward":event.get("reward",0.0)
        })

    def plan_next(self,world):
        """BFS returns the first safe step on a shortest route to target."""
        start=world.position; goal=world.target
        queue=[(start,[])]
        seen={start}
        while queue:
            pos,path=queue.pop(0)
            if pos==goal:
                return path[0] if path else (0,0)
            x,y=pos
            for delta in [(0,-1),(1,0),(0,1),(-1,0)]:
                dx,dy=delta; nxt=(x+dx,y+dy)
                if (0<=nxt[0]<WIDTH and 0<=nxt[1]<HEIGHT
                    and nxt not in world.obstacles and nxt not in seen):
                    seen.add(nxt); queue.append((nxt,path+[delta]))
        return (0,0)
