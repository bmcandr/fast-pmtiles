import os


def pytest_generate_tests(metafunc):
    os.environ["AWS_REGION"] = "us-west-2"
    os.environ["AWS_SKIP_SIGNATURE"] = "True"
