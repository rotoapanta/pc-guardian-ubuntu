"""PC Guardian Ubuntu command-line entry point."""

from core.config import load_config
from core.guardian import PCGuardian
from core.logger import setup_logger
from core.version import __version__


def main() -> None:
    """Load configuration and start the monitoring loop."""
    cfg = load_config()
    logger = setup_logger(cfg)

    print("=" * 70)
    print(f" PC GUARDIAN UBUNTU v{__version__}")
    print(" Diagnostics · Monitoring · Freeze Evidence · Zabbix 7")
    print("=" * 70)

    try:
        PCGuardian(cfg, logger).run()
    except KeyboardInterrupt:
        logger.info("PC Guardian detenido por el usuario.")


if __name__ == "__main__":
    main()
