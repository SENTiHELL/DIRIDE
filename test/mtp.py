
#from pymtp import MTP
#mtp = MTP()
#mtp.connect()
#print(mtp.get_modelname())
#print(mtp.get_batterylevel())
import os

from gi.repository import Gio, GObject, GLib
VOLUME_NAME='Cintiq Companion Hybrid 13HD'

dir = '/'
def mount_done_cb(obj, res, user_data):
    # print(obj, res, user_data)
    # obj.mount_enclosing_volume_finish(res)
    obj.mount_finish(res)
    # print('done.')
    # print(1, obj.get_name(), obj.get_uuid(), obj.get_mount(), obj.get_drive())
    # print(2, obj.get_mount().get_uuid())
    # print(3, obj.get_mount().get_default_location().get_path())
    print(4, obj.get_mount().get_root().get_path())
    global dir
    dir = obj.get_mount().get_root().get_path()
    # print(5, obj.get_mount().get_volume())
    # print(6, obj.get_mount().get_drive())
    user_data.quit()

def main():
    mo = Gio.MountOperation()
    mo.set_anonymous(True)

    vm = Gio.VolumeMonitor.get()
    # print(dir(vm))
    # print(vm.get_mount_for_uuid(VOLUME_UUID))
    # print(vm.get_volume_for_uuid(VOLUME_UUID))
    loop = GLib.MainLoop()
    found = False
    for v in vm.get_volumes():
        name = v.get_name()

        if name == VOLUME_NAME:
            mount = v.get_mount()
            print(name, v.get_uuid(), v.get_mount(), v.get_drive())
            if not mount:
                v.mount(0, mo, None, mount_done_cb, loop)
                # print(name, v.get_uuid(), v.get_mount(), v.get_drive())
                found = True

    if found:
        loop.run()

if __name__ == "__main__":
    main()


