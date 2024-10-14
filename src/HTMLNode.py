


class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}


    def to_html(self):
        raise NotImplementedError("Subclasses must implement to_html() method")
    
    def props_to_html(self):
        #return f"{self.props}"
        return "".join(f' {key}="{value}"' for key, value in self.props.items())
    

    def __repr__(self):
        return f"HTMLNode(tag:{self.tag}, value:{self.value}, children:{self.children}, props:{self.props})"
    



class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        if value is None:
            raise ValueError("LeafNode must have a value.")
        # Call the parent (HTMLNode) constructor with no children (children should always be empty)
        super().__init__(tag=tag, value=value, children=[], props=props)

    def to_html(self):
        # If no tag is provided, return the raw value as plain text
        if self.tag is None:
            return self.value
        
        # Otherwise, render as an HTML tag with the value and props (if any)
        props_html = self.props_to_html()
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return (
            f"LeafNode(tag={self.tag}, value={self.value}, props={self.props})"
        )
    


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        if not tag:
            raise ValueError("ParentNode must have a tag.")
        if not children:
            raise ValueError("ParentNode must have at least one child.")

        # Call the parent constructor
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNode must have a tag.")
        children_html = "".join(child.to_html() for child in self.children)
        props_html = self.props_to_html()
        return f"<{self.tag}{props_html}>{children_html}</{self.tag}>"

    def __repr__(self):
        return (
            f"ParentNode(tag={self.tag}, children={self.children}, props={self.props})"
        )