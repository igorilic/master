watchdiff:
	inotifywait -qmre close_write ./ --format "%w%f" --exclude diff*|\
		while read f; do \
			git difftex $$f > diff.tex ;\
			pdflatex -synctex=1 -interaction=nonstopmode -halt-on-error -shell-escape master.tex ;\
			killall -HUP mupdf ;\
		done

