from core.reader import read_pdf
from core.parser import parse_report
from core.rag import retrieve
from core.generator import generate_recommendation


text = read_pdf("test_report.pdf")

parsed = parse_report(text)

docs = retrieve(parsed)

result = generate_recommendation(parsed, docs)

print("----- RESULT -----")
print(result)