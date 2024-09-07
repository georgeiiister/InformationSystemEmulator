import environment

def create_environment():
    env = environment.Environment()
    print(env.path2db)

def main():
    create_environment()

if __name__ == '__main__':
    main()
