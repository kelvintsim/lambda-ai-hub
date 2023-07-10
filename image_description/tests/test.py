from handler import lambda_handler

def main():
    event = {'url': 'https://media-cldnry.s-nbcnews.com/image/upload/t_fit-1240w,f_auto,q_auto:best/rockcms/2023-03/230321-donald-trump-ivanka-eric-mn-1430-c95c85.jpg'}
    print(lambda_handler(event, None))

if __name__ == "__main__":
    main()
