import smct_pkg.config as config
import smct_pkg.tray as tray


def main():
    config.read_config()
    tray.init_tray()


if __name__ == "__main__":
    main()
