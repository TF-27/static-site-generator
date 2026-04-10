


class HTMLNode():
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def __repr__(self):
        return f"tag: {self.tag}\n value: {self.value}\n children: {self.children}\n props: {self.props}"

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if self.props == None:
            return ""
        fstring = ""
        for key in self.props:
            fstring += f' {key}="{self.props[key]}"'
        return fstring


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        self.super = HTMLNode
        self.tag = tag
        self.value = value
        self.props = props

    def __repr__(self):
        return f"tag: {self.tag}\n value: {self.value}\n props: {self.props}"

    def to_html(self):
        if self.value is None:
            raise ValueError("None or no value provided")
        if self.tag == None:
            return f"{self.value}"
        if self.props == None:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        self.super = HTMLNode
        self.tag = tag
        self.children = children
        self.props =  props

    def __repr__(self):
        return f"tag: {self.tag}\n children: {self.children}\n props: {self.props}"

    def to_html(self):
        if self.tag == None:
            raise ValueError("provide a valid tag")
        if self.children == None:
            raise ValueError("provide at least one valid child")
        html_string = f"<{self.tag}>"
        for child in self.children:
            html_string += child.to_html()
        html_string += f"</{self.tag}>"
        return html_string
