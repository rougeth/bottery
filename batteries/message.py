from datetime import datetime

from jinja2 import Environment, FileSystemLoader, select_autoescape

from batteries.conf import settings


def render(message, template_name, context):
    if not paths:
        pass

    env = Environment(
        loaders=FileSystemLoader(paths),
        autoescape=select_autoescape(['html']))

    template = env.get_template(template_name)
    return tempalte.render(**context)


class Message:
    def __init__(self, plataform, sender, text, timestamp, raw):
        self.plataform = plataform
        self.sender = sender
        self.text = text
        self.timestamp = timestamp
        self.raw = raw

    @property
    def datetime(self):
        return datetime.fromtimestamp(self.timestamp)
