import ast
import os
import sys

class CodeQualityAnalyzer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.score = 100  # Սկզբնական գնահատական
        self.issues = []
        self.loc = 0      # Lines of Code
        self.complexity = 0

    def analyze(self):
        """Հիմնական ֆունկցիան, որը կատարում է վերլուծությունը"""
        if not os.path.exists(self.file_path):
            return "Ֆայլը չի գտնվել"

        with open(self.file_path, "r", encoding="utf-8") as f:
            source_code = f.read()
            self.loc = len(source_code.splitlines())

        try:
            tree = ast.parse(source_code)
        except SyntaxError as e:
            return f"Սինտաքսի սխալ: {e}"

        # Կատարել ստուգումներ
        self._check_imports(tree)
        self._check_function_lengths(tree)
        self._check_class_names(tree)
        self._calculate_complexity(tree)
        
        return self._generate_report()

    def _check_imports(self, tree):
        """Ստուգում է իմպորտները (օրինակ՝ չօգտագործել wildcard imports *)"""
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                for name in node.names:
                    if name.name == '*':
                        self.issues.append(f"Տող {node.lineno}: Խուսափեք 'from module import *' օգտագործելուց (-5 միավոր)")
                        self.score -= 5

    def _check_function_lengths(self, tree):
        """Ստուգում է ֆունկցիաների երկարությունը"""
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func_len = node.end_lineno - node.lineno
                if func_len > 20: # Եթե ֆունկցիան 20 տողից երկար է
                    self.issues.append(f"Տող {node.lineno}: Ֆունկցիան '{node.name}' շատ երկար է ({func_len} տող) (-2 միավոր)")
                    self.score -= 2

    def _check_class_names(self, tree):
        """Ստուգում է, որ դասերը սկսվեն մեծատառով (CamelCase)"""
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                if not node.name[0].isupper():
                    self.issues.append(f"Տող {node.lineno}: Class '{node.name}' պետք է սկսվի մեծատառով (-3 միավոր)")
                    self.score -= 3

    def _calculate_complexity(self, tree):
        """Հաշվարկում է պարզունակ ցիկլոմատիկ բարդությունը"""
        # Հաշվում ենք ճյուղավորումները (if, for, while)
        complexity_points = 0
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.For, ast.While, ast.ExceptHandler)):
                complexity_points += 1
        
        self.complexity = complexity_points
        if complexity_points > 10:
             self.issues.append(f"Կոդի բարդությունը շատ բարձր է ({complexity_points}) (-10 միավոր)")
             self.score -= 10

    def _generate_report(self):
        """Վերջնական հաշվետվության ձևավորում"""
        if self.score < 0: self.score = 0
        
        report = "=" * 40 + "\n"
        report += f"ԿՈԴԻ ՈՐԱԿԻ ՀԱՇՎԵՏՎՈՒԹՅՈՒՆ: {self.file_path}\n"
        report += "=" * 40 + "\n"
        report += f"Ընդհանուր տողեր (LOC): {self.loc}\n"
        report += f"Բարդության աստիճան: {self.complexity}\n"
        report += f"Վերջնական գնահատական: {self.score}/100\n\n"
        
        report += "Հայտնաբերված խնդիրներ:\n"
        if not self.issues:
            report += "   Խնդիրներ չեն հայտնաբերվել: Գերազանց կոդ:\n"
        else:
            for issue in self.issues:
                report += f" - {issue}\n"
        
        return report

# Ծրագրի գործարկման օրինակ
if __name__ == "__main__":
    # Ստեղծում ենք թեստային ֆայլ ստուգման համար
    test_code = """
import os
from math import * 

def very_long_function():
    print('start')
    # Սա արհեստականորեն երկարացված ֆունկցիա է
    x = 1
    if x == 1:
        print(1)
    if x == 1:
        print(1)
    if x == 1:
        print(1)
    if x == 1:
        print(1)
    if x == 1:
        print(1)
    if x == 1:
        print(1)
    if x == 1:
        print(1)
    if x == 1:
        print(1)
    if x == 1:
        print(1)
    if x == 1:
        print(1)
    if x == 1:
        print(1)
    if x == 1:
        print(1)
    print('end')

class myBadNamedClass:
    pass
    """
    
    with open("test_script.py", "w", encoding="utf-8") as f:
        f.write(test_code)

    # Սկսում ենք ստուգումը
    analyzer = CodeQualityAnalyzer("test_script.py")
    result = analyzer.analyze()
    print(result)
