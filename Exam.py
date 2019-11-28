class Exam:
    def __init__(self, text, a, b, c, d, answer):
        self.Text = text
        self.A = a
        self.B = b
        self.C = c
        self.D = d
        self.Answer = answer

    def show(self):
        print(self.Text + "\n")
        print("A." + self.A + "\n")
        print("B." + self.B + "\n")
        print("C." + self.C + "\n")
        print("D." + self.D + "\n")

    def to_json(self):
        return {"Text": self.Text,
                "A": self.A,
                "B": self.B,
                "C": self.C,
                "D": self.D,
                "Answer": self.Answer}