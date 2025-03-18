import os
import re
import subprocess


def buildFile(source: str, fileName: str):
	for _ in range(2):
		subprocess.run(
			[
				"pdflatex",
				"-interaction=nonstopmode",
				"-halt-on-error",
				"-output-directory=../leesmateriaal",
				f"-jobname={fileName:s}",
				source,
			],
			shell = False
		)


if __name__ == "__main__":
	
	assert os.path.split(os.getcwd())[-1] == "broncode", "Please run this script from the broncode directory"

	buildFile("main.tex", f"main")

	with open("main.tex", 'r') as main:
		mainContent = main.read()
		head, body, tail = mainContent.split("%%TOPICS", 2)

		cheatSheets = []

		i = 0
		for match in re.findall(
			re.compile(r"\\input\{([^}]+)\}"),
			body
		):
			with open(match, 'r') as topic:
				topicName = os.path.splitext(
					os.path.split(match)[-1]
				)[0]

				topicContent = topic.read()

				cheatSheets.append(
					(
						topicName,
						topicContent.split("%%CHEAT_SHEET_START", 1)[1]
					)
				)
				
				with open("tmp.tex", 'w') as source:
					source.write(head + topicContent + tail)

				buildFile("tmp.tex", f"{i:02d}_{topicName:s}")
			
			i += 1
		
		with open("tmp.tex", 'w') as source:
			source.write(head)
			source.write("\\renewcommand{\\thesubsection}{\\arabic{subsection}}\n")
			source.write("\\section*{Python Cheat Sheet}\n")
			for topicName, content in cheatSheets:
				source.write(f"\\subsection{{{topicName.replace('_', ' ').capitalize():s}}}\n")
				source.write(f"{content:s}\n")
			source.write(tail)

		buildFile("tmp.tex", f"cheat_sheet")