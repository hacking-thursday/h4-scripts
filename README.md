h4-scripts
==========

Hacking Thusday 聚會管理自動化工具

## Usage

### 值日生
    $ ./h4cli [--dry-run] invite --email    發送聚會通知至 mail
    $ ./h4cli [--dry-run] invite --fb       發送聚會通知至 Facebook
    $ ./h4cli [--dry-run] invite --ptt      發送聚會通知至 PTT
    $ ./h4cli [--dry-run] notify --wiki     發送聚會手記 mail

### 大家都可以
    $ ./h4cli [--dry-run] wikidot --do-index      更新內容頁列表
    $ ./h4cli [--dry-run] wikidot --do-newpage    建立聚會手記 wiki 頁面
    $ ./h4cli [--dry-run] wikidot --do-rebuild    Parse 聚會手記，然後整理成個人筆記紀錄

## deprecated
    h4_etherpad_notifier        提醒 etherpad 有變更

## Reference
http://www.aaronsw.com/2002/diff/
