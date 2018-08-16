from databasetools.csv import CSV


def main():
    data = [list(range(0, 10)), list(range(10, 20)), list(range(30, 40))]
    d = '/Users/Stephen/Desktop'
    CSV.write(data, file_path=d)


if __name__ == '__main__':
    main()
