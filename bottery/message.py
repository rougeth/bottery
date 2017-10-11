import os
from datetime import datetime

from jinja2 import Environment, FileSystemLoader, select_autoescape

from bottery.conf import settings


class Message:
    def __init__(self, id, platform, user, text, timestamp, raw):
        self.id = id
        self.platform = platform
        self.user = user
        self.text = text
        self.timestamp = timestamp
        self.raw = raw

    @property
    def datetime(self):
        return datetime.utcfromtimestamp(self.timestamp)


def render(message, template_name, context={}):
    base_dir = os.path.join(os.getcwd(), 'templates')
    paths = [base_dir]
    paths.extend(settings.TEMPLATES)

    env = Environment(
        loader=FileSystemLoader(paths),
        autoescape=select_autoescape(['html']))

    template = env.get_template(template_name)

    default_context = {
        'user': message.user
    }
    default_context.update(context)
    return template.render(**default_context)
