"""

    Copyright (C) 2025 Software
    Credits to Hazret Hasanov 


    NOTE: ALL THE CLASSES BELOW ASSUMES THAT GIVEN INPUT IS FROM SIMPLIFIED ABSTRACT SYNTAX TREE!
    DO NOT TRY CALL THEM BY RANDOM EXPRESSIONS!
    AND PLEASE DO NOT MODIFY THE CODE!

"""

from copy import copy
from itertools import chain

AndCombined = False

class true_obj:
    def __init__(self):
        pass 

    def __repr__(self):
        return '1'

    def __str__(self):
        return '1'
    
    def to_str(self): 
        return '1'
    
    def __mul__(self,other): 
        if isinstance(other,CE) or  isinstance(other,AndExpr) or isinstance(other,true_obj) or isinstance(other,false_obj):
            return other 
        raise ValueError("Not suitable for multiplication of true_obj with other!")

    def copy(self):
        return true_obj()

class false_obj:
    def __init__(self):
        pass 

    def __str__(self):
        return '0'
    
    def to_str(self):
        return '0'
    
    def __repr__(self):
        return '0'
    
    def __mul__(self,other):
        if isinstance(other,CE) or  isinstance(other,AndExpr) or isinstance(other,true_obj) or isinstance(other,false_obj):
            return self
        raise ValueError("Not suitable for multiplication of false_obj with other!")
    
    def copy(self):
        return false_obj()

class CE: 
    def __init__(self,sym,is_not):
        self.symbol = sym
        self.negotation = is_not
        self.string = self.to_str()

    def __eq__(self, value): # SUCCESS 
        return self.symbol == value.symbol and self.negotation == value.negotation
    
    def __hash__(self):
        return hash(self.to_str())
    
    def __mul__(self,other): # AND IS DEFINED 
        if isinstance(other,CE): 
            if self == other: 
                return self
            elif self.is_negotated_of_this(other): 
                return false_obj()
            else: 
                return AndExpr([self,other])
            
        elif isinstance(other,AndExpr): 
            if other.contains(self): 
                return other
            elif other.contains(self.negotate()): 
                return false_obj()
            else: 
                return AndExpr([*other.ls, self])
            
        elif isinstance(other,false_obj): 
            return false_obj()
        
        elif isinstance(other,true_obj): 
            return self 
        
        else: 
            print("The method is not defined for interaction with this object!")

    def __str__(self): # SUCCESS
        return self.string

    def is_negotated_of_this(self,other): # SUCCESS 
        return self.symbol == other.symbol and self.negotation == (not other.negotation)
    
    def negotate(self): # SUCCESS  
        return CE(self.symbol,not self.negotation)
    
    def to_str(self): # SUCCESS
        return (self.symbol if (not self.negotation) else '!'+self.symbol)
    
    def copy(self): 
        return CE(self.symbol,self.negotation)
    
    def __add__(self,other): # OR IS DEFINED
        if isinstance(other,CE): 
            if self == other: # A + A = A
                return self 
            elif self.is_negotated_of_this(other): 
                return true_obj() # A + !A = 1 
            else: 
                return OrExpr([self,other])
        elif isinstance(other, true_obj):  # A + 1 = 1
            return true_obj 
        elif isinstance(other,false_obj): # A + 0 = A
            return self 
        elif isinstance(other, AndExpr): # A + AndExpr
            if other.contains(self): 
                return self
            elif other.contains(self.negotate()): 
                other.delete_item(self.negotate())
                return OrExpr([self, other]) 
            return OrExpr([self,other])
        else: 
            raise ValueError("Add(A.K.A logical or) is not defined for Constant Expr and other object!")
    
class OrExpr: 
    def __init__(self, ls):
        self.ls = ls
        if len(list(filter(lambda x: isinstance(x,CE) or isinstance(x,AndExpr),self.ls))) != len(self.ls): 
            raise ValueError("Construction of OrExpr not only AndExprs and CEs!")

    def combine(self, AE): 
        for i in range(len(self.ls)): 
            if isinstance(self.ls[i],CE): 
                self.ls[i] = AndExpr([self.ls[i],*AE.ls])
            elif isinstance(self.ls[i],AndExpr): 
                self.ls[i] = AndExpr([*self.ls[i].ls,*AE.ls])

    def to_str(self):
        result = ""
        for i in self.ls: 
            result += (i.to_str() + "+")
        result = result.strip('+')
        return result 

    def __str__(self):
        return self.to_str()
    
    def copy(self):
        return OrExpr(copy(self.ls))
    
class AndExpr: 

    def __init__(self,ls):
        self.ls = ls
        self.string = self.to_str()

    def contains(self,ce) -> bool:  # SUCCESS!  
        if not isinstance(ce,CE): 
            print("Error! Call of contains with non-CE object!")
            return
        for i in self.ls: 
            if i == ce: 
                return True
        return False 
    
    def delete_item(self,ce): 
        for i in range(len(self.ls)): 
            if self.ls[i] == ce: 
                del self.ls[i]
                return 

    def to_str(self):
        res = "" 
        for i in self.ls: 
            res += i.to_str()
            res += '*'
        res = '*'.join(sorted(res.strip('*').split('*')))
        return res
    
    def __str__(self):
        return self.string
    
    def __mul__(self, other):
        if isinstance(other, CE):
            return (other * self)
        elif isinstance(other,true_obj):
            return self
        elif isinstance(other, false_obj): 
            return false_obj()
        elif isinstance(other,AndExpr): 
            return AndExpr([*self.ls , *other.ls])
        else:
            raise ValueError("Multiplication(A.K.A. logical and) is not defined AndObj and other!")
        
    def __eq__(self, value):
        if isinstance(value,AndExpr):
            size = 0 
            if len(self.ls) != len(value.ls): 
                return False
            for i in self.ls:   
                if value.contains(i): 
                    size+=1
            if size == len(self.ls): 
                return True
            return False
        # elif isinstance(value,CE): 
        #     if len(self.ls) != 1: 
        #         return False
        #     else: 
        #         return (self.ls[0] == value) 
        return False
    
    def __hash__(self):
        str1 = self.to_str()
        str1 = ('').join(sorted(str1))
        return hash(str1)

    def is_castable(self):
        return len(self.ls) == 1
             
    def cast(self):
        return self.ls[0]

    def __add__(self, other): 

        global AndCombined

        if isinstance(other,CE): 
            return (other + self)
        elif isinstance(other,false_obj):
            return self 
        elif isinstance(other,true_obj): 
            return true_obj()
        elif isinstance(other,AndExpr): 
            expr2 = self.extract_same(other)  # AndExpr
            if len(expr2.ls) == 0: 
                return OrExpr([self,other]) # If there is nothing common, return OrExpr 
            # that combines them
            ls1 = list(filter(lambda x : not x in expr2.ls, self.ls))
            ls2 = list(filter(lambda x : not x in expr2.ls, other.ls))
            obj1 = None 
            obj2 = None 

            if len(ls1) == 1: 
                obj1 = ls1[0]
            elif len(ls1) == 0: 
                return expr2
            else: 
                obj1 = AndExpr(ls1)
            if len(ls2) == 1: 
                obj2 = ls2[0]
            elif len(ls2) == 0: 
                return expr2 
            else: 
                obj2 = AndExpr(ls2)
            
            if isinstance(obj1,CE): 
                result = obj1 + obj2 
                if isinstance(result,OrExpr):
                    # DELETE HERE AFTER FIX IF DOES NOT WORK <----------------------------
                    AndCombined = True
                    result.combine(expr2)
                    return result
                else: 
                    expr2  = (expr2*result)
                    return expr2

            elif isinstance(obj2,CE): 
                result = obj2 + obj1 
                if isinstance(result,OrExpr):
                    # DELETE HERE IF NEEDED TOO 
                    AndCombined = True
                    result.combine(expr2)
                    return result 
                else: 
                    expr2  = (expr2*result)  
                    return expr2
            else: 
                return OrExpr([self, other])
            
        else: 
            raise ValueError("Addition(A.K.A. logical or) is not defined for AndExpr and other!")
        

    def extract_same(self, other): 
        ls = []
        for i in self.ls: 
            if other.contains(i): 
                ls.append(i)
        return AndExpr(ls)
    
    def copy(self):
        return AndExpr(copy(self.ls))
    
    def get_different_negotated_str(self,other): 
        same = self.extract_same(other)
        different_negotation = [i.negotate() for i in chain(self.ls, other.ls) if i not in same.ls]
        return AndExpr(different_negotation).to_str()
    
    def is_double(self):
        return len(self.ls) == 2

    

class SAST: 

    def __init__(self, ls):
        self.ls = ls
        self.simplified = self.simplify()

    def simplify(self): 

        if len(self.ls) == 0 : 
            return ""
        elif len(self.ls) == 1: 
            if isinstance(self.ls[0], true_obj): 
                return '1'
            elif isinstance(self.ls[0],false_obj): 
                return '0'
        
        is_simplified = False
        while not is_simplified: 
            #breakpoint()
            result_ls = []
            old_size = len(self.ls)
            is_changed = [False for i in range(old_size)]

            for i in range(old_size): 
                if is_changed[i]: 
                    continue
                for j in range(i+1,old_size): 
                    result = self.ls[i].copy() + self.ls[j].copy()
                    if isinstance(result,OrExpr):
                        if  result.ls[0] == self.ls[i] and result.ls[1] == self.ls[j]:
                            # it remained unchanged!
                            continue
                        else:
                            is_changed[i] = True 
                            is_changed[j] = True
                            if isinstance(result.ls[0],AndExpr) and result.ls[0].is_castable():
                                result.ls[0] = result.ls[0].cast()
                            if isinstance(result.ls[1],AndExpr) and result.ls[1].is_castable():
                                result.ls[1] = result.ls[1].cast()
                            result_ls += result.ls
                            break
                    else: 
                        is_changed[i] = True 
                        is_changed[j] = True
                        if isinstance(result,AndExpr) and result.is_castable():
                            result = result.cast()
                        result_ls.append(result)
                        break

            # EDIT STARTED HERE
            # for i in range(len(result_ls)):
            #     if isinstance(result_ls[i],AndExpr) and result_ls[i].is_castable():
            #         result_ls[i] = result_ls[i].cast()

            if is_changed.count(False)==len(is_changed): 
                break

            filtered = []
            for i in range(old_size): 
                if not is_changed[i]: 
                    filtered.append(self.ls[i])

            self.ls = result_ls + filtered
            
        
        str_out = ""
        for i in self.ls: 
            str_out += (i.to_str() + '+')
        str_out = str_out.strip('+')
        return str_out

def generateAnd(string): 
    out = string.split('*')
    ls = []
    for i in out: 
        if i[0] == '!': 
            ls.append(CE(i[1],True))
        else: 
            ls.append(CE(i[0],False))
    return AndExpr(ls)

class ExtendedSAST: 

    def __init__(self, input):
        self.doubles = []
        self.doubles_prev = []
        self.simplified = self.simplify(input)

    def simplify(self,out):

        global AndCombined

        out = out.split('+')
        
        ls = [generateAnd(i) for i in out]
        for i in range(len(ls)):
            if ls[i].is_castable():
                ls[i] = ls[i].cast()
        self.register_doubles(ls)

        fully_simplified = False 
        while not fully_simplified: 

            result_ls = []
            old_size = len(ls)
            is_changed = [False for i in range(old_size)] 

            for i in range(old_size): 
                if is_changed[i]: 
                    continue
                for j in range(i+1,old_size): 
                    result = ls[i].copy() + ls[j].copy()
                    if isinstance(result,OrExpr):

                        if AndCombined: 
                            AndCombined = False 
                            if isinstance(ls[i], AndExpr) and isinstance(ls[j], AndExpr):
                                different_negotated = ls[i].get_different_negotated_str(ls[j])
                                if self.doubles_prev.count(different_negotated) >= 1:
                                    self.doubles_prev.remove(different_negotated) 
                                    is_changed[i] = True 
                                    is_changed[j] = True 
                                    out = ls[i].extract_same(ls[j])
                                    if out.is_castable(): 
                                        out = out.cast()
                                    result_ls.append(out)
                                    break 

                        if  result.ls[0] == ls[i] and result.ls[1] == ls[j]:
                            # it remained unchanged!
                            continue
                        else:
                            is_changed[i] = True 
                            is_changed[j] = True
                            if isinstance(result.ls[0],AndExpr):
                                if result.ls[0].is_castable():
                                    result.ls[0] = result.ls[0].cast()
                                elif result.ls[0].is_double():
                                    self.doubles.append(result.ls[0].to_str())

                            if isinstance(result.ls[1],AndExpr): 
                                if result.ls[1].is_castable():
                                    result.ls[1] = result.ls[1].cast()
                                elif result.ls[1].is_double(): 
                                    self.doubles.append(result.ls[1].to_str())
                            
                            result_ls += result.ls
                            break
                    else: 
                        is_changed[i] = True 
                        is_changed[j] = True
                        if isinstance(result,AndExpr):
                            if result.is_castable():
                                result = result.cast()
                            elif result.is_double():
                                self.doubles.append(result.to_str())

                        result_ls.append(result)
                        break
            
            if is_changed.count(False)==len(is_changed): 
                break

            filtered = []
            for i in range(old_size): 
                if not is_changed[i]: 
                    filtered.append(ls[i])

            self.doubles_prev = copy(self.doubles)
            self.doubles = []
            ls = result_ls + filtered

        
        str_out = ""
        for i in ls: 
            str_out += (i.to_str() + '+')
        str_out = str_out.strip('+')
        return str_out



    def register_doubles(self,ls):
        for i in ls: 
            if isinstance(i,AndExpr) and len(i.ls) == 2:
                self.doubles_prev.append(i.to_str())


