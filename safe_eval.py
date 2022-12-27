# safe_eval.py  --  evaluate mathematical expression without risk


import ast
import operator
import math


__all__ = 'SafeEval'


class SafeEval:
    
    @staticmethod
    def valid_math(x, *args):
        if x not in dir(math) and '__' not in x:
            raise SyntaxError(f'Unknown function {x}')
        func = getattr(math, x)
        return func(*args)
    
    
    unary_ops = {   ast.USub:       operator.neg, 
                    ast.UAdd:       operator.pos, 
                    ast.UnaryOp:    ast.UnaryOp, 
                }
    
    binary_ops = {  ast.Add:    operator.add, 
                    ast.Sub:    operator.sub, 
                    ast.Mult:   operator.mul, 
                    ast.Div:    operator.truediv, 
                    ast.Mod:    operator.mod, 
                    ast.Pow:    operator.pow, 
                    ast.Call:   valid_math, 
                    ast.BinOp:  ast.BinOp, 
                 }
    
    ops = tuple(unary_ops) + tuple(binary_ops)
    
    
    @staticmethod
    def evaluate(s):
        tree = ast.parse(s, mode='eval')
        return __class__.new_eval(tree)
    
    ev = evaluate
    
    
    @staticmethod
    def new_eval(node):
        if isinstance(node, ast.Expression):
            return __class__.new_eval(node.body)
        
        elif isinstance(node, ast.Str):
            return node.s
        
        elif isinstance(node, ast.Num):
            return node.value
        
        elif isinstance(node, ast.Constant):
            return node.value
        
        elif isinstance(node, ast.BinOp):
            if isinstance(node.left, __class__.ops):
                left = __class__.new_eval(node.left)
            else:
                left = node.left.value
            
            if isinstance(node.right, __class__.ops):
                right = __class__.new_eval(node.right)
            else:
                right = node.right.value
            
            return __class__.binary_ops[type(node.op)](left, right)
        
        elif isinstance(node, ast.UnaryOp):
            if isinstance(node.operand, __class__.ops):
                operand = __class__.new_eval(node.operand)
            else:
                operand = node.operand.value
            
            return __class__.unary_ops[type(node.op)](operand)
        
        elif isinstance(node, ast.Call):
            args = [__class__.new_eval(x) for x in node.args]
            r = __class__.valid_math(node.func.id, *args)
            return r
        
        else:
            raise SyntaxError(f'Bad syntax, {type(node)}')



if __name__ == '__main__':
    se = SafeEval()
    
    assert se.ev('3 + 4') == 3 + 4
    assert se.ev('1 + -9') == 1 + -9
    assert se.ev('-1') == -1
    assert se.ev('-+1') == -+1
    assert se.ev('(2000 / 10) + 3') == (2000 / 10) + 3
    assert se.ev('100 * (12 + 4)') == 100 * (12 + 4)
    assert se.ev('2 ** 3') == 2 ** 3
    assert se.ev('sqrt(16) + 1') == math.sqrt(16) + 1
    assert se.ev('1.2345 * 10') == 1.2345 * 10
    
    print('All tests passed')

