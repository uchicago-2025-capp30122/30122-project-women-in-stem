import sys
from .predict_model import user_prediction

def main():
    if len(sys.argv) != 2:
        print("Please run the following: uv run -m mortality map or v run -m mortality prediction")
        sys.exit(1)
    elif sys.argv[1] == "prediction":
        region = input("Enter Your Region: ")
        race = input("Enter Your Race: ")
        education = input("Enter Your Region: ")
        age = input("Enter Your Region: ")
        user_prediction(region, race, education, age)
        # state = input("Enter State (if no preference please press Enter): ")

if __name__ == "__main__":
    main()