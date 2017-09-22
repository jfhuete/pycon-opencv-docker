import red_ball
import tinto_verano
import face

if __name__ == "__main__":
    selection = 0
    while selection not in list(range(1, 4)):
        print('\n\nSelect the example:\n'+40*'-')
        print('\t1. Red ball')
        print('\t2. Where is my tinto de verano')
        print('\t3. My Face')
        try:
            selection = int(input('\nSelect the app: '))
        except ValueError:
            print('\nPut a number of the list!!')

    if selection == 1:
        app = red_ball
    if selection == 2:
        app = tinto_verano
    if selection == 3:
        app = face

    app.main()
