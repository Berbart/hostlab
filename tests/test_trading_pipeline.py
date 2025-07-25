import os
import sys
from pathlib import Path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from trading.pipeline import TradingPipeline


def test_trading_pipeline_run_and_resume(tmp_path):
    runs_dir = tmp_path / "runs"
    config = {"param": 1}
    pipeline = TradingPipeline(config, name="demo", runs_dir=runs_dir)

    run_path = pipeline.run()
    assert run_path.exists()
    assert (run_path / "config.yml").is_file()

    latest_file = runs_dir / "latest.txt"
    assert latest_file.is_file()
    assert latest_file.read_text() == str(run_path)

    loaded = TradingPipeline.load(run_path)
    loaded.run(resume=True)

    # ensure no new directory created
    subdirs = [p for p in (runs_dir / "demo").iterdir() if p.is_dir()]
    assert len(subdirs) == 1
    assert subdirs[0] == run_path
