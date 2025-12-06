from picard.file import File, register_file_post_save_processor

from picard.plugins.add_to_collection import batch
from picard.plugins.add_to_collection.override_module import override_module


def post_save_processor(file: File) -> None:
    """
    Processes a file after it has been saved and adds the release to the batch.
    """
    release_id = file.metadata.get("musicbrainz_albumid")
    if release_id:
        batch.add_to_batch(release_id)


def register_processor() -> None:
    with override_module(post_save_processor):
        register_file_post_save_processor(post_save_processor)
