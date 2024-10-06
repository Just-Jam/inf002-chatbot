import json

def main():
    print("Hello World")
    with open('response.json', 'r') as file:
        data = json.load(file)

    # Print the data
    print(data['choices'][0]['message']['content'])


if __name__ == "__main__":
    main()
