from src.request import sender


def before_all(context):
    sender.clean()


def before_scenario(scenario, context):
    print("before_scenario")


def after_scenario(scenario, context):
    print("after_scenario")


def after_all(content):
    sender.clean()
