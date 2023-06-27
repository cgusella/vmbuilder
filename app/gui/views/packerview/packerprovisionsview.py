from gui.views.provisionsview import ProvisionsFrame
from gui.widgets.buttonswidget.packermainbuttonswidget import PackerMainButtons


class PackerProvisionsView(ProvisionsFrame):

    def __init__(self, master, provisions_configs):
        self.frame_name = 'provisions'
        super().__init__(
            master=master,
            provisions_configs=provisions_configs,
            title='Packer'
        )

    def _initialize_main_buttons_frame(self):
        self.main_buttons_frame = PackerMainButtons(
            master=self,
            provisions_configs=self.provisions_configs,
            wanted_buttons=['configs']
        )
