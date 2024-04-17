from smct_pkg import config, tray


def main():
    config.read_config()
    tray.init_tray()


if __name__ == "__main__":
    main()
