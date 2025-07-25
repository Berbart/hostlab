from __future__ import annotations
from pathlib import Path
from datetime import datetime
import json


class TradingPipeline:
    def __init__(self, config: dict, name: str, runs_dir: str | Path = "runs"):
        self.config = config
        self.name = name
        self.runs_dir = Path(runs_dir)
        self.run_path: Path | None = None

    def run(self, resume: bool = False) -> Path:
        if resume:
            if self.run_path is None:
                raise ValueError("No run_path set for resume")
            # Do not create new directories when resuming
            return self.run_path

        root = self.runs_dir / self.name
        root.mkdir(parents=True, exist_ok=True)
        run_id = datetime.now().strftime("%Y%m%d%H%M%S")
        self.run_path = root / run_id
        self.run_path.mkdir(parents=True, exist_ok=True)

        # Save config
        config_file = self.run_path / "config.yml"
        with open(config_file, "w") as f:
            json.dump(self.config, f)

        # Update latest pointer
        latest_file = self.runs_dir / "latest.txt"
        latest_file.write_text(str(self.run_path))

        return self.run_path

    @classmethod
    def load(cls, run_path: str | Path) -> "TradingPipeline":
        run_path = Path(run_path)
        config_file = run_path / "config.yml"
        with open(config_file) as f:
            config = json.load(f)
        name = run_path.parent.name
        runs_dir = run_path.parents[1]
        pipeline = cls(config=config, name=name, runs_dir=runs_dir)
        pipeline.run_path = run_path
        return pipeline
