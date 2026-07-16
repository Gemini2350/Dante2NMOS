"""Discovery of AES67-capable Dante devices (read path).

Uses netaudio's high-level ``discover()`` helper — the same code path as the
``netaudio device list`` CLI — which browses via mDNS and then queries each
device over the Dante control protocol (UDP 4440) to fill in name, channel
counts and AES67 status. No packet capture / raw sockets and thus no elevated
privileges are needed, only UDP + mDNS reachability (host networking in Docker).

Without netaudio installed an empty list is returned and the gateway works
purely config-based (receivers added by IP in the UI).
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class DanteDevice:
    name: str
    ip: str
    aes67_enabled: bool
    rx_channels: int = 0
    tx_channels: int = 0
    sample_rate: int = 0
    model: str = ""


def _int(value):
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def _model(dev):
    m = getattr(dev, "model", "") or getattr(dev, "model_id", "") or ""
    # model_id often arrives as a raw padded hex id like "_0000000000004420".
    stripped = m.lstrip("_").lstrip("0")
    return stripped or m


def discover_aes67_devices():
    """Return all Dante devices on the network with their AES67 status."""
    try:
        from netaudio._common import discover
    except ImportError:
        print("[dante] netaudio not installed -- working config-based only.")
        return []

    try:
        devices = discover()
    except Exception as e:  # noqa: BLE001 - surface any netaudio runtime error
        print(f"[dante] device discovery failed: {e}")
        return []

    out = []
    for dev in devices.values():
        ip = getattr(dev, "ipv4", None)
        if ip is None:
            continue
        out.append(DanteDevice(
            name=getattr(dev, "name", "") or "",
            ip=str(ip),
            aes67_enabled=bool(getattr(dev, "aes67_configured", False)),
            rx_channels=_int(getattr(dev, "rx_count", 0)),
            tx_channels=_int(getattr(dev, "tx_count", 0)),
            sample_rate=_int(getattr(dev, "sample_rate", 0)),
            model=_model(dev),
        ))
    out.sort(key=lambda d: (not d.aes67_enabled, d.name.lower()))
    return out
