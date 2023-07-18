import dotenv
dotenv.load_dotenv()
from handler import lambda_handler, EventDict

def main():
    event: EventDict = {'type': 'Food', 'name': '紅燒牛肉麵'}
    print(lambda_handler(event, None))

if __name__ == "__main__":
    main()
