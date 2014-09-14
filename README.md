# 值日生
    h4_invitation_notifier      發送聚會通知 mail
    h4_wiki_notifier            發送聚會手記 mail

# 大家都可以
    h4_wikidot_indexing         更新內容頁列表 
    h4_wikidot_page_creater     建立聚會手記 wiki 頁面
    h4_wikidot_rebuild          Parse 聚會手記，然後整理成個人筆記紀錄

# deprecated
    h4_etherpad_notifier        提醒 etherpad 有變更

# Install
將 dot.h4notifier.ini 編輯修改 USERNAME, PASSWORD，...等參數後，複製到 $HOME/.h4notifier.ini

## Ubuntu
```
apt-get install python-pip mercurial
pip install -r requirements.txt
```

# Reference
http://www.aaronsw.com/2002/diff/