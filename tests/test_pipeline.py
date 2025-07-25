from pathlib import Path
from pipeline import TradingPipeline, load_pipeline


def test_run_and_load(tmp_path, monkeypatch):
    runs_root = tmp_path / "runs"
    monkeypatch.setattr(TradingPipeline, "RUNS_ROOT", runs_root)
    cfg = {"lr": 0.1, "epochs": 1}
    pipe = TradingPipeline(cfg, "demo")
    run_dir = pipe.run()

    # files created
    assert (run_dir / "config.yml").exists()
    assert (run_dir / "metrics.json").exists()
    assert (run_dir / "tensorboard").is_dir()
    assert (run_dir / "model.ckpt").exists()
    latest = runs_root / "latest.txt"
    assert latest.read_text() == str(run_dir)

    # load and resume
    loaded = load_pipeline(run_dir)
    monkeypatch.setattr(loaded, "RUNS_ROOT", runs_root)
    resumed_dir = loaded.run(resume=True)
    assert resumed_dir == run_dir
    assert latest.read_text() == str(run_dir)
