help:  # 顯示命令列
	cat Makefile | grep -e '^\(\w*\):' | sed -e 's/^\(\w*\):.*#\(.*\)/make \1 \t #\2/g'

setup: # 安裝 dependencies
	test -d logs || mkdir logs
	test -d 3rd || mkdir 3rd
	test -d 3rd/wikidot/ || ( cd 3rd; git clone git://github.com/gabrys/wikidot.git )

run:   # rebuild 個人頁面
	./h4_wikidot_rebuild 2>&1 | tee logs/h4_wikidot_rebuild_$$(date "+%Y-%m-%d_%H%M%S").log

log: # 顯示最新產生的 log
	echo $$(find logs -type f | xargs ls -t | head -1)

logedit: # 編輯最新產生的 log
	$$EDITOR $$(find logs -type f | xargs ls -t | head -1)

