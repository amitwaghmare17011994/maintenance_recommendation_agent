from core.reader import read_pdf
from core.parser import parse_report

text = read_pdf("test_report.pdf")

parsed = parse_report(text)

print("----PARSED----")
print(parsed)