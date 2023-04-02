from PositioningServer.positioningServer import PositioningServer


if __name__ == '__main__':
    mode = input("Please enter the server's working mode (offline/online): ")
    server = PositioningServer("192.168.1.144", 1883, mode)