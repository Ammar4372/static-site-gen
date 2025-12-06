class HTMLNode:
    def __init__(
        self,
        tag=None,
        value=None,
        children=None,
        props=None,
    ) -> None:
        self.tag = tag
        self.value = value
        self.props = props
        self.children = children

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self) -> str:
        if self.props:
            html_props = " "
            for prop in self.props:
                html_props += f'{prop}="{self.props[prop]}" '
            return html_props.rstrip(" ")
        return ""

    def __repr__(self) -> str:
        if self.tag:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        return f"{self.value}"


class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None) -> None:
        if value == None:
            raise ValueError("Leaf Node requires value")
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.tag:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        return f"{self.value}"


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag=None,
        children=None,
        props=None,
    ) -> None:
        if tag == None:
            raise ValueError("tag is required")
        if children == None or type(children) != list:
            raise ValueError("either no child is provided or children are not a list")
        super().__init__(tag, None, children, props)

    def to_html(self):
        node = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            if type(child) == LeafNode or type(child) == ParentNode:
                node += child.to_html()
            else:
                raise ValueError(f"{child} is not a htmlnode")
        node += f"</{self.tag}>"
        return node
