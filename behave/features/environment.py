from layers import BehaveLayerStack, ClientLayer, ResetLayer, SeleniumLayer, ServerLayer

behave_layer_stack = BehaveLayerStack(
    ServerLayer(),
    ClientLayer(),
    SeleniumLayer(),
    ResetLayer()
)


def before_all(context):
    behave_layer_stack.before_all(context)


def before_feature(context, feature):
    behave_layer_stack.before_feature(context, feature)


def before_scenario(context, scenario):
    behave_layer_stack.before_scenario(context, scenario)


def before_step(context, step):
    behave_layer_stack.before_step(context, step)


def before_tag(context, tag):
    behave_layer_stack.before_tag(context, tag)


def after_tag(context, tag):
    behave_layer_stack.after_tag(context, tag)


def after_step(context, step):
    behave_layer_stack.after_step(context, step)


def after_scenario(context, scenario):
    behave_layer_stack.after_scenario(context, scenario)


def after_feature(context, feature):
    behave_layer_stack.after_feature(context, feature)


def after_all(context):
    behave_layer_stack.after_all(context)