import sys
from mortality.predict_model import user_input_dash
from mortality.map_viz import run_app

def main():
    if len(sys.argv) != 2:
        print("Please run the following: uv run python -m mortality map or uv run python -m mortality prediction")
        sys.exit(1)
    elif sys.argv[1] == "prediction":
        print("To close the Dash, please press Control+c (MacOs) or press Ctrl (Window)")
        user_input_dash()
    elif sys.argv[1] == "map":
        print("To close the Dash, please press Control+c (MacOs) or press Ctrl (Window)")
        run_app()

if __name__ == "__main__":
    main()