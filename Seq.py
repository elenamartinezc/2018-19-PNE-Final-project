class Seq():
    def __init__(self,strbase):
        self.strbase = strbase
    def len(self):
        return len(self.strbase)

    def complement(self):
        complementary = ''
        for base in self.strbase:
            if base  == 'A':
                complementary += 'T'
            elif base  == 'T':
                complementary += 'A'
            elif base  == 'C':
                complementary += 'G'
            elif base  == 'G':
                complementary += 'C'
        complementary2 = Seq( complementary)
        return  complementary2

    def reverse(self):
        reverse = self.strbase[::-1]
        reverse2 = Seq(reverse)
        return reverse2

    def count(self, base):
        counting = (self.strbase.count(base))
        return counting


    def perc(self, base):
        length = len(self.strbase)
        percentage = round(((self.strbase.count(base))/length)*100,1)
        return percentage

