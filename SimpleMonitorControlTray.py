import smct_pkg.config as config
import smct_pkg.tray as tray


# TODO add selection of monitor at startup
# TODO clean up imports like so:
# import smct_pkg.config


def main():
    config.read_config()
    tray.init_tray()


if __name__ == "__main__":
    main()
