def print_prompt():
    print("db >", end="", flush=True)

def main():
    print_prompt()
    while True:
        try:
            command = input().strip()
        except(EOFError):
            print("\nerror reading input")

        if command == '.exit':
            break
        else:
            print(f"unrecognized command '{command}'.")

    print("Goodbye!")

if __name__ == '__main__':
    main()
        
