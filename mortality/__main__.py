import sys
from .predict_model import user_input_dash

def main():
    if len(sys.argv) != 2:
        print("Please run the following: uv run python -m mortality map or uv run python -m mortality prediction")
        sys.exit(1)
    elif sys.argv[1] == "prediction":
        print("To close the Dash, please press Control+c (MacOs) or press XX (Window)")
        user_input_dash()
if __name__ == "__main__":
    main()