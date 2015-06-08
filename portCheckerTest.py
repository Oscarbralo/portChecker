from portChecker import portChecker

def main():
    checker = portChecker('youtsite.com', initPort=1, endPort=200, threads=20)
    checker.checkOpenPorts()


if __name__ == "__main__":
    main()
