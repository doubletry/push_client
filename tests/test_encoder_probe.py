"""encoder_probe 模块单元测试。

不依赖真实的 FFmpeg / 硬件，通过 mock ``subprocess.run`` 验证决策逻辑。
"""

from __future__ import annotations

from unittest import mock

from beaverpush.services import encoder_probe


def _fake_completed(returncode=0, stdout=""):
    cp = mock.MagicMock()
    cp.returncode = returncode
    cp.stdout = stdout
    return cp


class TestFFmpegListsEncoder:
    def test_present_in_listing(self):
        listing = " V..... libx264              H.264\n V..... h264_nvenc           NVIDIA\n"
        with mock.patch(
            "beaverpush.services.encoder_probe.subprocess.run",
            return_value=_fake_completed(stdout=listing),
        ):
            assert encoder_probe._ffmpeg_lists_encoder("libx264") is True
            assert encoder_probe._ffmpeg_lists_encoder("h264_nvenc") is True

    def test_missing_from_listing(self):
        with mock.patch(
            "beaverpush.services.encoder_probe.subprocess.run",
            return_value=_fake_completed(stdout=" V..... libx264 H.264\n"),
        ):
            assert encoder_probe._ffmpeg_lists_encoder("h264_qsv") is False

    def test_ffmpeg_missing_returns_false(self):
        with mock.patch(
            "beaverpush.services.encoder_probe.subprocess.run",
            side_effect=FileNotFoundError(),
        ):
            assert encoder_probe._ffmpeg_lists_encoder("libx264") is False


class TestProbeEncoder:
    def test_success(self):
        with mock.patch(
            "beaverpush.services.encoder_probe.subprocess.run",
            return_value=_fake_completed(returncode=0),
        ):
            assert encoder_probe._probe_encoder("h264_qsv") is True

    def test_failure_returncode(self):
        with mock.patch(
            "beaverpush.services.encoder_probe.subprocess.run",
            return_value=_fake_completed(returncode=1),
        ):
            assert encoder_probe._probe_encoder("h264_nvenc") is False

    def test_timeout_treated_as_unavailable(self):
        import subprocess as sp
        with mock.patch(
            "beaverpush.services.encoder_probe.subprocess.run",
            side_effect=sp.TimeoutExpired(cmd="ffmpeg", timeout=5),
        ):
            assert encoder_probe._probe_encoder("h264_nvenc") is False


class TestDetectAvailableEncoders:
    def test_only_software_when_no_hardware(self):
        # 软件编码器在列表中，硬件编码器列表中存在但 _probe_encoder 失败
        with mock.patch.object(
            encoder_probe, "_ffmpeg_lists_encoder", return_value=True,
        ), mock.patch.object(
            encoder_probe, "_probe_encoder", return_value=False,
        ):
            result = encoder_probe.detect_available_encoders()
        assert "libx264" in result
        assert "libx265" in result
        assert "h264_nvenc" not in result
        assert "h264_qsv" not in result

    def test_includes_hardware_when_probe_succeeds(self):
        with mock.patch.object(
            encoder_probe, "_ffmpeg_lists_encoder", return_value=True,
        ), mock.patch.object(
            encoder_probe, "_probe_encoder",
            side_effect=lambda name: name in ("h264_qsv", "hevc_qsv"),
        ):
            result = encoder_probe.detect_available_encoders()
        assert "libx264" in result
        assert "h264_qsv" in result
        assert "hevc_qsv" in result
        assert "h264_nvenc" not in result

    def test_skips_codec_not_in_ffmpeg_listing(self):
        listed = {"libx264"}  # 只有 libx264 在 -encoders 输出里
        with mock.patch.object(
            encoder_probe, "_ffmpeg_lists_encoder",
            side_effect=lambda name: name in listed,
        ), mock.patch.object(
            encoder_probe, "_probe_encoder", return_value=True,
        ):
            result = encoder_probe.detect_available_encoders()
        assert result == ["libx264"]
