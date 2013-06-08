help:  # 顯示命令列
	@cat Makefile | grep -e '^\(\w*\):' | sed -e 's/^\(\w*\):.*#\(.*\)/make \1 \t #\2/g'

setup: # 安裝 dependencies
	test -d _logs || mkdir _logs
	test -d 3rd || mkdir 3rd
	test -d 3rd/wikidot/ || ( cd 3rd; git clone git://github.com/gabrys/wikidot.git )
	test -d 3rd/gdata-python-client/ || ( cd 3rd; hg clone http://code.google.com/p/gdata-python-client/ )

run:   # rebuild 個人頁面
	./h4_wikidot_rebuild 2>&1 | tee _logs/h4_wikidot_rebuild_$$(date "+%Y-%m-%d_%H%M%S").log

log: # 顯示最新產生的 log
	echo $$(find _logs -type f | xargs ls -t | head -1)

logedit: # 編輯最新產生的 log
	$$EDITOR $$(find _logs -type f | xargs ls -t | head -1)

clean: # 清除執行期的暫存檔
	find . -type f -name '*.pyc' -print0 | xargs -0 rm -v

.SILENT: clean
