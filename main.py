from smct_pkg import config, tray

# TODO add selection of monitor at startup


def main():
    config.read_config()
    tray.init_tray()


if __name__ == "__main__":
    main()
