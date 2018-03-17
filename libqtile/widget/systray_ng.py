from . import base
import dbus
from dbus.mainloop.glib import DBusGMainLoop
from pprint import pformat

import daiquiri
import logging

daiquiri.setup(
    outputs=[daiquiri.output.File("/tmp/systray_ng.log")]
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class SystrayNg(base._TextBox):

    orientations = base.ORIENTATION_HORIZONTAL
    defaults = [
        ("update_interval", 1, "Update interval in seconds."),
    ]

    def __init__(self, **config):
        logger.debug("Starting initialization")
        base._TextBox.__init__(self, **config)
        self.add_defaults(SystrayNg.defaults)
        self.items = []
        self._dbus_init()

    def _dbus_init(self):
        self.dbus_loop = DBusGMainLoop()
        self.bus = dbus.SessionBus(mainloop=self.dbus_loop)
        self.status_notifier_watcher = self.bus.get_object(
            'org.kde.StatusNotifierWatcher',
            '/StatusNotifierWatcher'
        )
        self.status_notifier_watcher.connect_to_signal(
            handler_function=self._item_registered,
            signal_name='StatusNotifierItemRegistered'
        )
        self.status_notifier_watcher.connect_to_signal(
            handler_function=self._item_unregistered,
            signal_name='StatusNotifierItemUnregistered'
        )
        # bus.call_async(reply_handler=self._items_registered)
        logger.debug("Hey i'm initialized!")

    def _items_registered(self, *args, **kwargs):
        """Get items already registered (in case we start later)"""
        logger.debug("Registered items")
        logger.debug(pformat(args))
        logger.debug(pformat(kwargs))

    def _item_registered(self, *args, **kwargs):
        """An item has been registered."""
        logger.debug("Registered item")
        logger.debug(pformat(args))
        logger.debug(pformat(kwargs))

    def _item_unregistered(self, *args, **kwargs):
        """An item has been unregistered."""
        logger.debug("Unregistered item")
        logger.debug(pformat(args))
        logger.debug(pformat(kwargs))
