from gui.views.provisionsview import ProvisionsFrame
from gui.widgets.buttonswidget.vagrantmainbuttonswidget import VagrantMainButtons


class VagrantProvisionsView(ProvisionsFrame):

    def __init__(self, master, provisions_configs):
        self.frame_name = 'provisions'
        super().__init__(
            master=master,
            provisions_configs=provisions_configs,
            title='Vagrant'
        )

    def _initialize_main_buttons_frame(self):
        self.main_buttons_frame = VagrantMainButtons(
            master=self,
            provisions_configs=self.provisions_configs,
            wanted_buttons=['configs', 'networks']
        )
