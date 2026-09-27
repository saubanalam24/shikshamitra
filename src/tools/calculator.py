import ast
import operator as op

# only the safe stuff, no eval() on raw user text
OPS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
    ast.USub: op.neg,
}


def _eval(node):
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("bad constant")
    if isinstance(node, ast.BinOp) and type(node.op) in OPS:
        return OPS[type(node.op)](_eval(node.left), _eval(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in OPS:
        return OPS[type(node.op)](_eval(node.operand))
    raise ValueError("expression not allowed")


def calculate(expr: str):
    expr = expr.strip().replace("^", "**")
    try:
        tree = ast.parse(expr, mode="eval")
        result = _eval(tree.body)
        return result
    except Exception as e:
        return f"couldn't compute that ({e})"


if __name__ == "__main__":
    print(calculate("2 + 3 * (4 - 1)"))
    print(calculate("10 / 0"))
