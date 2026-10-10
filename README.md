# NeuroBot Surgical Robotics Research Lab (simulation-only)

## Run on Ubuntu / WSL
```bash
sudo apt update
sudo apt install python3 python3-tk -y
python3 main.py
```
Arrow keys move the abstract tool marker. **Run safe demo** uses a BFS planner; **Stop** stops it; **Reset** resets the toy world.

## Tests
```bash
python3 -m unittest discover -s tests -v
```

## Current architecture
- Perception: abstract position and target-relative state.
- Memory: bounded episodic event log.
- Planning: BFS shortest safe path.
- Action: discrete moves with boundary/obstacle rejection.
- Feedback: event reward values logged for analysis.

## Important limitations
This is a 2D educational software toy, not a surgical simulator, not a validated robotics controller, and not for clinical decisions or real surgical devices. It models no anatomy, tissue, forces, tool dynamics, or medical workflow. Do not infer medical safety from successful toy navigation.

## Planned research stages
1. Add metrics and reproducible experiment seeds.
2. Add PyTorch DQN in a separate non-clinical navigation benchmark and compare against tabular Q-learning.
3. Add a separate validated robotics simulator only after reviewing its license, capabilities, and safety limitations.
4. Keep any surgical manipulation work sandboxed and simulation-only with independent safety review.
# neurobot-surgical-lab
