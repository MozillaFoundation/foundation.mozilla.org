import io

from django.test import SimpleTestCase

from foundation_cms.images import gif


def _data_sub_blocks(payload):
    """Chunk payload into the format's length-prefixed sub-blocks (max 255 bytes)."""
    out = b""
    for start in range(0, len(payload), 255):
        chunk = payload[start : start + 255]
        out += bytes([len(chunk)]) + chunk
    return out + b"\x00"  # terminator


def build_gif(
    width=4,
    height=3,
    frames=1,
    global_table=True,
    local_table=False,
    extensions=True,
    frame_payload=b"\x4c\x01",
):
    """
    Assemble a structurally valid GIF89a with a known frame count.

    Hand-built rather than generated with Pillow so these tests exercise the
    parser against the format itself, not against one encoder's output.
    """
    packed = 0x80 if global_table else 0x00
    out = io.BytesIO()
    out.write(b"GIF89a")
    out.write(width.to_bytes(2, "little"))
    out.write(height.to_bytes(2, "little"))
    out.write(bytes([packed, 0, 0]))
    if global_table:
        out.write(b"\x00\x00\x00\xff\xff\xff")  # 2 entries, 3 bytes each

    for _ in range(frames):
        if extensions:
            out.write(b"\x21\xf9\x04\x00\x00\x00\x00\x00")  # graphic control extension
        local_packed = 0x80 if local_table else 0x00
        out.write(b"\x2c")
        out.write(b"\x00\x00\x00\x00")  # left, top
        out.write(width.to_bytes(2, "little"))
        out.write(height.to_bytes(2, "little"))
        out.write(bytes([local_packed]))
        if local_table:
            out.write(b"\x00\x00\x00\xff\xff\xff")
        out.write(b"\x02")  # LZW minimum code size
        out.write(_data_sub_blocks(frame_payload))

    out.write(b"\x3b")  # trailer
    out.seek(0)
    return out


class ProbeTests(SimpleTestCase):
    def test_reads_dimensions(self):
        info = gif.probe(build_gif(width=640, height=480))
        self.assertEqual((info.width, info.height), (640, 480))

    def test_counts_a_single_frame(self):
        self.assertEqual(gif.probe(build_gif(frames=1)).frames, 1)

    def test_counts_many_frames(self):
        self.assertEqual(gif.probe(build_gif(frames=109)).frames, 109)

    def test_skips_graphic_control_extensions(self):
        """Extensions sit between frames and must not be counted as frames."""
        with_ext = gif.probe(build_gif(frames=5, extensions=True))
        without_ext = gif.probe(build_gif(frames=5, extensions=False))
        self.assertEqual(with_ext.frames, 5)
        self.assertEqual(without_ext.frames, 5)

    def test_skips_local_colour_tables(self):
        """A local table shifts where the frame's data begins."""
        self.assertEqual(gif.probe(build_gif(frames=3, local_table=True)).frames, 3)

    def test_handles_no_global_colour_table(self):
        info = gif.probe(build_gif(frames=2, global_table=False))
        self.assertEqual(info.frames, 2)

    def test_animated_flag(self):
        self.assertFalse(gif.probe(build_gif(frames=1)).animated)
        self.assertTrue(gif.probe(build_gif(frames=2)).animated)

    def test_accepts_gif87a(self):
        data = build_gif().getvalue().replace(b"GIF89a", b"GIF87a", 1)
        self.assertEqual(gif.probe(io.BytesIO(data)).frames, 1)

    def test_rejects_non_gif(self):
        with self.assertRaises(gif.GifParseError):
            gif.probe(io.BytesIO(b"\x89PNG\r\n\x1a\n" + b"\x00" * 64))

    def test_rejects_empty_file(self):
        with self.assertRaises(gif.GifParseError):
            gif.probe(io.BytesIO(b""))

    def test_rejects_truncated_file(self):
        truncated = build_gif(frames=4).getvalue()[:20]
        with self.assertRaises(gif.GifParseError):
            gif.probe(io.BytesIO(truncated))

    def test_missing_trailer_still_counts_frames(self):
        """A GIF cut off after its last frame should not lose the frames it has."""
        data = build_gif(frames=3).getvalue()[:-1]  # drop the trailer
        self.assertEqual(gif.probe(io.BytesIO(data)).frames, 3)


class DecodedSizeTests(SimpleTestCase):
    def test_multiplies_area_frames_and_depth(self):
        info = gif.probe(build_gif(width=100, height=50, frames=10))
        self.assertEqual(info.decoded_size, 100 * 50 * 4 * 10)

    def test_matches_the_asset_that_broke_production(self):
        """
        The real numbers behind GIF_MAX_FRAME_VOLUME, kept here so the constant
        is not mistaken for an arbitrary choice: 950x950x109 is the GIF that
        killed a Standard-2X worker during upload.
        """
        info = gif.probe(build_gif(width=950, height=950, frames=109))
        self.assertEqual(info.decoded_size, 393_490_000)
        self.assertGreater(info.decoded_size, 100 * 1024 * 1024)

    def test_small_animated_gif_stays_well_under_the_limit(self):
        """The 220x154x21 GIF that uploaded without trouble."""
        info = gif.probe(build_gif(width=220, height=154, frames=21))
        self.assertLess(info.decoded_size, 10 * 1024 * 1024)


class LargePayloadTests(SimpleTestCase):
    def test_walks_frames_split_across_many_sub_blocks(self):
        """
        Real image data spans many maximal (255-byte) sub-blocks per frame.
        The toy frames above use one tiny block, so cover the chained case too.
        """
        gif_bytes = build_gif(frames=4, frame_payload=b"\xab" * 1000)
        info = gif.probe(gif_bytes)
        self.assertEqual(info.frames, 4)
