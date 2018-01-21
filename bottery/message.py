import os
from datetime import datetime

import attr
from jinja2 import Environment, FileSystemLoader, select_autoescape


@attr.s
class Message:
    id = attr.ib()
    platform = attr.ib()
    user = attr.ib()
    chat = attr.ib()
    text = attr.ib()
    timestamp = attr.ib()
    raw = attr.ib()

    @property
    def datetime(self):
        return datetime.utcfromtimestamp(self.timestamp)


def render(message, template_name, context={}):
    base_dir = os.path.join(os.getcwd(), 'templates')
    paths = [base_dir]
    # Include paths on settings
    # paths.extend(settings.TEMPLATES)

    env = Environment(
        loader=FileSystemLoader(paths),
        autoescape=select_autoescape(['html']))

    template = env.get_template(template_name)

    default_context = {
        'user': message.user,
        'platform': message.platform,
    }
    default_context.update(context)
    return template.render(**default_context)
