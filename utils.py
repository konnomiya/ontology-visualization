from rdflib import URIRef
from collections import namedtuple
from rdflib.namespace import Namespace


SCHEMA = Namespace('http://schema.org/')


class Colors:
    cls = '#1f77b4'
    lit = '#ff7f0e'
    ins = '#e377c2'
    filled = True


class Config:
    def __init__(self, config_file=None):
        self.blacklist = set()
        self.class_inference_in_object = set()
        self.property_inference_in_object = set()
        self.max_label_length = 0
        self.colors = Colors()
        if config_file:
            self.read_config_file(config_file)

    def read_config_file(self, config_file):
        import json
        with open(config_file) as f:
            config = json.load(f)
            self.blacklist = {URIRef(x) for x in config.get('blacklist', [])}
            self.class_inference_in_object = {URIRef(x) for x in config.get('class_inference_in_object', [])}
            self.property_inference_in_object = {URIRef(x) for x in config.get('property_inference_in_object', [])}
            self.max_label_length = int(config.get('max_label_length', 0))
        if 'colors' in config:
            config_color = ConfigColor()
            colors = config['colors']
            self.colors.cls = config_color.parse(colors.get('class', self.colors.cls))
            self.colors.lit = config_color.parse(colors.get('literal', self.colors.cls))
            self.colors.ins = config_color.parse(colors.get('instance', self.colors.cls))
            self.colors.filled = colors.get('filled', True)


class UndefinedColorError(Exception):
    pass


class ConfigColor:
    default_color_map = {
        'y': '#ffff00',  # yellow
        'yellow': '#ffff00',
        'm': '#ff00ff',  # magenta
        'magenta': '#ff00ff',
        'c': '#00ffff',  # cyan
        'cyan': '#00ffff',
        'r': '#ff0000',  # red
        'red': '#ff0000',
        'g': '#00ff00',  # green
        'green': '#00ff00',
        'b': '#0000ff',  # blue
        'blue': '#0000ff',
        'w': '#ffffff',  # white
        'white': '#ffffff',
        'k': '#000000',  # black
        'black': '#000000',
    }

    def parse(self, s):
        if s.startswith('#'):
            return s
        if s in self.default_color_map:
            return self.default_color_map[s]
        else:
            raise UndefinedColorError("UndefinedColorError: %s isn't defined.", s)
