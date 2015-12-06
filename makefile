watchdiff:
	inotifywait -qmre close_write ./ --format "%w%f" |\
		while read f; do ;\
			git difftex $$f > master.tex ;\
			pdflatex -synctex=on -interaction=nonstopmode -halt-on-error -shell-escape master.tex ;\
			killall -HUP mupdf ;\
		done

