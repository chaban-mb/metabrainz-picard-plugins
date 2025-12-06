from PyQt5.QtCore import QTimer
from picard import log
from picard.collection import Collection, user_collections
from picard.plugins.add_to_collection import settings

_releases_to_add = set()
_timer = QTimer()
_timer.setSingleShot(True)
_timer.setInterval(5000)

def _send_batch():
    """
    Sends the batched releases to the selected collection.
    """
    collection_id = settings.collection_id()
    if not collection_id:
        log.error("cannot find collection ID setting")
        return

    collection: Collection = user_collections.get(collection_id)
    if not collection:
        log.error(f"cannot find collection with id {collection_id}")
        return

    releases_to_add_now = _releases_to_add.copy()
    _releases_to_add.clear()

    releases_to_add_filtered = {
        release_id
        for release_id in releases_to_add_now
        if release_id not in collection.releases
    }

    if releases_to_add_filtered:
        log.debug("Adding releases %r to %r", releases_to_add_filtered, collection.name)
        collection.add_releases(releases_to_add_filtered, callback=lambda: None)


_timer.timeout.connect(_send_batch)


def add_to_batch(release_id: str):
    """
    Adds a release to the batch and starts the timer.
    """
    _releases_to_add.add(release_id)
    _timer.start()