from PositioningServer.fingerprintDatabase import *
import time

class DataOrganizer:
    def __init__(self):
        self.attributes = {'beacon1': 'channel1', 'beacon2': 'channel2', 'beacon3': 'channel3', 'beacon4': 'channel4',
                           'beacon5': 'channel5', 'beacon6': 'channel6', 'beacon7': 'channel7', 'beacon8': 'channel8',
                           'beacon9': 'channel9', 'beacon10': 'channel10', 'beacon11': 'channel11', 'beacon12': 'channel12',
                           'beacon13': "channel13", 'beacon14': 'channel14', 'beacon15': 'channel15', 'beacon16': 'channel16',
                           'beacon17': 'channel17', 'beacon18': 'channel18', 'beacon19': 'channel19', 'beacon20': 'channel20'}
    @db_session
    def create_fingerprints(self):
        scan_count = max(ad.scan_number for ad in Advertisement)
        for scan in range(1,scan_count+1):
            scan_advertisements = select(ad for ad in Advertisement if ad.scan_number == scan)[:]
            if len(scan_advertisements)!=0:
                info = {}
                for curr_scan in scan_advertisements:
                    info[curr_scan.advertised_device.beacon_name] = [curr_scan.advertised_channel, curr_scan.rssi]
                fingerprint = Fingerprint(scan_number=scan, date=scan_advertisements[0].date,
                                          location=scan_advertisements[0].location)
                for curr_info in info:
                    fingerprint.__setattr__(curr_info, info[curr_info][1])
                    fingerprint.__setattr__(self.attributes[curr_info], info[curr_info][0])
            commit()


dataOrganizer = DataOrganizer()
dataOrganizer.create_fingerprints()