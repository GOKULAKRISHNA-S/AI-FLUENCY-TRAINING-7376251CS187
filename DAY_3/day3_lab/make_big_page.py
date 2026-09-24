"""Creates big.html: a large page used to trigger the context-overflow failure."""
rows = "\n".join(
    f"<tr><td>Student {n:04d}</td><td>Roll BA{n:04d}</td>"
    f"<td>Attendance {60 + n % 40}%</td><td>Remarks: regular attendance recorded</td></tr>"
    for n in range(1, 3001))

html = f"<html><body><h1>Attendance Register</h1><table>{rows}</table></body></html>"
open("big.html", "w", encoding="utf-8").write(html)
print(f"big.html created: {len(html):,} characters")