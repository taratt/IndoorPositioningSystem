from PositioningServer.positioningServer import PositioningServer


if __name__ == '__main__':
    valid_modes = {"online", "offline"}
    while True:
        mode = input("Please enter the server's working mode (offline/online): ")
        if mode in valid_modes:
            break
        print("Invalid mode. Try again.")
    if mode == "offline":
        level = int(input("Please enter the level for scene analysis:"))
        scan_count = int(input("Please enter the scan number for scene analysis:"))
    server = PositioningServer("192.168.43.245", 1883, mode, level, scan_count)