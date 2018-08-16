from databasetools.csv import CSV


def main():
    d = '/Users/Stephen/Desktop/csv.csv'
    data = CSV.read(d)
    print(data)


if __name__ == '__main__':
    main()
