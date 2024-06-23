class ComplexNumber:
    def __init__(self,real_part,imaginary_part):
        self.real_part = real_part
        self.imaginary_part = imaginary_part
    def __str__(self):
        sign = '?'
        if self.imaginary_part <0:
            sign = '-'
        else:
            sign = '+';
        return '{0} {1} {2}*i'.format(self.real_part,sign,abs(self.imaginary_part))
    def __add__(self, other):
        return ComplexNumber(self.real_part+other.real_part,self.imaginary_part+other.imaginary_part);
    def __sub__(self, other):
        return self + ComplexNumber(-other.real_part,-other.imaginary_part);
    def __mul__(self, other):
        return ComplexNumber(self.real_part*other.real_part-self.imaginary_part*other.imaginary_part,self.real_part*other.imaginary_part+self.imaginary_part*other.real_part);

cn = ComplexNumber(1,-2)
dn = ComplexNumber(1,2);
print(cn);
