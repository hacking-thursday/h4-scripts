help:  # 顯示命令列表
	@cat Makefile | grep -e '^\([[:alpha:]].*\):' | sed -e 's/^\(.*\):.*#\(.*\)/make \1 \t #\2/g'

setup: # 安裝 dependencies
	test -d _logs || mkdir _logs
	test -d 3rd || mkdir 3rd
	test -d 3rd/wikidot/ || ( cd 3rd; git clone git://github.com/gabrys/wikidot.git )
	test -d 3rd/gdata-python-client/ || ( cd 3rd; hg clone http://code.google.com/p/gdata-python-client/ )

run-wiki:   # wididot 之個人頁面 rebuild
	./h4_wikidot_rebuild 2>&1 | tee _logs/h4_wikidot_rebuild_$$(date "+%Y-%m-%d_%H%M%S").log

run-fb:   # 發送 facebook 活動通知
	# ./h4_create_fb_event.py | tee _logs/h4_create_fb_event.py_$$(date "+%Y-%m-%d_%H%M%S").log
	# ./h4_cli --fb invite    | tee _logs/h4_cli_fb_$$(date "+%Y-%m-%d_%H%M%S").log

log: # 顯示最新產生的 log
	echo $$(find _logs -type f | xargs ls -t | head -1)

logedit: # 編輯最新產生的 log
	$$EDITOR $$(find _logs -type f | xargs ls -t | head -1)

clean: # 清除執行期的暫存檔
	find . -type f -name '*.pyc' -print0 | xargs -0 rm -v

.SILENT: clean