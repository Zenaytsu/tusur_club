import os

class ProgressManager:
    def __init__(self, filename="progress.txt"):
        self.filename = filename
        self.data = {
            "cafe": 0,
            "park": 0,
            "dom_Elcovoi": 0,
            "MakSim": 0,
            "end_1": 0
        }
        self.branch_flags = {
            "branch_male_begin": 0,
            "branch_svidanie": 0,
            
            "branch_cafe": 0,
            "branch_park": 0,
            "branch_end_1": 0, 
            "branch_maksim": 0,
            
            "branch_dom_Elcovoi": 0
        }
        self.load_progress()

    def load_progress(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if "=" in line:
                        key, value = line.split("=")
                        if key in self.data:
                            self.data[key] = int(value)
                        elif key in self.branch_flags:
                            self.branch_flags[key] = int(value)
            print(f"[PROGRESS] Loaded progress: {self.data}")
            print(f"[PROGRESS] Loaded branches: {self.branch_flags}")

    def save_progress(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            for key, value in self.data.items():
                f.write(f"{key}={value}\n")
            for key, value in self.branch_flags.items():
                f.write(f"{key}={value}\n")
        print(f"[PROGRESS] Saved progress: {self.data}")
        print(f"[PROGRESS] Saved branches: {self.branch_flags}")

    def mark_ending_completed(self, ending_name):
        if ending_name in self.data:
            self.data[ending_name] = 1
            self.save_progress()
            print(f"[PROGRESS] Marked ending as completed: {ending_name}")

    def mark_branch_completed(self, branch_name):
        if branch_name in self.branch_flags:
            self.branch_flags[branch_name] = 1
            self.save_progress()
            print(f"[PROGRESS] Marked branch as completed: {branch_name}")

    def has_completed_any_ending(self):
        result = any(v == 1 for v in self.data.values())
        print(f"[PROGRESS] Has any ending completed: {result}")
        return result

    def has_completed_branch(self, branch_name):
        result = self.branch_flags.get(branch_name, 0) == 1
        print(f"[PROGRESS] Has branch {branch_name} completed: {result}")
        return result

    def get_completed_endings_count(self):
        count = sum(1 for v in self.data.values() if v == 1)
        print(f"[PROGRESS] Completed endings count: {count}")
        return count

    def get_completed_branches_count(self):
        count = sum(1 for v in self.branch_flags.values() if v == 1)
        print(f"[PROGRESS] Completed branches count: {count}")
        return count

    def reset_progress(self):
        for key in self.data:
            self.data[key] = 0
        for key in self.branch_flags:
            self.branch_flags[key] = 0
        self.save_progress()
        print("[PROGRESS] Progress reset to zero")

    def get_progress_summary(self):
        completed_endings = [k for k, v in self.data.items() if v == 1]
        completed_branches = [k for k, v in self.branch_flags.items() if v == 1]
        
        summary = f"Концовки: {len(completed_endings)}/{len(self.data)}, "
        summary += f"Ветки: {len(completed_branches)}/{len(self.branch_flags)}"
        return summary