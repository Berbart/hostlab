from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any, Dict


class TradingPipeline:
    """Simple pipeline utility for saving run artifacts."""

    RUNS_ROOT = Path("runs")

    def __init__(self, config: Dict[str, Any], run_name: str, run_dir: Path | None = None):
        self.config = config
        self.run_name = run_name
        self.run_dir = Path(run_dir) if run_dir else None

    def _write_config(self) -> None:
        config_file = self.run_dir / "config.yml"
        with config_file.open("w", encoding="utf-8") as f:
            for key, value in self.config.items():
                f.write(f"{key}: {value}\n")

    def _prepare_run_dir(self) -> None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.RUNS_ROOT.mkdir(exist_ok=True)
        self.run_dir = self.RUNS_ROOT / f"{timestamp}_{self.run_name}"
        self.run_dir.mkdir(parents=True, exist_ok=True)
        self._write_config()
        (self.run_dir / "tensorboard").mkdir(exist_ok=True)
        (self.run_dir / "model.ckpt").write_text("placeholder", encoding="utf-8")
        (self.run_dir / "metrics.json").write_text("{}", encoding="utf-8")

    def run(self, resume: bool = False) -> Path:
        if not resume or self.run_dir is None:
            self._prepare_run_dir()
        latest = self.RUNS_ROOT / "latest.txt"
        latest.write_text(str(self.run_dir), encoding="utf-8")
        return self.run_dir

    @classmethod
    def load(cls, run_dir: str | Path) -> "TradingPipeline":
        run_dir_path = Path(run_dir)
        config = {}
        config_path = run_dir_path / "config.yml"
        if config_path.exists():
            with config_path.open("r", encoding="utf-8") as f:
                for line in f:
                    if ":" in line:
                        key, value = line.split(":", 1)
                        config[key.strip()] = value.strip()
        run_name = run_dir_path.name.split("_", 2)[-1]
        return cls(config, run_name, run_dir=run_dir_path)

def load_pipeline(run_dir: str | Path) -> TradingPipeline:
    return TradingPipeline.load(run_dir)
