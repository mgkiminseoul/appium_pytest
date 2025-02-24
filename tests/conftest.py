def pytest_addoption(parser):
    parser.addoption(
        "--udid",
        action="store",
        default="default_device",
        help="디바이스 식별자"
    )