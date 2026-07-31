from core.oroboro_mind import create_engine


def main() -> None:
    engine = create_engine()
    result = engine.loop("hello from the new structure", source="main")
    print(result["state"])
    print(result["action"])


if __name__ == "__main__":
    main()
