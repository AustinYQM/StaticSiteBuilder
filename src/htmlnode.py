from typing import List


class HTMLNode:
    def __init__(self, tag: str = None, value: str = None, children: List = None, props: dict = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        prop_string = ""
        for key, value in self.props.items():
            prop_string += f' {key}="{value}"'
        return prop_string

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props_to_html()})"
