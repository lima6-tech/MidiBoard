import storage

try:
    storage.remount("/", readonly=False)
    m = storage.getmount("/")
    m.lablel = "MIDIPAD"
    storage.remount("/", readonly=True)
except:
    pass