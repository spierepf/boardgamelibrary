class BehaveLayerStack:
    def __init__(self, *args):
        self._stack = args

    def before_all(self, context):
        for layer in self._stack:
            layer.before_all(context)

    def before_feature(self, context, feature):
        for layer in self._stack:
            layer.before_feature(context, feature)

    def before_scenario(self, context, scenario):
        for layer in self._stack:
            layer.before_scenario(context, scenario)

    def before_step(self, context, step):
        for layer in self._stack:
            layer.before_step(context, step)

    def before_tag(self, context, tag):
        for layer in self._stack:
            layer.before_tag(context, tag)

    def after_tag(self, context, tag):
        for layer in reversed(self._stack):
            layer.after_tag(context, tag)

    def after_step(self, context, step):
        for layer in reversed(self._stack):
            layer.after_step(context, step)

    def after_scenario(self, context, scenario):
        for layer in reversed(self._stack):
            layer.after_scenario(context, scenario)

    def after_feature(self, context, feature):
        for layer in reversed(self._stack):
            layer.after_feature(context, feature)

    def after_all(self, context):
        for layer in reversed(self._stack):
            layer.after_all(context)
