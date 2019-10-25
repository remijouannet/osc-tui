from npyscreen import *
import pyperclip
inspector = None
import sys
import main

def add_inspector(form):
    y, x = form.useable_space()
    a = form.add_widget(Textfield, rely = int(y/2+1), value="No instance selected",
            editable = False)
    run_stop = form.add_widget(ButtonPress, name="RUN")
    restart = form.add_widget(ButtonPress, name="RESTART")
    force_stop = form.add_widget(ButtonPress, name="FORCE STOP")
    cp_ip = form.add_widget(ButtonPress, name="COPY IP")
    exit = form.add_widget(ButtonPress, name="EXIT")
    def stop():
        main.kill_threads()
        main.APP.switchForm('MAIN')
    exit.whenPressed = stop
    i = Inspector(a, run_stop, restart, force_stop,cp_ip)
    return i

class Inspector():
    def __init__(self, name_label, run_stop, restart,
            force_stop, cp_ip):
        self.copy_ip = cp_ip
        self.name_label = name_label
        self.run_stop = run_stop
        self.force_stop = force_stop
        self.restart = restart
    def set_value(self, vm):
        self.vm = vm
        self.name = vm[1]
        self.name_label.value = 'Instance selected: ' + self.name
        self.run_stop.name = 'RUN' if vm[0] == 'stopped' else 'STOP'
        self.name_label.update()
        self.run_stop.update()
        #Operations availables:
        def copy_ip():
            pyperclip.copy(vm[5])
        def start_vm():
            main.GATEWAY.StartVms(VmIds = [vm[2]])
        def stop_vm():
            main.GATEWAY.StopVms(VmIds = [vm[2]])
        def force_stop_vm():
            main.GATEWAY.StopVms(ForceStop = True, VmIds = [vm[2]])
        def restart_vm():
            main.GATEWAY.RebootVms(VmIds = [vm[2]])
        self.copy_ip.whenPressed = copy_ip
        self.run_stop.whenPressed = start_vm if vm[0] == 'stopped' else stop_vm
        self.force_stop.whenPressed = force_stop_vm
        #self.restart.whenPressed = restart_vm

class Toolbar(SimpleGrid):
    def __init__(self, screen, *args , **keywords):
        super().__init__(screen, *args , **keywords)
        self.values = [('RENAME STOP RUN RESTART'.split())]

class VmInspector(BoxTitle):
    _contained_widget = Toolbar
    def __init__(self, screen, *args , **keywords):
        super().__init__(screen, *args, **keywords)
        self.scroll_exit=True
        self.exit_left = True
        self.exit_right = True
    def set_value(self, values):
        self.name = values[1]
        self.update()
