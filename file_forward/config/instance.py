from file_forward.util import human_split

from .const import APP

class InstanceConfig:

    def __init__(self, named_items, get_context=None):
        """
        :param named_items:
            List of pairs (key, prefix). The key is to a name in the app config
            section and prefix is the prefix to find another section from the
            values in the app config.
        """
        self.named_items = named_items
        self.get_context = get_context

    def __call__(self, cp):
        """
        Return dict of named instances from configparser file.
        """
        context = {}
        if callable(self.get_context):
            context.update(self.get_context())
        result = {}
        for key, prefix in self.named_items:
            instances = named_instances(cp, key, prefix, context)
            result[key] = instances
            context[key] = instances
        return result


def safer_eval(expr, context):
    return eval(expr, {'__builtins__': {}}, context)

def instance_from_section(section, context):
    """
    Instantiate from config section.
    """
    class_ = safer_eval(section['class'], context)
    args = safer_eval(section.get('args', '()'), context)
    kwargs = safer_eval(section.get('kwargs', '{}'), context)
    instance = class_(*args, **kwargs)
    return instance

def named_instances(cp, appkey, prefix, context):
    """
    Split a key's value and find sections to instance from, creating a dict of
    named instances.
    """
    return {
        suffix: instance_from_section(cp[prefix + suffix], context)
        for suffix in human_split(cp[APP][appkey])
    }
