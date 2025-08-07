#About the code: I was working on my master thesis, in that we were performing Molecular dynamics simulation where we need to use Linux CLI to command to run each steps line by line so i came up with idea to automate the procedure by using python script so this the one. This code can able to run each command, line after line while ensuring the previous step is completed: 

import subprocess
import os
import time

# File being written by the NPT mdrun step — adjust if needed
watched_file = "npt.cpt"  # could be "npt.log" or "npt.gro" depending on your setup
wait_until_stable_for = 5 * 60  # seconds (5 minutes)

print(f"[INFO] Watching '{watched_file}' for inactivity...")

def file_is_stable(file_path, stable_time=300):
    if not os.path.exists(file_path):
        print("[WARN] File does not exist yet.")
        return False

    last_mod = os.path.getmtime(file_path)
    print("[INFO] Initial last modified time:", time.ctime(last_mod))
    
    while True:
        time.sleep(60)  # check every 60 seconds
        current_mod = os.path.getmtime(file_path)
        
        if current_mod != last_mod:
            print(f"[INFO] File still changing... Last mod time: {time.ctime(current_mod)}")
            last_mod = current_mod
            continue
        
        print(f"[INFO] File unchanged. Waiting {stable_time} seconds to confirm...")
        time.sleep(stable_time)
        final_mod = os.path.getmtime(file_path)
        if final_mod == current_mod:
            print("[INFO] File is stable now. Proceeding.")
            return True
        else:
            print("[INFO] File modified again. Restarting check.")
            last_mod = final_mod

# Wait for file to stop changing
if file_is_stable(watched_file, stable_time=300):
    # Proceed with GROMACS commands
    commands = [
        "gmx_mpi grompp -f md.mdp -p topol.top -c nvt.gro -t npt.cpt -n index.ndx -o md.tpr",
        "gmx_mpi mdrun -deffnm md -tunepme -v -nb gpu -bonded gpu -pme gpu -update gpu -gpu_id 0"
    ]

    for cmd in commands:
        print(f"\n[INFO] Running: {cmd}")
        result = subprocess.run(cmd, shell=True)
        if result.returncode != 0:
            print(f"[ERROR] Command failed: {cmd}")
            break

    print("\n✅ All commands completed.")


