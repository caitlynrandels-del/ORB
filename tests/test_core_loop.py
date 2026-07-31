from core.oroboro_mind import create_engine


def test_loop_returns_meaning_and_action() -> None:
    engine = create_engine()
    result = engine.loop("artifact discovered", source="pygame")
    assert result["meaning"]["intent"] == "track"
    assert result["action"]["intent"] == "track"
