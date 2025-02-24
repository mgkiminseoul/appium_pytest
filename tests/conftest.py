def pytest_addoption(parser):
    parser.addoption(
        "--udid",
        action="store",
        default="default_device",
        help="디바이스 식별자"
    )
"""
conftest.py를 작성하는 대표적인 이유중 하나는 fixture를 이용해 테스트 코드들의 공통된 설정을 중복 코드 없이 conftest.py 내에서 하기 위함입니다.
혹시 코드 내에서 중복된 설정이 있다면 fixture 데코레이터를 활용하는 것을 추천드립니다.
"""
