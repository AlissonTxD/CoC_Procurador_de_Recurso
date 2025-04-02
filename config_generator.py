import json

GOLD_CUT = (180, 145, 310, 175)
ELIXIR_CUT = (180, 188, 310, 217)
DARK_CUT = (180, 230, 310, 260)
TARGET_PIXEL = (1644, 733)


def save_json(obj: any, path: str) -> None:
    with open(path, "w") as fp:
        json.dump(obj, fp, indent=2)


config = {
    "generator": {
        "goldcut": [GOLD_CUT[0], GOLD_CUT[1], GOLD_CUT[2], GOLD_CUT[3]],
        "elixircut": [ELIXIR_CUT[0], ELIXIR_CUT[1], ELIXIR_CUT[2], ELIXIR_CUT[3]],
        "darkcut": [DARK_CUT[0], DARK_CUT[1], DARK_CUT[2], DARK_CUT[3]],
    },
    "target": [TARGET_PIXEL[0], TARGET_PIXEL[1]],
}
save_json(config, "config.json")
