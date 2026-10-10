"""NeuroBot Surgical Robotics Research Lab — simulation-only toy.
Run: python3 main.py
This is NOT a medical simulator and must never be used for clinical decisions or real surgery.
"""
import tkinter as tk
from tkinter import ttk
from neurobot.brain import CognitiveBrain
from neurobot.simulation import SurgicalToyWorld, WIDTH, HEIGHT, CELL

class NeuroBotLab:
    def __init__(self, root):
        self.root=root
        root.title("NeuroBot | Brain-Inspired Surgical Robotics Research Lab (SIMULATION ONLY)")
        root.resizable(False,False)
        self.world=SurgicalToyWorld()
        self.brain=CognitiveBrain()
        self.running=False
        self.canvas=tk.Canvas(root,width=WIDTH*CELL,height=HEIGHT*CELL,bg="#101827",highlightthickness=0)
        self.canvas.grid(row=0,column=0,columnspan=3,padx=12,pady=12)
        self.status=tk.StringVar()
        ttk.Label(root,textvariable=self.status,justify="left").grid(row=1,column=0,columnspan=3,sticky="w",padx=14)
        ttk.Button(root,text="Run safe demo",command=self.run_demo).grid(row=2,column=0,padx=8,pady=10,sticky="ew")
        ttk.Button(root,text="Stop",command=self.stop).grid(row=2,column=1,padx=8,pady=10,sticky="ew")
        ttk.Button(root,text="Reset",command=self.reset).grid(row=2,column=2,padx=8,pady=10,sticky="ew")
        self.log=tk.Text(root,width=76,height=8,state="disabled",font=("Consolas",9))
        self.log.grid(row=3,column=0,columnspan=3,padx=12,pady=(0,12))
        root.bind("<Up>",lambda e:self.manual((0,-1)))
        root.bind("<Down>",lambda e:self.manual((0,1)))
        root.bind("<Left>",lambda e:self.manual((-1,0)))
        root.bind("<Right>",lambda e:self.manual((1,0)))
        root.bind("<Escape>",lambda e:root.destroy())
        self.say("Research sandbox ready. Use arrow keys or Run safe demo.")
        self.say("Safety: abstract grid only; no anatomy, tissue, patient data, or real-device control.")
        self.draw()

    def say(self,msg):
        self.log.configure(state="normal"); self.log.insert("end",msg+"\n")
        self.log.see("end"); self.log.configure(state="disabled")

    def manual(self,delta):
        if self.running: return
        event=self.world.move(delta)
        self.brain.remember(self.world.snapshot(),event)
        self.say(f"Manual action: {event['event']} | reward={event['reward']:+.2f}")
        self.draw()

    def run_demo(self):
        if self.running: return
        self.running=True
        self.say("Safe demo started: planner proposes moves; world rejects unsafe moves.")
        self._demo_step()

    def _demo_step(self):
        if not self.running: return
        if self.world.at_target():
            self.running=False
            self.say(f"Toy target reached in {self.world.steps} accepted moves. This is not surgical validation.")
            self.draw(); return
        action=self.brain.plan_next(self.world)
        event=self.world.move(action)
        self.brain.remember(self.world.snapshot(),event)
        if event["event"]=="blocked": self.say("Planner action blocked by toy safety boundary.")
        self.draw()
        self.root.after(180,self._demo_step)

    def stop(self):
        self.running=False
        self.say("Demo stopped.")

    def reset(self):
        self.running=False; self.world.reset(); self.brain.reset_episode()
        self.say("Toy world reset. Persistent learning is not claimed in this prototype.")
        self.draw()

    def draw(self):
        c=self.canvas;c.delete("all")
        for y in range(HEIGHT):
            for x in range(WIDTH):
                p=(x,y); fill="#f8fafc"
                if p in self.world.obstacles: fill="#475569"
                if p==self.world.target: fill="#86efac"
                c.create_rectangle(x*CELL,y*CELL,(x+1)*CELL,(y+1)*CELL,fill=fill,outline="#cbd5e1")
                if p in self.world.obstacles:
                    c.create_text(x*CELL+CELL/2,y*CELL+CELL/2,text="×",fill="#e2e8f0",font=("Arial",17))
                elif p==self.world.target:
                    c.create_text(x*CELL+CELL/2,y*CELL+CELL/2,text="TARGET",fill="#14532d",font=("Arial",8,"bold"))
        for x,y in self.world.path:
            c.create_oval(x*CELL+CELL*.42,y*CELL+CELL*.42,x*CELL+CELL*.58,y*CELL+CELL*.58,fill="#93c5fd",outline="")
        x,y=self.world.start
        c.create_text(x*CELL+CELL/2,y*CELL+CELL/2,text="START",fill="#1d4ed8",font=("Arial",8,"bold"))
        x,y=self.world.position
        c.create_oval(x*CELL+9,y*CELL+9,x*CELL+CELL-9,y*CELL+CELL-9,fill="#fb923c",outline="#9a3412",width=2)
        self.status.set(
            f"Simulation only | step={self.world.steps} | target reached={self.world.at_target()} | "
            f"memory events={len(self.brain.episodic_memory)} | planner={self.brain.planner_name}"
        )

if __name__=="__main__":
    root=tk.Tk(); app=NeuroBotLab(root); root.mainloop()
