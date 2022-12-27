# example of the use of safe_eval


from safe_eval import SafeEval


se = SafeEval()
result = se.ev('1 + 5 * 6 / 3')
print(result)  # 11.0

