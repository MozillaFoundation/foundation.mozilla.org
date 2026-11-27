"""
Read an animated GIF's structure without decoding any pixel data.

Format reference: https://www.w3.org/Graphics/GIF/spec-gif89a.txt
"""

from typing import NamedTuple

MAGIC = (b"GIF87a", b"GIF89a")

# Frames are composited into RGBA by the decoders in this stack, so this is the
# widest a single pixel gets. Deliberately an upper bound: the point of the
# check this feeds is to stay clear of the memory ceiling, not to predict
# allocation exactly.
BYTES_PER_PIXEL = 4

_EXTENSION = 0x21
_IMAGE_DESCRIPTOR = 0x2C
_TRAILER = 0x3B


class GifParseError(ValueError):
    """The bytes are not a GIF whose structure can be read."""


class GifInfo(NamedTuple):
    width: int
    height: int
    frames: int

    @property
    def animated(self):
        return self.frames > 1

    @property
    def decoded_size(self):
        """
        Upper bound on the bytes one full decode of this GIF would occupy.

        Every frame costs the full canvas, not its own rectangle: a frame may
        cover any sub-region of the logical screen, but it is composited onto
        the whole thing.
        """
        return self.width * self.height * BYTES_PER_PIXEL * self.frames


def _read(fileobj, size, what):
    data = fileobj.read(size)
    if len(data) != size:
        raise GifParseError(f"truncated while reading {what}")
    return data


def _skip_color_table(fileobj, packed):
    """Skip a global or local colour table, if the packed byte says there is one."""
    if packed & 0x80:
        _read(fileobj, 3 * (2 ** ((packed & 0x07) + 1)), "colour table")


def _skip_data_subblocks(fileobj):
    """
    Skip a chain of length-prefixed sub-blocks, terminated by a zero length.

    This is where the compressed image data lives, so skipping rather than
    reading it is the whole reason this module is cheap.
    """
    while True:
        size = _read(fileobj, 1, "sub-block size")[0]
        if size == 0:
            return
        _read(fileobj, size, "sub-block data")


def probe(fileobj) -> GifInfo:
    """
    Return the canvas dimensions and frame count of the GIF in `fileobj`.

    Reads from the current position and leaves the position undefined -- a
    caller that needs the file afterwards must seek it back itself.
    """
    if _read(fileobj, 6, "header") not in MAGIC:
        raise GifParseError("not a GIF")

    screen = _read(fileobj, 7, "logical screen descriptor")
    width = int.from_bytes(screen[0:2], "little")
    height = int.from_bytes(screen[2:4], "little")
    _skip_color_table(fileobj, screen[4])

    frames = 0
    while True:
        block = fileobj.read(1)
        if not block or block[0] == _TRAILER:
            break

        if block[0] == _EXTENSION:
            _read(fileobj, 1, "extension label")
            _skip_data_subblocks(fileobj)
        elif block[0] == _IMAGE_DESCRIPTOR:
            frames += 1
            # 9 bytes: left, top, width, height (2 each), then the packed byte.
            _skip_color_table(fileobj, _read(fileobj, 9, "image descriptor")[8])
            _read(fileobj, 1, "LZW minimum code size")
            _skip_data_subblocks(fileobj)
        else:
            # An introducer we don't recognise means the rest can't be walked,
            # but every frame counted so far is real. Stop rather than guess.
            break

    return GifInfo(width=width, height=height, frames=frames)
